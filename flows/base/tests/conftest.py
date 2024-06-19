# flows/base/tests/conftest.py
# pylint: disable=unused-argument
# pylint: disable=redefined-outer-name

"""
This module contains fixtures and configurations for testing the base module.

Fixtures:
- event_loop: Fixture to provide a new event loop for each test function.
- engine: Fixture to create an async engine for the database.
- session: Fixture to create an async session for the database.

Configurations:
- DATABASE_URL: The URL for the in-memory SQLite database.
"""

import asyncio
from typing import Generator
import pytest
import pytest_asyncio
from sqlalchemy import event
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from models import Base
from database import AsyncSessionLocal

DATABASE_URL = "sqlite+aiosqlite:///:memory:"


@pytest.fixture(scope="function")
def event_loop() -> Generator[asyncio.AbstractEventLoop, None, None]:
    """
    Fixture to provide a new event loop for each test function.

    This fixture ensures that each test function runs in its own event loop,
    providing isolation and avoiding potential issues with shared state.

    Yields:
        asyncio.AbstractEventLoop: The event loop for the
        current test function.
    """

    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function")
def engine():
    """
    Fixture to create an async engine for the database.

    Returns:
        sqlalchemy.ext.asyncio.AsyncEngine: The async engine for the database.
    """

    engine = create_async_engine(DATABASE_URL, echo=False)
    yield engine
    engine.sync_engine.dispose()


@pytest_asyncio.fixture(scope="function")
async def session(engine) -> AsyncSessionLocal:  # type: ignore
    """
    Fixture to create an async session for the database.

    Args:
        engine (sqlalchemy.ext.asyncio.AsyncEngine):
            The async engine for the database.

    Returns:
        database.AsyncSessionLocal: The async session for the database.
    """

    @event.listens_for(engine.sync_engine, "connect")
    def set_sqlite_pragma(dbapi_connection, connection_record):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()
    async with engine.begin() as connection:
        await connection.begin_nested()
        await connection.run_sync(Base.metadata.drop_all)
        await connection.run_sync(Base.metadata.create_all)
        TestingSessionLocal = sessionmaker(  # pylint: disable=invalid-name
            expire_on_commit=False,
            class_=AsyncSession,
            bind=engine,
        )
        async with TestingSessionLocal(bind=connection) as session_obj:  # type: ignore # noqa: E501
            @event.listens_for(
                session_obj.sync_session, "after_transaction_end"
            )
            def end_savepoint(session, transaction):
                if connection.closed:
                    return
                if not connection.in_nested_transaction():
                    connection.sync_connection.begin_nested()
            yield session_obj  # type: ignore
            await session_obj.flush()
            await session_obj.rollback()
