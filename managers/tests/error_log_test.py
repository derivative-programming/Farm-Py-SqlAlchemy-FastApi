import pytest
import uuid
from unittest.mock import AsyncMock, patch
from managers import ErrorLogManager, ErrorLog
from models.factory import ErrorLogFactory
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models import Base, ErrorLog
DATABASE_URL = "sqlite:///:memory:"
db_dialect = "sqlite"
class TestErrorLogManager:
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
    async def error_log_manager(self, session):
        return ErrorLogManager(session)
    @pytest.mark.asyncio
    async def test_build(self, error_log_manager):
        # Define some mock data for our error_log
        mock_data = {
            "name": "Rose",
            "species": "Rosa",
            "age": 2
        }
        # Call the build function of the manager
        error_log = await error_log_manager.build(**mock_data)
        # Assert that the returned object is an instance of ErrorLog
        assert isinstance(error_log, ErrorLog)
        # Assert that the attributes of the error_log match our mock data
        assert error_log.name == mock_data["name"]
        assert error_log.species == mock_data["species"]
        assert error_log.age == mock_data["age"]
        # Optionally, if the build method has some default values or computations:
        # assert error_log.some_attribute == some_expected_value
    @pytest.mark.asyncio
    async def test_build_with_missing_data(self, error_log_manager):
        # Define mock data with a missing key
        mock_data = {
            "name": "Rose",
            "age": 2
        }
        # If the build method is expected to raise an exception for missing data, test for that
        with pytest.raises(SomeSpecificException):
            await error_log_manager.build(**mock_data)
    @pytest.mark.asyncio
    async def test_add(self, error_log_manager, mock_session):
        error_log_data = ErrorLogFactory.build()
        mock_session.add.return_value = None
        mock_session.commit.return_value = None
        error_log = await error_log_manager.add(**error_log_data)
        mock_session.add.assert_called_once_with(error_log)
        mock_session.commit.assert_called_once()
        assert isinstance(error_log, ErrorLog)
    @pytest.mark.asyncio
    async def test_add_correctly_adds_error_log_to_database(self, error_log_manager, db_session):
        # Create a test error_log using the ErrorLogFactory without persisting it to the database
        test_error_log = ErrorLogFactory.build()
        # Add the error_log using the manager's add method
        added_error_log = await error_log_manager.add(error_log=test_error_log)
        # Fetch the error_log from the database directly
        result = await db_session.execute(select(ErrorLog).filter(ErrorLog.error_log_id == added_error_log.error_log_id))
        fetched_error_log = result.scalars().first()
        # Assert that the fetched error_log is not None and matches the added error_log
        assert fetched_error_log is not None
        assert fetched_error_log.error_log_id == added_error_log.error_log_id
        assert fetched_error_log.name == added_error_log.name
        # ... other attribute checks ...
    @pytest.mark.asyncio
    async def test_add_returns_correct_error_log_object(self, error_log_manager):
        # Create a test error_log using the ErrorLogFactory without persisting it to the database
        test_error_log = ErrorLogFactory.build()
        # Add the error_log using the manager's add method
        added_error_log = await error_log_manager.add(error_log=test_error_log)
        # Assert that the returned error_log matches the test error_log
        assert added_error_log.error_log_id == test_error_log.error_log_id
        assert added_error_log.name == test_error_log.name
        # ... other attribute checks ...
    @pytest.mark.asyncio
    async def test_get_by_id(self, error_log_manager, mock_session):
        error_log_data = ErrorLogFactory.build()
        mock_session.execute.return_value = AsyncMock(scalars=AsyncMock(first=AsyncMock(return_value=error_log_data)))
        error_log = await error_log_manager.get_by_id(1)
        mock_session.execute.assert_called_once()
        assert isinstance(error_log, ErrorLog)
    async def test_get_by_id(self, session: AsyncSession, sample_error_log: ErrorLog):
        manager = ErrorLogManager(session)
        retrieved_error_log = await manager.get_by_id(sample_error_log.error_log_id)
        assert retrieved_error_log is not None
        assert retrieved_error_log.error_log_id == sample_error_log.error_log_id
        assert retrieved_error_log.name == "Rose"
        assert retrieved_error_log.color == "Red"
    async def test_get_by_id_not_found(self, session: AsyncSession):
        manager = ErrorLogManager(session)
        non_existent_id = 9999  # An ID that's not in the database
        retrieved_error_log = await manager.get_by_id(non_existent_id)
        assert retrieved_error_log is None
    @pytest.mark.asyncio
    async def test_get_by_code_returns_error_log(self, error_log_manager, db_session):
        # Use your ErrorLogFactory to create and save a ErrorLog object
        code = uuid.uuid4()
        error_log = ErrorLogFactory(code=code)
        db_session.add(error_log)
        await db_session.commit()
        # Fetch the error_log using the manager's get_by_code method
        fetched_error_log = await error_log_manager.get_by_code(code)
        # Assert that the fetched error_log is not None and has the expected code
        assert fetched_error_log is not None
        assert fetched_error_log.code == code
    @pytest.mark.asyncio
    async def test_get_by_code_returns_none_for_nonexistent_code(self, error_log_manager):
        # Generate a random UUID that doesn't correspond to any ErrorLog in the database
        random_code = uuid.uuid4()
        # Try fetching a error_log using the manager's get_by_code method
        fetched_error_log = await error_log_manager.get_by_code(random_code)
        # Assert that the result is None since no error_log with the given code exists
        assert fetched_error_log is None
    @pytest.mark.asyncio
    async def test_update(self, error_log_manager, mock_session):
        error_log_data = ErrorLogFactory.build()
        updated_data = {"name": "Updated ErrorLog"}
        mock_session.execute.return_value = AsyncMock(scalars=AsyncMock(first=AsyncMock(return_value=error_log_data)))
        mock_session.commit.return_value = None
        updated_error_log = await error_log_manager.update(1, **updated_data)
        assert updated_error_log.name == "Updated ErrorLog"
        mock_session.commit.assert_called_once()
        assert isinstance(updated_error_log, ErrorLog)
    async def test_update_valid_error_log(self):
        # Mocking a error_log instance
        error_log = ErrorLog(error_log_id=1, name="Rose", code="ROSE123")
        # Mocking the commit method
        self.session_mock.commit = AsyncMock()
        # Update the error_log with new attributes
        updated_error_log = await self.manager.update(error_log, name="Red Rose", code="REDROSE123")
        # Assertions
        assert updated_error_log.name == "Red Rose"
        assert updated_error_log.code == "REDROSE123"
        self.session_mock.commit.assert_called_once()
    async def test_update_invalid_error_log(self):
        # None error_log
        error_log = None
        updated_error_log = await self.manager.update(error_log, name="Red Rose", code="REDROSE123")
        # Assertions
        assert updated_error_log is None
        self.session_mock.commit.assert_not_called()
    async def test_update_with_nonexistent_attribute(self):
        # Mocking a error_log instance
        error_log = ErrorLog(error_log_id=1, name="Rose", code="ROSE123")
        # Mocking the commit method
        self.session_mock.commit = AsyncMock()
        # This should raise an AttributeError since 'color' is not an attribute of ErrorLog
        with pytest.raises(AttributeError):
            await self.manager.update(error_log, color="Red")
        self.session_mock.commit.assert_not_called()
    @pytest.mark.asyncio
    async def test_delete(self, error_log_manager, mock_session):
        error_log_data = ErrorLogFactory.build()
        mock_session.execute.return_value = AsyncMock(scalars=AsyncMock(first=AsyncMock(return_value=error_log_data)))
        mock_session.delete.return_value = None
        mock_session.commit.return_value = None
        deleted_error_log = await error_log_manager.delete(1)
        mock_session.delete.assert_called_once_with(deleted_error_log)
        mock_session.commit.assert_called_once()
        assert isinstance(deleted_error_log, ErrorLog)
    @pytest.mark.asyncio
    async def test_delete_nonexistent(self, error_log_manager, mock_session):
        mock_session.execute.return_value = AsyncMock(scalars=AsyncMock(first=AsyncMock(return_value=None)))
        with pytest.raises(ValueError, match="ErrorLog not found"):
            await error_log_manager.delete(999)
    @pytest.mark.asyncio
    async def test_get_list(self, error_log_manager, mock_session):
        error_logs_data = [ErrorLogFactory.build() for _ in range(5)]
        mock_session.execute.return_value = AsyncMock(scalars=AsyncMock(all=AsyncMock(return_value=error_logs_data)))
        error_logs = await error_log_manager.get_list()
        mock_session.execute.assert_called_once()
        assert len(error_logs) == 5
        assert all(isinstance(error_log, ErrorLog) for error_log in error_logs)
    @pytest.mark.asyncio
    async def test_to_json(self, error_log_manager):
        error_log_data = ErrorLogFactory.build()
        error_log = ErrorLog(**error_log_data)
        json_data = error_log_manager.to_json(error_log)
        assert json_data is not None
        # You might want to do more specific checks on the JSON structure
    @pytest.mark.asyncio
    async def test_from_json(self, error_log_manager):
        error_log_data = ErrorLogFactory.build()
        error_log = ErrorLog(**error_log_data)
        json_data = error_log_manager.to_json(error_log)
        deserialized_error_log = error_log_manager.from_json(json_data)
        assert isinstance(deserialized_error_log, ErrorLog)
        # Additional checks on the deserialized data can be added
    @pytest.mark.asyncio
    async def test_add_bulk(self, error_log_manager, mock_session):
        error_logs_data = [ErrorLogFactory.build() for _ in range(5)]
        mock_session.add_all.return_value = None
        mock_session.commit.return_value = None
        error_logs = await error_log_manager.add_bulk(error_logs_data)
        mock_session.add_all.assert_called_once()
        mock_session.commit.assert_called_once()
        assert len(error_logs) == 5
    @pytest.mark.asyncio
    async def test_update_bulk_success():
        manager = ErrorLogManager()
        session_mock = AsyncMock()
        manager.session = session_mock
        # Mocking error_log instances
        error_log1 = ErrorLog(error_log_id=1, name="Rose", code="ROSE123")
        error_log2 = ErrorLog(error_log_id=2, name="Tulip", code="TULIP123")
        # Mocking the get_by_id method to return the corresponding error_log
        async def mock_get_by_id(error_log_id):
            if error_log_id == 1:
                return error_log1
            if error_log_id == 2:
                return error_log2
        manager.get_by_id = mock_get_by_id
        # Mocking the commit method
        session_mock.commit = AsyncMock()
        # Update error_logs
        updates = [{"error_log_id": 1, "name": "Red Rose"}, {"error_log_id": 2, "name": "Yellow Tulip"}]
        updated_error_logs = await manager.update_bulk(updates)
        # Assertions
        assert len(updated_error_logs) == 2
        assert updated_error_logs[0].name == "Red Rose"
        assert updated_error_logs[1].name == "Yellow Tulip"
        session_mock.commit.assert_called_once()
    @pytest.mark.asyncio
    async def test_update_bulk_missing_error_log_id():
        manager = ErrorLogManager()
        # No error_logs to update since error_log_id is missing
        updates = [{"name": "Red Rose"}]
        updated_error_logs = await manager.update_bulk(updates)
        # Assertions
        assert len(updated_error_logs) == 0
    @pytest.mark.asyncio
    async def test_update_bulk_error_log_not_found():
        manager = ErrorLogManager()
        session_mock = AsyncMock()
        manager.session = session_mock
        # Mocking the get_by_id method to return None (error_log not found)
        manager.get_by_id = AsyncMock(return_value=None)
        # Mocking the commit method
        session_mock.commit = AsyncMock()
        # Update error_logs
        updates = [{"error_log_id": 1, "name": "Red Rose"}]
        updated_error_logs = await manager.update_bulk(updates)
        # Assertions
        assert len(updated_error_logs) == 0
        session_mock.commit.assert_not_called()
    @pytest.mark.asyncio
    async def test_delete_bulk_success():
        manager = ErrorLogManager()
        session_mock = AsyncMock()
        manager.session = session_mock
        # Mocking error_log instances
        error_log1 = ErrorLog(error_log_id=1, name="Rose", code="ROSE123")
        error_log2 = ErrorLog(error_log_id=2, name="Tulip", code="TULIP123")
        # Mocking the get_by_id method to return the corresponding error_log
        async def mock_get_by_id(error_log_id):
            if error_log_id == 1:
                return error_log1
            if error_log_id == 2:
                return error_log2
        manager.get_by_id = mock_get_by_id
        # Mocking the commit and delete methods
        session_mock.commit = AsyncMock()
        session_mock.delete = AsyncMock()
        # Delete error_logs
        error_log_ids = [1, 2]
        result = await manager.delete_bulk(error_log_ids)
        # Assertions
        assert result is True
        session_mock.delete.assert_called()
        session_mock.commit.assert_called_once()
    @pytest.mark.asyncio
    async def test_delete_bulk_some_error_logs_not_found():
        manager = ErrorLogManager()
        session_mock = AsyncMock()
        manager.session = session_mock
        # Mocking the get_by_id method to return None (error_log not found)
        async def mock_get_by_id(error_log_id):
            if error_log_id == 1:
                return None
            if error_log_id == 2:
                return ErrorLog(error_log_id=2, name="Tulip", code="TULIP123")
        manager.get_by_id = mock_get_by_id
        # Mocking the commit and delete methods
        session_mock.commit = AsyncMock()
        session_mock.delete = AsyncMock()
        # Delete error_logs
        error_log_ids = [1, 2]
        result = await manager.delete_bulk(error_log_ids)
        # Assertions
        assert result is True
        session_mock.delete.assert_called_once_with(ErrorLog(error_log_id=2, name="Tulip", code="TULIP123"))
        session_mock.commit.assert_called_once()
    @pytest.mark.asyncio
    async def test_delete_bulk_empty_list():
        manager = ErrorLogManager()
        session_mock = AsyncMock()
        manager.session = session_mock
        # Mocking the commit and delete methods
        session_mock.commit = AsyncMock()
        session_mock.delete = AsyncMock()
        # Delete error_logs with an empty list
        error_log_ids = []
        result = await manager.delete_bulk(error_log_ids)
        # Assertions
        assert result is True
        session_mock.delete.assert_not_called()
        session_mock.commit.assert_not_called()
    @pytest.mark.asyncio
    async def test_count(self, error_log_manager, mock_session):
        error_logs_data = [ErrorLogFactory.build() for _ in range(5)]
        mock_session.execute.return_value = AsyncMock(scalars=AsyncMock(all=AsyncMock(return_value=error_logs_data)))
        count = await error_log_manager.count()
        mock_session.execute.assert_called_once()
        assert count == 5
    @pytest.mark.asyncio
    async def test_count_basic_functionality(async_session):
        # Add a error_log
        new_error_log = ErrorLog()
        async_session.add(new_error_log)
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
        # Add multiple error_logs
        error_logs = [ErrorLog() for _ in range(5)]
        async_session.add_all(error_logs)
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
        # Add error_logs
        error_logs = [ErrorLog(name=f"ErrorLog_{i}") for i in range(5)]
        async_session.add_all(error_logs)
        await async_session.commit()
        manager = YourManagerClass(session=async_session)
        sorted_error_logs = await manager.get_sorted_list(sort_by="name")
        assert [error_log.name for error_log in sorted_error_logs] == [f"ErrorLog_{i}" for i in range(5)]
    @pytest.mark.asyncio
    async def test_get_sorted_list_descending_sorting(async_session):
        # Add error_logs
        error_logs = [ErrorLog(name=f"ErrorLog_{i}") for i in range(5)]
        async_session.add_all(error_logs)
        await async_session.commit()
        manager = YourManagerClass(session=async_session)
        sorted_error_logs = await manager.get_sorted_list(sort_by="name", order="desc")
        assert [error_log.name for error_log in sorted_error_logs] == [f"ErrorLog_{i}" for i in reversed(range(5))]
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
        sorted_error_logs = await manager.get_sorted_list(sort_by="name")
        assert len(sorted_error_logs) == 0
    @pytest.mark.asyncio
    async def test_refresh_basic(async_session):
        # Add a error_log
        error_log = ErrorLog(name="ErrorLog_1")
        async_session.add(error_log)
        await async_session.commit()
        # Modify the error_log directly in the database
        await async_session.execute('UPDATE error_logs SET name = :new_name WHERE id = :error_log_id', {"new_name": "Modified_ErrorLog", "error_log_id": error_log.id})
        await async_session.commit()
        # Now, refresh the error_log using the manager function
        manager = YourManagerClass(session=async_session)
        refreshed_error_log = await manager.refresh(error_log)
        assert refreshed_error_log.name == "Modified_ErrorLog"
    @pytest.mark.asyncio
    async def test_refresh_nonexistent_error_log(async_session):
        error_log = ErrorLog(id=999, name="Nonexistent_ErrorLog")
        manager = YourManagerClass(session=async_session)
        with pytest.raises(Exception):  # Modify the exception type based on your ORM's behavior
            await manager.refresh(error_log)
    @pytest.mark.asyncio
    async def test_refresh_database_connection_issues(async_session, mocker):
        # Mock the session's refresh method to simulate a database connection error
        mocker.patch.object(async_session, 'refresh', side_effect=Exception("DB connection error"))
        error_log = ErrorLog(name="ErrorLog_1")
        manager = YourManagerClass(session=async_session)
        with pytest.raises(Exception, match="DB connection error"):
            await manager.refresh(error_log)
    @pytest.mark.asyncio
    async def test_exists_with_existing_error_log(async_session):
        # Add a error_log
        error_log = ErrorLog(name="ErrorLog_1")
        async_session.add(error_log)
        await async_session.commit()
        # Check if the error_log exists using the manager function
        manager = YourManagerClass(session=async_session)
        assert await manager.exists(error_log.id) == True
    @pytest.mark.asyncio
    async def test_exists_with_nonexistent_error_log(async_session):
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
        # Add a error_log with a specific pac_id
        error_log = ErrorLog(name="ErrorLog_1", pac_id=5)
        async_session.add(error_log)
        await async_session.commit()
        # Fetch the error_log using the manager function
        manager = YourManagerClass(session=async_session)
        fetched_error_logs = await manager.get_by_pac_id(5)
        assert len(fetched_error_logs) == 1
        assert fetched_error_logs[0].name == "ErrorLog_1"
    @pytest.mark.asyncio
    async def test_get_by_pac_id_nonexistent(async_session):
        non_existent_id = 999
        manager = YourManagerClass(session=async_session)
        fetched_error_logs = await manager.get_by_pac_id(non_existent_id)
        assert len(fetched_error_logs) == 0
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
