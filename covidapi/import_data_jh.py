from .db.models import JHDailyReport
from .db.database import SessionLocal, engine, Base
from .services.crud import JHCRUD
from .jh_cleaning.lookup_table import Matcher
from .jh_cleaning.region_info import RegionNames
from .jh_cleaning.clean_columns import clean_extra_whitespace
from .jh_cleaning.util import parse_datetime, clean_optional_field
from sqlalchemy.orm.exc import NoResultFound
from datetime import datetime, date, timedelta
from requests import Session
from requests.exceptions import HTTPError
from collections import defaultdict, Counter
from typing import Optional
import csv


class ImportResult:
    def __init__(self):
        self._unmatched_locations = Counter()
        self._resolved_duplicate_locations = Counter()
        self._unresolved_duplicate_locations = Counter()
        self._matched_records = defaultdict(list)
        self._ignored_regions = Counter()
        self._unexpected_decreases = []
        self._errors = []
        self._warnings = []

    def record_error(self, message):
        self._errors.append(message)

    def record_warning(self, message):
        self._warnings.append(message)

    def record_matched_record(self, jh_id, record):
        """
        Keep track of records that we do match to the lookup table.
        This is used to detect duplicates.
        """
        self._matched_records[jh_id].append(record)

    def record_unmatched_location(self, region_names):
        """
        Record a location that we couldn't match to the lookup table
        """
        self._unmatched_locations[region_names] += 1

    def record_ignored_location(self, region_names):
        """
        Record a location that we're ignoring, for example city-level information, or subgroups
        within a population that have returned from a cruise ship
        """
        self._ignored_regions[region_names] += 1

    def record_resolved_duplicate(self, jh_id):
        """
        Record a duplicate record in the same report that we have been able to de-duplicate
        """
        self._resolved_duplicate_locations[jh_id] += 1

    def record_unexpected_decrease(self, record, confirmed, deaths, recovered):
        """
        This happens when we receive two reports with the same timestamp, but
        different numbers. This happens when revised estimates are reported on different
        days, but the last_updated timestamp has not been changed.

        If this happens, the script always records the higher estimates. This
        ensures we always store 1 report per timestamp, and the script can be rerun
        without changing the result.
        """
        self._unexpected_decreases.append((record, confirmed, deaths, recovered))

    def duplicate_records(self):
        return [records for records in self._matched_records.values() if len(records) > 1]

    def info(self):
        info_list = ['Warning: ' + warning for warning in self._warnings]

        for location in self._unmatched_locations:
            info_list.append(f'Warning: No match found for {location}')

        info_list.extend([
            f'Number of processed locations: {len(self._matched_records)}',
            f'Number of duplicate locations: {len(self.duplicate_records())}',
            f'Number of resolved duplicate locations: {len(self._resolved_duplicate_locations)}',
            f'Number of ignored locations: {len(self._ignored_regions)}',
        ])

        for (record, confirmed, deaths, recovered) in self._unexpected_decreases:
            info_list.append(f'Timestamp has been reused for {record!r} (conflicting report: confirmed={confirmed}, deaths={deaths}, recovered={recovered})')

        return info_list

    def errors(self):
        return self._errors


class ReportFetcher:
    """
    Fetch the raw data from Github
    """
    BASE_URL = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/'

    def __init__(self):
        self.session = Session()

    def fetch_report(self, report_date):
        date_string = report_date.strftime(r'%m-%d-%Y')

        response = self.session.get(f'{self.BASE_URL}{date_string}.csv')
        response.raise_for_status()

        records = []
        for record in csv.DictReader((line.decode('utf8') for line in response.iter_lines())):
            record = clean_extra_whitespace(record)
            records.append(record)

        return records


DUPLICATE_ADMIN2 = {
    'Dona Ana': 'Doña Ana',
    'Elko County': 'Elko',
    'Garfield County': 'Garfield',
    'Walla Walla County': 'Walla Walla',
}


def clean_admin2(original: Optional[str]):
    """
    Some US records are duplicated.
    These have the same FIPS (which should be unique) but slightly
    different admin2 values. See https://github.com/CSSEGISandData/COVID-19/issues/1620

    Normalise these to a single name so we can deduplicate them.
    """
    value = clean_optional_field(original)
    return DUPLICATE_ADMIN2.get(value, value) if value else None


class Importer:
    def __init__(self, matcher):
        self.db_instance = SessionLocal()
        self.matcher = matcher
        self.crud = JHCRUD()

    def _deduplicate(self, result):
        """
        Try to remove suspected duplicate reports from the SQLAlchemy session
        """
        for duplicates in result.duplicate_records():
            duplicates.sort(key=lambda dr: (dr.confirmed, dr.deaths, dr.recovered), reverse=True)
            first = duplicates[0]

            for other in duplicates[1:]:
                pairs = (
                    (first.confirmed, other.confirmed),
                    (first.deaths, other.deaths),
                    (first.recovered, other.recovered)
                )
                if all(lower == 0 or (higher == lower) for (higher, lower) in pairs):
                    result.record_resolved_duplicate(other.jh_id)
                    self.db_instance.expunge(other)
                else:
                    # Conflicting reports for the same place. Choose the highest estimate and print a warning.
                    # Example: Washington/Washington County, Utah, 2020-04-03 22:46:37
                    # https://github.com/CSSEGISandData/COVID-19/blob/master/csse_covid_19_data/csse_covid_19_daily_reports/04-03-2020.csv
                    result.record_warning(f'Ambiguous record {first}: other record has confirmed={other.confirmed}, deaths={other.deaths}, recovered={other.recovered}')
                    self.db_instance.expunge(other)

    def _sanity_check(self, result):
        """
        Run some checks on the database before we commit
        """
        row = self.db_instance.execute('''
            select fips
            from jh_daily_reports
            where fips is not null
            group by fips, last_update
            having count(*) > 1
            ''').fetchone()
        if row:
            result.record_error(f'Found records with the same FIPS and last_update: {row}')

        row = self.db_instance.execute('''
            select jh_id
            from jh_daily_reports
            where jh_id is not null
            group by jh_id, last_update
            having count(*) > 1
            ''').fetchone()
        if row:
            result.record_error(f'Found records with the same jh_id and last_update: {row}')

        row = self.db_instance.execute('''
            select country_region, province_state, admin2, last_update
            from jh_daily_reports
            where fips is null and jh_id is null
            group by country_region, province_state, admin2, last_update
            having count(*) > 1
            ''').fetchone()
        if row:
            result.record_error(f'Found records with the same country_region, province_state, admin2, last_update and no FIPS: {row}')

    def import_daily_report(self, report):
        result = ImportResult()

        for row in report:
            self._import_row(row, result)

        self._deduplicate(result)
        self.db_instance.flush()
        self._sanity_check(result)

        errors = result.errors()
        if errors:
            self.db_instance.rollback()
            for error in errors:
                print(error)
            raise Exception('Unrecoverable errors while importing data.')

        self.db_instance.commit()

        return result

    def _import_row(self, row, result):
        last_update_str = row.get('Last Update') or row['Last_Update']
        last_update = parse_datetime(last_update_str)

        # Region identifiers
        country_region = row.get('Country_Region') or row['Country/Region']
        province_state = row.get('Province_State') or row.get('Province/State')
        admin2 = row.get('Admin2')
        fips = row.get('FIPS')

        province_state = clean_optional_field(province_state)
        fips = clean_optional_field(fips)
        admin2 = clean_admin2(admin2)

        region_names = RegionNames.parse_from_report(row)

        try:
            region_info = self.matcher.match_region(region_names)

            if region_info is None:
                result.record_ignored_location(region_names)
                jh_id = None
            else:
                jh_id = region_info.identified_region.uid
        except KeyError:
            result.record_unmatched_location(region_names)
            region_info = None
            jh_id = None

        # Measures
        confirmed = int(row['Confirmed'])
        deaths = int(row['Deaths'])
        recovered = int(row['Recovered'])

        try:
            dr = self.crud.get_daily_report_by_region_and_date(
                db=self.db_instance,
                province_state=province_state,
                country_region=country_region,
                admin2=admin2,
                fips=fips,
                last_update=last_update
            )
        except NoResultFound:
            dr = JHDailyReport(
                province_state=province_state,
                country_region=country_region,
                admin2=admin2,
                fips=fips,
                last_update=last_update,
                confirmed=confirmed,
                deaths=deaths,
                recovered=recovered,
                jh_id=jh_id
            )
        except Exception:
            print(f'Invalid row: {row!r}')
            raise
        else:
            if dr.confirmed > confirmed or dr.deaths > deaths or dr.recovered > recovered:
                result.record_unexpected_decrease(dr, confirmed, deaths, recovered)
                return
            else:
                dr.confirmed = confirmed
                dr.deaths = deaths
                dr.recovered = recovered

        if jh_id is not None:
            result.record_matched_record(jh_id, dr)

        self.db_instance.add(dr)


def main(args):
    Base.metadata.create_all(engine)

    today = date.today()

    if args.all:
        # Available data starts from 29th February 2020
        current = date.fromisoformat('2020-02-29')
    elif args.latest:
        current = today - timedelta(days=1)
    else:
        current = args.from_date

    report_fetcher = ReportFetcher()
    matcher = Matcher()
    importer = Importer(matcher)

    while current <= today:
        print(f'Importing data for {current}')

        try:
            report = report_fetcher.fetch_report(current)
            result = importer.import_daily_report(report)
            for info in result.info():
                print(info)
        except HTTPError:
            if current == today:
                print('Unable to fetch report. It may not be available yet.')
                break
            else:
                print('Unable to fetch report')
                raise

        current = current + timedelta(days=1)
