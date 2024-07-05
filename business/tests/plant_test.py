# business/tests/plant_test.py
# pylint: disable=redefined-outer-name
# pylint: disable=unused-import
"""
Unit tests for the
PlantBusObj class.
"""

from unittest.mock import AsyncMock, Mock, patch

import pytest
import pytest_asyncio

import models
from models.factory import (
    PlantFactory)
from business.plant import (
    PlantBusObj)
from helpers.session_context import SessionContext
from models import (
    Plant)


@pytest.fixture
def session_context():
    """
    Return a mock SessionContext object.
    """
    return Mock(spec=SessionContext)


@pytest.fixture
def plant():
    """
    Fixture that returns a mock
    plant object.
    """
    return Mock(spec=Plant)


@pytest.fixture
def obj_list():
    """
    Return a list of mock Plant objects.
    """
    plants = []
    for _ in range(3):
        plant = Mock(spec=Plant)
        plants.append(plant)
    return plants


@pytest_asyncio.fixture(scope="function")
async def new_obj(session):
    """
    Fixture that returns a new instance of
    the Plant class.
    """

    return await PlantFactory.create_async(
        session)


@pytest_asyncio.fixture(scope="function")
async def new_bus_obj(session, new_obj) -> PlantBusObj:
    """
    Fixture that returns a new instance of
    the Plant class.
    """

    session_context = SessionContext({}, session)
    plant_bus_obj = PlantBusObj(session_context, new_obj)

    return plant_bus_obj


class TestPlantBusObj:
    """
    Unit tests for the
    PlantBusObj class.
    """

    @pytest.mark.asyncio
    async def test_to_bus_obj_list(
            self, session_context, obj_list):
        """
        Test the to_bus_obj_list method.
        """
        with patch(
                "business.plant"
                ".PlantBusObj"
                ".load_from_obj_instance",
                new_callable=AsyncMock) as mock_load:
            bus_obj_list = await \
                PlantBusObj.to_bus_obj_list(
                    session_context, obj_list)

            assert len(bus_obj_list) == len(obj_list)
            assert all(
                isinstance(bus_obj, PlantBusObj)
                for bus_obj in bus_obj_list)
            assert all(
                bus_obj.load_from_obj_instance.called
                for bus_obj in bus_obj_list)

            for bus_obj, plant in zip(bus_obj_list, obj_list):
                mock_load.assert_any_call(plant)

    @pytest.mark.asyncio
    async def test_to_bus_obj_list_empty(
            self, session_context):
        """
        Test the to_bus_obj_list
        method with an empty list.
        """
        empty_obj_list = []
        bus_obj_list = await \
            PlantBusObj.to_bus_obj_list(
                session_context,
                empty_obj_list)

        assert len(bus_obj_list) == 0
# endset
    # isDeleteAllowed,
    # isEditAllowed,
    # otherFlavor,
    # someBigIntVal,
    # someBitVal,
    # someDecimalVal,
    # someEmailAddress,
    # someFloatVal,
    # someIntVal,
    # someMoneyVal,
    # someNVarCharVal,
    # someDateVal
    # someUTCDateTimeVal
    # LandID

    @pytest.mark.asyncio
    async def test_get_land_id_obj(
        self, new_bus_obj: PlantBusObj
    ):
        """
        Test the get_land_id_obj method.
        """

        # Call the get_land_id_bus_obj method
        fk_obj: models.Land = await \
            new_bus_obj.get_land_id_obj()

        assert fk_obj is not None

        assert isinstance(fk_obj, models.Land)

        assert fk_obj.land_id == \
            new_bus_obj.land_id

        assert fk_obj.code == \
            new_bus_obj.land_code_peek

    @pytest.mark.asyncio
    async def test_get_land_id_bus_obj(
        self, new_bus_obj: PlantBusObj
    ):
        """
        Test the get_land_id_bus_obj method.
        """
        from ..land import (  # LandID
            LandBusObj)
        # Call the get_land_id_bus_obj method
        fk_bus_obj: LandBusObj = await \
            new_bus_obj.get_land_id_bus_obj()

        assert fk_bus_obj is not None

        assert isinstance(fk_bus_obj, LandBusObj)

        assert fk_bus_obj.land_id == \
            new_bus_obj.land_id

        assert fk_bus_obj.code == \
            new_bus_obj.land_code_peek
    # FlvrForeignKeyID

    @pytest.mark.asyncio
    async def test_get_flvr_foreign_key_id_obj(
        self, new_bus_obj: PlantBusObj
    ):
        """
        Test the get_flvr_foreign_key_id_obj method.
        """

        # Call the get_flvr_foreign_key_id_obj method
        fk_obj: models.Flavor = \
            await new_bus_obj.get_flvr_foreign_key_id_obj()

        assert fk_obj is not None

        assert isinstance(fk_obj, models.Flavor)

        assert fk_obj.flavor_id == \
            new_bus_obj.flvr_foreign_key_id

        assert fk_obj.code == \
            new_bus_obj.flvr_foreign_key_code_peek

    @pytest.mark.asyncio
    async def test_get_flvr_foreign_key_id_bus_obj(
        self, new_bus_obj: PlantBusObj
    ):
        """
        Test the get_flvr_foreign_key_id_bus_obj
        method.
        """

        from ..flavor import (  # FlvrForeignKeyID
            FlavorBusObj)
        # Call the get_flvr_foreign_key_id_bus_obj method
        fk_bus_obj: FlavorBusObj = \
            await new_bus_obj.get_flvr_foreign_key_id_bus_obj()

        assert fk_bus_obj is not None

        assert isinstance(fk_bus_obj, FlavorBusObj)

        assert fk_bus_obj.flavor_id == \
            new_bus_obj.flvr_foreign_key_id

        assert fk_bus_obj.code == \
            new_bus_obj.flvr_foreign_key_code_peek
    # somePhoneNumber,
    # someTextVal,
    # someUniqueidentifierVal,
    # someVarCharVal
