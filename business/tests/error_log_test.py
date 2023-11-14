import pytest
import pytest_asyncio
from datetime import datetime, date
from sqlalchemy.ext.asyncio import AsyncSession
from models import ErrorLog
from models.factory import ErrorLogFactory
from managers.error_log import ErrorLogManager
from business.error_log import ErrorLogBusObj
from services.db_config import db_dialect
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
from services.db_config import db_dialect,generate_uuid
from sqlalchemy import String
from services.logging_config import get_logger
import managers as managers_and_enums
import current_runtime

logger = get_logger(__name__)
db_dialect = "sqlite"
# Conditionally set the UUID column type
if db_dialect == 'postgresql':
    UUIDType = UUID(as_uuid=True)
elif db_dialect == 'mssql':
    UUIDType = UNIQUEIDENTIFIER
else:  # This will cover SQLite, MySQL, and other databases
    UUIDType = String(36)
class TestErrorLogBusObj:
    @pytest_asyncio.fixture(scope="function")
    async def error_log_manager(self, session:AsyncSession):
        return ErrorLogManager(session)
    @pytest_asyncio.fixture(scope="function")
    async def error_log_bus_obj(self, session):
        # Assuming that the ErrorLogBusObj requires a session object
        return ErrorLogBusObj(session)
    @pytest_asyncio.fixture(scope="function")
    async def new_error_log(self, session):
        # Use the ErrorLogFactory to create a new error_log instance
        # Assuming ErrorLogFactory.create() is an async function
        return await ErrorLogFactory.create_async(session)
    @pytest.mark.asyncio
    async def test_create_error_log(self, error_log_manager:ErrorLogManager, error_log_bus_obj:ErrorLogBusObj, new_error_log:ErrorLog):
        # Test creating a new error_log
        assert error_log_bus_obj.error_log_id is None
        # assert isinstance(error_log_bus_obj.error_log_id, int)
        if db_dialect == 'postgresql':
            assert isinstance(error_log_bus_obj.code, UUID)
        elif db_dialect == 'mssql':
            assert isinstance(error_log_bus_obj.code, UNIQUEIDENTIFIER)
        else:  # This will cover SQLite, MySQL, and other databases
            assert isinstance(error_log_bus_obj.code, str)
        assert isinstance(error_log_bus_obj.last_change_code, int)
        assert error_log_bus_obj.insert_user_id is None
        assert error_log_bus_obj.last_update_user_id is None
        #BrowserCode
        if db_dialect == 'postgresql':
            assert isinstance(error_log_bus_obj.browser_code, UUID)
        elif db_dialect == 'mssql':
            assert isinstance(error_log_bus_obj.browser_code, UNIQUEIDENTIFIER)
        else:  # This will cover SQLite, MySQL, and other databases
            assert isinstance(error_log_bus_obj.browser_code, str)
        #ContextCode
        if db_dialect == 'postgresql':
            assert isinstance(error_log_bus_obj.context_code, UUID)
        elif db_dialect == 'mssql':
            assert isinstance(error_log_bus_obj.context_code, UNIQUEIDENTIFIER)
        else:  # This will cover SQLite, MySQL, and other databases
            assert isinstance(error_log_bus_obj.context_code, str)
        assert isinstance(error_log_bus_obj.created_utc_date_time, datetime)
        assert error_log_bus_obj.description == "" or isinstance(error_log_bus_obj.description, str)
        assert isinstance(error_log_bus_obj.is_client_side_error, bool)
        assert isinstance(error_log_bus_obj.is_resolved, bool)
        assert isinstance(error_log_bus_obj.pac_id, int)
        assert error_log_bus_obj.url == "" or isinstance(error_log_bus_obj.url, str)
    @pytest.mark.asyncio
    async def test_load_with_error_log_obj(self, error_log_manager:ErrorLogManager, error_log_bus_obj:ErrorLogBusObj, new_error_log:ErrorLog):
        await error_log_bus_obj.load(error_log_obj_instance=new_error_log)
        assert error_log_manager.is_equal(error_log_bus_obj.error_log,new_error_log) == True
    @pytest.mark.asyncio
    async def test_load_with_error_log_id(self, error_log_manager:ErrorLogManager, error_log_bus_obj:ErrorLogBusObj, new_error_log:ErrorLog):
        await error_log_bus_obj.load(error_log_id=new_error_log.error_log_id)
        assert error_log_manager.is_equal(error_log_bus_obj.error_log,new_error_log)  == True
    @pytest.mark.asyncio
    async def test_load_with_error_log_code(self, error_log_manager:ErrorLogManager, error_log_bus_obj:ErrorLogBusObj, new_error_log:ErrorLog):
        await error_log_bus_obj.load(code=new_error_log.code)
        assert error_log_manager.is_equal(error_log_bus_obj.error_log,new_error_log)  == True
    @pytest.mark.asyncio
    async def test_load_with_error_log_json(self, error_log_manager:ErrorLogManager, error_log_bus_obj:ErrorLogBusObj, new_error_log:ErrorLog):
        error_log_json = error_log_manager.to_json(new_error_log)
        await error_log_bus_obj.load(json_data=error_log_json)
        assert error_log_manager.is_equal(error_log_bus_obj.error_log,new_error_log)  == True
    @pytest.mark.asyncio
    async def test_load_with_error_log_dict(self, session, error_log_manager:ErrorLogManager, error_log_bus_obj:ErrorLogBusObj, new_error_log:ErrorLog):
        logger.info("test_load_with_error_log_dict 1")
        error_log_dict = error_log_manager.to_dict(new_error_log)
        logger.info(error_log_dict)
        await error_log_bus_obj.load(error_log_dict=error_log_dict)
        assert error_log_manager.is_equal(error_log_bus_obj.error_log,new_error_log)  == True
    @pytest.mark.asyncio
    async def test_get_nonexistent_error_log(self, error_log_manager:ErrorLogManager, error_log_bus_obj:ErrorLogBusObj, new_error_log:ErrorLog):
        # Test retrieving a nonexistent error_log raises an exception
        assert await error_log_bus_obj.load(error_log_id=-1) is None # Assuming -1 is an id that wouldn't exist
    @pytest.mark.asyncio
    async def test_update_error_log(self, error_log_manager:ErrorLogManager, error_log_bus_obj:ErrorLogBusObj, new_error_log:ErrorLog):
        # Test updating a error_log's data
        new_error_log = await error_log_manager.get_by_id(new_error_log.error_log_id)
        new_code = generate_uuid()
        await error_log_bus_obj.load(error_log_obj_instance=new_error_log)
        error_log_bus_obj.code = new_code
        await error_log_bus_obj.save()
        new_error_log = await error_log_manager.get_by_id(new_error_log.error_log_id)
        assert error_log_manager.is_equal(error_log_bus_obj.error_log,new_error_log)  == True
    @pytest.mark.asyncio
    async def test_delete_error_log(self, error_log_manager:ErrorLogManager, error_log_bus_obj:ErrorLogBusObj, new_error_log:ErrorLog):
        assert new_error_log.error_log_id is not None
        assert error_log_bus_obj.error_log_id is None
        await error_log_bus_obj.load(error_log_id=new_error_log.error_log_id)
        assert error_log_bus_obj.error_log_id is not None
        await error_log_bus_obj.delete()
        new_error_log = await error_log_manager.get_by_id(new_error_log.error_log_id)
        assert new_error_log is None

