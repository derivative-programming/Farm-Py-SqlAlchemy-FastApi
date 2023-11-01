import pytest
import uuid
from unittest.mock import AsyncMock, patch
from managers import CustomerManager, Customer
from models.factory import CustomerFactory
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models import Base, Customer
DATABASE_URL = "sqlite:///:memory:"
db_dialect = "sqlite"
class TestCustomerManager:
    @pytest.fixture(scope="module")
    def engine(self):
        engine = create_engine(DATABASE_URL, echo=True)
        #FKs are not activated by default in sqllite
        with engine.connect() as conn:
            conn.connection.execute("PRAGMA foreign_keys=ON")
        yield engine
        engine.dispose()
    @pytest.fixture
    def session(self, engine):
        Base.metadata.create_all(engine)
        SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)
        session_instance = SessionLocal()
        yield session_instance
        session_instance.close()
    @pytest.fixture
    async def customer_manager(self, session):
        return CustomerManager(session)
    @pytest.mark.asyncio
    async def test_build(self, customer_manager):
        # Define some mock data for our customer
        mock_data = {
            "name": "Rose",
            "species": "Rosa",
            "age": 2
        }
        # Call the build function of the manager
        customer = await customer_manager.build(**mock_data)
        # Assert that the returned object is an instance of Customer
        assert isinstance(customer, Customer)
        # Assert that the attributes of the customer match our mock data
        assert customer.name == mock_data["name"]
        assert customer.species == mock_data["species"]
        assert customer.age == mock_data["age"]
        # Optionally, if the build method has some default values or computations:
        # assert customer.some_attribute == some_expected_value
    @pytest.mark.asyncio
    async def test_build_with_missing_data(self, customer_manager):
        # Define mock data with a missing key
        mock_data = {
            "name": "Rose",
            "age": 2
        }
        # If the build method is expected to raise an exception for missing data, test for that
        with pytest.raises(SomeSpecificException):
            await customer_manager.build(**mock_data)
    @pytest.mark.asyncio
    async def test_add(self, customer_manager, mock_session):
        customer_data = CustomerFactory.build()
        mock_session.add.return_value = None
        mock_session.commit.return_value = None
        customer = await customer_manager.add(**customer_data)
        mock_session.add.assert_called_once_with(customer)
        mock_session.commit.assert_called_once()
        assert isinstance(customer, Customer)
    @pytest.mark.asyncio
    async def test_add_correctly_adds_customer_to_database(self, customer_manager, db_session):
        # Create a test customer using the CustomerFactory without persisting it to the database
        test_customer = CustomerFactory.build()
        # Add the customer using the manager's add method
        added_customer = await customer_manager.add(customer=test_customer)
        # Fetch the customer from the database directly
        result = await db_session.execute(select(Customer).filter(Customer.customer_id == added_customer.customer_id))
        fetched_customer = result.scalars().first()
        # Assert that the fetched customer is not None and matches the added customer
        assert fetched_customer is not None
        assert fetched_customer.customer_id == added_customer.customer_id
        assert fetched_customer.name == added_customer.name
        # ... other attribute checks ...
    @pytest.mark.asyncio
    async def test_add_returns_correct_customer_object(self, customer_manager):
        # Create a test customer using the CustomerFactory without persisting it to the database
        test_customer = CustomerFactory.build()
        # Add the customer using the manager's add method
        added_customer = await customer_manager.add(customer=test_customer)
        # Assert that the returned customer matches the test customer
        assert added_customer.customer_id == test_customer.customer_id
        assert added_customer.name == test_customer.name
        # ... other attribute checks ...
    @pytest.mark.asyncio
    async def test_get_by_id(self, customer_manager, mock_session):
        customer_data = CustomerFactory.build()
        mock_session.execute.return_value = AsyncMock(scalars=AsyncMock(first=AsyncMock(return_value=customer_data)))
        customer = await customer_manager.get_by_id(1)
        mock_session.execute.assert_called_once()
        assert isinstance(customer, Customer)
    async def test_get_by_id(self, session: AsyncSession, sample_customer: Customer):
        manager = CustomerManager(session)
        retrieved_customer = await manager.get_by_id(sample_customer.customer_id)
        assert retrieved_customer is not None
        assert retrieved_customer.customer_id == sample_customer.customer_id
        assert retrieved_customer.name == "Rose"
        assert retrieved_customer.color == "Red"
    async def test_get_by_id_not_found(self, session: AsyncSession):
        manager = CustomerManager(session)
        non_existent_id = 9999  # An ID that's not in the database
        retrieved_customer = await manager.get_by_id(non_existent_id)
        assert retrieved_customer is None
    @pytest.mark.asyncio
    async def test_get_by_code_returns_customer(self, customer_manager, db_session):
        # Use your CustomerFactory to create and save a Customer object
        code = uuid.uuid4()
        customer = CustomerFactory(code=code)
        db_session.add(customer)
        await db_session.commit()
        # Fetch the customer using the manager's get_by_code method
        fetched_customer = await customer_manager.get_by_code(code)
        # Assert that the fetched customer is not None and has the expected code
        assert fetched_customer is not None
        assert fetched_customer.code == code
    @pytest.mark.asyncio
    async def test_get_by_code_returns_none_for_nonexistent_code(self, customer_manager):
        # Generate a random UUID that doesn't correspond to any Customer in the database
        random_code = uuid.uuid4()
        # Try fetching a customer using the manager's get_by_code method
        fetched_customer = await customer_manager.get_by_code(random_code)
        # Assert that the result is None since no customer with the given code exists
        assert fetched_customer is None
    @pytest.mark.asyncio
    async def test_update(self, customer_manager, mock_session):
        customer_data = CustomerFactory.build()
        updated_data = {"name": "Updated Customer"}
        mock_session.execute.return_value = AsyncMock(scalars=AsyncMock(first=AsyncMock(return_value=customer_data)))
        mock_session.commit.return_value = None
        updated_customer = await customer_manager.update(1, **updated_data)
        assert updated_customer.name == "Updated Customer"
        mock_session.commit.assert_called_once()
        assert isinstance(updated_customer, Customer)
    async def test_update_valid_customer(self):
        # Mocking a customer instance
        customer = Customer(customer_id=1, name="Rose", code="ROSE123")
        # Mocking the commit method
        self.session_mock.commit = AsyncMock()
        # Update the customer with new attributes
        updated_customer = await self.manager.update(customer, name="Red Rose", code="REDROSE123")
        # Assertions
        assert updated_customer.name == "Red Rose"
        assert updated_customer.code == "REDROSE123"
        self.session_mock.commit.assert_called_once()
    async def test_update_invalid_customer(self):
        # None customer
        customer = None
        updated_customer = await self.manager.update(customer, name="Red Rose", code="REDROSE123")
        # Assertions
        assert updated_customer is None
        self.session_mock.commit.assert_not_called()
    async def test_update_with_nonexistent_attribute(self):
        # Mocking a customer instance
        customer = Customer(customer_id=1, name="Rose", code="ROSE123")
        # Mocking the commit method
        self.session_mock.commit = AsyncMock()
        # This should raise an AttributeError since 'color' is not an attribute of Customer
        with pytest.raises(AttributeError):
            await self.manager.update(customer, color="Red")
        self.session_mock.commit.assert_not_called()
    @pytest.mark.asyncio
    async def test_delete(self, customer_manager, mock_session):
        customer_data = CustomerFactory.build()
        mock_session.execute.return_value = AsyncMock(scalars=AsyncMock(first=AsyncMock(return_value=customer_data)))
        mock_session.delete.return_value = None
        mock_session.commit.return_value = None
        deleted_customer = await customer_manager.delete(1)
        mock_session.delete.assert_called_once_with(deleted_customer)
        mock_session.commit.assert_called_once()
        assert isinstance(deleted_customer, Customer)
    @pytest.mark.asyncio
    async def test_delete_nonexistent(self, customer_manager, mock_session):
        mock_session.execute.return_value = AsyncMock(scalars=AsyncMock(first=AsyncMock(return_value=None)))
        with pytest.raises(ValueError, match="Customer not found"):
            await customer_manager.delete(999)
    @pytest.mark.asyncio
    async def test_get_list(self, customer_manager, mock_session):
        customers_data = [CustomerFactory.build() for _ in range(5)]
        mock_session.execute.return_value = AsyncMock(scalars=AsyncMock(all=AsyncMock(return_value=customers_data)))
        customers = await customer_manager.get_list()
        mock_session.execute.assert_called_once()
        assert len(customers) == 5
        assert all(isinstance(customer, Customer) for customer in customers)
    @pytest.mark.asyncio
    async def test_to_json(self, customer_manager):
        customer_data = CustomerFactory.build()
        customer = Customer(**customer_data)
        json_data = customer_manager.to_json(customer)
        assert json_data is not None
        # You might want to do more specific checks on the JSON structure
    @pytest.mark.asyncio
    async def test_from_json(self, customer_manager):
        customer_data = CustomerFactory.build()
        customer = Customer(**customer_data)
        json_data = customer_manager.to_json(customer)
        deserialized_customer = customer_manager.from_json(json_data)
        assert isinstance(deserialized_customer, Customer)
        # Additional checks on the deserialized data can be added
    @pytest.mark.asyncio
    async def test_add_bulk(self, customer_manager, mock_session):
        customers_data = [CustomerFactory.build() for _ in range(5)]
        mock_session.add_all.return_value = None
        mock_session.commit.return_value = None
        customers = await customer_manager.add_bulk(customers_data)
        mock_session.add_all.assert_called_once()
        mock_session.commit.assert_called_once()
        assert len(customers) == 5
    @pytest.mark.asyncio
    async def test_update_bulk_success():
        manager = CustomerManager()
        session_mock = AsyncMock()
        manager.session = session_mock
        # Mocking customer instances
        customer1 = Customer(customer_id=1, name="Rose", code="ROSE123")
        customer2 = Customer(customer_id=2, name="Tulip", code="TULIP123")
        # Mocking the get_by_id method to return the corresponding customer
        async def mock_get_by_id(customer_id):
            if customer_id == 1:
                return customer1
            if customer_id == 2:
                return customer2
        manager.get_by_id = mock_get_by_id
        # Mocking the commit method
        session_mock.commit = AsyncMock()
        # Update customers
        updates = [{"customer_id": 1, "name": "Red Rose"}, {"customer_id": 2, "name": "Yellow Tulip"}]
        updated_customers = await manager.update_bulk(updates)
        # Assertions
        assert len(updated_customers) == 2
        assert updated_customers[0].name == "Red Rose"
        assert updated_customers[1].name == "Yellow Tulip"
        session_mock.commit.assert_called_once()
    @pytest.mark.asyncio
    async def test_update_bulk_missing_customer_id():
        manager = CustomerManager()
        # No customers to update since customer_id is missing
        updates = [{"name": "Red Rose"}]
        updated_customers = await manager.update_bulk(updates)
        # Assertions
        assert len(updated_customers) == 0
    @pytest.mark.asyncio
    async def test_update_bulk_customer_not_found():
        manager = CustomerManager()
        session_mock = AsyncMock()
        manager.session = session_mock
        # Mocking the get_by_id method to return None (customer not found)
        manager.get_by_id = AsyncMock(return_value=None)
        # Mocking the commit method
        session_mock.commit = AsyncMock()
        # Update customers
        updates = [{"customer_id": 1, "name": "Red Rose"}]
        updated_customers = await manager.update_bulk(updates)
        # Assertions
        assert len(updated_customers) == 0
        session_mock.commit.assert_not_called()
    @pytest.mark.asyncio
    async def test_delete_bulk_success():
        manager = CustomerManager()
        session_mock = AsyncMock()
        manager.session = session_mock
        # Mocking customer instances
        customer1 = Customer(customer_id=1, name="Rose", code="ROSE123")
        customer2 = Customer(customer_id=2, name="Tulip", code="TULIP123")
        # Mocking the get_by_id method to return the corresponding customer
        async def mock_get_by_id(customer_id):
            if customer_id == 1:
                return customer1
            if customer_id == 2:
                return customer2
        manager.get_by_id = mock_get_by_id
        # Mocking the commit and delete methods
        session_mock.commit = AsyncMock()
        session_mock.delete = AsyncMock()
        # Delete customers
        customer_ids = [1, 2]
        result = await manager.delete_bulk(customer_ids)
        # Assertions
        assert result is True
        session_mock.delete.assert_called()
        session_mock.commit.assert_called_once()
    @pytest.mark.asyncio
    async def test_delete_bulk_some_customers_not_found():
        manager = CustomerManager()
        session_mock = AsyncMock()
        manager.session = session_mock
        # Mocking the get_by_id method to return None (customer not found)
        async def mock_get_by_id(customer_id):
            if customer_id == 1:
                return None
            if customer_id == 2:
                return Customer(customer_id=2, name="Tulip", code="TULIP123")
        manager.get_by_id = mock_get_by_id
        # Mocking the commit and delete methods
        session_mock.commit = AsyncMock()
        session_mock.delete = AsyncMock()
        # Delete customers
        customer_ids = [1, 2]
        result = await manager.delete_bulk(customer_ids)
        # Assertions
        assert result is True
        session_mock.delete.assert_called_once_with(Customer(customer_id=2, name="Tulip", code="TULIP123"))
        session_mock.commit.assert_called_once()
    @pytest.mark.asyncio
    async def test_delete_bulk_empty_list():
        manager = CustomerManager()
        session_mock = AsyncMock()
        manager.session = session_mock
        # Mocking the commit and delete methods
        session_mock.commit = AsyncMock()
        session_mock.delete = AsyncMock()
        # Delete customers with an empty list
        customer_ids = []
        result = await manager.delete_bulk(customer_ids)
        # Assertions
        assert result is True
        session_mock.delete.assert_not_called()
        session_mock.commit.assert_not_called()
    @pytest.mark.asyncio
    async def test_count(self, customer_manager, mock_session):
        customers_data = [CustomerFactory.build() for _ in range(5)]
        mock_session.execute.return_value = AsyncMock(scalars=AsyncMock(all=AsyncMock(return_value=customers_data)))
        count = await customer_manager.count()
        mock_session.execute.assert_called_once()
        assert count == 5
    @pytest.mark.asyncio
    async def test_count_basic_functionality(async_session):
        # Add a customer
        new_customer = Customer()
        async_session.add(new_customer)
        await async_session.commit()
        manager = YourManagerClass(session=async_session)
        count = await manager.count()
        assert count == 1
    @pytest.mark.asyncio
    async def test_count_empty_database(async_session):
        manager = YourManagerClass(session=async_session)
        count = await manager.count()
        assert count == 0
    @pytest.mark.asyncio
    async def test_count_multiple_additions(async_session):
        # Add multiple customers
        customers = [Customer() for _ in range(5)]
        async_session.add_all(customers)
        await async_session.commit()
        manager = YourManagerClass(session=async_session)
        count = await manager.count()
        assert count == 5
    @pytest.mark.asyncio
    async def test_count_database_connection_issues(async_session, mocker):
        # Mock the session's execute method to simulate a database connection error
        mocker.patch.object(async_session, 'execute', side_effect=Exception("DB connection error"))
        manager = YourManagerClass(session=async_session)
        with pytest.raises(Exception, match="DB connection error"):
            await manager.count()
    @pytest.mark.asyncio
    async def test_get_sorted_list_basic_sorting(async_session):
        # Add customers
        customers = [Customer(name=f"Customer_{i}") for i in range(5)]
        async_session.add_all(customers)
        await async_session.commit()
        manager = YourManagerClass(session=async_session)
        sorted_customers = await manager.get_sorted_list(sort_by="name")
        assert [customer.name for customer in sorted_customers] == [f"Customer_{i}" for i in range(5)]
    @pytest.mark.asyncio
    async def test_get_sorted_list_descending_sorting(async_session):
        # Add customers
        customers = [Customer(name=f"Customer_{i}") for i in range(5)]
        async_session.add_all(customers)
        await async_session.commit()
        manager = YourManagerClass(session=async_session)
        sorted_customers = await manager.get_sorted_list(sort_by="name", order="desc")
        assert [customer.name for customer in sorted_customers] == [f"Customer_{i}" for i in reversed(range(5))]
    @pytest.mark.asyncio
    async def test_get_sorted_list_invalid_attribute(async_session):
        manager = YourManagerClass(session=async_session)
        with pytest.raises(AttributeError):
            await manager.get_sorted_list(sort_by="invalid_attribute")
    @pytest.mark.asyncio
    async def test_get_sorted_list_database_connection_issues(async_session, mocker):
        # Mock the session's execute method to simulate a database connection error
        mocker.patch.object(async_session, 'execute', side_effect=Exception("DB connection error"))
        manager = YourManagerClass(session=async_session)
        with pytest.raises(Exception, match="DB connection error"):
            await manager.get_sorted_list(sort_by="name")
    @pytest.mark.asyncio
    async def test_get_sorted_list_empty_database(async_session):
        manager = YourManagerClass(session=async_session)
        sorted_customers = await manager.get_sorted_list(sort_by="name")
        assert len(sorted_customers) == 0
    @pytest.mark.asyncio
    async def test_refresh_basic(async_session):
        # Add a customer
        customer = Customer(name="Customer_1")
        async_session.add(customer)
        await async_session.commit()
        # Modify the customer directly in the database
        await async_session.execute('UPDATE customers SET name = :new_name WHERE id = :customer_id', {"new_name": "Modified_Customer", "customer_id": customer.id})
        await async_session.commit()
        # Now, refresh the customer using the manager function
        manager = YourManagerClass(session=async_session)
        refreshed_customer = await manager.refresh(customer)
        assert refreshed_customer.name == "Modified_Customer"
    @pytest.mark.asyncio
    async def test_refresh_nonexistent_customer(async_session):
        customer = Customer(id=999, name="Nonexistent_Customer")
        manager = YourManagerClass(session=async_session)
        with pytest.raises(Exception):  # Modify the exception type based on your ORM's behavior
            await manager.refresh(customer)
    @pytest.mark.asyncio
    async def test_refresh_database_connection_issues(async_session, mocker):
        # Mock the session's refresh method to simulate a database connection error
        mocker.patch.object(async_session, 'refresh', side_effect=Exception("DB connection error"))
        customer = Customer(name="Customer_1")
        manager = YourManagerClass(session=async_session)
        with pytest.raises(Exception, match="DB connection error"):
            await manager.refresh(customer)
    @pytest.mark.asyncio
    async def test_exists_with_existing_customer(async_session):
        # Add a customer
        customer = Customer(name="Customer_1")
        async_session.add(customer)
        await async_session.commit()
        # Check if the customer exists using the manager function
        manager = YourManagerClass(session=async_session)
        assert await manager.exists(customer.id) == True
    @pytest.mark.asyncio
    async def test_exists_with_nonexistent_customer(async_session):
        non_existent_id = 999
        manager = YourManagerClass(session=async_session)
        assert await manager.exists(non_existent_id) == False
    @pytest.mark.asyncio
    async def test_exists_with_invalid_id_type(async_session):
        invalid_id = "invalid_id"
        manager = YourManagerClass(session=async_session)
        with pytest.raises(Exception):  # Modify the exception type based on your ORM's behavior or validation
            await manager.exists(invalid_id)
    @pytest.mark.asyncio
    async def test_exists_database_connection_issues(async_session, mocker):
        # Mock the get_by_id method to simulate a database connection error
        mocker.patch.object(YourManagerClass, 'get_by_id', side_effect=Exception("DB connection error"))
        manager = YourManagerClass(session=async_session)
        with pytest.raises(Exception, match="DB connection error"):
            await manager.exists(1)
    #get_by_tac_id
    @pytest.mark.asyncio
    async def test_get_by_tac_id_existing(async_session):
        # Add a customer with a specific tac_id
        customer = Customer(name="Customer_1", tac_id=5)
        async_session.add(customer)
        await async_session.commit()
        # Fetch the customer using the manager function
        manager = YourManagerClass(session=async_session)
        fetched_customers = await manager.get_by_tac_id(5)
        assert len(fetched_customers) == 1
        assert fetched_customers[0].name == "Customer_1"
    @pytest.mark.asyncio
    async def test_get_by_tac_id_nonexistent(async_session):
        non_existent_id = 999
        manager = YourManagerClass(session=async_session)
        fetched_customers = await manager.get_by_tac_id(non_existent_id)
        assert len(fetched_customers) == 0
    @pytest.mark.asyncio
    async def test_get_by_tac_id_invalid_type(async_session):
        invalid_id = "invalid_id"
        manager = YourManagerClass(session=async_session)
        with pytest.raises(Exception):  # Modify the exception type based on your ORM's behavior or validation
            await manager.get_by_tac_id(invalid_id)
    @pytest.mark.asyncio
    async def test_get_by_tac_id_database_connection_issues(async_session, mocker):
        # Mock the execute method to simulate a database connection error
        mocker.patch.object(async_session, 'execute', side_effect=Exception("DB connection error"))
        manager = YourManagerClass(session=async_session)
        with pytest.raises(Exception, match="DB connection error"):
            await manager.get_by_tac_id(1)
