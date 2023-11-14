import pytest
import pytest_asyncio
from datetime import datetime, date
from sqlalchemy.ext.asyncio import AsyncSession
from models import Role
from models.factory import RoleFactory
from managers.role import RoleManager
from business.role import RoleBusObj
from services.db_config import db_dialect
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
from services.db_config import db_dialect,generate_uuid
from sqlalchemy import String
from services.logging_config import get_logger
import managers as managers_and_enums
import current_runtime

logger = get_logger(__name__)
db_dialect = "sqlite"
# Conditionally set the UUID column type
if db_dialect == 'postgresql':
    UUIDType = UUID(as_uuid=True)
elif db_dialect == 'mssql':
    UUIDType = UNIQUEIDENTIFIER
else:  # This will cover SQLite, MySQL, and other databases
    UUIDType = String(36)
class TestRoleBusObj:
    @pytest_asyncio.fixture(scope="function")
    async def role_manager(self, session:AsyncSession):
        return RoleManager(session)
    @pytest_asyncio.fixture(scope="function")
    async def role_bus_obj(self, session):
        # Assuming that the RoleBusObj requires a session object
        return RoleBusObj(session)
    @pytest_asyncio.fixture(scope="function")
    async def new_role(self, session):
        # Use the RoleFactory to create a new role instance
        # Assuming RoleFactory.create() is an async function
        return await RoleFactory.create_async(session)
    @pytest.mark.asyncio
    async def test_create_role(self, role_manager:RoleManager, role_bus_obj:RoleBusObj, new_role:Role):
        # Test creating a new role
        assert role_bus_obj.role_id is None
        # assert isinstance(role_bus_obj.role_id, int)
        if db_dialect == 'postgresql':
            assert isinstance(role_bus_obj.code, UUID)
        elif db_dialect == 'mssql':
            assert isinstance(role_bus_obj.code, UNIQUEIDENTIFIER)
        else:  # This will cover SQLite, MySQL, and other databases
            assert isinstance(role_bus_obj.code, str)
        assert isinstance(role_bus_obj.last_change_code, int)
        assert role_bus_obj.insert_user_id is None
        assert role_bus_obj.last_update_user_id is None
        assert role_bus_obj.description == "" or isinstance(role_bus_obj.description, str)
        assert isinstance(role_bus_obj.display_order, int)
        assert isinstance(role_bus_obj.is_active, bool)
        assert role_bus_obj.lookup_enum_name == "" or isinstance(role_bus_obj.lookup_enum_name, str)
        assert role_bus_obj.name == "" or isinstance(role_bus_obj.name, str)
        assert isinstance(role_bus_obj.pac_id, int)
    @pytest.mark.asyncio
    async def test_load_with_role_obj(self, role_manager:RoleManager, role_bus_obj:RoleBusObj, new_role:Role):
        await role_bus_obj.load(role_obj_instance=new_role)
        assert role_manager.is_equal(role_bus_obj.role,new_role) == True
    @pytest.mark.asyncio
    async def test_load_with_role_id(self, role_manager:RoleManager, role_bus_obj:RoleBusObj, new_role:Role):
        await role_bus_obj.load(role_id=new_role.role_id)
        assert role_manager.is_equal(role_bus_obj.role,new_role)  == True
    @pytest.mark.asyncio
    async def test_load_with_role_code(self, role_manager:RoleManager, role_bus_obj:RoleBusObj, new_role:Role):
        await role_bus_obj.load(code=new_role.code)
        assert role_manager.is_equal(role_bus_obj.role,new_role)  == True
    @pytest.mark.asyncio
    async def test_load_with_role_json(self, role_manager:RoleManager, role_bus_obj:RoleBusObj, new_role:Role):
        role_json = role_manager.to_json(new_role)
        await role_bus_obj.load(json_data=role_json)
        assert role_manager.is_equal(role_bus_obj.role,new_role)  == True
    @pytest.mark.asyncio
    async def test_load_with_role_dict(self, session, role_manager:RoleManager, role_bus_obj:RoleBusObj, new_role:Role):
        logger.info("test_load_with_role_dict 1")
        role_dict = role_manager.to_dict(new_role)
        logger.info(role_dict)
        await role_bus_obj.load(role_dict=role_dict)
        assert role_manager.is_equal(role_bus_obj.role,new_role)  == True
    @pytest.mark.asyncio
    async def test_get_nonexistent_role(self, role_manager:RoleManager, role_bus_obj:RoleBusObj, new_role:Role):
        # Test retrieving a nonexistent role raises an exception
        assert await role_bus_obj.load(role_id=-1) is None # Assuming -1 is an id that wouldn't exist
    @pytest.mark.asyncio
    async def test_update_role(self, role_manager:RoleManager, role_bus_obj:RoleBusObj, new_role:Role):
        # Test updating a role's data
        new_role = await role_manager.get_by_id(new_role.role_id)
        new_code = generate_uuid()
        await role_bus_obj.load(role_obj_instance=new_role)
        role_bus_obj.code = new_code
        await role_bus_obj.save()
        new_role = await role_manager.get_by_id(new_role.role_id)
        assert role_manager.is_equal(role_bus_obj.role,new_role)  == True
    @pytest.mark.asyncio
    async def test_delete_role(self, role_manager:RoleManager, role_bus_obj:RoleBusObj, new_role:Role):
        assert new_role.role_id is not None
        assert role_bus_obj.role_id is None
        await role_bus_obj.load(role_id=new_role.role_id)
        assert role_bus_obj.role_id is not None
        await role_bus_obj.delete()
        new_role = await role_manager.get_by_id(new_role.role_id)
        assert new_role is None

