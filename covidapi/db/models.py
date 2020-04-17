from sqlalchemy import Column, Integer, String, DateTime, Enum, inspect, ForeignKey
from sqlalchemy.orm import relationship

from .database import Base, engine
from ..schemas.enums import Scope


class JHRegionInfo(Base):
    __tablename__ = "jh_region_info"

    jh_id = Column(Integer, primary_key=True, index=True)
    scope = Column(Enum(Scope))
    country_code_iso2 = Column(String(length=2))
    country_code_iso3 = Column(String(length=3))
    country_region = Column(String)
    province_state = Column(String)
    fips = Column(String)
    admin2 = Column(String)
    reports = relationship("JHDailyReport", backref='region_info')

class JHDailyReport(Base):
    __tablename__ = "jh_daily_reports"

    id = Column(Integer, primary_key=True, index=True)
    country_region = Column(String)
    province_state = Column(String)
    fips = Column(String)
    admin2 = Column(String)
    last_update = Column(DateTime)
    confirmed = Column(Integer)
    deaths = Column(Integer)
    recovered = Column(Integer)
    jh_id = Column(Integer, ForeignKey('jh_region_info.jh_id'))

    def __repr__(self):
        state = inspect(self)
        field_reprs = []
        fields = state.mapper.columns.keys()
        for key in fields:
            value = state.attrs[key].loaded_value
            value = repr(value)
            field_reprs.append('='.join((key, value)))

        parameters_repr = ', '.join(field_reprs)

        return f'DailyReport({parameters_repr})'
