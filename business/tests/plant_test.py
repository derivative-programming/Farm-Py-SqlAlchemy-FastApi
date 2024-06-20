# business/tests/plant_test.py
# pylint: disable=unused-import

"""
This module contains unit tests for the PlantBusObj class.
"""

from decimal import Decimal
import uuid
from datetime import datetime, date  # noqa: F401
from sqlalchemy.ext.asyncio import AsyncSession
import pytest
import pytest_asyncio
from helpers.session_context import SessionContext
from models import Plant
from models.factory import PlantFactory
from managers.plant import PlantManager
from business.plant import PlantBusObj
from services.logging_config import get_logger
import current_runtime  # noqa: F401
##GENINCLUDEFILE[GENVALPascalName.top.include.*]

logger = get_logger(__name__)


class TestPlantBusObj:
    """
    Unit tests for the PlantBusObj class.
    """

    @pytest_asyncio.fixture(scope="function")
    async def plant_manager(self, session: AsyncSession):
        """
        Fixture that returns an instance of the PlantManager class.
        """
        session_context = SessionContext(dict(), session)
        return PlantManager(session_context)

    @pytest_asyncio.fixture(scope="function")
    async def plant_bus_obj(self, session):
        """
        Fixture that returns an instance of the PlantBusObj class.
        """
        session_context = SessionContext(dict(), session)
        return PlantBusObj(session_context)

    @pytest_asyncio.fixture(scope="function")
    async def new_plant(self, session):
        """
        Fixture that returns a new instance of the Plant class.
        """
        # Use the PlantFactory to create a new plant instance
        # Assuming PlantFactory.create() is an async function
        return await PlantFactory.create_async(session)

    @pytest.mark.asyncio
    async def test_create_plant(
        self,
        plant_bus_obj: PlantBusObj
    ):
        """
        Test case for creating a new plant.
        """
        # Test creating a new plant

        assert plant_bus_obj.plant_id == 0

        # assert isinstance(plant_bus_obj.plant_id, int)
        assert isinstance(plant_bus_obj.code, uuid.UUID)

        assert isinstance(plant_bus_obj.last_change_code, int)

        assert plant_bus_obj.insert_user_id == uuid.UUID(int=0)

        assert plant_bus_obj.last_update_user_id == uuid.UUID(int=0)

        assert isinstance(plant_bus_obj.flvr_foreign_key_id, int)
        assert isinstance(plant_bus_obj.is_delete_allowed, bool)
        assert isinstance(plant_bus_obj.is_edit_allowed, bool)
        assert isinstance(plant_bus_obj.land_id, int)
        assert isinstance(plant_bus_obj.other_flavor, str)
        assert isinstance(plant_bus_obj.some_big_int_val, int)
        assert isinstance(plant_bus_obj.some_bit_val, bool)
        assert isinstance(plant_bus_obj.some_date_val, date)
        assert isinstance(plant_bus_obj.some_decimal_val, Decimal)
        assert isinstance(plant_bus_obj.some_email_address, str)
        assert isinstance(plant_bus_obj.some_float_val, float)
        assert isinstance(plant_bus_obj.some_int_val, int)
        assert isinstance(plant_bus_obj.some_money_val, Decimal)
        assert isinstance(plant_bus_obj.some_n_var_char_val, str)
        assert isinstance(plant_bus_obj.some_phone_number, str)
        assert isinstance(plant_bus_obj.some_text_val, str)
        # some_uniqueidentifier_val
        assert isinstance(plant_bus_obj.some_uniqueidentifier_val, uuid.UUID)
        assert isinstance(plant_bus_obj.some_utc_date_time_val, datetime)
        assert isinstance(plant_bus_obj.some_var_char_val, str)

    @pytest.mark.asyncio
    async def test_load_with_plant_obj(
        self,
        plant_manager: PlantManager,
        plant_bus_obj: PlantBusObj,
        new_plant: Plant
    ):
        """
        Test case for loading data from a plant object instance.
        """

        await plant_bus_obj.load_from_obj_instance(new_plant)

        assert plant_manager.is_equal(plant_bus_obj.plant, new_plant) is True

    @pytest.mark.asyncio
    async def test_load_with_plant_id(
        self,
        plant_manager: PlantManager,
        plant_bus_obj: PlantBusObj,
        new_plant: Plant
    ):
        """
        Test case for loading data from a plant ID.
        """

        new_plant_plant_id = new_plant.plant_id

        await plant_bus_obj.load_from_id(new_plant_plant_id)

        assert plant_manager.is_equal(plant_bus_obj.plant, new_plant) is True

    @pytest.mark.asyncio
    async def test_load_with_plant_code(
        self,
        plant_manager: PlantManager,
        plant_bus_obj: PlantBusObj,
        new_plant: Plant
    ):
        """
        Test case for loading data from a plant code.
        """

        await plant_bus_obj.load_from_code(new_plant.code)

        assert plant_manager.is_equal(plant_bus_obj.plant, new_plant) is True

    @pytest.mark.asyncio
    async def test_load_with_plant_json(
        self,
        plant_manager: PlantManager,
        plant_bus_obj: PlantBusObj,
        new_plant: Plant
    ):
        """
        Test case for loading data from a plant JSON.
        """

        plant_json = plant_manager.to_json(new_plant)

        await plant_bus_obj.load_from_json(plant_json)

        assert plant_manager.is_equal(plant_bus_obj.plant, new_plant) is True

    @pytest.mark.asyncio
    async def test_load_with_plant_dict(
        self,
        plant_manager: PlantManager,
        plant_bus_obj: PlantBusObj,
        new_plant: Plant
    ):
        """
        Test case for loading data from a plant dictionary.
        """

        logger.info("test_load_with_plant_dict 1")

        plant_dict = plant_manager.to_dict(new_plant)

        logger.info(plant_dict)

        await plant_bus_obj.load_from_dict(plant_dict)

        assert plant_manager.is_equal(
            plant_bus_obj.plant,
            new_plant) is True

    @pytest.mark.asyncio
    async def test_get_nonexistent_plant(
        self,
        plant_bus_obj: PlantBusObj
    ):
        """
        Test case for retrieving a nonexistent plant.
        """
        # Test retrieving a nonexistent plant raises an exception
        await plant_bus_obj.load_from_id(-1)

        # Assuming -1 is an id that wouldn't exist
        assert plant_bus_obj.is_valid() is False

    @pytest.mark.asyncio
    async def test_update_plant(
        self,
        plant_manager: PlantManager,
        plant_bus_obj: PlantBusObj,
        new_plant: Plant
    ):
        """
        Test case for updating a plant's data.
        """
        # Test updating a plant's data

        new_plant_plant_id_value = new_plant.plant_id

        new_plant = await plant_manager.get_by_id(new_plant_plant_id_value)

        assert isinstance(new_plant, Plant)

        new_code = uuid.uuid4()

        await plant_bus_obj.load_from_obj_instance(new_plant)

        plant_bus_obj.code = new_code

        await plant_bus_obj.save()

        new_plant_plant_id_value = new_plant.plant_id

        new_plant = await plant_manager.get_by_id(new_plant_plant_id_value)

        assert plant_manager.is_equal(
            plant_bus_obj.plant,
            new_plant) is True

    @pytest.mark.asyncio
    async def test_delete_plant(
        self,
        plant_manager: PlantManager,
        plant_bus_obj: PlantBusObj,
        new_plant: Plant
    ):
        """
        Test case for deleting a plant.
        """

        assert new_plant.plant_id is not None

        assert plant_bus_obj.plant_id == 0

        new_plant_plant_id_value = new_plant.plant_id

        await plant_bus_obj.load_from_id(new_plant_plant_id_value)

        assert plant_bus_obj.plant_id is not None

        await plant_bus_obj.delete()

        new_plant_plant_id_value = new_plant.plant_id

        new_plant = await plant_manager.get_by_id(new_plant_plant_id_value)

        assert new_plant is None

    ##GENINCLUDEFILE[GENVALPascalName.bottom.include.*]
