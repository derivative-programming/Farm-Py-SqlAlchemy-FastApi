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
from models import Base, Land
from models.factory import LandFactory
from managers.land import LandManager
from business.land import LandBusObj
from models.serialization_schema.land import LandSchema
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
class TestLandBusObj:
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
    async def land_manager(self, session:AsyncSession):
        return LandManager(session)
    @pytest_asyncio.fixture(scope="function")
    async def land_bus_obj(self, session):
        # Assuming that the LandBusObj requires a session object
        return LandBusObj(session)
    @pytest_asyncio.fixture(scope="function")
    async def new_land(self, session):
        # Use the LandFactory to create a new land instance
        # Assuming LandFactory.create() is an async function
        return await LandFactory.create_async(session)
    @pytest.mark.asyncio
    async def test_create_land(self, land_manager:LandManager, land_bus_obj:LandBusObj, new_land:Land):
        # Test creating a new land
        assert land_bus_obj.land_id is None
        # assert isinstance(land_bus_obj.land_id, int)
        if db_dialect == 'postgresql':
            assert isinstance(land_bus_obj.code, UUID)
        elif db_dialect == 'mssql':
            assert isinstance(land_bus_obj.code, UNIQUEIDENTIFIER)
        else:  # This will cover SQLite, MySQL, and other databases
            assert isinstance(land_bus_obj.code, str)
        assert isinstance(land_bus_obj.last_change_code, int)
        assert land_bus_obj.insert_user_id is None
        assert land_bus_obj.last_update_user_id is None
        assert land_bus_obj.description == "" or isinstance(land_bus_obj.description, str)
        assert isinstance(land_bus_obj.display_order, int)
        assert isinstance(land_bus_obj.is_active, bool)
        assert land_bus_obj.lookup_enum_name == "" or isinstance(land_bus_obj.lookup_enum_name, str)
        assert land_bus_obj.name == "" or isinstance(land_bus_obj.name, str)
        assert isinstance(land_bus_obj.pac_id, int)
    @pytest.mark.asyncio
    async def test_load_with_land_obj(self, land_manager:LandManager, land_bus_obj:LandBusObj, new_land:Land):
        await land_bus_obj.load(land_obj_instance=new_land)
        assert land_manager.is_equal(land_bus_obj.land,new_land) == True
    @pytest.mark.asyncio
    async def test_load_with_land_id(self, land_manager:LandManager, land_bus_obj:LandBusObj, new_land:Land):
        await land_bus_obj.load(land_id=new_land.land_id)
        assert land_manager.is_equal(land_bus_obj.land,new_land)  == True
    @pytest.mark.asyncio
    async def test_load_with_land_code(self, land_manager:LandManager, land_bus_obj:LandBusObj, new_land:Land):
        await land_bus_obj.load(code=new_land.code)
        assert land_manager.is_equal(land_bus_obj.land,new_land)  == True
    @pytest.mark.asyncio
    async def test_load_with_land_json(self, land_manager:LandManager, land_bus_obj:LandBusObj, new_land:Land):
        land_json = land_manager.to_json(new_land)
        await land_bus_obj.load(json_data=land_json)
        assert land_manager.is_equal(land_bus_obj.land,new_land)  == True
    @pytest.mark.asyncio
    async def test_load_with_land_dict(self, session, land_manager:LandManager, land_bus_obj:LandBusObj, new_land:Land):
        logger.info("test_load_with_land_dict 1")
        land_dict = land_manager.to_dict(new_land)
        logger.info(land_dict)
        await land_bus_obj.load(land_dict=land_dict)
        assert land_manager.is_equal(land_bus_obj.land,new_land)  == True
    @pytest.mark.asyncio
    async def test_get_nonexistent_land(self, land_manager:LandManager, land_bus_obj:LandBusObj, new_land:Land):
        # Test retrieving a nonexistent land raises an exception
        assert await land_bus_obj.load(land_id=-1) is None # Assuming -1 is an id that wouldn't exist
    @pytest.mark.asyncio
    async def test_update_land(self, land_manager:LandManager, land_bus_obj:LandBusObj, new_land:Land):
        # Test updating a land's data
        new_land = await land_manager.get_by_id(new_land.land_id)
        new_code = generate_uuid()
        await land_bus_obj.load(land_obj_instance=new_land)
        land_bus_obj.code = new_code
        await land_bus_obj.save()
        new_land = await land_manager.get_by_id(new_land.land_id)
        assert land_manager.is_equal(land_bus_obj.land,new_land)  == True
    @pytest.mark.asyncio
    async def test_delete_land(self, land_manager:LandManager, land_bus_obj:LandBusObj, new_land:Land):
        assert new_land.land_id is not None
        assert land_bus_obj.land_id is None
        await land_bus_obj.load(land_id=new_land.land_id)
        assert land_bus_obj.land_id is not None
        await land_bus_obj.delete()
        new_land = await land_manager.get_by_id(new_land.land_id)
        assert new_land is None
