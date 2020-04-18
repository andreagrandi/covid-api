from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from .enums import Scope

class JHRegionInfo(BaseModel):
    jh_id: int = Field(None, alias='uid')
    scope: Scope
    country_code_iso2: str
    country_code_iso3: str
    country_region: str
    province_state: Optional[str]
    fips: Optional[str]
    admin2: Optional[str]

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class JHDailyReport(BaseModel):
    id: Optional[int]
    country_region: str
    province_state: Optional[str]
    fips: Optional[str]
    admin2: Optional[str]
    last_update: datetime
    confirmed: int
    deaths: int
    recovered: int
    region_info: JHRegionInfo

    class Config:
        orm_mode = True
