# models/factory/tests/error_log_async_test.py
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
from models import Base, ErrorLog
from models.factory import ErrorLogFactory
DATABASE_URL = "sqlite+aiosqlite:///:memory:"
class TestErrorLogFactoryAsync:
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
    async def test_error_log_creation(self, session):
        """
        #TODO add comment
        """
        error_log = await ErrorLogFactory.create_async(session=session)
        assert error_log.error_log_id is not None
    @pytest.mark.asyncio
    async def test_code_default(self, session):
        """
        #TODO add comment
        """
        error_log = await ErrorLogFactory.create_async(session=session)
        assert isinstance(error_log.code, uuid.UUID)
    @pytest.mark.asyncio
    async def test_last_change_code_default_on_build(self, session):
        """
        #TODO add comment
        """
        error_log: ErrorLog = await ErrorLogFactory.build_async(session=session)
        assert error_log.last_change_code == 0
    @pytest.mark.asyncio
    async def test_last_change_code_default_on_creation(self, session):
        """
        #TODO add comment
        """
        error_log: ErrorLog = await ErrorLogFactory.create_async(session=session)
        assert error_log.last_change_code == 1
    @pytest.mark.asyncio
    async def test_last_change_code_default_on_update(self, session):
        """
        #TODO add comment
        """
        error_log = await ErrorLogFactory.create_async(session=session)
        initial_code = error_log.last_change_code
        error_log.code = uuid.uuid4()
        await session.commit()
        assert error_log.last_change_code != initial_code
    @pytest.mark.asyncio
    async def test_date_inserted_on_build(self, session):
        """
        #TODO add comment
        """
        error_log = await ErrorLogFactory.build_async(session=session)
        assert error_log.insert_utc_date_time is not None
        assert isinstance(error_log.insert_utc_date_time, datetime)
    @pytest.mark.asyncio
    async def test_date_inserted_on_initial_save(self, session):
        """
        #TODO add comment
        """
        error_log = await ErrorLogFactory.build_async(session=session)
        assert error_log.insert_utc_date_time is not None
        assert isinstance(error_log.insert_utc_date_time, datetime)
        initial_time = datetime.utcnow() + timedelta(days=-1)
        error_log.code = uuid.uuid4()
        await session.commit()
        assert error_log.insert_utc_date_time > initial_time
    @pytest.mark.asyncio
    async def test_date_inserted_on_second_save(self, session):
        """
        #TODO add comment
        """
        error_log = await ErrorLogFactory.create_async(session=session)
        assert error_log.insert_utc_date_time is not None
        assert isinstance(error_log.insert_utc_date_time, datetime)
        initial_time = error_log.insert_utc_date_time
        error_log.code = uuid.uuid4()
        time.sleep(1)
        await session.commit()
        assert error_log.insert_utc_date_time == initial_time
    @pytest.mark.asyncio
    async def test_date_updated_on_build(self, session):
        """
        #TODO add comment
        """
        error_log = await ErrorLogFactory.build_async(session=session)
        assert error_log.last_update_utc_date_time is not None
        assert isinstance(error_log.last_update_utc_date_time, datetime)
    @pytest.mark.asyncio
    async def test_date_updated_on_initial_save(self, session):
        """
        #TODO add comment
        """
        error_log = await ErrorLogFactory.build_async(session=session)
        assert error_log.last_update_utc_date_time is not None
        assert isinstance(error_log.last_update_utc_date_time, datetime)
        initial_time = datetime.utcnow() + timedelta(days=-1)
        error_log.code = uuid.uuid4()
        await session.commit()
        assert error_log.last_update_utc_date_time > initial_time
    @pytest.mark.asyncio
    async def test_date_updated_on_second_save(self, session):
        """
        #TODO add comment
        """
        error_log = await ErrorLogFactory.create_async(session=session)
        assert error_log.last_update_utc_date_time is not None
        assert isinstance(error_log.last_update_utc_date_time, datetime)
        initial_time = error_log.last_update_utc_date_time
        error_log.code = uuid.uuid4()
        time.sleep(1)
        await session.commit()
        assert error_log.last_update_utc_date_time > initial_time
    @pytest.mark.asyncio
    async def test_model_deletion(self, session):
        """
        #TODO add comment
        """
        error_log = await ErrorLogFactory.create_async(session=session)
        await session.delete(error_log)
        await session.commit()
        # Construct the select statement
        stmt = select(ErrorLog).where(ErrorLog.error_log_id == error_log.error_log_id)
        # Execute the statement asynchronously
        result = await session.execute(stmt)
        # Fetch all results
        deleted_error_log = result.scalars().first()
        # deleted_error_log = await session.query(ErrorLog).filter_by(
        # error_log_id=error_log.error_log_id).first()
        assert deleted_error_log is None
    @pytest.mark.asyncio
    async def test_data_types(self, session):
        """
        #TODO add comment
        """
        error_log = await ErrorLogFactory.create_async(session=session)
        assert isinstance(error_log.error_log_id, int)
        assert isinstance(error_log.code, uuid.UUID)
        assert isinstance(error_log.last_change_code, int)
        assert isinstance(error_log.insert_user_id, uuid.UUID)
        assert isinstance(error_log.last_update_user_id, uuid.UUID)
        assert isinstance(error_log.browser_code, uuid.UUID)
        assert isinstance(error_log.context_code, uuid.UUID)
        assert isinstance(error_log.created_utc_date_time, datetime)
        assert error_log.description == "" or isinstance(error_log.description, str)
        assert isinstance(error_log.is_client_side_error, bool)
        assert isinstance(error_log.is_resolved, bool)
        assert isinstance(error_log.pac_id, int)
        assert error_log.url == "" or isinstance(error_log.url, str)
        # Check for the peek values
# endset
        # browserCode,
        # contextCode,
        # createdUTCDateTime
        # description,
        # isClientSideError,
        # isResolved,
        # pacID
        assert isinstance(error_log.pac_code_peek, uuid.UUID)
        # url,
# endset
        assert isinstance(error_log.insert_utc_date_time, datetime)
        assert isinstance(error_log.last_update_utc_date_time, datetime)
    @pytest.mark.asyncio
    async def test_unique_code_constraint(self, session):
        """
        #TODO add comment
        """
        error_log_1 = await ErrorLogFactory.create_async(session=session)
        error_log_2 = await ErrorLogFactory.create_async(session=session)
        error_log_2.code = error_log_1.code
        session.add_all([error_log_1, error_log_2])
        with pytest.raises(Exception):
            await session.commit()
        await session.rollback()
    @pytest.mark.asyncio
    async def test_fields_default(self, session):
        """
        #TODO add comment
        """
        error_log = ErrorLog()
        assert error_log.code is not None
        assert error_log.last_change_code is not None
        assert error_log.insert_user_id is not None
        assert error_log.last_update_user_id is not None
        assert error_log.insert_utc_date_time is not None
        assert error_log.last_update_utc_date_time is not None
# endset
        # browserCode,
        # contextCode,
        # createdUTCDateTime
        # description,
        # isClientSideError,
        # isResolved,
        # PacID
        assert isinstance(error_log.pac_code_peek, uuid.UUID)
        # url,
# endset
        assert isinstance(error_log.browser_code, uuid.UUID)
        assert isinstance(error_log.context_code, uuid.UUID)
        assert error_log.created_utc_date_time == datetime(1753, 1, 1)
        assert error_log.description == ""
        assert error_log.is_client_side_error is False
        assert error_log.is_resolved is False
        assert error_log.pac_id == 0
        assert error_log.url == ""
# endset
    @pytest.mark.asyncio
    async def test_last_change_code_concurrency(self, session):
        """
        #TODO add comment
        """
        error_log = await ErrorLogFactory.create_async(session=session)
        original_last_change_code = error_log.last_change_code
        stmt = select(ErrorLog).where(ErrorLog.error_log_id == error_log.error_log_id)
        result = await session.execute(stmt)
        error_log_1 = result.scalars().first()
        # error_log_1 = await session.query(ErrorLog).filter_by(
        # error_log_id=error_log.error_log_id).first()
        error_log_1.code = uuid.uuid4()
        await session.commit()
        stmt = select(ErrorLog).where(ErrorLog.error_log_id == error_log.error_log_id)
        result = await session.execute(stmt)
        error_log_2 = result.scalars().first()
        # error_log_2 = await session.query(ErrorLog).filter_by(
        # error_log_id=error_log.error_log_id).first()
        error_log_2.code = uuid.uuid4()
        await session.commit()
        assert error_log_2.last_change_code != original_last_change_code
# endset
    # browserCode,
    # contextCode,
    # createdUTCDateTime
    # description,
    # isClientSideError,
    # isResolved,
    # PacID
    @pytest.mark.asyncio
    async def test_invalid_pac_id(self, session):
        """
        #TODO add comment
        """
        error_log = await ErrorLogFactory.create_async(session=session)
        error_log.pac_id = 99999
        with pytest.raises(IntegrityError):
            await session.commit()
        await session.rollback()
    # url,
# endset
