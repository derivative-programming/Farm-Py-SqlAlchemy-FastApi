# business/tests/customer_role_test.py  # pylint: disable=duplicate-code
# pylint: disable=redefined-outer-name, too-many-public-methods
# pylint: disable=unused-import
# pylint: disable=too-few-public-methods
# pylint: disable=import-outside-toplevel
# pylint: disable=too-many-lines
"""
Unit tests for the
CustomerRoleBusObj class.
"""

from unittest.mock import AsyncMock, Mock, patch

import pytest_asyncio

import models
import pytest
from business.customer_role import CustomerRoleBusObj
from helpers.session_context import SessionContext
from models import CustomerRole
from models.factory import CustomerRoleFactory


@pytest.fixture
def session_context():
    """
    Return a mock SessionContext object.
    """
    return Mock(spec=SessionContext)


@pytest.fixture
def customer_role():
    """
    Fixture that returns a mock
    customer_role object.
    """
    return Mock(spec=CustomerRole)


@pytest.fixture
def obj_list():
    """
    Return a list of mock CustomerRole objects.
    """
    customer_roles = []
    for _ in range(3):
        customer_role = Mock(spec=CustomerRole)
        customer_roles.append(customer_role)
    return customer_roles


@pytest_asyncio.fixture(scope="function")
async def new_obj(session):
    """
    Fixture that returns a new instance of
    the CustomerRole class.
    """

    return await CustomerRoleFactory.create_async(
        session)


@pytest_asyncio.fixture(scope="function")
async def new_bus_obj(session, new_obj) -> CustomerRoleBusObj:
    """
    Fixture that returns a new instance of
    the CustomerRole class.
    """

    session_context = SessionContext({}, session)
    customer_role_bus_obj = CustomerRoleBusObj(
        session_context, new_obj)

    return customer_role_bus_obj


class TestCustomerRoleBusObj:
    """
    Unit tests for the
    CustomerRoleBusObj class.
    """

    @pytest.mark.asyncio
    async def test_to_bus_obj_list(
            self, session_context, obj_list):
        """
        Test the to_bus_obj_list method.
        """
        with patch(
                "business.customer_role"
                ".CustomerRoleBusObj"
                ".load_from_obj_instance",
                new_callable=AsyncMock) as mock_load:
            bus_obj_list = await \
                CustomerRoleBusObj.to_bus_obj_list(
                    session_context, obj_list)

            assert len(bus_obj_list) == len(obj_list)
            assert all(
                isinstance(bus_obj, CustomerRoleBusObj)
                for bus_obj in bus_obj_list)
            assert all(
                bus_obj.load_from_obj_instance.called
                for bus_obj in bus_obj_list)

            for bus_obj, customer_role in \
                    zip(bus_obj_list, obj_list):
                mock_load.assert_any_call(customer_role)

    @pytest.mark.asyncio
    async def test_to_bus_obj_list_empty(
            self, session_context):
        """
        Test the to_bus_obj_list
        method with an empty list.
        """
        empty_obj_list = []
        bus_obj_list = await \
            CustomerRoleBusObj.to_bus_obj_list(
                session_context,
                empty_obj_list)

        assert len(bus_obj_list) == 0
    # CustomerID

    @pytest.mark.asyncio
    async def test_get_customer_id_obj(
        self, new_bus_obj: CustomerRoleBusObj
    ):
        """
        Test the get_customer_id_obj method.
        """

        # Call the get_customer_id_bus_obj method
        fk_obj: models.Customer = await \
            new_bus_obj.get_customer_id_obj()

        assert fk_obj is not None

        assert isinstance(fk_obj, models.Customer)

        assert fk_obj.customer_id == \
            new_bus_obj.customer_id

        assert fk_obj.code == \
            new_bus_obj.customer_code_peek

    @pytest.mark.asyncio
    async def test_get_customer_id_bus_obj(
        self, new_bus_obj: CustomerRoleBusObj
    ):
        """
        Test the get_customer_id_bus_obj method.
        """
        from business.customer import CustomerBusObj  # CustomerID

        # Call the get_customer_id_bus_obj method
        fk_bus_obj: CustomerBusObj = await \
            new_bus_obj.get_customer_id_bus_obj()

        assert fk_bus_obj is not None

        assert isinstance(fk_bus_obj, CustomerBusObj)

        assert fk_bus_obj.customer_id == \
            new_bus_obj.customer_id

        assert fk_bus_obj.code == \
            new_bus_obj.customer_code_peek
    # isPlaceholder
    # placeholder
    # RoleID

    @pytest.mark.asyncio
    async def test_get_role_id_obj(
        self, new_bus_obj: CustomerRoleBusObj
    ):
        """
        Test the get_role_id_obj method.
        """

        # Call the get_role_id_obj method
        fk_obj: models.Role = \
            await new_bus_obj.get_role_id_obj()

        assert fk_obj is not None

        assert isinstance(fk_obj, models.Role)

        assert fk_obj.role_id == \
            new_bus_obj.role_id

        assert fk_obj.code == \
            new_bus_obj.role_code_peek

    @pytest.mark.asyncio
    async def test_get_role_id_bus_obj(
        self, new_bus_obj: CustomerRoleBusObj
    ):
        """
        Test the get_role_id_bus_obj
        method.
        """

        from business.role import RoleBusObj  # RoleID

        # Call the get_role_id_bus_obj method
        fk_bus_obj: RoleBusObj = \
            await new_bus_obj.get_role_id_bus_obj()

        assert fk_bus_obj is not None

        assert isinstance(fk_bus_obj, RoleBusObj)

        assert fk_bus_obj.role_id == \
            new_bus_obj.role_id

        assert fk_bus_obj.code == \
            new_bus_obj.role_code_peek
