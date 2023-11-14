import pytest
import pytest_asyncio
from datetime import datetime, date
from sqlalchemy.ext.asyncio import AsyncSession
from models import OrgApiKey
from models.factory import OrgApiKeyFactory
from managers.org_api_key import OrgApiKeyManager
from business.org_api_key import OrgApiKeyBusObj
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
class TestOrgApiKeyBusObj:
    @pytest_asyncio.fixture(scope="function")
    async def org_api_key_manager(self, session:AsyncSession):
        return OrgApiKeyManager(session)
    @pytest_asyncio.fixture(scope="function")
    async def org_api_key_bus_obj(self, session):
        # Assuming that the OrgApiKeyBusObj requires a session object
        return OrgApiKeyBusObj(session)
    @pytest_asyncio.fixture(scope="function")
    async def new_org_api_key(self, session):
        # Use the OrgApiKeyFactory to create a new org_api_key instance
        # Assuming OrgApiKeyFactory.create() is an async function
        return await OrgApiKeyFactory.create_async(session)
    @pytest.mark.asyncio
    async def test_create_org_api_key(self, org_api_key_manager:OrgApiKeyManager, org_api_key_bus_obj:OrgApiKeyBusObj, new_org_api_key:OrgApiKey):
        # Test creating a new org_api_key
        assert org_api_key_bus_obj.org_api_key_id is None
        # assert isinstance(org_api_key_bus_obj.org_api_key_id, int)
        if db_dialect == 'postgresql':
            assert isinstance(org_api_key_bus_obj.code, UUID)
        elif db_dialect == 'mssql':
            assert isinstance(org_api_key_bus_obj.code, UNIQUEIDENTIFIER)
        else:  # This will cover SQLite, MySQL, and other databases
            assert isinstance(org_api_key_bus_obj.code, str)
        assert isinstance(org_api_key_bus_obj.last_change_code, int)
        assert org_api_key_bus_obj.insert_user_id is None
        assert org_api_key_bus_obj.last_update_user_id is None
        assert org_api_key_bus_obj.api_key_value == "" or isinstance(org_api_key_bus_obj.api_key_value, str)
        assert org_api_key_bus_obj.created_by == "" or isinstance(org_api_key_bus_obj.created_by, str)
        assert isinstance(org_api_key_bus_obj.created_utc_date_time, datetime)
        assert isinstance(org_api_key_bus_obj.expiration_utc_date_time, datetime)
        assert isinstance(org_api_key_bus_obj.is_active, bool)
        assert isinstance(org_api_key_bus_obj.is_temp_user_key, bool)
        assert org_api_key_bus_obj.name == "" or isinstance(org_api_key_bus_obj.name, str)
        assert isinstance(org_api_key_bus_obj.organization_id, int)
        assert isinstance(org_api_key_bus_obj.org_customer_id, int)
    @pytest.mark.asyncio
    async def test_load_with_org_api_key_obj(self, org_api_key_manager:OrgApiKeyManager, org_api_key_bus_obj:OrgApiKeyBusObj, new_org_api_key:OrgApiKey):
        await org_api_key_bus_obj.load(org_api_key_obj_instance=new_org_api_key)
        assert org_api_key_manager.is_equal(org_api_key_bus_obj.org_api_key,new_org_api_key) == True
    @pytest.mark.asyncio
    async def test_load_with_org_api_key_id(self, org_api_key_manager:OrgApiKeyManager, org_api_key_bus_obj:OrgApiKeyBusObj, new_org_api_key:OrgApiKey):
        await org_api_key_bus_obj.load(org_api_key_id=new_org_api_key.org_api_key_id)
        assert org_api_key_manager.is_equal(org_api_key_bus_obj.org_api_key,new_org_api_key)  == True
    @pytest.mark.asyncio
    async def test_load_with_org_api_key_code(self, org_api_key_manager:OrgApiKeyManager, org_api_key_bus_obj:OrgApiKeyBusObj, new_org_api_key:OrgApiKey):
        await org_api_key_bus_obj.load(code=new_org_api_key.code)
        assert org_api_key_manager.is_equal(org_api_key_bus_obj.org_api_key,new_org_api_key)  == True
    @pytest.mark.asyncio
    async def test_load_with_org_api_key_json(self, org_api_key_manager:OrgApiKeyManager, org_api_key_bus_obj:OrgApiKeyBusObj, new_org_api_key:OrgApiKey):
        org_api_key_json = org_api_key_manager.to_json(new_org_api_key)
        await org_api_key_bus_obj.load(json_data=org_api_key_json)
        assert org_api_key_manager.is_equal(org_api_key_bus_obj.org_api_key,new_org_api_key)  == True
    @pytest.mark.asyncio
    async def test_load_with_org_api_key_dict(self, session, org_api_key_manager:OrgApiKeyManager, org_api_key_bus_obj:OrgApiKeyBusObj, new_org_api_key:OrgApiKey):
        logger.info("test_load_with_org_api_key_dict 1")
        org_api_key_dict = org_api_key_manager.to_dict(new_org_api_key)
        logger.info(org_api_key_dict)
        await org_api_key_bus_obj.load(org_api_key_dict=org_api_key_dict)
        assert org_api_key_manager.is_equal(org_api_key_bus_obj.org_api_key,new_org_api_key)  == True
    @pytest.mark.asyncio
    async def test_get_nonexistent_org_api_key(self, org_api_key_manager:OrgApiKeyManager, org_api_key_bus_obj:OrgApiKeyBusObj, new_org_api_key:OrgApiKey):
        # Test retrieving a nonexistent org_api_key raises an exception
        assert await org_api_key_bus_obj.load(org_api_key_id=-1) is None # Assuming -1 is an id that wouldn't exist
    @pytest.mark.asyncio
    async def test_update_org_api_key(self, org_api_key_manager:OrgApiKeyManager, org_api_key_bus_obj:OrgApiKeyBusObj, new_org_api_key:OrgApiKey):
        # Test updating a org_api_key's data
        new_org_api_key = await org_api_key_manager.get_by_id(new_org_api_key.org_api_key_id)
        new_code = generate_uuid()
        await org_api_key_bus_obj.load(org_api_key_obj_instance=new_org_api_key)
        org_api_key_bus_obj.code = new_code
        await org_api_key_bus_obj.save()
        new_org_api_key = await org_api_key_manager.get_by_id(new_org_api_key.org_api_key_id)
        assert org_api_key_manager.is_equal(org_api_key_bus_obj.org_api_key,new_org_api_key)  == True
    @pytest.mark.asyncio
    async def test_delete_org_api_key(self, org_api_key_manager:OrgApiKeyManager, org_api_key_bus_obj:OrgApiKeyBusObj, new_org_api_key:OrgApiKey):
        assert new_org_api_key.org_api_key_id is not None
        assert org_api_key_bus_obj.org_api_key_id is None
        await org_api_key_bus_obj.load(org_api_key_id=new_org_api_key.org_api_key_id)
        assert org_api_key_bus_obj.org_api_key_id is not None
        await org_api_key_bus_obj.delete()
        new_org_api_key = await org_api_key_manager.get_by_id(new_org_api_key.org_api_key_id)
        assert new_org_api_key is None

