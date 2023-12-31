import asyncio
from decimal import Decimal
import pytest
import pytest_asyncio
import time
from typing import AsyncGenerator
from decimal import Decimal
from datetime import datetime, date, timedelta
from sqlalchemy import event
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from models import Base, ErrorLog
from models.factory import ErrorLogFactory
from services.db_config import db_dialect
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
from services.db_config import db_dialect,generate_uuid
from sqlalchemy import String
from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select
DATABASE_URL = "sqlite+aiosqlite:///:memory:"
db_dialect = "sqlite"
# Conditionally set the UUID column type
if db_dialect == 'postgresql':
    UUIDType = UUID(as_uuid=True)
elif db_dialect == 'mssql':
    UUIDType = UNIQUEIDENTIFIER
else:  # This will cover SQLite, MySQL, and other databases
    UUIDType = String(36)
class TestErrorLogFactoryAsync:
    @pytest.fixture(scope="function")
    def event_loop(self) -> asyncio.AbstractEventLoop:
        loop = asyncio.get_event_loop_policy().new_event_loop()
        yield loop
        loop.close()
    @pytest.fixture(scope="function")
    def engine(self):
        engine = create_async_engine(DATABASE_URL, echo=False)
        yield engine
        engine.sync_engine.dispose()
    @pytest_asyncio.fixture(scope="function")
    async def session(self,engine) -> AsyncGenerator[AsyncSession, None]:
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
        error_log = await ErrorLogFactory.create_async(session=session)
        assert error_log.error_log_id is not None
    @pytest.mark.asyncio
    async def test_code_default(self, session):
        error_log = await ErrorLogFactory.create_async(session=session)
        if db_dialect == 'postgresql':
            assert isinstance(error_log.code, UUID)
        elif db_dialect == 'mssql':
            assert isinstance(error_log.code, UNIQUEIDENTIFIER)
        else:  # This will cover SQLite, MySQL, and other databases
            assert isinstance(error_log.code, str)
    @pytest.mark.asyncio
    async def test_last_change_code_default_on_build(self, session):
        error_log:ErrorLog = await ErrorLogFactory.build_async(session=session)
        assert error_log.last_change_code == 0
    @pytest.mark.asyncio
    async def test_last_change_code_default_on_creation(self, session):
        error_log:ErrorLog = await ErrorLogFactory.create_async(session=session)
        assert error_log.last_change_code == 1
    @pytest.mark.asyncio
    async def test_last_change_code_default_on_update(self, session):
        error_log = await ErrorLogFactory.create_async(session=session)
        initial_code = error_log.last_change_code
        error_log.code = generate_uuid()
        await session.commit()
        assert error_log.last_change_code != initial_code
    @pytest.mark.asyncio
    async def test_date_inserted_on_build(self, session):
        error_log = await ErrorLogFactory.build_async(session=session)
        assert error_log.insert_utc_date_time is not None
        assert isinstance(error_log.insert_utc_date_time, datetime)
    @pytest.mark.asyncio
    async def test_date_inserted_on_initial_save(self, session):
        error_log = await ErrorLogFactory.build_async(session=session)
        assert error_log.insert_utc_date_time is not None
        assert isinstance(error_log.insert_utc_date_time, datetime)
        initial_time = datetime.utcnow() + timedelta(days=-1)
        error_log.code = generate_uuid()
        await session.commit()
        assert error_log.insert_utc_date_time > initial_time
    @pytest.mark.asyncio
    async def test_date_inserted_on_second_save(self, session):
        error_log = await ErrorLogFactory.create_async(session=session)
        assert error_log.insert_utc_date_time is not None
        assert isinstance(error_log.insert_utc_date_time, datetime)
        initial_time = error_log.insert_utc_date_time
        error_log.code = generate_uuid()
        time.sleep(1)
        await session.commit()
        assert error_log.insert_utc_date_time == initial_time
    @pytest.mark.asyncio
    async def test_date_updated_on_build(self, session):
        error_log = await ErrorLogFactory.build_async(session=session)
        assert error_log.last_update_utc_date_time is not None
        assert isinstance(error_log.last_update_utc_date_time, datetime)
    @pytest.mark.asyncio
    async def test_date_updated_on_initial_save(self, session):
        error_log = await ErrorLogFactory.build_async(session=session)
        assert error_log.last_update_utc_date_time is not None
        assert isinstance(error_log.last_update_utc_date_time, datetime)
        initial_time = datetime.utcnow() + timedelta(days=-1)
        error_log.code = generate_uuid()
        await session.commit()
        assert error_log.last_update_utc_date_time > initial_time
    @pytest.mark.asyncio
    async def test_date_updated_on_second_save(self, session):
        error_log = await ErrorLogFactory.create_async(session=session)
        assert error_log.last_update_utc_date_time is not None
        assert isinstance(error_log.last_update_utc_date_time, datetime)
        initial_time = error_log.last_update_utc_date_time
        error_log.code = generate_uuid()
        time.sleep(1)
        await session.commit()
        assert error_log.last_update_utc_date_time > initial_time
    @pytest.mark.asyncio
    async def test_model_deletion(self, session):
        error_log = await ErrorLogFactory.create_async(session=session)
        await session.delete(error_log)
        await session.commit()
        # Construct the select statement
        stmt = select(ErrorLog).where(ErrorLog.error_log_id==error_log.error_log_id)
        # Execute the statement asynchronously
        result = await session.execute(stmt)
        # Fetch all results
        deleted_error_log = result.scalars().first()
        # deleted_error_log = await session.query(ErrorLog).filter_by(error_log_id=error_log.error_log_id).first()
        assert deleted_error_log is None
    @pytest.mark.asyncio
    async def test_data_types(self, session):
        error_log = await ErrorLogFactory.create_async(session=session)
        assert isinstance(error_log.error_log_id, int)
        if db_dialect == 'postgresql':
            assert isinstance(error_log.code, UUID)
        elif db_dialect == 'mssql':
            assert isinstance(error_log.code, UNIQUEIDENTIFIER)
        else:  # This will cover SQLite, MySQL, and other databases
            assert isinstance(error_log.code, str)
        assert isinstance(error_log.last_change_code, int)
        if db_dialect == 'postgresql':
            assert isinstance(error_log.insert_user_id, UUID)
        elif db_dialect == 'mssql':
            assert isinstance(error_log.insert_user_id, UNIQUEIDENTIFIER)
        else:  # This will cover SQLite, MySQL, and other databases
            assert isinstance(error_log.insert_user_id, str)
        if db_dialect == 'postgresql':
            assert isinstance(error_log.last_update_user_id, UUID)
        elif db_dialect == 'mssql':
            assert isinstance(error_log.last_update_user_id, UNIQUEIDENTIFIER)
        else:  # This will cover SQLite, MySQL, and other databases
            assert isinstance(error_log.last_update_user_id, str)
        #BrowserCode
        if db_dialect == 'postgresql':
            assert isinstance(error_log.browser_code, UUID)
        elif db_dialect == 'mssql':
            assert isinstance(error_log.browser_code, UNIQUEIDENTIFIER)
        else:  # This will cover SQLite, MySQL, and other databases
            assert isinstance(error_log.browser_code, str)
        #ContextCode
        if db_dialect == 'postgresql':
            assert isinstance(error_log.context_code, UUID)
        elif db_dialect == 'mssql':
            assert isinstance(error_log.context_code, UNIQUEIDENTIFIER)
        else:  # This will cover SQLite, MySQL, and other databases
            assert isinstance(error_log.context_code, str)
        assert isinstance(error_log.created_utc_date_time, datetime)
        assert error_log.description == "" or isinstance(error_log.description, str)
        assert isinstance(error_log.is_client_side_error, bool)
        assert isinstance(error_log.is_resolved, bool)
        assert isinstance(error_log.pac_id, int)
        assert error_log.url == "" or isinstance(error_log.url, str)
        # Check for the peek values, assuming they are UUIDs based on your model

        #browserCode,
        #contextCode,
        #createdUTCDateTime
        #description,
        #isClientSideError,
        #isResolved,
        #pacID
        if db_dialect == 'postgresql':
            assert isinstance(error_log.pac_code_peek, UUID)
        elif db_dialect == 'mssql':
            assert isinstance(error_log.pac_code_peek, UNIQUEIDENTIFIER)
        else:  # This will cover SQLite, MySQL, and other databases
            assert isinstance(error_log.pac_code_peek, str)
        #url,

        assert isinstance(error_log.insert_utc_date_time, datetime)
        assert isinstance(error_log.last_update_utc_date_time, datetime)
    @pytest.mark.asyncio
    async def test_unique_code_constraint(self, session):
        error_log_1 = await ErrorLogFactory.create_async(session=session)
        error_log_2 = await ErrorLogFactory.create_async(session=session)
        error_log_2.code = error_log_1.code
        session.add_all([error_log_1, error_log_2])
        with pytest.raises(Exception):  # adjust for the specific DB exception you'd expect
            await session.commit()
        await session.rollback()
    @pytest.mark.asyncio
    async def test_fields_default(self, session):
        error_log = ErrorLog()
        assert error_log.code is not None
        assert error_log.last_change_code is not None
        assert error_log.insert_user_id is None
        assert error_log.last_update_user_id is None
        assert error_log.insert_utc_date_time is not None
        assert error_log.last_update_utc_date_time is not None

        #browserCode,
        #contextCode,
        #createdUTCDateTime
        #description,
        #isClientSideError,
        #isResolved,
        #PacID
        if db_dialect == 'postgresql':
            assert isinstance(error_log.pac_code_peek, UUID)
        elif db_dialect == 'mssql':
            assert isinstance(error_log.pac_code_peek, UNIQUEIDENTIFIER)
        else:  # This will cover SQLite, MySQL, and other databases
            assert isinstance(error_log.pac_code_peek, str)
        #url,

        #SomeUniqueIdentifierVal
        if db_dialect == 'postgresql':
            assert isinstance(error_log.browser_code, UUID)
        elif db_dialect == 'mssql':
            assert isinstance(error_log.browser_code, UNIQUEIDENTIFIER)
        else:  # This will cover SQLite, MySQL, and other databases
            assert isinstance(error_log.browser_code, str)
        #SomeUniqueIdentifierVal
        if db_dialect == 'postgresql':
            assert isinstance(error_log.context_code, UUID)
        elif db_dialect == 'mssql':
            assert isinstance(error_log.context_code, UNIQUEIDENTIFIER)
        else:  # This will cover SQLite, MySQL, and other databases
            assert isinstance(error_log.context_code, str)
        assert error_log.created_utc_date_time == datetime(1753, 1, 1)
        assert error_log.description == ""
        assert error_log.is_client_side_error == False
        assert error_log.is_resolved == False
        assert error_log.pac_id == 0
        assert error_log.url == ""

    @pytest.mark.asyncio
    async def test_last_change_code_concurrency(self, session):
        error_log = await ErrorLogFactory.create_async(session=session)
        original_last_change_code = error_log.last_change_code
        stmt = select(ErrorLog).where(ErrorLog.error_log_id==error_log.error_log_id)
        result = await session.execute(stmt)
        error_log_1 = result.scalars().first()
        # error_log_1 = await session.query(ErrorLog).filter_by(error_log_id=error_log.error_log_id).first()
        error_log_1.code = generate_uuid()
        await session.commit()
        stmt = select(ErrorLog).where(ErrorLog.error_log_id==error_log.error_log_id)
        result = await session.execute(stmt)
        error_log_2 = result.scalars().first()
        # error_log_2 = await session.query(ErrorLog).filter_by(error_log_id=error_log.error_log_id).first()
        error_log_2.code = generate_uuid()
        await session.commit()
        assert error_log_2.last_change_code != original_last_change_code

    #browserCode,
    #contextCode,
    #createdUTCDateTime
    #description,
    #isClientSideError,
    #isResolved,
    #PacID
    @pytest.mark.asyncio
    async def test_invalid_pac_id(self, session):
        error_log = await ErrorLogFactory.create_async(session=session)
        error_log.pac_id = 99999
        with pytest.raises(IntegrityError):  # adjust for the specific DB exception you'd expect
            await session.commit()
        await session.rollback()
    #url,

