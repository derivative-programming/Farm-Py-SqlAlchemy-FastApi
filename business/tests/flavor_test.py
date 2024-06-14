# business/tests/flavor_test.py
"""
    #TODO add comment
"""
import uuid
from datetime import datetime, date
from sqlalchemy.ext.asyncio import AsyncSession
import pytest
import pytest_asyncio
from helpers.session_context import SessionContext
from models import Flavor
from models.factory import FlavorFactory
from managers.flavor import FlavorManager
from business.flavor import FlavorBusObj
from services.logging_config import get_logger
import managers as managers_and_enums
import current_runtime

logger = get_logger(__name__)
class TestFlavorBusObj:
    """
        #TODO add comment
    """
    @pytest_asyncio.fixture(scope="function")
    async def flavor_manager(self, session: AsyncSession):
        """
            #TODO add comment
        """
        session_context = SessionContext(dict(), session)
        return FlavorManager(session_context)
    @pytest_asyncio.fixture(scope="function")
    async def flavor_bus_obj(self, session):
        """
            #TODO add comment
        """
        session_context = SessionContext(dict(), session)
        return FlavorBusObj(session_context)
    @pytest_asyncio.fixture(scope="function")
    async def new_flavor(self, session):
        """
            #TODO add comment
        """
        # Use the FlavorFactory to create a new flavor instance
        # Assuming FlavorFactory.create() is an async function
        return await FlavorFactory.create_async(session)
    @pytest.mark.asyncio
    async def test_create_flavor(
        self,
        flavor_bus_obj: FlavorBusObj
    ):
        """
            #TODO add comment
        """
        # Test creating a new flavor
        assert flavor_bus_obj.flavor_id is None
        # assert isinstance(flavor_bus_obj.flavor_id, int)
        assert isinstance(flavor_bus_obj.code, uuid.UUID)
        assert isinstance(flavor_bus_obj.last_change_code, int)
        assert flavor_bus_obj.insert_user_id == uuid.UUID(int=0)
        assert flavor_bus_obj.last_update_user_id == uuid.UUID(int=0)
        assert isinstance(flavor_bus_obj.description, str)
        assert isinstance(flavor_bus_obj.display_order, int)
        assert isinstance(flavor_bus_obj.is_active, bool)
        assert isinstance(flavor_bus_obj.lookup_enum_name, str)
        assert isinstance(flavor_bus_obj.name, str)
        assert isinstance(flavor_bus_obj.pac_id, int)
    @pytest.mark.asyncio
    async def test_load_with_flavor_obj(
        self,
        flavor_manager: FlavorManager,
        flavor_bus_obj: FlavorBusObj,
        new_flavor: Flavor
    ):
        """
            #TODO add comment
        """
        await flavor_bus_obj.load_from_obj_instance(new_flavor)
        assert flavor_manager.is_equal(flavor_bus_obj.flavor, new_flavor) is True
    @pytest.mark.asyncio
    async def test_load_with_flavor_id(
        self,
        flavor_manager: FlavorManager,
        flavor_bus_obj: FlavorBusObj,
        new_flavor: Flavor
    ):
        """
            #TODO add comment
        """
        new_flavor_flavor_id = new_flavor.flavor_id
        await flavor_bus_obj.load_from_id(new_flavor_flavor_id)
        assert flavor_manager.is_equal(flavor_bus_obj.flavor, new_flavor) is True
    @pytest.mark.asyncio
    async def test_load_with_flavor_code(
        self,
        flavor_manager: FlavorManager,
        flavor_bus_obj: FlavorBusObj,
        new_flavor: Flavor
    ):
        """
            #TODO add comment
        """
        await flavor_bus_obj.load_from_code(new_flavor.code)
        assert flavor_manager.is_equal(flavor_bus_obj.flavor, new_flavor) is True
    @pytest.mark.asyncio
    async def test_load_with_flavor_json(
        self,
        flavor_manager: FlavorManager,
        flavor_bus_obj: FlavorBusObj,
        new_flavor: Flavor
    ):
        """
            #TODO add comment
        """
        flavor_json = flavor_manager.to_json(new_flavor)
        await flavor_bus_obj.load_from_json(flavor_json)
        assert flavor_manager.is_equal(flavor_bus_obj.flavor, new_flavor) is True
    @pytest.mark.asyncio
    async def test_load_with_flavor_dict(
        self,
        flavor_manager: FlavorManager,
        flavor_bus_obj: FlavorBusObj,
        new_flavor: Flavor
    ):
        """
            #TODO add comment
        """
        logger.info("test_load_with_flavor_dict 1")
        flavor_dict = flavor_manager.to_dict(new_flavor)
        logger.info(flavor_dict)
        await flavor_bus_obj.load_from_dict(flavor_dict)
        assert flavor_manager.is_equal(
            flavor_bus_obj.flavor,
            new_flavor) is True
    @pytest.mark.asyncio
    async def test_get_nonexistent_flavor(
        self,
        flavor_bus_obj: FlavorBusObj
    ):
        """
            #TODO add comment
        """
        # Test retrieving a nonexistent flavor raises an exception
        await flavor_bus_obj.load_from_id(-1)
        assert flavor_bus_obj.is_valid() is False  # Assuming -1 is an id that wouldn't exist
    @pytest.mark.asyncio
    async def test_update_flavor(
        self,
        flavor_manager: FlavorManager,
        flavor_bus_obj: FlavorBusObj,
        new_flavor: Flavor
    ):
        """
            #TODO add comment
        """
        # Test updating a flavor's data
        new_flavor_flavor_id_value = new_flavor.flavor_id
        new_flavor = await flavor_manager.get_by_id(new_flavor_flavor_id_value)
        assert isinstance(new_flavor, Flavor)
        new_code = uuid.uuid4()
        await flavor_bus_obj.load_from_obj_instance(new_flavor)
        flavor_bus_obj.code = new_code
        await flavor_bus_obj.save()
        new_flavor_flavor_id_value = new_flavor.flavor_id
        new_flavor = await flavor_manager.get_by_id(new_flavor_flavor_id_value)
        assert flavor_manager.is_equal(
            flavor_bus_obj.flavor,
            new_flavor) is True
    @pytest.mark.asyncio
    async def test_delete_flavor(
        self,
        flavor_manager: FlavorManager,
        flavor_bus_obj: FlavorBusObj,
        new_flavor: Flavor
    ):
        """
            #TODO add comment
        """
        assert new_flavor.flavor_id is not None
        assert flavor_bus_obj.flavor_id is None
        new_flavor_flavor_id_value = new_flavor.flavor_id
        await flavor_bus_obj.load_from_id(new_flavor_flavor_id_value)
        assert flavor_bus_obj.flavor_id is not None
        await flavor_bus_obj.delete()
        new_flavor_flavor_id_value = new_flavor.flavor_id
        new_flavor = await flavor_manager.get_by_id(new_flavor_flavor_id_value)
        assert new_flavor is None

