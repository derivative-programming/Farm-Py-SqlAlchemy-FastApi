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
from models import Base, Tac
from models.factory import TacFactory
from managers.tac import TacManager
from business.tac import TacBusObj
from models.serialization_schema.tac import TacSchema
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
class TestTacBusObj:
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
    async def tac_manager(self, session:AsyncSession):
        return TacManager(session)
    @pytest_asyncio.fixture(scope="function")
    async def tac_bus_obj(self, session):
        # Assuming that the TacBusObj requires a session object
        return TacBusObj(session)
    @pytest_asyncio.fixture(scope="function")
    async def new_tac(self, session):
        # Use the TacFactory to create a new tac instance
        # Assuming TacFactory.create() is an async function
        return await TacFactory.create_async(session)
    @pytest.mark.asyncio
    async def test_create_tac(self, tac_manager:TacManager, tac_bus_obj:TacBusObj, new_tac:Tac):
        # Test creating a new tac
        assert tac_bus_obj.tac_id is None
        # assert isinstance(tac_bus_obj.tac_id, int)
        if db_dialect == 'postgresql':
            assert isinstance(tac_bus_obj.code, UUID)
        elif db_dialect == 'mssql':
            assert isinstance(tac_bus_obj.code, UNIQUEIDENTIFIER)
        else:  # This will cover SQLite, MySQL, and other databases
            assert isinstance(tac_bus_obj.code, str)
        assert isinstance(tac_bus_obj.last_change_code, int)
        assert tac_bus_obj.insert_user_id is None
        assert tac_bus_obj.last_update_user_id is None
        assert tac_bus_obj.description == "" or isinstance(tac_bus_obj.description, str)
        assert isinstance(tac_bus_obj.display_order, int)
        assert isinstance(tac_bus_obj.is_active, bool)
        assert tac_bus_obj.lookup_enum_name == "" or isinstance(tac_bus_obj.lookup_enum_name, str)
        assert tac_bus_obj.name == "" or isinstance(tac_bus_obj.name, str)
        assert isinstance(tac_bus_obj.pac_id, int)
    @pytest.mark.asyncio
    async def test_load_with_tac_obj(self, tac_manager:TacManager, tac_bus_obj:TacBusObj, new_tac:Tac):
        await tac_bus_obj.load(tac_obj_instance=new_tac)
        assert tac_manager.is_equal(tac_bus_obj.tac,new_tac) == True
    @pytest.mark.asyncio
    async def test_load_with_tac_id(self, tac_manager:TacManager, tac_bus_obj:TacBusObj, new_tac:Tac):
        await tac_bus_obj.load(tac_id=new_tac.tac_id)
        assert tac_manager.is_equal(tac_bus_obj.tac,new_tac)  == True
    @pytest.mark.asyncio
    async def test_load_with_tac_code(self, tac_manager:TacManager, tac_bus_obj:TacBusObj, new_tac:Tac):
        await tac_bus_obj.load(code=new_tac.code)
        assert tac_manager.is_equal(tac_bus_obj.tac,new_tac)  == True
    @pytest.mark.asyncio
    async def test_load_with_tac_json(self, tac_manager:TacManager, tac_bus_obj:TacBusObj, new_tac:Tac):
        tac_json = tac_manager.to_json(new_tac)
        await tac_bus_obj.load(json_data=tac_json)
        assert tac_manager.is_equal(tac_bus_obj.tac,new_tac)  == True
    @pytest.mark.asyncio
    async def test_load_with_tac_dict(self, session, tac_manager:TacManager, tac_bus_obj:TacBusObj, new_tac:Tac):
        logger.info("test_load_with_tac_dict 1")
        tac_dict = tac_manager.to_dict(new_tac)
        logger.info(tac_dict)
        await tac_bus_obj.load(tac_dict=tac_dict)
        assert tac_manager.is_equal(tac_bus_obj.tac,new_tac)  == True
    @pytest.mark.asyncio
    async def test_get_nonexistent_tac(self, tac_manager:TacManager, tac_bus_obj:TacBusObj, new_tac:Tac):
        # Test retrieving a nonexistent tac raises an exception
        assert await tac_bus_obj.load(tac_id=-1) is None # Assuming -1 is an id that wouldn't exist
    @pytest.mark.asyncio
    async def test_update_tac(self, tac_manager:TacManager, tac_bus_obj:TacBusObj, new_tac:Tac):
        # Test updating a tac's data
        new_tac = await tac_manager.get_by_id(new_tac.tac_id)
        new_code = generate_uuid()
        await tac_bus_obj.load(tac_obj_instance=new_tac)
        tac_bus_obj.code = new_code
        await tac_bus_obj.save()
        new_tac = await tac_manager.get_by_id(new_tac.tac_id)
        assert tac_manager.is_equal(tac_bus_obj.tac,new_tac)  == True
    @pytest.mark.asyncio
    async def test_delete_tac(self, tac_manager:TacManager, tac_bus_obj:TacBusObj, new_tac:Tac):
        assert new_tac.tac_id is not None
        assert tac_bus_obj.tac_id is None
        await tac_bus_obj.load(tac_id=new_tac.tac_id)
        assert tac_bus_obj.tac_id is not None
        await tac_bus_obj.delete()
        new_tac = await tac_manager.get_by_id(new_tac.tac_id)
        assert new_tac is None
