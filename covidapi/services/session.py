from sqlalchemy.orm import Session
from ..db.database import SessionLocal, TestSessionLocal


def get_db() -> Session:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
