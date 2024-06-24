# business/tests/tri_state_filter_test.py
"""
Unit tests for the TriStateFilterBusObj class.
"""
from typing import List
from unittest.mock import AsyncMock, Mock, patch

import pytest

from business.tri_state_filter import TriStateFilterBusObj
from helpers.session_context import SessionContext
from models import TriStateFilter

@pytest.fixture
def session_context():
    """
    Return a mock SessionContext object.
    """
    return Mock(spec=SessionContext)

@pytest.fixture
def tri_state_filter_list():
    """
    Return a list of mock TriStateFilter objects.
    """
    tri_state_filters = []
    for _ in range(3):
        tri_state_filter = Mock(spec=TriStateFilter)
        tri_state_filters.append(tri_state_filter)
    return tri_state_filters

@pytest.mark.asyncio
async def test_to_bus_obj_list(session_context, tri_state_filter_list):
    """
    Test the to_bus_obj_list method.
    """
    with patch('business.tri_state_filter.TriStateFilterBusObj.load_from_obj_instance',
               new_callable=AsyncMock) as mock_load:
        bus_obj_list = await TriStateFilterBusObj.to_bus_obj_list(
            session_context, tri_state_filter_list)

        assert len(bus_obj_list) == len(tri_state_filter_list)
        assert all(
            isinstance(bus_obj, TriStateFilterBusObj) for bus_obj in bus_obj_list)
        assert all(
            bus_obj.load_from_obj_instance.called for bus_obj in bus_obj_list)

        for bus_obj, tri_state_filter in zip(bus_obj_list, tri_state_filter_list):
            mock_load.assert_any_call(tri_state_filter)

@pytest.mark.asyncio
async def test_to_bus_obj_list_empty(session_context):
    """
    Test the to_bus_obj_list method with an empty list.
    """
    empty_tri_state_filter_list = []
    bus_obj_list = await TriStateFilterBusObj.to_bus_obj_list(session_context, empty_tri_state_filter_list)

    assert len(bus_obj_list) == 0
