from sqlalchemy.orm import Session
from ..db.database import SessionLocal


def get_db() -> Session:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
