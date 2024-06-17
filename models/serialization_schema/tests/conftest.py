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
    Create a new database session for a test and
    ensure it is properly closed after the test.

    This fixture sets up a new database session
    using the provided engine. It ensures that
    the database schema is created before the test
    and that the session is closed after the test.

    Args:
        engine (Engine): The SQLAlchemy engine to bind the session to.

    Yields:
        Session: A SQLAlchemy session object.

    Example:
        def test_something(session):
            # use the session object for database operations
    """
    # Create all tables in the database
    Base.metadata.create_all(engine)

    # Create a configured "Session" class
    SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)

    # Instantiate a session
    session_instance = SessionLocal()

    try:
        yield session_instance
    finally:
        # Close the session after the test
        session_instance.close()
