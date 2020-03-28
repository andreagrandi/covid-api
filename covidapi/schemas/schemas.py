from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class DailyReport(BaseModel):
    id: Optional[int]
    country_region: str
    province_state: Optional[str]
    last_update: datetime
    confirmed: int
    deaths: int
    recovered: int

    class Config:
        orm_mode = True
