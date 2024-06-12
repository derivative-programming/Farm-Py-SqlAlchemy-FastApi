# business/tests/plant_test.py

"""
    #TODO add comment
"""

from datetime import datetime, date
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
from sqlalchemy import String
import pytest
import pytest_asyncio
from helpers.session_context import SessionContext
from models import Plant
from models.factory import PlantFactory
from managers.plant import PlantManager
from business.plant import PlantBusObj
from services.db_config import DB_DIALECT, generate_uuid, get_uuid_type
from services.logging_config import get_logger
import managers as managers_and_enums
import current_runtime
##GENINCLUDEFILE[GENVALPascalName.top.include.*]

logger = get_logger(__name__)

DB_DIALECT = "sqlite"  # noqa: F811


class TestPlantBusObj:
    """
        #TODO add comment
    """

    @pytest_asyncio.fixture(scope="function")
    async def plant_manager(self, session: AsyncSession):
        """
            #TODO add comment
        """
        session_context = SessionContext(dict(), session)
        return PlantManager(session_context)

    @pytest_asyncio.fixture(scope="function")
    async def plant_bus_obj(self, session):
        """
            #TODO add comment
        """
        session_context = SessionContext(dict(), session)
        return PlantBusObj(session_context)

    @pytest_asyncio.fixture(scope="function")
    async def new_plant(self, session):
        """
            #TODO add comment
        """
        # Use the PlantFactory to create a new plant instance
        # Assuming PlantFactory.create() is an async function
        return await PlantFactory.create_async(session)

    @pytest.mark.asyncio
    async def test_create_plant(
        self,
        plant_manager: PlantManager,
        plant_bus_obj: PlantBusObj,
        new_plant: Plant
    ):
        """
            #TODO add comment
        """
        # Test creating a new plant

        assert plant_bus_obj.plant_id is None

        # assert isinstance(plant_bus_obj.plant_id, int)
        if DB_DIALECT == 'postgresql':
            assert isinstance(plant_bus_obj.code, UUID)
        elif DB_DIALECT == 'mssql':
            assert isinstance(plant_bus_obj.code, UNIQUEIDENTIFIER)
        else:  # This will cover SQLite, MySQL, and other databases
            assert isinstance(plant_bus_obj.code, str)

        assert isinstance(plant_bus_obj.last_change_code, int)

        assert plant_bus_obj.insert_user_id is None

        assert plant_bus_obj.last_update_user_id is None

        assert isinstance(plant_bus_obj.flvr_foreign_key_id, int)
        assert isinstance(plant_bus_obj.is_delete_allowed, bool)
        assert isinstance(plant_bus_obj.is_edit_allowed, bool)
        assert isinstance(plant_bus_obj.land_id, int)
        assert plant_bus_obj.other_flavor == "" or isinstance(
            plant_bus_obj.other_flavor, str)
        assert isinstance(plant_bus_obj.some_big_int_val, int)
        assert isinstance(plant_bus_obj.some_bit_val, bool)
        assert isinstance(plant_bus_obj.some_date_val, date)
        assert isinstance(plant_bus_obj.some_decimal_val, int or float)
        assert plant_bus_obj.some_email_address == "" or isinstance(
            plant_bus_obj.some_email_address, str)
        assert isinstance(plant_bus_obj.some_float_val, float)
        assert isinstance(plant_bus_obj.some_int_val, int)
        assert isinstance(plant_bus_obj.some_money_val, int or float)
        assert plant_bus_obj.some_n_var_char_val == "" or isinstance(
            plant_bus_obj.some_n_var_char_val, str)
        assert plant_bus_obj.some_phone_number == "" or isinstance(
            plant_bus_obj.some_phone_number, str)
        assert plant_bus_obj.some_text_val == "" or isinstance(
            plant_bus_obj.some_text_val, str)
        # some_uniqueidentifier_val
        if DB_DIALECT == 'postgresql':
            assert isinstance(plant_bus_obj.some_uniqueidentifier_val, UUID)
        elif DB_DIALECT == 'mssql':
            assert isinstance(
                plant_bus_obj.some_uniqueidentifier_val,
                UNIQUEIDENTIFIER)
        else:  # This will cover SQLite, MySQL, and other databases
            assert isinstance(plant_bus_obj.some_uniqueidentifier_val, str)
        assert isinstance(plant_bus_obj.some_utc_date_time_val, datetime)
        assert plant_bus_obj.some_var_char_val == "" or isinstance(
            plant_bus_obj.some_var_char_val, str)

    @pytest.mark.asyncio
    async def test_load_with_plant_obj(
        self,
        plant_manager: PlantManager,
        plant_bus_obj: PlantBusObj,
        new_plant: Plant
    ):
        """
            #TODO add comment
        """

        await plant_bus_obj.load(plant_obj_instance=new_plant)

        assert plant_manager.is_equal(plant_bus_obj.plant, new_plant) is True

    @pytest.mark.asyncio
    async def test_load_with_plant_id(
        self,
        plant_manager: PlantManager,
        plant_bus_obj: PlantBusObj,
        new_plant: Plant
    ):
        """
            #TODO add comment
        """

        await plant_bus_obj.load(plant_id=new_plant.plant_id)

        assert plant_manager.is_equal(plant_bus_obj.plant, new_plant) is True

    @pytest.mark.asyncio
    async def test_load_with_plant_code(
        self,
        plant_manager: PlantManager,
        plant_bus_obj: PlantBusObj,
        new_plant: Plant
    ):
        """
            #TODO add comment
        """

        await plant_bus_obj.load(code=new_plant.code)

        assert plant_manager.is_equal(plant_bus_obj.plant, new_plant) is True

    @pytest.mark.asyncio
    async def test_load_with_plant_json(
        self,
        plant_manager: PlantManager,
        plant_bus_obj: PlantBusObj,
        new_plant: Plant
    ):
        """
            #TODO add comment
        """

        plant_json = plant_manager.to_json(new_plant)

        await plant_bus_obj.load(json_data=plant_json)

        assert plant_manager.is_equal(plant_bus_obj.plant, new_plant) is True

    @pytest.mark.asyncio
    async def test_load_with_plant_dict(
        self,
        plant_manager: PlantManager,
        plant_bus_obj: PlantBusObj,
        new_plant: Plant
    ):
        """
            #TODO add comment
        """

        logger.info("test_load_with_plant_dict 1")

        plant_dict = plant_manager.to_dict(new_plant)

        logger.info(plant_dict)

        await plant_bus_obj.load(plant_dict=plant_dict)

        assert plant_manager.is_equal(
            plant_bus_obj.plant,
            new_plant) is True

    @pytest.mark.asyncio
    async def test_get_nonexistent_plant(
        self,
        plant_manager: PlantManager,
        plant_bus_obj: PlantBusObj,
        new_plant: Plant
    ):
        """
            #TODO add comment
        """
        # Test retrieving a nonexistent plant raises an exception
        await plant_bus_obj.load(plant_id=-1)
        assert plant_bus_obj.is_valid() is False  # Assuming -1 is an id that wouldn't exist

    @pytest.mark.asyncio
    async def test_update_plant(
        self,
        plant_manager: PlantManager,
        plant_bus_obj: PlantBusObj,
        new_plant: Plant
    ):
        """
            #TODO add comment
        """
        # Test updating a plant's data

        new_plant = await plant_manager.get_by_id(new_plant.plant_id)

        new_code = generate_uuid()

        await plant_bus_obj.load(plant_obj_instance=new_plant)

        plant_bus_obj.code = new_code

        await plant_bus_obj.save()

        new_plant = await plant_manager.get_by_id(new_plant.plant_id)

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
            #TODO add comment
        """

        assert new_plant.plant_id is not None

        assert plant_bus_obj.plant_id is None

        await plant_bus_obj.load(plant_id=new_plant.plant_id)

        assert plant_bus_obj.plant_id is not None

        await plant_bus_obj.delete()

        new_plant = await plant_manager.get_by_id(new_plant.plant_id)

        assert new_plant is None

    ##GENINCLUDEFILE[GENVALPascalName.bottom.include.*]
