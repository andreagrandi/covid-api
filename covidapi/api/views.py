import pkg_resources
from fastapi import Depends
from fastapi import APIRouter
from starlette.responses import HTMLResponse
from typing import List

from ..services.crud import JHCRUD
from ..services.session import get_db, Session
from ..schemas.schemas import JHDailyReport

router = APIRouter()


@router.get('/')
def root():
    return HTMLResponse(pkg_resources.resource_string(__name__, 'static/index.html'))


@router.get('/v1/health')
def health():
    return {'status': 'ok'}


@router.get("/v1/jh/daily-reports/", response_model=List[JHDailyReport])
def get_daily_reports(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    daily_reports = JHCRUD().get_daily_reports(db, skip=skip, limit=limit)
    return daily_reports
