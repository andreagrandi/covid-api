from fastapi import Depends
from fastapi import APIRouter
from sqlalchemy.orm import Session
from typing import List

from ..db import models
from ..services import crud
from ..schemas.schemas import DailyReport
from ..db.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

router = APIRouter()


# Dependency
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@router.get('/v1/health')
def health():
    return {'status': 'ok'}


@router.get("/v1/daily-reports/", response_model=List[DailyReport])
def get_daily_reports(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    daily_reports = crud.get_daily_reports(db, skip=skip, limit=limit)
    return daily_reports
