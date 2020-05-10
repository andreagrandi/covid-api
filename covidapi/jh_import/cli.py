from .transform.lookup_table import Matcher
from .load import Importer
from .extract import ReportFetcher
from ..db.models import JHRegionInfo
from ..db.database import SessionLocal
from ..services.crud import JHCRUD
from datetime import date, timedelta
from requests.exceptions import HTTPError


def import_data(args):
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


def link_region(db_instance, daily_report, matcher):
    region_names = JHRegionInfo(
        country_region=daily_report.country_region,
        province_state=daily_report.province_state,
        admin2=daily_report.admin2,
    )
    match = matcher.match_region(region_names)
    new_jh_id = match.identified_region.uid if match else None
    if new_jh_id and daily_report.jh_id != new_jh_id:
        print(f"Updating JH ID from {daily_report.jh_id} to {new_jh_id}")
        daily_report.jh_id = match.identified_region.jh_id
        db_instance.add(daily_report)


def retroactively_link_regions(args):
    db_instance = SessionLocal()
    matcher = Matcher()

    fetched = None
    skip = 0
    limit = 10000
    while fetched != 0:
        daily_reports = JHCRUD().get_daily_reports(db_instance, skip=skip, limit=limit,)
        fetched = len(daily_reports)

        for daily_report in daily_reports:
            link_region(db_instance, daily_report, matcher)

        db_instance.commit()

        skip += limit
        print(skip)
