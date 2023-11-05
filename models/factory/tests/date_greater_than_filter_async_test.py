import asyncio
from decimal import Decimal
import pytest
import pytest_asyncio
import time
from decimal import Decimal
from datetime import datetime, date
from sqlalchemy import event
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from models import Base, DateGreaterThanFilter
from models.factory import DateGreaterThanFilterFactory
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
class TestDateGreaterThanFilterFactoryAsync:
    @pytest.fixture(scope="session")
    def event_loop(self) -> asyncio.AbstractEventLoop:
        loop = asyncio.get_event_loop_policy().new_event_loop()
        yield loop
        loop.close()
    @pytest.fixture(scope="session")
    def engine(self):
        engine = create_async_engine(DATABASE_URL, echo=True)
        yield engine
        engine.sync_engine.dispose()
    @pytest_asyncio.fixture(scope="session")
    async def session(self,engine) -> AsyncSession:
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
        date_greater_than_filter = await DateGreaterThanFilterFactory.create_async(session=session)
        assert date_greater_than_filter.date_greater_than_filter_id is not None
    @pytest.mark.asyncio
    async def test_code_default(self, session):
        date_greater_than_filter = await DateGreaterThanFilterFactory.create_async(session=session)
        if db_dialect == 'postgresql':
            assert isinstance(date_greater_than_filter.code, UUID)
        elif db_dialect == 'mssql':
            assert isinstance(date_greater_than_filter.code, UNIQUEIDENTIFIER)
        else:  # This will cover SQLite, MySQL, and other databases
            assert isinstance(date_greater_than_filter.code, str)
    @pytest.mark.asyncio
    async def test_last_change_code_default_on_build(self, session):
        date_greater_than_filter:DateGreaterThanFilter = await DateGreaterThanFilterFactory.build_async(session=session)
        assert date_greater_than_filter.last_change_code == 0
    @pytest.mark.asyncio
    async def test_last_change_code_default_on_creation(self, session):
        date_greater_than_filter:DateGreaterThanFilter = await DateGreaterThanFilterFactory.create_async(session=session)
        assert date_greater_than_filter.last_change_code == 1
    @pytest.mark.asyncio
    async def test_last_change_code_default_on_update(self, session):
        date_greater_than_filter = await DateGreaterThanFilterFactory.create_async(session=session)
        initial_code = date_greater_than_filter.last_change_code
        date_greater_than_filter.code = generate_uuid()
        await session.commit()
        assert date_greater_than_filter.last_change_code != initial_code
    @pytest.mark.asyncio
    async def test_date_inserted_on_build(self, session):
        date_greater_than_filter = await DateGreaterThanFilterFactory.build_async(session=session)
        assert date_greater_than_filter.insert_utc_date_time is not None
        assert isinstance(date_greater_than_filter.insert_utc_date_time, datetime)
    @pytest.mark.asyncio
    async def test_date_inserted_on_initial_save(self, session):
        date_greater_than_filter = await DateGreaterThanFilterFactory.build_async(session=session)
        assert date_greater_than_filter.insert_utc_date_time is not None
        assert isinstance(date_greater_than_filter.insert_utc_date_time, datetime)
        initial_time = date_greater_than_filter.insert_utc_date_time
        date_greater_than_filter.code = generate_uuid()
        time.sleep(1)
        await session.commit()
        assert date_greater_than_filter.insert_utc_date_time > initial_time
    @pytest.mark.asyncio
    async def test_date_inserted_on_second_save(self, session):
        date_greater_than_filter = await DateGreaterThanFilterFactory.create_async(session=session)
        assert date_greater_than_filter.insert_utc_date_time is not None
        assert isinstance(date_greater_than_filter.insert_utc_date_time, datetime)
        initial_time = date_greater_than_filter.insert_utc_date_time
        date_greater_than_filter.code = generate_uuid()
        time.sleep(1)
        await session.commit()
        assert date_greater_than_filter.insert_utc_date_time == initial_time
    @pytest.mark.asyncio
    async def test_date_updated_on_build(self, session):
        date_greater_than_filter = await DateGreaterThanFilterFactory.build_async(session=session)
        assert date_greater_than_filter.last_update_utc_date_time is not None
        assert isinstance(date_greater_than_filter.last_update_utc_date_time, datetime)
    @pytest.mark.asyncio
    async def test_date_updated_on_initial_save(self, session):
        date_greater_than_filter = await DateGreaterThanFilterFactory.build_async(session=session)
        assert date_greater_than_filter.last_update_utc_date_time is not None
        assert isinstance(date_greater_than_filter.last_update_utc_date_time, datetime)
        initial_time = date_greater_than_filter.last_update_utc_date_time
        date_greater_than_filter.code = generate_uuid()
        time.sleep(1)
        await session.commit()
        assert date_greater_than_filter.last_update_utc_date_time > initial_time
    @pytest.mark.asyncio
    async def test_date_updated_on_second_save(self, session):
        date_greater_than_filter = await DateGreaterThanFilterFactory.create_async(session=session)
        assert date_greater_than_filter.last_update_utc_date_time is not None
        assert isinstance(date_greater_than_filter.last_update_utc_date_time, datetime)
        initial_time = date_greater_than_filter.last_update_utc_date_time
        date_greater_than_filter.code = generate_uuid()
        time.sleep(1)
        await session.commit()
        assert date_greater_than_filter.last_update_utc_date_time > initial_time
    @pytest.mark.asyncio
    async def test_model_deletion(self, session):
        date_greater_than_filter = await DateGreaterThanFilterFactory.create_async(session=session)
        await session.delete(date_greater_than_filter)
        await session.commit()
        # Construct the select statement
        stmt = select(DateGreaterThanFilter).where(DateGreaterThanFilter.date_greater_than_filter_id==date_greater_than_filter.date_greater_than_filter_id)
        # Execute the statement asynchronously
        result = await session.execute(stmt)
        # Fetch all results
        deleted_date_greater_than_filter = result.scalars().first()
        # deleted_date_greater_than_filter = await session.query(DateGreaterThanFilter).filter_by(date_greater_than_filter_id=date_greater_than_filter.date_greater_than_filter_id).first()
        assert deleted_date_greater_than_filter is None
    @pytest.mark.asyncio
    async def test_data_types(self, session):
        date_greater_than_filter = await DateGreaterThanFilterFactory.create_async(session=session)
        assert isinstance(date_greater_than_filter.date_greater_than_filter_id, int)
        if db_dialect == 'postgresql':
            assert isinstance(date_greater_than_filter.code, UUID)
        elif db_dialect == 'mssql':
            assert isinstance(date_greater_than_filter.code, UNIQUEIDENTIFIER)
        else:  # This will cover SQLite, MySQL, and other databases
            assert isinstance(date_greater_than_filter.code, str)
        assert isinstance(date_greater_than_filter.last_change_code, int)
        if db_dialect == 'postgresql':
            assert isinstance(date_greater_than_filter.insert_user_id, UUID)
        elif db_dialect == 'mssql':
            assert isinstance(date_greater_than_filter.insert_user_id, UNIQUEIDENTIFIER)
        else:  # This will cover SQLite, MySQL, and other databases
            assert isinstance(date_greater_than_filter.insert_user_id, str)
        if db_dialect == 'postgresql':
            assert isinstance(date_greater_than_filter.last_update_user_id, UUID)
        elif db_dialect == 'mssql':
            assert isinstance(date_greater_than_filter.last_update_user_id, UNIQUEIDENTIFIER)
        else:  # This will cover SQLite, MySQL, and other databases
            assert isinstance(date_greater_than_filter.last_update_user_id, str)
        assert isinstance(date_greater_than_filter.day_count, int)
        assert date_greater_than_filter.description == "" or isinstance(date_greater_than_filter.description, str)
        assert isinstance(date_greater_than_filter.display_order, int)
        assert isinstance(date_greater_than_filter.is_active, bool)
        assert date_greater_than_filter.lookup_enum_name == "" or isinstance(date_greater_than_filter.lookup_enum_name, str)
        assert date_greater_than_filter.name == "" or isinstance(date_greater_than_filter.name, str)
        assert isinstance(date_greater_than_filter.pac_id, int)
        # Check for the peek values, assuming they are UUIDs based on your model

        #dayCount,
        #description,
        #displayOrder,
        #isActive,
        #lookupEnumName,
        #name,
        #pacID
        if db_dialect == 'postgresql':
            assert isinstance(date_greater_than_filter.pac_code_peek, UUID)
        elif db_dialect == 'mssql':
            assert isinstance(date_greater_than_filter.pac_code_peek, UNIQUEIDENTIFIER)
        else:  # This will cover SQLite, MySQL, and other databases
            assert isinstance(date_greater_than_filter.pac_code_peek, str)

        assert isinstance(date_greater_than_filter.insert_utc_date_time, datetime)
        assert isinstance(date_greater_than_filter.last_update_utc_date_time, datetime)
    @pytest.mark.asyncio
    async def test_unique_code_constraint(self, session):
        date_greater_than_filter_1 = await DateGreaterThanFilterFactory.create_async(session=session)
        date_greater_than_filter_2 = await DateGreaterThanFilterFactory.create_async(session=session)
        date_greater_than_filter_2.code = date_greater_than_filter_1.code
        session.add_all([date_greater_than_filter_1, date_greater_than_filter_2])
        with pytest.raises(Exception):  # adjust for the specific DB exception you'd expect
            await session.commit()
        await session.rollback()
    @pytest.mark.asyncio
    async def test_fields_default(self, session):
        date_greater_than_filter = DateGreaterThanFilter()
        assert date_greater_than_filter.code is not None
        assert date_greater_than_filter.last_change_code is not None
        assert date_greater_than_filter.insert_user_id is None
        assert date_greater_than_filter.last_update_user_id is None
        assert date_greater_than_filter.insert_utc_date_time is not None
        assert date_greater_than_filter.last_update_utc_date_time is not None

        #dayCount,
        #description,
        #displayOrder,
        #isActive,
        #lookupEnumName,
        #name,
        #PacID
        if db_dialect == 'postgresql':
            assert isinstance(date_greater_than_filter.pac_code_peek, UUID)
        elif db_dialect == 'mssql':
            assert isinstance(date_greater_than_filter.pac_code_peek, UNIQUEIDENTIFIER)
        else:  # This will cover SQLite, MySQL, and other databases
            assert isinstance(date_greater_than_filter.pac_code_peek, str)

        assert date_greater_than_filter.day_count == 0
        assert date_greater_than_filter.description == ""
        assert date_greater_than_filter.display_order == 0
        assert date_greater_than_filter.is_active == False
        assert date_greater_than_filter.lookup_enum_name == ""
        assert date_greater_than_filter.name == ""
        assert date_greater_than_filter.pac_id == 0

    @pytest.mark.asyncio
    async def test_last_change_code_concurrency(self, session):
        date_greater_than_filter = await DateGreaterThanFilterFactory.create_async(session=session)
        original_last_change_code = date_greater_than_filter.last_change_code
        stmt = select(DateGreaterThanFilter).where(DateGreaterThanFilter.date_greater_than_filter_id==date_greater_than_filter.date_greater_than_filter_id)
        result = await session.execute(stmt)
        date_greater_than_filter_1 = result.scalars().first()
        # date_greater_than_filter_1 = await session.query(DateGreaterThanFilter).filter_by(date_greater_than_filter_id=date_greater_than_filter.date_greater_than_filter_id).first()
        date_greater_than_filter_1.code = generate_uuid()
        await session.commit()
        stmt = select(DateGreaterThanFilter).where(DateGreaterThanFilter.date_greater_than_filter_id==date_greater_than_filter.date_greater_than_filter_id)
        result = await session.execute(stmt)
        date_greater_than_filter_2 = result.scalars().first()
        # date_greater_than_filter_2 = await session.query(DateGreaterThanFilter).filter_by(date_greater_than_filter_id=date_greater_than_filter.date_greater_than_filter_id).first()
        date_greater_than_filter_2.code = generate_uuid()
        await session.commit()
        assert date_greater_than_filter_2.last_change_code != original_last_change_code

    #dayCount,
    #description,
    #displayOrder,
    #isActive,
    #lookupEnumName,
    #name,
    #PacID
    @pytest.mark.asyncio
    async def test_invalid_pac_id(self, session):
        date_greater_than_filter = await DateGreaterThanFilterFactory.create_async(session=session)
        date_greater_than_filter.pac_id = 99999
        with pytest.raises(IntegrityError):  # adjust for the specific DB exception you'd expect
            await session.commit()
        await session.rollback()

