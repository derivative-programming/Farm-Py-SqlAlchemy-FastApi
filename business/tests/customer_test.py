# business/tests/customer_test.py
"""
    #TODO add comment
"""
import uuid
from datetime import datetime, date  # pylint: disable=unused-import
from sqlalchemy.ext.asyncio import AsyncSession
import pytest
import pytest_asyncio
from helpers.session_context import SessionContext
from models import Customer
from models.factory import CustomerFactory
from managers.customer import CustomerManager
from business.customer import CustomerBusObj
from services.logging_config import get_logger
import current_runtime  # pylint: disable=unused-import

logger = get_logger(__name__)
class TestCustomerBusObj:
    """
        #TODO add comment
    """
    @pytest_asyncio.fixture(scope="function")
    async def customer_manager(self, session: AsyncSession):
        """
            #TODO add comment
        """
        session_context = SessionContext(dict(), session)
        return CustomerManager(session_context)
    @pytest_asyncio.fixture(scope="function")
    async def customer_bus_obj(self, session):
        """
            #TODO add comment
        """
        session_context = SessionContext(dict(), session)
        return CustomerBusObj(session_context)
    @pytest_asyncio.fixture(scope="function")
    async def new_customer(self, session):
        """
            #TODO add comment
        """
        # Use the CustomerFactory to create a new customer instance
        # Assuming CustomerFactory.create() is an async function
        return await CustomerFactory.create_async(session)
    @pytest.mark.asyncio
    async def test_create_customer(
        self,
        customer_bus_obj: CustomerBusObj
    ):
        """
            #TODO add comment
        """
        # Test creating a new customer
        assert customer_bus_obj.customer_id is None
        # assert isinstance(customer_bus_obj.customer_id, int)
        assert isinstance(customer_bus_obj.code, uuid.UUID)
        assert isinstance(customer_bus_obj.last_change_code, int)
        assert customer_bus_obj.insert_user_id == uuid.UUID(int=0)
        assert customer_bus_obj.last_update_user_id == uuid.UUID(int=0)
        assert isinstance(customer_bus_obj.active_organization_id, int)
        assert isinstance(customer_bus_obj.email, str)
        assert isinstance(customer_bus_obj.email_confirmed_utc_date_time, datetime)
        assert isinstance(customer_bus_obj.first_name, str)
        assert isinstance(customer_bus_obj.forgot_password_key_expiration_utc_date_time, datetime)
        assert isinstance(customer_bus_obj.forgot_password_key_value, str)
        # fs_user_code_value
        assert isinstance(customer_bus_obj.fs_user_code_value, uuid.UUID)
        assert isinstance(customer_bus_obj.is_active, bool)
        assert isinstance(customer_bus_obj.is_email_allowed, bool)
        assert isinstance(customer_bus_obj.is_email_confirmed, bool)
        assert isinstance(customer_bus_obj.is_email_marketing_allowed, bool)
        assert isinstance(customer_bus_obj.is_locked, bool)
        assert isinstance(customer_bus_obj.is_multiple_organizations_allowed, bool)
        assert isinstance(customer_bus_obj.is_verbose_logging_forced, bool)
        assert isinstance(customer_bus_obj.last_login_utc_date_time, datetime)
        assert isinstance(customer_bus_obj.last_name, str)
        assert isinstance(customer_bus_obj.password, str)
        assert isinstance(customer_bus_obj.phone, str)
        assert isinstance(customer_bus_obj.province, str)
        assert isinstance(customer_bus_obj.registration_utc_date_time, datetime)
        assert isinstance(customer_bus_obj.tac_id, int)
        assert isinstance(customer_bus_obj.utc_offset_in_minutes, int)
        assert isinstance(customer_bus_obj.zip, str)
    @pytest.mark.asyncio
    async def test_load_with_customer_obj(
        self,
        customer_manager: CustomerManager,
        customer_bus_obj: CustomerBusObj,
        new_customer: Customer
    ):
        """
            #TODO add comment
        """
        await customer_bus_obj.load_from_obj_instance(new_customer)
        assert customer_manager.is_equal(customer_bus_obj.customer, new_customer) is True
    @pytest.mark.asyncio
    async def test_load_with_customer_id(
        self,
        customer_manager: CustomerManager,
        customer_bus_obj: CustomerBusObj,
        new_customer: Customer
    ):
        """
            #TODO add comment
        """
        new_customer_customer_id = new_customer.customer_id
        await customer_bus_obj.load_from_id(new_customer_customer_id)
        assert customer_manager.is_equal(customer_bus_obj.customer, new_customer) is True
    @pytest.mark.asyncio
    async def test_load_with_customer_code(
        self,
        customer_manager: CustomerManager,
        customer_bus_obj: CustomerBusObj,
        new_customer: Customer
    ):
        """
            #TODO add comment
        """
        await customer_bus_obj.load_from_code(new_customer.code)
        assert customer_manager.is_equal(customer_bus_obj.customer, new_customer) is True
    @pytest.mark.asyncio
    async def test_load_with_customer_json(
        self,
        customer_manager: CustomerManager,
        customer_bus_obj: CustomerBusObj,
        new_customer: Customer
    ):
        """
            #TODO add comment
        """
        customer_json = customer_manager.to_json(new_customer)
        await customer_bus_obj.load_from_json(customer_json)
        assert customer_manager.is_equal(customer_bus_obj.customer, new_customer) is True
    @pytest.mark.asyncio
    async def test_load_with_customer_dict(
        self,
        customer_manager: CustomerManager,
        customer_bus_obj: CustomerBusObj,
        new_customer: Customer
    ):
        """
            #TODO add comment
        """
        logger.info("test_load_with_customer_dict 1")
        customer_dict = customer_manager.to_dict(new_customer)
        logger.info(customer_dict)
        await customer_bus_obj.load_from_dict(customer_dict)
        assert customer_manager.is_equal(
            customer_bus_obj.customer,
            new_customer) is True
    @pytest.mark.asyncio
    async def test_get_nonexistent_customer(
        self,
        customer_bus_obj: CustomerBusObj
    ):
        """
            #TODO add comment
        """
        # Test retrieving a nonexistent customer raises an exception
        await customer_bus_obj.load_from_id(-1)
        assert customer_bus_obj.is_valid() is False  # Assuming -1 is an id that wouldn't exist
    @pytest.mark.asyncio
    async def test_update_customer(
        self,
        customer_manager: CustomerManager,
        customer_bus_obj: CustomerBusObj,
        new_customer: Customer
    ):
        """
            #TODO add comment
        """
        # Test updating a customer's data
        new_customer_customer_id_value = new_customer.customer_id
        new_customer = await customer_manager.get_by_id(new_customer_customer_id_value)
        assert isinstance(new_customer, Customer)
        new_code = uuid.uuid4()
        await customer_bus_obj.load_from_obj_instance(new_customer)
        customer_bus_obj.code = new_code
        await customer_bus_obj.save()
        new_customer_customer_id_value = new_customer.customer_id
        new_customer = await customer_manager.get_by_id(new_customer_customer_id_value)
        assert customer_manager.is_equal(
            customer_bus_obj.customer,
            new_customer) is True
    @pytest.mark.asyncio
    async def test_delete_customer(
        self,
        customer_manager: CustomerManager,
        customer_bus_obj: CustomerBusObj,
        new_customer: Customer
    ):
        """
            #TODO add comment
        """
        assert new_customer.customer_id is not None
        assert customer_bus_obj.customer_id is None
        new_customer_customer_id_value = new_customer.customer_id
        await customer_bus_obj.load_from_id(new_customer_customer_id_value)
        assert customer_bus_obj.customer_id is not None
        await customer_bus_obj.delete()
        new_customer_customer_id_value = new_customer.customer_id
        new_customer = await customer_manager.get_by_id(new_customer_customer_id_value)
        assert new_customer is None

    @pytest.mark.asyncio
    async def test_build_customer_role(
        self,
        customer_bus_obj: CustomerBusObj,
        new_customer: Customer,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """

        session_context = SessionContext(dict(), session)

        await current_runtime.initialize(session_context)

        await customer_bus_obj.load_from_id(
            new_customer.customer_id
        )

        customer_role_bus_obj = await customer_bus_obj.build_customer_role()

        assert customer_role_bus_obj.customer_id == customer_bus_obj.customer_id
        assert customer_role_bus_obj.customer_code_peek == customer_bus_obj.code

        await customer_role_bus_obj.save()

        assert customer_role_bus_obj.customer_role_id > 0

    @pytest.mark.asyncio
    async def test_get_all_customer_role(
        self,
        customer_bus_obj: CustomerBusObj,
        new_customer: Customer,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """

        session_context = SessionContext(dict(), session)

        await current_runtime.initialize(session_context)

        new_customer_customer_id = (
            new_customer.customer_id
        )

        await customer_bus_obj.load_from_id(
            new_customer_customer_id
        )

        customer_role_bus_obj = await customer_bus_obj.build_customer_role()

        await customer_role_bus_obj.save()

        customer_role_list = await customer_bus_obj.get_all_customer_role()

        assert len(customer_role_list) >= 1

        #assert customer_role_list[0].customer_role_id > 0

        #assert customer_role_list[0].customer_role_id == customer_role_bus_obj.customer_role_id

