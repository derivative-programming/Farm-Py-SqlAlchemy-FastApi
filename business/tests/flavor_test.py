# business/tests/flavor_test.py
# pylint: disable=unused-import
"""
This module contains unit tests for the FlavorBusObj class.
"""
from decimal import Decimal
import uuid
from datetime import datetime, date  # noqa: F401
from sqlalchemy.ext.asyncio import AsyncSession
import pytest
import pytest_asyncio
from helpers.session_context import SessionContext
from models import Flavor
from models.factory import FlavorFactory
from managers.flavor import FlavorManager
from business.flavor import FlavorBusObj
from services.logging_config import get_logger
import current_runtime  # noqa: F401

logger = get_logger(__name__)
class TestFlavorBusObj:
    """
    Unit tests for the FlavorBusObj class.
    """
    @pytest_asyncio.fixture(scope="function")
    async def flavor_manager(self, session: AsyncSession):
        """
        Fixture that returns an instance of the FlavorManager class.
        """
        session_context = SessionContext(dict(), session)
        return FlavorManager(session_context)
    @pytest_asyncio.fixture(scope="function")
    async def flavor_bus_obj(self, session):
        """
        Fixture that returns an instance of the FlavorBusObj class.
        """
        session_context = SessionContext(dict(), session)
        return FlavorBusObj(session_context)
    @pytest_asyncio.fixture(scope="function")
    async def new_flavor(self, session):
        """
        Fixture that returns a new instance of the Flavor class.
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
        Test case for creating a new flavor.
        """
        # Test creating a new flavor
        assert flavor_bus_obj.flavor_id == 0
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
        Test case for loading data from a flavor object instance.
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
        Test case for loading data from a flavor ID.
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
        Test case for loading data from a flavor code.
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
        Test case for loading data from a flavor JSON.
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
        Test case for loading data from a flavor dictionary.
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
        Test case for retrieving a nonexistent flavor.
        """
        # Test retrieving a nonexistent flavor raises an exception
        await flavor_bus_obj.load_from_id(-1)
        # Assuming -1 is an id that wouldn't exist
        assert flavor_bus_obj.is_valid() is False
    @pytest.mark.asyncio
    async def test_update_flavor(
        self,
        flavor_manager: FlavorManager,
        flavor_bus_obj: FlavorBusObj,
        new_flavor: Flavor
    ):
        """
        Test case for updating a flavor's data.
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
        Test case for deleting a flavor.
        """
        assert new_flavor.flavor_id is not None
        assert flavor_bus_obj.flavor_id == 0
        new_flavor_flavor_id_value = new_flavor.flavor_id
        await flavor_bus_obj.load_from_id(new_flavor_flavor_id_value)
        assert flavor_bus_obj.flavor_id is not None
        await flavor_bus_obj.delete()
        new_flavor_flavor_id_value = new_flavor.flavor_id
        new_flavor = await flavor_manager.get_by_id(new_flavor_flavor_id_value)
        assert new_flavor is None

