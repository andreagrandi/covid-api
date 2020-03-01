from sqlalchemy.orm import Session

from . import models


def get_daily_report(db: Session, daily_report_id: int):
    return db.query(
            models.DailyReport
        ).filter(
            models.DailyReport.id == daily_report_id
        ).first()


def get_daily_reports(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.DailyReport).offset(skip).limit(limit).all()
