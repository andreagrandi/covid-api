from db.models import JHDailyReport
from db.database import SessionLocal, engine, Base
from sqlalchemy.orm.exc import NoResultFound
from datetime import datetime, date, timedelta
from requests import Session
from requests.exceptions import HTTPError
from collections import defaultdict
from typing import Optional
import argparse
import csv

parser = argparse.ArgumentParser(description='Import data into the database')
parser.add_argument(
    '--from-date',
    metavar='DATE',
    type=date.fromisoformat,
    default=date(year=2020, month=2, day=29),
    help='date to start importing from (default: 2020-02-29)'
)
parser.add_argument("--all", help="import all the available data", action="store_true")
parser.add_argument("--latest", help="import last couple of days of data", action="store_true")


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
            if '\ufeffProvince/State' in record:
                # 2020-03-13 includes this invisible character, which messed up the column names
                # see https://github.com/CSSEGISandData/COVID-19/pull/1738
                record['Province/State'] = record['\ufeffProvince/State']

            records.append(record)

        return records


def deduplicate(db_instance, to_deduplicate):
    """
    Try to remove suspected duplicate reports from the session
    """
    for duplicates in to_deduplicate.values():
        duplicates.sort(key=lambda dr: dr.confirmed, reverse=True)
        first = duplicates[0]
        for other in duplicates[1:]:
            print(f'Deduplicating:\n\t- {first!r}\n\t- {other!r}')

            if other.confirmed == 0 and other.deaths == 0 and other.recovered == 0:
                print('\t-> Ignoring duplicate with zero cases, deaths and recovered')
                db_instance.expunge(other)
            else:
                raise Exception('Duplicate records have different numbers. Giving up.')


def get_daily_report_by_region_and_date(
        db: SessionLocal, country_region: str,
        province_state: Optional[str],
        fips: Optional[str],
        admin2: Optional[str], last_update: datetime) -> JHDailyReport:
    """
    Get a single daily report from the db by matching some kind of region and the date.

    Note that province_state is null for some values of country_region.
    admin2 and fips were added to the reports later on, so they may be null.
    FIPS is a code that uniquely identifies a region in the US, whereas admin2
    is a place name that needs to be used in conjunction with country_region
    and province_state.
    """
    if fips:
        dr = db.query(JHDailyReport).filter(
            JHDailyReport.fips == fips,
            JHDailyReport.last_update == last_update
        )
    elif province_state and admin2:
        dr = db.query(JHDailyReport).filter(
            JHDailyReport.province_state == province_state,
            JHDailyReport.country_region == country_region,
            JHDailyReport.admin2 == admin2,
            JHDailyReport.fips.is_(None),
            JHDailyReport.last_update == last_update
        )
    elif province_state:
        dr = db.query(JHDailyReport).filter(
            JHDailyReport.fips.is_(None),
            JHDailyReport.admin2.is_(None),
            JHDailyReport.province_state == province_state,
            JHDailyReport.country_region == country_region,
            JHDailyReport.last_update == last_update
        )
    else:
        dr = db.query(JHDailyReport).filter(
            JHDailyReport.fips.is_(None),
            JHDailyReport.admin2.is_(None),
            JHDailyReport.province_state.is_(None),
            JHDailyReport.country_region == country_region,
            JHDailyReport.last_update == last_update
        )

    return dr.one()


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


def clean_optional_field(original: Optional[str]) -> Optional[str]:
    return original if original else None


def sanity_check(db_instance):
    """
    Run some checks on the database before we commit
    """
    if db_instance.execute('''
        select 1
        from daily_reports
        where fips is not null
        group by fips, last_update
        having count(*) > 1
        ''').fetchone():
        db_instance.rollback()
        raise Exception(f'Found records with the same FIPS and last_update')

    print('Unique FIPS codes ✅')

    if db_instance.execute('''
        select 1
        from daily_reports
        where fips is null
        group by country_region, province_state, admin2, last_update
        having count(*) > 1
        ''').fetchone():
        db_instance.rollback()
        raise Exception(f'Found records with the same country_region, province_state, admin2, last_update and no FIPS')

    print('Unique admin2/province_state/country_region records ✅')


def import_daily_report(report):
    db_instance = SessionLocal()
    to_deduplicate = defaultdict(list)

    for row in report:
        last_update_str = row.get('Last Update') or row['Last_Update']
        last_update = datetime.fromisoformat(last_update_str)

        # Region identifiers
        country_region = row.get('Country_Region') or row['Country/Region']
        province_state = row.get('Province_State') or row.get('Province/State')
        admin2 = row.get('Admin2')
        fips = row.get('fips')

        province_state = clean_optional_field(province_state)
        fips = clean_optional_field(fips)
        admin2 = clean_admin2(admin2)

        # Measures
        confirmed = int(row['Confirmed'])
        deaths = int(row['Deaths'])
        recovered = int(row['Recovered'])

        try:
            dr = get_daily_report_by_region_and_date(
                db=db_instance,
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
            )
        except Exception:
            print(f'Invalid row: {row!r}')
            raise
        else:
            if dr.confirmed > confirmed or dr.deaths > deaths or dr.recovered > recovered:
                print(f'Warning: NOT lowering estimates for {dr!r}')
                print(f'New data: confirmed={confirmed}, deaths={deaths}, recovered={recovered}')
                continue
            else:
                dr.confirmed = confirmed
                dr.deaths = deaths
                dr.recovered = recovered

        db_instance.add(dr)

        # Track potentially duplicated admin2s
        if dr.admin2 in DUPLICATE_ADMIN2.values():
            to_deduplicate[dr.admin2].append(dr)

    try:
        deduplicate(db_instance, to_deduplicate)
    except Exception:
        print(f'Cannot deduplicate day {last_update_str}')

    db_instance.flush()
    sanity_check(db_instance)
    db_instance.commit()


if __name__ == "__main__":
    args = parser.parse_args()

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

    while current <= today:
        if current == date(year=2020, month=3, day=22):
            # Skip this report for now,
            # this commit changed the timestamp format, and apparently added duplicates as well
            # https://github.com/CSSEGISandData/COVID-19/commit/f5963e75b11ef35894657c5fd4d96a1690a20696#diff-6b1c9a83928deda4b1f61bf59cd9d68f
            current = current + timedelta(days=1)
            continue

        print(f'Importing data for {current}')

        try:
            report = report_fetcher.fetch_report(current)
            import_daily_report(report)
        except HTTPError:
            if current == today:
                print('Unable to fetch report. It may not be available yet.')
                break
            else:
                print('Unable to fetch report')
                raise

        current = current + timedelta(days=1)
