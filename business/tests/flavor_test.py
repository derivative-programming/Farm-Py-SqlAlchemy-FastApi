# business/tests/flavor_test.py
"""
    #TODO add comment
"""
import pytest
import pytest_asyncio
from datetime import datetime, date
from sqlalchemy.ext.asyncio import AsyncSession
from helpers.session_context import SessionContext
from models import Flavor
from models.factory import FlavorFactory
from managers.flavor import FlavorManager
from business.flavor import FlavorBusObj
from services.db_config import DB_DIALECT
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
from services.db_config import DB_DIALECT, generate_uuid
from sqlalchemy import String
from services.logging_config import get_logger
import managers as managers_and_enums
import current_runtime

logger = get_logger(__name__)
DB_DIALECT = "sqlite"
# Conditionally set the UUID column type
if DB_DIALECT == 'postgresql':
    UUIDType = UUID(as_uuid=True)
elif DB_DIALECT == 'mssql':
    UUIDType = UNIQUEIDENTIFIER
else:  # This will cover SQLite, MySQL, and other databases
    UUIDType = String(36)
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
        flavor_manager: FlavorManager,
        flavor_bus_obj: FlavorBusObj,
        new_flavor: Flavor
    ):
        """
            #TODO add comment
        """
        # Test creating a new flavor
        assert flavor_bus_obj.flavor_id is None
        # assert isinstance(flavor_bus_obj.flavor_id, int)
        if DB_DIALECT == 'postgresql':
            assert isinstance(flavor_bus_obj.code, UUID)
        elif DB_DIALECT == 'mssql':
            assert isinstance(flavor_bus_obj.code, UNIQUEIDENTIFIER)
        else:  # This will cover SQLite, MySQL, and other databases
            assert isinstance(flavor_bus_obj.code, str)
        assert isinstance(flavor_bus_obj.last_change_code, int)
        assert flavor_bus_obj.insert_user_id is None
        assert flavor_bus_obj.last_update_user_id is None
        assert flavor_bus_obj.description == "" or isinstance(
            flavor_bus_obj.description, str)
        assert isinstance(flavor_bus_obj.display_order, int)
        assert isinstance(flavor_bus_obj.is_active, bool)
        assert flavor_bus_obj.lookup_enum_name == "" or isinstance(
            flavor_bus_obj.lookup_enum_name, str)
        assert flavor_bus_obj.name == "" or isinstance(
            flavor_bus_obj.name, str)
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
        await flavor_bus_obj.load(flavor_obj_instance=new_flavor)
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
        await flavor_bus_obj.load(flavor_id=new_flavor.flavor_id)
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
        await flavor_bus_obj.load(code=new_flavor.code)
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
        await flavor_bus_obj.load(json_data=flavor_json)
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
        await flavor_bus_obj.load(flavor_dict=flavor_dict)
        assert flavor_manager.is_equal(
            flavor_bus_obj.flavor,
            new_flavor) is True
    @pytest.mark.asyncio
    async def test_get_nonexistent_flavor(
        self,
        flavor_manager: FlavorManager,
        flavor_bus_obj: FlavorBusObj,
        new_flavor: Flavor
    ):
        """
            #TODO add comment
        """
        # Test retrieving a nonexistent flavor raises an exception
        await flavor_bus_obj.load(flavor_id=-1)
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
        new_flavor = await flavor_manager.get_by_id(new_flavor.flavor_id)
        new_code = generate_uuid()
        await flavor_bus_obj.load(flavor_obj_instance=new_flavor)
        flavor_bus_obj.code = new_code
        await flavor_bus_obj.save()
        new_flavor = await flavor_manager.get_by_id(new_flavor.flavor_id)
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
        await flavor_bus_obj.load(flavor_id=new_flavor.flavor_id)
        assert flavor_bus_obj.flavor_id is not None
        await flavor_bus_obj.delete()
        new_flavor = await flavor_manager.get_by_id(new_flavor.flavor_id)
        assert new_flavor is None

