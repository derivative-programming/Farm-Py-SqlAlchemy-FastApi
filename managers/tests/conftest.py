# models/managers/tests/conftest.py  # pylint: disable=duplicate-code # noqa: E501
# pylint: disable=unused-argument
# pylint: disable=redefined-outer-name

"""
This module contains fixtures for testing the managers module.

Fixtures are functions that provide test resources to other test functions.
In this module, we have fixtures for creating a
new event loop, creating a SQLAlchemy engine,
and creating an asynchronous session object for interacting with the database.
"""

import asyncio
from typing import Generator

import pytest_asyncio
from sqlalchemy import event
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

import pytest
from config import TEST_DATABASE_URL
from models import Base


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
    Returns a SQLAlchemy engine.

    This function creates and returns a SQLAlchemy
    engine using the provided TEST_DATABASE_URL.
    The engine is created as an asynchronous engine
    and is yielded as a context manager.
    After the context manager is exited, the engine is disposed.

    Returns:
        sqlalchemy.ext.asyncio.AsyncEngine: The SQLAlchemy engine.

    """
    engine = create_async_engine(TEST_DATABASE_URL, echo=False)
    yield engine
    engine.sync_engine.dispose()


@pytest_asyncio.fixture(scope="function")
async def session(engine) -> AsyncSession:  # type: ignore
    """
    Returns an asynchronous session object for interacting with the database.

    Args:
        engine: The SQLAlchemy engine used to connect to the database.

    Returns:
        An asynchronous session object.

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
        testing_session_local = sessionmaker(
            expire_on_commit=False,
            class_=AsyncSession,
            bind=engine,
        )
        async with testing_session_local(bind=connection) as session_obj:  # type: ignore # noqa: E501
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
