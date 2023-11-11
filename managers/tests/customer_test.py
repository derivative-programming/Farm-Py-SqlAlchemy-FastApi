import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from models import Customer
from models.factory import CustomerFactory
from managers.customer import CustomerManager
from models.serialization_schema.customer import CustomerSchema
from services.db_config import db_dialect
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
from services.db_config import db_dialect,generate_uuid
from sqlalchemy import String
from sqlalchemy.future import select
# DATABASE_URL = "sqlite+aiosqlite:///:memory:"
db_dialect = "sqlite"
# Conditionally set the UUID column type
if db_dialect == 'postgresql':
    UUIDType = UUID(as_uuid=True)
elif db_dialect == 'mssql':
    UUIDType = UNIQUEIDENTIFIER
else:  # This will cover SQLite, MySQL, and other databases
    UUIDType = String(36)
class TestCustomerManager:
    @pytest_asyncio.fixture(scope="function")
    async def customer_manager(self, session:AsyncSession):
        return CustomerManager(session)
    @pytest.mark.asyncio
    async def test_build(self, customer_manager:CustomerManager, session:AsyncSession):
        # Define some mock data for our customer
        mock_data = {
            "code": generate_uuid()
        }
        # Call the build function of the manager
        customer = await customer_manager.build(**mock_data)
        # Assert that the returned object is an instance of Customer
        assert isinstance(customer, Customer)
        # Assert that the attributes of the customer match our mock data
        assert customer.code == mock_data["code"]
        # Optionally, if the build method has some default values or computations:
        # assert customer.some_attribute == some_expected_value
    @pytest.mark.asyncio
    async def test_build_with_missing_data(self, customer_manager:CustomerManager, session:AsyncSession):
        # Define mock data with a missing key
        mock_data = {
            "non_existant_property": "Rose"
        }
        # If the build method is expected to raise an exception for missing data, test for that
        with pytest.raises(Exception):
            await customer_manager.build_async(**mock_data)
        await session.rollback()
    @pytest.mark.asyncio
    async def test_add_correctly_adds_customer_to_database(self, customer_manager:CustomerManager, session:AsyncSession):
        test_customer = await CustomerFactory.build_async(session)
        assert test_customer.customer_id is None
        # Add the customer using the manager's add method
        added_customer = await customer_manager.add(customer=test_customer)
        assert isinstance(added_customer, Customer)
        assert added_customer.customer_id > 0
        # Fetch the customer from the database directly
        result = await session.execute(select(Customer).filter(Customer.customer_id == added_customer.customer_id))
        fetched_customer = result.scalars().first()
        # Assert that the fetched customer is not None and matches the added customer
        assert fetched_customer is not None
        assert isinstance(fetched_customer, Customer)
        assert fetched_customer.customer_id == added_customer.customer_id
    @pytest.mark.asyncio
    async def test_add_returns_correct_customer_object(self, customer_manager:CustomerManager, session:AsyncSession):
        # Create a test customer using the CustomerFactory without persisting it to the database
        test_customer = await CustomerFactory.build_async(session)
        assert test_customer.customer_id is None
        test_customer.code = generate_uuid()
        # Add the customer using the manager's add method
        added_customer = await customer_manager.add(customer=test_customer)
        assert isinstance(added_customer, Customer)
        assert added_customer.customer_id > 0
        # Assert that the returned customer matches the test customer
        assert added_customer.customer_id == test_customer.customer_id
        assert added_customer.code == test_customer.code
    @pytest.mark.asyncio
    async def test_get_by_id(self, customer_manager:CustomerManager, session:AsyncSession):
        test_customer = await CustomerFactory.create_async(session)
        customer = await customer_manager.get_by_id(test_customer.customer_id)
        assert isinstance(customer, Customer)
        assert test_customer.customer_id == customer.customer_id
        assert test_customer.code == customer.code
    @pytest.mark.asyncio
    async def test_get_by_id_not_found(self, customer_manager:CustomerManager, session: AsyncSession):
        non_existent_id = 9999  # An ID that's not in the database
        retrieved_customer = await customer_manager.get_by_id(non_existent_id)
        assert retrieved_customer is None
    @pytest.mark.asyncio
    async def test_get_by_code_returns_customer(self, customer_manager:CustomerManager, session:AsyncSession):
        test_customer = await CustomerFactory.create_async(session)
        customer = await customer_manager.get_by_code(test_customer.code)
        assert isinstance(customer, Customer)
        assert test_customer.customer_id == customer.customer_id
        assert test_customer.code == customer.code
    @pytest.mark.asyncio
    async def test_get_by_code_returns_none_for_nonexistent_code(self, customer_manager:CustomerManager, session:AsyncSession):
        # Generate a random UUID that doesn't correspond to any Customer in the database
        random_code = generate_uuid()
        customer = await customer_manager.get_by_code(random_code)
        assert customer is None
    @pytest.mark.asyncio
    async def test_update(self, customer_manager:CustomerManager, session:AsyncSession):
        test_customer = await CustomerFactory.create_async(session)
        test_customer.code = generate_uuid()
        updated_customer = await customer_manager.update(customer=test_customer)
        assert isinstance(updated_customer, Customer)
        assert updated_customer.customer_id == test_customer.customer_id
        assert updated_customer.code == test_customer.code
        result = await session.execute(select(Customer).filter(Customer.customer_id == test_customer.customer_id))
        fetched_customer = result.scalars().first()
        assert updated_customer.customer_id == fetched_customer.customer_id
        assert updated_customer.code == fetched_customer.code
        assert test_customer.customer_id == fetched_customer.customer_id
        assert test_customer.code == fetched_customer.code
    @pytest.mark.asyncio
    async def test_update_via_dict(self, customer_manager:CustomerManager, session:AsyncSession):
        test_customer = await CustomerFactory.create_async(session)
        new_code = generate_uuid()
        updated_customer = await customer_manager.update(customer=test_customer,code=new_code)
        assert isinstance(updated_customer, Customer)
        assert updated_customer.customer_id == test_customer.customer_id
        assert updated_customer.code == new_code
        result = await session.execute(select(Customer).filter(Customer.customer_id == test_customer.customer_id))
        fetched_customer = result.scalars().first()
        assert updated_customer.customer_id == fetched_customer.customer_id
        assert updated_customer.code == fetched_customer.code
        assert test_customer.customer_id == fetched_customer.customer_id
        assert new_code == fetched_customer.code
    @pytest.mark.asyncio
    async def test_update_invalid_customer(self, customer_manager:CustomerManager):
        # None customer
        customer = None
        new_code = generate_uuid()
        updated_customer = await customer_manager.update(customer, code=new_code)
        # Assertions
        assert updated_customer is None
    #todo fix test
    # @pytest.mark.asyncio
    # async def test_update_with_nonexistent_attribute(self, customer_manager:CustomerManager, session:AsyncSession):
    #     test_customer = await CustomerFactory.create_async(session)
    #     new_code = generate_uuid()
    #     # This should raise an AttributeError since 'color' is not an attribute of Customer
    #     with pytest.raises(Exception):
    #         updated_customer = await customer_manager.update(customer=test_customer,xxx=new_code)
    #     await session.rollback()
    @pytest.mark.asyncio
    async def test_delete(self, customer_manager:CustomerManager, session:AsyncSession):
        customer_data = await CustomerFactory.create_async(session)
        result = await session.execute(select(Customer).filter(Customer.customer_id == customer_data.customer_id))
        fetched_customer = result.scalars().first()
        assert isinstance(fetched_customer, Customer)
        assert fetched_customer.customer_id == customer_data.customer_id
        deleted_customer = await customer_manager.delete(customer_id=customer_data.customer_id)
        result = await session.execute(select(Customer).filter(Customer.customer_id == customer_data.customer_id))
        fetched_customer = result.scalars().first()
        assert fetched_customer is None
    @pytest.mark.asyncio
    async def test_delete_nonexistent(self, customer_manager:CustomerManager, session:AsyncSession):
        with pytest.raises(Exception):
            await customer_manager.delete(999)
        await session.rollback()
    @pytest.mark.asyncio
    async def test_delete_invalid_type(self, customer_manager:CustomerManager, session:AsyncSession):
        with pytest.raises(Exception):
            await customer_manager.delete("999")
        await session.rollback()
    @pytest.mark.asyncio
    async def test_get_list(self, customer_manager:CustomerManager, session:AsyncSession):
        customers = await customer_manager.get_list()
        assert len(customers) == 0
        customers_data = [await CustomerFactory.create_async(session) for _ in range(5)]
        customers = await customer_manager.get_list()
        assert len(customers) == 5
        assert all(isinstance(customer, Customer) for customer in customers)
    @pytest.mark.asyncio
    async def test_to_json(self, customer_manager:CustomerManager, session:AsyncSession):
        customer = await CustomerFactory.build_async(session)
        json_data = customer_manager.to_json(customer)
        assert json_data is not None
    @pytest.mark.asyncio
    async def test_to_dict(self, customer_manager:CustomerManager, session:AsyncSession):
        customer = await CustomerFactory.build_async(session)
        dict_data = customer_manager.to_dict(customer)
        assert dict_data is not None
    @pytest.mark.asyncio
    async def test_from_json(self, customer_manager:CustomerManager, session:AsyncSession):
        customer = await CustomerFactory.create_async(session)
        json_data = customer_manager.to_json(customer)
        deserialized_customer = customer_manager.from_json(json_data)
        assert isinstance(deserialized_customer, Customer)
        assert deserialized_customer.code == customer.code
    @pytest.mark.asyncio
    async def test_from_dict(self, customer_manager:CustomerManager, session:AsyncSession):
        customer = await CustomerFactory.create_async(session)
        schema = CustomerSchema()
        customer_data = schema.dump(customer)
        deserialized_customer = customer_manager.from_dict(customer_data)
        assert isinstance(deserialized_customer, Customer)
        assert deserialized_customer.code == customer.code
    @pytest.mark.asyncio
    async def test_add_bulk(self, customer_manager:CustomerManager, session:AsyncSession):
        customers_data = [await CustomerFactory.build_async(session) for _ in range(5)]
        customers = await customer_manager.add_bulk(customers_data)
        assert len(customers) == 5
        for updated_customer in customers:
            result = await session.execute(select(Customer).filter(Customer.customer_id == updated_customer.customer_id))
            fetched_customer = result.scalars().first()
            assert isinstance(fetched_customer, Customer)
            assert fetched_customer.customer_id == updated_customer.customer_id
    @pytest.mark.asyncio
    async def test_update_bulk_success(self, customer_manager:CustomerManager, session:AsyncSession):
        # Mocking customer instances
        customer1 = await CustomerFactory.create_async(session=session)
        customer2 = await CustomerFactory.create_async(session=session)
        code_updated1 = generate_uuid()
        code_updated2 = generate_uuid()
        # Update customers
        updates = [{"customer_id": 1, "code": code_updated1}, {"customer_id": 2, "code": code_updated2}]
        updated_customers = await customer_manager.update_bulk(updates)
        # Assertions
        assert len(updated_customers) == 2
        assert updated_customers[0].code == code_updated1
        assert updated_customers[1].code == code_updated2
        result = await session.execute(select(Customer).filter(Customer.customer_id == 1))
        fetched_customer = result.scalars().first()
        assert isinstance(fetched_customer, Customer)
        assert fetched_customer.code == code_updated1
        result = await session.execute(select(Customer).filter(Customer.customer_id == 2))
        fetched_customer = result.scalars().first()
        assert isinstance(fetched_customer, Customer)
        assert fetched_customer.code == code_updated2
    @pytest.mark.asyncio
    async def test_update_bulk_missing_customer_id(self, customer_manager:CustomerManager, session:AsyncSession):
        # No customers to update since customer_id is missing
        updates = [{"name": "Red Rose"}]
        with pytest.raises(Exception):
            updated_customers = await customer_manager.update_bulk(updates)
        await session.rollback()
    @pytest.mark.asyncio
    async def test_update_bulk_customer_not_found(self, customer_manager:CustomerManager, session:AsyncSession):
        # Update customers
        updates = [{"customer_id": 1, "code": generate_uuid()}]
        with pytest.raises(Exception):
            updated_customers = await customer_manager.update_bulk(updates)
        await session.rollback()
    @pytest.mark.asyncio
    async def test_update_bulk_invalid_type(self, customer_manager:CustomerManager, session:AsyncSession):
        updates = [{"customer_id": "2", "code": generate_uuid()}]
        with pytest.raises(Exception):
            updated_customers = await customer_manager.update_bulk(updates)
        await session.rollback()
    @pytest.mark.asyncio
    async def test_delete_bulk_success(self, customer_manager:CustomerManager, session:AsyncSession):
        customer1 = await CustomerFactory.create_async(session=session)
        customer2 = await CustomerFactory.create_async(session=session)
        # Delete customers
        customer_ids = [1, 2]
        result = await customer_manager.delete_bulk(customer_ids)
        assert result is True
        for customer_id in customer_ids:
            execute_result = await session.execute(select(Customer).filter(Customer.customer_id == customer_id))
            fetched_customer = execute_result.scalars().first()
            assert fetched_customer is None
    @pytest.mark.asyncio
    async def test_delete_bulk_some_customers_not_found(self, customer_manager:CustomerManager, session:AsyncSession):
        customer1 = await CustomerFactory.create_async(session=session)
        # Delete customers
        customer_ids = [1, 2]
        with pytest.raises(Exception):
           result = await customer_manager.delete_bulk(customer_ids)
        await session.rollback()
    @pytest.mark.asyncio
    async def test_delete_bulk_empty_list(self, customer_manager:CustomerManager, session:AsyncSession):
        # Delete customers with an empty list
        customer_ids = []
        result = await customer_manager.delete_bulk(customer_ids)
        # Assertions
        assert result is True
    @pytest.mark.asyncio
    async def test_delete_bulk_invalid_type(self, customer_manager:CustomerManager, session:AsyncSession):
        customer_ids = ["1", 2]
        with pytest.raises(Exception):
           result = await customer_manager.delete_bulk(customer_ids)
        await session.rollback()
    @pytest.mark.asyncio
    async def test_count_basic_functionality(self, customer_manager:CustomerManager, session:AsyncSession):
        customers_data = [await CustomerFactory.create_async(session) for _ in range(5)]
        count = await customer_manager.count()
        assert count == 5
    @pytest.mark.asyncio
    async def test_count_empty_database(self, customer_manager:CustomerManager, session:AsyncSession):
        count = await customer_manager.count()
        assert count == 0
    @pytest.mark.asyncio
    async def test_get_sorted_list_basic_sorting(self, customer_manager:CustomerManager, session:AsyncSession):
        # Add customers
        customers_data = [await CustomerFactory.create_async(session) for _ in range(5)]
        sorted_customers = await customer_manager.get_sorted_list(sort_by="customer_id")
        assert [customer.customer_id for customer in sorted_customers] == [(i + 1) for i in range(5)]
    @pytest.mark.asyncio
    async def test_get_sorted_list_descending_sorting(self, customer_manager:CustomerManager, session:AsyncSession):
        # Add customers
        customers_data = [await CustomerFactory.create_async(session) for _ in range(5)]
        sorted_customers = await customer_manager.get_sorted_list(sort_by="customer_id", order="desc")
        assert [customer.customer_id for customer in sorted_customers] == [(i + 1) for i in reversed(range(5))]
    @pytest.mark.asyncio
    async def test_get_sorted_list_invalid_attribute(self, customer_manager:CustomerManager, session:AsyncSession):
        with pytest.raises(AttributeError):
            await customer_manager.get_sorted_list(sort_by="invalid_attribute")
        await session.rollback()
    @pytest.mark.asyncio
    async def test_get_sorted_list_empty_database(self, customer_manager:CustomerManager, session:AsyncSession):
        sorted_customers = await customer_manager.get_sorted_list(sort_by="customer_id")
        assert len(sorted_customers) == 0
    @pytest.mark.asyncio
    async def test_refresh_basic(self, customer_manager:CustomerManager, session:AsyncSession):
        # Add a customer
        customer1 = await CustomerFactory.create_async(session=session)
        result = await session.execute(select(Customer).filter(Customer.customer_id == customer1.customer_id))
        customer2 = result.scalars().first()
        assert customer1.code == customer2.code
        updated_code1 = generate_uuid()
        customer1.code = updated_code1
        updated_customer1 = await customer_manager.update(customer1)
        assert updated_customer1.code == updated_code1
        refreshed_customer2 = await customer_manager.refresh(customer2)
        assert refreshed_customer2.code == updated_code1
    @pytest.mark.asyncio
    async def test_refresh_nonexistent_customer(self, customer_manager:CustomerManager, session:AsyncSession):
        customer = Customer(customer_id=999)
        with pytest.raises(Exception):
            await customer_manager.refresh(customer)
        await session.rollback()
    @pytest.mark.asyncio
    async def test_exists_with_existing_customer(self, customer_manager:CustomerManager, session:AsyncSession):
        # Add a customer
        customer1 = await CustomerFactory.create_async(session=session)
        # Check if the customer exists using the manager function
        assert await customer_manager.exists(customer1.customer_id) == True
    @pytest.mark.asyncio
    async def test_is_equal_with_existing_customer(self, customer_manager:CustomerManager, session:AsyncSession):
        # Add a customer
        customer1 = await CustomerFactory.create_async(session=session)
        customer2 = await customer_manager.get_by_id(customer_id=customer1.customer_id)
        assert customer_manager.is_equal(customer1,customer2) == True
        customer1_dict = customer_manager.to_dict(customer1)
        customer3 = customer_manager.from_dict(customer1_dict)
        assert customer_manager.is_equal(customer1,customer3) == True
    @pytest.mark.asyncio
    async def test_exists_with_nonexistent_customer(self, customer_manager:CustomerManager, session:AsyncSession):
        non_existent_id = 999
        assert await customer_manager.exists(non_existent_id) == False
    @pytest.mark.asyncio
    async def test_exists_with_invalid_id_type(self, customer_manager:CustomerManager, session:AsyncSession):
        invalid_id = "invalid_id"
        with pytest.raises(Exception):
            await customer_manager.exists(invalid_id)
        await session.rollback()
#endet
    #activeOrganizationID,
    #email,
    #emailConfirmedUTCDateTime
    #firstName,
    #forgotPasswordKeyExpirationUTCDateTime
    #forgotPasswordKeyValue,
    #fSUserCodeValue,
    #isActive,
    #isEmailAllowed,
    #isEmailConfirmed,
    #isEmailMarketingAllowed,
    #isLocked,
    #isMultipleOrganizationsAllowed,
    #isVerboseLoggingForced,
    #lastLoginUTCDateTime
    #lastName,
    #password,
    #phone,
    #province,
    #registrationUTCDateTime
    #TacID
    @pytest.mark.asyncio
    async def test_get_by_tac_id_existing(self, customer_manager:CustomerManager, session:AsyncSession):
        # Add a customer with a specific tac_id
        customer1 = await CustomerFactory.create_async(session=session)
        # Fetch the customer using the manager function
        fetched_customers = await customer_manager.get_by_tac_id(customer1.tac_id)
        assert len(fetched_customers) == 1
        assert fetched_customers[0].code == customer1.code
    @pytest.mark.asyncio
    async def test_get_by_tac_id_nonexistent(self, customer_manager:CustomerManager, session:AsyncSession):
        non_existent_id = 999
        fetched_customers = await customer_manager.get_by_tac_id(non_existent_id)
        assert len(fetched_customers) == 0
    @pytest.mark.asyncio
    async def test_get_by_tac_id_invalid_type(self, customer_manager:CustomerManager, session:AsyncSession):
        invalid_id = "invalid_id"
        with pytest.raises(Exception):
            await customer_manager.get_by_tac_id(invalid_id)
        await session.rollback()
    #uTCOffsetInMinutes,
    #zip,
#endet
