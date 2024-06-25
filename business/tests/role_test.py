# business/tests/role_test.py
# pylint: disable=redefined-outer-name
# pylint: disable=unused-import
"""
Unit tests for the
RoleBusObj class.
"""

from unittest.mock import AsyncMock, Mock, patch

import pytest

from business.role import (
    RoleBusObj)
from helpers.session_context import SessionContext
from models import (
    Role)


@pytest.fixture
def session_context():
    """
    Return a mock SessionContext object.
    """
    return Mock(spec=SessionContext)


@pytest.fixture
def role_list():
    """
    Return a list of mock Role objects.
    """
    roles = []
    for _ in range(3):
        role = Mock(spec=Role)
        roles.append(role)
    return roles


@pytest.mark.asyncio
async def test_to_bus_obj_list(
        session_context, role_list):
    """
    Test the to_bus_obj_list method.
    """
    with patch('business.role.RoleBusObj.load_from_obj_instance',
               new_callable=AsyncMock) as mock_load:
        bus_obj_list = await \
            RoleBusObj.to_bus_obj_list(
                session_context, role_list)

        assert len(bus_obj_list) == len(role_list)
        assert all(
            isinstance(bus_obj, RoleBusObj) for bus_obj in bus_obj_list)
        assert all(
            bus_obj.load_from_obj_instance.called for bus_obj in bus_obj_list)

        for bus_obj, role in zip(bus_obj_list, role_list):
            mock_load.assert_any_call(role)


@pytest.mark.asyncio
async def test_to_bus_obj_list_empty(
        session_context):
    """
    Test the to_bus_obj_list
    method with an empty list.
    """
    empty_role_list = []
    bus_obj_list = await \
        RoleBusObj.to_bus_obj_list(
            session_context,
            empty_role_list)

    assert len(bus_obj_list) == 0

