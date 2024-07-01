# business/tests/org_api_key_base_test.py
# pylint: disable=unused-import
# pylint: disable=redefined-outer-name

"""
This module contains unit tests for the
OrgApiKeyBusObj class.
"""

import uuid  # noqa: F401
import math  # noqa: F401
from datetime import date, datetime  # noqa: F401
from decimal import Decimal  # noqa: F401
from unittest.mock import AsyncMock, Mock, patch

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

import current_runtime  # noqa: F401
from business.org_api_key_base import (
    OrgApiKeyBaseBusObj)
from helpers.session_context import SessionContext
from managers.org_api_key import (
    OrgApiKeyManager)
from models import OrgApiKey
from models.factory import (
    OrgApiKeyFactory)
from services.logging_config import get_logger

from ..org_api_key import OrgApiKeyBusObj


logger = get_logger(__name__)


@pytest.fixture
def mock_session_context():
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
    Fixture that returns a mock
    org_api_key object.
    """
    return Mock(spec=OrgApiKey)


@pytest.fixture
def mock_sess_base_bus_obj(
    mock_session_context, org_api_key
):
    """
    Fixture that returns a
    OrgApiKeyBaseBusObj instance.
    """
    mock_sess_base_bus_obj = OrgApiKeyBaseBusObj(
        mock_session_context)
    mock_sess_base_bus_obj.org_api_key = \
        org_api_key
    return mock_sess_base_bus_obj


class TestOrgApiKeyBaseBusObj:
    """
    Unit tests for the
    OrgApiKeyBusObj class.
    """

    @pytest_asyncio.fixture(scope="function")
    async def obj_manager(self, session: AsyncSession):
        """
        Fixture that returns an instance of the
        OrgApiKeyManager class.
        """
        session_context = SessionContext(dict(), session)
        return OrgApiKeyManager(session_context)

    @pytest_asyncio.fixture(scope="function")
    async def new_bus_obj(self, session):
        """
        Fixture that returns an instance of the
        OrgApiKeyBusObj class.
        """
        session_context = SessionContext(dict(), session)
        return OrgApiKeyBusObj(
            session_context)

    @pytest_asyncio.fixture(scope="function")
    async def new_obj(self, session):
        """
        Fixture that returns a new instance of
        the OrgApiKey class.
        """

        return await OrgApiKeyFactory.create_async(
            session)

    @pytest.mark.asyncio
    async def test_create_org_api_key(
        self,
        new_bus_obj: OrgApiKeyBusObj
    ):
        """
        Test case for creating a new org_api_key.
        """
        # Test creating a new org_api_key

        assert new_bus_obj.org_api_key_id == 0

        # assert isinstance(new_bus_obj.org_api_key_id, int)
        assert isinstance(
            new_bus_obj.code, uuid.UUID)

        assert isinstance(
            new_bus_obj.last_change_code, int)

        assert new_bus_obj.insert_user_id == uuid.UUID(int=0)

        assert new_bus_obj.last_update_user_id == uuid.UUID(int=0)

        assert isinstance(new_bus_obj.api_key_value,
                          str)
        assert isinstance(new_bus_obj.created_by,
                          str)
        assert isinstance(new_bus_obj.created_utc_date_time,
                          datetime)
        assert isinstance(new_bus_obj.expiration_utc_date_time,
                          datetime)
        assert isinstance(new_bus_obj.is_active,
                          bool)
        assert isinstance(new_bus_obj.is_temp_user_key,
                          bool)
        assert isinstance(new_bus_obj.name,
                          str)
        assert isinstance(new_bus_obj.organization_id,
                          int)
        assert isinstance(new_bus_obj.org_customer_id,
                          int)

    @pytest.mark.asyncio
    async def test_load_with_org_api_key_obj(
        self,
        obj_manager: OrgApiKeyManager,
        new_bus_obj: OrgApiKeyBusObj,
        new_obj: OrgApiKey
    ):
        """
        Test case for loading data from a
        org_api_key object instance.
        """

        new_bus_obj.load_from_obj_instance(
            new_obj)

        assert obj_manager.is_equal(
            new_bus_obj.org_api_key, new_obj) is True

    @pytest.mark.asyncio
    async def test_load_with_org_api_key_id(
        self,
        obj_manager: OrgApiKeyManager,
        new_bus_obj: OrgApiKeyBusObj,
        new_obj: OrgApiKey
    ):
        """
        Test case for loading data from a
        org_api_key ID.
        """

        new_obj_org_api_key_id = \
            new_obj.org_api_key_id

        await new_bus_obj.load_from_id(
            new_obj_org_api_key_id)

        assert obj_manager.is_equal(
            new_bus_obj.org_api_key, new_obj) is True

    @pytest.mark.asyncio
    async def test_load_with_org_api_key_code(
        self,
        obj_manager: OrgApiKeyManager,
        new_bus_obj: OrgApiKeyBusObj,
        new_obj: OrgApiKey
    ):
        """
        Test case for loading data from a
        org_api_key code.
        """

        await new_bus_obj.load_from_code(
            new_obj.code)

        assert obj_manager.is_equal(
            new_bus_obj.org_api_key, new_obj) is True

    @pytest.mark.asyncio
    async def test_load_with_org_api_key_json(
        self,
        obj_manager: OrgApiKeyManager,
        new_bus_obj: OrgApiKeyBusObj,
        new_obj: OrgApiKey
    ):
        """
        Test case for loading data from a
        org_api_key JSON.
        """

        org_api_key_json = \
            obj_manager.to_json(
                new_obj)

        await new_bus_obj.load_from_json(
            org_api_key_json)

        assert obj_manager.is_equal(
            new_bus_obj.org_api_key, new_obj) is True

    @pytest.mark.asyncio
    async def test_load_with_org_api_key_dict(
        self,
        obj_manager: OrgApiKeyManager,
        new_bus_obj: OrgApiKeyBusObj,
        new_obj: OrgApiKey
    ):
        """
        Test case for loading data from a
        org_api_key dictionary.
        """

        logger.info("test_load_with_org_api_key_dict 1")

        org_api_key_dict = \
            obj_manager.to_dict(
                new_obj)

        logger.info(org_api_key_dict)

        await new_bus_obj.load_from_dict(
            org_api_key_dict)

        assert obj_manager.is_equal(
            new_bus_obj.org_api_key,
            new_obj) is True

    @pytest.mark.asyncio
    async def test_get_nonexistent_org_api_key(
        self,
        new_bus_obj: OrgApiKeyBusObj
    ):
        """
        Test case for retrieving a nonexistent
        org_api_key.
        """
        # Test retrieving a nonexistent
        # org_api_key raises an exception
        await new_bus_obj.load_from_id(-1)

        # Assuming -1 is an id that wouldn't exist
        assert new_bus_obj.is_valid() is False

    @pytest.mark.asyncio
    async def test_update_org_api_key(
        self,
        obj_manager: OrgApiKeyManager,
        new_bus_obj: OrgApiKeyBusObj,
        new_obj: OrgApiKey
    ):
        """
        Test case for updating a org_api_key's data.
        """
        # Test updating a org_api_key's data

        new_obj_org_api_key_id_value = \
            new_obj.org_api_key_id

        new_obj = await \
            obj_manager.get_by_id(
                new_obj_org_api_key_id_value)

        assert isinstance(new_obj,
                          OrgApiKey)

        new_code = uuid.uuid4()

        new_bus_obj.load_from_obj_instance(
            new_obj)

        assert obj_manager.is_equal(
            new_bus_obj.org_api_key,
            new_obj) is True

        new_bus_obj.code = new_code

        await new_bus_obj.save()

        new_obj_org_api_key_id_value = \
            new_obj.org_api_key_id

        new_obj = await \
            obj_manager.get_by_id(
                new_obj_org_api_key_id_value)

        assert obj_manager.is_equal(
            new_bus_obj.org_api_key,
            new_obj) is True

    @pytest.mark.asyncio
    async def test_delete_org_api_key(
        self,
        obj_manager: OrgApiKeyManager,
        new_bus_obj: OrgApiKeyBusObj,
        new_obj: OrgApiKey
    ):
        """
        Test case for deleting a org_api_key.
        """

        assert new_bus_obj.org_api_key is not None

        assert new_bus_obj.org_api_key_id == 0

        new_bus_obj.load_from_obj_instance(
            new_obj)

        assert new_bus_obj.org_api_key_id is not None

        await new_bus_obj.delete()

        new_obj_org_api_key_id_value = \
            new_obj.org_api_key_id

        new_obj = await \
            obj_manager.get_by_id(
                new_obj_org_api_key_id_value)

        assert new_obj is None

    def test_get_session_context(
        self,
        mock_sess_base_bus_obj,
        mock_session_context
    ):
        """
        Test case for getting the session context.
        """
        assert mock_sess_base_bus_obj.get_session_context() == \
            mock_session_context

    @pytest.mark.asyncio
    async def test_refresh(
        self,
        mock_sess_base_bus_obj,
        org_api_key
    ):
        """
        Test case for refreshing the org_api_key data.
        """
        with patch(
            "business.org_api_key_base"
            ".OrgApiKeyManager",
            autospec=True
        ) as mock_obj_manager:
            mock_obj_manager_instance = \
                mock_obj_manager.return_value
            mock_obj_manager_instance.refresh =\
                AsyncMock(return_value=org_api_key)

            refreshed_mock_sess_base_bus_obj = await \
                mock_sess_base_bus_obj.refresh()
            assert refreshed_mock_sess_base_bus_obj \
                .org_api_key == org_api_key
            mock_obj_manager_instance.refresh \
                .assert_called_once_with(org_api_key)

    def test_is_valid(
            self, mock_sess_base_bus_obj):
        """
        Test case for checking if the org_api_key data is valid.
        """
        assert mock_sess_base_bus_obj.is_valid() is True

        mock_sess_base_bus_obj.org_api_key = None
        assert mock_sess_base_bus_obj.is_valid() is False

    def test_to_dict(
            self, mock_sess_base_bus_obj):
        """
        Test case for converting the org_api_key
        data to a dictionary.
        """
        with patch(
            "business.org_api_key_base"
            ".OrgApiKeyManager",
            autospec=True
        ) as mock_obj_manager:
            mock_obj_manager_instance = \
                mock_obj_manager.return_value
            mock_obj_manager_instance.to_dict = Mock(
                return_value={"key": "value"})

            org_api_key_dict = mock_sess_base_bus_obj.to_dict()
            assert org_api_key_dict == {"key": "value"}
            mock_obj_manager_instance.to_dict.assert_called_once_with(
                mock_sess_base_bus_obj.org_api_key)

    def test_to_json(
            self, mock_sess_base_bus_obj):
        """
        Test case for converting the org_api_key data to JSON.
        """
        with patch(
            "business.org_api_key_base"
            ".OrgApiKeyManager",
            autospec=True
        ) as mock_obj_manager:
            mock_obj_manager_instance = \
                mock_obj_manager.return_value
            mock_obj_manager_instance.to_json = Mock(
                return_value='{"key": "value"}')

            org_api_key_json = mock_sess_base_bus_obj.to_json()
            assert org_api_key_json == '{"key": "value"}'
            mock_obj_manager_instance.to_json.assert_called_once_with(
                mock_sess_base_bus_obj.org_api_key)

    def test_get_obj(
            self, mock_sess_base_bus_obj, org_api_key):
        """
        Test case for getting the org_api_key object.
        """
        assert mock_sess_base_bus_obj.get_obj() == org_api_key

    def test_get_object_name(
            self, mock_sess_base_bus_obj):
        """
        Test case for getting the object name.
        """
        assert mock_sess_base_bus_obj \
            .get_object_name() == "org_api_key"

    def test_get_id(
            self, mock_sess_base_bus_obj, org_api_key):
        """
        Test case for getting the org_api_key ID.
        """
        org_api_key.org_api_key_id = 1
        assert mock_sess_base_bus_obj.get_id() == 1

    def test_org_api_key_id(
            self, mock_sess_base_bus_obj, org_api_key):
        """
        Test case for the org_api_key_id property.
        """
        org_api_key.org_api_key_id = 1
        assert mock_sess_base_bus_obj.org_api_key_id == 1

    def test_code(
            self, mock_sess_base_bus_obj, org_api_key):
        """
        Test case for the code property.
        """
        test_uuid = uuid.uuid4()
        org_api_key.code = test_uuid
        assert mock_sess_base_bus_obj.code == \
            test_uuid

    def test_code_setter(
            self, mock_sess_base_bus_obj):
        """
        Test case for the code setter.
        """
        test_uuid = uuid.uuid4()
        mock_sess_base_bus_obj.code = test_uuid
        assert mock_sess_base_bus_obj.code == \
            test_uuid

    def test_code_invalid_value(
            self, mock_sess_base_bus_obj):
        """
        Test case for setting an invalid value for the code property.
        """
        with pytest.raises(ValueError):
            mock_sess_base_bus_obj.code = "not-a-uuid"

    def test_last_change_code(
            self, mock_sess_base_bus_obj, org_api_key):
        """
        Test case to verify the behavior of the last_change_code
        attribute in the OrgApiKeyBaseBusiness class.

        Args:
            mock_sess_base_bus_obj (OrgApiKeyBaseBusiness):
                An instance of the
                OrgApiKeyBaseBusiness class.
            org_api_key (OrgApiKey):
                An instance of the
                OrgApiKey class.

        Returns:
            None
        """
        org_api_key.last_change_code = 123
        assert mock_sess_base_bus_obj.last_change_code == 123

    def test_last_change_code_setter(
            self, mock_sess_base_bus_obj):
        """
        Test case for the
        last_change_code setter.
        """
        mock_sess_base_bus_obj.last_change_code = 123
        assert mock_sess_base_bus_obj.last_change_code == 123

    def test_last_change_code_invalid_value(
            self, mock_sess_base_bus_obj):
        """
        Test case for setting an invalid value for the
        last_change_code property.
        """
        with pytest.raises(ValueError):
            mock_sess_base_bus_obj.last_change_code = "not-an-int"

    def test_insert_user_id(
            self, mock_sess_base_bus_obj, org_api_key):
        """
        Test case for the
        insert_user_id property.
        """
        test_uuid = uuid.uuid4()
        org_api_key.insert_user_id = test_uuid
        assert mock_sess_base_bus_obj.insert_user_id == \
            test_uuid

    def test_insert_user_id_setter(
            self, mock_sess_base_bus_obj):
        """
        Test case for the
        insert_user_id setter.
        """
        test_uuid = uuid.uuid4()
        mock_sess_base_bus_obj.insert_user_id = test_uuid
        assert mock_sess_base_bus_obj.insert_user_id == \
            test_uuid

    def test_insert_user_id_invalid_value(
            self, mock_sess_base_bus_obj):
        """
        Test case for setting an invalid value for the
        insert_user_id property.
        """
        with pytest.raises(ValueError):
            mock_sess_base_bus_obj.insert_user_id = "not-a-uuid"
    # apiKeyValue

    def test_api_key_value(
            self, mock_sess_base_bus_obj, org_api_key):
        """
        Test case for the
        api_key_value property.
        """
        org_api_key.api_key_value = \
            "Vanilla"
        assert mock_sess_base_bus_obj \
            .api_key_value == "Vanilla"

    def test_api_key_value_setter(
            self, mock_sess_base_bus_obj):
        """
        Test case for the
        api_key_value setter.
        """
        mock_sess_base_bus_obj.api_key_value = \
            "Vanilla"
        assert mock_sess_base_bus_obj \
            .api_key_value == "Vanilla"

    def test_api_key_value_invalid_value(
            self, mock_sess_base_bus_obj):
        """
        Test case for setting an invalid value for the
        api_key_value property.
        """
        with pytest.raises(AssertionError):
            mock_sess_base_bus_obj.api_key_value = \
                123
    # createdBy

    def test_created_by(
            self, mock_sess_base_bus_obj, org_api_key):
        """
        Test case for the
        created_by property.
        """
        org_api_key.created_by = \
            "Vanilla"
        assert mock_sess_base_bus_obj \
            .created_by == "Vanilla"

    def test_created_by_setter(
            self, mock_sess_base_bus_obj):
        """
        Test case for the
        created_by setter.
        """
        mock_sess_base_bus_obj.created_by = \
            "Vanilla"
        assert mock_sess_base_bus_obj \
            .created_by == "Vanilla"

    def test_created_by_invalid_value(
            self, mock_sess_base_bus_obj):
        """
        Test case for setting an invalid value for the
        created_by property.
        """
        with pytest.raises(AssertionError):
            mock_sess_base_bus_obj.created_by = \
                123
    # createdUTCDateTime

    def test_created_utc_date_time(
            self, mock_sess_base_bus_obj, org_api_key):
        """
        Test case for the
        created_utc_date_time property.
        """
        test_datetime = datetime.utcnow()
        org_api_key.created_utc_date_time = \
            test_datetime
        assert mock_sess_base_bus_obj \
            .created_utc_date_time == \
            test_datetime

    def test_created_utc_date_time_setter(
            self, mock_sess_base_bus_obj):
        """
        Test case for the
        created_utc_date_time setter.
        """
        test_datetime = datetime.utcnow()
        mock_sess_base_bus_obj.created_utc_date_time = \
            test_datetime
        assert mock_sess_base_bus_obj \
            .created_utc_date_time == \
            test_datetime

    def test_created_utc_date_time_invalid_value(
            self, mock_sess_base_bus_obj):
        """
        Test case for setting an invalid value for the
        created_utc_date_time property.
        """
        with pytest.raises(AssertionError):
            mock_sess_base_bus_obj.created_utc_date_time = \
                "not-a-datetime"
    # expirationUTCDateTime

    def test_expiration_utc_date_time(
            self, mock_sess_base_bus_obj, org_api_key):
        """
        Test case for the
        expiration_utc_date_time property.
        """
        test_datetime = datetime.utcnow()
        org_api_key.expiration_utc_date_time = \
            test_datetime
        assert mock_sess_base_bus_obj \
            .expiration_utc_date_time == \
            test_datetime

    def test_expiration_utc_date_time_setter(
            self, mock_sess_base_bus_obj):
        """
        Test case for the
        expiration_utc_date_time setter.
        """
        test_datetime = datetime.utcnow()
        mock_sess_base_bus_obj.expiration_utc_date_time = \
            test_datetime
        assert mock_sess_base_bus_obj \
            .expiration_utc_date_time == \
            test_datetime

    def test_expiration_utc_date_time_invalid_value(
            self, mock_sess_base_bus_obj):
        """
        Test case for setting an invalid value for the
        expiration_utc_date_time property.
        """
        with pytest.raises(AssertionError):
            mock_sess_base_bus_obj.expiration_utc_date_time = \
                "not-a-datetime"
    # isActive

    def test_is_active(
            self, mock_sess_base_bus_obj, org_api_key):
        """
        Test case for the
        is_active property.
        """
        org_api_key.is_active = True
        assert mock_sess_base_bus_obj \
            .is_active is True

    def test_is_active_setter(
            self, mock_sess_base_bus_obj):
        """
        Test case for the
        is_active setter.
        """
        mock_sess_base_bus_obj.is_active = \
            True
        assert mock_sess_base_bus_obj \
            .is_active is True

    def test_is_active_invalid_value(
            self, mock_sess_base_bus_obj):
        """
        Test case for setting an invalid value for the
        is_active property.
        """
        with pytest.raises(ValueError):
            mock_sess_base_bus_obj.is_active = \
                "not-a-boolean"
    # isTempUserKey

    def test_is_temp_user_key(
            self, mock_sess_base_bus_obj, org_api_key):
        """
        Test case for the
        is_temp_user_key property.
        """
        org_api_key.is_temp_user_key = True
        assert mock_sess_base_bus_obj \
            .is_temp_user_key is True

    def test_is_temp_user_key_setter(
            self, mock_sess_base_bus_obj):
        """
        Test case for the
        is_temp_user_key setter.
        """
        mock_sess_base_bus_obj.is_temp_user_key = \
            True
        assert mock_sess_base_bus_obj \
            .is_temp_user_key is True

    def test_is_temp_user_key_invalid_value(
            self, mock_sess_base_bus_obj):
        """
        Test case for setting an invalid value for the
        is_temp_user_key property.
        """
        with pytest.raises(ValueError):
            mock_sess_base_bus_obj.is_temp_user_key = \
                "not-a-boolean"
    # name

    def test_name(
            self, mock_sess_base_bus_obj, org_api_key):
        """
        Test case for the
        name property.
        """
        org_api_key.name = \
            "Vanilla"
        assert mock_sess_base_bus_obj \
            .name == "Vanilla"

    def test_name_setter(
            self, mock_sess_base_bus_obj):
        """
        Test case for the
        name setter.
        """
        mock_sess_base_bus_obj.name = \
            "Vanilla"
        assert mock_sess_base_bus_obj \
            .name == "Vanilla"

    def test_name_invalid_value(
            self, mock_sess_base_bus_obj):
        """
        Test case for setting an invalid value for the
        name property.
        """
        with pytest.raises(AssertionError):
            mock_sess_base_bus_obj.name = \
                123
    # OrganizationID
    # OrgCustomerID
    # apiKeyValue,
    # createdBy,
    # createdUTCDateTime
    # expirationUTCDateTime
    # isActive,
    # isTempUserKey,
    # name,
    # OrganizationID

    def test_organization_id(
            self, mock_sess_base_bus_obj, org_api_key):
        """
        Test case for the organization_id property.
        """
        org_api_key.organization_id = 1
        assert mock_sess_base_bus_obj \
            .organization_id == 1

    def test_organization_id_setter(
            self, mock_sess_base_bus_obj):
        """
        Test case for the organization_id setter.
        """
        mock_sess_base_bus_obj.organization_id = 1
        assert mock_sess_base_bus_obj \
            .organization_id == 1

    def test_organization_id_invalid_value(
            self, mock_sess_base_bus_obj):
        """
        Test case for setting an invalid value for the
        organization_id property.
        """
        with pytest.raises(AssertionError):
            mock_sess_base_bus_obj.organization_id = \
                "not-an-int"
    # OrgCustomerID

    def test_org_customer_id(
            self, mock_sess_base_bus_obj, org_api_key):
        """
        Test case for the
        org_customer_id property.
        """
        org_api_key.org_customer_id = 1
        assert mock_sess_base_bus_obj \
            .org_customer_id == 1

    def test_org_customer_id_setter(
            self, mock_sess_base_bus_obj):
        """
        Test case for the
        org_customer_id setter.
        """
        mock_sess_base_bus_obj.org_customer_id = 1
        assert mock_sess_base_bus_obj \
            .org_customer_id == 1

    def test_org_customer_id_invalid_value(
            self, mock_sess_base_bus_obj):
        """
        Test case for setting an invalid value for the
        org_customer_id property.
        """
        with pytest.raises(ValueError):
            mock_sess_base_bus_obj.org_customer_id = \
                "not-an-int"

    def test_insert_utc_date_time(
            self,
            mock_sess_base_bus_obj,
            org_api_key):
        """
        Test case for the
        insert_utc_date_time property.
        """
        test_datetime = datetime.utcnow()
        org_api_key.insert_utc_date_time = test_datetime
        assert mock_sess_base_bus_obj \
            .insert_utc_date_time == \
            test_datetime

    def test_insert_utc_date_time_setter(
            self, mock_sess_base_bus_obj):
        """
        Test case for the
        insert_utc_date_time setter.
        """
        test_datetime = datetime.utcnow()
        mock_sess_base_bus_obj.insert_utc_date_time = test_datetime
        assert mock_sess_base_bus_obj \
            .insert_utc_date_time == \
            test_datetime

    def test_insert_utc_date_time_invalid_value(
            self, mock_sess_base_bus_obj):
        """
        Test case for setting an invalid value for the
        insert_utc_date_time property.
        """
        with pytest.raises(AssertionError):
            mock_sess_base_bus_obj.insert_utc_date_time = \
                "not-a-datetime"

    def test_last_update_utc_date_time(
            self,
            mock_sess_base_bus_obj,
            org_api_key):
        """
        Test case for the
        last_update_utc_date_time property.
        """
        test_datetime = datetime.utcnow()
        org_api_key.last_update_utc_date_time = test_datetime
        assert mock_sess_base_bus_obj \
            .last_update_utc_date_time == \
            test_datetime

    def test_last_update_utc_date_time_setter(
            self, mock_sess_base_bus_obj):
        """
        Test case for the
        last_update_utc_date_time setter.
        """
        test_datetime = datetime.utcnow()
        mock_sess_base_bus_obj.last_update_utc_date_time = test_datetime
        assert mock_sess_base_bus_obj \
            .last_update_utc_date_time == \
            test_datetime

    def test_last_update_utc_date_time_invalid_value(
            self, mock_sess_base_bus_obj):
        """
        Test case for setting an invalid value for the
        last_update_utc_date_time property.
        """
        with pytest.raises(AssertionError):
            mock_sess_base_bus_obj.last_update_utc_date_time = \
                "not-a-datetime"
