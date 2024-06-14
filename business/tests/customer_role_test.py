# business/tests/customer_role_test.py
"""
    #TODO add comment
"""
import uuid
from datetime import datetime, date
from sqlalchemy.ext.asyncio import AsyncSession
import pytest
import pytest_asyncio
from helpers.session_context import SessionContext
from models import CustomerRole
from models.factory import CustomerRoleFactory
from managers.customer_role import CustomerRoleManager
from business.customer_role import CustomerRoleBusObj
from services.logging_config import get_logger
import managers as managers_and_enums
import current_runtime

logger = get_logger(__name__)
class TestCustomerRoleBusObj:
    """
        #TODO add comment
    """
    @pytest_asyncio.fixture(scope="function")
    async def customer_role_manager(self, session: AsyncSession):
        """
            #TODO add comment
        """
        session_context = SessionContext(dict(), session)
        return CustomerRoleManager(session_context)
    @pytest_asyncio.fixture(scope="function")
    async def customer_role_bus_obj(self, session):
        """
            #TODO add comment
        """
        session_context = SessionContext(dict(), session)
        return CustomerRoleBusObj(session_context)
    @pytest_asyncio.fixture(scope="function")
    async def new_customer_role(self, session):
        """
            #TODO add comment
        """
        # Use the CustomerRoleFactory to create a new customer_role instance
        # Assuming CustomerRoleFactory.create() is an async function
        return await CustomerRoleFactory.create_async(session)
    @pytest.mark.asyncio
    async def test_create_customer_role(
        self,
        customer_role_bus_obj: CustomerRoleBusObj
    ):
        """
            #TODO add comment
        """
        # Test creating a new customer_role
        assert customer_role_bus_obj.customer_role_id is None
        # assert isinstance(customer_role_bus_obj.customer_role_id, int)
        assert isinstance(customer_role_bus_obj.code, uuid.UUID)
        assert isinstance(customer_role_bus_obj.last_change_code, int)
        assert customer_role_bus_obj.insert_user_id == uuid.UUID(int=0)
        assert customer_role_bus_obj.last_update_user_id == uuid.UUID(int=0)
        assert isinstance(customer_role_bus_obj.customer_id, int)
        assert isinstance(customer_role_bus_obj.is_placeholder, bool)
        assert isinstance(customer_role_bus_obj.placeholder, bool)
        assert isinstance(customer_role_bus_obj.role_id, int)
    @pytest.mark.asyncio
    async def test_load_with_customer_role_obj(
        self,
        customer_role_manager: CustomerRoleManager,
        customer_role_bus_obj: CustomerRoleBusObj,
        new_customer_role: CustomerRole
    ):
        """
            #TODO add comment
        """
        await customer_role_bus_obj.load_from_obj_instance(new_customer_role)
        assert customer_role_manager.is_equal(customer_role_bus_obj.customer_role, new_customer_role) is True
    @pytest.mark.asyncio
    async def test_load_with_customer_role_id(
        self,
        customer_role_manager: CustomerRoleManager,
        customer_role_bus_obj: CustomerRoleBusObj,
        new_customer_role: CustomerRole
    ):
        """
            #TODO add comment
        """
        new_customer_role_customer_role_id = new_customer_role.customer_role_id
        await customer_role_bus_obj.load_from_id(new_customer_role_customer_role_id)
        assert customer_role_manager.is_equal(customer_role_bus_obj.customer_role, new_customer_role) is True
    @pytest.mark.asyncio
    async def test_load_with_customer_role_code(
        self,
        customer_role_manager: CustomerRoleManager,
        customer_role_bus_obj: CustomerRoleBusObj,
        new_customer_role: CustomerRole
    ):
        """
            #TODO add comment
        """
        await customer_role_bus_obj.load_from_code(new_customer_role.code)
        assert customer_role_manager.is_equal(customer_role_bus_obj.customer_role, new_customer_role) is True
    @pytest.mark.asyncio
    async def test_load_with_customer_role_json(
        self,
        customer_role_manager: CustomerRoleManager,
        customer_role_bus_obj: CustomerRoleBusObj,
        new_customer_role: CustomerRole
    ):
        """
            #TODO add comment
        """
        customer_role_json = customer_role_manager.to_json(new_customer_role)
        await customer_role_bus_obj.load_from_json(customer_role_json)
        assert customer_role_manager.is_equal(customer_role_bus_obj.customer_role, new_customer_role) is True
    @pytest.mark.asyncio
    async def test_load_with_customer_role_dict(
        self,
        customer_role_manager: CustomerRoleManager,
        customer_role_bus_obj: CustomerRoleBusObj,
        new_customer_role: CustomerRole
    ):
        """
            #TODO add comment
        """
        logger.info("test_load_with_customer_role_dict 1")
        customer_role_dict = customer_role_manager.to_dict(new_customer_role)
        logger.info(customer_role_dict)
        await customer_role_bus_obj.load_from_dict(customer_role_dict)
        assert customer_role_manager.is_equal(
            customer_role_bus_obj.customer_role,
            new_customer_role) is True
    @pytest.mark.asyncio
    async def test_get_nonexistent_customer_role(
        self,
        customer_role_bus_obj: CustomerRoleBusObj
    ):
        """
            #TODO add comment
        """
        # Test retrieving a nonexistent customer_role raises an exception
        await customer_role_bus_obj.load_from_id(-1)
        assert customer_role_bus_obj.is_valid() is False  # Assuming -1 is an id that wouldn't exist
    @pytest.mark.asyncio
    async def test_update_customer_role(
        self,
        customer_role_manager: CustomerRoleManager,
        customer_role_bus_obj: CustomerRoleBusObj,
        new_customer_role: CustomerRole
    ):
        """
            #TODO add comment
        """
        # Test updating a customer_role's data
        new_customer_role_customer_role_id_value = new_customer_role.customer_role_id
        new_customer_role = await customer_role_manager.get_by_id(new_customer_role_customer_role_id_value)
        assert isinstance(new_customer_role, CustomerRole)
        new_code = uuid.uuid4()
        await customer_role_bus_obj.load_from_obj_instance(new_customer_role)
        customer_role_bus_obj.code = new_code
        await customer_role_bus_obj.save()
        new_customer_role_customer_role_id_value = new_customer_role.customer_role_id
        new_customer_role = await customer_role_manager.get_by_id(new_customer_role_customer_role_id_value)
        assert customer_role_manager.is_equal(
            customer_role_bus_obj.customer_role,
            new_customer_role) is True
    @pytest.mark.asyncio
    async def test_delete_customer_role(
        self,
        customer_role_manager: CustomerRoleManager,
        customer_role_bus_obj: CustomerRoleBusObj,
        new_customer_role: CustomerRole
    ):
        """
            #TODO add comment
        """
        assert new_customer_role.customer_role_id is not None
        assert customer_role_bus_obj.customer_role_id is None
        new_customer_role_customer_role_id_value = new_customer_role.customer_role_id
        await customer_role_bus_obj.load_from_id(new_customer_role_customer_role_id_value)
        assert customer_role_bus_obj.customer_role_id is not None
        await customer_role_bus_obj.delete()
        new_customer_role_customer_role_id_value = new_customer_role.customer_role_id
        new_customer_role = await customer_role_manager.get_by_id(new_customer_role_customer_role_id_value)
        assert new_customer_role is None

