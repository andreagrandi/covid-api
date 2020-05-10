from .region_info import RegionNames
from .transform.util import parse_datetime, clean_optional_field
from ..db.models import JHDailyReport
from ..db.database import SessionLocal
from ..services.crud import JHCRUD
from .result import ImportResult
from sqlalchemy.orm.exc import NoResultFound


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
            duplicates.sort(
                key=lambda dr: (dr.confirmed, dr.deaths, dr.recovered), reverse=True
            )
            first = duplicates[0]

            for other in duplicates[1:]:
                pairs = (
                    (first.confirmed, other.confirmed),
                    (first.deaths, other.deaths),
                    (first.recovered, other.recovered),
                )
                if all(lower == 0 or (higher == lower) for (higher, lower) in pairs):
                    result.record_resolved_duplicate(other.jh_id)
                    self.db_instance.expunge(other)
                else:
                    # Conflicting reports for the same place. Choose the highest estimate and print a warning.
                    # Example: Washington/Washington County, Utah, 2020-04-03 22:46:37
                    # https://github.com/CSSEGISandData/COVID-19/blob/master/csse_covid_19_data/csse_covid_19_daily_reports/04-03-2020.csv
                    result.record_warning(
                        f"Ambiguous record {first}: other record has confirmed={other.confirmed}, deaths={other.deaths}, recovered={other.recovered}"
                    )
                    self.db_instance.expunge(other)

    def _sanity_check(self, result):
        """
        Run some checks on the database before we commit
        """
        row = self.db_instance.execute(
            """
            select fips
            from jh_daily_reports
            where fips is not null
            group by fips, last_update
            having count(*) > 1
            """
        ).fetchone()
        if row:
            result.record_error(
                f"Found records with the same FIPS and last_update: {row}"
            )

        row = self.db_instance.execute(
            """
            select jh_id
            from jh_daily_reports
            where jh_id is not null
            group by jh_id, last_update
            having count(*) > 1
            """
        ).fetchone()
        if row:
            result.record_error(
                f"Found records with the same jh_id and last_update: {row}"
            )

        row = self.db_instance.execute(
            """
            select country_region, province_state, admin2, last_update
            from jh_daily_reports
            where fips is null and jh_id is null
            group by country_region, province_state, admin2, last_update
            having count(*) > 1
            """
        ).fetchone()
        if row:
            result.record_error(
                f"Found records with the same country_region, province_state, admin2, last_update and no FIPS: {row}"
            )

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
            raise Exception("Unrecoverable errors while importing data.")

        self.db_instance.commit()

        return result

    def _import_row(self, row, result):
        last_update_str = row.get("Last Update") or row["Last_Update"]
        last_update = parse_datetime(last_update_str)

        # Region identifiers
        country_region = row.get("Country_Region") or row["Country/Region"]
        province_state = row.get("Province_State") or row.get("Province/State")
        admin2 = row.get("Admin2")
        fips = row.get("FIPS")

        province_state = clean_optional_field(province_state)
        fips = clean_optional_field(fips)
        admin2 = clean_optional_field(admin2)

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
        confirmed = int(row["Confirmed"])
        deaths = int(row["Deaths"])
        recovered = int(row["Recovered"])

        try:
            dr = self.crud.get_daily_report_by_region_and_date(
                db=self.db_instance,
                province_state=province_state,
                country_region=country_region,
                admin2=admin2,
                fips=fips,
                last_update=last_update,
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
                jh_id=jh_id,
            )
        except Exception:
            print(f"Invalid row: {row!r}")
            raise
        else:
            if (
                dr.confirmed > confirmed
                or dr.deaths > deaths
                or dr.recovered > recovered
            ):
                result.record_unexpected_decrease(dr, confirmed, deaths, recovered)
                return
            else:
                dr.confirmed = confirmed
                dr.deaths = deaths
                dr.recovered = recovered

        if jh_id is not None:
            result.record_matched_record(jh_id, dr)

        self.db_instance.add(dr)
