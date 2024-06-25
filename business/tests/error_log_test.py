# business/tests/error_log_test.py
# pylint: disable=redefined-outer-name
# pylint: disable=unused-import
"""
Unit tests for the
ErrorLogBusObj class.
"""

from unittest.mock import AsyncMock, Mock, patch

import pytest

from business.error_log import (
    ErrorLogBusObj)
from helpers.session_context import SessionContext
from models import (
    ErrorLog)


@pytest.fixture
def session_context():
    """
    Return a mock SessionContext object.
    """
    return Mock(spec=SessionContext)


@pytest.fixture
def error_log_list():
    """
    Return a list of mock ErrorLog objects.
    """
    error_logs = []
    for _ in range(3):
        error_log = Mock(spec=ErrorLog)
        error_logs.append(error_log)
    return error_logs


@pytest.mark.asyncio
async def test_to_bus_obj_list(
        session_context, error_log_list):
    """
    Test the to_bus_obj_list method.
    """
    with patch('business.error_log.ErrorLogBusObj.load_from_obj_instance',
               new_callable=AsyncMock) as mock_load:
        bus_obj_list = await \
            ErrorLogBusObj.to_bus_obj_list(
                session_context, error_log_list)

        assert len(bus_obj_list) == len(error_log_list)
        assert all(
            isinstance(bus_obj, ErrorLogBusObj) for bus_obj in bus_obj_list)
        assert all(
            bus_obj.load_from_obj_instance.called for bus_obj in bus_obj_list)

        for bus_obj, error_log in zip(bus_obj_list, error_log_list):
            mock_load.assert_any_call(error_log)


@pytest.mark.asyncio
async def test_to_bus_obj_list_empty(
        session_context):
    """
    Test the to_bus_obj_list
    method with an empty list.
    """
    empty_error_log_list = []
    bus_obj_list = await \
        ErrorLogBusObj.to_bus_obj_list(
            session_context,
            empty_error_log_list)

    assert len(bus_obj_list) == 0

