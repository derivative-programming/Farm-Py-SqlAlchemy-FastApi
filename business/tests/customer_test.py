import pytest
import pytest_asyncio
from datetime import datetime, date
from sqlalchemy.ext.asyncio import AsyncSession
from models import Customer
from models.factory import CustomerFactory
from managers.customer import CustomerManager
from business.customer import CustomerBusObj
from services.db_config import db_dialect
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
from services.db_config import db_dialect,generate_uuid
from sqlalchemy import String
from services.logging_config import get_logger
logger = get_logger(__name__)
db_dialect = "sqlite"
# Conditionally set the UUID column type
if db_dialect == 'postgresql':
    UUIDType = UUID(as_uuid=True)
elif db_dialect == 'mssql':
    UUIDType = UNIQUEIDENTIFIER
else:  # This will cover SQLite, MySQL, and other databases
    UUIDType = String(36)
class TestCustomerBusObj:
    @pytest_asyncio.fixture(scope="function")
    async def customer_manager(self, session:AsyncSession):
        return CustomerManager(session)
    @pytest_asyncio.fixture(scope="function")
    async def customer_bus_obj(self, session):
        # Assuming that the CustomerBusObj requires a session object
        return CustomerBusObj(session)
    @pytest_asyncio.fixture(scope="function")
    async def new_customer(self, session):
        # Use the CustomerFactory to create a new customer instance
        # Assuming CustomerFactory.create() is an async function
        return await CustomerFactory.create_async(session)
    @pytest.mark.asyncio
    async def test_create_customer(self, customer_manager:CustomerManager, customer_bus_obj:CustomerBusObj, new_customer:Customer):
        # Test creating a new customer
        assert customer_bus_obj.customer_id is None
        # assert isinstance(customer_bus_obj.customer_id, int)
        if db_dialect == 'postgresql':
            assert isinstance(customer_bus_obj.code, UUID)
        elif db_dialect == 'mssql':
            assert isinstance(customer_bus_obj.code, UNIQUEIDENTIFIER)
        else:  # This will cover SQLite, MySQL, and other databases
            assert isinstance(customer_bus_obj.code, str)
        assert isinstance(customer_bus_obj.last_change_code, int)
        assert customer_bus_obj.insert_user_id is None
        assert customer_bus_obj.last_update_user_id is None
        assert isinstance(customer_bus_obj.active_organization_id, int)
        assert customer_bus_obj.email == "" or isinstance(customer_bus_obj.email, str)
        assert isinstance(customer_bus_obj.email_confirmed_utc_date_time, datetime)
        assert customer_bus_obj.first_name == "" or isinstance(customer_bus_obj.first_name, str)
        assert isinstance(customer_bus_obj.forgot_password_key_expiration_utc_date_time, datetime)
        assert customer_bus_obj.forgot_password_key_value == "" or isinstance(customer_bus_obj.forgot_password_key_value, str)
        #FSUserCodeValue
        if db_dialect == 'postgresql':
            assert isinstance(customer_bus_obj.fs_user_code_value, UUID)
        elif db_dialect == 'mssql':
            assert isinstance(customer_bus_obj.fs_user_code_value, UNIQUEIDENTIFIER)
        else:  # This will cover SQLite, MySQL, and other databases
            assert isinstance(customer_bus_obj.fs_user_code_value, str)
        assert isinstance(customer_bus_obj.is_active, bool)
        assert isinstance(customer_bus_obj.is_email_allowed, bool)
        assert isinstance(customer_bus_obj.is_email_confirmed, bool)
        assert isinstance(customer_bus_obj.is_email_marketing_allowed, bool)
        assert isinstance(customer_bus_obj.is_locked, bool)
        assert isinstance(customer_bus_obj.is_multiple_organizations_allowed, bool)
        assert isinstance(customer_bus_obj.is_verbose_logging_forced, bool)
        assert isinstance(customer_bus_obj.last_login_utc_date_time, datetime)
        assert customer_bus_obj.last_name == "" or isinstance(customer_bus_obj.last_name, str)
        assert customer_bus_obj.password == "" or isinstance(customer_bus_obj.password, str)
        assert customer_bus_obj.phone == "" or isinstance(customer_bus_obj.phone, str)
        assert customer_bus_obj.province == "" or isinstance(customer_bus_obj.province, str)
        assert isinstance(customer_bus_obj.registration_utc_date_time, datetime)
        assert isinstance(customer_bus_obj.tac_id, int)
        assert isinstance(customer_bus_obj.utc_offset_in_minutes, int)
        assert customer_bus_obj.zip == "" or isinstance(customer_bus_obj.zip, str)
    @pytest.mark.asyncio
    async def test_load_with_customer_obj(self, customer_manager:CustomerManager, customer_bus_obj:CustomerBusObj, new_customer:Customer):
        await customer_bus_obj.load(customer_obj_instance=new_customer)
        assert customer_manager.is_equal(customer_bus_obj.customer,new_customer) == True
    @pytest.mark.asyncio
    async def test_load_with_customer_id(self, customer_manager:CustomerManager, customer_bus_obj:CustomerBusObj, new_customer:Customer):
        await customer_bus_obj.load(customer_id=new_customer.customer_id)
        assert customer_manager.is_equal(customer_bus_obj.customer,new_customer)  == True
    @pytest.mark.asyncio
    async def test_load_with_customer_code(self, customer_manager:CustomerManager, customer_bus_obj:CustomerBusObj, new_customer:Customer):
        await customer_bus_obj.load(code=new_customer.code)
        assert customer_manager.is_equal(customer_bus_obj.customer,new_customer)  == True
    @pytest.mark.asyncio
    async def test_load_with_customer_json(self, customer_manager:CustomerManager, customer_bus_obj:CustomerBusObj, new_customer:Customer):
        customer_json = customer_manager.to_json(new_customer)
        await customer_bus_obj.load(json_data=customer_json)
        assert customer_manager.is_equal(customer_bus_obj.customer,new_customer)  == True
    @pytest.mark.asyncio
    async def test_load_with_customer_dict(self, session, customer_manager:CustomerManager, customer_bus_obj:CustomerBusObj, new_customer:Customer):
        logger.info("test_load_with_customer_dict 1")
        customer_dict = customer_manager.to_dict(new_customer)
        logger.info(customer_dict)
        await customer_bus_obj.load(customer_dict=customer_dict)
        assert customer_manager.is_equal(customer_bus_obj.customer,new_customer)  == True
    @pytest.mark.asyncio
    async def test_get_nonexistent_customer(self, customer_manager:CustomerManager, customer_bus_obj:CustomerBusObj, new_customer:Customer):
        # Test retrieving a nonexistent customer raises an exception
        assert await customer_bus_obj.load(customer_id=-1) is None # Assuming -1 is an id that wouldn't exist
    @pytest.mark.asyncio
    async def test_update_customer(self, customer_manager:CustomerManager, customer_bus_obj:CustomerBusObj, new_customer:Customer):
        # Test updating a customer's data
        new_customer = await customer_manager.get_by_id(new_customer.customer_id)
        new_code = generate_uuid()
        await customer_bus_obj.load(customer_obj_instance=new_customer)
        customer_bus_obj.code = new_code
        await customer_bus_obj.save()
        new_customer = await customer_manager.get_by_id(new_customer.customer_id)
        assert customer_manager.is_equal(customer_bus_obj.customer,new_customer)  == True
    @pytest.mark.asyncio
    async def test_delete_customer(self, customer_manager:CustomerManager, customer_bus_obj:CustomerBusObj, new_customer:Customer):
        assert new_customer.customer_id is not None
        assert customer_bus_obj.customer_id is None
        await customer_bus_obj.load(customer_id=new_customer.customer_id)
        assert customer_bus_obj.customer_id is not None
        await customer_bus_obj.delete()
        new_customer = await customer_manager.get_by_id(new_customer.customer_id)
        assert new_customer is None
