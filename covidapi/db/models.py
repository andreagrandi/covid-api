from sqlalchemy import Column, Integer, String, DateTime, inspect

from .database import Base, engine


class DailyReport(Base):
    __tablename__ = "daily_reports"

    id = Column(Integer, primary_key=True, index=True)
    country_region = Column(String)
    province_state = Column(String)
    fips = Column(String)
    admin2 = Column(String)
    last_update = Column(DateTime)
    confirmed = Column(Integer)
    deaths = Column(Integer)
    recovered = Column(Integer)

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


Base.metadata.create_all(bind=engine)
