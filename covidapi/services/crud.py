from sqlalchemy.orm import Session
from datetime import date

from ..db import models
from ..schemas import schemas


class JHCRUD:
    def get_daily_report(self, db: Session, daily_report_id: int):
        return db.query(
                models.JHDailyReport
            ).filter(
                models.JHDailyReport.id == daily_report_id
            ).first()

    def get_daily_reports(
        self, db: Session, skip: int = 0, limit: int = 1000,
        last_update_from: date = None,
        last_update_to: date = None,
        country: str = None,
        province: str = None,
    ):
        query = db.query(models.JHDailyReport)

        if last_update_from:
            query = query.filter(models.JHDailyReport.last_update >= last_update_from)
        if last_update_to:
            query = query.filter(models.JHDailyReport.last_update <= last_update_to)
        if country:
            query = query.filter(models.JHDailyReport.country_region == country)
        if province:
            query = query.filter(models.JHDailyReport.province_state == province)

        query = query.offset(skip).limit(limit)
        return query.all()

    def create_daily_report(self, db: Session, daily_report: schemas.JHDailyReport):
        db_daily_report = models.JHDailyReport(
            country_region=daily_report.country_region,
            province_state=daily_report.province_state,
            last_update=daily_report.last_update,
            confirmed=daily_report.confirmed,
            deaths=daily_report.deaths,
            recovered=daily_report.recovered,
        )

        db.add(db_daily_report)
        db.commit()
        db.refresh(db_daily_report)

        return db_daily_report
