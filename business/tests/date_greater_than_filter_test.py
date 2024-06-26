# business/tests/date_greater_than_filter_test.py
# pylint: disable=redefined-outer-name
# pylint: disable=unused-import
"""
Unit tests for the
DateGreaterThanFilterBusObj class.
"""

from unittest.mock import AsyncMock, Mock, patch

import pytest

from business.date_greater_than_filter import (
    DateGreaterThanFilterBusObj)
from helpers.session_context import SessionContext
from models import (
    DateGreaterThanFilter)


@pytest.fixture
def session_context():
    """
    Return a mock SessionContext object.
    """
    return Mock(spec=SessionContext)


@pytest.fixture
def obj_list():
    """
    Return a list of mock DateGreaterThanFilter objects.
    """
    date_greater_than_filters = []
    for _ in range(3):
        date_greater_than_filter = Mock(spec=DateGreaterThanFilter)
        date_greater_than_filters.append(date_greater_than_filter)
    return date_greater_than_filters


@pytest.mark.asyncio
async def test_to_bus_obj_list(
        session_context, obj_list):
    """
    Test the to_bus_obj_list method.
    """
    with patch("business.date_greater_than_filter"
               ".DateGreaterThanFilterBusObj"
               ".load_from_obj_instance",
               new_callable=AsyncMock) as mock_load:
        bus_obj_list = await \
            DateGreaterThanFilterBusObj.to_bus_obj_list(
                session_context, obj_list)

        assert len(bus_obj_list) == len(obj_list)
        assert all(
            isinstance(bus_obj, DateGreaterThanFilterBusObj)
            for bus_obj in bus_obj_list)
        assert all(
            bus_obj.load_from_obj_instance.called
            for bus_obj in bus_obj_list)

        for bus_obj, date_greater_than_filter in zip(bus_obj_list, obj_list):
            mock_load.assert_any_call(date_greater_than_filter)


@pytest.mark.asyncio
async def test_to_bus_obj_list_empty(
        session_context):
    """
    Test the to_bus_obj_list
    method with an empty list.
    """
    empty_obj_list = []
    bus_obj_list = await \
        DateGreaterThanFilterBusObj.to_bus_obj_list(
            session_context,
            empty_obj_list)

    assert len(bus_obj_list) == 0
