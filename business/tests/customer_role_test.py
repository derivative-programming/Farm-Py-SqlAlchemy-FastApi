import pytest
import pytest_asyncio
from datetime import datetime, date
from sqlalchemy.ext.asyncio import AsyncSession
from helpers.session_context import SessionContext
from models import CustomerRole
from models.factory import CustomerRoleFactory
from managers.customer_role import CustomerRoleManager
from business.customer_role import CustomerRoleBusObj
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
class TestCustomerRoleBusObj:
    @pytest_asyncio.fixture(scope="function")
    async def customer_role_manager(self, session:AsyncSession):
        session_context = SessionContext(dict(),session)
        return CustomerRoleManager(session_context)
    @pytest_asyncio.fixture(scope="function")
    async def customer_role_bus_obj(self, session):
        session_context = SessionContext(dict(),session)
        return CustomerRoleBusObj(session_context)
    @pytest_asyncio.fixture(scope="function")
    async def new_customer_role(self, session):
        # Use the CustomerRoleFactory to create a new customer_role instance
        # Assuming CustomerRoleFactory.create() is an async function
        return await CustomerRoleFactory.create_async(session)
    @pytest.mark.asyncio
    async def test_create_customer_role(self, customer_role_manager:CustomerRoleManager, customer_role_bus_obj:CustomerRoleBusObj, new_customer_role:CustomerRole):
        # Test creating a new customer_role
        assert customer_role_bus_obj.customer_role_id is None
        # assert isinstance(customer_role_bus_obj.customer_role_id, int)
        if db_dialect == 'postgresql':
            assert isinstance(customer_role_bus_obj.code, UUID)
        elif db_dialect == 'mssql':
            assert isinstance(customer_role_bus_obj.code, UNIQUEIDENTIFIER)
        else:  # This will cover SQLite, MySQL, and other databases
            assert isinstance(customer_role_bus_obj.code, str)
        assert isinstance(customer_role_bus_obj.last_change_code, int)
        assert customer_role_bus_obj.insert_user_id is None
        assert customer_role_bus_obj.last_update_user_id is None
        assert isinstance(customer_role_bus_obj.customer_id, int)
        assert isinstance(customer_role_bus_obj.is_placeholder, bool)
        assert isinstance(customer_role_bus_obj.placeholder, bool)
        assert isinstance(customer_role_bus_obj.role_id, int)
    @pytest.mark.asyncio
    async def test_load_with_customer_role_obj(self, customer_role_manager:CustomerRoleManager, customer_role_bus_obj:CustomerRoleBusObj, new_customer_role:CustomerRole):
        await customer_role_bus_obj.load(customer_role_obj_instance=new_customer_role)
        assert customer_role_manager.is_equal(customer_role_bus_obj.customer_role,new_customer_role) == True
    @pytest.mark.asyncio
    async def test_load_with_customer_role_id(self, customer_role_manager:CustomerRoleManager, customer_role_bus_obj:CustomerRoleBusObj, new_customer_role:CustomerRole):
        await customer_role_bus_obj.load(customer_role_id=new_customer_role.customer_role_id)
        assert customer_role_manager.is_equal(customer_role_bus_obj.customer_role,new_customer_role)  == True
    @pytest.mark.asyncio
    async def test_load_with_customer_role_code(self, customer_role_manager:CustomerRoleManager, customer_role_bus_obj:CustomerRoleBusObj, new_customer_role:CustomerRole):
        await customer_role_bus_obj.load(code=new_customer_role.code)
        assert customer_role_manager.is_equal(customer_role_bus_obj.customer_role,new_customer_role)  == True
    @pytest.mark.asyncio
    async def test_load_with_customer_role_json(self, customer_role_manager:CustomerRoleManager, customer_role_bus_obj:CustomerRoleBusObj, new_customer_role:CustomerRole):
        customer_role_json = customer_role_manager.to_json(new_customer_role)
        await customer_role_bus_obj.load(json_data=customer_role_json)
        assert customer_role_manager.is_equal(customer_role_bus_obj.customer_role,new_customer_role)  == True
    @pytest.mark.asyncio
    async def test_load_with_customer_role_dict(self, session, customer_role_manager:CustomerRoleManager, customer_role_bus_obj:CustomerRoleBusObj, new_customer_role:CustomerRole):
        logger.info("test_load_with_customer_role_dict 1")
        customer_role_dict = customer_role_manager.to_dict(new_customer_role)
        logger.info(customer_role_dict)
        await customer_role_bus_obj.load(customer_role_dict=customer_role_dict)
        assert customer_role_manager.is_equal(customer_role_bus_obj.customer_role,new_customer_role)  == True
    @pytest.mark.asyncio
    async def test_get_nonexistent_customer_role(self, customer_role_manager:CustomerRoleManager, customer_role_bus_obj:CustomerRoleBusObj, new_customer_role:CustomerRole):
        # Test retrieving a nonexistent customer_role raises an exception
        await customer_role_bus_obj.load(customer_role_id=-1)
        assert customer_role_bus_obj.is_valid() == False # Assuming -1 is an id that wouldn't exist
    @pytest.mark.asyncio
    async def test_update_customer_role(self, customer_role_manager:CustomerRoleManager, customer_role_bus_obj:CustomerRoleBusObj, new_customer_role:CustomerRole):
        # Test updating a customer_role's data
        new_customer_role = await customer_role_manager.get_by_id(new_customer_role.customer_role_id)
        new_code = generate_uuid()
        await customer_role_bus_obj.load(customer_role_obj_instance=new_customer_role)
        customer_role_bus_obj.code = new_code
        await customer_role_bus_obj.save()
        new_customer_role = await customer_role_manager.get_by_id(new_customer_role.customer_role_id)
        assert customer_role_manager.is_equal(customer_role_bus_obj.customer_role,new_customer_role)  == True
    @pytest.mark.asyncio
    async def test_delete_customer_role(self, customer_role_manager:CustomerRoleManager, customer_role_bus_obj:CustomerRoleBusObj, new_customer_role:CustomerRole):
        assert new_customer_role.customer_role_id is not None
        assert customer_role_bus_obj.customer_role_id is None
        await customer_role_bus_obj.load(customer_role_id=new_customer_role.customer_role_id)
        assert customer_role_bus_obj.customer_role_id is not None
        await customer_role_bus_obj.delete()
        new_customer_role = await customer_role_manager.get_by_id(new_customer_role.customer_role_id)
        assert new_customer_role is None

