# business/tests/role_test.py
"""
    #TODO add comment
"""
from datetime import datetime, date
from sqlalchemy.ext.asyncio import AsyncSession
import pytest
import pytest_asyncio
from helpers.session_context import SessionContext
from models import Role
from models.factory import RoleFactory
from managers.role import RoleManager
from business.role import RoleBusObj
from services.logging_config import get_logger
import managers as managers_and_enums
import current_runtime

logger = get_logger(__name__)
class TestRoleBusObj:
    """
        #TODO add comment
    """
    @pytest_asyncio.fixture(scope="function")
    async def role_manager(self, session: AsyncSession):
        """
            #TODO add comment
        """
        session_context = SessionContext(dict(), session)
        return RoleManager(session_context)
    @pytest_asyncio.fixture(scope="function")
    async def role_bus_obj(self, session):
        """
            #TODO add comment
        """
        session_context = SessionContext(dict(), session)
        return RoleBusObj(session_context)
    @pytest_asyncio.fixture(scope="function")
    async def new_role(self, session):
        """
            #TODO add comment
        """
        # Use the RoleFactory to create a new role instance
        # Assuming RoleFactory.create() is an async function
        return await RoleFactory.create_async(session)
    @pytest.mark.asyncio
    async def test_create_role(
        self,
        role_manager: RoleManager,
        role_bus_obj: RoleBusObj,
        new_role: Role
    ):
        """
            #TODO add comment
        """
        # Test creating a new role
        assert role_bus_obj.role_id is None
        # assert isinstance(role_bus_obj.role_id, int)
        assert isinstance(role_bus_obj.code, UUID)
        assert isinstance(role_bus_obj.last_change_code, int)
        assert role_bus_obj.insert_user_id is None
        assert role_bus_obj.last_update_user_id is None
        assert role_bus_obj.description == "" or isinstance(
            role_bus_obj.description, str)
        assert isinstance(role_bus_obj.display_order, int)
        assert isinstance(role_bus_obj.is_active, bool)
        assert role_bus_obj.lookup_enum_name == "" or isinstance(
            role_bus_obj.lookup_enum_name, str)
        assert role_bus_obj.name == "" or isinstance(
            role_bus_obj.name, str)
        assert isinstance(role_bus_obj.pac_id, int)
    @pytest.mark.asyncio
    async def test_load_with_role_obj(
        self,
        role_manager: RoleManager,
        role_bus_obj: RoleBusObj,
        new_role: Role
    ):
        """
            #TODO add comment
        """
        await role_bus_obj.load(role_obj_instance=new_role)
        assert role_manager.is_equal(role_bus_obj.role, new_role) is True
    @pytest.mark.asyncio
    async def test_load_with_role_id(
        self,
        role_manager: RoleManager,
        role_bus_obj: RoleBusObj,
        new_role: Role
    ):
        """
            #TODO add comment
        """
        await role_bus_obj.load(role_id=new_role.role_id)
        assert role_manager.is_equal(role_bus_obj.role, new_role) is True
    @pytest.mark.asyncio
    async def test_load_with_role_code(
        self,
        role_manager: RoleManager,
        role_bus_obj: RoleBusObj,
        new_role: Role
    ):
        """
            #TODO add comment
        """
        await role_bus_obj.load(code=new_role.code)
        assert role_manager.is_equal(role_bus_obj.role, new_role) is True
    @pytest.mark.asyncio
    async def test_load_with_role_json(
        self,
        role_manager: RoleManager,
        role_bus_obj: RoleBusObj,
        new_role: Role
    ):
        """
            #TODO add comment
        """
        role_json = role_manager.to_json(new_role)
        await role_bus_obj.load(json_data=role_json)
        assert role_manager.is_equal(role_bus_obj.role, new_role) is True
    @pytest.mark.asyncio
    async def test_load_with_role_dict(
        self,
        role_manager: RoleManager,
        role_bus_obj: RoleBusObj,
        new_role: Role
    ):
        """
            #TODO add comment
        """
        logger.info("test_load_with_role_dict 1")
        role_dict = role_manager.to_dict(new_role)
        logger.info(role_dict)
        await role_bus_obj.load(role_dict=role_dict)
        assert role_manager.is_equal(
            role_bus_obj.role,
            new_role) is True
    @pytest.mark.asyncio
    async def test_get_nonexistent_role(
        self,
        role_manager: RoleManager,
        role_bus_obj: RoleBusObj,
        new_role: Role
    ):
        """
            #TODO add comment
        """
        # Test retrieving a nonexistent role raises an exception
        await role_bus_obj.load(role_id=-1)
        assert role_bus_obj.is_valid() is False  # Assuming -1 is an id that wouldn't exist
    @pytest.mark.asyncio
    async def test_update_role(
        self,
        role_manager: RoleManager,
        role_bus_obj: RoleBusObj,
        new_role: Role
    ):
        """
            #TODO add comment
        """
        # Test updating a role's data
        new_role = await role_manager.get_by_id(new_role.role_id)
        new_code = uuid.uuid4()
        await role_bus_obj.load(role_obj_instance=new_role)
        role_bus_obj.code = new_code
        await role_bus_obj.save()
        new_role = await role_manager.get_by_id(new_role.role_id)
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
            #TODO add comment
        """
        assert new_role.role_id is not None
        assert role_bus_obj.role_id is None
        await role_bus_obj.load(role_id=new_role.role_id)
        assert role_bus_obj.role_id is not None
        await role_bus_obj.delete()
        new_role = await role_manager.get_by_id(new_role.role_id)
        assert new_role is None

