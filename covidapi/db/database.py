from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from os import environ

SQLALCHEMY_DATABASE_URL = environ.get("DATABASE_URL", "postgresql://covidapi:dummypassword@localhost:5432/covidapi")

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
