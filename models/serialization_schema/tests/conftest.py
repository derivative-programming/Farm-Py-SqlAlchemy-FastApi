# conftest.py

"""
    #TODO add comment
"""

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base
from services.logging_config import get_logger

logger = get_logger(__name__)

DATABASE_URL = "sqlite:///:memory:"


@pytest.fixture(scope="module")
def engine():
    """
        #TODO add comment
    """

    engine = create_engine(DATABASE_URL, echo=False)
    with engine.connect() as conn:
        conn.connection.execute("PRAGMA foreign_keys=ON")
    yield engine
    engine.dispose()


@pytest.fixture(scope="function")
def session(engine):
    """
        #TODO add comment
    """

    Base.metadata.create_all(engine)
    SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)
    session_instance = SessionLocal()
    yield session_instance
    session_instance.close()
