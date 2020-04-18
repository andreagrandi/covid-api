import pkg_resources
from fastapi import Depends
from fastapi import APIRouter
from fastapi import Query
from starlette.responses import HTMLResponse
from typing import List
from datetime import date

from ..services.crud import JHCRUD
from ..services.session import get_db, Session
from ..schemas.schemas import JHDailyReport
from ..schemas.enums import Scope

router = APIRouter()


@router.get('/')
def root():
    return HTMLResponse(pkg_resources.resource_string(__name__, 'static/index.html'))


@router.get('/v1/health')
def health():
    return {'status': 'ok'}


@router.get("/v1/jh/daily-reports/", response_model=List[JHDailyReport])
def get_daily_reports(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db),
    last_update_from: date = None,
    last_update_to: date = None,
    country: str = None,
    province: str = None,
    country_code_iso2: str = Query(None, min_length=2, max_length=2),
    country_code_iso3: str = Query(None, min_length=2, max_length=3),
    scope: Scope = None
):
    if country_code_iso2:
        country_code_iso2 = country_code_iso2.upper()

    if country_code_iso3:
        country_code_iso3 = country_code_iso3.upper()

    daily_reports = JHCRUD().get_daily_reports(
        db, skip=skip, limit=limit,
        last_update_from=last_update_from,
        last_update_to=last_update_to,
        country=country,
        province=province,
        country_code_iso2=country_code_iso2,
        country_code_iso3=country_code_iso3,
        scope=scope
    )

    return daily_reports
