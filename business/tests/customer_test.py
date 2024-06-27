# business/tests/customer_test.py
# pylint: disable=redefined-outer-name
# pylint: disable=unused-import
"""
Unit tests for the
CustomerBusObj class.
"""

from unittest.mock import AsyncMock, Mock, patch

import pytest
import pytest_asyncio

import models
from models.factory import (
    CustomerFactory)
from business.customer import (
    CustomerBusObj)
from helpers.session_context import SessionContext
from models import (
    Customer)


@pytest.fixture
def session_context():
    """
    Return a mock SessionContext object.
    """
    return Mock(spec=SessionContext)


@pytest.fixture
def customer():
    """
    Fixture that returns a mock
    customer object.
    """
    return Mock(spec=Customer)


@pytest.fixture
def obj_list():
    """
    Return a list of mock Customer objects.
    """
    customers = []
    for _ in range(3):
        customer = Mock(spec=Customer)
        customers.append(customer)
    return customers


@pytest_asyncio.fixture(scope="function")
async def new_obj(session):
    """
    Fixture that returns a new instance of
    the Customer class.
    """

    return await CustomerFactory.create_async(
        session)


@pytest_asyncio.fixture(scope="function")
async def new_bus_obj(session, new_obj) -> CustomerBusObj:
    """
    Fixture that returns a new instance of
    the Customer class.
    """

    session_context = SessionContext(dict(), session)
    customer_bus_obj = CustomerBusObj(session_context, new_obj)

    return customer_bus_obj


class TestCustomerBusObj:
    """
    Unit tests for the
    CustomerBusObj class.
    """

    @pytest.mark.asyncio
    async def test_to_bus_obj_list(
            self, session_context, obj_list):
        """
        Test the to_bus_obj_list method.
        """
        with patch(
                "business.customer"
                ".CustomerBusObj"
                ".load_from_obj_instance",
                new_callable=AsyncMock) as mock_load:
            bus_obj_list = await \
                CustomerBusObj.to_bus_obj_list(
                    session_context, obj_list)

            assert len(bus_obj_list) == len(obj_list)
            assert all(
                isinstance(bus_obj, CustomerBusObj)
                for bus_obj in bus_obj_list)
            assert all(
                bus_obj.load_from_obj_instance.called
                for bus_obj in bus_obj_list)

            for bus_obj, customer in zip(bus_obj_list, obj_list):
                mock_load.assert_any_call(customer)

    @pytest.mark.asyncio
    async def test_to_bus_obj_list_empty(
            self, session_context):
        """
        Test the to_bus_obj_list
        method with an empty list.
        """
        empty_obj_list = []
        bus_obj_list = await \
            CustomerBusObj.to_bus_obj_list(
                session_context,
                empty_obj_list)

        assert len(bus_obj_list) == 0
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

    @pytest.mark.asyncio
    async def test_get_tac_id_obj(
        self, new_bus_obj: CustomerBusObj
    ):
        """
        Test the get_tac_id_obj method.
        """

        # Call the get_tac_id_bus_obj method
        fk_obj: models.Tac = await \
            new_bus_obj.get_tac_id_obj()

        assert fk_obj is not None

        assert isinstance(fk_obj, models.Tac)

        assert fk_obj.tac_id == \
            new_bus_obj.tac_id

        assert fk_obj.code == \
            new_bus_obj.tac_code_peek

    @pytest.mark.asyncio
    async def test_get_tac_id_bus_obj(
        self, new_bus_obj: CustomerBusObj
    ):
        """
        Test the get_tac_id_bus_obj method.
        """
        from ..tac import (  # TacID
            TacBusObj)
        # Call the get_tac_id_bus_obj method
        fk_bus_obj: TacBusObj = await \
            new_bus_obj.get_tac_id_bus_obj()

        assert fk_bus_obj is not None

        assert isinstance(fk_bus_obj, TacBusObj)

        assert fk_bus_obj.tac_id == \
            new_bus_obj.tac_id

        assert fk_bus_obj.code == \
            new_bus_obj.tac_code_peek
    # uTCOffsetInMinutes,
    # zip,
