import pytest
import uuid
from unittest.mock import AsyncMock, patch
from managers import TacManager, Tac
from models.factory import TacFactory
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models import Base, Tac
DATABASE_URL = "sqlite:///:memory:"
db_dialect = "sqlite"
class TestTacManager:
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
    async def tac_manager(self, session):
        return TacManager(session)
    @pytest.mark.asyncio
    async def test_build(self, tac_manager):
        # Define some mock data for our tac
        mock_data = {
            "name": "Rose",
            "species": "Rosa",
            "age": 2
        }
        # Call the build function of the manager
        tac = await tac_manager.build(**mock_data)
        # Assert that the returned object is an instance of Tac
        assert isinstance(tac, Tac)
        # Assert that the attributes of the tac match our mock data
        assert tac.name == mock_data["name"]
        assert tac.species == mock_data["species"]
        assert tac.age == mock_data["age"]
        # Optionally, if the build method has some default values or computations:
        # assert tac.some_attribute == some_expected_value
    @pytest.mark.asyncio
    async def test_build_with_missing_data(self, tac_manager):
        # Define mock data with a missing key
        mock_data = {
            "name": "Rose",
            "age": 2
        }
        # If the build method is expected to raise an exception for missing data, test for that
        with pytest.raises(SomeSpecificException):
            await tac_manager.build(**mock_data)
    @pytest.mark.asyncio
    async def test_add(self, tac_manager, mock_session):
        tac_data = TacFactory.build()
        mock_session.add.return_value = None
        mock_session.commit.return_value = None
        tac = await tac_manager.add(**tac_data)
        mock_session.add.assert_called_once_with(tac)
        mock_session.commit.assert_called_once()
        assert isinstance(tac, Tac)
    @pytest.mark.asyncio
    async def test_add_correctly_adds_tac_to_database(self, tac_manager, db_session):
        # Create a test tac using the TacFactory without persisting it to the database
        test_tac = TacFactory.build()
        # Add the tac using the manager's add method
        added_tac = await tac_manager.add(tac=test_tac)
        # Fetch the tac from the database directly
        result = await db_session.execute(select(Tac).filter(Tac.tac_id == added_tac.tac_id))
        fetched_tac = result.scalars().first()
        # Assert that the fetched tac is not None and matches the added tac
        assert fetched_tac is not None
        assert fetched_tac.tac_id == added_tac.tac_id
        assert fetched_tac.name == added_tac.name
        # ... other attribute checks ...
    @pytest.mark.asyncio
    async def test_add_returns_correct_tac_object(self, tac_manager):
        # Create a test tac using the TacFactory without persisting it to the database
        test_tac = TacFactory.build()
        # Add the tac using the manager's add method
        added_tac = await tac_manager.add(tac=test_tac)
        # Assert that the returned tac matches the test tac
        assert added_tac.tac_id == test_tac.tac_id
        assert added_tac.name == test_tac.name
        # ... other attribute checks ...
    @pytest.mark.asyncio
    async def test_get_by_id(self, tac_manager, mock_session):
        tac_data = TacFactory.build()
        mock_session.execute.return_value = AsyncMock(scalars=AsyncMock(first=AsyncMock(return_value=tac_data)))
        tac = await tac_manager.get_by_id(1)
        mock_session.execute.assert_called_once()
        assert isinstance(tac, Tac)
    async def test_get_by_id(self, session: AsyncSession, sample_tac: Tac):
        manager = TacManager(session)
        retrieved_tac = await manager.get_by_id(sample_tac.tac_id)
        assert retrieved_tac is not None
        assert retrieved_tac.tac_id == sample_tac.tac_id
        assert retrieved_tac.name == "Rose"
        assert retrieved_tac.color == "Red"
    async def test_get_by_id_not_found(self, session: AsyncSession):
        manager = TacManager(session)
        non_existent_id = 9999  # An ID that's not in the database
        retrieved_tac = await manager.get_by_id(non_existent_id)
        assert retrieved_tac is None
    @pytest.mark.asyncio
    async def test_get_by_code_returns_tac(self, tac_manager, db_session):
        # Use your TacFactory to create and save a Tac object
        code = uuid.uuid4()
        tac = TacFactory(code=code)
        db_session.add(tac)
        await db_session.commit()
        # Fetch the tac using the manager's get_by_code method
        fetched_tac = await tac_manager.get_by_code(code)
        # Assert that the fetched tac is not None and has the expected code
        assert fetched_tac is not None
        assert fetched_tac.code == code
    @pytest.mark.asyncio
    async def test_get_by_code_returns_none_for_nonexistent_code(self, tac_manager):
        # Generate a random UUID that doesn't correspond to any Tac in the database
        random_code = uuid.uuid4()
        # Try fetching a tac using the manager's get_by_code method
        fetched_tac = await tac_manager.get_by_code(random_code)
        # Assert that the result is None since no tac with the given code exists
        assert fetched_tac is None
    @pytest.mark.asyncio
    async def test_update(self, tac_manager, mock_session):
        tac_data = TacFactory.build()
        updated_data = {"name": "Updated Tac"}
        mock_session.execute.return_value = AsyncMock(scalars=AsyncMock(first=AsyncMock(return_value=tac_data)))
        mock_session.commit.return_value = None
        updated_tac = await tac_manager.update(1, **updated_data)
        assert updated_tac.name == "Updated Tac"
        mock_session.commit.assert_called_once()
        assert isinstance(updated_tac, Tac)
    async def test_update_valid_tac(self):
        # Mocking a tac instance
        tac = Tac(tac_id=1, name="Rose", code="ROSE123")
        # Mocking the commit method
        self.session_mock.commit = AsyncMock()
        # Update the tac with new attributes
        updated_tac = await self.manager.update(tac, name="Red Rose", code="REDROSE123")
        # Assertions
        assert updated_tac.name == "Red Rose"
        assert updated_tac.code == "REDROSE123"
        self.session_mock.commit.assert_called_once()
    async def test_update_invalid_tac(self):
        # None tac
        tac = None
        updated_tac = await self.manager.update(tac, name="Red Rose", code="REDROSE123")
        # Assertions
        assert updated_tac is None
        self.session_mock.commit.assert_not_called()
    async def test_update_with_nonexistent_attribute(self):
        # Mocking a tac instance
        tac = Tac(tac_id=1, name="Rose", code="ROSE123")
        # Mocking the commit method
        self.session_mock.commit = AsyncMock()
        # This should raise an AttributeError since 'color' is not an attribute of Tac
        with pytest.raises(AttributeError):
            await self.manager.update(tac, color="Red")
        self.session_mock.commit.assert_not_called()
    @pytest.mark.asyncio
    async def test_delete(self, tac_manager, mock_session):
        tac_data = TacFactory.build()
        mock_session.execute.return_value = AsyncMock(scalars=AsyncMock(first=AsyncMock(return_value=tac_data)))
        mock_session.delete.return_value = None
        mock_session.commit.return_value = None
        deleted_tac = await tac_manager.delete(1)
        mock_session.delete.assert_called_once_with(deleted_tac)
        mock_session.commit.assert_called_once()
        assert isinstance(deleted_tac, Tac)
    @pytest.mark.asyncio
    async def test_delete_nonexistent(self, tac_manager, mock_session):
        mock_session.execute.return_value = AsyncMock(scalars=AsyncMock(first=AsyncMock(return_value=None)))
        with pytest.raises(ValueError, match="Tac not found"):
            await tac_manager.delete(999)
    @pytest.mark.asyncio
    async def test_get_list(self, tac_manager, mock_session):
        tacs_data = [TacFactory.build() for _ in range(5)]
        mock_session.execute.return_value = AsyncMock(scalars=AsyncMock(all=AsyncMock(return_value=tacs_data)))
        tacs = await tac_manager.get_list()
        mock_session.execute.assert_called_once()
        assert len(tacs) == 5
        assert all(isinstance(tac, Tac) for tac in tacs)
    @pytest.mark.asyncio
    async def test_to_json(self, tac_manager):
        tac_data = TacFactory.build()
        tac = Tac(**tac_data)
        json_data = tac_manager.to_json(tac)
        assert json_data is not None
        # You might want to do more specific checks on the JSON structure
    @pytest.mark.asyncio
    async def test_from_json(self, tac_manager):
        tac_data = TacFactory.build()
        tac = Tac(**tac_data)
        json_data = tac_manager.to_json(tac)
        deserialized_tac = tac_manager.from_json(json_data)
        assert isinstance(deserialized_tac, Tac)
        # Additional checks on the deserialized data can be added
    @pytest.mark.asyncio
    async def test_add_bulk(self, tac_manager, mock_session):
        tacs_data = [TacFactory.build() for _ in range(5)]
        mock_session.add_all.return_value = None
        mock_session.commit.return_value = None
        tacs = await tac_manager.add_bulk(tacs_data)
        mock_session.add_all.assert_called_once()
        mock_session.commit.assert_called_once()
        assert len(tacs) == 5
    @pytest.mark.asyncio
    async def test_update_bulk_success():
        manager = TacManager()
        session_mock = AsyncMock()
        manager.session = session_mock
        # Mocking tac instances
        tac1 = Tac(tac_id=1, name="Rose", code="ROSE123")
        tac2 = Tac(tac_id=2, name="Tulip", code="TULIP123")
        # Mocking the get_by_id method to return the corresponding tac
        async def mock_get_by_id(tac_id):
            if tac_id == 1:
                return tac1
            if tac_id == 2:
                return tac2
        manager.get_by_id = mock_get_by_id
        # Mocking the commit method
        session_mock.commit = AsyncMock()
        # Update tacs
        updates = [{"tac_id": 1, "name": "Red Rose"}, {"tac_id": 2, "name": "Yellow Tulip"}]
        updated_tacs = await manager.update_bulk(updates)
        # Assertions
        assert len(updated_tacs) == 2
        assert updated_tacs[0].name == "Red Rose"
        assert updated_tacs[1].name == "Yellow Tulip"
        session_mock.commit.assert_called_once()
    @pytest.mark.asyncio
    async def test_update_bulk_missing_tac_id():
        manager = TacManager()
        # No tacs to update since tac_id is missing
        updates = [{"name": "Red Rose"}]
        updated_tacs = await manager.update_bulk(updates)
        # Assertions
        assert len(updated_tacs) == 0
    @pytest.mark.asyncio
    async def test_update_bulk_tac_not_found():
        manager = TacManager()
        session_mock = AsyncMock()
        manager.session = session_mock
        # Mocking the get_by_id method to return None (tac not found)
        manager.get_by_id = AsyncMock(return_value=None)
        # Mocking the commit method
        session_mock.commit = AsyncMock()
        # Update tacs
        updates = [{"tac_id": 1, "name": "Red Rose"}]
        updated_tacs = await manager.update_bulk(updates)
        # Assertions
        assert len(updated_tacs) == 0
        session_mock.commit.assert_not_called()
    @pytest.mark.asyncio
    async def test_delete_bulk_success():
        manager = TacManager()
        session_mock = AsyncMock()
        manager.session = session_mock
        # Mocking tac instances
        tac1 = Tac(tac_id=1, name="Rose", code="ROSE123")
        tac2 = Tac(tac_id=2, name="Tulip", code="TULIP123")
        # Mocking the get_by_id method to return the corresponding tac
        async def mock_get_by_id(tac_id):
            if tac_id == 1:
                return tac1
            if tac_id == 2:
                return tac2
        manager.get_by_id = mock_get_by_id
        # Mocking the commit and delete methods
        session_mock.commit = AsyncMock()
        session_mock.delete = AsyncMock()
        # Delete tacs
        tac_ids = [1, 2]
        result = await manager.delete_bulk(tac_ids)
        # Assertions
        assert result is True
        session_mock.delete.assert_called()
        session_mock.commit.assert_called_once()
    @pytest.mark.asyncio
    async def test_delete_bulk_some_tacs_not_found():
        manager = TacManager()
        session_mock = AsyncMock()
        manager.session = session_mock
        # Mocking the get_by_id method to return None (tac not found)
        async def mock_get_by_id(tac_id):
            if tac_id == 1:
                return None
            if tac_id == 2:
                return Tac(tac_id=2, name="Tulip", code="TULIP123")
        manager.get_by_id = mock_get_by_id
        # Mocking the commit and delete methods
        session_mock.commit = AsyncMock()
        session_mock.delete = AsyncMock()
        # Delete tacs
        tac_ids = [1, 2]
        result = await manager.delete_bulk(tac_ids)
        # Assertions
        assert result is True
        session_mock.delete.assert_called_once_with(Tac(tac_id=2, name="Tulip", code="TULIP123"))
        session_mock.commit.assert_called_once()
    @pytest.mark.asyncio
    async def test_delete_bulk_empty_list():
        manager = TacManager()
        session_mock = AsyncMock()
        manager.session = session_mock
        # Mocking the commit and delete methods
        session_mock.commit = AsyncMock()
        session_mock.delete = AsyncMock()
        # Delete tacs with an empty list
        tac_ids = []
        result = await manager.delete_bulk(tac_ids)
        # Assertions
        assert result is True
        session_mock.delete.assert_not_called()
        session_mock.commit.assert_not_called()
    @pytest.mark.asyncio
    async def test_count(self, tac_manager, mock_session):
        tacs_data = [TacFactory.build() for _ in range(5)]
        mock_session.execute.return_value = AsyncMock(scalars=AsyncMock(all=AsyncMock(return_value=tacs_data)))
        count = await tac_manager.count()
        mock_session.execute.assert_called_once()
        assert count == 5
    @pytest.mark.asyncio
    async def test_count_basic_functionality(async_session):
        # Add a tac
        new_tac = Tac()
        async_session.add(new_tac)
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
        # Add multiple tacs
        tacs = [Tac() for _ in range(5)]
        async_session.add_all(tacs)
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
        # Add tacs
        tacs = [Tac(name=f"Tac_{i}") for i in range(5)]
        async_session.add_all(tacs)
        await async_session.commit()
        manager = YourManagerClass(session=async_session)
        sorted_tacs = await manager.get_sorted_list(sort_by="name")
        assert [tac.name for tac in sorted_tacs] == [f"Tac_{i}" for i in range(5)]
    @pytest.mark.asyncio
    async def test_get_sorted_list_descending_sorting(async_session):
        # Add tacs
        tacs = [Tac(name=f"Tac_{i}") for i in range(5)]
        async_session.add_all(tacs)
        await async_session.commit()
        manager = YourManagerClass(session=async_session)
        sorted_tacs = await manager.get_sorted_list(sort_by="name", order="desc")
        assert [tac.name for tac in sorted_tacs] == [f"Tac_{i}" for i in reversed(range(5))]
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
        sorted_tacs = await manager.get_sorted_list(sort_by="name")
        assert len(sorted_tacs) == 0
    @pytest.mark.asyncio
    async def test_refresh_basic(async_session):
        # Add a tac
        tac = Tac(name="Tac_1")
        async_session.add(tac)
        await async_session.commit()
        # Modify the tac directly in the database
        await async_session.execute('UPDATE tacs SET name = :new_name WHERE id = :tac_id', {"new_name": "Modified_Tac", "tac_id": tac.id})
        await async_session.commit()
        # Now, refresh the tac using the manager function
        manager = YourManagerClass(session=async_session)
        refreshed_tac = await manager.refresh(tac)
        assert refreshed_tac.name == "Modified_Tac"
    @pytest.mark.asyncio
    async def test_refresh_nonexistent_tac(async_session):
        tac = Tac(id=999, name="Nonexistent_Tac")
        manager = YourManagerClass(session=async_session)
        with pytest.raises(Exception):  # Modify the exception type based on your ORM's behavior
            await manager.refresh(tac)
    @pytest.mark.asyncio
    async def test_refresh_database_connection_issues(async_session, mocker):
        # Mock the session's refresh method to simulate a database connection error
        mocker.patch.object(async_session, 'refresh', side_effect=Exception("DB connection error"))
        tac = Tac(name="Tac_1")
        manager = YourManagerClass(session=async_session)
        with pytest.raises(Exception, match="DB connection error"):
            await manager.refresh(tac)
    @pytest.mark.asyncio
    async def test_exists_with_existing_tac(async_session):
        # Add a tac
        tac = Tac(name="Tac_1")
        async_session.add(tac)
        await async_session.commit()
        # Check if the tac exists using the manager function
        manager = YourManagerClass(session=async_session)
        assert await manager.exists(tac.id) == True
    @pytest.mark.asyncio
    async def test_exists_with_nonexistent_tac(async_session):
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
        # Add a tac with a specific pac_id
        tac = Tac(name="Tac_1", pac_id=5)
        async_session.add(tac)
        await async_session.commit()
        # Fetch the tac using the manager function
        manager = YourManagerClass(session=async_session)
        fetched_tacs = await manager.get_by_pac_id(5)
        assert len(fetched_tacs) == 1
        assert fetched_tacs[0].name == "Tac_1"
    @pytest.mark.asyncio
    async def test_get_by_pac_id_nonexistent(async_session):
        non_existent_id = 999
        manager = YourManagerClass(session=async_session)
        fetched_tacs = await manager.get_by_pac_id(non_existent_id)
        assert len(fetched_tacs) == 0
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
