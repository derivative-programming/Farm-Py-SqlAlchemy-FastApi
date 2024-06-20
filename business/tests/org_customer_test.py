# business/tests/org_customer_test.py
# pylint: disable=unused-import
"""
This module contains unit tests for the OrgCustomerBusObj class.
"""
from decimal import Decimal
import uuid
from datetime import datetime, date  # noqa: F401
from sqlalchemy.ext.asyncio import AsyncSession
import pytest
import pytest_asyncio
from helpers.session_context import SessionContext
from models import OrgCustomer
from models.factory import OrgCustomerFactory
from managers.org_customer import OrgCustomerManager
from business.org_customer import OrgCustomerBusObj
from services.logging_config import get_logger
import current_runtime  # noqa: F401

logger = get_logger(__name__)
class TestOrgCustomerBusObj:
    """
    Unit tests for the OrgCustomerBusObj class.
    """
    @pytest_asyncio.fixture(scope="function")
    async def org_customer_manager(self, session: AsyncSession):
        """
        Fixture that returns an instance of the OrgCustomerManager class.
        """
        session_context = SessionContext(dict(), session)
        return OrgCustomerManager(session_context)
    @pytest_asyncio.fixture(scope="function")
    async def org_customer_bus_obj(self, session):
        """
        Fixture that returns an instance of the OrgCustomerBusObj class.
        """
        session_context = SessionContext(dict(), session)
        return OrgCustomerBusObj(session_context)
    @pytest_asyncio.fixture(scope="function")
    async def new_org_customer(self, session):
        """
        Fixture that returns a new instance of the OrgCustomer class.
        """
        # Use the OrgCustomerFactory to create a new org_customer instance
        # Assuming OrgCustomerFactory.create() is an async function
        return await OrgCustomerFactory.create_async(session)
    @pytest.mark.asyncio
    async def test_create_org_customer(
        self,
        org_customer_bus_obj: OrgCustomerBusObj
    ):
        """
        Test case for creating a new org_customer.
        """
        # Test creating a new org_customer
        assert org_customer_bus_obj.org_customer_id == 0
        # assert isinstance(org_customer_bus_obj.org_customer_id, int)
        assert isinstance(org_customer_bus_obj.code, uuid.UUID)
        assert isinstance(org_customer_bus_obj.last_change_code, int)
        assert org_customer_bus_obj.insert_user_id == uuid.UUID(int=0)
        assert org_customer_bus_obj.last_update_user_id == uuid.UUID(int=0)
        assert isinstance(org_customer_bus_obj.customer_id, int)
        assert isinstance(org_customer_bus_obj.email, str)
        assert isinstance(org_customer_bus_obj.organization_id, int)
    @pytest.mark.asyncio
    async def test_load_with_org_customer_obj(
        self,
        org_customer_manager: OrgCustomerManager,
        org_customer_bus_obj: OrgCustomerBusObj,
        new_org_customer: OrgCustomer
    ):
        """
        Test case for loading data from a org_customer object instance.
        """
        await org_customer_bus_obj.load_from_obj_instance(new_org_customer)
        assert org_customer_manager.is_equal(org_customer_bus_obj.org_customer, new_org_customer) is True
    @pytest.mark.asyncio
    async def test_load_with_org_customer_id(
        self,
        org_customer_manager: OrgCustomerManager,
        org_customer_bus_obj: OrgCustomerBusObj,
        new_org_customer: OrgCustomer
    ):
        """
        Test case for loading data from a org_customer ID.
        """
        new_org_customer_org_customer_id = new_org_customer.org_customer_id
        await org_customer_bus_obj.load_from_id(new_org_customer_org_customer_id)
        assert org_customer_manager.is_equal(org_customer_bus_obj.org_customer, new_org_customer) is True
    @pytest.mark.asyncio
    async def test_load_with_org_customer_code(
        self,
        org_customer_manager: OrgCustomerManager,
        org_customer_bus_obj: OrgCustomerBusObj,
        new_org_customer: OrgCustomer
    ):
        """
        Test case for loading data from a org_customer code.
        """
        await org_customer_bus_obj.load_from_code(new_org_customer.code)
        assert org_customer_manager.is_equal(org_customer_bus_obj.org_customer, new_org_customer) is True
    @pytest.mark.asyncio
    async def test_load_with_org_customer_json(
        self,
        org_customer_manager: OrgCustomerManager,
        org_customer_bus_obj: OrgCustomerBusObj,
        new_org_customer: OrgCustomer
    ):
        """
        Test case for loading data from a org_customer JSON.
        """
        org_customer_json = org_customer_manager.to_json(new_org_customer)
        await org_customer_bus_obj.load_from_json(org_customer_json)
        assert org_customer_manager.is_equal(org_customer_bus_obj.org_customer, new_org_customer) is True
    @pytest.mark.asyncio
    async def test_load_with_org_customer_dict(
        self,
        org_customer_manager: OrgCustomerManager,
        org_customer_bus_obj: OrgCustomerBusObj,
        new_org_customer: OrgCustomer
    ):
        """
        Test case for loading data from a org_customer dictionary.
        """
        logger.info("test_load_with_org_customer_dict 1")
        org_customer_dict = org_customer_manager.to_dict(new_org_customer)
        logger.info(org_customer_dict)
        await org_customer_bus_obj.load_from_dict(org_customer_dict)
        assert org_customer_manager.is_equal(
            org_customer_bus_obj.org_customer,
            new_org_customer) is True
    @pytest.mark.asyncio
    async def test_get_nonexistent_org_customer(
        self,
        org_customer_bus_obj: OrgCustomerBusObj
    ):
        """
        Test case for retrieving a nonexistent org_customer.
        """
        # Test retrieving a nonexistent org_customer raises an exception
        await org_customer_bus_obj.load_from_id(-1)
        # Assuming -1 is an id that wouldn't exist
        assert org_customer_bus_obj.is_valid() is False
    @pytest.mark.asyncio
    async def test_update_org_customer(
        self,
        org_customer_manager: OrgCustomerManager,
        org_customer_bus_obj: OrgCustomerBusObj,
        new_org_customer: OrgCustomer
    ):
        """
        Test case for updating a org_customer's data.
        """
        # Test updating a org_customer's data
        new_org_customer_org_customer_id_value = new_org_customer.org_customer_id
        new_org_customer = await org_customer_manager.get_by_id(new_org_customer_org_customer_id_value)
        assert isinstance(new_org_customer, OrgCustomer)
        new_code = uuid.uuid4()
        await org_customer_bus_obj.load_from_obj_instance(new_org_customer)
        org_customer_bus_obj.code = new_code
        await org_customer_bus_obj.save()
        new_org_customer_org_customer_id_value = new_org_customer.org_customer_id
        new_org_customer = await org_customer_manager.get_by_id(new_org_customer_org_customer_id_value)
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
        Test case for deleting a org_customer.
        """
        assert new_org_customer.org_customer_id is not None
        assert org_customer_bus_obj.org_customer_id == 0
        new_org_customer_org_customer_id_value = new_org_customer.org_customer_id
        await org_customer_bus_obj.load_from_id(new_org_customer_org_customer_id_value)
        assert org_customer_bus_obj.org_customer_id is not None
        await org_customer_bus_obj.delete()
        new_org_customer_org_customer_id_value = new_org_customer.org_customer_id
        new_org_customer = await org_customer_manager.get_by_id(new_org_customer_org_customer_id_value)
        assert new_org_customer is None

