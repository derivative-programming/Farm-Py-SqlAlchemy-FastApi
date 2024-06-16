# models/factory/tests/date_greater_than_filter_async_test.py
"""
    #TODO add comment
"""
import uuid
import asyncio
import time
import math
from decimal import Decimal
from datetime import datetime, date, timedelta
from typing import AsyncGenerator
from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select
from sqlalchemy import event
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
import pytest
import pytest_asyncio
from models import Base, DateGreaterThanFilter
from models.factory import DateGreaterThanFilterFactory
DATABASE_URL = "sqlite+aiosqlite:///:memory:"
class TestDateGreaterThanFilterFactoryAsync:
    """
    #TODO add comment
    """
    @pytest.fixture(scope="function")
    def event_loop(self) -> asyncio.AbstractEventLoop:
        """
        #TODO add comment
        """
        loop = asyncio.get_event_loop_policy().new_event_loop()
        yield loop
        loop.close()
    @pytest.fixture(scope="function")
    def engine(self):
        """
        #TODO add comment
        """
        engine = create_async_engine(DATABASE_URL, echo=False)
        yield engine
        engine.sync_engine.dispose()
    @pytest_asyncio.fixture(scope="function")
    async def session(self, engine) -> AsyncGenerator[AsyncSession, None]:
        """
        #TODO add comment
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
    @pytest.mark.asyncio
    async def test_date_greater_than_filter_creation(self, session):
        """
        #TODO add comment
        """
        date_greater_than_filter = await DateGreaterThanFilterFactory.create_async(session=session)
        assert date_greater_than_filter.date_greater_than_filter_id is not None
    @pytest.mark.asyncio
    async def test_code_default(self, session):
        """
        #TODO add comment
        """
        date_greater_than_filter = await DateGreaterThanFilterFactory.create_async(session=session)
        assert isinstance(date_greater_than_filter.code, uuid.UUID)
    @pytest.mark.asyncio
    async def test_last_change_code_default_on_build(self, session):
        """
        #TODO add comment
        """
        date_greater_than_filter: DateGreaterThanFilter = await DateGreaterThanFilterFactory.build_async(session=session)
        assert date_greater_than_filter.last_change_code == 0
    @pytest.mark.asyncio
    async def test_last_change_code_default_on_creation(self, session):
        """
        #TODO add comment
        """
        date_greater_than_filter: DateGreaterThanFilter = await DateGreaterThanFilterFactory.create_async(session=session)
        assert date_greater_than_filter.last_change_code == 1
    @pytest.mark.asyncio
    async def test_last_change_code_default_on_update(self, session):
        """
        #TODO add comment
        """
        date_greater_than_filter = await DateGreaterThanFilterFactory.create_async(session=session)
        initial_code = date_greater_than_filter.last_change_code
        date_greater_than_filter.code = uuid.uuid4()
        await session.commit()
        assert date_greater_than_filter.last_change_code != initial_code
    @pytest.mark.asyncio
    async def test_date_inserted_on_build(self, session):
        """
        #TODO add comment
        """
        date_greater_than_filter = await DateGreaterThanFilterFactory.build_async(session=session)
        assert date_greater_than_filter.insert_utc_date_time is not None
        assert isinstance(date_greater_than_filter.insert_utc_date_time, datetime)
    @pytest.mark.asyncio
    async def test_date_inserted_on_initial_save(self, session):
        """
        #TODO add comment
        """
        date_greater_than_filter = await DateGreaterThanFilterFactory.build_async(session=session)
        assert date_greater_than_filter.insert_utc_date_time is not None
        assert isinstance(date_greater_than_filter.insert_utc_date_time, datetime)
        initial_time = datetime.utcnow() + timedelta(days=-1)
        date_greater_than_filter.code = uuid.uuid4()
        session.add(date_greater_than_filter)
        await session.commit()
        assert date_greater_than_filter.insert_utc_date_time > initial_time
    @pytest.mark.asyncio
    async def test_date_inserted_on_second_save(self, session):
        """
        #TODO add comment
        """
        date_greater_than_filter = await DateGreaterThanFilterFactory.create_async(session=session)
        assert date_greater_than_filter.insert_utc_date_time is not None
        assert isinstance(date_greater_than_filter.insert_utc_date_time, datetime)
        initial_time = date_greater_than_filter.insert_utc_date_time
        date_greater_than_filter.code = uuid.uuid4()
        time.sleep(1)
        await session.commit()
        assert date_greater_than_filter.insert_utc_date_time == initial_time
    @pytest.mark.asyncio
    async def test_date_updated_on_build(self, session):
        """
        #TODO add comment
        """
        date_greater_than_filter = await DateGreaterThanFilterFactory.build_async(session=session)
        assert date_greater_than_filter.last_update_utc_date_time is not None
        assert isinstance(date_greater_than_filter.last_update_utc_date_time, datetime)
    @pytest.mark.asyncio
    async def test_date_updated_on_initial_save(self, session):
        """
        #TODO add comment
        """
        date_greater_than_filter = await DateGreaterThanFilterFactory.build_async(session=session)
        assert date_greater_than_filter.last_update_utc_date_time is not None
        assert isinstance(date_greater_than_filter.last_update_utc_date_time, datetime)
        initial_time = datetime.utcnow() + timedelta(days=-1)
        date_greater_than_filter.code = uuid.uuid4()
        session.add(date_greater_than_filter)
        await session.commit()
        assert date_greater_than_filter.last_update_utc_date_time > initial_time
    @pytest.mark.asyncio
    async def test_date_updated_on_second_save(self, session):
        """
        #TODO add comment
        """
        date_greater_than_filter = await DateGreaterThanFilterFactory.create_async(session=session)
        assert date_greater_than_filter.last_update_utc_date_time is not None
        assert isinstance(date_greater_than_filter.last_update_utc_date_time, datetime)
        initial_time = date_greater_than_filter.last_update_utc_date_time
        date_greater_than_filter.code = uuid.uuid4()
        time.sleep(1)
        await session.commit()
        assert date_greater_than_filter.last_update_utc_date_time > initial_time
    @pytest.mark.asyncio
    async def test_model_deletion(self, session):
        """
        #TODO add comment
        """
        date_greater_than_filter = await DateGreaterThanFilterFactory.create_async(session=session)
        await session.delete(date_greater_than_filter)
        await session.commit()
        # Construct the select statement
        stmt = select(DateGreaterThanFilter).where(DateGreaterThanFilter._date_greater_than_filter_id == date_greater_than_filter.date_greater_than_filter_id)
        # Execute the statement asynchronously
        result = await session.execute(stmt)
        # Fetch all results
        deleted_date_greater_than_filter = result.scalars().first()
        # deleted_date_greater_than_filter = await session.query(DateGreaterThanFilter).filter_by(
        # date_greater_than_filter_id=date_greater_than_filter.date_greater_than_filter_id).first()
        assert deleted_date_greater_than_filter is None
    @pytest.mark.asyncio
    async def test_data_types(self, session):
        """
        #TODO add comment
        """
        date_greater_than_filter = await DateGreaterThanFilterFactory.create_async(session=session)
        assert isinstance(date_greater_than_filter.date_greater_than_filter_id, int)
        assert isinstance(date_greater_than_filter.code, uuid.UUID)
        assert isinstance(date_greater_than_filter.last_change_code, int)
        assert isinstance(date_greater_than_filter.insert_user_id, uuid.UUID)
        assert isinstance(date_greater_than_filter.last_update_user_id, uuid.UUID)
        assert isinstance(date_greater_than_filter.day_count, int)
        assert date_greater_than_filter.description == "" or isinstance(date_greater_than_filter.description, str)
        assert isinstance(date_greater_than_filter.display_order, int)
        assert isinstance(date_greater_than_filter.is_active, bool)
        assert date_greater_than_filter.lookup_enum_name == "" or isinstance(date_greater_than_filter.lookup_enum_name, str)
        assert date_greater_than_filter.name == "" or isinstance(date_greater_than_filter.name, str)
        assert isinstance(date_greater_than_filter.pac_id, int)
        # Check for the peek values
# endset
        # dayCount,
        # description,
        # displayOrder,
        # isActive,
        # lookupEnumName,
        # name,
        # pacID
        assert isinstance(date_greater_than_filter.pac_code_peek, uuid.UUID)
# endset
        assert isinstance(date_greater_than_filter.insert_utc_date_time, datetime)
        assert isinstance(date_greater_than_filter.last_update_utc_date_time, datetime)
    @pytest.mark.asyncio
    async def test_unique_code_constraint(self, session):
        """
        #TODO add comment
        """
        date_greater_than_filter_1 = await DateGreaterThanFilterFactory.create_async(session=session)
        date_greater_than_filter_2 = await DateGreaterThanFilterFactory.create_async(session=session)
        date_greater_than_filter_2.code = date_greater_than_filter_1.code
        session.add_all([date_greater_than_filter_1, date_greater_than_filter_2])
        with pytest.raises(Exception):
            await session.commit()
        await session.rollback()
    @pytest.mark.asyncio
    async def test_fields_default(self):
        """
        #TODO add comment
        """
        date_greater_than_filter = DateGreaterThanFilter()
        assert date_greater_than_filter.code is not None
        assert date_greater_than_filter.last_change_code is not None
        assert date_greater_than_filter.insert_user_id is not None
        assert date_greater_than_filter.last_update_user_id is not None
        assert date_greater_than_filter.insert_utc_date_time is not None
        assert date_greater_than_filter.last_update_utc_date_time is not None
# endset
        # dayCount,
        # description,
        # displayOrder,
        # isActive,
        # lookupEnumName,
        # name,
        # PacID
        assert isinstance(date_greater_than_filter.pac_code_peek, uuid.UUID)
# endset
        assert date_greater_than_filter.day_count == 0
        assert date_greater_than_filter.description == ""
        assert date_greater_than_filter.display_order == 0
        assert date_greater_than_filter.is_active is False
        assert date_greater_than_filter.lookup_enum_name == ""
        assert date_greater_than_filter.name == ""
        assert date_greater_than_filter.pac_id == 0
# endset
    @pytest.mark.asyncio
    async def test_last_change_code_concurrency(self, session):
        """
        #TODO add comment
        """
        date_greater_than_filter = await DateGreaterThanFilterFactory.create_async(session=session)
        original_last_change_code = date_greater_than_filter.last_change_code
        stmt = select(DateGreaterThanFilter).where(DateGreaterThanFilter._date_greater_than_filter_id == date_greater_than_filter.date_greater_than_filter_id)
        result = await session.execute(stmt)
        date_greater_than_filter_1 = result.scalars().first()
        # date_greater_than_filter_1 = await session.query(DateGreaterThanFilter).filter_by(
        # date_greater_than_filter_id=date_greater_than_filter.date_greater_than_filter_id).first()
        date_greater_than_filter_1.code = uuid.uuid4()
        await session.commit()
        stmt = select(DateGreaterThanFilter).where(DateGreaterThanFilter._date_greater_than_filter_id == date_greater_than_filter.date_greater_than_filter_id)
        result = await session.execute(stmt)
        date_greater_than_filter_2 = result.scalars().first()
        # date_greater_than_filter_2 = await session.query(DateGreaterThanFilter).filter_by(
        # date_greater_than_filter_id=date_greater_than_filter.date_greater_than_filter_id).first()
        date_greater_than_filter_2.code = uuid.uuid4()
        await session.commit()
        assert date_greater_than_filter_2.last_change_code != original_last_change_code
# endset
    # dayCount,
    # description,
    # displayOrder,
    # isActive,
    # lookupEnumName,
    # name,
    # PacID
    @pytest.mark.asyncio
    async def test_invalid_pac_id(self, session):
        """
        #TODO add comment
        """
        date_greater_than_filter = await DateGreaterThanFilterFactory.create_async(session=session)
        date_greater_than_filter.pac_id = 99999
        with pytest.raises(IntegrityError):
            await session.commit()
        await session.rollback()
# endset
