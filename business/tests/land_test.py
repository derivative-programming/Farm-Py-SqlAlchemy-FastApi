# business/tests/land_test.py
# pylint: disable=unused-import
"""
    #TODO add comment
"""
import uuid
from datetime import datetime, date  # noqa: F401
from sqlalchemy.ext.asyncio import AsyncSession
import pytest
import pytest_asyncio
from helpers.session_context import SessionContext
from models import Land
from models.factory import LandFactory
from managers.land import LandManager
from business.land import LandBusObj
from services.logging_config import get_logger
import current_runtime  # noqa: F401

logger = get_logger(__name__)
class TestLandBusObj:
    """
        #TODO add comment
    """
    @pytest_asyncio.fixture(scope="function")
    async def land_manager(self, session: AsyncSession):
        """
            #TODO add comment
        """
        session_context = SessionContext(dict(), session)
        return LandManager(session_context)
    @pytest_asyncio.fixture(scope="function")
    async def land_bus_obj(self, session):
        """
            #TODO add comment
        """
        session_context = SessionContext(dict(), session)
        return LandBusObj(session_context)
    @pytest_asyncio.fixture(scope="function")
    async def new_land(self, session):
        """
            #TODO add comment
        """
        # Use the LandFactory to create a new land instance
        # Assuming LandFactory.create() is an async function
        return await LandFactory.create_async(session)
    @pytest.mark.asyncio
    async def test_create_land(
        self,
        land_bus_obj: LandBusObj
    ):
        """
            #TODO add comment
        """
        # Test creating a new land
        assert land_bus_obj.land_id == 0
        # assert isinstance(land_bus_obj.land_id, int)
        assert isinstance(land_bus_obj.code, uuid.UUID)
        assert isinstance(land_bus_obj.last_change_code, int)
        assert land_bus_obj.insert_user_id == uuid.UUID(int=0)
        assert land_bus_obj.last_update_user_id == uuid.UUID(int=0)
        assert isinstance(land_bus_obj.description, str)
        assert isinstance(land_bus_obj.display_order, int)
        assert isinstance(land_bus_obj.is_active, bool)
        assert isinstance(land_bus_obj.lookup_enum_name, str)
        assert isinstance(land_bus_obj.name, str)
        assert isinstance(land_bus_obj.pac_id, int)
    @pytest.mark.asyncio
    async def test_load_with_land_obj(
        self,
        land_manager: LandManager,
        land_bus_obj: LandBusObj,
        new_land: Land
    ):
        """
            #TODO add comment
        """
        await land_bus_obj.load_from_obj_instance(new_land)
        assert land_manager.is_equal(land_bus_obj.land, new_land) is True
    @pytest.mark.asyncio
    async def test_load_with_land_id(
        self,
        land_manager: LandManager,
        land_bus_obj: LandBusObj,
        new_land: Land
    ):
        """
            #TODO add comment
        """
        new_land_land_id = new_land.land_id
        await land_bus_obj.load_from_id(new_land_land_id)
        assert land_manager.is_equal(land_bus_obj.land, new_land) is True
    @pytest.mark.asyncio
    async def test_load_with_land_code(
        self,
        land_manager: LandManager,
        land_bus_obj: LandBusObj,
        new_land: Land
    ):
        """
            #TODO add comment
        """
        await land_bus_obj.load_from_code(new_land.code)
        assert land_manager.is_equal(land_bus_obj.land, new_land) is True
    @pytest.mark.asyncio
    async def test_load_with_land_json(
        self,
        land_manager: LandManager,
        land_bus_obj: LandBusObj,
        new_land: Land
    ):
        """
            #TODO add comment
        """
        land_json = land_manager.to_json(new_land)
        await land_bus_obj.load_from_json(land_json)
        assert land_manager.is_equal(land_bus_obj.land, new_land) is True
    @pytest.mark.asyncio
    async def test_load_with_land_dict(
        self,
        land_manager: LandManager,
        land_bus_obj: LandBusObj,
        new_land: Land
    ):
        """
            #TODO add comment
        """
        logger.info("test_load_with_land_dict 1")
        land_dict = land_manager.to_dict(new_land)
        logger.info(land_dict)
        await land_bus_obj.load_from_dict(land_dict)
        assert land_manager.is_equal(
            land_bus_obj.land,
            new_land) is True
    @pytest.mark.asyncio
    async def test_get_nonexistent_land(
        self,
        land_bus_obj: LandBusObj
    ):
        """
            #TODO add comment
        """
        # Test retrieving a nonexistent land raises an exception
        await land_bus_obj.load_from_id(-1)
        # Assuming -1 is an id that wouldn't exist
        assert land_bus_obj.is_valid() is False
    @pytest.mark.asyncio
    async def test_update_land(
        self,
        land_manager: LandManager,
        land_bus_obj: LandBusObj,
        new_land: Land
    ):
        """
            #TODO add comment
        """
        # Test updating a land's data
        new_land_land_id_value = new_land.land_id
        new_land = await land_manager.get_by_id(new_land_land_id_value)
        assert isinstance(new_land, Land)
        new_code = uuid.uuid4()
        await land_bus_obj.load_from_obj_instance(new_land)
        land_bus_obj.code = new_code
        await land_bus_obj.save()
        new_land_land_id_value = new_land.land_id
        new_land = await land_manager.get_by_id(new_land_land_id_value)
        assert land_manager.is_equal(
            land_bus_obj.land,
            new_land) is True
    @pytest.mark.asyncio
    async def test_delete_land(
        self,
        land_manager: LandManager,
        land_bus_obj: LandBusObj,
        new_land: Land
    ):
        """
            #TODO add comment
        """
        assert new_land.land_id is not None
        assert land_bus_obj.land_id == 0
        new_land_land_id_value = new_land.land_id
        await land_bus_obj.load_from_id(new_land_land_id_value)
        assert land_bus_obj.land_id is not None
        await land_bus_obj.delete()
        new_land_land_id_value = new_land.land_id
        new_land = await land_manager.get_by_id(new_land_land_id_value)
        assert new_land is None

    @pytest.mark.asyncio
    async def test_build_plant(
        self,
        land_bus_obj: LandBusObj,
        new_land: Land,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """

        session_context = SessionContext(dict(), session)

        await current_runtime.initialize(session_context)

        await land_bus_obj.load_from_id(
            new_land.land_id
        )

        plant_bus_obj = await land_bus_obj.build_plant()

        assert plant_bus_obj.land_id == land_bus_obj.land_id
        assert plant_bus_obj.land_code_peek == land_bus_obj.code

        await plant_bus_obj.save()

        assert plant_bus_obj.plant_id > 0

    @pytest.mark.asyncio
    async def test_get_all_plant(
        self,
        land_bus_obj: LandBusObj,
        new_land: Land,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """

        session_context = SessionContext(dict(), session)

        await current_runtime.initialize(session_context)

        new_land_land_id = (
            new_land.land_id
        )

        await land_bus_obj.load_from_id(
            new_land_land_id
        )

        plant_bus_obj = await land_bus_obj.build_plant()

        await plant_bus_obj.save()

        plant_list = await land_bus_obj.get_all_plant()

        assert len(plant_list) >= 1

        #assert plant_list[0].plant_id > 0

        #assert plant_list[0].plant_id == plant_bus_obj.plant_id

