import pytest
import uuid
from unittest.mock import AsyncMock, patch
from managers import RoleManager, Role
from models.factory import RoleFactory
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models import Base, Role
DATABASE_URL = "sqlite:///:memory:"
db_dialect = "sqlite"
class TestRoleManager:
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
    async def role_manager(self, session):
        return RoleManager(session)
    @pytest.mark.asyncio
    async def test_build(self, role_manager):
        # Define some mock data for our role
        mock_data = {
            "name": "Rose",
            "species": "Rosa",
            "age": 2
        }
        # Call the build function of the manager
        role = await role_manager.build(**mock_data)
        # Assert that the returned object is an instance of Role
        assert isinstance(role, Role)
        # Assert that the attributes of the role match our mock data
        assert role.name == mock_data["name"]
        assert role.species == mock_data["species"]
        assert role.age == mock_data["age"]
        # Optionally, if the build method has some default values or computations:
        # assert role.some_attribute == some_expected_value
    @pytest.mark.asyncio
    async def test_build_with_missing_data(self, role_manager):
        # Define mock data with a missing key
        mock_data = {
            "name": "Rose",
            "age": 2
        }
        # If the build method is expected to raise an exception for missing data, test for that
        with pytest.raises(SomeSpecificException):
            await role_manager.build(**mock_data)
    @pytest.mark.asyncio
    async def test_add(self, role_manager, mock_session):
        role_data = RoleFactory.build()
        mock_session.add.return_value = None
        mock_session.commit.return_value = None
        role = await role_manager.add(**role_data)
        mock_session.add.assert_called_once_with(role)
        mock_session.commit.assert_called_once()
        assert isinstance(role, Role)
    @pytest.mark.asyncio
    async def test_add_correctly_adds_role_to_database(self, role_manager, db_session):
        # Create a test role using the RoleFactory without persisting it to the database
        test_role = RoleFactory.build()
        # Add the role using the manager's add method
        added_role = await role_manager.add(role=test_role)
        # Fetch the role from the database directly
        result = await db_session.execute(select(Role).filter(Role.role_id == added_role.role_id))
        fetched_role = result.scalars().first()
        # Assert that the fetched role is not None and matches the added role
        assert fetched_role is not None
        assert fetched_role.role_id == added_role.role_id
        assert fetched_role.name == added_role.name
        # ... other attribute checks ...
    @pytest.mark.asyncio
    async def test_add_returns_correct_role_object(self, role_manager):
        # Create a test role using the RoleFactory without persisting it to the database
        test_role = RoleFactory.build()
        # Add the role using the manager's add method
        added_role = await role_manager.add(role=test_role)
        # Assert that the returned role matches the test role
        assert added_role.role_id == test_role.role_id
        assert added_role.name == test_role.name
        # ... other attribute checks ...
    @pytest.mark.asyncio
    async def test_get_by_id(self, role_manager, mock_session):
        role_data = RoleFactory.build()
        mock_session.execute.return_value = AsyncMock(scalars=AsyncMock(first=AsyncMock(return_value=role_data)))
        role = await role_manager.get_by_id(1)
        mock_session.execute.assert_called_once()
        assert isinstance(role, Role)
    async def test_get_by_id(self, session: AsyncSession, sample_role: Role):
        manager = RoleManager(session)
        retrieved_role = await manager.get_by_id(sample_role.role_id)
        assert retrieved_role is not None
        assert retrieved_role.role_id == sample_role.role_id
        assert retrieved_role.name == "Rose"
        assert retrieved_role.color == "Red"
    async def test_get_by_id_not_found(self, session: AsyncSession):
        manager = RoleManager(session)
        non_existent_id = 9999  # An ID that's not in the database
        retrieved_role = await manager.get_by_id(non_existent_id)
        assert retrieved_role is None
    @pytest.mark.asyncio
    async def test_get_by_code_returns_role(self, role_manager, db_session):
        # Use your RoleFactory to create and save a Role object
        code = uuid.uuid4()
        role = RoleFactory(code=code)
        db_session.add(role)
        await db_session.commit()
        # Fetch the role using the manager's get_by_code method
        fetched_role = await role_manager.get_by_code(code)
        # Assert that the fetched role is not None and has the expected code
        assert fetched_role is not None
        assert fetched_role.code == code
    @pytest.mark.asyncio
    async def test_get_by_code_returns_none_for_nonexistent_code(self, role_manager):
        # Generate a random UUID that doesn't correspond to any Role in the database
        random_code = uuid.uuid4()
        # Try fetching a role using the manager's get_by_code method
        fetched_role = await role_manager.get_by_code(random_code)
        # Assert that the result is None since no role with the given code exists
        assert fetched_role is None
    @pytest.mark.asyncio
    async def test_update(self, role_manager, mock_session):
        role_data = RoleFactory.build()
        updated_data = {"name": "Updated Role"}
        mock_session.execute.return_value = AsyncMock(scalars=AsyncMock(first=AsyncMock(return_value=role_data)))
        mock_session.commit.return_value = None
        updated_role = await role_manager.update(1, **updated_data)
        assert updated_role.name == "Updated Role"
        mock_session.commit.assert_called_once()
        assert isinstance(updated_role, Role)
    async def test_update_valid_role(self):
        # Mocking a role instance
        role = Role(role_id=1, name="Rose", code="ROSE123")
        # Mocking the commit method
        self.session_mock.commit = AsyncMock()
        # Update the role with new attributes
        updated_role = await self.manager.update(role, name="Red Rose", code="REDROSE123")
        # Assertions
        assert updated_role.name == "Red Rose"
        assert updated_role.code == "REDROSE123"
        self.session_mock.commit.assert_called_once()
    async def test_update_invalid_role(self):
        # None role
        role = None
        updated_role = await self.manager.update(role, name="Red Rose", code="REDROSE123")
        # Assertions
        assert updated_role is None
        self.session_mock.commit.assert_not_called()
    async def test_update_with_nonexistent_attribute(self):
        # Mocking a role instance
        role = Role(role_id=1, name="Rose", code="ROSE123")
        # Mocking the commit method
        self.session_mock.commit = AsyncMock()
        # This should raise an AttributeError since 'color' is not an attribute of Role
        with pytest.raises(AttributeError):
            await self.manager.update(role, color="Red")
        self.session_mock.commit.assert_not_called()
    @pytest.mark.asyncio
    async def test_delete(self, role_manager, mock_session):
        role_data = RoleFactory.build()
        mock_session.execute.return_value = AsyncMock(scalars=AsyncMock(first=AsyncMock(return_value=role_data)))
        mock_session.delete.return_value = None
        mock_session.commit.return_value = None
        deleted_role = await role_manager.delete(1)
        mock_session.delete.assert_called_once_with(deleted_role)
        mock_session.commit.assert_called_once()
        assert isinstance(deleted_role, Role)
    @pytest.mark.asyncio
    async def test_delete_nonexistent(self, role_manager, mock_session):
        mock_session.execute.return_value = AsyncMock(scalars=AsyncMock(first=AsyncMock(return_value=None)))
        with pytest.raises(ValueError, match="Role not found"):
            await role_manager.delete(999)
    @pytest.mark.asyncio
    async def test_get_list(self, role_manager, mock_session):
        roles_data = [RoleFactory.build() for _ in range(5)]
        mock_session.execute.return_value = AsyncMock(scalars=AsyncMock(all=AsyncMock(return_value=roles_data)))
        roles = await role_manager.get_list()
        mock_session.execute.assert_called_once()
        assert len(roles) == 5
        assert all(isinstance(role, Role) for role in roles)
    @pytest.mark.asyncio
    async def test_to_json(self, role_manager):
        role_data = RoleFactory.build()
        role = Role(**role_data)
        json_data = role_manager.to_json(role)
        assert json_data is not None
        # You might want to do more specific checks on the JSON structure
    @pytest.mark.asyncio
    async def test_from_json(self, role_manager):
        role_data = RoleFactory.build()
        role = Role(**role_data)
        json_data = role_manager.to_json(role)
        deserialized_role = role_manager.from_json(json_data)
        assert isinstance(deserialized_role, Role)
        # Additional checks on the deserialized data can be added
    @pytest.mark.asyncio
    async def test_add_bulk(self, role_manager, mock_session):
        roles_data = [RoleFactory.build() for _ in range(5)]
        mock_session.add_all.return_value = None
        mock_session.commit.return_value = None
        roles = await role_manager.add_bulk(roles_data)
        mock_session.add_all.assert_called_once()
        mock_session.commit.assert_called_once()
        assert len(roles) == 5
    @pytest.mark.asyncio
    async def test_update_bulk_success():
        manager = RoleManager()
        session_mock = AsyncMock()
        manager.session = session_mock
        # Mocking role instances
        role1 = Role(role_id=1, name="Rose", code="ROSE123")
        role2 = Role(role_id=2, name="Tulip", code="TULIP123")
        # Mocking the get_by_id method to return the corresponding role
        async def mock_get_by_id(role_id):
            if role_id == 1:
                return role1
            if role_id == 2:
                return role2
        manager.get_by_id = mock_get_by_id
        # Mocking the commit method
        session_mock.commit = AsyncMock()
        # Update roles
        updates = [{"role_id": 1, "name": "Red Rose"}, {"role_id": 2, "name": "Yellow Tulip"}]
        updated_roles = await manager.update_bulk(updates)
        # Assertions
        assert len(updated_roles) == 2
        assert updated_roles[0].name == "Red Rose"
        assert updated_roles[1].name == "Yellow Tulip"
        session_mock.commit.assert_called_once()
    @pytest.mark.asyncio
    async def test_update_bulk_missing_role_id():
        manager = RoleManager()
        # No roles to update since role_id is missing
        updates = [{"name": "Red Rose"}]
        updated_roles = await manager.update_bulk(updates)
        # Assertions
        assert len(updated_roles) == 0
    @pytest.mark.asyncio
    async def test_update_bulk_role_not_found():
        manager = RoleManager()
        session_mock = AsyncMock()
        manager.session = session_mock
        # Mocking the get_by_id method to return None (role not found)
        manager.get_by_id = AsyncMock(return_value=None)
        # Mocking the commit method
        session_mock.commit = AsyncMock()
        # Update roles
        updates = [{"role_id": 1, "name": "Red Rose"}]
        updated_roles = await manager.update_bulk(updates)
        # Assertions
        assert len(updated_roles) == 0
        session_mock.commit.assert_not_called()
    @pytest.mark.asyncio
    async def test_delete_bulk_success():
        manager = RoleManager()
        session_mock = AsyncMock()
        manager.session = session_mock
        # Mocking role instances
        role1 = Role(role_id=1, name="Rose", code="ROSE123")
        role2 = Role(role_id=2, name="Tulip", code="TULIP123")
        # Mocking the get_by_id method to return the corresponding role
        async def mock_get_by_id(role_id):
            if role_id == 1:
                return role1
            if role_id == 2:
                return role2
        manager.get_by_id = mock_get_by_id
        # Mocking the commit and delete methods
        session_mock.commit = AsyncMock()
        session_mock.delete = AsyncMock()
        # Delete roles
        role_ids = [1, 2]
        result = await manager.delete_bulk(role_ids)
        # Assertions
        assert result is True
        session_mock.delete.assert_called()
        session_mock.commit.assert_called_once()
    @pytest.mark.asyncio
    async def test_delete_bulk_some_roles_not_found():
        manager = RoleManager()
        session_mock = AsyncMock()
        manager.session = session_mock
        # Mocking the get_by_id method to return None (role not found)
        async def mock_get_by_id(role_id):
            if role_id == 1:
                return None
            if role_id == 2:
                return Role(role_id=2, name="Tulip", code="TULIP123")
        manager.get_by_id = mock_get_by_id
        # Mocking the commit and delete methods
        session_mock.commit = AsyncMock()
        session_mock.delete = AsyncMock()
        # Delete roles
        role_ids = [1, 2]
        result = await manager.delete_bulk(role_ids)
        # Assertions
        assert result is True
        session_mock.delete.assert_called_once_with(Role(role_id=2, name="Tulip", code="TULIP123"))
        session_mock.commit.assert_called_once()
    @pytest.mark.asyncio
    async def test_delete_bulk_empty_list():
        manager = RoleManager()
        session_mock = AsyncMock()
        manager.session = session_mock
        # Mocking the commit and delete methods
        session_mock.commit = AsyncMock()
        session_mock.delete = AsyncMock()
        # Delete roles with an empty list
        role_ids = []
        result = await manager.delete_bulk(role_ids)
        # Assertions
        assert result is True
        session_mock.delete.assert_not_called()
        session_mock.commit.assert_not_called()
    @pytest.mark.asyncio
    async def test_count(self, role_manager, mock_session):
        roles_data = [RoleFactory.build() for _ in range(5)]
        mock_session.execute.return_value = AsyncMock(scalars=AsyncMock(all=AsyncMock(return_value=roles_data)))
        count = await role_manager.count()
        mock_session.execute.assert_called_once()
        assert count == 5
    @pytest.mark.asyncio
    async def test_count_basic_functionality(async_session):
        # Add a role
        new_role = Role()
        async_session.add(new_role)
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
        # Add multiple roles
        roles = [Role() for _ in range(5)]
        async_session.add_all(roles)
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
        # Add roles
        roles = [Role(name=f"Role_{i}") for i in range(5)]
        async_session.add_all(roles)
        await async_session.commit()
        manager = YourManagerClass(session=async_session)
        sorted_roles = await manager.get_sorted_list(sort_by="name")
        assert [role.name for role in sorted_roles] == [f"Role_{i}" for i in range(5)]
    @pytest.mark.asyncio
    async def test_get_sorted_list_descending_sorting(async_session):
        # Add roles
        roles = [Role(name=f"Role_{i}") for i in range(5)]
        async_session.add_all(roles)
        await async_session.commit()
        manager = YourManagerClass(session=async_session)
        sorted_roles = await manager.get_sorted_list(sort_by="name", order="desc")
        assert [role.name for role in sorted_roles] == [f"Role_{i}" for i in reversed(range(5))]
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
        sorted_roles = await manager.get_sorted_list(sort_by="name")
        assert len(sorted_roles) == 0
    @pytest.mark.asyncio
    async def test_refresh_basic(async_session):
        # Add a role
        role = Role(name="Role_1")
        async_session.add(role)
        await async_session.commit()
        # Modify the role directly in the database
        await async_session.execute('UPDATE roles SET name = :new_name WHERE id = :role_id', {"new_name": "Modified_Role", "role_id": role.id})
        await async_session.commit()
        # Now, refresh the role using the manager function
        manager = YourManagerClass(session=async_session)
        refreshed_role = await manager.refresh(role)
        assert refreshed_role.name == "Modified_Role"
    @pytest.mark.asyncio
    async def test_refresh_nonexistent_role(async_session):
        role = Role(id=999, name="Nonexistent_Role")
        manager = YourManagerClass(session=async_session)
        with pytest.raises(Exception):  # Modify the exception type based on your ORM's behavior
            await manager.refresh(role)
    @pytest.mark.asyncio
    async def test_refresh_database_connection_issues(async_session, mocker):
        # Mock the session's refresh method to simulate a database connection error
        mocker.patch.object(async_session, 'refresh', side_effect=Exception("DB connection error"))
        role = Role(name="Role_1")
        manager = YourManagerClass(session=async_session)
        with pytest.raises(Exception, match="DB connection error"):
            await manager.refresh(role)
    @pytest.mark.asyncio
    async def test_exists_with_existing_role(async_session):
        # Add a role
        role = Role(name="Role_1")
        async_session.add(role)
        await async_session.commit()
        # Check if the role exists using the manager function
        manager = YourManagerClass(session=async_session)
        assert await manager.exists(role.id) == True
    @pytest.mark.asyncio
    async def test_exists_with_nonexistent_role(async_session):
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
    #get_by_pac_id
    @pytest.mark.asyncio
    async def test_get_by_pac_id_existing(async_session):
        # Add a role with a specific pac_id
        role = Role(name="Role_1", pac_id=5)
        async_session.add(role)
        await async_session.commit()
        # Fetch the role using the manager function
        manager = YourManagerClass(session=async_session)
        fetched_roles = await manager.get_by_pac_id(5)
        assert len(fetched_roles) == 1
        assert fetched_roles[0].name == "Role_1"
    @pytest.mark.asyncio
    async def test_get_by_pac_id_nonexistent(async_session):
        non_existent_id = 999
        manager = YourManagerClass(session=async_session)
        fetched_roles = await manager.get_by_pac_id(non_existent_id)
        assert len(fetched_roles) == 0
    @pytest.mark.asyncio
    async def test_get_by_pac_id_invalid_type(async_session):
        invalid_id = "invalid_id"
        manager = YourManagerClass(session=async_session)
        with pytest.raises(Exception):  # Modify the exception type based on your ORM's behavior or validation
            await manager.get_by_pac_id(invalid_id)
    @pytest.mark.asyncio
    async def test_get_by_pac_id_database_connection_issues(async_session, mocker):
        # Mock the execute method to simulate a database connection error
        mocker.patch.object(async_session, 'execute', side_effect=Exception("DB connection error"))
        manager = YourManagerClass(session=async_session)
        with pytest.raises(Exception, match="DB connection error"):
            await manager.get_by_pac_id(1)
