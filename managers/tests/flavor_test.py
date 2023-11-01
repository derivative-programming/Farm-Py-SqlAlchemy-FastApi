import pytest
import uuid
from unittest.mock import AsyncMock, patch
from managers import FlavorManager, Flavor
from models.factory import FlavorFactory
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models import Base, Flavor
DATABASE_URL = "sqlite:///:memory:"
db_dialect = "sqlite"
class TestFlavorManager:
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
    async def flavor_manager(self, session):
        return FlavorManager(session)
    @pytest.mark.asyncio
    async def test_build(self, flavor_manager):
        # Define some mock data for our flavor
        mock_data = {
            "name": "Rose",
            "species": "Rosa",
            "age": 2
        }
        # Call the build function of the manager
        flavor = await flavor_manager.build(**mock_data)
        # Assert that the returned object is an instance of Flavor
        assert isinstance(flavor, Flavor)
        # Assert that the attributes of the flavor match our mock data
        assert flavor.name == mock_data["name"]
        assert flavor.species == mock_data["species"]
        assert flavor.age == mock_data["age"]
        # Optionally, if the build method has some default values or computations:
        # assert flavor.some_attribute == some_expected_value
    @pytest.mark.asyncio
    async def test_build_with_missing_data(self, flavor_manager):
        # Define mock data with a missing key
        mock_data = {
            "name": "Rose",
            "age": 2
        }
        # If the build method is expected to raise an exception for missing data, test for that
        with pytest.raises(SomeSpecificException):
            await flavor_manager.build(**mock_data)
    @pytest.mark.asyncio
    async def test_add(self, flavor_manager, mock_session):
        flavor_data = FlavorFactory.build()
        mock_session.add.return_value = None
        mock_session.commit.return_value = None
        flavor = await flavor_manager.add(**flavor_data)
        mock_session.add.assert_called_once_with(flavor)
        mock_session.commit.assert_called_once()
        assert isinstance(flavor, Flavor)
    @pytest.mark.asyncio
    async def test_add_correctly_adds_flavor_to_database(self, flavor_manager, db_session):
        # Create a test flavor using the FlavorFactory without persisting it to the database
        test_flavor = FlavorFactory.build()
        # Add the flavor using the manager's add method
        added_flavor = await flavor_manager.add(flavor=test_flavor)
        # Fetch the flavor from the database directly
        result = await db_session.execute(select(Flavor).filter(Flavor.flavor_id == added_flavor.flavor_id))
        fetched_flavor = result.scalars().first()
        # Assert that the fetched flavor is not None and matches the added flavor
        assert fetched_flavor is not None
        assert fetched_flavor.flavor_id == added_flavor.flavor_id
        assert fetched_flavor.name == added_flavor.name
        # ... other attribute checks ...
    @pytest.mark.asyncio
    async def test_add_returns_correct_flavor_object(self, flavor_manager):
        # Create a test flavor using the FlavorFactory without persisting it to the database
        test_flavor = FlavorFactory.build()
        # Add the flavor using the manager's add method
        added_flavor = await flavor_manager.add(flavor=test_flavor)
        # Assert that the returned flavor matches the test flavor
        assert added_flavor.flavor_id == test_flavor.flavor_id
        assert added_flavor.name == test_flavor.name
        # ... other attribute checks ...
    @pytest.mark.asyncio
    async def test_get_by_id(self, flavor_manager, mock_session):
        flavor_data = FlavorFactory.build()
        mock_session.execute.return_value = AsyncMock(scalars=AsyncMock(first=AsyncMock(return_value=flavor_data)))
        flavor = await flavor_manager.get_by_id(1)
        mock_session.execute.assert_called_once()
        assert isinstance(flavor, Flavor)
    async def test_get_by_id(self, session: AsyncSession, sample_flavor: Flavor):
        manager = FlavorManager(session)
        retrieved_flavor = await manager.get_by_id(sample_flavor.flavor_id)
        assert retrieved_flavor is not None
        assert retrieved_flavor.flavor_id == sample_flavor.flavor_id
        assert retrieved_flavor.name == "Rose"
        assert retrieved_flavor.color == "Red"
    async def test_get_by_id_not_found(self, session: AsyncSession):
        manager = FlavorManager(session)
        non_existent_id = 9999  # An ID that's not in the database
        retrieved_flavor = await manager.get_by_id(non_existent_id)
        assert retrieved_flavor is None
    @pytest.mark.asyncio
    async def test_get_by_code_returns_flavor(self, flavor_manager, db_session):
        # Use your FlavorFactory to create and save a Flavor object
        code = uuid.uuid4()
        flavor = FlavorFactory(code=code)
        db_session.add(flavor)
        await db_session.commit()
        # Fetch the flavor using the manager's get_by_code method
        fetched_flavor = await flavor_manager.get_by_code(code)
        # Assert that the fetched flavor is not None and has the expected code
        assert fetched_flavor is not None
        assert fetched_flavor.code == code
    @pytest.mark.asyncio
    async def test_get_by_code_returns_none_for_nonexistent_code(self, flavor_manager):
        # Generate a random UUID that doesn't correspond to any Flavor in the database
        random_code = uuid.uuid4()
        # Try fetching a flavor using the manager's get_by_code method
        fetched_flavor = await flavor_manager.get_by_code(random_code)
        # Assert that the result is None since no flavor with the given code exists
        assert fetched_flavor is None
    @pytest.mark.asyncio
    async def test_update(self, flavor_manager, mock_session):
        flavor_data = FlavorFactory.build()
        updated_data = {"name": "Updated Flavor"}
        mock_session.execute.return_value = AsyncMock(scalars=AsyncMock(first=AsyncMock(return_value=flavor_data)))
        mock_session.commit.return_value = None
        updated_flavor = await flavor_manager.update(1, **updated_data)
        assert updated_flavor.name == "Updated Flavor"
        mock_session.commit.assert_called_once()
        assert isinstance(updated_flavor, Flavor)
    async def test_update_valid_flavor(self):
        # Mocking a flavor instance
        flavor = Flavor(flavor_id=1, name="Rose", code="ROSE123")
        # Mocking the commit method
        self.session_mock.commit = AsyncMock()
        # Update the flavor with new attributes
        updated_flavor = await self.manager.update(flavor, name="Red Rose", code="REDROSE123")
        # Assertions
        assert updated_flavor.name == "Red Rose"
        assert updated_flavor.code == "REDROSE123"
        self.session_mock.commit.assert_called_once()
    async def test_update_invalid_flavor(self):
        # None flavor
        flavor = None
        updated_flavor = await self.manager.update(flavor, name="Red Rose", code="REDROSE123")
        # Assertions
        assert updated_flavor is None
        self.session_mock.commit.assert_not_called()
    async def test_update_with_nonexistent_attribute(self):
        # Mocking a flavor instance
        flavor = Flavor(flavor_id=1, name="Rose", code="ROSE123")
        # Mocking the commit method
        self.session_mock.commit = AsyncMock()
        # This should raise an AttributeError since 'color' is not an attribute of Flavor
        with pytest.raises(AttributeError):
            await self.manager.update(flavor, color="Red")
        self.session_mock.commit.assert_not_called()
    @pytest.mark.asyncio
    async def test_delete(self, flavor_manager, mock_session):
        flavor_data = FlavorFactory.build()
        mock_session.execute.return_value = AsyncMock(scalars=AsyncMock(first=AsyncMock(return_value=flavor_data)))
        mock_session.delete.return_value = None
        mock_session.commit.return_value = None
        deleted_flavor = await flavor_manager.delete(1)
        mock_session.delete.assert_called_once_with(deleted_flavor)
        mock_session.commit.assert_called_once()
        assert isinstance(deleted_flavor, Flavor)
    @pytest.mark.asyncio
    async def test_delete_nonexistent(self, flavor_manager, mock_session):
        mock_session.execute.return_value = AsyncMock(scalars=AsyncMock(first=AsyncMock(return_value=None)))
        with pytest.raises(ValueError, match="Flavor not found"):
            await flavor_manager.delete(999)
    @pytest.mark.asyncio
    async def test_get_list(self, flavor_manager, mock_session):
        flavors_data = [FlavorFactory.build() for _ in range(5)]
        mock_session.execute.return_value = AsyncMock(scalars=AsyncMock(all=AsyncMock(return_value=flavors_data)))
        flavors = await flavor_manager.get_list()
        mock_session.execute.assert_called_once()
        assert len(flavors) == 5
        assert all(isinstance(flavor, Flavor) for flavor in flavors)
    @pytest.mark.asyncio
    async def test_to_json(self, flavor_manager):
        flavor_data = FlavorFactory.build()
        flavor = Flavor(**flavor_data)
        json_data = flavor_manager.to_json(flavor)
        assert json_data is not None
        # You might want to do more specific checks on the JSON structure
    @pytest.mark.asyncio
    async def test_from_json(self, flavor_manager):
        flavor_data = FlavorFactory.build()
        flavor = Flavor(**flavor_data)
        json_data = flavor_manager.to_json(flavor)
        deserialized_flavor = flavor_manager.from_json(json_data)
        assert isinstance(deserialized_flavor, Flavor)
        # Additional checks on the deserialized data can be added
    @pytest.mark.asyncio
    async def test_add_bulk(self, flavor_manager, mock_session):
        flavors_data = [FlavorFactory.build() for _ in range(5)]
        mock_session.add_all.return_value = None
        mock_session.commit.return_value = None
        flavors = await flavor_manager.add_bulk(flavors_data)
        mock_session.add_all.assert_called_once()
        mock_session.commit.assert_called_once()
        assert len(flavors) == 5
    @pytest.mark.asyncio
    async def test_update_bulk_success():
        manager = FlavorManager()
        session_mock = AsyncMock()
        manager.session = session_mock
        # Mocking flavor instances
        flavor1 = Flavor(flavor_id=1, name="Rose", code="ROSE123")
        flavor2 = Flavor(flavor_id=2, name="Tulip", code="TULIP123")
        # Mocking the get_by_id method to return the corresponding flavor
        async def mock_get_by_id(flavor_id):
            if flavor_id == 1:
                return flavor1
            if flavor_id == 2:
                return flavor2
        manager.get_by_id = mock_get_by_id
        # Mocking the commit method
        session_mock.commit = AsyncMock()
        # Update flavors
        updates = [{"flavor_id": 1, "name": "Red Rose"}, {"flavor_id": 2, "name": "Yellow Tulip"}]
        updated_flavors = await manager.update_bulk(updates)
        # Assertions
        assert len(updated_flavors) == 2
        assert updated_flavors[0].name == "Red Rose"
        assert updated_flavors[1].name == "Yellow Tulip"
        session_mock.commit.assert_called_once()
    @pytest.mark.asyncio
    async def test_update_bulk_missing_flavor_id():
        manager = FlavorManager()
        # No flavors to update since flavor_id is missing
        updates = [{"name": "Red Rose"}]
        updated_flavors = await manager.update_bulk(updates)
        # Assertions
        assert len(updated_flavors) == 0
    @pytest.mark.asyncio
    async def test_update_bulk_flavor_not_found():
        manager = FlavorManager()
        session_mock = AsyncMock()
        manager.session = session_mock
        # Mocking the get_by_id method to return None (flavor not found)
        manager.get_by_id = AsyncMock(return_value=None)
        # Mocking the commit method
        session_mock.commit = AsyncMock()
        # Update flavors
        updates = [{"flavor_id": 1, "name": "Red Rose"}]
        updated_flavors = await manager.update_bulk(updates)
        # Assertions
        assert len(updated_flavors) == 0
        session_mock.commit.assert_not_called()
    @pytest.mark.asyncio
    async def test_delete_bulk_success():
        manager = FlavorManager()
        session_mock = AsyncMock()
        manager.session = session_mock
        # Mocking flavor instances
        flavor1 = Flavor(flavor_id=1, name="Rose", code="ROSE123")
        flavor2 = Flavor(flavor_id=2, name="Tulip", code="TULIP123")
        # Mocking the get_by_id method to return the corresponding flavor
        async def mock_get_by_id(flavor_id):
            if flavor_id == 1:
                return flavor1
            if flavor_id == 2:
                return flavor2
        manager.get_by_id = mock_get_by_id
        # Mocking the commit and delete methods
        session_mock.commit = AsyncMock()
        session_mock.delete = AsyncMock()
        # Delete flavors
        flavor_ids = [1, 2]
        result = await manager.delete_bulk(flavor_ids)
        # Assertions
        assert result is True
        session_mock.delete.assert_called()
        session_mock.commit.assert_called_once()
    @pytest.mark.asyncio
    async def test_delete_bulk_some_flavors_not_found():
        manager = FlavorManager()
        session_mock = AsyncMock()
        manager.session = session_mock
        # Mocking the get_by_id method to return None (flavor not found)
        async def mock_get_by_id(flavor_id):
            if flavor_id == 1:
                return None
            if flavor_id == 2:
                return Flavor(flavor_id=2, name="Tulip", code="TULIP123")
        manager.get_by_id = mock_get_by_id
        # Mocking the commit and delete methods
        session_mock.commit = AsyncMock()
        session_mock.delete = AsyncMock()
        # Delete flavors
        flavor_ids = [1, 2]
        result = await manager.delete_bulk(flavor_ids)
        # Assertions
        assert result is True
        session_mock.delete.assert_called_once_with(Flavor(flavor_id=2, name="Tulip", code="TULIP123"))
        session_mock.commit.assert_called_once()
    @pytest.mark.asyncio
    async def test_delete_bulk_empty_list():
        manager = FlavorManager()
        session_mock = AsyncMock()
        manager.session = session_mock
        # Mocking the commit and delete methods
        session_mock.commit = AsyncMock()
        session_mock.delete = AsyncMock()
        # Delete flavors with an empty list
        flavor_ids = []
        result = await manager.delete_bulk(flavor_ids)
        # Assertions
        assert result is True
        session_mock.delete.assert_not_called()
        session_mock.commit.assert_not_called()
    @pytest.mark.asyncio
    async def test_count(self, flavor_manager, mock_session):
        flavors_data = [FlavorFactory.build() for _ in range(5)]
        mock_session.execute.return_value = AsyncMock(scalars=AsyncMock(all=AsyncMock(return_value=flavors_data)))
        count = await flavor_manager.count()
        mock_session.execute.assert_called_once()
        assert count == 5
    @pytest.mark.asyncio
    async def test_count_basic_functionality(async_session):
        # Add a flavor
        new_flavor = Flavor()
        async_session.add(new_flavor)
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
        # Add multiple flavors
        flavors = [Flavor() for _ in range(5)]
        async_session.add_all(flavors)
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
        # Add flavors
        flavors = [Flavor(name=f"Flavor_{i}") for i in range(5)]
        async_session.add_all(flavors)
        await async_session.commit()
        manager = YourManagerClass(session=async_session)
        sorted_flavors = await manager.get_sorted_list(sort_by="name")
        assert [flavor.name for flavor in sorted_flavors] == [f"Flavor_{i}" for i in range(5)]
    @pytest.mark.asyncio
    async def test_get_sorted_list_descending_sorting(async_session):
        # Add flavors
        flavors = [Flavor(name=f"Flavor_{i}") for i in range(5)]
        async_session.add_all(flavors)
        await async_session.commit()
        manager = YourManagerClass(session=async_session)
        sorted_flavors = await manager.get_sorted_list(sort_by="name", order="desc")
        assert [flavor.name for flavor in sorted_flavors] == [f"Flavor_{i}" for i in reversed(range(5))]
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
        sorted_flavors = await manager.get_sorted_list(sort_by="name")
        assert len(sorted_flavors) == 0
    @pytest.mark.asyncio
    async def test_refresh_basic(async_session):
        # Add a flavor
        flavor = Flavor(name="Flavor_1")
        async_session.add(flavor)
        await async_session.commit()
        # Modify the flavor directly in the database
        await async_session.execute('UPDATE flavors SET name = :new_name WHERE id = :flavor_id', {"new_name": "Modified_Flavor", "flavor_id": flavor.id})
        await async_session.commit()
        # Now, refresh the flavor using the manager function
        manager = YourManagerClass(session=async_session)
        refreshed_flavor = await manager.refresh(flavor)
        assert refreshed_flavor.name == "Modified_Flavor"
    @pytest.mark.asyncio
    async def test_refresh_nonexistent_flavor(async_session):
        flavor = Flavor(id=999, name="Nonexistent_Flavor")
        manager = YourManagerClass(session=async_session)
        with pytest.raises(Exception):  # Modify the exception type based on your ORM's behavior
            await manager.refresh(flavor)
    @pytest.mark.asyncio
    async def test_refresh_database_connection_issues(async_session, mocker):
        # Mock the session's refresh method to simulate a database connection error
        mocker.patch.object(async_session, 'refresh', side_effect=Exception("DB connection error"))
        flavor = Flavor(name="Flavor_1")
        manager = YourManagerClass(session=async_session)
        with pytest.raises(Exception, match="DB connection error"):
            await manager.refresh(flavor)
    @pytest.mark.asyncio
    async def test_exists_with_existing_flavor(async_session):
        # Add a flavor
        flavor = Flavor(name="Flavor_1")
        async_session.add(flavor)
        await async_session.commit()
        # Check if the flavor exists using the manager function
        manager = YourManagerClass(session=async_session)
        assert await manager.exists(flavor.id) == True
    @pytest.mark.asyncio
    async def test_exists_with_nonexistent_flavor(async_session):
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
        # Add a flavor with a specific pac_id
        flavor = Flavor(name="Flavor_1", pac_id=5)
        async_session.add(flavor)
        await async_session.commit()
        # Fetch the flavor using the manager function
        manager = YourManagerClass(session=async_session)
        fetched_flavors = await manager.get_by_pac_id(5)
        assert len(fetched_flavors) == 1
        assert fetched_flavors[0].name == "Flavor_1"
    @pytest.mark.asyncio
    async def test_get_by_pac_id_nonexistent(async_session):
        non_existent_id = 999
        manager = YourManagerClass(session=async_session)
        fetched_flavors = await manager.get_by_pac_id(non_existent_id)
        assert len(fetched_flavors) == 0
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
