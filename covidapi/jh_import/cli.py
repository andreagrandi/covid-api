from .transform.lookup_table import Matcher
from .load import Importer
from .extract import ReportFetcher
from ..db.models import JHRegionInfo
from ..db.database import SessionLocal, engine, Base
from datetime import date, timedelta
from requests.exceptions import HTTPError


def import_data(args):
    Base.metadata.create_all(engine)

    today = date.today()

    if args.all:
        # Available data starts from 29th February 2020
        current = date.fromisoformat("2020-02-29")
    elif args.latest:
        current = today - timedelta(days=1)
    else:
        current = args.from_date

    report_fetcher = ReportFetcher()
    matcher = Matcher()
    importer = Importer(matcher)

    while current <= today:
        print(f"Importing data for {current}")

        try:
            report = report_fetcher.fetch_report(current)
            result = importer.import_daily_report(report)
            for info in result.info():
                print(info)
        except HTTPError:
            if current == today:
                print("Unable to fetch report. It may not be available yet.")
                break
            else:
                print("Unable to fetch report")
                raise

        current = current + timedelta(days=1)


def convert_region_info(region):
    return JHRegionInfo(
        jh_id=region.identified_region.uid,
        scope=region.identified_region.scope,
        country_code_iso2=region.identified_region.iso2,
        country_code_iso3=region.identified_region.iso3,
        fips=region.identified_region.fips,
        country_region=region.region_names.country_region,
        province_state=region.region_names.province_state,
        admin2=region.region_names.admin2,
    )


def region_exists(db, uid):
    """
    Check whether a region already exists in the DB.
    """
    return bool(db.query(JHRegionInfo).filter(JHRegionInfo.jh_id == uid).count())


def import_regions(args):
    Base.metadata.create_all(engine)

    db_instance = SessionLocal()

    for region in Matcher():
        uid = region.identified_region.uid

        if region_exists(db_instance, uid):
            print(f"Skipping {uid}, already exists")
            continue

        print(f"Storing {uid}")
        row = convert_region_info(region)
        db_instance.add(row)

    db_instance.commit()
