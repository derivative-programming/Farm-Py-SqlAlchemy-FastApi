# business/tests/customer_test.py
"""
Unit tests for the CustomerBusObj class.
"""
from typing import List
from unittest.mock import AsyncMock, Mock, patch

import pytest

from business.customer import CustomerBusObj
from helpers.session_context import SessionContext
from models import Customer

@pytest.fixture
def session_context():
    """
    Return a mock SessionContext object.
    """
    return Mock(spec=SessionContext)

@pytest.fixture
def customer_list():
    """
    Return a list of mock Customer objects.
    """
    customers = []
    for _ in range(3):
        customer = Mock(spec=Customer)
        customers.append(customer)
    return customers

@pytest.mark.asyncio
async def test_to_bus_obj_list(session_context, customer_list):
    """
    Test the to_bus_obj_list method.
    """
    with patch('business.customer.CustomerBusObj.load_from_obj_instance',
               new_callable=AsyncMock) as mock_load:
        bus_obj_list = await CustomerBusObj.to_bus_obj_list(
            session_context, customer_list)

        assert len(bus_obj_list) == len(customer_list)
        assert all(
            isinstance(bus_obj, CustomerBusObj) for bus_obj in bus_obj_list)
        assert all(
            bus_obj.load_from_obj_instance.called for bus_obj in bus_obj_list)

        for bus_obj, customer in zip(bus_obj_list, customer_list):
            mock_load.assert_any_call(customer)

@pytest.mark.asyncio
async def test_to_bus_obj_list_empty(session_context):
    """
    Test the to_bus_obj_list method with an empty list.
    """
    empty_customer_list = []
    bus_obj_list = await CustomerBusObj.to_bus_obj_list(session_context, empty_customer_list)

    assert len(bus_obj_list) == 0
