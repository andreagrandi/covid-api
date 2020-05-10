from .transform.clean_columns import clean_extra_whitespace
from requests import Session
import csv


class ReportFetcher:
    """
    Fetch the raw data from Github
    """

    BASE_URL = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/"

    def __init__(self):
        self.session = Session()

    def fetch_report(self, report_date):
        date_string = report_date.strftime(r"%m-%d-%Y")

        response = self.session.get(f"{self.BASE_URL}{date_string}.csv")
        response.raise_for_status()

        records = []
        for record in csv.DictReader(
            (line.decode("utf8") for line in response.iter_lines())
        ):
            record = clean_extra_whitespace(record)
            records.append(record)

        return records
