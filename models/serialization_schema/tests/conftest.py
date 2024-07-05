# conftest.py
# pylint: disable=redefined-outer-name

"""
This module contains fixtures for testing the serialization schema.
"""

import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from models import Base
from services.logging_config import get_logger
# from config import TEST_DATABASE_URL

TEST_DATABASE_URL = "sqlite:///:memory:"
logger = get_logger(__name__)


@pytest.fixture(scope="module")
def engine():
    """
    Fixture that creates a SQLAlchemy engine for the test module.

    This fixture creates an in-memory SQLite database engine
    and enables foreign key constraints. The engine is yielded
    to the test module and disposed of after the tests are run.

    Returns:
        Engine: The SQLAlchemy engine object.

    Example:
        def test_something(engine):
            # use the engine object for database operations
    """

    engine = create_engine(TEST_DATABASE_URL, echo=False)
    with engine.connect() as conn:
        conn.execute(text("PRAGMA foreign_keys=ON"))
    yield engine
    engine.dispose()


@pytest.fixture(scope="function")
def session(engine):
    """
    Fixture that creates a new database session for a test.

    This fixture sets up a new database session using the provided
    engine. It ensures that the database schema is created before
    the test and that the session is closed after the test.

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
    SessionLocal = sessionmaker(  # pylint: disable=invalid-name
        bind=engine, expire_on_commit=False)

    # Instantiate a session
    session_instance = SessionLocal()

    try:
        yield session_instance
    finally:
        # Close the session after the test
        session_instance.close()
