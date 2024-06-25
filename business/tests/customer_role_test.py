# business/tests/customer_role_test.py
# pylint: disable=redefined-outer-name
# pylint: disable=unused-import
"""
Unit tests for the
CustomerRoleBusObj class.
"""

from unittest.mock import AsyncMock, Mock, patch

import pytest

from business.customer_role import (
    CustomerRoleBusObj)
from helpers.session_context import SessionContext
from models import (
    CustomerRole)


@pytest.fixture
def session_context():
    """
    Return a mock SessionContext object.
    """
    return Mock(spec=SessionContext)


@pytest.fixture
def customer_role_list():
    """
    Return a list of mock CustomerRole objects.
    """
    customer_roles = []
    for _ in range(3):
        customer_role = Mock(spec=CustomerRole)
        customer_roles.append(customer_role)
    return customer_roles


@pytest.mark.asyncio
async def test_to_bus_obj_list(
        session_context, customer_role_list):
    """
    Test the to_bus_obj_list method.
    """
    with patch('business.customer_role.CustomerRoleBusObj.load_from_obj_instance',
               new_callable=AsyncMock) as mock_load:
        bus_obj_list = await \
            CustomerRoleBusObj.to_bus_obj_list(
                session_context, customer_role_list)

        assert len(bus_obj_list) == len(customer_role_list)
        assert all(
            isinstance(bus_obj, CustomerRoleBusObj) for bus_obj in bus_obj_list)
        assert all(
            bus_obj.load_from_obj_instance.called for bus_obj in bus_obj_list)

        for bus_obj, customer_role in zip(bus_obj_list, customer_role_list):
            mock_load.assert_any_call(customer_role)


@pytest.mark.asyncio
async def test_to_bus_obj_list_empty(
        session_context):
    """
    Test the to_bus_obj_list
    method with an empty list.
    """
    empty_customer_role_list = []
    bus_obj_list = await \
        CustomerRoleBusObj.to_bus_obj_list(
            session_context,
            empty_customer_role_list)

    assert len(bus_obj_list) == 0

