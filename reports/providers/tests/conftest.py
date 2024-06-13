# conftest.py

"""
    #TODO add comment
"""

import asyncio
from decimal import Decimal
import pytest
import pytest_asyncio
import time
from typing import AsyncGenerator
from decimal import Decimal
from datetime import datetime, date
from sqlalchemy import event
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
from sqlalchemy import String
from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select
from helpers.session_context import SessionContext
from helpers.type_conversion import TypeConversion
from models import Base, CustomerRole
from models.factory import CustomerRoleFactory
from models.factory.land import LandFactory
# from reports.providers.land_plant_list import ReportProviderLandPlantList
import sqlite3

DATABASE_URL = "sqlite+aiosqlite:///:memory:"

@pytest.fixture(scope="session")
def event_loop() -> asyncio.AbstractEventLoop:
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="session")
def engine():
    engine = create_async_engine(DATABASE_URL, echo=False)
    yield engine
    engine.sync_engine.dispose()

@pytest_asyncio.fixture(scope="function")
async def session(engine) -> AsyncGenerator[AsyncSession, None]:
    @event.listens_for(engine.sync_engine, "connect")
    def set_sqlite_pragma(dbapi_connection, connection_record):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()
    async with engine.begin() as connection:
        await connection.begin_nested()
        await connection.run_sync(Base.metadata.drop_all)
        await connection.run_sync(Base.metadata.create_all)
        TestingSessionLocal = sessionmaker(
            expire_on_commit=False,
            class_=AsyncSession,
            bind=engine,
        )
        async with TestingSessionLocal(bind=connection) as session:
            @event.listens_for(
                session.sync_session, "after_transaction_end"
            )
            def end_savepoint(session, transaction):
                if connection.closed:
                    return
                if not connection.in_nested_transaction():
                    connection.sync_connection.begin_nested()
            yield session
            await session.flush()
            await session.rollback()
