# conftest.py
# pylint: disable=unused-argument
# pylint: disable=redefined-outer-name

"""
This module contains fixtures and utilities for testing the application.
"""

import asyncio
from typing import AsyncGenerator
from typing import Generator

import pytest
import pytest_asyncio
from sqlalchemy import event
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from models import Base

# Define your in-memory SQLite test database URL
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


@pytest.fixture(scope="session")
def engine():
    """
    Fixture to create the SQLAlchemy async engine.

    This fixture creates the SQLAlchemy async engine object
    using the specified database URL.

    Yields:
        Engine: The SQLAlchemy async engine object.
    """

    engine_obj = create_async_engine(DATABASE_URL, echo=False)
    yield engine_obj
    engine_obj.sync_engine.dispose()


@pytest_asyncio.fixture(scope="function")
async def session(engine) -> AsyncGenerator[AsyncSession, None]:
    """
    Async fixture to provide a database session for testing.

    This fixture ensures that the database schema is created
    before each test and dropped afterwards.
    It also ensures that SQLite foreign key constraints are enforced.

    Args:
        engine: The SQLAlchemy async engine.

    Yields:
        AsyncSession: A SQLAlchemy async session object.
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
            def end_savepoint(session_obj, transaction):
                if connection.closed:
                    return
                if not connection.in_nested_transaction():
                    connection.sync_connection.begin_nested()
            yield session_obj  # type: ignore
            await session_obj.flush()
            await session_obj.rollback()
