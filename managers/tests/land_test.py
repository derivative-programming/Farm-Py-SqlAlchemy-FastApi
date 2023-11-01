import pytest
import uuid
from unittest.mock import AsyncMock, patch
from managers import LandManager, Land
from models.factory import LandFactory
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models import Base, Land
DATABASE_URL = "sqlite:///:memory:"
db_dialect = "sqlite"
class TestLandManager:
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
    async def land_manager(self, session):
        return LandManager(session)
    @pytest.mark.asyncio
    async def test_build(self, land_manager):
        # Define some mock data for our land
        mock_data = {
            "name": "Rose",
            "species": "Rosa",
            "age": 2
        }
        # Call the build function of the manager
        land = await land_manager.build(**mock_data)
        # Assert that the returned object is an instance of Land
        assert isinstance(land, Land)
        # Assert that the attributes of the land match our mock data
        assert land.name == mock_data["name"]
        assert land.species == mock_data["species"]
        assert land.age == mock_data["age"]
        # Optionally, if the build method has some default values or computations:
        # assert land.some_attribute == some_expected_value
    @pytest.mark.asyncio
    async def test_build_with_missing_data(self, land_manager):
        # Define mock data with a missing key
        mock_data = {
            "name": "Rose",
            "age": 2
        }
        # If the build method is expected to raise an exception for missing data, test for that
        with pytest.raises(SomeSpecificException):
            await land_manager.build(**mock_data)
    @pytest.mark.asyncio
    async def test_add(self, land_manager, mock_session):
        land_data = LandFactory.build()
        mock_session.add.return_value = None
        mock_session.commit.return_value = None
        land = await land_manager.add(**land_data)
        mock_session.add.assert_called_once_with(land)
        mock_session.commit.assert_called_once()
        assert isinstance(land, Land)
    @pytest.mark.asyncio
    async def test_add_correctly_adds_land_to_database(self, land_manager, db_session):
        # Create a test land using the LandFactory without persisting it to the database
        test_land = LandFactory.build()
        # Add the land using the manager's add method
        added_land = await land_manager.add(land=test_land)
        # Fetch the land from the database directly
        result = await db_session.execute(select(Land).filter(Land.land_id == added_land.land_id))
        fetched_land = result.scalars().first()
        # Assert that the fetched land is not None and matches the added land
        assert fetched_land is not None
        assert fetched_land.land_id == added_land.land_id
        assert fetched_land.name == added_land.name
        # ... other attribute checks ...
    @pytest.mark.asyncio
    async def test_add_returns_correct_land_object(self, land_manager):
        # Create a test land using the LandFactory without persisting it to the database
        test_land = LandFactory.build()
        # Add the land using the manager's add method
        added_land = await land_manager.add(land=test_land)
        # Assert that the returned land matches the test land
        assert added_land.land_id == test_land.land_id
        assert added_land.name == test_land.name
        # ... other attribute checks ...
    @pytest.mark.asyncio
    async def test_get_by_id(self, land_manager, mock_session):
        land_data = LandFactory.build()
        mock_session.execute.return_value = AsyncMock(scalars=AsyncMock(first=AsyncMock(return_value=land_data)))
        land = await land_manager.get_by_id(1)
        mock_session.execute.assert_called_once()
        assert isinstance(land, Land)
    async def test_get_by_id(self, session: AsyncSession, sample_land: Land):
        manager = LandManager(session)
        retrieved_land = await manager.get_by_id(sample_land.land_id)
        assert retrieved_land is not None
        assert retrieved_land.land_id == sample_land.land_id
        assert retrieved_land.name == "Rose"
        assert retrieved_land.color == "Red"
    async def test_get_by_id_not_found(self, session: AsyncSession):
        manager = LandManager(session)
        non_existent_id = 9999  # An ID that's not in the database
        retrieved_land = await manager.get_by_id(non_existent_id)
        assert retrieved_land is None
    @pytest.mark.asyncio
    async def test_get_by_code_returns_land(self, land_manager, db_session):
        # Use your LandFactory to create and save a Land object
        code = uuid.uuid4()
        land = LandFactory(code=code)
        db_session.add(land)
        await db_session.commit()
        # Fetch the land using the manager's get_by_code method
        fetched_land = await land_manager.get_by_code(code)
        # Assert that the fetched land is not None and has the expected code
        assert fetched_land is not None
        assert fetched_land.code == code
    @pytest.mark.asyncio
    async def test_get_by_code_returns_none_for_nonexistent_code(self, land_manager):
        # Generate a random UUID that doesn't correspond to any Land in the database
        random_code = uuid.uuid4()
        # Try fetching a land using the manager's get_by_code method
        fetched_land = await land_manager.get_by_code(random_code)
        # Assert that the result is None since no land with the given code exists
        assert fetched_land is None
    @pytest.mark.asyncio
    async def test_update(self, land_manager, mock_session):
        land_data = LandFactory.build()
        updated_data = {"name": "Updated Land"}
        mock_session.execute.return_value = AsyncMock(scalars=AsyncMock(first=AsyncMock(return_value=land_data)))
        mock_session.commit.return_value = None
        updated_land = await land_manager.update(1, **updated_data)
        assert updated_land.name == "Updated Land"
        mock_session.commit.assert_called_once()
        assert isinstance(updated_land, Land)
    async def test_update_valid_land(self):
        # Mocking a land instance
        land = Land(land_id=1, name="Rose", code="ROSE123")
        # Mocking the commit method
        self.session_mock.commit = AsyncMock()
        # Update the land with new attributes
        updated_land = await self.manager.update(land, name="Red Rose", code="REDROSE123")
        # Assertions
        assert updated_land.name == "Red Rose"
        assert updated_land.code == "REDROSE123"
        self.session_mock.commit.assert_called_once()
    async def test_update_invalid_land(self):
        # None land
        land = None
        updated_land = await self.manager.update(land, name="Red Rose", code="REDROSE123")
        # Assertions
        assert updated_land is None
        self.session_mock.commit.assert_not_called()
    async def test_update_with_nonexistent_attribute(self):
        # Mocking a land instance
        land = Land(land_id=1, name="Rose", code="ROSE123")
        # Mocking the commit method
        self.session_mock.commit = AsyncMock()
        # This should raise an AttributeError since 'color' is not an attribute of Land
        with pytest.raises(AttributeError):
            await self.manager.update(land, color="Red")
        self.session_mock.commit.assert_not_called()
    @pytest.mark.asyncio
    async def test_delete(self, land_manager, mock_session):
        land_data = LandFactory.build()
        mock_session.execute.return_value = AsyncMock(scalars=AsyncMock(first=AsyncMock(return_value=land_data)))
        mock_session.delete.return_value = None
        mock_session.commit.return_value = None
        deleted_land = await land_manager.delete(1)
        mock_session.delete.assert_called_once_with(deleted_land)
        mock_session.commit.assert_called_once()
        assert isinstance(deleted_land, Land)
    @pytest.mark.asyncio
    async def test_delete_nonexistent(self, land_manager, mock_session):
        mock_session.execute.return_value = AsyncMock(scalars=AsyncMock(first=AsyncMock(return_value=None)))
        with pytest.raises(ValueError, match="Land not found"):
            await land_manager.delete(999)
    @pytest.mark.asyncio
    async def test_get_list(self, land_manager, mock_session):
        lands_data = [LandFactory.build() for _ in range(5)]
        mock_session.execute.return_value = AsyncMock(scalars=AsyncMock(all=AsyncMock(return_value=lands_data)))
        lands = await land_manager.get_list()
        mock_session.execute.assert_called_once()
        assert len(lands) == 5
        assert all(isinstance(land, Land) for land in lands)
    @pytest.mark.asyncio
    async def test_to_json(self, land_manager):
        land_data = LandFactory.build()
        land = Land(**land_data)
        json_data = land_manager.to_json(land)
        assert json_data is not None
        # You might want to do more specific checks on the JSON structure
    @pytest.mark.asyncio
    async def test_from_json(self, land_manager):
        land_data = LandFactory.build()
        land = Land(**land_data)
        json_data = land_manager.to_json(land)
        deserialized_land = land_manager.from_json(json_data)
        assert isinstance(deserialized_land, Land)
        # Additional checks on the deserialized data can be added
    @pytest.mark.asyncio
    async def test_add_bulk(self, land_manager, mock_session):
        lands_data = [LandFactory.build() for _ in range(5)]
        mock_session.add_all.return_value = None
        mock_session.commit.return_value = None
        lands = await land_manager.add_bulk(lands_data)
        mock_session.add_all.assert_called_once()
        mock_session.commit.assert_called_once()
        assert len(lands) == 5
    @pytest.mark.asyncio
    async def test_update_bulk_success():
        manager = LandManager()
        session_mock = AsyncMock()
        manager.session = session_mock
        # Mocking land instances
        land1 = Land(land_id=1, name="Rose", code="ROSE123")
        land2 = Land(land_id=2, name="Tulip", code="TULIP123")
        # Mocking the get_by_id method to return the corresponding land
        async def mock_get_by_id(land_id):
            if land_id == 1:
                return land1
            if land_id == 2:
                return land2
        manager.get_by_id = mock_get_by_id
        # Mocking the commit method
        session_mock.commit = AsyncMock()
        # Update lands
        updates = [{"land_id": 1, "name": "Red Rose"}, {"land_id": 2, "name": "Yellow Tulip"}]
        updated_lands = await manager.update_bulk(updates)
        # Assertions
        assert len(updated_lands) == 2
        assert updated_lands[0].name == "Red Rose"
        assert updated_lands[1].name == "Yellow Tulip"
        session_mock.commit.assert_called_once()
    @pytest.mark.asyncio
    async def test_update_bulk_missing_land_id():
        manager = LandManager()
        # No lands to update since land_id is missing
        updates = [{"name": "Red Rose"}]
        updated_lands = await manager.update_bulk(updates)
        # Assertions
        assert len(updated_lands) == 0
    @pytest.mark.asyncio
    async def test_update_bulk_land_not_found():
        manager = LandManager()
        session_mock = AsyncMock()
        manager.session = session_mock
        # Mocking the get_by_id method to return None (land not found)
        manager.get_by_id = AsyncMock(return_value=None)
        # Mocking the commit method
        session_mock.commit = AsyncMock()
        # Update lands
        updates = [{"land_id": 1, "name": "Red Rose"}]
        updated_lands = await manager.update_bulk(updates)
        # Assertions
        assert len(updated_lands) == 0
        session_mock.commit.assert_not_called()
    @pytest.mark.asyncio
    async def test_delete_bulk_success():
        manager = LandManager()
        session_mock = AsyncMock()
        manager.session = session_mock
        # Mocking land instances
        land1 = Land(land_id=1, name="Rose", code="ROSE123")
        land2 = Land(land_id=2, name="Tulip", code="TULIP123")
        # Mocking the get_by_id method to return the corresponding land
        async def mock_get_by_id(land_id):
            if land_id == 1:
                return land1
            if land_id == 2:
                return land2
        manager.get_by_id = mock_get_by_id
        # Mocking the commit and delete methods
        session_mock.commit = AsyncMock()
        session_mock.delete = AsyncMock()
        # Delete lands
        land_ids = [1, 2]
        result = await manager.delete_bulk(land_ids)
        # Assertions
        assert result is True
        session_mock.delete.assert_called()
        session_mock.commit.assert_called_once()
    @pytest.mark.asyncio
    async def test_delete_bulk_some_lands_not_found():
        manager = LandManager()
        session_mock = AsyncMock()
        manager.session = session_mock
        # Mocking the get_by_id method to return None (land not found)
        async def mock_get_by_id(land_id):
            if land_id == 1:
                return None
            if land_id == 2:
                return Land(land_id=2, name="Tulip", code="TULIP123")
        manager.get_by_id = mock_get_by_id
        # Mocking the commit and delete methods
        session_mock.commit = AsyncMock()
        session_mock.delete = AsyncMock()
        # Delete lands
        land_ids = [1, 2]
        result = await manager.delete_bulk(land_ids)
        # Assertions
        assert result is True
        session_mock.delete.assert_called_once_with(Land(land_id=2, name="Tulip", code="TULIP123"))
        session_mock.commit.assert_called_once()
    @pytest.mark.asyncio
    async def test_delete_bulk_empty_list():
        manager = LandManager()
        session_mock = AsyncMock()
        manager.session = session_mock
        # Mocking the commit and delete methods
        session_mock.commit = AsyncMock()
        session_mock.delete = AsyncMock()
        # Delete lands with an empty list
        land_ids = []
        result = await manager.delete_bulk(land_ids)
        # Assertions
        assert result is True
        session_mock.delete.assert_not_called()
        session_mock.commit.assert_not_called()
    @pytest.mark.asyncio
    async def test_count(self, land_manager, mock_session):
        lands_data = [LandFactory.build() for _ in range(5)]
        mock_session.execute.return_value = AsyncMock(scalars=AsyncMock(all=AsyncMock(return_value=lands_data)))
        count = await land_manager.count()
        mock_session.execute.assert_called_once()
        assert count == 5
    @pytest.mark.asyncio
    async def test_count_basic_functionality(async_session):
        # Add a land
        new_land = Land()
        async_session.add(new_land)
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
        # Add multiple lands
        lands = [Land() for _ in range(5)]
        async_session.add_all(lands)
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
        # Add lands
        lands = [Land(name=f"Land_{i}") for i in range(5)]
        async_session.add_all(lands)
        await async_session.commit()
        manager = YourManagerClass(session=async_session)
        sorted_lands = await manager.get_sorted_list(sort_by="name")
        assert [land.name for land in sorted_lands] == [f"Land_{i}" for i in range(5)]
    @pytest.mark.asyncio
    async def test_get_sorted_list_descending_sorting(async_session):
        # Add lands
        lands = [Land(name=f"Land_{i}") for i in range(5)]
        async_session.add_all(lands)
        await async_session.commit()
        manager = YourManagerClass(session=async_session)
        sorted_lands = await manager.get_sorted_list(sort_by="name", order="desc")
        assert [land.name for land in sorted_lands] == [f"Land_{i}" for i in reversed(range(5))]
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
        sorted_lands = await manager.get_sorted_list(sort_by="name")
        assert len(sorted_lands) == 0
    @pytest.mark.asyncio
    async def test_refresh_basic(async_session):
        # Add a land
        land = Land(name="Land_1")
        async_session.add(land)
        await async_session.commit()
        # Modify the land directly in the database
        await async_session.execute('UPDATE lands SET name = :new_name WHERE id = :land_id', {"new_name": "Modified_Land", "land_id": land.id})
        await async_session.commit()
        # Now, refresh the land using the manager function
        manager = YourManagerClass(session=async_session)
        refreshed_land = await manager.refresh(land)
        assert refreshed_land.name == "Modified_Land"
    @pytest.mark.asyncio
    async def test_refresh_nonexistent_land(async_session):
        land = Land(id=999, name="Nonexistent_Land")
        manager = YourManagerClass(session=async_session)
        with pytest.raises(Exception):  # Modify the exception type based on your ORM's behavior
            await manager.refresh(land)
    @pytest.mark.asyncio
    async def test_refresh_database_connection_issues(async_session, mocker):
        # Mock the session's refresh method to simulate a database connection error
        mocker.patch.object(async_session, 'refresh', side_effect=Exception("DB connection error"))
        land = Land(name="Land_1")
        manager = YourManagerClass(session=async_session)
        with pytest.raises(Exception, match="DB connection error"):
            await manager.refresh(land)
    @pytest.mark.asyncio
    async def test_exists_with_existing_land(async_session):
        # Add a land
        land = Land(name="Land_1")
        async_session.add(land)
        await async_session.commit()
        # Check if the land exists using the manager function
        manager = YourManagerClass(session=async_session)
        assert await manager.exists(land.id) == True
    @pytest.mark.asyncio
    async def test_exists_with_nonexistent_land(async_session):
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
        # Add a land with a specific pac_id
        land = Land(name="Land_1", pac_id=5)
        async_session.add(land)
        await async_session.commit()
        # Fetch the land using the manager function
        manager = YourManagerClass(session=async_session)
        fetched_lands = await manager.get_by_pac_id(5)
        assert len(fetched_lands) == 1
        assert fetched_lands[0].name == "Land_1"
    @pytest.mark.asyncio
    async def test_get_by_pac_id_nonexistent(async_session):
        non_existent_id = 999
        manager = YourManagerClass(session=async_session)
        fetched_lands = await manager.get_by_pac_id(non_existent_id)
        assert len(fetched_lands) == 0
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
