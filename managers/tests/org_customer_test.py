import pytest
import uuid
from unittest.mock import AsyncMock, patch
from managers import OrgCustomerManager, OrgCustomer
from models.factory import OrgCustomerFactory
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models import Base, OrgCustomer
DATABASE_URL = "sqlite:///:memory:"
db_dialect = "sqlite"
class TestOrgCustomerManager:
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
    async def org_customer_manager(self, session):
        return OrgCustomerManager(session)
    @pytest.mark.asyncio
    async def test_build(self, org_customer_manager):
        # Define some mock data for our org_customer
        mock_data = {
            "name": "Rose",
            "species": "Rosa",
            "age": 2
        }
        # Call the build function of the manager
        org_customer = await org_customer_manager.build(**mock_data)
        # Assert that the returned object is an instance of OrgCustomer
        assert isinstance(org_customer, OrgCustomer)
        # Assert that the attributes of the org_customer match our mock data
        assert org_customer.name == mock_data["name"]
        assert org_customer.species == mock_data["species"]
        assert org_customer.age == mock_data["age"]
        # Optionally, if the build method has some default values or computations:
        # assert org_customer.some_attribute == some_expected_value
    @pytest.mark.asyncio
    async def test_build_with_missing_data(self, org_customer_manager):
        # Define mock data with a missing key
        mock_data = {
            "name": "Rose",
            "age": 2
        }
        # If the build method is expected to raise an exception for missing data, test for that
        with pytest.raises(SomeSpecificException):
            await org_customer_manager.build(**mock_data)
    @pytest.mark.asyncio
    async def test_add(self, org_customer_manager, mock_session):
        org_customer_data = OrgCustomerFactory.build()
        mock_session.add.return_value = None
        mock_session.commit.return_value = None
        org_customer = await org_customer_manager.add(**org_customer_data)
        mock_session.add.assert_called_once_with(org_customer)
        mock_session.commit.assert_called_once()
        assert isinstance(org_customer, OrgCustomer)
    @pytest.mark.asyncio
    async def test_add_correctly_adds_org_customer_to_database(self, org_customer_manager, db_session):
        # Create a test org_customer using the OrgCustomerFactory without persisting it to the database
        test_org_customer = OrgCustomerFactory.build()
        # Add the org_customer using the manager's add method
        added_org_customer = await org_customer_manager.add(org_customer=test_org_customer)
        # Fetch the org_customer from the database directly
        result = await db_session.execute(select(OrgCustomer).filter(OrgCustomer.org_customer_id == added_org_customer.org_customer_id))
        fetched_org_customer = result.scalars().first()
        # Assert that the fetched org_customer is not None and matches the added org_customer
        assert fetched_org_customer is not None
        assert fetched_org_customer.org_customer_id == added_org_customer.org_customer_id
        assert fetched_org_customer.name == added_org_customer.name
        # ... other attribute checks ...
    @pytest.mark.asyncio
    async def test_add_returns_correct_org_customer_object(self, org_customer_manager):
        # Create a test org_customer using the OrgCustomerFactory without persisting it to the database
        test_org_customer = OrgCustomerFactory.build()
        # Add the org_customer using the manager's add method
        added_org_customer = await org_customer_manager.add(org_customer=test_org_customer)
        # Assert that the returned org_customer matches the test org_customer
        assert added_org_customer.org_customer_id == test_org_customer.org_customer_id
        assert added_org_customer.name == test_org_customer.name
        # ... other attribute checks ...
    @pytest.mark.asyncio
    async def test_get_by_id(self, org_customer_manager, mock_session):
        org_customer_data = OrgCustomerFactory.build()
        mock_session.execute.return_value = AsyncMock(scalars=AsyncMock(first=AsyncMock(return_value=org_customer_data)))
        org_customer = await org_customer_manager.get_by_id(1)
        mock_session.execute.assert_called_once()
        assert isinstance(org_customer, OrgCustomer)
    async def test_get_by_id(self, session: AsyncSession, sample_org_customer: OrgCustomer):
        manager = OrgCustomerManager(session)
        retrieved_org_customer = await manager.get_by_id(sample_org_customer.org_customer_id)
        assert retrieved_org_customer is not None
        assert retrieved_org_customer.org_customer_id == sample_org_customer.org_customer_id
        assert retrieved_org_customer.name == "Rose"
        assert retrieved_org_customer.color == "Red"
    async def test_get_by_id_not_found(self, session: AsyncSession):
        manager = OrgCustomerManager(session)
        non_existent_id = 9999  # An ID that's not in the database
        retrieved_org_customer = await manager.get_by_id(non_existent_id)
        assert retrieved_org_customer is None
    @pytest.mark.asyncio
    async def test_get_by_code_returns_org_customer(self, org_customer_manager, db_session):
        # Use your OrgCustomerFactory to create and save a OrgCustomer object
        code = uuid.uuid4()
        org_customer = OrgCustomerFactory(code=code)
        db_session.add(org_customer)
        await db_session.commit()
        # Fetch the org_customer using the manager's get_by_code method
        fetched_org_customer = await org_customer_manager.get_by_code(code)
        # Assert that the fetched org_customer is not None and has the expected code
        assert fetched_org_customer is not None
        assert fetched_org_customer.code == code
    @pytest.mark.asyncio
    async def test_get_by_code_returns_none_for_nonexistent_code(self, org_customer_manager):
        # Generate a random UUID that doesn't correspond to any OrgCustomer in the database
        random_code = uuid.uuid4()
        # Try fetching a org_customer using the manager's get_by_code method
        fetched_org_customer = await org_customer_manager.get_by_code(random_code)
        # Assert that the result is None since no org_customer with the given code exists
        assert fetched_org_customer is None
    @pytest.mark.asyncio
    async def test_update(self, org_customer_manager, mock_session):
        org_customer_data = OrgCustomerFactory.build()
        updated_data = {"name": "Updated OrgCustomer"}
        mock_session.execute.return_value = AsyncMock(scalars=AsyncMock(first=AsyncMock(return_value=org_customer_data)))
        mock_session.commit.return_value = None
        updated_org_customer = await org_customer_manager.update(1, **updated_data)
        assert updated_org_customer.name == "Updated OrgCustomer"
        mock_session.commit.assert_called_once()
        assert isinstance(updated_org_customer, OrgCustomer)
    async def test_update_valid_org_customer(self):
        # Mocking a org_customer instance
        org_customer = OrgCustomer(org_customer_id=1, name="Rose", code="ROSE123")
        # Mocking the commit method
        self.session_mock.commit = AsyncMock()
        # Update the org_customer with new attributes
        updated_org_customer = await self.manager.update(org_customer, name="Red Rose", code="REDROSE123")
        # Assertions
        assert updated_org_customer.name == "Red Rose"
        assert updated_org_customer.code == "REDROSE123"
        self.session_mock.commit.assert_called_once()
    async def test_update_invalid_org_customer(self):
        # None org_customer
        org_customer = None
        updated_org_customer = await self.manager.update(org_customer, name="Red Rose", code="REDROSE123")
        # Assertions
        assert updated_org_customer is None
        self.session_mock.commit.assert_not_called()
    async def test_update_with_nonexistent_attribute(self):
        # Mocking a org_customer instance
        org_customer = OrgCustomer(org_customer_id=1, name="Rose", code="ROSE123")
        # Mocking the commit method
        self.session_mock.commit = AsyncMock()
        # This should raise an AttributeError since 'color' is not an attribute of OrgCustomer
        with pytest.raises(AttributeError):
            await self.manager.update(org_customer, color="Red")
        self.session_mock.commit.assert_not_called()
    @pytest.mark.asyncio
    async def test_delete(self, org_customer_manager, mock_session):
        org_customer_data = OrgCustomerFactory.build()
        mock_session.execute.return_value = AsyncMock(scalars=AsyncMock(first=AsyncMock(return_value=org_customer_data)))
        mock_session.delete.return_value = None
        mock_session.commit.return_value = None
        deleted_org_customer = await org_customer_manager.delete(1)
        mock_session.delete.assert_called_once_with(deleted_org_customer)
        mock_session.commit.assert_called_once()
        assert isinstance(deleted_org_customer, OrgCustomer)
    @pytest.mark.asyncio
    async def test_delete_nonexistent(self, org_customer_manager, mock_session):
        mock_session.execute.return_value = AsyncMock(scalars=AsyncMock(first=AsyncMock(return_value=None)))
        with pytest.raises(ValueError, match="OrgCustomer not found"):
            await org_customer_manager.delete(999)
    @pytest.mark.asyncio
    async def test_get_list(self, org_customer_manager, mock_session):
        org_customers_data = [OrgCustomerFactory.build() for _ in range(5)]
        mock_session.execute.return_value = AsyncMock(scalars=AsyncMock(all=AsyncMock(return_value=org_customers_data)))
        org_customers = await org_customer_manager.get_list()
        mock_session.execute.assert_called_once()
        assert len(org_customers) == 5
        assert all(isinstance(org_customer, OrgCustomer) for org_customer in org_customers)
    @pytest.mark.asyncio
    async def test_to_json(self, org_customer_manager):
        org_customer_data = OrgCustomerFactory.build()
        org_customer = OrgCustomer(**org_customer_data)
        json_data = org_customer_manager.to_json(org_customer)
        assert json_data is not None
        # You might want to do more specific checks on the JSON structure
    @pytest.mark.asyncio
    async def test_from_json(self, org_customer_manager):
        org_customer_data = OrgCustomerFactory.build()
        org_customer = OrgCustomer(**org_customer_data)
        json_data = org_customer_manager.to_json(org_customer)
        deserialized_org_customer = org_customer_manager.from_json(json_data)
        assert isinstance(deserialized_org_customer, OrgCustomer)
        # Additional checks on the deserialized data can be added
    @pytest.mark.asyncio
    async def test_add_bulk(self, org_customer_manager, mock_session):
        org_customers_data = [OrgCustomerFactory.build() for _ in range(5)]
        mock_session.add_all.return_value = None
        mock_session.commit.return_value = None
        org_customers = await org_customer_manager.add_bulk(org_customers_data)
        mock_session.add_all.assert_called_once()
        mock_session.commit.assert_called_once()
        assert len(org_customers) == 5
    @pytest.mark.asyncio
    async def test_update_bulk_success():
        manager = OrgCustomerManager()
        session_mock = AsyncMock()
        manager.session = session_mock
        # Mocking org_customer instances
        org_customer1 = OrgCustomer(org_customer_id=1, name="Rose", code="ROSE123")
        org_customer2 = OrgCustomer(org_customer_id=2, name="Tulip", code="TULIP123")
        # Mocking the get_by_id method to return the corresponding org_customer
        async def mock_get_by_id(org_customer_id):
            if org_customer_id == 1:
                return org_customer1
            if org_customer_id == 2:
                return org_customer2
        manager.get_by_id = mock_get_by_id
        # Mocking the commit method
        session_mock.commit = AsyncMock()
        # Update org_customers
        updates = [{"org_customer_id": 1, "name": "Red Rose"}, {"org_customer_id": 2, "name": "Yellow Tulip"}]
        updated_org_customers = await manager.update_bulk(updates)
        # Assertions
        assert len(updated_org_customers) == 2
        assert updated_org_customers[0].name == "Red Rose"
        assert updated_org_customers[1].name == "Yellow Tulip"
        session_mock.commit.assert_called_once()
    @pytest.mark.asyncio
    async def test_update_bulk_missing_org_customer_id():
        manager = OrgCustomerManager()
        # No org_customers to update since org_customer_id is missing
        updates = [{"name": "Red Rose"}]
        updated_org_customers = await manager.update_bulk(updates)
        # Assertions
        assert len(updated_org_customers) == 0
    @pytest.mark.asyncio
    async def test_update_bulk_org_customer_not_found():
        manager = OrgCustomerManager()
        session_mock = AsyncMock()
        manager.session = session_mock
        # Mocking the get_by_id method to return None (org_customer not found)
        manager.get_by_id = AsyncMock(return_value=None)
        # Mocking the commit method
        session_mock.commit = AsyncMock()
        # Update org_customers
        updates = [{"org_customer_id": 1, "name": "Red Rose"}]
        updated_org_customers = await manager.update_bulk(updates)
        # Assertions
        assert len(updated_org_customers) == 0
        session_mock.commit.assert_not_called()
    @pytest.mark.asyncio
    async def test_delete_bulk_success():
        manager = OrgCustomerManager()
        session_mock = AsyncMock()
        manager.session = session_mock
        # Mocking org_customer instances
        org_customer1 = OrgCustomer(org_customer_id=1, name="Rose", code="ROSE123")
        org_customer2 = OrgCustomer(org_customer_id=2, name="Tulip", code="TULIP123")
        # Mocking the get_by_id method to return the corresponding org_customer
        async def mock_get_by_id(org_customer_id):
            if org_customer_id == 1:
                return org_customer1
            if org_customer_id == 2:
                return org_customer2
        manager.get_by_id = mock_get_by_id
        # Mocking the commit and delete methods
        session_mock.commit = AsyncMock()
        session_mock.delete = AsyncMock()
        # Delete org_customers
        org_customer_ids = [1, 2]
        result = await manager.delete_bulk(org_customer_ids)
        # Assertions
        assert result is True
        session_mock.delete.assert_called()
        session_mock.commit.assert_called_once()
    @pytest.mark.asyncio
    async def test_delete_bulk_some_org_customers_not_found():
        manager = OrgCustomerManager()
        session_mock = AsyncMock()
        manager.session = session_mock
        # Mocking the get_by_id method to return None (org_customer not found)
        async def mock_get_by_id(org_customer_id):
            if org_customer_id == 1:
                return None
            if org_customer_id == 2:
                return OrgCustomer(org_customer_id=2, name="Tulip", code="TULIP123")
        manager.get_by_id = mock_get_by_id
        # Mocking the commit and delete methods
        session_mock.commit = AsyncMock()
        session_mock.delete = AsyncMock()
        # Delete org_customers
        org_customer_ids = [1, 2]
        result = await manager.delete_bulk(org_customer_ids)
        # Assertions
        assert result is True
        session_mock.delete.assert_called_once_with(OrgCustomer(org_customer_id=2, name="Tulip", code="TULIP123"))
        session_mock.commit.assert_called_once()
    @pytest.mark.asyncio
    async def test_delete_bulk_empty_list():
        manager = OrgCustomerManager()
        session_mock = AsyncMock()
        manager.session = session_mock
        # Mocking the commit and delete methods
        session_mock.commit = AsyncMock()
        session_mock.delete = AsyncMock()
        # Delete org_customers with an empty list
        org_customer_ids = []
        result = await manager.delete_bulk(org_customer_ids)
        # Assertions
        assert result is True
        session_mock.delete.assert_not_called()
        session_mock.commit.assert_not_called()
    @pytest.mark.asyncio
    async def test_count(self, org_customer_manager, mock_session):
        org_customers_data = [OrgCustomerFactory.build() for _ in range(5)]
        mock_session.execute.return_value = AsyncMock(scalars=AsyncMock(all=AsyncMock(return_value=org_customers_data)))
        count = await org_customer_manager.count()
        mock_session.execute.assert_called_once()
        assert count == 5
    @pytest.mark.asyncio
    async def test_count_basic_functionality(async_session):
        # Add a org_customer
        new_org_customer = OrgCustomer()
        async_session.add(new_org_customer)
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
        # Add multiple org_customers
        org_customers = [OrgCustomer() for _ in range(5)]
        async_session.add_all(org_customers)
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
        # Add org_customers
        org_customers = [OrgCustomer(name=f"OrgCustomer_{i}") for i in range(5)]
        async_session.add_all(org_customers)
        await async_session.commit()
        manager = YourManagerClass(session=async_session)
        sorted_org_customers = await manager.get_sorted_list(sort_by="name")
        assert [org_customer.name for org_customer in sorted_org_customers] == [f"OrgCustomer_{i}" for i in range(5)]
    @pytest.mark.asyncio
    async def test_get_sorted_list_descending_sorting(async_session):
        # Add org_customers
        org_customers = [OrgCustomer(name=f"OrgCustomer_{i}") for i in range(5)]
        async_session.add_all(org_customers)
        await async_session.commit()
        manager = YourManagerClass(session=async_session)
        sorted_org_customers = await manager.get_sorted_list(sort_by="name", order="desc")
        assert [org_customer.name for org_customer in sorted_org_customers] == [f"OrgCustomer_{i}" for i in reversed(range(5))]
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
        sorted_org_customers = await manager.get_sorted_list(sort_by="name")
        assert len(sorted_org_customers) == 0
    @pytest.mark.asyncio
    async def test_refresh_basic(async_session):
        # Add a org_customer
        org_customer = OrgCustomer(name="OrgCustomer_1")
        async_session.add(org_customer)
        await async_session.commit()
        # Modify the org_customer directly in the database
        await async_session.execute('UPDATE org_customers SET name = :new_name WHERE id = :org_customer_id', {"new_name": "Modified_OrgCustomer", "org_customer_id": org_customer.id})
        await async_session.commit()
        # Now, refresh the org_customer using the manager function
        manager = YourManagerClass(session=async_session)
        refreshed_org_customer = await manager.refresh(org_customer)
        assert refreshed_org_customer.name == "Modified_OrgCustomer"
    @pytest.mark.asyncio
    async def test_refresh_nonexistent_org_customer(async_session):
        org_customer = OrgCustomer(id=999, name="Nonexistent_OrgCustomer")
        manager = YourManagerClass(session=async_session)
        with pytest.raises(Exception):  # Modify the exception type based on your ORM's behavior
            await manager.refresh(org_customer)
    @pytest.mark.asyncio
    async def test_refresh_database_connection_issues(async_session, mocker):
        # Mock the session's refresh method to simulate a database connection error
        mocker.patch.object(async_session, 'refresh', side_effect=Exception("DB connection error"))
        org_customer = OrgCustomer(name="OrgCustomer_1")
        manager = YourManagerClass(session=async_session)
        with pytest.raises(Exception, match="DB connection error"):
            await manager.refresh(org_customer)
    @pytest.mark.asyncio
    async def test_exists_with_existing_org_customer(async_session):
        # Add a org_customer
        org_customer = OrgCustomer(name="OrgCustomer_1")
        async_session.add(org_customer)
        await async_session.commit()
        # Check if the org_customer exists using the manager function
        manager = YourManagerClass(session=async_session)
        assert await manager.exists(org_customer.id) == True
    @pytest.mark.asyncio
    async def test_exists_with_nonexistent_org_customer(async_session):
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
    #get_by_customer_id
    @pytest.mark.asyncio
    async def test_get_by_customer_id_existing(async_session):
        # Add a org_customer with a specific customer_id
        org_customer = OrgCustomer(name="OrgCustomer_1", customer_id=5)
        async_session.add(org_customer)
        await async_session.commit()
        # Fetch the org_customer using the manager function
        manager = YourManagerClass(session=async_session)
        fetched_org_customers = await manager.get_by_customer_id(5)
        assert len(fetched_org_customers) == 1
        assert fetched_org_customers[0].name == "OrgCustomer_1"
    @pytest.mark.asyncio
    async def test_get_by_customer_id_nonexistent(async_session):
        non_existent_id = 999
        manager = YourManagerClass(session=async_session)
        fetched_org_customers = await manager.get_by_customer_id(non_existent_id)
        assert len(fetched_org_customers) == 0
    @pytest.mark.asyncio
    async def test_get_by_customer_id_invalid_type(async_session):
        invalid_id = "invalid_id"
        manager = YourManagerClass(session=async_session)
        with pytest.raises(Exception):  # Modify the exception type based on your ORM's behavior or validation
            await manager.get_by_customer_id(invalid_id)
    @pytest.mark.asyncio
    async def test_get_by_customer_id_database_connection_issues(async_session, mocker):
        # Mock the execute method to simulate a database connection error
        mocker.patch.object(async_session, 'execute', side_effect=Exception("DB connection error"))
        manager = YourManagerClass(session=async_session)
        with pytest.raises(Exception, match="DB connection error"):
            await manager.get_by_customer_id(1)
    #get_by_organization_id
    @pytest.mark.asyncio
    async def test_get_by_organization_id_existing(async_session):
        # Add a org_customer with a specific organization_id
        org_customer = OrgCustomer(name="OrgCustomer_1", organization_id=5)
        async_session.add(org_customer)
        await async_session.commit()
        # Fetch the org_customer using the manager function
        manager = YourManagerClass(session=async_session)
        fetched_org_customers = await manager.get_by_organization_id(5)
        assert len(fetched_org_customers) == 1
        assert fetched_org_customers[0].name == "OrgCustomer_1"
    @pytest.mark.asyncio
    async def test_get_by_organization_id_nonexistent(async_session):
        non_existent_id = 999
        manager = YourManagerClass(session=async_session)
        fetched_org_customers = await manager.get_by_organization_id(non_existent_id)
        assert len(fetched_org_customers) == 0
    @pytest.mark.asyncio
    async def test_get_by_organization_id_invalid_type(async_session):
        invalid_id = "invalid_id"
        manager = YourManagerClass(session=async_session)
        with pytest.raises(Exception):  # Modify the exception type based on your ORM's behavior or validation
            await manager.get_by_organization_id(invalid_id)
    @pytest.mark.asyncio
    async def test_get_by_organization_id_database_connection_issues(async_session, mocker):
        # Mock the execute method to simulate a database connection error
        mocker.patch.object(async_session, 'execute', side_effect=Exception("DB connection error"))
        manager = YourManagerClass(session=async_session)
        with pytest.raises(Exception, match="DB connection error"):
            await manager.get_by_organization_id(1)
