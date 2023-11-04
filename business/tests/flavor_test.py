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
from models import Base, Flavor
from models.factory import FlavorFactory
from managers.flavor import FlavorManager
from business.flavor import FlavorBusObj
from models.serialization_schema.flavor import FlavorSchema
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
class TestFlavorBusObj:
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
    async def flavor_manager(self, session:AsyncSession):
        return FlavorManager(session)
    @pytest_asyncio.fixture(scope="function")
    async def flavor_bus_obj(self, session):
        # Assuming that the FlavorBusObj requires a session object
        return FlavorBusObj(session)
    @pytest_asyncio.fixture(scope="function")
    async def new_flavor(self, session):
        # Use the FlavorFactory to create a new flavor instance
        # Assuming FlavorFactory.create() is an async function
        return await FlavorFactory.create_async(session)
    @pytest.mark.asyncio
    async def test_create_flavor(self, flavor_manager:FlavorManager, flavor_bus_obj:FlavorBusObj, new_flavor:Flavor):
        # Test creating a new flavor
        assert flavor_bus_obj.flavor_id is None
        # assert isinstance(flavor_bus_obj.flavor_id, int)
        if db_dialect == 'postgresql':
            assert isinstance(flavor_bus_obj.code, UUID)
        elif db_dialect == 'mssql':
            assert isinstance(flavor_bus_obj.code, UNIQUEIDENTIFIER)
        else:  # This will cover SQLite, MySQL, and other databases
            assert isinstance(flavor_bus_obj.code, str)
        assert isinstance(flavor_bus_obj.last_change_code, int)
        assert flavor_bus_obj.insert_user_id is None
        assert flavor_bus_obj.last_update_user_id is None
        assert flavor_bus_obj.description == "" or isinstance(flavor_bus_obj.description, str)
        assert isinstance(flavor_bus_obj.display_order, int)
        assert isinstance(flavor_bus_obj.is_active, bool)
        assert flavor_bus_obj.lookup_enum_name == "" or isinstance(flavor_bus_obj.lookup_enum_name, str)
        assert flavor_bus_obj.name == "" or isinstance(flavor_bus_obj.name, str)
        assert isinstance(flavor_bus_obj.pac_id, int)
    @pytest.mark.asyncio
    async def test_load_with_flavor_obj(self, flavor_manager:FlavorManager, flavor_bus_obj:FlavorBusObj, new_flavor:Flavor):
        await flavor_bus_obj.load(flavor_obj_instance=new_flavor)
        assert flavor_manager.is_equal(flavor_bus_obj.flavor,new_flavor) == True
    @pytest.mark.asyncio
    async def test_load_with_flavor_id(self, flavor_manager:FlavorManager, flavor_bus_obj:FlavorBusObj, new_flavor:Flavor):
        await flavor_bus_obj.load(flavor_id=new_flavor.flavor_id)
        assert flavor_manager.is_equal(flavor_bus_obj.flavor,new_flavor)  == True
    @pytest.mark.asyncio
    async def test_load_with_flavor_code(self, flavor_manager:FlavorManager, flavor_bus_obj:FlavorBusObj, new_flavor:Flavor):
        await flavor_bus_obj.load(code=new_flavor.code)
        assert flavor_manager.is_equal(flavor_bus_obj.flavor,new_flavor)  == True
    @pytest.mark.asyncio
    async def test_load_with_flavor_json(self, flavor_manager:FlavorManager, flavor_bus_obj:FlavorBusObj, new_flavor:Flavor):
        flavor_json = flavor_manager.to_json(new_flavor)
        await flavor_bus_obj.load(json_data=flavor_json)
        assert flavor_manager.is_equal(flavor_bus_obj.flavor,new_flavor)  == True
    # todo fix test
    @pytest.mark.asyncio
    async def test_load_with_flavor_dict(self, session, flavor_manager:FlavorManager, flavor_bus_obj:FlavorBusObj, new_flavor:Flavor):
        logger.info("test_load_with_flavor_dict 1")
        flavor_dict = flavor_manager.to_dict(new_flavor)
        logger.info(flavor_dict)
        await flavor_bus_obj.load(flavor_dict=flavor_dict)
        assert flavor_manager.is_equal(flavor_bus_obj.flavor,new_flavor)  == True
    @pytest.mark.asyncio
    async def test_get_nonexistent_flavor(self, flavor_manager:FlavorManager, flavor_bus_obj:FlavorBusObj, new_flavor:Flavor):
        # Test retrieving a nonexistent flavor raises an exception
        assert await flavor_bus_obj.load(flavor_id=-1) is None # Assuming -1 is an id that wouldn't exist
    @pytest.mark.asyncio
    async def test_update_flavor(self, flavor_manager:FlavorManager, flavor_bus_obj:FlavorBusObj, new_flavor:Flavor):
        # Test updating a flavor's data
        new_flavor = await flavor_manager.get_by_id(new_flavor.flavor_id)
        new_code = generate_uuid()
        await flavor_bus_obj.load(flavor_obj_instance=new_flavor)
        flavor_bus_obj.code = new_code
        await flavor_bus_obj.save()
        new_flavor = await flavor_manager.get_by_id(new_flavor.flavor_id)
        assert flavor_manager.is_equal(flavor_bus_obj.flavor,new_flavor)  == True
    @pytest.mark.asyncio
    async def test_delete_flavor(self, flavor_manager:FlavorManager, flavor_bus_obj:FlavorBusObj, new_flavor:Flavor):
        assert new_flavor.flavor_id is not None
        assert flavor_bus_obj.flavor_id is None
        await flavor_bus_obj.load(flavor_id=new_flavor.flavor_id)
        assert flavor_bus_obj.flavor_id is not None
        await flavor_bus_obj.delete()
        new_flavor = await flavor_manager.get_by_id(new_flavor.flavor_id)
        assert new_flavor is None