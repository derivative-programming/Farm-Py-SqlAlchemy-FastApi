# business/tests/org_api_key_test.py
"""
Unit tests for the OrgApiKeyBusObj class.
"""
from typing import List
from unittest.mock import AsyncMock, Mock, patch

import pytest

from business.org_api_key import OrgApiKeyBusObj
from helpers.session_context import SessionContext
from models import OrgApiKey

@pytest.fixture
def session_context():
    """
    Return a mock SessionContext object.
    """
    return Mock(spec=SessionContext)

@pytest.fixture
def org_api_key_list():
    """
    Return a list of mock OrgApiKey objects.
    """
    org_api_keys = []
    for _ in range(3):
        org_api_key = Mock(spec=OrgApiKey)
        org_api_keys.append(org_api_key)
    return org_api_keys

@pytest.mark.asyncio
async def test_to_bus_obj_list(session_context, org_api_key_list):
    """
    Test the to_bus_obj_list method.
    """
    with patch('business.org_api_key.OrgApiKeyBusObj.load_from_obj_instance',
               new_callable=AsyncMock) as mock_load:
        bus_obj_list = await OrgApiKeyBusObj.to_bus_obj_list(
            session_context, org_api_key_list)

        assert len(bus_obj_list) == len(org_api_key_list)
        assert all(
            isinstance(bus_obj, OrgApiKeyBusObj) for bus_obj in bus_obj_list)
        assert all(
            bus_obj.load_from_obj_instance.called for bus_obj in bus_obj_list)

        for bus_obj, org_api_key in zip(bus_obj_list, org_api_key_list):
            mock_load.assert_any_call(org_api_key)

@pytest.mark.asyncio
async def test_to_bus_obj_list_empty(session_context):
    """
    Test the to_bus_obj_list method with an empty list.
    """
    empty_org_api_key_list = []
    bus_obj_list = await OrgApiKeyBusObj.to_bus_obj_list(session_context, empty_org_api_key_list)

    assert len(bus_obj_list) == 0
