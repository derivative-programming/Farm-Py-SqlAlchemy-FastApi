# business/tests/role_test.py
# pylint: disable=unused-import
"""
This module contains unit tests for the RoleBusObj class.
"""
from decimal import Decimal
import uuid
from datetime import datetime, date  # noqa: F401
from sqlalchemy.ext.asyncio import AsyncSession
import pytest
import pytest_asyncio
from helpers.session_context import SessionContext
from models import Role
from models.factory import RoleFactory
from managers.role import RoleManager
from business.role import RoleBusObj
from services.logging_config import get_logger
import current_runtime  # noqa: F401

logger = get_logger(__name__)
class TestRoleBusObj:
    """
    Unit tests for the RoleBusObj class.
    """
    @pytest_asyncio.fixture(scope="function")
    async def role_manager(self, session: AsyncSession):
        """
        Fixture that returns an instance of the RoleManager class.
        """
        session_context = SessionContext(dict(), session)
        return RoleManager(session_context)
    @pytest_asyncio.fixture(scope="function")
    async def role_bus_obj(self, session):
        """
        Fixture that returns an instance of the RoleBusObj class.
        """
        session_context = SessionContext(dict(), session)
        return RoleBusObj(session_context)
    @pytest_asyncio.fixture(scope="function")
    async def new_role(self, session):
        """
        Fixture that returns a new instance of the Role class.
        """
        # Use the RoleFactory to create a new role instance
        # Assuming RoleFactory.create() is an async function
        return await RoleFactory.create_async(session)
    @pytest.mark.asyncio
    async def test_create_role(
        self,
        role_bus_obj: RoleBusObj
    ):
        """
        Test case for creating a new role.
        """
        # Test creating a new role
        assert role_bus_obj.role_id == 0
        # assert isinstance(role_bus_obj.role_id, int)
        assert isinstance(role_bus_obj.code, uuid.UUID)
        assert isinstance(role_bus_obj.last_change_code, int)
        assert role_bus_obj.insert_user_id == uuid.UUID(int=0)
        assert role_bus_obj.last_update_user_id == uuid.UUID(int=0)
        assert isinstance(role_bus_obj.description, str)
        assert isinstance(role_bus_obj.display_order, int)
        assert isinstance(role_bus_obj.is_active, bool)
        assert isinstance(role_bus_obj.lookup_enum_name, str)
        assert isinstance(role_bus_obj.name, str)
        assert isinstance(role_bus_obj.pac_id, int)
    @pytest.mark.asyncio
    async def test_load_with_role_obj(
        self,
        role_manager: RoleManager,
        role_bus_obj: RoleBusObj,
        new_role: Role
    ):
        """
        Test case for loading data from a role object instance.
        """
        await role_bus_obj.load_from_obj_instance(new_role)
        assert role_manager.is_equal(role_bus_obj.role, new_role) is True
    @pytest.mark.asyncio
    async def test_load_with_role_id(
        self,
        role_manager: RoleManager,
        role_bus_obj: RoleBusObj,
        new_role: Role
    ):
        """
        Test case for loading data from a role ID.
        """
        new_role_role_id = new_role.role_id
        await role_bus_obj.load_from_id(new_role_role_id)
        assert role_manager.is_equal(role_bus_obj.role, new_role) is True
    @pytest.mark.asyncio
    async def test_load_with_role_code(
        self,
        role_manager: RoleManager,
        role_bus_obj: RoleBusObj,
        new_role: Role
    ):
        """
        Test case for loading data from a role code.
        """
        await role_bus_obj.load_from_code(new_role.code)
        assert role_manager.is_equal(role_bus_obj.role, new_role) is True
    @pytest.mark.asyncio
    async def test_load_with_role_json(
        self,
        role_manager: RoleManager,
        role_bus_obj: RoleBusObj,
        new_role: Role
    ):
        """
        Test case for loading data from a role JSON.
        """
        role_json = role_manager.to_json(new_role)
        await role_bus_obj.load_from_json(role_json)
        assert role_manager.is_equal(role_bus_obj.role, new_role) is True
    @pytest.mark.asyncio
    async def test_load_with_role_dict(
        self,
        role_manager: RoleManager,
        role_bus_obj: RoleBusObj,
        new_role: Role
    ):
        """
        Test case for loading data from a role dictionary.
        """
        logger.info("test_load_with_role_dict 1")
        role_dict = role_manager.to_dict(new_role)
        logger.info(role_dict)
        await role_bus_obj.load_from_dict(role_dict)
        assert role_manager.is_equal(
            role_bus_obj.role,
            new_role) is True
    @pytest.mark.asyncio
    async def test_get_nonexistent_role(
        self,
        role_bus_obj: RoleBusObj
    ):
        """
        Test case for retrieving a nonexistent role.
        """
        # Test retrieving a nonexistent role raises an exception
        await role_bus_obj.load_from_id(-1)
        # Assuming -1 is an id that wouldn't exist
        assert role_bus_obj.is_valid() is False
    @pytest.mark.asyncio
    async def test_update_role(
        self,
        role_manager: RoleManager,
        role_bus_obj: RoleBusObj,
        new_role: Role
    ):
        """
        Test case for updating a role's data.
        """
        # Test updating a role's data
        new_role_role_id_value = new_role.role_id
        new_role = await role_manager.get_by_id(new_role_role_id_value)
        assert isinstance(new_role, Role)
        new_code = uuid.uuid4()
        await role_bus_obj.load_from_obj_instance(new_role)
        role_bus_obj.code = new_code
        await role_bus_obj.save()
        new_role_role_id_value = new_role.role_id
        new_role = await role_manager.get_by_id(new_role_role_id_value)
        assert role_manager.is_equal(
            role_bus_obj.role,
            new_role) is True
    @pytest.mark.asyncio
    async def test_delete_role(
        self,
        role_manager: RoleManager,
        role_bus_obj: RoleBusObj,
        new_role: Role
    ):
        """
        Test case for deleting a role.
        """
        assert new_role.role_id is not None
        assert role_bus_obj.role_id == 0
        new_role_role_id_value = new_role.role_id
        await role_bus_obj.load_from_id(new_role_role_id_value)
        assert role_bus_obj.role_id is not None
        await role_bus_obj.delete()
        new_role_role_id_value = new_role.role_id
        new_role = await role_manager.get_by_id(new_role_role_id_value)
        assert new_role is None

