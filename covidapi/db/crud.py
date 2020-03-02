from sqlalchemy.orm import Session

from . import models, schemas


def get_daily_report(db: Session, daily_report_id: int):
    return db.query(
            models.DailyReport
        ).filter(
            models.DailyReport.id == daily_report_id
        ).first()


def get_daily_reports(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.DailyReport).offset(skip).limit(limit).all()


def create_daily_report(db: Session, daily_report: schemas.DailyReport):
    db_daily_report = models.DailyReport(
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
