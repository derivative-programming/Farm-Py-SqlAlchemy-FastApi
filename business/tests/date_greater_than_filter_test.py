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
from managers.date_greater_than_filter import DateGreaterThanFilterManager
from business.date_greater_than_filter import DateGreaterThanFilterBusObj
from models.serialization_schema.date_greater_than_filter import DateGreaterThanFilterSchema
from services.db_config import db_dialect
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
from services.db_config import db_dialect,generate_uuid
from sqlalchemy import String
from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select
from services.logging_config import get_logger
logger = get_logger(__name__)
DATABASE_URL = "sqlite+aiosqlite:///:memory:"
db_dialect = "sqlite"
# Conditionally set the UUID column type
if db_dialect == 'postgresql':
    UUIDType = UUID(as_uuid=True)
elif db_dialect == 'mssql':
    UUIDType = UNIQUEIDENTIFIER
else:  # This will cover SQLite, MySQL, and other databases
    UUIDType = String(36)
class TestDateGreaterThanFilterBusObj:
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
    @pytest_asyncio.fixture(scope="function")
    async def date_greater_than_filter_manager(self, session:AsyncSession):
        return DateGreaterThanFilterManager(session)
    @pytest_asyncio.fixture(scope="function")
    async def date_greater_than_filter_bus_obj(self, session):
        # Assuming that the DateGreaterThanFilterBusObj requires a session object
        return DateGreaterThanFilterBusObj(session)
    @pytest_asyncio.fixture(scope="function")
    async def new_date_greater_than_filter(self, session):
        # Use the DateGreaterThanFilterFactory to create a new date_greater_than_filter instance
        # Assuming DateGreaterThanFilterFactory.create() is an async function
        return await DateGreaterThanFilterFactory.create_async(session)
    @pytest.mark.asyncio
    async def test_create_date_greater_than_filter(self, date_greater_than_filter_manager:DateGreaterThanFilterManager, date_greater_than_filter_bus_obj:DateGreaterThanFilterBusObj, new_date_greater_than_filter:DateGreaterThanFilter):
        # Test creating a new date_greater_than_filter
        assert date_greater_than_filter_bus_obj.date_greater_than_filter_id is None
        # assert isinstance(date_greater_than_filter_bus_obj.date_greater_than_filter_id, int)
        if db_dialect == 'postgresql':
            assert isinstance(date_greater_than_filter_bus_obj.code, UUID)
        elif db_dialect == 'mssql':
            assert isinstance(date_greater_than_filter_bus_obj.code, UNIQUEIDENTIFIER)
        else:  # This will cover SQLite, MySQL, and other databases
            assert isinstance(date_greater_than_filter_bus_obj.code, str)
        assert isinstance(date_greater_than_filter_bus_obj.last_change_code, int)
        assert date_greater_than_filter_bus_obj.insert_user_id is None
        assert date_greater_than_filter_bus_obj.last_update_user_id is None
        assert isinstance(date_greater_than_filter_bus_obj.day_count, int)
        assert date_greater_than_filter_bus_obj.description == "" or isinstance(date_greater_than_filter_bus_obj.description, str)
        assert isinstance(date_greater_than_filter_bus_obj.display_order, int)
        assert isinstance(date_greater_than_filter_bus_obj.is_active, bool)
        assert date_greater_than_filter_bus_obj.lookup_enum_name == "" or isinstance(date_greater_than_filter_bus_obj.lookup_enum_name, str)
        assert date_greater_than_filter_bus_obj.name == "" or isinstance(date_greater_than_filter_bus_obj.name, str)
        assert isinstance(date_greater_than_filter_bus_obj.pac_id, int)
    @pytest.mark.asyncio
    async def test_load_with_date_greater_than_filter_obj(self, date_greater_than_filter_manager:DateGreaterThanFilterManager, date_greater_than_filter_bus_obj:DateGreaterThanFilterBusObj, new_date_greater_than_filter:DateGreaterThanFilter):
        await date_greater_than_filter_bus_obj.load(date_greater_than_filter_obj_instance=new_date_greater_than_filter)
        assert date_greater_than_filter_manager.is_equal(date_greater_than_filter_bus_obj.date_greater_than_filter,new_date_greater_than_filter) == True
    @pytest.mark.asyncio
    async def test_load_with_date_greater_than_filter_id(self, date_greater_than_filter_manager:DateGreaterThanFilterManager, date_greater_than_filter_bus_obj:DateGreaterThanFilterBusObj, new_date_greater_than_filter:DateGreaterThanFilter):
        await date_greater_than_filter_bus_obj.load(date_greater_than_filter_id=new_date_greater_than_filter.date_greater_than_filter_id)
        assert date_greater_than_filter_manager.is_equal(date_greater_than_filter_bus_obj.date_greater_than_filter,new_date_greater_than_filter)  == True
    @pytest.mark.asyncio
    async def test_load_with_date_greater_than_filter_code(self, date_greater_than_filter_manager:DateGreaterThanFilterManager, date_greater_than_filter_bus_obj:DateGreaterThanFilterBusObj, new_date_greater_than_filter:DateGreaterThanFilter):
        await date_greater_than_filter_bus_obj.load(code=new_date_greater_than_filter.code)
        assert date_greater_than_filter_manager.is_equal(date_greater_than_filter_bus_obj.date_greater_than_filter,new_date_greater_than_filter)  == True
    @pytest.mark.asyncio
    async def test_load_with_date_greater_than_filter_json(self, date_greater_than_filter_manager:DateGreaterThanFilterManager, date_greater_than_filter_bus_obj:DateGreaterThanFilterBusObj, new_date_greater_than_filter:DateGreaterThanFilter):
        date_greater_than_filter_json = date_greater_than_filter_manager.to_json(new_date_greater_than_filter)
        await date_greater_than_filter_bus_obj.load(json_data=date_greater_than_filter_json)
        assert date_greater_than_filter_manager.is_equal(date_greater_than_filter_bus_obj.date_greater_than_filter,new_date_greater_than_filter)  == True
    # todo fix test
    @pytest.mark.asyncio
    async def test_load_with_date_greater_than_filter_dict(self, session, date_greater_than_filter_manager:DateGreaterThanFilterManager, date_greater_than_filter_bus_obj:DateGreaterThanFilterBusObj, new_date_greater_than_filter:DateGreaterThanFilter):
        logger.info("test_load_with_date_greater_than_filter_dict 1")
        date_greater_than_filter_dict = date_greater_than_filter_manager.to_dict(new_date_greater_than_filter)
        logger.info(date_greater_than_filter_dict)
        await date_greater_than_filter_bus_obj.load(date_greater_than_filter_dict=date_greater_than_filter_dict)
        assert date_greater_than_filter_manager.is_equal(date_greater_than_filter_bus_obj.date_greater_than_filter,new_date_greater_than_filter)  == True
    @pytest.mark.asyncio
    async def test_get_nonexistent_date_greater_than_filter(self, date_greater_than_filter_manager:DateGreaterThanFilterManager, date_greater_than_filter_bus_obj:DateGreaterThanFilterBusObj, new_date_greater_than_filter:DateGreaterThanFilter):
        # Test retrieving a nonexistent date_greater_than_filter raises an exception
        assert await date_greater_than_filter_bus_obj.load(date_greater_than_filter_id=-1) is None # Assuming -1 is an id that wouldn't exist
    @pytest.mark.asyncio
    async def test_update_date_greater_than_filter(self, date_greater_than_filter_manager:DateGreaterThanFilterManager, date_greater_than_filter_bus_obj:DateGreaterThanFilterBusObj, new_date_greater_than_filter:DateGreaterThanFilter):
        # Test updating a date_greater_than_filter's data
        new_date_greater_than_filter = await date_greater_than_filter_manager.get_by_id(new_date_greater_than_filter.date_greater_than_filter_id)
        new_code = generate_uuid()
        await date_greater_than_filter_bus_obj.load(date_greater_than_filter_obj_instance=new_date_greater_than_filter)
        date_greater_than_filter_bus_obj.code = new_code
        await date_greater_than_filter_bus_obj.save()
        new_date_greater_than_filter = await date_greater_than_filter_manager.get_by_id(new_date_greater_than_filter.date_greater_than_filter_id)
        assert date_greater_than_filter_manager.is_equal(date_greater_than_filter_bus_obj.date_greater_than_filter,new_date_greater_than_filter)  == True
    @pytest.mark.asyncio
    async def test_delete_date_greater_than_filter(self, date_greater_than_filter_manager:DateGreaterThanFilterManager, date_greater_than_filter_bus_obj:DateGreaterThanFilterBusObj, new_date_greater_than_filter:DateGreaterThanFilter):
        assert new_date_greater_than_filter.date_greater_than_filter_id is not None
        assert date_greater_than_filter_bus_obj.date_greater_than_filter_id is None
        await date_greater_than_filter_bus_obj.load(date_greater_than_filter_id=new_date_greater_than_filter.date_greater_than_filter_id)
        assert date_greater_than_filter_bus_obj.date_greater_than_filter_id is not None
        await date_greater_than_filter_bus_obj.delete()
        new_date_greater_than_filter = await date_greater_than_filter_manager.get_by_id(new_date_greater_than_filter.date_greater_than_filter_id)
        assert new_date_greater_than_filter is None
