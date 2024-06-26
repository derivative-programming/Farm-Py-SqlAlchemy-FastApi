# business/tests/customer_role_base_test.py
# pylint: disable=unused-import
# pylint: disable=redefined-outer-name

"""
This module contains unit tests for the
CustomerRoleBusObj class.
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
from business.customer_role_base import (
    CustomerRoleBaseBusObj)
from helpers.session_context import SessionContext
from managers.customer_role import (
    CustomerRoleManager)
from models import CustomerRole
from models.factory import (
    CustomerRoleFactory)
from services.logging_config import get_logger

from ..customer_role import CustomerRoleBusObj


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
def customer_role():
    """
    Fixture that returns a mock
    customer_role object.
    """
    return Mock(spec=CustomerRole)


@pytest.fixture
def mock_sess_base_bus_obj(
    mock_session_context, customer_role
):
    """
    Fixture that returns a
    CustomerRoleBaseBusObj instance.
    """
    mock_sess_base_bus_obj = CustomerRoleBaseBusObj(
        mock_session_context)
    mock_sess_base_bus_obj.customer_role = \
        customer_role
    return mock_sess_base_bus_obj


class TestCustomerRoleBaseBusObj:
    """
    Unit tests for the
    CustomerRoleBusObj class.
    """

    @pytest_asyncio.fixture(scope="function")
    async def obj_manager(self, session: AsyncSession):
        """
        Fixture that returns an instance of the
        CustomerRoleManager class.
        """
        session_context = SessionContext(dict(), session)
        return CustomerRoleManager(session_context)

    @pytest_asyncio.fixture(scope="function")
    async def new_bus_obj(self, session):
        """
        Fixture that returns an instance of the
        CustomerRoleBusObj class.
        """
        session_context = SessionContext(dict(), session)
        return CustomerRoleBusObj(session_context)

    @pytest_asyncio.fixture(scope="function")
    async def new_obj(self, session):
        """
        Fixture that returns a new instance of
        the CustomerRole class.
        """

        return await CustomerRoleFactory.create_async(
            session)

    @pytest.mark.asyncio
    async def test_create_customer_role(
        self,
        new_bus_obj: CustomerRoleBusObj
    ):
        """
        Test case for creating a new customer_role.
        """
        # Test creating a new customer_role

        assert new_bus_obj.customer_role_id == 0

        # assert isinstance(new_bus_obj.customer_role_id, int)
        assert isinstance(
            new_bus_obj.code, uuid.UUID)

        assert isinstance(
            new_bus_obj.last_change_code, int)

        assert new_bus_obj.insert_user_id == uuid.UUID(int=0)

        assert new_bus_obj.last_update_user_id == uuid.UUID(int=0)

        assert isinstance(new_bus_obj.customer_id,
                          int)
        assert isinstance(new_bus_obj.is_placeholder,
                          bool)
        assert isinstance(new_bus_obj.placeholder,
                          bool)
        assert isinstance(new_bus_obj.role_id,
                          int)

    @pytest.mark.asyncio
    async def test_load_with_customer_role_obj(
        self,
        obj_manager: CustomerRoleManager,
        new_bus_obj: CustomerRoleBusObj,
        new_obj: CustomerRole
    ):
        """
        Test case for loading data from a
        customer_role object instance.
        """

        new_bus_obj.load_from_obj_instance(
            new_obj)

        assert obj_manager.is_equal(
            new_bus_obj.customer_role, new_obj) is True

    @pytest.mark.asyncio
    async def test_load_with_customer_role_id(
        self,
        obj_manager: CustomerRoleManager,
        new_bus_obj: CustomerRoleBusObj,
        new_obj: CustomerRole
    ):
        """
        Test case for loading data from a
        customer_role ID.
        """

        new_obj_customer_role_id = \
            new_obj.customer_role_id

        await new_bus_obj.load_from_id(
            new_obj_customer_role_id)

        assert obj_manager.is_equal(
            new_bus_obj.customer_role, new_obj) is True

    @pytest.mark.asyncio
    async def test_load_with_customer_role_code(
        self,
        obj_manager: CustomerRoleManager,
        new_bus_obj: CustomerRoleBusObj,
        new_obj: CustomerRole
    ):
        """
        Test case for loading data from a
        customer_role code.
        """

        await new_bus_obj.load_from_code(
            new_obj.code)

        assert obj_manager.is_equal(
            new_bus_obj.customer_role, new_obj) is True

    @pytest.mark.asyncio
    async def test_load_with_customer_role_json(
        self,
        obj_manager: CustomerRoleManager,
        new_bus_obj: CustomerRoleBusObj,
        new_obj: CustomerRole
    ):
        """
        Test case for loading data from a
        customer_role JSON.
        """

        customer_role_json = \
            obj_manager.to_json(
                new_obj)

        await new_bus_obj.load_from_json(
            customer_role_json)

        assert obj_manager.is_equal(
            new_bus_obj.customer_role, new_obj) is True

    @pytest.mark.asyncio
    async def test_load_with_customer_role_dict(
        self,
        obj_manager: CustomerRoleManager,
        new_bus_obj: CustomerRoleBusObj,
        new_obj: CustomerRole
    ):
        """
        Test case for loading data from a
        customer_role dictionary.
        """

        logger.info("test_load_with_customer_role_dict 1")

        customer_role_dict = \
            obj_manager.to_dict(
                new_obj)

        logger.info(customer_role_dict)

        await new_bus_obj.load_from_dict(
            customer_role_dict)

        assert obj_manager.is_equal(
            new_bus_obj.customer_role,
            new_obj) is True

    @pytest.mark.asyncio
    async def test_get_nonexistent_customer_role(
        self,
        new_bus_obj: CustomerRoleBusObj
    ):
        """
        Test case for retrieving a nonexistent
        customer_role.
        """
        # Test retrieving a nonexistent
        # customer_role raises an exception
        await new_bus_obj.load_from_id(-1)

        # Assuming -1 is an id that wouldn't exist
        assert new_bus_obj.is_valid() is False

    @pytest.mark.asyncio
    async def test_update_customer_role(
        self,
        obj_manager: CustomerRoleManager,
        new_bus_obj: CustomerRoleBusObj,
        new_obj: CustomerRole
    ):
        """
        Test case for updating a customer_role's data.
        """
        # Test updating a customer_role's data

        new_obj_customer_role_id_value = \
            new_obj.customer_role_id

        new_obj = await \
            obj_manager.get_by_id(
                new_obj_customer_role_id_value)

        assert isinstance(new_obj,
                          CustomerRole)

        new_code = uuid.uuid4()

        new_bus_obj.load_from_obj_instance(
            new_obj)

        assert obj_manager.is_equal(
            new_bus_obj.customer_role,
            new_obj) is True

        new_bus_obj.code = new_code

        await new_bus_obj.save()

        new_obj_customer_role_id_value = \
            new_obj.customer_role_id

        new_obj = await \
            obj_manager.get_by_id(
                new_obj_customer_role_id_value)

        assert obj_manager.is_equal(
            new_bus_obj.customer_role,
            new_obj) is True

    @pytest.mark.asyncio
    async def test_delete_customer_role(
        self,
        obj_manager: CustomerRoleManager,
        new_bus_obj: CustomerRoleBusObj,
        new_obj: CustomerRole
    ):
        """
        Test case for deleting a customer_role.
        """

        assert new_bus_obj.customer_role is not None

        assert new_bus_obj.customer_role_id == 0

        new_bus_obj.load_from_obj_instance(
            new_obj)

        assert new_bus_obj.customer_role_id is not None

        await new_bus_obj.delete()

        new_obj_customer_role_id_value = \
            new_obj.customer_role_id

        new_obj = await \
            obj_manager.get_by_id(
                new_obj_customer_role_id_value)

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
        customer_role
    ):
        """
        Test case for refreshing the customer_role data.
        """
        with patch(
            "business.customer_role_base"
            ".CustomerRoleManager",
            autospec=True
        ) as mock_obj_manager:
            mock_obj_manager_instance = \
                mock_obj_manager.return_value
            mock_obj_manager_instance.refresh =\
                AsyncMock(return_value=customer_role)

            refreshed_mock_sess_base_bus_obj = await \
                mock_sess_base_bus_obj.refresh()
            assert refreshed_mock_sess_base_bus_obj \
                .customer_role == customer_role
            mock_obj_manager_instance.refresh \
                .assert_called_once_with(customer_role)

    def test_is_valid(
            self, mock_sess_base_bus_obj):
        """
        Test case for checking if the customer_role data is valid.
        """
        assert mock_sess_base_bus_obj.is_valid() is True

        mock_sess_base_bus_obj.customer_role = None
        assert mock_sess_base_bus_obj.is_valid() is False

    def test_to_dict(
            self, mock_sess_base_bus_obj):
        """
        Test case for converting the customer_role
        data to a dictionary.
        """
        with patch(
            "business.customer_role_base"
            ".CustomerRoleManager",
            autospec=True
        ) as mock_obj_manager:
            mock_obj_manager_instance = \
                mock_obj_manager.return_value
            mock_obj_manager_instance.to_dict = Mock(
                return_value={"key": "value"})

            customer_role_dict = mock_sess_base_bus_obj.to_dict()
            assert customer_role_dict == {"key": "value"}
            mock_obj_manager_instance.to_dict.assert_called_once_with(
                mock_sess_base_bus_obj.customer_role)

    def test_to_json(
            self, mock_sess_base_bus_obj):
        """
        Test case for converting the customer_role data to JSON.
        """
        with patch(
            "business.customer_role_base"
            ".CustomerRoleManager",
            autospec=True
        ) as mock_obj_manager:
            mock_obj_manager_instance = \
                mock_obj_manager.return_value
            mock_obj_manager_instance.to_json = Mock(
                return_value='{"key": "value"}')

            customer_role_json = mock_sess_base_bus_obj.to_json()
            assert customer_role_json == '{"key": "value"}'
            mock_obj_manager_instance.to_json.assert_called_once_with(
                mock_sess_base_bus_obj.customer_role)

    def test_get_obj(
            self, mock_sess_base_bus_obj, customer_role):
        """
        Test case for getting the customer_role object.
        """
        assert mock_sess_base_bus_obj.get_obj() == customer_role

    def test_get_object_name(
            self, mock_sess_base_bus_obj):
        """
        Test case for getting the object name.
        """
        assert mock_sess_base_bus_obj \
            .get_object_name() == "customer_role"

    def test_get_id(
            self, mock_sess_base_bus_obj, customer_role):
        """
        Test case for getting the customer_role ID.
        """
        customer_role.customer_role_id = 1
        assert mock_sess_base_bus_obj.get_id() == 1

    def test_customer_role_id(
            self, mock_sess_base_bus_obj, customer_role):
        """
        Test case for the customer_role_id property.
        """
        customer_role.customer_role_id = 1
        assert mock_sess_base_bus_obj.customer_role_id == 1

    def test_code(
            self, mock_sess_base_bus_obj, customer_role):
        """
        Test case for the code property.
        """
        test_uuid = uuid.uuid4()
        customer_role.code = test_uuid
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
            self, mock_sess_base_bus_obj, customer_role):
        """
        Test case to verify the behavior of the last_change_code
        attribute in the CustomerRoleBaseBusiness class.

        Args:
            mock_sess_base_bus_obj (CustomerRoleBaseBusiness):
                An instance of the
                CustomerRoleBaseBusiness class.
            customer_role (CustomerRole):
                An instance of the
                CustomerRole class.

        Returns:
            None
        """
        customer_role.last_change_code = 123
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
            self, mock_sess_base_bus_obj, customer_role):
        """
        Test case for the
        insert_user_id property.
        """
        test_uuid = uuid.uuid4()
        customer_role.insert_user_id = test_uuid
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
    # CustomerID
    # isPlaceholder

    def test_is_placeholder(
            self, mock_sess_base_bus_obj, customer_role):
        """
        Test case for the
        is_placeholder property.
        """
        customer_role.is_placeholder = True
        assert mock_sess_base_bus_obj \
            .is_placeholder is True

    def test_is_placeholder_setter(
            self, mock_sess_base_bus_obj):
        """
        Test case for the
        is_placeholder setter.
        """
        mock_sess_base_bus_obj.is_placeholder = \
            True
        assert mock_sess_base_bus_obj \
            .is_placeholder is True

    def test_is_placeholder_invalid_value(
            self, mock_sess_base_bus_obj):
        """
        Test case for setting an invalid value for the
        is_placeholder property.
        """
        with pytest.raises(ValueError):
            mock_sess_base_bus_obj.is_placeholder = \
                "not-a-boolean"
    # placeholder

    def test_placeholder(
            self, mock_sess_base_bus_obj, customer_role):
        """
        Test case for the
        placeholder property.
        """
        customer_role.placeholder = True
        assert mock_sess_base_bus_obj \
            .placeholder is True

    def test_placeholder_setter(
            self, mock_sess_base_bus_obj):
        """
        Test case for the
        placeholder setter.
        """
        mock_sess_base_bus_obj.placeholder = \
            True
        assert mock_sess_base_bus_obj \
            .placeholder is True

    def test_placeholder_invalid_value(
            self, mock_sess_base_bus_obj):
        """
        Test case for setting an invalid value for the
        placeholder property.
        """
        with pytest.raises(ValueError):
            mock_sess_base_bus_obj.placeholder = \
                "not-a-boolean"
    # RoleID
    # CustomerID

    def test_customer_id(
            self, mock_sess_base_bus_obj, customer_role):
        """
        Test case for the customer_id property.
        """
        customer_role.customer_id = 1
        assert mock_sess_base_bus_obj \
            .customer_id == 1

    def test_customer_id_setter(
            self, mock_sess_base_bus_obj):
        """
        Test case for the customer_id setter.
        """
        mock_sess_base_bus_obj.customer_id = 1
        assert mock_sess_base_bus_obj \
            .customer_id == 1

    def test_customer_id_invalid_value(
            self, mock_sess_base_bus_obj):
        """
        Test case for setting an invalid value for the
        customer_id property.
        """
        with pytest.raises(AssertionError):
            mock_sess_base_bus_obj.customer_id = \
                "not-an-int"
    # isPlaceholder,
    # placeholder,
    # RoleID

    def test_role_id(
            self, mock_sess_base_bus_obj, customer_role):
        """
        Test case for the
        role_id property.
        """
        customer_role.role_id = 1
        assert mock_sess_base_bus_obj \
            .role_id == 1

    def test_role_id_setter(
            self, mock_sess_base_bus_obj):
        """
        Test case for the
        role_id setter.
        """
        mock_sess_base_bus_obj.role_id = 1
        assert mock_sess_base_bus_obj \
            .role_id == 1

    def test_role_id_invalid_value(
            self, mock_sess_base_bus_obj):
        """
        Test case for setting an invalid value for the
        role_id property.
        """
        with pytest.raises(ValueError):
            mock_sess_base_bus_obj.role_id = \
                "not-an-int"

    def test_insert_utc_date_time(
            self,
            mock_sess_base_bus_obj,
            customer_role):
        """
        Test case for the
        insert_utc_date_time property.
        """
        test_datetime = datetime.utcnow()
        customer_role.insert_utc_date_time = test_datetime
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
            customer_role):
        """
        Test case for the
        last_update_utc_date_time property.
        """
        test_datetime = datetime.utcnow()
        customer_role.last_update_utc_date_time = test_datetime
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
