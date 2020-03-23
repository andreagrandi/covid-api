from db.models import DailyReport
from db.database import SessionLocal, engine, Base
from datetime import datetime
from pathlib import Path
from dataflows import Flow, load, checkpoint

BASE_URL = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/'


def get_data_with_caching(date_string):
    result = Flow(
      load(f'{BASE_URL}{date_string}.csv'),
      checkpoint(date_string),
    ).results()

    return result[0][0]


def main():
    print("Importing data into db")

    Base.metadata.create_all(engine)
    db_instance = SessionLocal()

    for row in get_data_with_caching('02-29-2020'):
        dr = DailyReport(
            province_state=row['Province/State'],
            country_region=row['Country/Region'],
            last_update=datetime.fromisoformat(row['Last Update']),
            confirmed=row['Confirmed'],
            deaths=row['Deaths'],
            recovered=row['Recovered'],
        )

        db_instance.add(dr)

    db_instance.commit()


if __name__ == "__main__":
    main()
