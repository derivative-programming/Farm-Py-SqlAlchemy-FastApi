# business/tests/org_customer_base_test.py
# pylint: disable=unused-import
# pylint: disable=redefined-outer-name

"""
This module contains unit tests for the
OrgCustomerBusObj class.
"""

import uuid  # noqa: F401
import math  # noqa: F401
from datetime import date, datetime, timezone  # noqa: F401
from decimal import Decimal  # noqa: F401
from unittest.mock import AsyncMock, Mock, patch

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

import current_runtime  # noqa: F401
from business.org_customer_base import (
    OrgCustomerBaseBusObj)
from helpers.session_context import SessionContext
from managers.org_customer import (
    OrgCustomerManager)
from models import OrgCustomer
from models.factory import (
    OrgCustomerFactory)
from services.logging_config import get_logger

from ..org_customer import OrgCustomerBusObj


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
def org_customer():
    """
    Fixture that returns a mock
    org_customer object.
    """
    return Mock(spec=OrgCustomer)


@pytest.fixture
def mock_sess_base_bus_obj(
    mock_session_context, org_customer
):
    """
    Fixture that returns a
    OrgCustomerBaseBusObj instance.
    """
    mock_sess_base_bus_obj = OrgCustomerBaseBusObj(
        mock_session_context)
    mock_sess_base_bus_obj.org_customer = \
        org_customer
    return mock_sess_base_bus_obj


class TestOrgCustomerBaseBusObj:
    """
    Unit tests for the
    OrgCustomerBusObj class.
    """

    @pytest_asyncio.fixture(scope="function")
    async def obj_manager(self, session: AsyncSession):
        """
        Fixture that returns an instance of the
        OrgCustomerManager class.
        """
        session_context = SessionContext(dict(), session)
        return OrgCustomerManager(session_context)

    @pytest_asyncio.fixture(scope="function")
    async def new_bus_obj(self, session):
        """
        Fixture that returns an instance of the
        OrgCustomerBusObj class.
        """
        session_context = SessionContext(dict(), session)
        return OrgCustomerBusObj(
            session_context)

    @pytest_asyncio.fixture(scope="function")
    async def new_obj(self, session):
        """
        Fixture that returns a new instance of
        the OrgCustomer class.
        """

        return await OrgCustomerFactory.create_async(
            session)

    @pytest.mark.asyncio
    async def test_create_org_customer(
        self,
        new_bus_obj: OrgCustomerBusObj
    ):
        """
        Test case for creating a new org_customer.
        """
        # Test creating a new org_customer

        assert new_bus_obj.org_customer_id == 0

        assert isinstance(new_bus_obj.org_customer_id, int)
        assert isinstance(
            new_bus_obj.code, uuid.UUID)

        assert isinstance(
            new_bus_obj.last_change_code, int)

        assert new_bus_obj.insert_user_id == uuid.UUID(int=0)

        assert new_bus_obj.last_update_user_id == uuid.UUID(int=0)

        assert isinstance(new_bus_obj.customer_id,
                          int)
        assert isinstance(new_bus_obj.email,
                          str)
        assert isinstance(new_bus_obj.organization_id,
                          int)

    @pytest.mark.asyncio
    async def test_load_with_org_customer_obj(
        self,
        obj_manager: OrgCustomerManager,
        new_bus_obj: OrgCustomerBusObj,
        new_obj: OrgCustomer
    ):
        """
        Test case for loading data from a
        org_customer object instance.
        """

        new_bus_obj.load_from_obj_instance(
            new_obj)

        assert obj_manager.is_equal(
            new_bus_obj.org_customer, new_obj) is True

    @pytest.mark.asyncio
    async def test_load_with_org_customer_id(
        self,
        obj_manager: OrgCustomerManager,
        new_bus_obj: OrgCustomerBusObj,
        new_obj: OrgCustomer
    ):
        """
        Test case for loading data from a
        org_customer ID.
        """

        new_obj_org_customer_id = \
            new_obj.org_customer_id

        await new_bus_obj.load_from_id(
            new_obj_org_customer_id)

        assert obj_manager.is_equal(
            new_bus_obj.org_customer, new_obj) is True

    @pytest.mark.asyncio
    async def test_load_with_org_customer_code(
        self,
        obj_manager: OrgCustomerManager,
        new_bus_obj: OrgCustomerBusObj,
        new_obj: OrgCustomer
    ):
        """
        Test case for loading data from a
        org_customer code.
        """

        await new_bus_obj.load_from_code(
            new_obj.code)

        assert obj_manager.is_equal(
            new_bus_obj.org_customer, new_obj) is True

    @pytest.mark.asyncio
    async def test_load_with_org_customer_json(
        self,
        obj_manager: OrgCustomerManager,
        new_bus_obj: OrgCustomerBusObj,
        new_obj: OrgCustomer
    ):
        """
        Test case for loading data from a
        org_customer JSON.
        """

        org_customer_json = \
            obj_manager.to_json(
                new_obj)

        await new_bus_obj.load_from_json(
            org_customer_json)

        assert obj_manager.is_equal(
            new_bus_obj.org_customer, new_obj) is True

    @pytest.mark.asyncio
    async def test_load_with_org_customer_dict(
        self,
        obj_manager: OrgCustomerManager,
        new_bus_obj: OrgCustomerBusObj,
        new_obj: OrgCustomer
    ):
        """
        Test case for loading data from a
        org_customer dictionary.
        """

        logger.info("test_load_with_org_customer_dict 1")

        org_customer_dict = \
            obj_manager.to_dict(
                new_obj)

        logger.info(org_customer_dict)

        await new_bus_obj.load_from_dict(
            org_customer_dict)

        assert obj_manager.is_equal(
            new_bus_obj.org_customer,
            new_obj) is True

    @pytest.mark.asyncio
    async def test_get_nonexistent_org_customer(
        self,
        new_bus_obj: OrgCustomerBusObj
    ):
        """
        Test case for retrieving a nonexistent
        org_customer.
        """
        # Test retrieving a nonexistent
        # org_customer raises an exception
        await new_bus_obj.load_from_id(-1)

        # Assuming -1 is an id that wouldn't exist
        assert new_bus_obj.is_valid() is False

    @pytest.mark.asyncio
    async def test_update_org_customer(
        self,
        obj_manager: OrgCustomerManager,
        new_bus_obj: OrgCustomerBusObj,
        new_obj: OrgCustomer
    ):
        """
        Test case for updating a org_customer's data.
        """
        # Test updating a org_customer's data

        new_obj_org_customer_id_value = \
            new_obj.org_customer_id

        new_obj = await \
            obj_manager.get_by_id(
                new_obj_org_customer_id_value)

        assert isinstance(new_obj,
                          OrgCustomer)

        new_code = uuid.uuid4()

        new_bus_obj.load_from_obj_instance(
            new_obj)

        assert obj_manager.is_equal(
            new_bus_obj.org_customer,
            new_obj) is True

        new_bus_obj.code = new_code

        await new_bus_obj.save()

        new_obj_org_customer_id_value = \
            new_obj.org_customer_id

        new_obj = await \
            obj_manager.get_by_id(
                new_obj_org_customer_id_value)

        assert obj_manager.is_equal(
            new_bus_obj.org_customer,
            new_obj) is True

    @pytest.mark.asyncio
    async def test_delete_org_customer(
        self,
        obj_manager: OrgCustomerManager,
        new_bus_obj: OrgCustomerBusObj,
        new_obj: OrgCustomer
    ):
        """
        Test case for deleting a org_customer.
        """

        assert new_bus_obj.org_customer is not None

        assert new_bus_obj.org_customer_id == 0

        new_bus_obj.load_from_obj_instance(
            new_obj)

        assert new_bus_obj.org_customer_id is not None

        await new_bus_obj.delete()

        new_obj_org_customer_id_value = \
            new_obj.org_customer_id

        new_obj = await \
            obj_manager.get_by_id(
                new_obj_org_customer_id_value)

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
        org_customer
    ):
        """
        Test case for refreshing the org_customer data.
        """
        with patch(
            "business.org_customer_base"
            ".OrgCustomerManager",
            autospec=True
        ) as mock_obj_manager:
            mock_obj_manager_instance = \
                mock_obj_manager.return_value
            mock_obj_manager_instance.refresh =\
                AsyncMock(return_value=org_customer)

            refreshed_mock_sess_base_bus_obj = await \
                mock_sess_base_bus_obj.refresh()
            assert refreshed_mock_sess_base_bus_obj \
                .org_customer == org_customer
            mock_obj_manager_instance.refresh \
                .assert_called_once_with(org_customer)

    def test_is_valid(
            self, mock_sess_base_bus_obj):
        """
        Test case for checking if the org_customer data is valid.
        """
        assert mock_sess_base_bus_obj.is_valid() is True

        mock_sess_base_bus_obj.org_customer = None
        assert mock_sess_base_bus_obj.is_valid() is False

    def test_to_dict(
            self, mock_sess_base_bus_obj):
        """
        Test case for converting the org_customer
        data to a dictionary.
        """
        with patch(
            "business.org_customer_base"
            ".OrgCustomerManager",
            autospec=True
        ) as mock_obj_manager:
            mock_obj_manager_instance = \
                mock_obj_manager.return_value
            mock_obj_manager_instance.to_dict = Mock(
                return_value={"key": "value"})

            org_customer_dict = mock_sess_base_bus_obj.to_dict()
            assert org_customer_dict == {"key": "value"}
            mock_obj_manager_instance.to_dict.assert_called_once_with(
                mock_sess_base_bus_obj.org_customer)

    def test_to_json(
            self, mock_sess_base_bus_obj):
        """
        Test case for converting the org_customer data to JSON.
        """
        with patch(
            "business.org_customer_base"
            ".OrgCustomerManager",
            autospec=True
        ) as mock_obj_manager:
            mock_obj_manager_instance = \
                mock_obj_manager.return_value
            mock_obj_manager_instance.to_json = Mock(
                return_value='{"key": "value"}')

            org_customer_json = mock_sess_base_bus_obj.to_json()
            assert org_customer_json == '{"key": "value"}'
            mock_obj_manager_instance.to_json.assert_called_once_with(
                mock_sess_base_bus_obj.org_customer)

    def test_get_obj(
            self, mock_sess_base_bus_obj, org_customer):
        """
        Test case for getting the org_customer object.
        """
        assert mock_sess_base_bus_obj.get_obj() == org_customer

    def test_get_object_name(
            self, mock_sess_base_bus_obj):
        """
        Test case for getting the object name.
        """
        assert mock_sess_base_bus_obj \
            .get_object_name() == "org_customer"

    def test_get_id(
            self, mock_sess_base_bus_obj, org_customer):
        """
        Test case for getting the org_customer ID.
        """
        org_customer.org_customer_id = 1
        assert mock_sess_base_bus_obj.get_id() == 1

    def test_org_customer_id(
            self, mock_sess_base_bus_obj, org_customer):
        """
        Test case for the org_customer_id property.
        """
        org_customer.org_customer_id = 1
        assert mock_sess_base_bus_obj.org_customer_id == 1

    def test_code(
            self, mock_sess_base_bus_obj, org_customer):
        """
        Test case for the code property.
        """
        test_uuid = uuid.uuid4()
        org_customer.code = test_uuid
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
            self, mock_sess_base_bus_obj, org_customer):
        """
        Test case to verify the behavior of the last_change_code
        attribute in the OrgCustomerBaseBusiness class.

        Args:
            mock_sess_base_bus_obj (OrgCustomerBaseBusiness):
                An instance of the
                OrgCustomerBaseBusiness class.
            org_customer (OrgCustomer):
                An instance of the
                OrgCustomer class.

        Returns:
            None
        """
        org_customer.last_change_code = 123
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
            self, mock_sess_base_bus_obj, org_customer):
        """
        Test case for the
        insert_user_id property.
        """
        test_uuid = uuid.uuid4()
        org_customer.insert_user_id = test_uuid
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
    # email

    def test_email(
            self, mock_sess_base_bus_obj, org_customer):
        """
        Test case for the
        email property.
        """
        org_customer.email = \
            "test@example.com"
        assert mock_sess_base_bus_obj \
            .email == "test@example.com"

    def test_email_setter(
            self, mock_sess_base_bus_obj):
        """
        Test case for the
        email setter.
        """
        mock_sess_base_bus_obj.email = \
            "test@example.com"
        assert mock_sess_base_bus_obj \
            .email == "test@example.com"

    def test_email_invalid_value(
            self, mock_sess_base_bus_obj):
        """
        Test case for setting an invalid value for the
        email property.
        """
        with pytest.raises(AssertionError):
            mock_sess_base_bus_obj.email = \
                123
    # OrganizationID
    # CustomerID

    def test_customer_id(
            self, mock_sess_base_bus_obj, org_customer):
        """
        Test case for the
        customer_id property.
        """
        org_customer.customer_id = 1
        assert mock_sess_base_bus_obj \
            .customer_id == 1

    def test_customer_id_setter(
            self, mock_sess_base_bus_obj):
        """
        Test case for the
        customer_id setter.
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
        with pytest.raises(ValueError):
            mock_sess_base_bus_obj.customer_id = \
                "not-an-int"
    # email,
    # OrganizationID

    def test_organization_id(
            self, mock_sess_base_bus_obj, org_customer):
        """
        Test case for the organization_id property.
        """
        org_customer.organization_id = 1
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

    def test_insert_utc_date_time(
            self,
            mock_sess_base_bus_obj,
            org_customer):
        """
        Test case for the
        insert_utc_date_time property.
        """
        test_datetime = datetime.now(timezone.utc)
        org_customer.insert_utc_date_time = test_datetime
        assert mock_sess_base_bus_obj \
            .insert_utc_date_time == \
            test_datetime

    def test_insert_utc_date_time_setter(
            self, mock_sess_base_bus_obj):
        """
        Test case for the
        insert_utc_date_time setter.
        """
        test_datetime = datetime.now(timezone.utc)
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
            org_customer):
        """
        Test case for the
        last_update_utc_date_time property.
        """
        test_datetime = datetime.now(timezone.utc)
        org_customer.last_update_utc_date_time = test_datetime
        assert mock_sess_base_bus_obj \
            .last_update_utc_date_time == \
            test_datetime

    def test_last_update_utc_date_time_setter(
            self, mock_sess_base_bus_obj):
        """
        Test case for the
        last_update_utc_date_time setter.
        """
        test_datetime = datetime.now(timezone.utc)
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
