import pytest
import uuid
from unittest.mock import AsyncMock, patch
from managers import PacManager, Pac
from models.factory import PacFactory
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models import Base, Pac
DATABASE_URL = "sqlite:///:memory:"
db_dialect = "sqlite"
class TestPacManager:
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
    async def pac_manager(self, session):
        return PacManager(session)
    @pytest.mark.asyncio
    async def test_build(self, pac_manager):
        # Define some mock data for our pac
        mock_data = {
            "name": "Rose",
            "species": "Rosa",
            "age": 2
        }
        # Call the build function of the manager
        pac = await pac_manager.build(**mock_data)
        # Assert that the returned object is an instance of Pac
        assert isinstance(pac, Pac)
        # Assert that the attributes of the pac match our mock data
        assert pac.name == mock_data["name"]
        assert pac.species == mock_data["species"]
        assert pac.age == mock_data["age"]
        # Optionally, if the build method has some default values or computations:
        # assert pac.some_attribute == some_expected_value
    @pytest.mark.asyncio
    async def test_build_with_missing_data(self, pac_manager):
        # Define mock data with a missing key
        mock_data = {
            "name": "Rose",
            "age": 2
        }
        # If the build method is expected to raise an exception for missing data, test for that
        with pytest.raises(SomeSpecificException):
            await pac_manager.build(**mock_data)
    @pytest.mark.asyncio
    async def test_add(self, pac_manager, mock_session):
        pac_data = PacFactory.build()
        mock_session.add.return_value = None
        mock_session.commit.return_value = None
        pac = await pac_manager.add(**pac_data)
        mock_session.add.assert_called_once_with(pac)
        mock_session.commit.assert_called_once()
        assert isinstance(pac, Pac)
    @pytest.mark.asyncio
    async def test_add_correctly_adds_pac_to_database(self, pac_manager, db_session):
        # Create a test pac using the PacFactory without persisting it to the database
        test_pac = PacFactory.build()
        # Add the pac using the manager's add method
        added_pac = await pac_manager.add(pac=test_pac)
        # Fetch the pac from the database directly
        result = await db_session.execute(select(Pac).filter(Pac.pac_id == added_pac.pac_id))
        fetched_pac = result.scalars().first()
        # Assert that the fetched pac is not None and matches the added pac
        assert fetched_pac is not None
        assert fetched_pac.pac_id == added_pac.pac_id
        assert fetched_pac.name == added_pac.name
        # ... other attribute checks ...
    @pytest.mark.asyncio
    async def test_add_returns_correct_pac_object(self, pac_manager):
        # Create a test pac using the PacFactory without persisting it to the database
        test_pac = PacFactory.build()
        # Add the pac using the manager's add method
        added_pac = await pac_manager.add(pac=test_pac)
        # Assert that the returned pac matches the test pac
        assert added_pac.pac_id == test_pac.pac_id
        assert added_pac.name == test_pac.name
        # ... other attribute checks ...
    @pytest.mark.asyncio
    async def test_get_by_id(self, pac_manager, mock_session):
        pac_data = PacFactory.build()
        mock_session.execute.return_value = AsyncMock(scalars=AsyncMock(first=AsyncMock(return_value=pac_data)))
        pac = await pac_manager.get_by_id(1)
        mock_session.execute.assert_called_once()
        assert isinstance(pac, Pac)
    async def test_get_by_id(self, session: AsyncSession, sample_pac: Pac):
        manager = PacManager(session)
        retrieved_pac = await manager.get_by_id(sample_pac.pac_id)
        assert retrieved_pac is not None
        assert retrieved_pac.pac_id == sample_pac.pac_id
        assert retrieved_pac.name == "Rose"
        assert retrieved_pac.color == "Red"
    async def test_get_by_id_not_found(self, session: AsyncSession):
        manager = PacManager(session)
        non_existent_id = 9999  # An ID that's not in the database
        retrieved_pac = await manager.get_by_id(non_existent_id)
        assert retrieved_pac is None
    @pytest.mark.asyncio
    async def test_get_by_code_returns_pac(self, pac_manager, db_session):
        # Use your PacFactory to create and save a Pac object
        code = uuid.uuid4()
        pac = PacFactory(code=code)
        db_session.add(pac)
        await db_session.commit()
        # Fetch the pac using the manager's get_by_code method
        fetched_pac = await pac_manager.get_by_code(code)
        # Assert that the fetched pac is not None and has the expected code
        assert fetched_pac is not None
        assert fetched_pac.code == code
    @pytest.mark.asyncio
    async def test_get_by_code_returns_none_for_nonexistent_code(self, pac_manager):
        # Generate a random UUID that doesn't correspond to any Pac in the database
        random_code = uuid.uuid4()
        # Try fetching a pac using the manager's get_by_code method
        fetched_pac = await pac_manager.get_by_code(random_code)
        # Assert that the result is None since no pac with the given code exists
        assert fetched_pac is None
    @pytest.mark.asyncio
    async def test_update(self, pac_manager, mock_session):
        pac_data = PacFactory.build()
        updated_data = {"name": "Updated Pac"}
        mock_session.execute.return_value = AsyncMock(scalars=AsyncMock(first=AsyncMock(return_value=pac_data)))
        mock_session.commit.return_value = None
        updated_pac = await pac_manager.update(1, **updated_data)
        assert updated_pac.name == "Updated Pac"
        mock_session.commit.assert_called_once()
        assert isinstance(updated_pac, Pac)
    async def test_update_valid_pac(self):
        # Mocking a pac instance
        pac = Pac(pac_id=1, name="Rose", code="ROSE123")
        # Mocking the commit method
        self.session_mock.commit = AsyncMock()
        # Update the pac with new attributes
        updated_pac = await self.manager.update(pac, name="Red Rose", code="REDROSE123")
        # Assertions
        assert updated_pac.name == "Red Rose"
        assert updated_pac.code == "REDROSE123"
        self.session_mock.commit.assert_called_once()
    async def test_update_invalid_pac(self):
        # None pac
        pac = None
        updated_pac = await self.manager.update(pac, name="Red Rose", code="REDROSE123")
        # Assertions
        assert updated_pac is None
        self.session_mock.commit.assert_not_called()
    async def test_update_with_nonexistent_attribute(self):
        # Mocking a pac instance
        pac = Pac(pac_id=1, name="Rose", code="ROSE123")
        # Mocking the commit method
        self.session_mock.commit = AsyncMock()
        # This should raise an AttributeError since 'color' is not an attribute of Pac
        with pytest.raises(AttributeError):
            await self.manager.update(pac, color="Red")
        self.session_mock.commit.assert_not_called()
    @pytest.mark.asyncio
    async def test_delete(self, pac_manager, mock_session):
        pac_data = PacFactory.build()
        mock_session.execute.return_value = AsyncMock(scalars=AsyncMock(first=AsyncMock(return_value=pac_data)))
        mock_session.delete.return_value = None
        mock_session.commit.return_value = None
        deleted_pac = await pac_manager.delete(1)
        mock_session.delete.assert_called_once_with(deleted_pac)
        mock_session.commit.assert_called_once()
        assert isinstance(deleted_pac, Pac)
    @pytest.mark.asyncio
    async def test_delete_nonexistent(self, pac_manager, mock_session):
        mock_session.execute.return_value = AsyncMock(scalars=AsyncMock(first=AsyncMock(return_value=None)))
        with pytest.raises(ValueError, match="Pac not found"):
            await pac_manager.delete(999)
    @pytest.mark.asyncio
    async def test_get_list(self, pac_manager, mock_session):
        pacs_data = [PacFactory.build() for _ in range(5)]
        mock_session.execute.return_value = AsyncMock(scalars=AsyncMock(all=AsyncMock(return_value=pacs_data)))
        pacs = await pac_manager.get_list()
        mock_session.execute.assert_called_once()
        assert len(pacs) == 5
        assert all(isinstance(pac, Pac) for pac in pacs)
    @pytest.mark.asyncio
    async def test_to_json(self, pac_manager):
        pac_data = PacFactory.build()
        pac = Pac(**pac_data)
        json_data = pac_manager.to_json(pac)
        assert json_data is not None
        # You might want to do more specific checks on the JSON structure
    @pytest.mark.asyncio
    async def test_from_json(self, pac_manager):
        pac_data = PacFactory.build()
        pac = Pac(**pac_data)
        json_data = pac_manager.to_json(pac)
        deserialized_pac = pac_manager.from_json(json_data)
        assert isinstance(deserialized_pac, Pac)
        # Additional checks on the deserialized data can be added
    @pytest.mark.asyncio
    async def test_add_bulk(self, pac_manager, mock_session):
        pacs_data = [PacFactory.build() for _ in range(5)]
        mock_session.add_all.return_value = None
        mock_session.commit.return_value = None
        pacs = await pac_manager.add_bulk(pacs_data)
        mock_session.add_all.assert_called_once()
        mock_session.commit.assert_called_once()
        assert len(pacs) == 5
    @pytest.mark.asyncio
    async def test_update_bulk_success():
        manager = PacManager()
        session_mock = AsyncMock()
        manager.session = session_mock
        # Mocking pac instances
        pac1 = Pac(pac_id=1, name="Rose", code="ROSE123")
        pac2 = Pac(pac_id=2, name="Tulip", code="TULIP123")
        # Mocking the get_by_id method to return the corresponding pac
        async def mock_get_by_id(pac_id):
            if pac_id == 1:
                return pac1
            if pac_id == 2:
                return pac2
        manager.get_by_id = mock_get_by_id
        # Mocking the commit method
        session_mock.commit = AsyncMock()
        # Update pacs
        updates = [{"pac_id": 1, "name": "Red Rose"}, {"pac_id": 2, "name": "Yellow Tulip"}]
        updated_pacs = await manager.update_bulk(updates)
        # Assertions
        assert len(updated_pacs) == 2
        assert updated_pacs[0].name == "Red Rose"
        assert updated_pacs[1].name == "Yellow Tulip"
        session_mock.commit.assert_called_once()
    @pytest.mark.asyncio
    async def test_update_bulk_missing_pac_id():
        manager = PacManager()
        # No pacs to update since pac_id is missing
        updates = [{"name": "Red Rose"}]
        updated_pacs = await manager.update_bulk(updates)
        # Assertions
        assert len(updated_pacs) == 0
    @pytest.mark.asyncio
    async def test_update_bulk_pac_not_found():
        manager = PacManager()
        session_mock = AsyncMock()
        manager.session = session_mock
        # Mocking the get_by_id method to return None (pac not found)
        manager.get_by_id = AsyncMock(return_value=None)
        # Mocking the commit method
        session_mock.commit = AsyncMock()
        # Update pacs
        updates = [{"pac_id": 1, "name": "Red Rose"}]
        updated_pacs = await manager.update_bulk(updates)
        # Assertions
        assert len(updated_pacs) == 0
        session_mock.commit.assert_not_called()
    @pytest.mark.asyncio
    async def test_delete_bulk_success():
        manager = PacManager()
        session_mock = AsyncMock()
        manager.session = session_mock
        # Mocking pac instances
        pac1 = Pac(pac_id=1, name="Rose", code="ROSE123")
        pac2 = Pac(pac_id=2, name="Tulip", code="TULIP123")
        # Mocking the get_by_id method to return the corresponding pac
        async def mock_get_by_id(pac_id):
            if pac_id == 1:
                return pac1
            if pac_id == 2:
                return pac2
        manager.get_by_id = mock_get_by_id
        # Mocking the commit and delete methods
        session_mock.commit = AsyncMock()
        session_mock.delete = AsyncMock()
        # Delete pacs
        pac_ids = [1, 2]
        result = await manager.delete_bulk(pac_ids)
        # Assertions
        assert result is True
        session_mock.delete.assert_called()
        session_mock.commit.assert_called_once()
    @pytest.mark.asyncio
    async def test_delete_bulk_some_pacs_not_found():
        manager = PacManager()
        session_mock = AsyncMock()
        manager.session = session_mock
        # Mocking the get_by_id method to return None (pac not found)
        async def mock_get_by_id(pac_id):
            if pac_id == 1:
                return None
            if pac_id == 2:
                return Pac(pac_id=2, name="Tulip", code="TULIP123")
        manager.get_by_id = mock_get_by_id
        # Mocking the commit and delete methods
        session_mock.commit = AsyncMock()
        session_mock.delete = AsyncMock()
        # Delete pacs
        pac_ids = [1, 2]
        result = await manager.delete_bulk(pac_ids)
        # Assertions
        assert result is True
        session_mock.delete.assert_called_once_with(Pac(pac_id=2, name="Tulip", code="TULIP123"))
        session_mock.commit.assert_called_once()
    @pytest.mark.asyncio
    async def test_delete_bulk_empty_list():
        manager = PacManager()
        session_mock = AsyncMock()
        manager.session = session_mock
        # Mocking the commit and delete methods
        session_mock.commit = AsyncMock()
        session_mock.delete = AsyncMock()
        # Delete pacs with an empty list
        pac_ids = []
        result = await manager.delete_bulk(pac_ids)
        # Assertions
        assert result is True
        session_mock.delete.assert_not_called()
        session_mock.commit.assert_not_called()
    @pytest.mark.asyncio
    async def test_count(self, pac_manager, mock_session):
        pacs_data = [PacFactory.build() for _ in range(5)]
        mock_session.execute.return_value = AsyncMock(scalars=AsyncMock(all=AsyncMock(return_value=pacs_data)))
        count = await pac_manager.count()
        mock_session.execute.assert_called_once()
        assert count == 5
    @pytest.mark.asyncio
    async def test_count_basic_functionality(async_session):
        # Add a pac
        new_pac = Pac()
        async_session.add(new_pac)
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
        # Add multiple pacs
        pacs = [Pac() for _ in range(5)]
        async_session.add_all(pacs)
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
        # Add pacs
        pacs = [Pac(name=f"Pac_{i}") for i in range(5)]
        async_session.add_all(pacs)
        await async_session.commit()
        manager = YourManagerClass(session=async_session)
        sorted_pacs = await manager.get_sorted_list(sort_by="name")
        assert [pac.name for pac in sorted_pacs] == [f"Pac_{i}" for i in range(5)]
    @pytest.mark.asyncio
    async def test_get_sorted_list_descending_sorting(async_session):
        # Add pacs
        pacs = [Pac(name=f"Pac_{i}") for i in range(5)]
        async_session.add_all(pacs)
        await async_session.commit()
        manager = YourManagerClass(session=async_session)
        sorted_pacs = await manager.get_sorted_list(sort_by="name", order="desc")
        assert [pac.name for pac in sorted_pacs] == [f"Pac_{i}" for i in reversed(range(5))]
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
        sorted_pacs = await manager.get_sorted_list(sort_by="name")
        assert len(sorted_pacs) == 0
    @pytest.mark.asyncio
    async def test_refresh_basic(async_session):
        # Add a pac
        pac = Pac(name="Pac_1")
        async_session.add(pac)
        await async_session.commit()
        # Modify the pac directly in the database
        await async_session.execute('UPDATE pacs SET name = :new_name WHERE id = :pac_id', {"new_name": "Modified_Pac", "pac_id": pac.id})
        await async_session.commit()
        # Now, refresh the pac using the manager function
        manager = YourManagerClass(session=async_session)
        refreshed_pac = await manager.refresh(pac)
        assert refreshed_pac.name == "Modified_Pac"
    @pytest.mark.asyncio
    async def test_refresh_nonexistent_pac(async_session):
        pac = Pac(id=999, name="Nonexistent_Pac")
        manager = YourManagerClass(session=async_session)
        with pytest.raises(Exception):  # Modify the exception type based on your ORM's behavior
            await manager.refresh(pac)
    @pytest.mark.asyncio
    async def test_refresh_database_connection_issues(async_session, mocker):
        # Mock the session's refresh method to simulate a database connection error
        mocker.patch.object(async_session, 'refresh', side_effect=Exception("DB connection error"))
        pac = Pac(name="Pac_1")
        manager = YourManagerClass(session=async_session)
        with pytest.raises(Exception, match="DB connection error"):
            await manager.refresh(pac)
    @pytest.mark.asyncio
    async def test_exists_with_existing_pac(async_session):
        # Add a pac
        pac = Pac(name="Pac_1")
        async_session.add(pac)
        await async_session.commit()
        # Check if the pac exists using the manager function
        manager = YourManagerClass(session=async_session)
        assert await manager.exists(pac.id) == True
    @pytest.mark.asyncio
    async def test_exists_with_nonexistent_pac(async_session):
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

    @pytest.mark.asyncio
    async def test_get_by__id_existing(async_session):
        # Add a pac with a specific _id
        pac = Pac(name="Pac_1", _id=5)
        async_session.add(pac)
        await async_session.commit()
        # Fetch the pac using the manager function
        manager = YourManagerClass(session=async_session)
        fetched_pacs = await manager.get_by__id(5)
        assert len(fetched_pacs) == 1
        assert fetched_pacs[0].name == "Pac_1"
    @pytest.mark.asyncio
    async def test_get_by__id_nonexistent(async_session):
        non_existent_id = 999
        manager = YourManagerClass(session=async_session)
        fetched_pacs = await manager.get_by__id(non_existent_id)
        assert len(fetched_pacs) == 0
    @pytest.mark.asyncio
    async def test_get_by__id_invalid_type(async_session):
        invalid_id = "invalid_id"
        manager = YourManagerClass(session=async_session)
        with pytest.raises(Exception):  # Modify the exception type based on your ORM's behavior or validation
            await manager.get_by__id(invalid_id)
    @pytest.mark.asyncio
    async def test_get_by__id_database_connection_issues(async_session, mocker):
        # Mock the execute method to simulate a database connection error
        mocker.patch.object(async_session, 'execute', side_effect=Exception("DB connection error"))
        manager = YourManagerClass(session=async_session)
        with pytest.raises(Exception, match="DB connection error"):
            await manager.get_by__id(1)
