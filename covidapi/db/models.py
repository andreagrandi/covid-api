from sqlalchemy import Column, Integer, String, DateTime

from .database import Base


class DailyReport(Base):
    __tablename__ = "daily_reports"

    id = Column(Integer, primary_key=True, index=True)
    country_region = Column(String)
    province_state = Column(String)
    last_update = Column(DateTime)
    confirmed = Column(Integer)
    deaths = Column(Integer)
    recovered = Column(Integer)
