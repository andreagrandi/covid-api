from db.models import DailyReport
from db.database import SessionLocal, engine, Base
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound
from datetime import datetime
from dataflows import Flow, load, checkpoint

BASE_URL = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/'


def get_data_with_caching(date_string):
    result = Flow(
      load(f'{BASE_URL}{date_string}.csv'),
      checkpoint(date_string),
    ).results()

    return result[0][0]


def get_daily_report_by_region_and_date(db: Session, country_region: str, province_state: str, last_update: datetime) -> DailyReport:
    """
    Get a single daily report from the db by matching the region and date.

    Note that province_state is null for some values of country_region.
    """
    if province_state:
        dr = db.query(DailyReport).filter(
            DailyReport.province_state == province_state,
            DailyReport.country_region == country_region,
            DailyReport.last_update == last_update
        )
    else:
        dr = db.query(DailyReport).filter(
            DailyReport.province_state.is_(None),
            DailyReport.country_region == country_region,
            DailyReport.last_update == last_update
        )

    return dr.one()


def main():
    print("Importing data into db")

    Base.metadata.create_all(engine)
    db_instance = SessionLocal()

    for row in get_data_with_caching('02-29-2020'):
        province_state = row['Province/State']
        country_region = row['Country/Region']
        last_update = datetime.fromisoformat(row['Last Update'])

        try:
            dr = get_daily_report_by_region_and_date(
                db=db_instance,
                province_state=province_state,
                country_region=country_region,
                last_update=last_update
            )
        except NoResultFound:
            dr = DailyReport(
                province_state=province_state,
                country_region=country_region,
                last_update=last_update,
                confirmed=row['Confirmed'],
                deaths=row['Deaths'],
                recovered=row['Recovered'],
            )
        else:
            dr.confirmed = row['Confirmed']
            dr.deaths = row['Deaths']
            dr.recovered = row['Recovered']

        db_instance.add(dr)

    db_instance.commit()


if __name__ == "__main__":
    main()
