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
from models import Base, TriStateFilter
from models.factory import TriStateFilterFactory
from managers.tri_state_filter import TriStateFilterManager
from business.tri_state_filter import TriStateFilterBusObj
from models.serialization_schema.tri_state_filter import TriStateFilterSchema
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
class TestTriStateFilterBusObj:
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
    async def tri_state_filter_manager(self, session:AsyncSession):
        return TriStateFilterManager(session)
    @pytest_asyncio.fixture(scope="function")
    async def tri_state_filter_bus_obj(self, session):
        # Assuming that the TriStateFilterBusObj requires a session object
        return TriStateFilterBusObj(session)
    @pytest_asyncio.fixture(scope="function")
    async def new_tri_state_filter(self, session):
        # Use the TriStateFilterFactory to create a new tri_state_filter instance
        # Assuming TriStateFilterFactory.create() is an async function
        return await TriStateFilterFactory.create_async(session)
    @pytest.mark.asyncio
    async def test_create_tri_state_filter(self, tri_state_filter_manager:TriStateFilterManager, tri_state_filter_bus_obj:TriStateFilterBusObj, new_tri_state_filter:TriStateFilter):
        # Test creating a new tri_state_filter
        assert tri_state_filter_bus_obj.tri_state_filter_id is None
        # assert isinstance(tri_state_filter_bus_obj.tri_state_filter_id, int)
        if db_dialect == 'postgresql':
            assert isinstance(tri_state_filter_bus_obj.code, UUID)
        elif db_dialect == 'mssql':
            assert isinstance(tri_state_filter_bus_obj.code, UNIQUEIDENTIFIER)
        else:  # This will cover SQLite, MySQL, and other databases
            assert isinstance(tri_state_filter_bus_obj.code, str)
        assert isinstance(tri_state_filter_bus_obj.last_change_code, int)
        assert tri_state_filter_bus_obj.insert_user_id is None
        assert tri_state_filter_bus_obj.last_update_user_id is None
        assert tri_state_filter_bus_obj.description == "" or isinstance(tri_state_filter_bus_obj.description, str)
        assert isinstance(tri_state_filter_bus_obj.display_order, int)
        assert isinstance(tri_state_filter_bus_obj.is_active, bool)
        assert tri_state_filter_bus_obj.lookup_enum_name == "" or isinstance(tri_state_filter_bus_obj.lookup_enum_name, str)
        assert tri_state_filter_bus_obj.name == "" or isinstance(tri_state_filter_bus_obj.name, str)
        assert isinstance(tri_state_filter_bus_obj.pac_id, int)
        assert isinstance(tri_state_filter_bus_obj.state_int_value, int)
    @pytest.mark.asyncio
    async def test_load_with_tri_state_filter_obj(self, tri_state_filter_manager:TriStateFilterManager, tri_state_filter_bus_obj:TriStateFilterBusObj, new_tri_state_filter:TriStateFilter):
        await tri_state_filter_bus_obj.load(tri_state_filter_obj_instance=new_tri_state_filter)
        assert tri_state_filter_manager.is_equal(tri_state_filter_bus_obj.tri_state_filter,new_tri_state_filter) == True
    @pytest.mark.asyncio
    async def test_load_with_tri_state_filter_id(self, tri_state_filter_manager:TriStateFilterManager, tri_state_filter_bus_obj:TriStateFilterBusObj, new_tri_state_filter:TriStateFilter):
        await tri_state_filter_bus_obj.load(tri_state_filter_id=new_tri_state_filter.tri_state_filter_id)
        assert tri_state_filter_manager.is_equal(tri_state_filter_bus_obj.tri_state_filter,new_tri_state_filter)  == True
    @pytest.mark.asyncio
    async def test_load_with_tri_state_filter_code(self, tri_state_filter_manager:TriStateFilterManager, tri_state_filter_bus_obj:TriStateFilterBusObj, new_tri_state_filter:TriStateFilter):
        await tri_state_filter_bus_obj.load(code=new_tri_state_filter.code)
        assert tri_state_filter_manager.is_equal(tri_state_filter_bus_obj.tri_state_filter,new_tri_state_filter)  == True
    @pytest.mark.asyncio
    async def test_load_with_tri_state_filter_json(self, tri_state_filter_manager:TriStateFilterManager, tri_state_filter_bus_obj:TriStateFilterBusObj, new_tri_state_filter:TriStateFilter):
        tri_state_filter_json = tri_state_filter_manager.to_json(new_tri_state_filter)
        await tri_state_filter_bus_obj.load(json_data=tri_state_filter_json)
        assert tri_state_filter_manager.is_equal(tri_state_filter_bus_obj.tri_state_filter,new_tri_state_filter)  == True
    @pytest.mark.asyncio
    async def test_load_with_tri_state_filter_dict(self, session, tri_state_filter_manager:TriStateFilterManager, tri_state_filter_bus_obj:TriStateFilterBusObj, new_tri_state_filter:TriStateFilter):
        logger.info("test_load_with_tri_state_filter_dict 1")
        tri_state_filter_dict = tri_state_filter_manager.to_dict(new_tri_state_filter)
        logger.info(tri_state_filter_dict)
        await tri_state_filter_bus_obj.load(tri_state_filter_dict=tri_state_filter_dict)
        assert tri_state_filter_manager.is_equal(tri_state_filter_bus_obj.tri_state_filter,new_tri_state_filter)  == True
    @pytest.mark.asyncio
    async def test_get_nonexistent_tri_state_filter(self, tri_state_filter_manager:TriStateFilterManager, tri_state_filter_bus_obj:TriStateFilterBusObj, new_tri_state_filter:TriStateFilter):
        # Test retrieving a nonexistent tri_state_filter raises an exception
        assert await tri_state_filter_bus_obj.load(tri_state_filter_id=-1) is None # Assuming -1 is an id that wouldn't exist
    @pytest.mark.asyncio
    async def test_update_tri_state_filter(self, tri_state_filter_manager:TriStateFilterManager, tri_state_filter_bus_obj:TriStateFilterBusObj, new_tri_state_filter:TriStateFilter):
        # Test updating a tri_state_filter's data
        new_tri_state_filter = await tri_state_filter_manager.get_by_id(new_tri_state_filter.tri_state_filter_id)
        new_code = generate_uuid()
        await tri_state_filter_bus_obj.load(tri_state_filter_obj_instance=new_tri_state_filter)
        tri_state_filter_bus_obj.code = new_code
        await tri_state_filter_bus_obj.save()
        new_tri_state_filter = await tri_state_filter_manager.get_by_id(new_tri_state_filter.tri_state_filter_id)
        assert tri_state_filter_manager.is_equal(tri_state_filter_bus_obj.tri_state_filter,new_tri_state_filter)  == True
    @pytest.mark.asyncio
    async def test_delete_tri_state_filter(self, tri_state_filter_manager:TriStateFilterManager, tri_state_filter_bus_obj:TriStateFilterBusObj, new_tri_state_filter:TriStateFilter):
        assert new_tri_state_filter.tri_state_filter_id is not None
        assert tri_state_filter_bus_obj.tri_state_filter_id is None
        await tri_state_filter_bus_obj.load(tri_state_filter_id=new_tri_state_filter.tri_state_filter_id)
        assert tri_state_filter_bus_obj.tri_state_filter_id is not None
        await tri_state_filter_bus_obj.delete()
        new_tri_state_filter = await tri_state_filter_manager.get_by_id(new_tri_state_filter.tri_state_filter_id)
        assert new_tri_state_filter is None
