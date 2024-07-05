# business/tests/org_customer_test.py
# pylint: disable=redefined-outer-name
# pylint: disable=unused-import
"""
Unit tests for the
OrgCustomerBusObj class.
"""

from unittest.mock import AsyncMock, Mock, patch

import pytest
import pytest_asyncio

import models
from models.factory import (
    OrgCustomerFactory)
from business.org_customer import (
    OrgCustomerBusObj)
from helpers.session_context import SessionContext
from models import (
    OrgCustomer)


@pytest.fixture
def session_context():
    """
    Return a mock SessionContext object.
    """
    return Mock(spec=SessionContext)


@pytest.fixture
def org_customer():
    """
    Fixture that returns a mock
    org_customer object.
    """
    return Mock(spec=OrgCustomer)


@pytest.fixture
def obj_list():
    """
    Return a list of mock OrgCustomer objects.
    """
    org_customers = []
    for _ in range(3):
        org_customer = Mock(spec=OrgCustomer)
        org_customers.append(org_customer)
    return org_customers


@pytest_asyncio.fixture(scope="function")
async def new_obj(session):
    """
    Fixture that returns a new instance of
    the OrgCustomer class.
    """

    return await OrgCustomerFactory.create_async(
        session)


@pytest_asyncio.fixture(scope="function")
async def new_bus_obj(session, new_obj) -> OrgCustomerBusObj:
    """
    Fixture that returns a new instance of
    the OrgCustomer class.
    """

    session_context = SessionContext({}, session)
    org_customer_bus_obj = OrgCustomerBusObj(session_context, new_obj)

    return org_customer_bus_obj


class TestOrgCustomerBusObj:
    """
    Unit tests for the
    OrgCustomerBusObj class.
    """

    @pytest.mark.asyncio
    async def test_to_bus_obj_list(
            self, session_context, obj_list):
        """
        Test the to_bus_obj_list method.
        """
        with patch(
                "business.org_customer"
                ".OrgCustomerBusObj"
                ".load_from_obj_instance",
                new_callable=AsyncMock) as mock_load:
            bus_obj_list = await \
                OrgCustomerBusObj.to_bus_obj_list(
                    session_context, obj_list)

            assert len(bus_obj_list) == len(obj_list)
            assert all(
                isinstance(bus_obj, OrgCustomerBusObj)
                for bus_obj in bus_obj_list)
            assert all(
                bus_obj.load_from_obj_instance.called
                for bus_obj in bus_obj_list)

            for bus_obj, org_customer in zip(bus_obj_list, obj_list):
                mock_load.assert_any_call(org_customer)

    @pytest.mark.asyncio
    async def test_to_bus_obj_list_empty(
            self, session_context):
        """
        Test the to_bus_obj_list
        method with an empty list.
        """
        empty_obj_list = []
        bus_obj_list = await \
            OrgCustomerBusObj.to_bus_obj_list(
                session_context,
                empty_obj_list)

        assert len(bus_obj_list) == 0
    # CustomerID

    @pytest.mark.asyncio
    async def test_get_customer_id_obj(
        self, new_bus_obj: OrgCustomerBusObj
    ):
        """
        Test the get_customer_id_obj method.
        """

        # Call the get_customer_id_obj method
        fk_obj: models.Customer = \
            await new_bus_obj.get_customer_id_obj()

        assert fk_obj is not None

        assert isinstance(fk_obj, models.Customer)

        assert fk_obj.customer_id == \
            new_bus_obj.customer_id

        assert fk_obj.code == \
            new_bus_obj.customer_code_peek

    @pytest.mark.asyncio
    async def test_get_customer_id_bus_obj(
        self, new_bus_obj: OrgCustomerBusObj
    ):
        """
        Test the get_customer_id_bus_obj
        method.
        """

        from business.customer import (  # CustomerID
            CustomerBusObj)
        # Call the get_customer_id_bus_obj method
        fk_bus_obj: CustomerBusObj = \
            await new_bus_obj.get_customer_id_bus_obj()

        assert fk_bus_obj is not None

        assert isinstance(fk_bus_obj, CustomerBusObj)

        assert fk_bus_obj.customer_id == \
            new_bus_obj.customer_id

        assert fk_bus_obj.code == \
            new_bus_obj.customer_code_peek
    # email,
    # OrganizationID

    @pytest.mark.asyncio
    async def test_get_organization_id_obj(
        self, new_bus_obj: OrgCustomerBusObj
    ):
        """
        Test the get_organization_id_obj method.
        """

        # Call the get_organization_id_bus_obj method
        fk_obj: models.Organization = await \
            new_bus_obj.get_organization_id_obj()

        assert fk_obj is not None

        assert isinstance(fk_obj, models.Organization)

        assert fk_obj.organization_id == \
            new_bus_obj.organization_id

        assert fk_obj.code == \
            new_bus_obj.organization_code_peek

    @pytest.mark.asyncio
    async def test_get_organization_id_bus_obj(
        self, new_bus_obj: OrgCustomerBusObj
    ):
        """
        Test the get_organization_id_bus_obj method.
        """
        from business.organization import (  # OrganizationID
            OrganizationBusObj)
        # Call the get_organization_id_bus_obj method
        fk_bus_obj: OrganizationBusObj = await \
            new_bus_obj.get_organization_id_bus_obj()

        assert fk_bus_obj is not None

        assert isinstance(fk_bus_obj, OrganizationBusObj)

        assert fk_bus_obj.organization_id == \
            new_bus_obj.organization_id

        assert fk_bus_obj.code == \
            new_bus_obj.organization_code_peek
