# business/tests/org_customer_test.py
# pylint: disable=redefined-outer-name
# pylint: disable=unused-import
"""
Unit tests for the
OrgCustomerBusObj class.
"""

from unittest.mock import AsyncMock, Mock, patch

import pytest

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
def org_customer_list():
    """
    Return a list of mock OrgCustomer objects.
    """
    org_customers = []
    for _ in range(3):
        org_customer = Mock(spec=OrgCustomer)
        org_customers.append(org_customer)
    return org_customers


@pytest.mark.asyncio
async def test_to_bus_obj_list(
        session_context, org_customer_list):
    """
    Test the to_bus_obj_list method.
    """
    with patch('business.org_customer.OrgCustomerBusObj.load_from_obj_instance',
               new_callable=AsyncMock) as mock_load:
        bus_obj_list = await \
            OrgCustomerBusObj.to_bus_obj_list(
                session_context, org_customer_list)

        assert len(bus_obj_list) == len(org_customer_list)
        assert all(
            isinstance(bus_obj, OrgCustomerBusObj) for bus_obj in bus_obj_list)
        assert all(
            bus_obj.load_from_obj_instance.called for bus_obj in bus_obj_list)

        for bus_obj, org_customer in zip(bus_obj_list, org_customer_list):
            mock_load.assert_any_call(org_customer)


@pytest.mark.asyncio
async def test_to_bus_obj_list_empty(
        session_context):
    """
    Test the to_bus_obj_list
    method with an empty list.
    """
    empty_org_customer_list = []
    bus_obj_list = await \
        OrgCustomerBusObj.to_bus_obj_list(
            session_context,
            empty_org_customer_list)

    assert len(bus_obj_list) == 0

