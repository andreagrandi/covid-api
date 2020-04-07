from .db.models import JHRegionInfo
from .db.database import SessionLocal, engine, Base
from .jh_cleaning.lookup_table import Matcher


def convert_region_info(region):
    return JHRegionInfo(
        jh_id = region.identified_region.uid,
        scope = region.identified_region.scope,
        country_code_iso2 = region.identified_region.iso2,
        country_code_iso3 = region.identified_region.iso3,
        fips = region.identified_region.fips,
        country_region = region.region_names.country_region,
        province_state = region.region_names.province_state,
        admin2 = region.region_names.admin2
    )


def region_exists(db, uid):
    """
    Check whether a region already exists in the DB.
    """
    return bool(db.query(JHRegionInfo).filter(JHRegionInfo.jh_id == uid).count())


def main(args):
    Base.metadata.create_all(engine)

    db_instance = SessionLocal()

    for region in Matcher():
        uid = region.identified_region.uid

        if region_exists(db_instance, uid):
            print(f'Skipping {uid}')
            continue

        print(f'Storing {uid}')
        row = convert_region_info(region)
        db_instance.add(row)

    db_instance.commit()
