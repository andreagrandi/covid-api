from starlette.testclient import TestClient

from covidapi.app import app
from ..services.session import get_db
from ..db.models import DailyReport
from ..db.database import Base, test_engine, TestSessionLocal
import pytest
from datetime import datetime

# Create a test database
Base.metadata.create_all(bind=test_engine)

client = TestClient(app)

@pytest.fixture
def db_session():
    db = TestSessionLocal()

    def get_test_db():
        yield db

    # Use the test session
    app.dependency_overrides[get_db] = get_test_db

    yield db

    db.rollback()


def test_empty_daily_report(db_session):
    """
    Test something with a db dependency
    """
    response = client.get("/v1/daily-reports/")
    assert response.json() == []


def test_single_daily_report(db_session):
    dr = DailyReport(
        province_state='province',
        country_region='country',
        last_update=datetime(2020, 1, 1, 0, 0, 0),
        confirmed=1,
        deaths=0,
        recovered=0,
    )
    db_session.add(dr)
    db_session.flush()

    response = client.get("/v1/daily-reports/")

    assert response.json() == [
        {
            'id': 1,
            'province_state': 'province',
            'country_region': 'country',
            'last_update': '2020-01-01T00:00:00',
            'confirmed': 1,
            'deaths': 0,
            'recovered': 0,
        }
    ]
