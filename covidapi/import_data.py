from db.models import DailyReport
from db.database import SessionLocal, engine, Base
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound
from datetime import datetime
from dataflows import Flow, load, checkpoint
from collections import defaultdict

BASE_URL = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/'


def get_data_with_caching(date_string):
    result = Flow(
      load(f'{BASE_URL}{date_string}.csv', infer_strategy=load.INFER_STRINGS, cast_strategy=load.CAST_TO_STRINGS),
      checkpoint(date_string),
    ).results()

    return result[0][0]


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


def get_daily_report_by_region_and_date(db: Session, country_region: str, province_state: str, fips: str, admin2: str, last_update: datetime) -> DailyReport:
    """
    Get a single daily report from the db by matching some kind of region and the date.

    Note that province_state is null for some values of country_region.
    admin2 and fips were added to the reports later on, so they may be null.
    FIPS is a code that uniquely identifies a region in the US, whereas admin2
    is a place name that needs to be used in conjunction with country_region
    and province_state.
    """
    if fips:
        dr = db.query(DailyReport).filter(
            DailyReport.fips == fips
        )
    elif province_state and admin2:
        dr = db.query(DailyReport).filter(
            DailyReport.province_state == province_state,
            DailyReport.country_region == country_region,
            DailyReport.admin2 == admin2,
            DailyReport.fips.is_(None),
            DailyReport.last_update == last_update
        )
    elif province_state:
        dr = db.query(DailyReport).filter(
            DailyReport.fips.is_(None),
            DailyReport.admin2.is_(None),
            DailyReport.province_state == province_state,
            DailyReport.country_region == country_region,
            DailyReport.last_update == last_update
        )
    else:
        dr = db.query(DailyReport).filter(
            DailyReport.fips.is_(None),
            DailyReport.admin2.is_(None),
            DailyReport.province_state.is_(None),
            DailyReport.country_region == country_region,
            DailyReport.last_update == last_update
        )

    return dr.one()


DUPLICATE_ADMIN2 = {
    'Dona Ana': 'Doña Ana'
}

def clean_admin2(original):
    """
    Some US records are duplicated.
    These have the same FIPS (which should be unique) but slightly
    different admin2 values. See https://github.com/CSSEGISandData/COVID-19/issues/1620

    Normalise these to a single name so we can deduplicate them.
    """
    return DUPLICATE_ADMIN2.get(original, original)


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

    print('Unique admin2 records ✅')

    if db_instance.execute('''
        select 1
        from daily_reports
        where province_state is null
        group by country_region, last_update
        having count(*) > 1
        ''').fetchone():
        db_instance.rollback()
        raise Exception(f'Found records with the same country_region and last_update, and no province_state')

    print('Unique province/state records ✅')

    if db_instance.execute('''
        select 1
        from daily_reports
        where admin2 is null
        group by country_region, province_state, last_update
        having count(*) > 1
        ''').fetchone():
        db_instance.rollback()
        raise Exception(f'Found records with the same country_region, province_state and last_update, and no admin2')

    print('Unique country records ✅')


def main():
    print("Importing data into db")

    Base.metadata.create_all(engine)
    db_instance = SessionLocal()
    to_deduplicate = defaultdict(list)

    for row in get_data_with_caching('03-27-2020'):
        last_update_str = row.get('Last Update') or row['Last_Update']
        last_update = datetime.fromisoformat(last_update_str)

        # Region identifiers
        country_region = row.get('Country_Region') or row['Country/Region']
        province_state = row.get('Province_State') or row.get('Province/State')
        admin2 = clean_admin2(row.get('Admin2'))
        fips = row.get('FIPS')

        # Measures
        confirmed = int(row['Confirmed'])
        deaths = int(row['Deaths'])
        recovered = int(row['Recovered'])

        try:
            dr = get_daily_report_by_region_and_date(
                db=db_instance,
                province_state=province_state,
                country_region=country_region,
                admin2 = admin2,
                fips = fips,
                last_update=last_update
            )
        except NoResultFound:
            dr = DailyReport(
                province_state=province_state,
                country_region=country_region,
                admin2 = admin2,
                fips = fips,
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

    deduplicate(db_instance, to_deduplicate)
    db_instance.flush()
    sanity_check(db_instance)
    db_instance.commit()


if __name__ == "__main__":
    main()
