import csv
from db.models import DailyReport
from db.database import SessionLocal, engine, Base
from datetime import datetime
from pathlib import Path

CSV_FILE = Path(__file__).parent / '02-29-2020.csv'


def main():
    print("Importing data into db")

    Base.metadata.create_all(engine)
    db_instance = SessionLocal()

    with open(CSV_FILE) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        next(csv_reader, None)  # skip the headers

        for row in csv_reader:
            dr = DailyReport(
                province_state=row[0],
                country_region=row[1],
                last_update=datetime.fromisoformat(row[2]),
                confirmed=row[3],
                deaths=row[4],
                recovered=row[5],
            )

            db_instance.add(dr)

    db_instance.commit()


if __name__ == "__main__":
    main()
