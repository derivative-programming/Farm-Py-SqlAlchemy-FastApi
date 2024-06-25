# business/tests/customer_base_test.py
# pylint: disable=unused-import
# pylint: disable=redefined-outer-name

"""
This module contains unit tests for the
CustomerBusObj class.
"""

import uuid  # noqa: F401
import math
from datetime import date, datetime  # noqa: F401
from decimal import Decimal  # noqa: F401
from unittest.mock import AsyncMock, Mock, patch

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

import current_runtime  # noqa: F401
from business.customer_base import (
    CustomerBaseBusObj)
from helpers.session_context import SessionContext
from managers.customer import (
    CustomerManager)
from models import Customer
from models.factory import (
    CustomerFactory)
from services.logging_config import get_logger

from ..customer import CustomerBusObj


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
def customer():
    """
    Fixture that returns a mock customer object.
    """
    return Mock(spec=Customer)


@pytest.fixture
def customer_base_bus_obj(
    fake_session_context, customer
):
    """
    Fixture that returns a CustomerBaseBusObj instance.
    """
    customer_base = CustomerBaseBusObj(
        fake_session_context)
    customer_base.customer = customer
    return customer_base


class TestCustomerBaseBusObj:
    """
    Unit tests for the
    CustomerBusObj class.
    """

    @pytest_asyncio.fixture(scope="function")
    async def customer_manager(self, session: AsyncSession):
        """
        Fixture that returns an instance of the
        CustomerManager class.
        """
        session_context = SessionContext(dict(), session)
        return CustomerManager(session_context)

    @pytest_asyncio.fixture(scope="function")
    async def customer_bus_obj(self, session):
        """
        Fixture that returns an instance of the
        CustomerBusObj class.
        """
        session_context = SessionContext(dict(), session)
        return CustomerBusObj(session_context)

    @pytest_asyncio.fixture(scope="function")
    async def new_customer(self, session):
        """
        Fixture that returns a new instance of
        the Customer class.
        """

        return await CustomerFactory.create_async(
            session)

    @pytest.mark.asyncio
    async def test_create_customer(
        self,
        customer_bus_obj: CustomerBusObj
    ):
        """
        Test case for creating a new customer.
        """
        # Test creating a new customer

        assert customer_bus_obj.customer_id == 0

        # assert isinstance(customer_bus_obj.customer_id, int)
        assert isinstance(
            customer_bus_obj.code, uuid.UUID)

        assert isinstance(
            customer_bus_obj.last_change_code, int)

        assert customer_bus_obj.insert_user_id == uuid.UUID(int=0)

        assert customer_bus_obj.last_update_user_id == uuid.UUID(int=0)

        assert isinstance(customer_bus_obj.active_organization_id,
                          int)
        assert isinstance(customer_bus_obj.email,
                          str)
        assert isinstance(customer_bus_obj.email_confirmed_utc_date_time,
                          datetime)
        assert isinstance(customer_bus_obj.first_name,
                          str)
        assert isinstance(customer_bus_obj.forgot_password_key_expiration_utc_date_time,
                          datetime)
        assert isinstance(customer_bus_obj.forgot_password_key_value,
                          str)
        # fs_user_code_value
        assert isinstance(customer_bus_obj.fs_user_code_value,
                          uuid.UUID)
        assert isinstance(customer_bus_obj.is_active,
                          bool)
        assert isinstance(customer_bus_obj.is_email_allowed,
                          bool)
        assert isinstance(customer_bus_obj.is_email_confirmed,
                          bool)
        assert isinstance(customer_bus_obj.is_email_marketing_allowed,
                          bool)
        assert isinstance(customer_bus_obj.is_locked,
                          bool)
        assert isinstance(customer_bus_obj.is_multiple_organizations_allowed,
                          bool)
        assert isinstance(customer_bus_obj.is_verbose_logging_forced,
                          bool)
        assert isinstance(customer_bus_obj.last_login_utc_date_time,
                          datetime)
        assert isinstance(customer_bus_obj.last_name,
                          str)
        assert isinstance(customer_bus_obj.password,
                          str)
        assert isinstance(customer_bus_obj.phone,
                          str)
        assert isinstance(customer_bus_obj.province,
                          str)
        assert isinstance(customer_bus_obj.registration_utc_date_time,
                          datetime)
        assert isinstance(customer_bus_obj.tac_id,
                          int)
        assert isinstance(customer_bus_obj.utc_offset_in_minutes,
                          int)
        assert isinstance(customer_bus_obj.zip,
                          str)

    @pytest.mark.asyncio
    async def test_load_with_customer_obj(
        self,
        customer_manager: CustomerManager,
        customer_bus_obj: CustomerBusObj,
        new_customer: Customer
    ):
        """
        Test case for loading data from a
        customer object instance.
        """

        customer_bus_obj.load_from_obj_instance(
            new_customer)

        assert customer_manager.is_equal(
            customer_bus_obj.customer, new_customer) is True

    @pytest.mark.asyncio
    async def test_load_with_customer_id(
        self,
        customer_manager: CustomerManager,
        customer_bus_obj: CustomerBusObj,
        new_customer: Customer
    ):
        """
        Test case for loading data from a
        customer ID.
        """

        new_customer_customer_id = \
            new_customer.customer_id

        await customer_bus_obj.load_from_id(
            new_customer_customer_id)

        assert customer_manager.is_equal(
            customer_bus_obj.customer, new_customer) is True

    @pytest.mark.asyncio
    async def test_load_with_customer_code(
        self,
        customer_manager: CustomerManager,
        customer_bus_obj: CustomerBusObj,
        new_customer: Customer
    ):
        """
        Test case for loading data from a
        customer code.
        """

        await customer_bus_obj.load_from_code(
            new_customer.code)

        assert customer_manager.is_equal(
            customer_bus_obj.customer, new_customer) is True

    @pytest.mark.asyncio
    async def test_load_with_customer_json(
        self,
        customer_manager: CustomerManager,
        customer_bus_obj: CustomerBusObj,
        new_customer: Customer
    ):
        """
        Test case for loading data from a
        customer JSON.
        """

        customer_json = \
            customer_manager.to_json(
                new_customer)

        await customer_bus_obj.load_from_json(
            customer_json)

        assert customer_manager.is_equal(
            customer_bus_obj.customer, new_customer) is True

    @pytest.mark.asyncio
    async def test_load_with_customer_dict(
        self,
        customer_manager: CustomerManager,
        customer_bus_obj: CustomerBusObj,
        new_customer: Customer
    ):
        """
        Test case for loading data from a
        customer dictionary.
        """

        logger.info("test_load_with_customer_dict 1")

        customer_dict = \
            customer_manager.to_dict(
                new_customer)

        logger.info(customer_dict)

        await customer_bus_obj.load_from_dict(
            customer_dict)

        assert customer_manager.is_equal(
            customer_bus_obj.customer,
            new_customer) is True

    @pytest.mark.asyncio
    async def test_get_nonexistent_customer(
        self,
        customer_bus_obj: CustomerBusObj
    ):
        """
        Test case for retrieving a nonexistent customer.
        """
        # Test retrieving a nonexistent
        # customer raises an exception
        await customer_bus_obj.load_from_id(-1)

        # Assuming -1 is an id that wouldn't exist
        assert customer_bus_obj.is_valid() is False

    @pytest.mark.asyncio
    async def test_update_customer(
        self,
        customer_manager: CustomerManager,
        customer_bus_obj: CustomerBusObj,
        new_customer: Customer
    ):
        """
        Test case for updating a customer's data.
        """
        # Test updating a customer's data

        new_customer_customer_id_value = new_customer.customer_id

        new_customer = await \
            customer_manager.get_by_id(
                new_customer_customer_id_value)

        assert isinstance(new_customer,
                          Customer)

        new_code = uuid.uuid4()

        customer_bus_obj.load_from_obj_instance(
            new_customer)

        assert customer_manager.is_equal(
            customer_bus_obj.customer,
            new_customer) is True

        customer_bus_obj.code = new_code

        await customer_bus_obj.save()

        new_customer_customer_id_value = new_customer.customer_id

        new_customer = await \
            customer_manager.get_by_id(
                new_customer_customer_id_value)

        assert customer_manager.is_equal(
            customer_bus_obj.customer,
            new_customer) is True

    @pytest.mark.asyncio
    async def test_delete_customer(
        self,
        customer_manager: CustomerManager,
        customer_bus_obj: CustomerBusObj,
        new_customer: Customer
    ):
        """
        Test case for deleting a customer.
        """

        assert customer_bus_obj.customer is not None

        assert customer_bus_obj.customer_id == 0

        customer_bus_obj.load_from_obj_instance(
            new_customer)

        assert customer_bus_obj.customer_id is not None

        await customer_bus_obj.delete()

        new_customer_customer_id_value = new_customer.customer_id

        new_customer = await \
            customer_manager.get_by_id(
                new_customer_customer_id_value)

        assert new_customer is None

    def test_get_session_context(
        self,
        customer_base_bus_obj,
        fake_session_context
    ):
        """
        Test case for getting the session context.
        """
        assert customer_base_bus_obj.get_session_context() == fake_session_context

    @pytest.mark.asyncio
    async def test_refresh(
        self, customer_base_bus_obj, customer):
        """
        Test case for refreshing the customer data.
        """
        with patch(
            'business.customer_base.CustomerManager',
            autospec=True
        ) as mock_customer_manager:
            mock_customer_manager_instance = \
                mock_customer_manager.return_value
            mock_customer_manager_instance.refresh =\
                AsyncMock(return_value=customer)

            refreshed_customer_base = await customer_base_bus_obj.refresh()
            assert refreshed_customer_base.customer == customer
            mock_customer_manager_instance.refresh.assert_called_once_with(customer)

    def test_is_valid(
            self, customer_base_bus_obj):
        """
        Test case for checking if the customer data is valid.
        """
        assert customer_base_bus_obj.is_valid() is True

        customer_base_bus_obj.customer = None
        assert customer_base_bus_obj.is_valid() is False

    def test_to_dict(
            self, customer_base_bus_obj):
        """
        Test case for converting the customer data to a dictionary.
        """
        with patch(
            'business.customer_base.CustomerManager',
            autospec=True
        ) as mock_customer_manager:
            mock_customer_manager_instance = \
                mock_customer_manager.return_value
            mock_customer_manager_instance.to_dict = Mock(
                return_value={"key": "value"})

            customer_dict = customer_base_bus_obj.to_dict()
            assert customer_dict == {"key": "value"}
            mock_customer_manager_instance.to_dict.assert_called_once_with(
                customer_base_bus_obj.customer)

    def test_to_json(
            self, customer_base_bus_obj):
        """
        Test case for converting the customer data to JSON.
        """
        with patch(
            'business.customer_base.CustomerManager',
            autospec=True
        ) as mock_customer_manager:
            mock_customer_manager_instance = \
                mock_customer_manager.return_value
            mock_customer_manager_instance.to_json = Mock(
                return_value='{"key": "value"}')

            customer_json = customer_base_bus_obj.to_json()
            assert customer_json == '{"key": "value"}'
            mock_customer_manager_instance.to_json.assert_called_once_with(
                customer_base_bus_obj.customer)

    def test_get_obj(
            self, customer_base_bus_obj, customer):
        """
        Test case for getting the customer object.
        """
        assert customer_base_bus_obj.get_obj() == customer

    def test_get_object_name(
            self, customer_base_bus_obj):
        """
        Test case for getting the object name.
        """
        assert customer_base_bus_obj.get_object_name() == "customer"

    def test_get_id(
            self, customer_base_bus_obj, customer):
        """
        Test case for getting the customer ID.
        """
        customer.customer_id = 1
        assert customer_base_bus_obj.get_id() == 1

    def test_customer_id(
            self, customer_base_bus_obj, customer):
        """
        Test case for the customer_id property.
        """
        customer.customer_id = 1
        assert customer_base_bus_obj.customer_id == 1

    def test_code(
            self, customer_base_bus_obj, customer):
        """
        Test case for the code property.
        """
        test_uuid = uuid.uuid4()
        customer.code = test_uuid
        assert customer_base_bus_obj.code == test_uuid

    def test_code_setter(
            self, customer_base_bus_obj):
        """
        Test case for the code setter.
        """
        test_uuid = uuid.uuid4()
        customer_base_bus_obj.code = test_uuid
        assert customer_base_bus_obj.code == test_uuid

    def test_code_invalid_value(
            self, customer_base_bus_obj):
        """
        Test case for setting an invalid value for the code property.
        """
        with pytest.raises(ValueError):
            customer_base_bus_obj.code = "not-a-uuid"

    def test_last_change_code(
            self, customer_base_bus_obj, customer):
        """
        Test case to verify the behavior of the last_change_code
        attribute in the CustomerBaseBusiness class.

        Args:
            customer_base_bus_obj (CustomerBaseBusiness):
                An instance of the
                CustomerBaseBusiness class.
            customer (Customer): An instance of the
                Customer class.

        Returns:
            None
        """
        customer.last_change_code = 123
        assert customer_base_bus_obj.last_change_code == 123

    def test_last_change_code_setter(
            self, customer_base_bus_obj):
        """
        Test case for the last_change_code setter.
        """
        customer_base_bus_obj.last_change_code = 123
        assert customer_base_bus_obj.last_change_code == 123

    def test_last_change_code_invalid_value(
            self, customer_base_bus_obj):
        """
        Test case for setting an invalid value for the
        last_change_code property.
        """
        with pytest.raises(ValueError):
            customer_base_bus_obj.last_change_code = "not-an-int"

    def test_insert_user_id(
            self, customer_base_bus_obj, customer):
        """
        Test case for the insert_user_id property.
        """
        test_uuid = uuid.uuid4()
        customer.insert_user_id = test_uuid
        assert customer_base_bus_obj.insert_user_id == test_uuid

    def test_insert_user_id_setter(
            self, customer_base_bus_obj):
        """
        Test case for the insert_user_id setter.
        """
        test_uuid = uuid.uuid4()
        customer_base_bus_obj.insert_user_id = test_uuid
        assert customer_base_bus_obj.insert_user_id == test_uuid

    def test_insert_user_id_invalid_value(
            self, customer_base_bus_obj):
        """
        Test case for setting an invalid value for the
        insert_user_id property.
        """
        with pytest.raises(ValueError):
            customer_base_bus_obj.insert_user_id = "not-a-uuid"
    # activeOrganizationID

    def test_active_organization_id(
            self, customer_base_bus_obj, customer):
        """
        Test case for the active_organization_id property.
        """
        customer.active_organization_id = 1
        assert customer_base_bus_obj.active_organization_id == 1

    def test_active_organization_id_setter(
            self, customer_base_bus_obj):
        """
        Test case for the active_organization_id setter.
        """
        customer_base_bus_obj.active_organization_id = 1
        assert customer_base_bus_obj.active_organization_id == 1

    def test_active_organization_id_invalid_value(self, customer_base_bus_obj):
        """
        Test case for setting an invalid value for the
        active_organization_id property.
        """
        with pytest.raises(AssertionError):
            customer_base_bus_obj.active_organization_id = "not-an-int"
    # email

    def test_email(
            self, customer_base_bus_obj, customer):
        """
        Test case for the email property.
        """
        customer.email = "test@example.com"
        assert customer_base_bus_obj.email == "test@example.com"

    def test_email_setter(
            self, customer_base_bus_obj):
        """
        Test case for the email setter.
        """
        customer_base_bus_obj.email = "test@example.com"
        assert customer_base_bus_obj.email == "test@example.com"

    def test_email_invalid_value(
            self, customer_base_bus_obj):
        """
        Test case for setting an invalid value for the
        email property.
        """
        with pytest.raises(AssertionError):
            customer_base_bus_obj.email = 123
    # emailConfirmedUTCDateTime

    def test_email_confirmed_utc_date_time(
            self, customer_base_bus_obj, customer):
        """
        Test case for the email_confirmed_utc_date_time property.
        """
        test_datetime = datetime.utcnow()
        customer.email_confirmed_utc_date_time = test_datetime
        assert customer_base_bus_obj.email_confirmed_utc_date_time == test_datetime

    def test_email_confirmed_utc_date_time_setter(
            self, customer_base_bus_obj):
        """
        Test case for the email_confirmed_utc_date_time setter.
        """
        test_datetime = datetime.utcnow()
        customer_base_bus_obj.email_confirmed_utc_date_time = test_datetime
        assert customer_base_bus_obj.email_confirmed_utc_date_time == test_datetime

    def test_email_confirmed_utc_date_time_invalid_value(
            self, customer_base_bus_obj):
        """
        Test case for setting an invalid value for the
        email_confirmed_utc_date_time property.
        """
        with pytest.raises(AssertionError):
            customer_base_bus_obj.email_confirmed_utc_date_time = "not-a-datetime"
    # firstName

    def test_first_name(
            self, customer_base_bus_obj, customer):
        """
        Test case for the first_name property.
        """
        customer.first_name = "Vanilla"
        assert customer_base_bus_obj.first_name == "Vanilla"

    def test_first_name_setter(
            self, customer_base_bus_obj):
        """
        Test case for the first_name setter.
        """
        customer_base_bus_obj.first_name = "Vanilla"
        assert customer_base_bus_obj.first_name == "Vanilla"

    def test_first_name_invalid_value(
            self, customer_base_bus_obj):
        """
        Test case for setting an invalid value for the
        first_name property.
        """
        with pytest.raises(AssertionError):
            customer_base_bus_obj.first_name = 123
    # forgotPasswordKeyExpirationUTCDateTime

    def test_forgot_password_key_expiration_utc_date_time(
            self, customer_base_bus_obj, customer):
        """
        Test case for the forgot_password_key_expiration_utc_date_time property.
        """
        test_datetime = datetime.utcnow()
        customer.forgot_password_key_expiration_utc_date_time = test_datetime
        assert customer_base_bus_obj.forgot_password_key_expiration_utc_date_time == test_datetime

    def test_forgot_password_key_expiration_utc_date_time_setter(
            self, customer_base_bus_obj):
        """
        Test case for the forgot_password_key_expiration_utc_date_time setter.
        """
        test_datetime = datetime.utcnow()
        customer_base_bus_obj.forgot_password_key_expiration_utc_date_time = test_datetime
        assert customer_base_bus_obj.forgot_password_key_expiration_utc_date_time == test_datetime

    def test_forgot_password_key_expiration_utc_date_time_invalid_value(
            self, customer_base_bus_obj):
        """
        Test case for setting an invalid value for the
        forgot_password_key_expiration_utc_date_time property.
        """
        with pytest.raises(AssertionError):
            customer_base_bus_obj.forgot_password_key_expiration_utc_date_time = "not-a-datetime"
    # forgotPasswordKeyValue

    def test_forgot_password_key_value(
            self, customer_base_bus_obj, customer):
        """
        Test case for the forgot_password_key_value property.
        """
        customer.forgot_password_key_value = "Vanilla"
        assert customer_base_bus_obj.forgot_password_key_value == "Vanilla"

    def test_forgot_password_key_value_setter(
            self, customer_base_bus_obj):
        """
        Test case for the forgot_password_key_value setter.
        """
        customer_base_bus_obj.forgot_password_key_value = "Vanilla"
        assert customer_base_bus_obj.forgot_password_key_value == "Vanilla"

    def test_forgot_password_key_value_invalid_value(
            self, customer_base_bus_obj):
        """
        Test case for setting an invalid value for the
        forgot_password_key_value property.
        """
        with pytest.raises(AssertionError):
            customer_base_bus_obj.forgot_password_key_value = 123
    # fSUserCodeValue

    def test_fs_user_code_value(
            self, customer_base_bus_obj, customer):
        """
        Test case for the fs_user_code_value property.
        """
        test_uuid = uuid.uuid4()
        customer.fs_user_code_value = test_uuid
        assert customer_base_bus_obj.fs_user_code_value == test_uuid

    def test_fs_user_code_value_setter(
            self, customer_base_bus_obj):
        """
        Test case for the fs_user_code_value setter.
        """
        test_uuid = uuid.uuid4()
        customer_base_bus_obj.fs_user_code_value = test_uuid
        assert customer_base_bus_obj.fs_user_code_value == test_uuid

    def test_fs_user_code_value_invalid_value(
            self, customer_base_bus_obj):
        """
        Test case for setting an invalid value for the
        fs_user_code_value property.
        """
        with pytest.raises(AssertionError):
            customer_base_bus_obj.fs_user_code_value = "not-a-uuid"
    # isActive

    def test_is_active(
            self, customer_base_bus_obj, customer):
        """
        Test case for the is_active property.
        """
        customer.is_active = True
        assert customer_base_bus_obj.is_active is True

    def test_is_active_setter(
            self, customer_base_bus_obj):
        """
        Test case for the is_active setter.
        """
        customer_base_bus_obj.is_active = True
        assert customer_base_bus_obj.is_active is True

    def test_is_active_invalid_value(
            self, customer_base_bus_obj):
        """
        Test case for setting an invalid value for the
        is_active property.
        """
        with pytest.raises(ValueError):
            customer_base_bus_obj.is_active = "not-a-boolean"
    # isEmailAllowed

    def test_is_email_allowed(
            self, customer_base_bus_obj, customer):
        """
        Test case for the is_email_allowed property.
        """
        customer.is_email_allowed = True
        assert customer_base_bus_obj.is_email_allowed is True

    def test_is_email_allowed_setter(
            self, customer_base_bus_obj):
        """
        Test case for the is_email_allowed setter.
        """
        customer_base_bus_obj.is_email_allowed = True
        assert customer_base_bus_obj.is_email_allowed is True

    def test_is_email_allowed_invalid_value(
            self, customer_base_bus_obj):
        """
        Test case for setting an invalid value for the
        is_email_allowed property.
        """
        with pytest.raises(ValueError):
            customer_base_bus_obj.is_email_allowed = "not-a-boolean"
    # isEmailConfirmed

    def test_is_email_confirmed(
            self, customer_base_bus_obj, customer):
        """
        Test case for the is_email_confirmed property.
        """
        customer.is_email_confirmed = True
        assert customer_base_bus_obj.is_email_confirmed is True

    def test_is_email_confirmed_setter(
            self, customer_base_bus_obj):
        """
        Test case for the is_email_confirmed setter.
        """
        customer_base_bus_obj.is_email_confirmed = True
        assert customer_base_bus_obj.is_email_confirmed is True

    def test_is_email_confirmed_invalid_value(
            self, customer_base_bus_obj):
        """
        Test case for setting an invalid value for the
        is_email_confirmed property.
        """
        with pytest.raises(ValueError):
            customer_base_bus_obj.is_email_confirmed = "not-a-boolean"
    # isEmailMarketingAllowed

    def test_is_email_marketing_allowed(
            self, customer_base_bus_obj, customer):
        """
        Test case for the is_email_marketing_allowed property.
        """
        customer.is_email_marketing_allowed = True
        assert customer_base_bus_obj.is_email_marketing_allowed is True

    def test_is_email_marketing_allowed_setter(
            self, customer_base_bus_obj):
        """
        Test case for the is_email_marketing_allowed setter.
        """
        customer_base_bus_obj.is_email_marketing_allowed = True
        assert customer_base_bus_obj.is_email_marketing_allowed is True

    def test_is_email_marketing_allowed_invalid_value(
            self, customer_base_bus_obj):
        """
        Test case for setting an invalid value for the
        is_email_marketing_allowed property.
        """
        with pytest.raises(ValueError):
            customer_base_bus_obj.is_email_marketing_allowed = "not-a-boolean"
    # isLocked

    def test_is_locked(
            self, customer_base_bus_obj, customer):
        """
        Test case for the is_locked property.
        """
        customer.is_locked = True
        assert customer_base_bus_obj.is_locked is True

    def test_is_locked_setter(
            self, customer_base_bus_obj):
        """
        Test case for the is_locked setter.
        """
        customer_base_bus_obj.is_locked = True
        assert customer_base_bus_obj.is_locked is True

    def test_is_locked_invalid_value(
            self, customer_base_bus_obj):
        """
        Test case for setting an invalid value for the
        is_locked property.
        """
        with pytest.raises(ValueError):
            customer_base_bus_obj.is_locked = "not-a-boolean"
    # isMultipleOrganizationsAllowed

    def test_is_multiple_organizations_allowed(
            self, customer_base_bus_obj, customer):
        """
        Test case for the is_multiple_organizations_allowed property.
        """
        customer.is_multiple_organizations_allowed = True
        assert customer_base_bus_obj.is_multiple_organizations_allowed is True

    def test_is_multiple_organizations_allowed_setter(
            self, customer_base_bus_obj):
        """
        Test case for the is_multiple_organizations_allowed setter.
        """
        customer_base_bus_obj.is_multiple_organizations_allowed = True
        assert customer_base_bus_obj.is_multiple_organizations_allowed is True

    def test_is_multiple_organizations_allowed_invalid_value(
            self, customer_base_bus_obj):
        """
        Test case for setting an invalid value for the
        is_multiple_organizations_allowed property.
        """
        with pytest.raises(ValueError):
            customer_base_bus_obj.is_multiple_organizations_allowed = "not-a-boolean"
    # isVerboseLoggingForced

    def test_is_verbose_logging_forced(
            self, customer_base_bus_obj, customer):
        """
        Test case for the is_verbose_logging_forced property.
        """
        customer.is_verbose_logging_forced = True
        assert customer_base_bus_obj.is_verbose_logging_forced is True

    def test_is_verbose_logging_forced_setter(
            self, customer_base_bus_obj):
        """
        Test case for the is_verbose_logging_forced setter.
        """
        customer_base_bus_obj.is_verbose_logging_forced = True
        assert customer_base_bus_obj.is_verbose_logging_forced is True

    def test_is_verbose_logging_forced_invalid_value(
            self, customer_base_bus_obj):
        """
        Test case for setting an invalid value for the
        is_verbose_logging_forced property.
        """
        with pytest.raises(ValueError):
            customer_base_bus_obj.is_verbose_logging_forced = "not-a-boolean"
    # lastLoginUTCDateTime

    def test_last_login_utc_date_time(
            self, customer_base_bus_obj, customer):
        """
        Test case for the last_login_utc_date_time property.
        """
        test_datetime = datetime.utcnow()
        customer.last_login_utc_date_time = test_datetime
        assert customer_base_bus_obj.last_login_utc_date_time == test_datetime

    def test_last_login_utc_date_time_setter(
            self, customer_base_bus_obj):
        """
        Test case for the last_login_utc_date_time setter.
        """
        test_datetime = datetime.utcnow()
        customer_base_bus_obj.last_login_utc_date_time = test_datetime
        assert customer_base_bus_obj.last_login_utc_date_time == test_datetime

    def test_last_login_utc_date_time_invalid_value(
            self, customer_base_bus_obj):
        """
        Test case for setting an invalid value for the
        last_login_utc_date_time property.
        """
        with pytest.raises(AssertionError):
            customer_base_bus_obj.last_login_utc_date_time = "not-a-datetime"
    # lastName

    def test_last_name(
            self, customer_base_bus_obj, customer):
        """
        Test case for the last_name property.
        """
        customer.last_name = "Vanilla"
        assert customer_base_bus_obj.last_name == "Vanilla"

    def test_last_name_setter(
            self, customer_base_bus_obj):
        """
        Test case for the last_name setter.
        """
        customer_base_bus_obj.last_name = "Vanilla"
        assert customer_base_bus_obj.last_name == "Vanilla"

    def test_last_name_invalid_value(
            self, customer_base_bus_obj):
        """
        Test case for setting an invalid value for the
        last_name property.
        """
        with pytest.raises(AssertionError):
            customer_base_bus_obj.last_name = 123
    # password

    def test_password(
            self, customer_base_bus_obj, customer):
        """
        Test case for the password property.
        """
        customer.password = "Vanilla"
        assert customer_base_bus_obj.password == "Vanilla"

    def test_password_setter(
            self, customer_base_bus_obj):
        """
        Test case for the password setter.
        """
        customer_base_bus_obj.password = "Vanilla"
        assert customer_base_bus_obj.password == "Vanilla"

    def test_password_invalid_value(
            self, customer_base_bus_obj):
        """
        Test case for setting an invalid value for the
        password property.
        """
        with pytest.raises(AssertionError):
            customer_base_bus_obj.password = 123
    # phone

    def test_phone(
            self, customer_base_bus_obj, customer):
        """
        Test case for the phone property.
        """
        customer.phone = "123-456-7890"
        assert customer_base_bus_obj.phone == "123-456-7890"

    def test_phone_setter(
            self, customer_base_bus_obj):
        """
        Test case for the phone setter.
        """
        customer_base_bus_obj.phone = "123-456-7890"
        assert customer_base_bus_obj.phone == "123-456-7890"

    def test_phone_invalid_value(
            self, customer_base_bus_obj):
        """
        Test case for setting an invalid value for the
        phone property.
        """
        with pytest.raises(AssertionError):
            customer_base_bus_obj.phone = 123
    # province

    def test_province(
            self, customer_base_bus_obj, customer):
        """
        Test case for the province property.
        """
        customer.province = "Vanilla"
        assert customer_base_bus_obj.province == "Vanilla"

    def test_province_setter(
            self, customer_base_bus_obj):
        """
        Test case for the province setter.
        """
        customer_base_bus_obj.province = "Vanilla"
        assert customer_base_bus_obj.province == "Vanilla"

    def test_province_invalid_value(
            self, customer_base_bus_obj):
        """
        Test case for setting an invalid value for the
        province property.
        """
        with pytest.raises(AssertionError):
            customer_base_bus_obj.province = 123
    # registrationUTCDateTime

    def test_registration_utc_date_time(
            self, customer_base_bus_obj, customer):
        """
        Test case for the registration_utc_date_time property.
        """
        test_datetime = datetime.utcnow()
        customer.registration_utc_date_time = test_datetime
        assert customer_base_bus_obj.registration_utc_date_time == test_datetime

    def test_registration_utc_date_time_setter(
            self, customer_base_bus_obj):
        """
        Test case for the registration_utc_date_time setter.
        """
        test_datetime = datetime.utcnow()
        customer_base_bus_obj.registration_utc_date_time = test_datetime
        assert customer_base_bus_obj.registration_utc_date_time == test_datetime

    def test_registration_utc_date_time_invalid_value(
            self, customer_base_bus_obj):
        """
        Test case for setting an invalid value for the
        registration_utc_date_time property.
        """
        with pytest.raises(AssertionError):
            customer_base_bus_obj.registration_utc_date_time = "not-a-datetime"
    # TacID
    # uTCOffsetInMinutes

    def test_utc_offset_in_minutes(
            self, customer_base_bus_obj, customer):
        """
        Test case for the utc_offset_in_minutes property.
        """
        customer.utc_offset_in_minutes = 1
        assert customer_base_bus_obj.utc_offset_in_minutes == 1

    def test_utc_offset_in_minutes_setter(
            self, customer_base_bus_obj):
        """
        Test case for the utc_offset_in_minutes setter.
        """
        customer_base_bus_obj.utc_offset_in_minutes = 1
        assert customer_base_bus_obj.utc_offset_in_minutes == 1

    def test_utc_offset_in_minutes_invalid_value(self, customer_base_bus_obj):
        """
        Test case for setting an invalid value for the
        utc_offset_in_minutes property.
        """
        with pytest.raises(AssertionError):
            customer_base_bus_obj.utc_offset_in_minutes = "not-an-int"
    # zip

    def test_zip(
            self, customer_base_bus_obj, customer):
        """
        Test case for the zip property.
        """
        customer.zip = "Vanilla"
        assert customer_base_bus_obj.zip == "Vanilla"

    def test_zip_setter(
            self, customer_base_bus_obj):
        """
        Test case for the zip setter.
        """
        customer_base_bus_obj.zip = "Vanilla"
        assert customer_base_bus_obj.zip == "Vanilla"

    def test_zip_invalid_value(
            self, customer_base_bus_obj):
        """
        Test case for setting an invalid value for the
        zip property.
        """
        with pytest.raises(AssertionError):
            customer_base_bus_obj.zip = 123
    # activeOrganizationID,
    # email,
    # emailConfirmedUTCDateTime
    # firstName,
    # forgotPasswordKeyExpirationUTCDateTime
    # forgotPasswordKeyValue,
    # fSUserCodeValue,
    # isActive,
    # isEmailAllowed,
    # isEmailConfirmed,
    # isEmailMarketingAllowed,
    # isLocked,
    # isMultipleOrganizationsAllowed,
    # isVerboseLoggingForced,
    # lastLoginUTCDateTime
    # lastName,
    # password,
    # phone,
    # province,
    # registrationUTCDateTime
    # TacID

    def test_tac_id(
            self, customer_base_bus_obj, customer):
        """
        Test case for the tac_id property.
        """
        customer.tac_id = 1
        assert customer_base_bus_obj.tac_id == 1

    def test_tac_id_setter(
            self, customer_base_bus_obj):
        """
        Test case for the tac_id setter.
        """
        customer_base_bus_obj.tac_id = 1
        assert customer_base_bus_obj.tac_id == 1

    def test_tac_id_invalid_value(
            self, customer_base_bus_obj):
        """
        Test case for setting an invalid value for the
        tac_id property.
        """
        with pytest.raises(AssertionError):
            customer_base_bus_obj.tac_id = "not-an-int"
    # uTCOffsetInMinutes,
    # zip,

    def test_insert_utc_date_time(
            self,
            customer_base_bus_obj,
            customer):
        """
        Test case for the insert_utc_date_time property.
        """
        test_datetime = datetime.utcnow()
        customer.insert_utc_date_time = test_datetime
        assert customer_base_bus_obj.insert_utc_date_time == test_datetime

    def test_insert_utc_date_time_setter(
            self, customer_base_bus_obj):
        """
        Test case for the insert_utc_date_time setter.
        """
        test_datetime = datetime.utcnow()
        customer_base_bus_obj.insert_utc_date_time = test_datetime
        assert customer_base_bus_obj.insert_utc_date_time == test_datetime

    def test_insert_utc_date_time_invalid_value(
            self, customer_base_bus_obj):
        """
        Test case for setting an invalid value for the
        insert_utc_date_time property.
        """
        with pytest.raises(AssertionError):
            customer_base_bus_obj.insert_utc_date_time = "not-a-datetime"

    def test_last_update_utc_date_time(
            self,
            customer_base_bus_obj,
            customer):
        """
        Test case for the last_update_utc_date_time property.
        """
        test_datetime = datetime.utcnow()
        customer.last_update_utc_date_time = test_datetime
        assert customer_base_bus_obj.last_update_utc_date_time == test_datetime

    def test_last_update_utc_date_time_setter(
            self, customer_base_bus_obj):
        """
        Test case for the last_update_utc_date_time setter.
        """
        test_datetime = datetime.utcnow()
        customer_base_bus_obj.last_update_utc_date_time = test_datetime
        assert customer_base_bus_obj.last_update_utc_date_time == test_datetime

    def test_last_update_utc_date_time_invalid_value(
            self, customer_base_bus_obj):
        """
        Test case for setting an invalid value for the
        last_update_utc_date_time property.
        """
        with pytest.raises(AssertionError):
            customer_base_bus_obj.last_update_utc_date_time = "not-a-datetime"


    @pytest.mark.asyncio
    async def test_build_customer_role(
        self,
        customer_bus_obj: CustomerBusObj,
        new_customer: Customer,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """

        session_context = SessionContext(dict(), session)

        await current_runtime.initialize(session_context)

        await customer_bus_obj.load_from_id(
            new_customer.customer_id
        )

        customer_role_bus_obj = await customer_bus_obj.build_customer_role()

        assert customer_role_bus_obj.customer_id == customer_bus_obj.customer_id
        assert customer_role_bus_obj.customer_code_peek == customer_bus_obj.code

        await customer_role_bus_obj.save()

        assert customer_role_bus_obj.customer_role_id > 0

    @pytest.mark.asyncio
    async def test_get_all_customer_role(
        self,
        customer_bus_obj: CustomerBusObj,
        new_customer: Customer,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """

        session_context = SessionContext(dict(), session)

        await current_runtime.initialize(session_context)

        new_customer_customer_id = (
            new_customer.customer_id
        )

        await customer_bus_obj.load_from_id(
            new_customer_customer_id
        )

        customer_role_bus_obj = await customer_bus_obj.build_customer_role()

        await customer_role_bus_obj.save()

        customer_role_list = await customer_bus_obj.get_all_customer_role()

        assert len(customer_role_list) >= 1

        #assert customer_role_list[0].customer_role_id > 0

        #assert customer_role_list[0].customer_role_id == customer_role_bus_obj.customer_role_id

