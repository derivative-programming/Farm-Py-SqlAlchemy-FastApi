import pytest
import uuid
from unittest.mock import AsyncMock, patch
from managers import TriStateFilterManager, TriStateFilter
from models.factory import TriStateFilterFactory
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models import Base, TriStateFilter
DATABASE_URL = "sqlite:///:memory:"
db_dialect = "sqlite"
class TestTriStateFilterManager:
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
    async def tri_state_filter_manager(self, session):
        return TriStateFilterManager(session)
    @pytest.mark.asyncio
    async def test_build(self, tri_state_filter_manager):
        # Define some mock data for our tri_state_filter
        mock_data = {
            "name": "Rose",
            "species": "Rosa",
            "age": 2
        }
        # Call the build function of the manager
        tri_state_filter = await tri_state_filter_manager.build(**mock_data)
        # Assert that the returned object is an instance of TriStateFilter
        assert isinstance(tri_state_filter, TriStateFilter)
        # Assert that the attributes of the tri_state_filter match our mock data
        assert tri_state_filter.name == mock_data["name"]
        assert tri_state_filter.species == mock_data["species"]
        assert tri_state_filter.age == mock_data["age"]
        # Optionally, if the build method has some default values or computations:
        # assert tri_state_filter.some_attribute == some_expected_value
    @pytest.mark.asyncio
    async def test_build_with_missing_data(self, tri_state_filter_manager):
        # Define mock data with a missing key
        mock_data = {
            "name": "Rose",
            "age": 2
        }
        # If the build method is expected to raise an exception for missing data, test for that
        with pytest.raises(SomeSpecificException):
            await tri_state_filter_manager.build(**mock_data)
    @pytest.mark.asyncio
    async def test_add(self, tri_state_filter_manager, mock_session):
        tri_state_filter_data = TriStateFilterFactory.build()
        mock_session.add.return_value = None
        mock_session.commit.return_value = None
        tri_state_filter = await tri_state_filter_manager.add(**tri_state_filter_data)
        mock_session.add.assert_called_once_with(tri_state_filter)
        mock_session.commit.assert_called_once()
        assert isinstance(tri_state_filter, TriStateFilter)
    @pytest.mark.asyncio
    async def test_add_correctly_adds_tri_state_filter_to_database(self, tri_state_filter_manager, db_session):
        # Create a test tri_state_filter using the TriStateFilterFactory without persisting it to the database
        test_tri_state_filter = TriStateFilterFactory.build()
        # Add the tri_state_filter using the manager's add method
        added_tri_state_filter = await tri_state_filter_manager.add(tri_state_filter=test_tri_state_filter)
        # Fetch the tri_state_filter from the database directly
        result = await db_session.execute(select(TriStateFilter).filter(TriStateFilter.tri_state_filter_id == added_tri_state_filter.tri_state_filter_id))
        fetched_tri_state_filter = result.scalars().first()
        # Assert that the fetched tri_state_filter is not None and matches the added tri_state_filter
        assert fetched_tri_state_filter is not None
        assert fetched_tri_state_filter.tri_state_filter_id == added_tri_state_filter.tri_state_filter_id
        assert fetched_tri_state_filter.name == added_tri_state_filter.name
        # ... other attribute checks ...
    @pytest.mark.asyncio
    async def test_add_returns_correct_tri_state_filter_object(self, tri_state_filter_manager):
        # Create a test tri_state_filter using the TriStateFilterFactory without persisting it to the database
        test_tri_state_filter = TriStateFilterFactory.build()
        # Add the tri_state_filter using the manager's add method
        added_tri_state_filter = await tri_state_filter_manager.add(tri_state_filter=test_tri_state_filter)
        # Assert that the returned tri_state_filter matches the test tri_state_filter
        assert added_tri_state_filter.tri_state_filter_id == test_tri_state_filter.tri_state_filter_id
        assert added_tri_state_filter.name == test_tri_state_filter.name
        # ... other attribute checks ...
    @pytest.mark.asyncio
    async def test_get_by_id(self, tri_state_filter_manager, mock_session):
        tri_state_filter_data = TriStateFilterFactory.build()
        mock_session.execute.return_value = AsyncMock(scalars=AsyncMock(first=AsyncMock(return_value=tri_state_filter_data)))
        tri_state_filter = await tri_state_filter_manager.get_by_id(1)
        mock_session.execute.assert_called_once()
        assert isinstance(tri_state_filter, TriStateFilter)
    async def test_get_by_id(self, session: AsyncSession, sample_tri_state_filter: TriStateFilter):
        manager = TriStateFilterManager(session)
        retrieved_tri_state_filter = await manager.get_by_id(sample_tri_state_filter.tri_state_filter_id)
        assert retrieved_tri_state_filter is not None
        assert retrieved_tri_state_filter.tri_state_filter_id == sample_tri_state_filter.tri_state_filter_id
        assert retrieved_tri_state_filter.name == "Rose"
        assert retrieved_tri_state_filter.color == "Red"
    async def test_get_by_id_not_found(self, session: AsyncSession):
        manager = TriStateFilterManager(session)
        non_existent_id = 9999  # An ID that's not in the database
        retrieved_tri_state_filter = await manager.get_by_id(non_existent_id)
        assert retrieved_tri_state_filter is None
    @pytest.mark.asyncio
    async def test_get_by_code_returns_tri_state_filter(self, tri_state_filter_manager, db_session):
        # Use your TriStateFilterFactory to create and save a TriStateFilter object
        code = uuid.uuid4()
        tri_state_filter = TriStateFilterFactory(code=code)
        db_session.add(tri_state_filter)
        await db_session.commit()
        # Fetch the tri_state_filter using the manager's get_by_code method
        fetched_tri_state_filter = await tri_state_filter_manager.get_by_code(code)
        # Assert that the fetched tri_state_filter is not None and has the expected code
        assert fetched_tri_state_filter is not None
        assert fetched_tri_state_filter.code == code
    @pytest.mark.asyncio
    async def test_get_by_code_returns_none_for_nonexistent_code(self, tri_state_filter_manager):
        # Generate a random UUID that doesn't correspond to any TriStateFilter in the database
        random_code = uuid.uuid4()
        # Try fetching a tri_state_filter using the manager's get_by_code method
        fetched_tri_state_filter = await tri_state_filter_manager.get_by_code(random_code)
        # Assert that the result is None since no tri_state_filter with the given code exists
        assert fetched_tri_state_filter is None
    @pytest.mark.asyncio
    async def test_update(self, tri_state_filter_manager, mock_session):
        tri_state_filter_data = TriStateFilterFactory.build()
        updated_data = {"name": "Updated TriStateFilter"}
        mock_session.execute.return_value = AsyncMock(scalars=AsyncMock(first=AsyncMock(return_value=tri_state_filter_data)))
        mock_session.commit.return_value = None
        updated_tri_state_filter = await tri_state_filter_manager.update(1, **updated_data)
        assert updated_tri_state_filter.name == "Updated TriStateFilter"
        mock_session.commit.assert_called_once()
        assert isinstance(updated_tri_state_filter, TriStateFilter)
    async def test_update_valid_tri_state_filter(self):
        # Mocking a tri_state_filter instance
        tri_state_filter = TriStateFilter(tri_state_filter_id=1, name="Rose", code="ROSE123")
        # Mocking the commit method
        self.session_mock.commit = AsyncMock()
        # Update the tri_state_filter with new attributes
        updated_tri_state_filter = await self.manager.update(tri_state_filter, name="Red Rose", code="REDROSE123")
        # Assertions
        assert updated_tri_state_filter.name == "Red Rose"
        assert updated_tri_state_filter.code == "REDROSE123"
        self.session_mock.commit.assert_called_once()
    async def test_update_invalid_tri_state_filter(self):
        # None tri_state_filter
        tri_state_filter = None
        updated_tri_state_filter = await self.manager.update(tri_state_filter, name="Red Rose", code="REDROSE123")
        # Assertions
        assert updated_tri_state_filter is None
        self.session_mock.commit.assert_not_called()
    async def test_update_with_nonexistent_attribute(self):
        # Mocking a tri_state_filter instance
        tri_state_filter = TriStateFilter(tri_state_filter_id=1, name="Rose", code="ROSE123")
        # Mocking the commit method
        self.session_mock.commit = AsyncMock()
        # This should raise an AttributeError since 'color' is not an attribute of TriStateFilter
        with pytest.raises(AttributeError):
            await self.manager.update(tri_state_filter, color="Red")
        self.session_mock.commit.assert_not_called()
    @pytest.mark.asyncio
    async def test_delete(self, tri_state_filter_manager, mock_session):
        tri_state_filter_data = TriStateFilterFactory.build()
        mock_session.execute.return_value = AsyncMock(scalars=AsyncMock(first=AsyncMock(return_value=tri_state_filter_data)))
        mock_session.delete.return_value = None
        mock_session.commit.return_value = None
        deleted_tri_state_filter = await tri_state_filter_manager.delete(1)
        mock_session.delete.assert_called_once_with(deleted_tri_state_filter)
        mock_session.commit.assert_called_once()
        assert isinstance(deleted_tri_state_filter, TriStateFilter)
    @pytest.mark.asyncio
    async def test_delete_nonexistent(self, tri_state_filter_manager, mock_session):
        mock_session.execute.return_value = AsyncMock(scalars=AsyncMock(first=AsyncMock(return_value=None)))
        with pytest.raises(ValueError, match="TriStateFilter not found"):
            await tri_state_filter_manager.delete(999)
    @pytest.mark.asyncio
    async def test_get_list(self, tri_state_filter_manager, mock_session):
        tri_state_filters_data = [TriStateFilterFactory.build() for _ in range(5)]
        mock_session.execute.return_value = AsyncMock(scalars=AsyncMock(all=AsyncMock(return_value=tri_state_filters_data)))
        tri_state_filters = await tri_state_filter_manager.get_list()
        mock_session.execute.assert_called_once()
        assert len(tri_state_filters) == 5
        assert all(isinstance(tri_state_filter, TriStateFilter) for tri_state_filter in tri_state_filters)
    @pytest.mark.asyncio
    async def test_to_json(self, tri_state_filter_manager):
        tri_state_filter_data = TriStateFilterFactory.build()
        tri_state_filter = TriStateFilter(**tri_state_filter_data)
        json_data = tri_state_filter_manager.to_json(tri_state_filter)
        assert json_data is not None
        # You might want to do more specific checks on the JSON structure
    @pytest.mark.asyncio
    async def test_from_json(self, tri_state_filter_manager):
        tri_state_filter_data = TriStateFilterFactory.build()
        tri_state_filter = TriStateFilter(**tri_state_filter_data)
        json_data = tri_state_filter_manager.to_json(tri_state_filter)
        deserialized_tri_state_filter = tri_state_filter_manager.from_json(json_data)
        assert isinstance(deserialized_tri_state_filter, TriStateFilter)
        # Additional checks on the deserialized data can be added
    @pytest.mark.asyncio
    async def test_add_bulk(self, tri_state_filter_manager, mock_session):
        tri_state_filters_data = [TriStateFilterFactory.build() for _ in range(5)]
        mock_session.add_all.return_value = None
        mock_session.commit.return_value = None
        tri_state_filters = await tri_state_filter_manager.add_bulk(tri_state_filters_data)
        mock_session.add_all.assert_called_once()
        mock_session.commit.assert_called_once()
        assert len(tri_state_filters) == 5
    @pytest.mark.asyncio
    async def test_update_bulk_success():
        manager = TriStateFilterManager()
        session_mock = AsyncMock()
        manager.session = session_mock
        # Mocking tri_state_filter instances
        tri_state_filter1 = TriStateFilter(tri_state_filter_id=1, name="Rose", code="ROSE123")
        tri_state_filter2 = TriStateFilter(tri_state_filter_id=2, name="Tulip", code="TULIP123")
        # Mocking the get_by_id method to return the corresponding tri_state_filter
        async def mock_get_by_id(tri_state_filter_id):
            if tri_state_filter_id == 1:
                return tri_state_filter1
            if tri_state_filter_id == 2:
                return tri_state_filter2
        manager.get_by_id = mock_get_by_id
        # Mocking the commit method
        session_mock.commit = AsyncMock()
        # Update tri_state_filters
        updates = [{"tri_state_filter_id": 1, "name": "Red Rose"}, {"tri_state_filter_id": 2, "name": "Yellow Tulip"}]
        updated_tri_state_filters = await manager.update_bulk(updates)
        # Assertions
        assert len(updated_tri_state_filters) == 2
        assert updated_tri_state_filters[0].name == "Red Rose"
        assert updated_tri_state_filters[1].name == "Yellow Tulip"
        session_mock.commit.assert_called_once()
    @pytest.mark.asyncio
    async def test_update_bulk_missing_tri_state_filter_id():
        manager = TriStateFilterManager()
        # No tri_state_filters to update since tri_state_filter_id is missing
        updates = [{"name": "Red Rose"}]
        updated_tri_state_filters = await manager.update_bulk(updates)
        # Assertions
        assert len(updated_tri_state_filters) == 0
    @pytest.mark.asyncio
    async def test_update_bulk_tri_state_filter_not_found():
        manager = TriStateFilterManager()
        session_mock = AsyncMock()
        manager.session = session_mock
        # Mocking the get_by_id method to return None (tri_state_filter not found)
        manager.get_by_id = AsyncMock(return_value=None)
        # Mocking the commit method
        session_mock.commit = AsyncMock()
        # Update tri_state_filters
        updates = [{"tri_state_filter_id": 1, "name": "Red Rose"}]
        updated_tri_state_filters = await manager.update_bulk(updates)
        # Assertions
        assert len(updated_tri_state_filters) == 0
        session_mock.commit.assert_not_called()
    @pytest.mark.asyncio
    async def test_delete_bulk_success():
        manager = TriStateFilterManager()
        session_mock = AsyncMock()
        manager.session = session_mock
        # Mocking tri_state_filter instances
        tri_state_filter1 = TriStateFilter(tri_state_filter_id=1, name="Rose", code="ROSE123")
        tri_state_filter2 = TriStateFilter(tri_state_filter_id=2, name="Tulip", code="TULIP123")
        # Mocking the get_by_id method to return the corresponding tri_state_filter
        async def mock_get_by_id(tri_state_filter_id):
            if tri_state_filter_id == 1:
                return tri_state_filter1
            if tri_state_filter_id == 2:
                return tri_state_filter2
        manager.get_by_id = mock_get_by_id
        # Mocking the commit and delete methods
        session_mock.commit = AsyncMock()
        session_mock.delete = AsyncMock()
        # Delete tri_state_filters
        tri_state_filter_ids = [1, 2]
        result = await manager.delete_bulk(tri_state_filter_ids)
        # Assertions
        assert result is True
        session_mock.delete.assert_called()
        session_mock.commit.assert_called_once()
    @pytest.mark.asyncio
    async def test_delete_bulk_some_tri_state_filters_not_found():
        manager = TriStateFilterManager()
        session_mock = AsyncMock()
        manager.session = session_mock
        # Mocking the get_by_id method to return None (tri_state_filter not found)
        async def mock_get_by_id(tri_state_filter_id):
            if tri_state_filter_id == 1:
                return None
            if tri_state_filter_id == 2:
                return TriStateFilter(tri_state_filter_id=2, name="Tulip", code="TULIP123")
        manager.get_by_id = mock_get_by_id
        # Mocking the commit and delete methods
        session_mock.commit = AsyncMock()
        session_mock.delete = AsyncMock()
        # Delete tri_state_filters
        tri_state_filter_ids = [1, 2]
        result = await manager.delete_bulk(tri_state_filter_ids)
        # Assertions
        assert result is True
        session_mock.delete.assert_called_once_with(TriStateFilter(tri_state_filter_id=2, name="Tulip", code="TULIP123"))
        session_mock.commit.assert_called_once()
    @pytest.mark.asyncio
    async def test_delete_bulk_empty_list():
        manager = TriStateFilterManager()
        session_mock = AsyncMock()
        manager.session = session_mock
        # Mocking the commit and delete methods
        session_mock.commit = AsyncMock()
        session_mock.delete = AsyncMock()
        # Delete tri_state_filters with an empty list
        tri_state_filter_ids = []
        result = await manager.delete_bulk(tri_state_filter_ids)
        # Assertions
        assert result is True
        session_mock.delete.assert_not_called()
        session_mock.commit.assert_not_called()
    @pytest.mark.asyncio
    async def test_count(self, tri_state_filter_manager, mock_session):
        tri_state_filters_data = [TriStateFilterFactory.build() for _ in range(5)]
        mock_session.execute.return_value = AsyncMock(scalars=AsyncMock(all=AsyncMock(return_value=tri_state_filters_data)))
        count = await tri_state_filter_manager.count()
        mock_session.execute.assert_called_once()
        assert count == 5
    @pytest.mark.asyncio
    async def test_count_basic_functionality(async_session):
        # Add a tri_state_filter
        new_tri_state_filter = TriStateFilter()
        async_session.add(new_tri_state_filter)
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
        # Add multiple tri_state_filters
        tri_state_filters = [TriStateFilter() for _ in range(5)]
        async_session.add_all(tri_state_filters)
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
        # Add tri_state_filters
        tri_state_filters = [TriStateFilter(name=f"TriStateFilter_{i}") for i in range(5)]
        async_session.add_all(tri_state_filters)
        await async_session.commit()
        manager = YourManagerClass(session=async_session)
        sorted_tri_state_filters = await manager.get_sorted_list(sort_by="name")
        assert [tri_state_filter.name for tri_state_filter in sorted_tri_state_filters] == [f"TriStateFilter_{i}" for i in range(5)]
    @pytest.mark.asyncio
    async def test_get_sorted_list_descending_sorting(async_session):
        # Add tri_state_filters
        tri_state_filters = [TriStateFilter(name=f"TriStateFilter_{i}") for i in range(5)]
        async_session.add_all(tri_state_filters)
        await async_session.commit()
        manager = YourManagerClass(session=async_session)
        sorted_tri_state_filters = await manager.get_sorted_list(sort_by="name", order="desc")
        assert [tri_state_filter.name for tri_state_filter in sorted_tri_state_filters] == [f"TriStateFilter_{i}" for i in reversed(range(5))]
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
        sorted_tri_state_filters = await manager.get_sorted_list(sort_by="name")
        assert len(sorted_tri_state_filters) == 0
    @pytest.mark.asyncio
    async def test_refresh_basic(async_session):
        # Add a tri_state_filter
        tri_state_filter = TriStateFilter(name="TriStateFilter_1")
        async_session.add(tri_state_filter)
        await async_session.commit()
        # Modify the tri_state_filter directly in the database
        await async_session.execute('UPDATE tri_state_filters SET name = :new_name WHERE id = :tri_state_filter_id', {"new_name": "Modified_TriStateFilter", "tri_state_filter_id": tri_state_filter.id})
        await async_session.commit()
        # Now, refresh the tri_state_filter using the manager function
        manager = YourManagerClass(session=async_session)
        refreshed_tri_state_filter = await manager.refresh(tri_state_filter)
        assert refreshed_tri_state_filter.name == "Modified_TriStateFilter"
    @pytest.mark.asyncio
    async def test_refresh_nonexistent_tri_state_filter(async_session):
        tri_state_filter = TriStateFilter(id=999, name="Nonexistent_TriStateFilter")
        manager = YourManagerClass(session=async_session)
        with pytest.raises(Exception):  # Modify the exception type based on your ORM's behavior
            await manager.refresh(tri_state_filter)
    @pytest.mark.asyncio
    async def test_refresh_database_connection_issues(async_session, mocker):
        # Mock the session's refresh method to simulate a database connection error
        mocker.patch.object(async_session, 'refresh', side_effect=Exception("DB connection error"))
        tri_state_filter = TriStateFilter(name="TriStateFilter_1")
        manager = YourManagerClass(session=async_session)
        with pytest.raises(Exception, match="DB connection error"):
            await manager.refresh(tri_state_filter)
    @pytest.mark.asyncio
    async def test_exists_with_existing_tri_state_filter(async_session):
        # Add a tri_state_filter
        tri_state_filter = TriStateFilter(name="TriStateFilter_1")
        async_session.add(tri_state_filter)
        await async_session.commit()
        # Check if the tri_state_filter exists using the manager function
        manager = YourManagerClass(session=async_session)
        assert await manager.exists(tri_state_filter.id) == True
    @pytest.mark.asyncio
    async def test_exists_with_nonexistent_tri_state_filter(async_session):
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
        # Add a tri_state_filter with a specific pac_id
        tri_state_filter = TriStateFilter(name="TriStateFilter_1", pac_id=5)
        async_session.add(tri_state_filter)
        await async_session.commit()
        # Fetch the tri_state_filter using the manager function
        manager = YourManagerClass(session=async_session)
        fetched_tri_state_filters = await manager.get_by_pac_id(5)
        assert len(fetched_tri_state_filters) == 1
        assert fetched_tri_state_filters[0].name == "TriStateFilter_1"
    @pytest.mark.asyncio
    async def test_get_by_pac_id_nonexistent(async_session):
        non_existent_id = 999
        manager = YourManagerClass(session=async_session)
        fetched_tri_state_filters = await manager.get_by_pac_id(non_existent_id)
        assert len(fetched_tri_state_filters) == 0
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
