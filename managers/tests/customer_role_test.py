import pytest
import uuid
from unittest.mock import AsyncMock, patch
from managers import CustomerRoleManager, CustomerRole
from models.factory import CustomerRoleFactory
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models import Base, CustomerRole
DATABASE_URL = "sqlite:///:memory:"
db_dialect = "sqlite"
class TestCustomerRoleManager:
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
    async def customer_role_manager(self, session):
        return CustomerRoleManager(session)
    @pytest.mark.asyncio
    async def test_build(self, customer_role_manager):
        # Define some mock data for our customer_role
        mock_data = {
            "name": "Rose",
            "species": "Rosa",
            "age": 2
        }
        # Call the build function of the manager
        customer_role = await customer_role_manager.build(**mock_data)
        # Assert that the returned object is an instance of CustomerRole
        assert isinstance(customer_role, CustomerRole)
        # Assert that the attributes of the customer_role match our mock data
        assert customer_role.name == mock_data["name"]
        assert customer_role.species == mock_data["species"]
        assert customer_role.age == mock_data["age"]
        # Optionally, if the build method has some default values or computations:
        # assert customer_role.some_attribute == some_expected_value
    @pytest.mark.asyncio
    async def test_build_with_missing_data(self, customer_role_manager):
        # Define mock data with a missing key
        mock_data = {
            "name": "Rose",
            "age": 2
        }
        # If the build method is expected to raise an exception for missing data, test for that
        with pytest.raises(SomeSpecificException):
            await customer_role_manager.build(**mock_data)
    @pytest.mark.asyncio
    async def test_add(self, customer_role_manager, mock_session):
        customer_role_data = CustomerRoleFactory.build()
        mock_session.add.return_value = None
        mock_session.commit.return_value = None
        customer_role = await customer_role_manager.add(**customer_role_data)
        mock_session.add.assert_called_once_with(customer_role)
        mock_session.commit.assert_called_once()
        assert isinstance(customer_role, CustomerRole)
    @pytest.mark.asyncio
    async def test_add_correctly_adds_customer_role_to_database(self, customer_role_manager, db_session):
        # Create a test customer_role using the CustomerRoleFactory without persisting it to the database
        test_customer_role = CustomerRoleFactory.build()
        # Add the customer_role using the manager's add method
        added_customer_role = await customer_role_manager.add(customer_role=test_customer_role)
        # Fetch the customer_role from the database directly
        result = await db_session.execute(select(CustomerRole).filter(CustomerRole.customer_role_id == added_customer_role.customer_role_id))
        fetched_customer_role = result.scalars().first()
        # Assert that the fetched customer_role is not None and matches the added customer_role
        assert fetched_customer_role is not None
        assert fetched_customer_role.customer_role_id == added_customer_role.customer_role_id
        assert fetched_customer_role.name == added_customer_role.name
        # ... other attribute checks ...
    @pytest.mark.asyncio
    async def test_add_returns_correct_customer_role_object(self, customer_role_manager):
        # Create a test customer_role using the CustomerRoleFactory without persisting it to the database
        test_customer_role = CustomerRoleFactory.build()
        # Add the customer_role using the manager's add method
        added_customer_role = await customer_role_manager.add(customer_role=test_customer_role)
        # Assert that the returned customer_role matches the test customer_role
        assert added_customer_role.customer_role_id == test_customer_role.customer_role_id
        assert added_customer_role.name == test_customer_role.name
        # ... other attribute checks ...
    @pytest.mark.asyncio
    async def test_get_by_id(self, customer_role_manager, mock_session):
        customer_role_data = CustomerRoleFactory.build()
        mock_session.execute.return_value = AsyncMock(scalars=AsyncMock(first=AsyncMock(return_value=customer_role_data)))
        customer_role = await customer_role_manager.get_by_id(1)
        mock_session.execute.assert_called_once()
        assert isinstance(customer_role, CustomerRole)
    async def test_get_by_id(self, session: AsyncSession, sample_customer_role: CustomerRole):
        manager = CustomerRoleManager(session)
        retrieved_customer_role = await manager.get_by_id(sample_customer_role.customer_role_id)
        assert retrieved_customer_role is not None
        assert retrieved_customer_role.customer_role_id == sample_customer_role.customer_role_id
        assert retrieved_customer_role.name == "Rose"
        assert retrieved_customer_role.color == "Red"
    async def test_get_by_id_not_found(self, session: AsyncSession):
        manager = CustomerRoleManager(session)
        non_existent_id = 9999  # An ID that's not in the database
        retrieved_customer_role = await manager.get_by_id(non_existent_id)
        assert retrieved_customer_role is None
    @pytest.mark.asyncio
    async def test_get_by_code_returns_customer_role(self, customer_role_manager, db_session):
        # Use your CustomerRoleFactory to create and save a CustomerRole object
        code = uuid.uuid4()
        customer_role = CustomerRoleFactory(code=code)
        db_session.add(customer_role)
        await db_session.commit()
        # Fetch the customer_role using the manager's get_by_code method
        fetched_customer_role = await customer_role_manager.get_by_code(code)
        # Assert that the fetched customer_role is not None and has the expected code
        assert fetched_customer_role is not None
        assert fetched_customer_role.code == code
    @pytest.mark.asyncio
    async def test_get_by_code_returns_none_for_nonexistent_code(self, customer_role_manager):
        # Generate a random UUID that doesn't correspond to any CustomerRole in the database
        random_code = uuid.uuid4()
        # Try fetching a customer_role using the manager's get_by_code method
        fetched_customer_role = await customer_role_manager.get_by_code(random_code)
        # Assert that the result is None since no customer_role with the given code exists
        assert fetched_customer_role is None
    @pytest.mark.asyncio
    async def test_update(self, customer_role_manager, mock_session):
        customer_role_data = CustomerRoleFactory.build()
        updated_data = {"name": "Updated CustomerRole"}
        mock_session.execute.return_value = AsyncMock(scalars=AsyncMock(first=AsyncMock(return_value=customer_role_data)))
        mock_session.commit.return_value = None
        updated_customer_role = await customer_role_manager.update(1, **updated_data)
        assert updated_customer_role.name == "Updated CustomerRole"
        mock_session.commit.assert_called_once()
        assert isinstance(updated_customer_role, CustomerRole)
    async def test_update_valid_customer_role(self):
        # Mocking a customer_role instance
        customer_role = CustomerRole(customer_role_id=1, name="Rose", code="ROSE123")
        # Mocking the commit method
        self.session_mock.commit = AsyncMock()
        # Update the customer_role with new attributes
        updated_customer_role = await self.manager.update(customer_role, name="Red Rose", code="REDROSE123")
        # Assertions
        assert updated_customer_role.name == "Red Rose"
        assert updated_customer_role.code == "REDROSE123"
        self.session_mock.commit.assert_called_once()
    async def test_update_invalid_customer_role(self):
        # None customer_role
        customer_role = None
        updated_customer_role = await self.manager.update(customer_role, name="Red Rose", code="REDROSE123")
        # Assertions
        assert updated_customer_role is None
        self.session_mock.commit.assert_not_called()
    async def test_update_with_nonexistent_attribute(self):
        # Mocking a customer_role instance
        customer_role = CustomerRole(customer_role_id=1, name="Rose", code="ROSE123")
        # Mocking the commit method
        self.session_mock.commit = AsyncMock()
        # This should raise an AttributeError since 'color' is not an attribute of CustomerRole
        with pytest.raises(AttributeError):
            await self.manager.update(customer_role, color="Red")
        self.session_mock.commit.assert_not_called()
    @pytest.mark.asyncio
    async def test_delete(self, customer_role_manager, mock_session):
        customer_role_data = CustomerRoleFactory.build()
        mock_session.execute.return_value = AsyncMock(scalars=AsyncMock(first=AsyncMock(return_value=customer_role_data)))
        mock_session.delete.return_value = None
        mock_session.commit.return_value = None
        deleted_customer_role = await customer_role_manager.delete(1)
        mock_session.delete.assert_called_once_with(deleted_customer_role)
        mock_session.commit.assert_called_once()
        assert isinstance(deleted_customer_role, CustomerRole)
    @pytest.mark.asyncio
    async def test_delete_nonexistent(self, customer_role_manager, mock_session):
        mock_session.execute.return_value = AsyncMock(scalars=AsyncMock(first=AsyncMock(return_value=None)))
        with pytest.raises(ValueError, match="CustomerRole not found"):
            await customer_role_manager.delete(999)
    @pytest.mark.asyncio
    async def test_get_list(self, customer_role_manager, mock_session):
        customer_roles_data = [CustomerRoleFactory.build() for _ in range(5)]
        mock_session.execute.return_value = AsyncMock(scalars=AsyncMock(all=AsyncMock(return_value=customer_roles_data)))
        customer_roles = await customer_role_manager.get_list()
        mock_session.execute.assert_called_once()
        assert len(customer_roles) == 5
        assert all(isinstance(customer_role, CustomerRole) for customer_role in customer_roles)
    @pytest.mark.asyncio
    async def test_to_json(self, customer_role_manager):
        customer_role_data = CustomerRoleFactory.build()
        customer_role = CustomerRole(**customer_role_data)
        json_data = customer_role_manager.to_json(customer_role)
        assert json_data is not None
        # You might want to do more specific checks on the JSON structure
    @pytest.mark.asyncio
    async def test_from_json(self, customer_role_manager):
        customer_role_data = CustomerRoleFactory.build()
        customer_role = CustomerRole(**customer_role_data)
        json_data = customer_role_manager.to_json(customer_role)
        deserialized_customer_role = customer_role_manager.from_json(json_data)
        assert isinstance(deserialized_customer_role, CustomerRole)
        # Additional checks on the deserialized data can be added
    @pytest.mark.asyncio
    async def test_add_bulk(self, customer_role_manager, mock_session):
        customer_roles_data = [CustomerRoleFactory.build() for _ in range(5)]
        mock_session.add_all.return_value = None
        mock_session.commit.return_value = None
        customer_roles = await customer_role_manager.add_bulk(customer_roles_data)
        mock_session.add_all.assert_called_once()
        mock_session.commit.assert_called_once()
        assert len(customer_roles) == 5
    @pytest.mark.asyncio
    async def test_update_bulk_success():
        manager = CustomerRoleManager()
        session_mock = AsyncMock()
        manager.session = session_mock
        # Mocking customer_role instances
        customer_role1 = CustomerRole(customer_role_id=1, name="Rose", code="ROSE123")
        customer_role2 = CustomerRole(customer_role_id=2, name="Tulip", code="TULIP123")
        # Mocking the get_by_id method to return the corresponding customer_role
        async def mock_get_by_id(customer_role_id):
            if customer_role_id == 1:
                return customer_role1
            if customer_role_id == 2:
                return customer_role2
        manager.get_by_id = mock_get_by_id
        # Mocking the commit method
        session_mock.commit = AsyncMock()
        # Update customer_roles
        updates = [{"customer_role_id": 1, "name": "Red Rose"}, {"customer_role_id": 2, "name": "Yellow Tulip"}]
        updated_customer_roles = await manager.update_bulk(updates)
        # Assertions
        assert len(updated_customer_roles) == 2
        assert updated_customer_roles[0].name == "Red Rose"
        assert updated_customer_roles[1].name == "Yellow Tulip"
        session_mock.commit.assert_called_once()
    @pytest.mark.asyncio
    async def test_update_bulk_missing_customer_role_id():
        manager = CustomerRoleManager()
        # No customer_roles to update since customer_role_id is missing
        updates = [{"name": "Red Rose"}]
        updated_customer_roles = await manager.update_bulk(updates)
        # Assertions
        assert len(updated_customer_roles) == 0
    @pytest.mark.asyncio
    async def test_update_bulk_customer_role_not_found():
        manager = CustomerRoleManager()
        session_mock = AsyncMock()
        manager.session = session_mock
        # Mocking the get_by_id method to return None (customer_role not found)
        manager.get_by_id = AsyncMock(return_value=None)
        # Mocking the commit method
        session_mock.commit = AsyncMock()
        # Update customer_roles
        updates = [{"customer_role_id": 1, "name": "Red Rose"}]
        updated_customer_roles = await manager.update_bulk(updates)
        # Assertions
        assert len(updated_customer_roles) == 0
        session_mock.commit.assert_not_called()
    @pytest.mark.asyncio
    async def test_delete_bulk_success():
        manager = CustomerRoleManager()
        session_mock = AsyncMock()
        manager.session = session_mock
        # Mocking customer_role instances
        customer_role1 = CustomerRole(customer_role_id=1, name="Rose", code="ROSE123")
        customer_role2 = CustomerRole(customer_role_id=2, name="Tulip", code="TULIP123")
        # Mocking the get_by_id method to return the corresponding customer_role
        async def mock_get_by_id(customer_role_id):
            if customer_role_id == 1:
                return customer_role1
            if customer_role_id == 2:
                return customer_role2
        manager.get_by_id = mock_get_by_id
        # Mocking the commit and delete methods
        session_mock.commit = AsyncMock()
        session_mock.delete = AsyncMock()
        # Delete customer_roles
        customer_role_ids = [1, 2]
        result = await manager.delete_bulk(customer_role_ids)
        # Assertions
        assert result is True
        session_mock.delete.assert_called()
        session_mock.commit.assert_called_once()
    @pytest.mark.asyncio
    async def test_delete_bulk_some_customer_roles_not_found():
        manager = CustomerRoleManager()
        session_mock = AsyncMock()
        manager.session = session_mock
        # Mocking the get_by_id method to return None (customer_role not found)
        async def mock_get_by_id(customer_role_id):
            if customer_role_id == 1:
                return None
            if customer_role_id == 2:
                return CustomerRole(customer_role_id=2, name="Tulip", code="TULIP123")
        manager.get_by_id = mock_get_by_id
        # Mocking the commit and delete methods
        session_mock.commit = AsyncMock()
        session_mock.delete = AsyncMock()
        # Delete customer_roles
        customer_role_ids = [1, 2]
        result = await manager.delete_bulk(customer_role_ids)
        # Assertions
        assert result is True
        session_mock.delete.assert_called_once_with(CustomerRole(customer_role_id=2, name="Tulip", code="TULIP123"))
        session_mock.commit.assert_called_once()
    @pytest.mark.asyncio
    async def test_delete_bulk_empty_list():
        manager = CustomerRoleManager()
        session_mock = AsyncMock()
        manager.session = session_mock
        # Mocking the commit and delete methods
        session_mock.commit = AsyncMock()
        session_mock.delete = AsyncMock()
        # Delete customer_roles with an empty list
        customer_role_ids = []
        result = await manager.delete_bulk(customer_role_ids)
        # Assertions
        assert result is True
        session_mock.delete.assert_not_called()
        session_mock.commit.assert_not_called()
    @pytest.mark.asyncio
    async def test_count(self, customer_role_manager, mock_session):
        customer_roles_data = [CustomerRoleFactory.build() for _ in range(5)]
        mock_session.execute.return_value = AsyncMock(scalars=AsyncMock(all=AsyncMock(return_value=customer_roles_data)))
        count = await customer_role_manager.count()
        mock_session.execute.assert_called_once()
        assert count == 5
    @pytest.mark.asyncio
    async def test_count_basic_functionality(async_session):
        # Add a customer_role
        new_customer_role = CustomerRole()
        async_session.add(new_customer_role)
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
        # Add multiple customer_roles
        customer_roles = [CustomerRole() for _ in range(5)]
        async_session.add_all(customer_roles)
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
        # Add customer_roles
        customer_roles = [CustomerRole(name=f"CustomerRole_{i}") for i in range(5)]
        async_session.add_all(customer_roles)
        await async_session.commit()
        manager = YourManagerClass(session=async_session)
        sorted_customer_roles = await manager.get_sorted_list(sort_by="name")
        assert [customer_role.name for customer_role in sorted_customer_roles] == [f"CustomerRole_{i}" for i in range(5)]
    @pytest.mark.asyncio
    async def test_get_sorted_list_descending_sorting(async_session):
        # Add customer_roles
        customer_roles = [CustomerRole(name=f"CustomerRole_{i}") for i in range(5)]
        async_session.add_all(customer_roles)
        await async_session.commit()
        manager = YourManagerClass(session=async_session)
        sorted_customer_roles = await manager.get_sorted_list(sort_by="name", order="desc")
        assert [customer_role.name for customer_role in sorted_customer_roles] == [f"CustomerRole_{i}" for i in reversed(range(5))]
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
        sorted_customer_roles = await manager.get_sorted_list(sort_by="name")
        assert len(sorted_customer_roles) == 0
    @pytest.mark.asyncio
    async def test_refresh_basic(async_session):
        # Add a customer_role
        customer_role = CustomerRole(name="CustomerRole_1")
        async_session.add(customer_role)
        await async_session.commit()
        # Modify the customer_role directly in the database
        await async_session.execute('UPDATE customer_roles SET name = :new_name WHERE id = :customer_role_id', {"new_name": "Modified_CustomerRole", "customer_role_id": customer_role.id})
        await async_session.commit()
        # Now, refresh the customer_role using the manager function
        manager = YourManagerClass(session=async_session)
        refreshed_customer_role = await manager.refresh(customer_role)
        assert refreshed_customer_role.name == "Modified_CustomerRole"
    @pytest.mark.asyncio
    async def test_refresh_nonexistent_customer_role(async_session):
        customer_role = CustomerRole(id=999, name="Nonexistent_CustomerRole")
        manager = YourManagerClass(session=async_session)
        with pytest.raises(Exception):  # Modify the exception type based on your ORM's behavior
            await manager.refresh(customer_role)
    @pytest.mark.asyncio
    async def test_refresh_database_connection_issues(async_session, mocker):
        # Mock the session's refresh method to simulate a database connection error
        mocker.patch.object(async_session, 'refresh', side_effect=Exception("DB connection error"))
        customer_role = CustomerRole(name="CustomerRole_1")
        manager = YourManagerClass(session=async_session)
        with pytest.raises(Exception, match="DB connection error"):
            await manager.refresh(customer_role)
    @pytest.mark.asyncio
    async def test_exists_with_existing_customer_role(async_session):
        # Add a customer_role
        customer_role = CustomerRole(name="CustomerRole_1")
        async_session.add(customer_role)
        await async_session.commit()
        # Check if the customer_role exists using the manager function
        manager = YourManagerClass(session=async_session)
        assert await manager.exists(customer_role.id) == True
    @pytest.mark.asyncio
    async def test_exists_with_nonexistent_customer_role(async_session):
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
    #get_by_role_id
    @pytest.mark.asyncio
    async def test_get_by_role_id_existing(async_session):
        # Add a customer_role with a specific role_id
        customer_role = CustomerRole(name="CustomerRole_1", role_id=5)
        async_session.add(customer_role)
        await async_session.commit()
        # Fetch the customer_role using the manager function
        manager = YourManagerClass(session=async_session)
        fetched_customer_roles = await manager.get_by_role_id(5)
        assert len(fetched_customer_roles) == 1
        assert fetched_customer_roles[0].name == "CustomerRole_1"
    @pytest.mark.asyncio
    async def test_get_by_role_id_nonexistent(async_session):
        non_existent_id = 999
        manager = YourManagerClass(session=async_session)
        fetched_customer_roles = await manager.get_by_role_id(non_existent_id)
        assert len(fetched_customer_roles) == 0
    @pytest.mark.asyncio
    async def test_get_by_role_id_invalid_type(async_session):
        invalid_id = "invalid_id"
        manager = YourManagerClass(session=async_session)
        with pytest.raises(Exception):  # Modify the exception type based on your ORM's behavior or validation
            await manager.get_by_role_id(invalid_id)
    @pytest.mark.asyncio
    async def test_get_by_role_id_database_connection_issues(async_session, mocker):
        # Mock the execute method to simulate a database connection error
        mocker.patch.object(async_session, 'execute', side_effect=Exception("DB connection error"))
        manager = YourManagerClass(session=async_session)
        with pytest.raises(Exception, match="DB connection error"):
            await manager.get_by_role_id(1)
    @pytest.mark.asyncio
    async def test_get_by_customer_id_existing(async_session):
        # Add a customer_role with a specific customer_id
        customer_role = CustomerRole(name="CustomerRole_1", customer_id=5)
        async_session.add(customer_role)
        await async_session.commit()
        # Fetch the customer_role using the manager function
        manager = YourManagerClass(session=async_session)
        fetched_customer_roles = await manager.get_by_customer_id(5)
        assert len(fetched_customer_roles) == 1
        assert fetched_customer_roles[0].name == "CustomerRole_1"
    @pytest.mark.asyncio
    async def test_get_by_customer_id_nonexistent(async_session):
        non_existent_id = 999
        manager = YourManagerClass(session=async_session)
        fetched_customer_roles = await manager.get_by_customer_id(non_existent_id)
        assert len(fetched_customer_roles) == 0
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