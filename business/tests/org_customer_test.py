# business/tests/org_customer_test.py
"""
    #TODO add comment
"""
import pytest
import pytest_asyncio
from datetime import datetime, date
from sqlalchemy.ext.asyncio import AsyncSession
from helpers.session_context import SessionContext
from models import OrgCustomer
from models.factory import OrgCustomerFactory
from managers.org_customer import OrgCustomerManager
from business.org_customer import OrgCustomerBusObj
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
class TestOrgCustomerBusObj:
    """
        #TODO add comment
    """
    @pytest_asyncio.fixture(scope="function")
    async def org_customer_manager(self, session: AsyncSession):
        """
            #TODO add comment
        """
        session_context = SessionContext(dict(), session)
        return OrgCustomerManager(session_context)
    @pytest_asyncio.fixture(scope="function")
    async def org_customer_bus_obj(self, session):
        """
            #TODO add comment
        """
        session_context = SessionContext(dict(), session)
        return OrgCustomerBusObj(session_context)
    @pytest_asyncio.fixture(scope="function")
    async def new_org_customer(self, session):
        """
            #TODO add comment
        """
        # Use the OrgCustomerFactory to create a new org_customer instance
        # Assuming OrgCustomerFactory.create() is an async function
        return await OrgCustomerFactory.create_async(session)
    @pytest.mark.asyncio
    async def test_create_org_customer(
        self,
        org_customer_manager: OrgCustomerManager,
        org_customer_bus_obj: OrgCustomerBusObj,
        new_org_customer: OrgCustomer
    ):
        """
            #TODO add comment
        """
        # Test creating a new org_customer
        assert org_customer_bus_obj.org_customer_id is None
        # assert isinstance(org_customer_bus_obj.org_customer_id, int)
        if DB_DIALECT == 'postgresql':
            assert isinstance(org_customer_bus_obj.code, UUID)
        elif DB_DIALECT == 'mssql':
            assert isinstance(org_customer_bus_obj.code, UNIQUEIDENTIFIER)
        else:  # This will cover SQLite, MySQL, and other databases
            assert isinstance(org_customer_bus_obj.code, str)
        assert isinstance(org_customer_bus_obj.last_change_code, int)
        assert org_customer_bus_obj.insert_user_id is None
        assert org_customer_bus_obj.last_update_user_id is None
        assert isinstance(org_customer_bus_obj.customer_id, int)
        assert org_customer_bus_obj.email == "" or isinstance(
            org_customer_bus_obj.email, str)
        assert isinstance(org_customer_bus_obj.organization_id, int)
    @pytest.mark.asyncio
    async def test_load_with_org_customer_obj(
        self,
        org_customer_manager: OrgCustomerManager,
        org_customer_bus_obj: OrgCustomerBusObj,
        new_org_customer: OrgCustomer
    ):
        """
            #TODO add comment
        """
        await org_customer_bus_obj.load(org_customer_obj_instance=new_org_customer)
        assert org_customer_manager.is_equal(org_customer_bus_obj.org_customer, new_org_customer) is True
    @pytest.mark.asyncio
    async def test_load_with_org_customer_id(
        self,
        org_customer_manager: OrgCustomerManager,
        org_customer_bus_obj: OrgCustomerBusObj,
        new_org_customer: OrgCustomer
    ):
        """
            #TODO add comment
        """
        await org_customer_bus_obj.load(org_customer_id=new_org_customer.org_customer_id)
        assert org_customer_manager.is_equal(org_customer_bus_obj.org_customer, new_org_customer) is True
    @pytest.mark.asyncio
    async def test_load_with_org_customer_code(
        self,
        org_customer_manager: OrgCustomerManager,
        org_customer_bus_obj: OrgCustomerBusObj,
        new_org_customer: OrgCustomer
    ):
        """
            #TODO add comment
        """
        await org_customer_bus_obj.load(code=new_org_customer.code)
        assert org_customer_manager.is_equal(org_customer_bus_obj.org_customer, new_org_customer) is True
    @pytest.mark.asyncio
    async def test_load_with_org_customer_json(
        self,
        org_customer_manager: OrgCustomerManager,
        org_customer_bus_obj: OrgCustomerBusObj,
        new_org_customer: OrgCustomer
    ):
        """
            #TODO add comment
        """
        org_customer_json = org_customer_manager.to_json(new_org_customer)
        await org_customer_bus_obj.load(json_data=org_customer_json)
        assert org_customer_manager.is_equal(org_customer_bus_obj.org_customer, new_org_customer) is True
    @pytest.mark.asyncio
    async def test_load_with_org_customer_dict(
        self,
        org_customer_manager: OrgCustomerManager,
        org_customer_bus_obj: OrgCustomerBusObj,
        new_org_customer: OrgCustomer
    ):
        """
            #TODO add comment
        """
        logger.info("test_load_with_org_customer_dict 1")
        org_customer_dict = org_customer_manager.to_dict(new_org_customer)
        logger.info(org_customer_dict)
        await org_customer_bus_obj.load(org_customer_dict=org_customer_dict)
        assert org_customer_manager.is_equal(
            org_customer_bus_obj.org_customer,
            new_org_customer) is True
    @pytest.mark.asyncio
    async def test_get_nonexistent_org_customer(
        self,
        org_customer_manager: OrgCustomerManager,
        org_customer_bus_obj: OrgCustomerBusObj,
        new_org_customer: OrgCustomer
    ):
        """
            #TODO add comment
        """
        # Test retrieving a nonexistent org_customer raises an exception
        await org_customer_bus_obj.load(org_customer_id=-1)
        assert org_customer_bus_obj.is_valid() is False  # Assuming -1 is an id that wouldn't exist
    @pytest.mark.asyncio
    async def test_update_org_customer(
        self,
        org_customer_manager: OrgCustomerManager,
        org_customer_bus_obj: OrgCustomerBusObj,
        new_org_customer: OrgCustomer
    ):
        """
            #TODO add comment
        """
        # Test updating a org_customer's data
        new_org_customer = await org_customer_manager.get_by_id(new_org_customer.org_customer_id)
        new_code = generate_uuid()
        await org_customer_bus_obj.load(org_customer_obj_instance=new_org_customer)
        org_customer_bus_obj.code = new_code
        await org_customer_bus_obj.save()
        new_org_customer = await org_customer_manager.get_by_id(new_org_customer.org_customer_id)
        assert org_customer_manager.is_equal(
            org_customer_bus_obj.org_customer,
            new_org_customer) is True
    @pytest.mark.asyncio
    async def test_delete_org_customer(
        self,
        org_customer_manager: OrgCustomerManager,
        org_customer_bus_obj: OrgCustomerBusObj,
        new_org_customer: OrgCustomer
    ):
        """
            #TODO add comment
        """
        assert new_org_customer.org_customer_id is not None
        assert org_customer_bus_obj.org_customer_id is None
        await org_customer_bus_obj.load(org_customer_id=new_org_customer.org_customer_id)
        assert org_customer_bus_obj.org_customer_id is not None
        await org_customer_bus_obj.delete()
        new_org_customer = await org_customer_manager.get_by_id(new_org_customer.org_customer_id)
        assert new_org_customer is None

