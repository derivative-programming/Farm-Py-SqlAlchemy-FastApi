# apis/fs_farm_api/v1_0/endpoints/tests/conftest.py
# pylint: disable=redefined-outer-name
"""
This module contains fixtures for unit testing the endpoints in the API.

Fixtures:
- overridden_get_db: Fixture that creates an in-memory SQLite
    database and provides a session for testing.
- api_key_fixture: Fixture that builds a test API key for unit testing.
"""

import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

import current_runtime
from helpers.api_token import ApiToken
from helpers.session_context import SessionContext
from models import Base

# Define your in-memory SQLite test database URL
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"


@pytest_asyncio.fixture(scope="function")
async def overridden_get_db():
    """
    Fixture that creates an in-memory SQLite database and
    provides a session for testing.
    """
    # Create the async engine for the in-memory SQLite database
    engine = create_async_engine(TEST_DATABASE_URL, echo=False)

    # Create the tables in the database
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Create a sessionmaker
    AsyncSessionLocal = sessionmaker(  # pylint: disable=invalid-name
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False
    )

    # Create a new session for the test
    async with AsyncSessionLocal() as session:  # type: ignore
        yield session

    # After the test is done, drop all the tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    # Dispose the engine
    await engine.dispose()


@pytest_asyncio.fixture(scope="function")
async def api_key_fixture(overridden_get_db: AsyncSession):
    """
    Fixture that builds a test API key for unit testing.
    """

    session_context = SessionContext(dict(), overridden_get_db)

    await current_runtime.initialize(session_context)

    api_dict = {}
    test_api_key = ApiToken.create_token(api_dict, 1)
    return test_api_key
