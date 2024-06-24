# business/tests/org_api_key_base_test.py
# pylint: disable=unused-import
# pylint: disable=redefined-outer-name
"""
This module contains unit tests for the OrgApiKeyBusObj class.
"""
import uuid
from datetime import date, datetime  # noqa: F401
from decimal import Decimal
from unittest.mock import AsyncMock, Mock, patch
import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession
import current_runtime  # noqa: F401
from business.org_api_key_base import OrgApiKeyBaseBusObj
from helpers.session_context import SessionContext
from managers.org_api_key import OrgApiKeyManager
from models import OrgApiKey
from models.factory import OrgApiKeyFactory
from services.logging_config import get_logger
from ..org_api_key import OrgApiKeyBusObj

logger = get_logger(__name__)
@pytest.fixture
def fake_session_context():
    """
    Fixture that returns a fake session context.
    """
    session = Mock()
    session_context = Mock(spec=SessionContext)
    session_context.session = session
    return session_context
@pytest.fixture
def org_api_key():
    """
    Fixture that returns a mock org_api_key object.
    """
    return Mock(spec=OrgApiKey)
@pytest.fixture
def org_api_key_base_bus_obj(fake_session_context, org_api_key):
    """
    Fixture that returns a OrgApiKeyBaseBusObj instance.
    """
    org_api_key_base = OrgApiKeyBaseBusObj(fake_session_context)
    org_api_key_base.org_api_key = org_api_key
    return org_api_key_base
class TestOrgApiKeyBaseBusObj:
    """
    Unit tests for the OrgApiKeyBusObj class.
    """
    @pytest_asyncio.fixture(scope="function")
    async def org_api_key_manager(self, session: AsyncSession):
        """
        Fixture that returns an instance of the OrgApiKeyManager class.
        """
        session_context = SessionContext(dict(), session)
        return OrgApiKeyManager(session_context)
    @pytest_asyncio.fixture(scope="function")
    async def org_api_key_bus_obj(self, session):
        """
        Fixture that returns an instance of the OrgApiKeyBusObj class.
        """
        session_context = SessionContext(dict(), session)
        return OrgApiKeyBusObj(session_context)
    @pytest_asyncio.fixture(scope="function")
    async def new_org_api_key(self, session):
        """
        Fixture that returns a new instance of
        the OrgApiKey class.
        """
        return await OrgApiKeyFactory.create_async(
            session)
    @pytest.mark.asyncio
    async def test_create_org_api_key(
        self,
        org_api_key_bus_obj: OrgApiKeyBusObj
    ):
        """
        Test case for creating a new org_api_key.
        """
        # Test creating a new org_api_key
        assert org_api_key_bus_obj.org_api_key_id == 0
        # assert isinstance(org_api_key_bus_obj.org_api_key_id, int)
        assert isinstance(
            org_api_key_bus_obj.code, uuid.UUID)
        assert isinstance(
            org_api_key_bus_obj.last_change_code, int)
        assert org_api_key_bus_obj.insert_user_id == uuid.UUID(int=0)
        assert org_api_key_bus_obj.last_update_user_id == uuid.UUID(int=0)
# endset
        assert isinstance(org_api_key_bus_obj.api_key_value, str)
        assert isinstance(org_api_key_bus_obj.created_by, str)
        assert isinstance(org_api_key_bus_obj.created_utc_date_time, datetime)
        assert isinstance(org_api_key_bus_obj.expiration_utc_date_time, datetime)
        assert isinstance(org_api_key_bus_obj.is_active, bool)
        assert isinstance(org_api_key_bus_obj.is_temp_user_key, bool)
        assert isinstance(org_api_key_bus_obj.name, str)
        assert isinstance(org_api_key_bus_obj.organization_id, int)
        assert isinstance(org_api_key_bus_obj.org_customer_id, int)
# endset
    @pytest.mark.asyncio
    async def test_load_with_org_api_key_obj(
        self,
        org_api_key_manager: OrgApiKeyManager,
        org_api_key_bus_obj: OrgApiKeyBusObj,
        new_org_api_key: OrgApiKey
    ):
        """
        Test case for loading data from a
        org_api_key object instance.
        """
        await org_api_key_bus_obj.load_from_obj_instance(
            new_org_api_key)
        assert org_api_key_manager.is_equal(
            org_api_key_bus_obj.org_api_key, new_org_api_key) is True
    @pytest.mark.asyncio
    async def test_load_with_org_api_key_id(
        self,
        org_api_key_manager: OrgApiKeyManager,
        org_api_key_bus_obj: OrgApiKeyBusObj,
        new_org_api_key: OrgApiKey
    ):
        """
        Test case for loading data from a
        org_api_key ID.
        """
        new_org_api_key_org_api_key_id = new_org_api_key.org_api_key_id
        await org_api_key_bus_obj.load_from_id(
            new_org_api_key_org_api_key_id)
        assert org_api_key_manager.is_equal(
            org_api_key_bus_obj.org_api_key, new_org_api_key) is True
    @pytest.mark.asyncio
    async def test_load_with_org_api_key_code(
        self,
        org_api_key_manager: OrgApiKeyManager,
        org_api_key_bus_obj: OrgApiKeyBusObj,
        new_org_api_key: OrgApiKey
    ):
        """
        Test case for loading data from a
        org_api_key code.
        """
        await org_api_key_bus_obj.load_from_code(
            new_org_api_key.code)
        assert org_api_key_manager.is_equal(
            org_api_key_bus_obj.org_api_key, new_org_api_key) is True
    @pytest.mark.asyncio
    async def test_load_with_org_api_key_json(
        self,
        org_api_key_manager: OrgApiKeyManager,
        org_api_key_bus_obj: OrgApiKeyBusObj,
        new_org_api_key: OrgApiKey
    ):
        """
        Test case for loading data from a
        org_api_key JSON.
        """
        org_api_key_json = org_api_key_manager.to_json(new_org_api_key)
        await org_api_key_bus_obj.load_from_json(
            org_api_key_json)
        assert org_api_key_manager.is_equal(
            org_api_key_bus_obj.org_api_key, new_org_api_key) is True
    @pytest.mark.asyncio
    async def test_load_with_org_api_key_dict(
        self,
        org_api_key_manager: OrgApiKeyManager,
        org_api_key_bus_obj: OrgApiKeyBusObj,
        new_org_api_key: OrgApiKey
    ):
        """
        Test case for loading data from a
        org_api_key dictionary.
        """
        logger.info("test_load_with_org_api_key_dict 1")
        org_api_key_dict = org_api_key_manager.to_dict(new_org_api_key)
        logger.info(org_api_key_dict)
        await org_api_key_bus_obj.load_from_dict(
            org_api_key_dict)
        assert org_api_key_manager.is_equal(
            org_api_key_bus_obj.org_api_key,
            new_org_api_key) is True
    @pytest.mark.asyncio
    async def test_get_nonexistent_org_api_key(
        self,
        org_api_key_bus_obj: OrgApiKeyBusObj
    ):
        """
        Test case for retrieving a nonexistent org_api_key.
        """
        # Test retrieving a nonexistent
        # org_api_key raises an exception
        await org_api_key_bus_obj.load_from_id(-1)
        # Assuming -1 is an id that wouldn't exist
        assert org_api_key_bus_obj.is_valid() is False
    @pytest.mark.asyncio
    async def test_update_org_api_key(
        self,
        org_api_key_manager: OrgApiKeyManager,
        org_api_key_bus_obj: OrgApiKeyBusObj,
        new_org_api_key: OrgApiKey
    ):
        """
        Test case for updating a org_api_key's data.
        """
        # Test updating a org_api_key's data
        new_org_api_key_org_api_key_id_value = new_org_api_key.org_api_key_id
        new_org_api_key = await org_api_key_manager.get_by_id(
            new_org_api_key_org_api_key_id_value)
        assert isinstance(new_org_api_key, OrgApiKey)
        new_code = uuid.uuid4()
        await org_api_key_bus_obj.load_from_obj_instance(
            new_org_api_key)
        org_api_key_bus_obj.code = new_code
        await org_api_key_bus_obj.save()
        new_org_api_key_org_api_key_id_value = new_org_api_key.org_api_key_id
        new_org_api_key = await org_api_key_manager.get_by_id(
            new_org_api_key_org_api_key_id_value)
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
        Test case for deleting a org_api_key.
        """
        assert new_org_api_key.org_api_key_id is not None
        assert org_api_key_bus_obj.org_api_key_id == 0
        new_org_api_key_org_api_key_id_value = new_org_api_key.org_api_key_id
        await org_api_key_bus_obj.load_from_id(
            new_org_api_key_org_api_key_id_value)
        assert org_api_key_bus_obj.org_api_key_id is not None
        await org_api_key_bus_obj.delete()
        new_org_api_key_org_api_key_id_value = new_org_api_key.org_api_key_id
        new_org_api_key = await org_api_key_manager.get_by_id(
            new_org_api_key_org_api_key_id_value)
        assert new_org_api_key is None
    def test_get_session_context(
        self,
        org_api_key_base_bus_obj,
        fake_session_context
    ):
        """
        Test case for getting the session context.
        """
        assert org_api_key_base_bus_obj.get_session_context() == fake_session_context
    @pytest.mark.asyncio
    async def test_refresh(self, org_api_key_base_bus_obj, org_api_key):
        """
        Test case for refreshing the org_api_key data.
        """
        with patch(
            'business.org_api_key_base.OrgApiKeyManager',
            autospec=True
        ) as mock_org_api_key_manager:
            mock_org_api_key_manager_instance = mock_org_api_key_manager.return_value
            mock_org_api_key_manager_instance.refresh = AsyncMock(return_value=org_api_key)
            refreshed_org_api_key_base = await org_api_key_base_bus_obj.refresh()
            assert refreshed_org_api_key_base.org_api_key == org_api_key
            mock_org_api_key_manager_instance.refresh.assert_called_once_with(org_api_key)
    def test_is_valid(self, org_api_key_base_bus_obj):
        """
        Test case for checking if the org_api_key data is valid.
        """
        assert org_api_key_base_bus_obj.is_valid() is True
        org_api_key_base_bus_obj.org_api_key = None
        assert org_api_key_base_bus_obj.is_valid() is False
    def test_to_dict(self, org_api_key_base_bus_obj):
        """
        Test case for converting the org_api_key data to a dictionary.
        """
        with patch(
            'business.org_api_key_base.OrgApiKeyManager',
            autospec=True
        ) as mock_org_api_key_manager:
            mock_org_api_key_manager_instance = mock_org_api_key_manager.return_value
            mock_org_api_key_manager_instance.to_dict = Mock(
                return_value={"key": "value"})
            org_api_key_dict = org_api_key_base_bus_obj.to_dict()
            assert org_api_key_dict == {"key": "value"}
            mock_org_api_key_manager_instance.to_dict.assert_called_once_with(
                org_api_key_base_bus_obj.org_api_key)
    def test_to_json(self, org_api_key_base_bus_obj):
        """
        Test case for converting the org_api_key data to JSON.
        """
        with patch(
            'business.org_api_key_base.OrgApiKeyManager',
            autospec=True
        ) as mock_org_api_key_manager:
            mock_org_api_key_manager_instance = mock_org_api_key_manager.return_value
            mock_org_api_key_manager_instance.to_json = Mock(
                return_value='{"key": "value"}')
            org_api_key_json = org_api_key_base_bus_obj.to_json()
            assert org_api_key_json == '{"key": "value"}'
            mock_org_api_key_manager_instance.to_json.assert_called_once_with(
                org_api_key_base_bus_obj.org_api_key)
    def test_get_obj(self, org_api_key_base_bus_obj, org_api_key):
        """
        Test case for getting the org_api_key object.
        """
        assert org_api_key_base_bus_obj.get_obj() == org_api_key
    def test_get_object_name(self, org_api_key_base_bus_obj):
        """
        Test case for getting the object name.
        """
        assert org_api_key_base_bus_obj.get_object_name() == "org_api_key"
    def test_get_id(self, org_api_key_base_bus_obj, org_api_key):
        """
        Test case for getting the org_api_key ID.
        """
        org_api_key.org_api_key_id = 1
        assert org_api_key_base_bus_obj.get_id() == 1
    def test_org_api_key_id(self, org_api_key_base_bus_obj, org_api_key):
        """
        Test case for the org_api_key_id property.
        """
        org_api_key.org_api_key_id = 1
        assert org_api_key_base_bus_obj.org_api_key_id == 1
    def test_code(self, org_api_key_base_bus_obj, org_api_key):
        """
        Test case for the code property.
        """
        test_uuid = uuid.uuid4()
        org_api_key.code = test_uuid
        assert org_api_key_base_bus_obj.code == test_uuid
    def test_code_setter(self, org_api_key_base_bus_obj):
        """
        Test case for the code setter.
        """
        test_uuid = uuid.uuid4()
        org_api_key_base_bus_obj.code = test_uuid
        assert org_api_key_base_bus_obj.code == test_uuid
    def test_code_invalid_value(self, org_api_key_base_bus_obj):
        """
        Test case for setting an invalid value for the code property.
        """
        with pytest.raises(ValueError):
            org_api_key_base_bus_obj.code = "not-a-uuid"
    def test_last_change_code(self, org_api_key_base_bus_obj, org_api_key):
        """
        Test case to verify the behavior of the last_change_code
        attribute in the OrgApiKeyBaseBusiness class.
        Args:
            org_api_key_base_bus_obj (OrgApiKeyBaseBusiness):
                An instance of the
                OrgApiKeyBaseBusiness class.
            org_api_key (OrgApiKey): An instance of the OrgApiKey class.
        Returns:
            None
        """
        org_api_key.last_change_code = 123
        assert org_api_key_base_bus_obj.last_change_code == 123
    def test_last_change_code_setter(self, org_api_key_base_bus_obj):
        """
        Test case for the last_change_code setter.
        """
        org_api_key_base_bus_obj.last_change_code = 123
        assert org_api_key_base_bus_obj.last_change_code == 123
    def test_last_change_code_invalid_value(self, org_api_key_base_bus_obj):
        """
        Test case for setting an invalid value for the
        last_change_code property.
        """
        with pytest.raises(ValueError):
            org_api_key_base_bus_obj.last_change_code = "not-an-int"
    def test_insert_user_id(self, org_api_key_base_bus_obj, org_api_key):
        """
        Test case for the insert_user_id property.
        """
        test_uuid = uuid.uuid4()
        org_api_key.insert_user_id = test_uuid
        assert org_api_key_base_bus_obj.insert_user_id == test_uuid
    def test_insert_user_id_setter(self, org_api_key_base_bus_obj):
        """
        Test case for the insert_user_id setter.
        """
        test_uuid = uuid.uuid4()
        org_api_key_base_bus_obj.insert_user_id = test_uuid
        assert org_api_key_base_bus_obj.insert_user_id == test_uuid
    def test_insert_user_id_invalid_value(self, org_api_key_base_bus_obj):
        """
        Test case for setting an invalid value for the
        insert_user_id property.
        """
        with pytest.raises(ValueError):
            org_api_key_base_bus_obj.insert_user_id = "not-a-uuid"
# endset
    # apiKeyValue,
    def test_api_key_value(self, org_api_key_base_bus_obj, org_api_key):
        """
        Test case for the api_key_value property.
        """
        org_api_key.api_key_value = "Vanilla"
        assert org_api_key_base_bus_obj.api_key_value == "Vanilla"
    def test_api_key_value_setter(self, org_api_key_base_bus_obj):
        """
        Test case for the api_key_value setter.
        """
        org_api_key_base_bus_obj.api_key_value = "Vanilla"
        assert org_api_key_base_bus_obj.api_key_value == "Vanilla"
    def test_api_key_value_invalid_value(self, org_api_key_base_bus_obj):
        """
        Test case for setting an invalid value for the
        api_key_value property.
        """
        with pytest.raises(AssertionError):
            org_api_key_base_bus_obj.api_key_value = 123
    # createdBy,
    def test_created_by(self, org_api_key_base_bus_obj, org_api_key):
        """
        Test case for the created_by property.
        """
        org_api_key.created_by = "Vanilla"
        assert org_api_key_base_bus_obj.created_by == "Vanilla"
    def test_created_by_setter(self, org_api_key_base_bus_obj):
        """
        Test case for the created_by setter.
        """
        org_api_key_base_bus_obj.created_by = "Vanilla"
        assert org_api_key_base_bus_obj.created_by == "Vanilla"
    def test_created_by_invalid_value(self, org_api_key_base_bus_obj):
        """
        Test case for setting an invalid value for the
        created_by property.
        """
        with pytest.raises(AssertionError):
            org_api_key_base_bus_obj.created_by = 123
    # createdUTCDateTime
    def test_created_utc_date_time(self, org_api_key_base_bus_obj, org_api_key):
        """
        Test case for the created_utc_date_time property.
        """
        test_datetime = datetime.utcnow()
        org_api_key.created_utc_date_time = test_datetime
        assert org_api_key_base_bus_obj.created_utc_date_time == test_datetime
    def test_created_utc_date_time_setter(self, org_api_key_base_bus_obj):
        """
        Test case for the created_utc_date_time setter.
        """
        test_datetime = datetime.utcnow()
        org_api_key_base_bus_obj.created_utc_date_time = test_datetime
        assert org_api_key_base_bus_obj.created_utc_date_time == test_datetime
    def test_created_utc_date_time_invalid_value(self, org_api_key_base_bus_obj):
        """
        Test case for setting an invalid value for the
        created_utc_date_time property.
        """
        with pytest.raises(AssertionError):
            org_api_key_base_bus_obj.created_utc_date_time = "not-a-datetime"
    # expirationUTCDateTime
    def test_expiration_utc_date_time(self, org_api_key_base_bus_obj, org_api_key):
        """
        Test case for the expiration_utc_date_time property.
        """
        test_datetime = datetime.utcnow()
        org_api_key.expiration_utc_date_time = test_datetime
        assert org_api_key_base_bus_obj.expiration_utc_date_time == test_datetime
    def test_expiration_utc_date_time_setter(self, org_api_key_base_bus_obj):
        """
        Test case for the expiration_utc_date_time setter.
        """
        test_datetime = datetime.utcnow()
        org_api_key_base_bus_obj.expiration_utc_date_time = test_datetime
        assert org_api_key_base_bus_obj.expiration_utc_date_time == test_datetime
    def test_expiration_utc_date_time_invalid_value(self, org_api_key_base_bus_obj):
        """
        Test case for setting an invalid value for the
        expiration_utc_date_time property.
        """
        with pytest.raises(AssertionError):
            org_api_key_base_bus_obj.expiration_utc_date_time = "not-a-datetime"
    # isActive,
    def test_is_active(self, org_api_key_base_bus_obj, org_api_key):
        """
        Test case for the is_active property.
        """
        org_api_key.is_active = True
        assert org_api_key_base_bus_obj.is_active is True
    def test_is_active_setter(self, org_api_key_base_bus_obj):
        """
        Test case for the is_active setter.
        """
        org_api_key_base_bus_obj.is_active = True
        assert org_api_key_base_bus_obj.is_active is True
    def test_is_active_invalid_value(self, org_api_key_base_bus_obj):
        """
        Test case for setting an invalid value for the
        is_active property.
        """
        with pytest.raises(ValueError):
            org_api_key_base_bus_obj.is_active = "not-a-boolean"
    # isTempUserKey,
    def test_is_temp_user_key(self, org_api_key_base_bus_obj, org_api_key):
        """
        Test case for the is_temp_user_key property.
        """
        org_api_key.is_temp_user_key = True
        assert org_api_key_base_bus_obj.is_temp_user_key is True
    def test_is_temp_user_key_setter(self, org_api_key_base_bus_obj):
        """
        Test case for the is_temp_user_key setter.
        """
        org_api_key_base_bus_obj.is_temp_user_key = True
        assert org_api_key_base_bus_obj.is_temp_user_key is True
    def test_is_temp_user_key_invalid_value(self, org_api_key_base_bus_obj):
        """
        Test case for setting an invalid value for the
        is_temp_user_key property.
        """
        with pytest.raises(ValueError):
            org_api_key_base_bus_obj.is_temp_user_key = "not-a-boolean"
    # name,
    def test_name(self, org_api_key_base_bus_obj, org_api_key):
        """
        Test case for the name property.
        """
        org_api_key.name = "Vanilla"
        assert org_api_key_base_bus_obj.name == "Vanilla"
    def test_name_setter(self, org_api_key_base_bus_obj):
        """
        Test case for the name setter.
        """
        org_api_key_base_bus_obj.name = "Vanilla"
        assert org_api_key_base_bus_obj.name == "Vanilla"
    def test_name_invalid_value(self, org_api_key_base_bus_obj):
        """
        Test case for setting an invalid value for the
        name property.
        """
        with pytest.raises(AssertionError):
            org_api_key_base_bus_obj.name = 123
    # OrganizationID
    # OrgCustomerID
# endset
    # apiKeyValue,
    # createdBy,
    # createdUTCDateTime
    # expirationUTCDateTime
    # isActive,
    # isTempUserKey,
    # name,
    # OrganizationID
    def test_organization_id(self, org_api_key_base_bus_obj, org_api_key):
        """
        Test case for the organization_id property.
        """
        org_api_key.organization_id = 1
        assert org_api_key_base_bus_obj.organization_id == 1
    def test_organization_id_setter(self, org_api_key_base_bus_obj):
        """
        Test case for the organization_id setter.
        """
        org_api_key_base_bus_obj.organization_id = 1
        assert org_api_key_base_bus_obj.organization_id == 1
    def test_organization_id_invalid_value(self, org_api_key_base_bus_obj):
        """
        Test case for setting an invalid value for the
        organization_id property.
        """
        with pytest.raises(AssertionError):
            org_api_key_base_bus_obj.organization_id = "not-an-int"
    # OrgCustomerID
    def test_org_customer_id(self, org_api_key_base_bus_obj, org_api_key):
        """
        Test case for the org_customer_id property.
        """
        org_api_key.org_customer_id = 1
        assert org_api_key_base_bus_obj.org_customer_id == 1
    def test_org_customer_id_setter(self, org_api_key_base_bus_obj):
        """
        Test case for the org_customer_id setter.
        """
        org_api_key_base_bus_obj.org_customer_id = 1
        assert org_api_key_base_bus_obj.org_customer_id == 1
    def test_org_customer_id_invalid_value(self, org_api_key_base_bus_obj):
        """
        Test case for setting an invalid value for the
        org_customer_id property.
        """
        with pytest.raises(ValueError):
            org_api_key_base_bus_obj.org_customer_id = "not-an-int"
# endset
    def test_insert_utc_date_time(self, org_api_key_base_bus_obj, org_api_key):
        """
        Test case for the insert_utc_date_time property.
        """
        test_datetime = datetime.utcnow()
        org_api_key.insert_utc_date_time = test_datetime
        assert org_api_key_base_bus_obj.insert_utc_date_time == test_datetime
    def test_insert_utc_date_time_setter(self, org_api_key_base_bus_obj):
        """
        Test case for the insert_utc_date_time setter.
        """
        test_datetime = datetime.utcnow()
        org_api_key_base_bus_obj.insert_utc_date_time = test_datetime
        assert org_api_key_base_bus_obj.insert_utc_date_time == test_datetime
    def test_insert_utc_date_time_invalid_value(self, org_api_key_base_bus_obj):
        """
        Test case for setting an invalid value for the
        insert_utc_date_time property.
        """
        with pytest.raises(AssertionError):
            org_api_key_base_bus_obj.insert_utc_date_time = "not-a-datetime"
    def test_last_update_utc_date_time(self, org_api_key_base_bus_obj, org_api_key):
        """
        Test case for the last_update_utc_date_time property.
        """
        test_datetime = datetime.utcnow()
        org_api_key.last_update_utc_date_time = test_datetime
        assert org_api_key_base_bus_obj.last_update_utc_date_time == test_datetime
    def test_last_update_utc_date_time_setter(self, org_api_key_base_bus_obj):
        """
        Test case for the last_update_utc_date_time setter.
        """
        test_datetime = datetime.utcnow()
        org_api_key_base_bus_obj.last_update_utc_date_time = test_datetime
        assert org_api_key_base_bus_obj.last_update_utc_date_time == test_datetime
    def test_last_update_utc_date_time_invalid_value(self, org_api_key_base_bus_obj):
        """
        Test case for setting an invalid value for the
        last_update_utc_date_time property.
        """
        with pytest.raises(AssertionError):
            org_api_key_base_bus_obj.last_update_utc_date_time = "not-a-datetime"

