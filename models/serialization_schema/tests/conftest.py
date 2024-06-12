# conftest.py

"""
    #TODO add comment
"""

import json
import pytest
import pytz
from models import Plant
from datetime import date, datetime
from decimal import Decimal
from models.serialization_schema import PlantSchema
from models.factory import PlantFactory
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base
from services.logging_config import get_logger
logger = get_logger(__name__)

DATABASE_URL = "sqlite:///:memory:"


@pytest.fixture(scope="module")
def engine():
    engine = create_engine(DATABASE_URL, echo=False)
    with engine.connect() as conn:
        conn.connection.execute("PRAGMA foreign_keys=ON")
    yield engine
    engine.dispose()


@pytest.fixture(scope="function")
def session(engine):
    Base.metadata.create_all(engine)
    SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)
    session_instance = SessionLocal()
    yield session_instance
    session_instance.close()
