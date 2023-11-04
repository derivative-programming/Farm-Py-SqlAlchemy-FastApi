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
from models import Base, Pac
from models.factory import PacFactory
from managers.pac import PacManager
from business.pac import PacBusObj
from models.serialization_schema.pac import PacSchema
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
class TestPacBusObj:
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
    async def pac_manager(self, session:AsyncSession):
        return PacManager(session)
    @pytest_asyncio.fixture(scope="function")
    async def pac_bus_obj(self, session):
        # Assuming that the PacBusObj requires a session object
        return PacBusObj(session)
    @pytest_asyncio.fixture(scope="function")
    async def new_pac(self, session):
        # Use the PacFactory to create a new pac instance
        # Assuming PacFactory.create() is an async function
        return await PacFactory.create_async(session)
    @pytest.mark.asyncio
    async def test_create_pac(self, pac_manager:PacManager, pac_bus_obj:PacBusObj, new_pac:Pac):
        # Test creating a new pac
        assert pac_bus_obj.pac_id is None
        # assert isinstance(pac_bus_obj.pac_id, int)
        if db_dialect == 'postgresql':
            assert isinstance(pac_bus_obj.code, UUID)
        elif db_dialect == 'mssql':
            assert isinstance(pac_bus_obj.code, UNIQUEIDENTIFIER)
        else:  # This will cover SQLite, MySQL, and other databases
            assert isinstance(pac_bus_obj.code, str)
        assert isinstance(pac_bus_obj.last_change_code, int)
        assert pac_bus_obj.insert_user_id is None
        assert pac_bus_obj.last_update_user_id is None
        assert pac_bus_obj.description == "" or isinstance(pac_bus_obj.description, str)
        assert isinstance(pac_bus_obj.display_order, int)
        assert isinstance(pac_bus_obj.is_active, bool)
        assert pac_bus_obj.lookup_enum_name == "" or isinstance(pac_bus_obj.lookup_enum_name, str)
        assert pac_bus_obj.name == "" or isinstance(pac_bus_obj.name, str)
    @pytest.mark.asyncio
    async def test_load_with_pac_obj(self, pac_manager:PacManager, pac_bus_obj:PacBusObj, new_pac:Pac):
        await pac_bus_obj.load(pac_obj_instance=new_pac)
        assert pac_manager.is_equal(pac_bus_obj.pac,new_pac) == True
    @pytest.mark.asyncio
    async def test_load_with_pac_id(self, pac_manager:PacManager, pac_bus_obj:PacBusObj, new_pac:Pac):
        await pac_bus_obj.load(pac_id=new_pac.pac_id)
        assert pac_manager.is_equal(pac_bus_obj.pac,new_pac)  == True
    @pytest.mark.asyncio
    async def test_load_with_pac_code(self, pac_manager:PacManager, pac_bus_obj:PacBusObj, new_pac:Pac):
        await pac_bus_obj.load(code=new_pac.code)
        assert pac_manager.is_equal(pac_bus_obj.pac,new_pac)  == True
    @pytest.mark.asyncio
    async def test_load_with_pac_json(self, pac_manager:PacManager, pac_bus_obj:PacBusObj, new_pac:Pac):
        pac_json = pac_manager.to_json(new_pac)
        await pac_bus_obj.load(json_data=pac_json)
        assert pac_manager.is_equal(pac_bus_obj.pac,new_pac)  == True
    # todo fix test
    @pytest.mark.asyncio
    async def test_load_with_pac_dict(self, session, pac_manager:PacManager, pac_bus_obj:PacBusObj, new_pac:Pac):
        logger.info("test_load_with_pac_dict 1")
        pac_dict = pac_manager.to_dict(new_pac)
        logger.info(pac_dict)
        await pac_bus_obj.load(pac_dict=pac_dict)
        assert pac_manager.is_equal(pac_bus_obj.pac,new_pac)  == True
    @pytest.mark.asyncio
    async def test_get_nonexistent_pac(self, pac_manager:PacManager, pac_bus_obj:PacBusObj, new_pac:Pac):
        # Test retrieving a nonexistent pac raises an exception
        assert await pac_bus_obj.load(pac_id=-1) is None # Assuming -1 is an id that wouldn't exist
    @pytest.mark.asyncio
    async def test_update_pac(self, pac_manager:PacManager, pac_bus_obj:PacBusObj, new_pac:Pac):
        # Test updating a pac's data
        new_pac = await pac_manager.get_by_id(new_pac.pac_id)
        new_code = generate_uuid()
        await pac_bus_obj.load(pac_obj_instance=new_pac)
        pac_bus_obj.code = new_code
        await pac_bus_obj.save()
        new_pac = await pac_manager.get_by_id(new_pac.pac_id)
        assert pac_manager.is_equal(pac_bus_obj.pac,new_pac)  == True
    @pytest.mark.asyncio
    async def test_delete_pac(self, pac_manager:PacManager, pac_bus_obj:PacBusObj, new_pac:Pac):
        assert new_pac.pac_id is not None
        assert pac_bus_obj.pac_id is None
        await pac_bus_obj.load(pac_id=new_pac.pac_id)
        assert pac_bus_obj.pac_id is not None
        await pac_bus_obj.delete()
        new_pac = await pac_manager.get_by_id(new_pac.pac_id)
        assert new_pac is None
