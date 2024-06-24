# business/tests/tac_test.py
# pylint: disable=redefined-outer-name
"""
Unit tests for the TacBusObj class.
"""

from unittest.mock import AsyncMock, Mock, patch

import pytest

from business.tac import TacBusObj
from helpers.session_context import SessionContext
from models import Tac

@pytest.fixture
def session_context():
    """
    Return a mock SessionContext object.
    """
    return Mock(spec=SessionContext)

@pytest.fixture
def tac_list():
    """
    Return a list of mock Tac objects.
    """
    tacs = []
    for _ in range(3):
        tac = Mock(spec=Tac)
        tacs.append(tac)
    return tacs

@pytest.mark.asyncio
async def test_to_bus_obj_list(session_context, tac_list):
    """
    Test the to_bus_obj_list method.
    """
    with patch('business.tac.TacBusObj.load_from_obj_instance',
               new_callable=AsyncMock) as mock_load:
        bus_obj_list = await TacBusObj.to_bus_obj_list(
            session_context, tac_list)

        assert len(bus_obj_list) == len(tac_list)
        assert all(
            isinstance(bus_obj, TacBusObj) for bus_obj in bus_obj_list)
        assert all(
            bus_obj.load_from_obj_instance.called for bus_obj in bus_obj_list)

        for bus_obj, tac in zip(bus_obj_list, tac_list):
            mock_load.assert_any_call(tac)

@pytest.mark.asyncio
async def test_to_bus_obj_list_empty(session_context):
    """
    Test the to_bus_obj_list method with an empty list.
    """
    empty_tac_list = []
    bus_obj_list = await TacBusObj.to_bus_obj_list(session_context, empty_tac_list)

    assert len(bus_obj_list) == 0
