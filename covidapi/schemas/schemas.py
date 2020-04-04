from pydantic import BaseModel
from datetime import datetime
from typing import Optional


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

    class Config:
        orm_mode = True
