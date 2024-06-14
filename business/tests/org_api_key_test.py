# business/tests/org_api_key_test.py
"""
    #TODO add comment
"""
import uuid
from datetime import datetime, date
from sqlalchemy.ext.asyncio import AsyncSession
import pytest
import pytest_asyncio
from helpers.session_context import SessionContext
from models import OrgApiKey
from models.factory import OrgApiKeyFactory
from managers.org_api_key import OrgApiKeyManager
from business.org_api_key import OrgApiKeyBusObj
from services.logging_config import get_logger
import managers as managers_and_enums
import current_runtime

logger = get_logger(__name__)
class TestOrgApiKeyBusObj:
    """
        #TODO add comment
    """
    @pytest_asyncio.fixture(scope="function")
    async def org_api_key_manager(self, session: AsyncSession):
        """
            #TODO add comment
        """
        session_context = SessionContext(dict(), session)
        return OrgApiKeyManager(session_context)
    @pytest_asyncio.fixture(scope="function")
    async def org_api_key_bus_obj(self, session):
        """
            #TODO add comment
        """
        session_context = SessionContext(dict(), session)
        return OrgApiKeyBusObj(session_context)
    @pytest_asyncio.fixture(scope="function")
    async def new_org_api_key(self, session):
        """
            #TODO add comment
        """
        # Use the OrgApiKeyFactory to create a new org_api_key instance
        # Assuming OrgApiKeyFactory.create() is an async function
        return await OrgApiKeyFactory.create_async(session)
    @pytest.mark.asyncio
    async def test_create_org_api_key(
        self,
        org_api_key_bus_obj: OrgApiKeyBusObj
    ):
        """
            #TODO add comment
        """
        # Test creating a new org_api_key
        assert org_api_key_bus_obj.org_api_key_id is None
        # assert isinstance(org_api_key_bus_obj.org_api_key_id, int)
        assert isinstance(org_api_key_bus_obj.code, uuid.UUID)
        assert isinstance(org_api_key_bus_obj.last_change_code, int)
        assert org_api_key_bus_obj.insert_user_id == uuid.UUID(int=0)
        assert org_api_key_bus_obj.last_update_user_id == uuid.UUID(int=0)
        assert isinstance(org_api_key_bus_obj.api_key_value, str)
        assert isinstance(org_api_key_bus_obj.created_by, str)
        assert isinstance(org_api_key_bus_obj.created_utc_date_time, datetime)
        assert isinstance(org_api_key_bus_obj.expiration_utc_date_time, datetime)
        assert isinstance(org_api_key_bus_obj.is_active, bool)
        assert isinstance(org_api_key_bus_obj.is_temp_user_key, bool)
        assert isinstance(org_api_key_bus_obj.name, str)
        assert isinstance(org_api_key_bus_obj.organization_id, int)
        assert isinstance(org_api_key_bus_obj.org_customer_id, int)
    @pytest.mark.asyncio
    async def test_load_with_org_api_key_obj(
        self,
        org_api_key_manager: OrgApiKeyManager,
        org_api_key_bus_obj: OrgApiKeyBusObj,
        new_org_api_key: OrgApiKey
    ):
        """
            #TODO add comment
        """
        await org_api_key_bus_obj.load_from_obj_instance(new_org_api_key)
        assert org_api_key_manager.is_equal(org_api_key_bus_obj.org_api_key, new_org_api_key) is True
    @pytest.mark.asyncio
    async def test_load_with_org_api_key_id(
        self,
        org_api_key_manager: OrgApiKeyManager,
        org_api_key_bus_obj: OrgApiKeyBusObj,
        new_org_api_key: OrgApiKey
    ):
        """
            #TODO add comment
        """
        new_org_api_key_org_api_key_id = new_org_api_key.org_api_key_id
        await org_api_key_bus_obj.load_from_id(new_org_api_key_org_api_key_id)
        assert org_api_key_manager.is_equal(org_api_key_bus_obj.org_api_key, new_org_api_key) is True
    @pytest.mark.asyncio
    async def test_load_with_org_api_key_code(
        self,
        org_api_key_manager: OrgApiKeyManager,
        org_api_key_bus_obj: OrgApiKeyBusObj,
        new_org_api_key: OrgApiKey
    ):
        """
            #TODO add comment
        """
        await org_api_key_bus_obj.load_from_code(new_org_api_key.code)
        assert org_api_key_manager.is_equal(org_api_key_bus_obj.org_api_key, new_org_api_key) is True
    @pytest.mark.asyncio
    async def test_load_with_org_api_key_json(
        self,
        org_api_key_manager: OrgApiKeyManager,
        org_api_key_bus_obj: OrgApiKeyBusObj,
        new_org_api_key: OrgApiKey
    ):
        """
            #TODO add comment
        """
        org_api_key_json = org_api_key_manager.to_json(new_org_api_key)
        await org_api_key_bus_obj.load_from_json(org_api_key_json)
        assert org_api_key_manager.is_equal(org_api_key_bus_obj.org_api_key, new_org_api_key) is True
    @pytest.mark.asyncio
    async def test_load_with_org_api_key_dict(
        self,
        org_api_key_manager: OrgApiKeyManager,
        org_api_key_bus_obj: OrgApiKeyBusObj,
        new_org_api_key: OrgApiKey
    ):
        """
            #TODO add comment
        """
        logger.info("test_load_with_org_api_key_dict 1")
        org_api_key_dict = org_api_key_manager.to_dict(new_org_api_key)
        logger.info(org_api_key_dict)
        await org_api_key_bus_obj.load_from_dict(org_api_key_dict)
        assert org_api_key_manager.is_equal(
            org_api_key_bus_obj.org_api_key,
            new_org_api_key) is True
    @pytest.mark.asyncio
    async def test_get_nonexistent_org_api_key(
        self,
        org_api_key_bus_obj: OrgApiKeyBusObj
    ):
        """
            #TODO add comment
        """
        # Test retrieving a nonexistent org_api_key raises an exception
        await org_api_key_bus_obj.load_from_id(-1)
        assert org_api_key_bus_obj.is_valid() is False  # Assuming -1 is an id that wouldn't exist
    @pytest.mark.asyncio
    async def test_update_org_api_key(
        self,
        org_api_key_manager: OrgApiKeyManager,
        org_api_key_bus_obj: OrgApiKeyBusObj,
        new_org_api_key: OrgApiKey
    ):
        """
            #TODO add comment
        """
        # Test updating a org_api_key's data
        new_org_api_key_org_api_key_id_value = new_org_api_key.org_api_key_id
        new_org_api_key = await org_api_key_manager.get_by_id(new_org_api_key_org_api_key_id_value)
        assert isinstance(new_org_api_key, OrgApiKey)
        new_code = uuid.uuid4()
        await org_api_key_bus_obj.load_from_obj_instance(new_org_api_key)
        org_api_key_bus_obj.code = new_code
        await org_api_key_bus_obj.save()
        new_org_api_key_org_api_key_id_value = new_org_api_key.org_api_key_id
        new_org_api_key = await org_api_key_manager.get_by_id(new_org_api_key_org_api_key_id_value)
        assert org_api_key_manager.is_equal(
            org_api_key_bus_obj.org_api_key,
            new_org_api_key) is True
    @pytest.mark.asyncio
    async def test_delete_org_api_key(
        self,
        org_api_key_manager: OrgApiKeyManager,
        org_api_key_bus_obj: OrgApiKeyBusObj,
        new_org_api_key: OrgApiKey
    ):
        """
            #TODO add comment
        """
        assert new_org_api_key.org_api_key_id is not None
        assert org_api_key_bus_obj.org_api_key_id is None
        new_org_api_key_org_api_key_id_value = new_org_api_key.org_api_key_id
        await org_api_key_bus_obj.load_from_id(new_org_api_key_org_api_key_id_value)
        assert org_api_key_bus_obj.org_api_key_id is not None
        await org_api_key_bus_obj.delete()
        new_org_api_key_org_api_key_id_value = new_org_api_key.org_api_key_id
        new_org_api_key = await org_api_key_manager.get_by_id(new_org_api_key_org_api_key_id_value)
        assert new_org_api_key is None

