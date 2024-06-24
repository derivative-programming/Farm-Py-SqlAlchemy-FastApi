# business/tests/pac_test.py
"""
Unit tests for the PacBusObj class.
"""
from typing import List
from unittest.mock import AsyncMock, Mock, patch

import pytest

from business.pac import PacBusObj
from helpers.session_context import SessionContext
from models import Pac

@pytest.fixture
def session_context():
    """
    Return a mock SessionContext object.
    """
    return Mock(spec=SessionContext)

@pytest.fixture
def pac_list():
    """
    Return a list of mock Pac objects.
    """
    pacs = []
    for _ in range(3):
        pac = Mock(spec=Pac)
        pacs.append(pac)
    return pacs

@pytest.mark.asyncio
async def test_to_bus_obj_list(session_context, pac_list):
    """
    Test the to_bus_obj_list method.
    """
    with patch('business.pac.PacBusObj.load_from_obj_instance',
               new_callable=AsyncMock) as mock_load:
        bus_obj_list = await PacBusObj.to_bus_obj_list(
            session_context, pac_list)

        assert len(bus_obj_list) == len(pac_list)
        assert all(
            isinstance(bus_obj, PacBusObj) for bus_obj in bus_obj_list)
        assert all(
            bus_obj.load_from_obj_instance.called for bus_obj in bus_obj_list)

        for bus_obj, pac in zip(bus_obj_list, pac_list):
            mock_load.assert_any_call(pac)

@pytest.mark.asyncio
async def test_to_bus_obj_list_empty(session_context):
    """
    Test the to_bus_obj_list method with an empty list.
    """
    empty_pac_list = []
    bus_obj_list = await PacBusObj.to_bus_obj_list(session_context, empty_pac_list)

    assert len(bus_obj_list) == 0
