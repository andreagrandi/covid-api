from pydantic import BaseModel
from datetime import datetime


class DailyReport(BaseModel):
    id: int
    country_region: str
    province_state: str
    last_update: datetime
    confirmed: int
    deaths: int
    recovered: int

    class Config:
        orm_mode = True
