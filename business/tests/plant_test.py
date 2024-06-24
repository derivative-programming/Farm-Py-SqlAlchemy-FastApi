# business/tests/plant_test.py
# pylint: disable=redefined-outer-name
"""
Unit tests for the PlantBusObj class.
"""

from unittest.mock import AsyncMock, Mock, patch

import pytest

from business.plant import PlantBusObj
from helpers.session_context import SessionContext
from models import Plant


@pytest.fixture
def session_context():
    """
    Return a mock SessionContext object.
    """
    return Mock(spec=SessionContext)


@pytest.fixture
def plant_list():
    """
    Return a list of mock Plant objects.
    """
    plants = []
    for _ in range(3):
        plant = Mock(spec=Plant)
        plants.append(plant)
    return plants


@pytest.mark.asyncio
async def test_to_bus_obj_list(session_context, plant_list):
    """
    Test the to_bus_obj_list method.
    """
    with patch('business.plant.PlantBusObj.load_from_obj_instance',
               new_callable=AsyncMock) as mock_load:
        bus_obj_list = await PlantBusObj.to_bus_obj_list(
            session_context, plant_list)

        assert len(bus_obj_list) == len(plant_list)
        assert all(
            isinstance(bus_obj, PlantBusObj) for bus_obj in bus_obj_list)
        assert all(
            bus_obj.load_from_obj_instance.called for bus_obj in bus_obj_list)

        for bus_obj, plant in zip(bus_obj_list, plant_list):
            mock_load.assert_any_call(plant)


@pytest.mark.asyncio
async def test_to_bus_obj_list_empty(session_context):
    """
    Test the to_bus_obj_list method with an empty list.
    """
    empty_plant_list = []
    bus_obj_list = await PlantBusObj.to_bus_obj_list(session_context, empty_plant_list)

    assert len(bus_obj_list) == 0
