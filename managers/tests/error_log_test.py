import asyncio
from decimal import Decimal
import pytest
import pytest_asyncio
import time
from decimal import Decimal
from datetime import datetime, date
from sqlalchemy import event
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from models import Base, ErrorLog
from models.factory import ErrorLogFactory
from managers.error_log import ErrorLogManager
from models.serialization_schema.error_log import ErrorLogSchema
from services.db_config import db_dialect
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
from services.db_config import db_dialect,generate_uuid
from sqlalchemy import String
from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select
DATABASE_URL = "sqlite+aiosqlite:///:memory:"
db_dialect = "sqlite"
# Conditionally set the UUID column type
if db_dialect == 'postgresql':
    UUIDType = UUID(as_uuid=True)
elif db_dialect == 'mssql':
    UUIDType = UNIQUEIDENTIFIER
else:  # This will cover SQLite, MySQL, and other databases
    UUIDType = String(36)
class TestErrorLogManager:
    @pytest.fixture(scope="function")
    def event_loop(self) -> asyncio.AbstractEventLoop:
        loop = asyncio.get_event_loop_policy().new_event_loop()
        yield loop
        loop.close()
    @pytest.fixture(scope="function")
    def engine(self):
        engine = create_async_engine(DATABASE_URL, echo=True)
        yield engine
        engine.sync_engine.dispose()
    @pytest_asyncio.fixture(scope="function")
    async def session(self,engine) -> AsyncSession:
        @event.listens_for(engine.sync_engine, "connect")
        def set_sqlite_pragma(dbapi_connection, connection_record):
            cursor = dbapi_connection.cursor()
            cursor.execute("PRAGMA foreign_keys=ON")
            cursor.close()
        async with engine.begin() as connection:
            await connection.begin_nested()
            await connection.run_sync(Base.metadata.drop_all)
            await connection.run_sync(Base.metadata.create_all)
            TestingSessionLocal = sessionmaker(
                expire_on_commit=False,
                class_=AsyncSession,
                bind=engine,
            )
            async with TestingSessionLocal(bind=connection) as session:
                @event.listens_for(
                    session.sync_session, "after_transaction_end"
                )
                def end_savepoint(session, transaction):
                    if connection.closed:
                        return
                    if not connection.in_nested_transaction():
                        connection.sync_connection.begin_nested()
                yield session
                await session.flush()
                await session.rollback()
    @pytest_asyncio.fixture(scope="function")
    async def error_log_manager(self, session:AsyncSession):
        return ErrorLogManager(session)
    @pytest.mark.asyncio
    async def test_build(self, error_log_manager:ErrorLogManager, session:AsyncSession):
        # Define some mock data for our error_log
        mock_data = {
            "code": generate_uuid()
        }
        # Call the build function of the manager
        error_log = await error_log_manager.build(**mock_data)
        # Assert that the returned object is an instance of ErrorLog
        assert isinstance(error_log, ErrorLog)
        # Assert that the attributes of the error_log match our mock data
        assert error_log.code == mock_data["code"]
        # Optionally, if the build method has some default values or computations:
        # assert error_log.some_attribute == some_expected_value
    @pytest.mark.asyncio
    async def test_build_with_missing_data(self, error_log_manager:ErrorLogManager, session:AsyncSession):
        # Define mock data with a missing key
        mock_data = {
            "non_existant_property": "Rose"
        }
        # If the build method is expected to raise an exception for missing data, test for that
        with pytest.raises(Exception):
            await error_log_manager.build_async(**mock_data)
        await session.rollback()
    @pytest.mark.asyncio
    async def test_add_correctly_adds_error_log_to_database(self, error_log_manager:ErrorLogManager, session:AsyncSession):
        test_error_log = await ErrorLogFactory.build_async(session)
        assert test_error_log.error_log_id is None
        # Add the error_log using the manager's add method
        added_error_log = await error_log_manager.add(error_log=test_error_log)
        assert isinstance(added_error_log, ErrorLog)
        assert added_error_log.error_log_id > 0
        # Fetch the error_log from the database directly
        result = await session.execute(select(ErrorLog).filter(ErrorLog.error_log_id == added_error_log.error_log_id))
        fetched_error_log = result.scalars().first()
        # Assert that the fetched error_log is not None and matches the added error_log
        assert fetched_error_log is not None
        assert isinstance(fetched_error_log, ErrorLog)
        assert fetched_error_log.error_log_id == added_error_log.error_log_id
    @pytest.mark.asyncio
    async def test_add_returns_correct_error_log_object(self, error_log_manager:ErrorLogManager, session:AsyncSession):
        # Create a test error_log using the ErrorLogFactory without persisting it to the database
        test_error_log = await ErrorLogFactory.build_async(session)
        assert test_error_log.error_log_id is None
        test_error_log.code = generate_uuid()
        # Add the error_log using the manager's add method
        added_error_log = await error_log_manager.add(error_log=test_error_log)
        assert isinstance(added_error_log, ErrorLog)
        assert added_error_log.error_log_id > 0
        # Assert that the returned error_log matches the test error_log
        assert added_error_log.error_log_id == test_error_log.error_log_id
        assert added_error_log.code == test_error_log.code
    @pytest.mark.asyncio
    async def test_get_by_id(self, error_log_manager:ErrorLogManager, session:AsyncSession):
        test_error_log = await ErrorLogFactory.create_async(session)
        error_log = await error_log_manager.get_by_id(test_error_log.error_log_id)
        assert isinstance(error_log, ErrorLog)
        assert test_error_log.error_log_id == error_log.error_log_id
        assert test_error_log.code == error_log.code
    @pytest.mark.asyncio
    async def test_get_by_id_not_found(self, error_log_manager:ErrorLogManager, session: AsyncSession):
        non_existent_id = 9999  # An ID that's not in the database
        retrieved_error_log = await error_log_manager.get_by_id(non_existent_id)
        assert retrieved_error_log is None
    @pytest.mark.asyncio
    async def test_get_by_code_returns_error_log(self, error_log_manager:ErrorLogManager, session:AsyncSession):
        test_error_log = await ErrorLogFactory.create_async(session)
        error_log = await error_log_manager.get_by_code(test_error_log.code)
        assert isinstance(error_log, ErrorLog)
        assert test_error_log.error_log_id == error_log.error_log_id
        assert test_error_log.code == error_log.code
    @pytest.mark.asyncio
    async def test_get_by_code_returns_none_for_nonexistent_code(self, error_log_manager:ErrorLogManager, session:AsyncSession):
        # Generate a random UUID that doesn't correspond to any ErrorLog in the database
        random_code = generate_uuid()
        error_log = await error_log_manager.get_by_code(random_code)
        assert error_log is None
    @pytest.mark.asyncio
    async def test_update(self, error_log_manager:ErrorLogManager, session:AsyncSession):
        test_error_log = await ErrorLogFactory.create_async(session)
        test_error_log.code = generate_uuid()
        updated_error_log = await error_log_manager.update(error_log=test_error_log)
        assert isinstance(updated_error_log, ErrorLog)
        assert updated_error_log.error_log_id == test_error_log.error_log_id
        assert updated_error_log.code == test_error_log.code
        result = await session.execute(select(ErrorLog).filter(ErrorLog.error_log_id == test_error_log.error_log_id))
        fetched_error_log = result.scalars().first()
        assert updated_error_log.error_log_id == fetched_error_log.error_log_id
        assert updated_error_log.code == fetched_error_log.code
        assert test_error_log.error_log_id == fetched_error_log.error_log_id
        assert test_error_log.code == fetched_error_log.code
    @pytest.mark.asyncio
    async def test_update_via_dict(self, error_log_manager:ErrorLogManager, session:AsyncSession):
        test_error_log = await ErrorLogFactory.create_async(session)
        new_code = generate_uuid()
        updated_error_log = await error_log_manager.update(error_log=test_error_log,code=new_code)
        assert isinstance(updated_error_log, ErrorLog)
        assert updated_error_log.error_log_id == test_error_log.error_log_id
        assert updated_error_log.code == new_code
        result = await session.execute(select(ErrorLog).filter(ErrorLog.error_log_id == test_error_log.error_log_id))
        fetched_error_log = result.scalars().first()
        assert updated_error_log.error_log_id == fetched_error_log.error_log_id
        assert updated_error_log.code == fetched_error_log.code
        assert test_error_log.error_log_id == fetched_error_log.error_log_id
        assert new_code == fetched_error_log.code
    @pytest.mark.asyncio
    async def test_update_invalid_error_log(self, error_log_manager:ErrorLogManager):
        # None error_log
        error_log = None
        new_code = generate_uuid()
        updated_error_log = await error_log_manager.update(error_log, code=new_code)
        # Assertions
        assert updated_error_log is None
    #todo fix test
    # @pytest.mark.asyncio
    # async def test_update_with_nonexistent_attribute(self, error_log_manager:ErrorLogManager, session:AsyncSession):
    #     test_error_log = await ErrorLogFactory.create_async(session)
    #     new_code = generate_uuid()
    #     # This should raise an AttributeError since 'color' is not an attribute of ErrorLog
    #     with pytest.raises(Exception):
    #         updated_error_log = await error_log_manager.update(error_log=test_error_log,xxx=new_code)
    #     await session.rollback()
    @pytest.mark.asyncio
    async def test_delete(self, error_log_manager:ErrorLogManager, session:AsyncSession):
        error_log_data = await ErrorLogFactory.create_async(session)
        result = await session.execute(select(ErrorLog).filter(ErrorLog.error_log_id == error_log_data.error_log_id))
        fetched_error_log = result.scalars().first()
        assert isinstance(fetched_error_log, ErrorLog)
        assert fetched_error_log.error_log_id == error_log_data.error_log_id
        deleted_error_log = await error_log_manager.delete(error_log_id=error_log_data.error_log_id)
        result = await session.execute(select(ErrorLog).filter(ErrorLog.error_log_id == error_log_data.error_log_id))
        fetched_error_log = result.scalars().first()
        assert fetched_error_log is None
    @pytest.mark.asyncio
    async def test_delete_nonexistent(self, error_log_manager:ErrorLogManager, session:AsyncSession):
        with pytest.raises(Exception):
            await error_log_manager.delete(999)
        await session.rollback()
    @pytest.mark.asyncio
    async def test_delete_invalid_type(self, error_log_manager:ErrorLogManager, session:AsyncSession):
        with pytest.raises(Exception):
            await error_log_manager.delete("999")
        await session.rollback()
    @pytest.mark.asyncio
    async def test_get_list(self, error_log_manager:ErrorLogManager, session:AsyncSession):
        error_logs = await error_log_manager.get_list()
        assert len(error_logs) == 0
        error_logs_data = [await ErrorLogFactory.create_async(session) for _ in range(5)]
        error_logs = await error_log_manager.get_list()
        assert len(error_logs) == 5
        assert all(isinstance(error_log, ErrorLog) for error_log in error_logs)
    @pytest.mark.asyncio
    async def test_to_json(self, error_log_manager:ErrorLogManager, session:AsyncSession):
        error_log = await ErrorLogFactory.build_async(session)
        json_data = error_log_manager.to_json(error_log)
        assert json_data is not None
    @pytest.mark.asyncio
    async def test_to_dict(self, error_log_manager:ErrorLogManager, session:AsyncSession):
        error_log = await ErrorLogFactory.build_async(session)
        dict_data = error_log_manager.to_dict(error_log)
        assert dict_data is not None
    @pytest.mark.asyncio
    async def test_from_json(self, error_log_manager:ErrorLogManager, session:AsyncSession):
        error_log = await ErrorLogFactory.create_async(session)
        json_data = error_log_manager.to_json(error_log)
        deserialized_error_log = error_log_manager.from_json(json_data)
        assert isinstance(deserialized_error_log, ErrorLog)
        assert deserialized_error_log.code == error_log.code
    @pytest.mark.asyncio
    async def test_from_dict(self, error_log_manager:ErrorLogManager, session:AsyncSession):
        error_log = await ErrorLogFactory.create_async(session)
        schema = ErrorLogSchema()
        error_log_data = schema.dump(error_log)
        deserialized_error_log = error_log_manager.from_dict(error_log_data)
        assert isinstance(deserialized_error_log, ErrorLog)
        assert deserialized_error_log.code == error_log.code
    @pytest.mark.asyncio
    async def test_add_bulk(self, error_log_manager:ErrorLogManager, session:AsyncSession):
        error_logs_data = [await ErrorLogFactory.build_async(session) for _ in range(5)]
        error_logs = await error_log_manager.add_bulk(error_logs_data)
        assert len(error_logs) == 5
        for updated_error_log in error_logs:
            result = await session.execute(select(ErrorLog).filter(ErrorLog.error_log_id == updated_error_log.error_log_id))
            fetched_error_log = result.scalars().first()
            assert isinstance(fetched_error_log, ErrorLog)
            assert fetched_error_log.error_log_id == updated_error_log.error_log_id
    @pytest.mark.asyncio
    async def test_update_bulk_success(self, error_log_manager:ErrorLogManager, session:AsyncSession):
        # Mocking error_log instances
        error_log1 = await ErrorLogFactory.create_async(session=session)
        error_log2 = await ErrorLogFactory.create_async(session=session)
        code_updated1 = generate_uuid()
        code_updated2 = generate_uuid()
        # Update error_logs
        updates = [{"error_log_id": 1, "code": code_updated1}, {"error_log_id": 2, "code": code_updated2}]
        updated_error_logs = await error_log_manager.update_bulk(updates)
        # Assertions
        assert len(updated_error_logs) == 2
        assert updated_error_logs[0].code == code_updated1
        assert updated_error_logs[1].code == code_updated2
        result = await session.execute(select(ErrorLog).filter(ErrorLog.error_log_id == 1))
        fetched_error_log = result.scalars().first()
        assert isinstance(fetched_error_log, ErrorLog)
        assert fetched_error_log.code == code_updated1
        result = await session.execute(select(ErrorLog).filter(ErrorLog.error_log_id == 2))
        fetched_error_log = result.scalars().first()
        assert isinstance(fetched_error_log, ErrorLog)
        assert fetched_error_log.code == code_updated2
    @pytest.mark.asyncio
    async def test_update_bulk_missing_error_log_id(self, error_log_manager:ErrorLogManager, session:AsyncSession):
        # No error_logs to update since error_log_id is missing
        updates = [{"name": "Red Rose"}]
        with pytest.raises(Exception):
            updated_error_logs = await error_log_manager.update_bulk(updates)
        await session.rollback()
    @pytest.mark.asyncio
    async def test_update_bulk_error_log_not_found(self, error_log_manager:ErrorLogManager, session:AsyncSession):
        # Update error_logs
        updates = [{"error_log_id": 1, "code": generate_uuid()}]
        with pytest.raises(Exception):
            updated_error_logs = await error_log_manager.update_bulk(updates)
        await session.rollback()
    @pytest.mark.asyncio
    async def test_update_bulk_invalid_type(self, error_log_manager:ErrorLogManager, session:AsyncSession):
        updates = [{"error_log_id": "2", "code": generate_uuid()}]
        with pytest.raises(Exception):
            updated_error_logs = await error_log_manager.update_bulk(updates)
        await session.rollback()
    @pytest.mark.asyncio
    async def test_delete_bulk_success(self, error_log_manager:ErrorLogManager, session:AsyncSession):
        error_log1 = await ErrorLogFactory.create_async(session=session)
        error_log2 = await ErrorLogFactory.create_async(session=session)
        # Delete error_logs
        error_log_ids = [1, 2]
        result = await error_log_manager.delete_bulk(error_log_ids)
        assert result is True
        for error_log_id in error_log_ids:
            execute_result = await session.execute(select(ErrorLog).filter(ErrorLog.error_log_id == error_log_id))
            fetched_error_log = execute_result.scalars().first()
            assert fetched_error_log is None
    @pytest.mark.asyncio
    async def test_delete_bulk_some_error_logs_not_found(self, error_log_manager:ErrorLogManager, session:AsyncSession):
        error_log1 = await ErrorLogFactory.create_async(session=session)
        # Delete error_logs
        error_log_ids = [1, 2]
        with pytest.raises(Exception):
           result = await error_log_manager.delete_bulk(error_log_ids)
        await session.rollback()
    @pytest.mark.asyncio
    async def test_delete_bulk_empty_list(self, error_log_manager:ErrorLogManager, session:AsyncSession):
        # Delete error_logs with an empty list
        error_log_ids = []
        result = await error_log_manager.delete_bulk(error_log_ids)
        # Assertions
        assert result is True
    @pytest.mark.asyncio
    async def test_delete_bulk_invalid_type(self, error_log_manager:ErrorLogManager, session:AsyncSession):
        error_log_ids = ["1", 2]
        with pytest.raises(Exception):
           result = await error_log_manager.delete_bulk(error_log_ids)
        await session.rollback()
    @pytest.mark.asyncio
    async def test_count_basic_functionality(self, error_log_manager:ErrorLogManager, session:AsyncSession):
        error_logs_data = [await ErrorLogFactory.create_async(session) for _ in range(5)]
        count = await error_log_manager.count()
        assert count == 5
    @pytest.mark.asyncio
    async def test_count_empty_database(self, error_log_manager:ErrorLogManager, session:AsyncSession):
        count = await error_log_manager.count()
        assert count == 0
    @pytest.mark.asyncio
    async def test_get_sorted_list_basic_sorting(self, error_log_manager:ErrorLogManager, session:AsyncSession):
        # Add error_logs
        error_logs_data = [await ErrorLogFactory.create_async(session) for _ in range(5)]
        sorted_error_logs = await error_log_manager.get_sorted_list(sort_by="error_log_id")
        assert [error_log.error_log_id for error_log in sorted_error_logs] == [(i + 1) for i in range(5)]
    @pytest.mark.asyncio
    async def test_get_sorted_list_descending_sorting(self, error_log_manager:ErrorLogManager, session:AsyncSession):
        # Add error_logs
        error_logs_data = [await ErrorLogFactory.create_async(session) for _ in range(5)]
        sorted_error_logs = await error_log_manager.get_sorted_list(sort_by="error_log_id", order="desc")
        assert [error_log.error_log_id for error_log in sorted_error_logs] == [(i + 1) for i in reversed(range(5))]
    @pytest.mark.asyncio
    async def test_get_sorted_list_invalid_attribute(self, error_log_manager:ErrorLogManager, session:AsyncSession):
        with pytest.raises(AttributeError):
            await error_log_manager.get_sorted_list(sort_by="invalid_attribute")
        await session.rollback()
    @pytest.mark.asyncio
    async def test_get_sorted_list_empty_database(self, error_log_manager:ErrorLogManager, session:AsyncSession):
        sorted_error_logs = await error_log_manager.get_sorted_list(sort_by="error_log_id")
        assert len(sorted_error_logs) == 0
    @pytest.mark.asyncio
    async def test_refresh_basic(self, error_log_manager:ErrorLogManager, session:AsyncSession):
        # Add a error_log
        error_log1 = await ErrorLogFactory.create_async(session=session)
        result = await session.execute(select(ErrorLog).filter(ErrorLog.error_log_id == error_log1.error_log_id))
        error_log2 = result.scalars().first()
        assert error_log1.code == error_log2.code
        updated_code1 = generate_uuid()
        error_log1.code = updated_code1
        updated_error_log1 = await error_log_manager.update(error_log1)
        assert updated_error_log1.code == updated_code1
        refreshed_error_log2 = await error_log_manager.refresh(error_log2)
        assert refreshed_error_log2.code == updated_code1
    @pytest.mark.asyncio
    async def test_refresh_nonexistent_error_log(self, error_log_manager:ErrorLogManager, session:AsyncSession):
        error_log = ErrorLog(error_log_id=999)
        with pytest.raises(Exception):
            await error_log_manager.refresh(error_log)
        await session.rollback()
    @pytest.mark.asyncio
    async def test_exists_with_existing_error_log(self, error_log_manager:ErrorLogManager, session:AsyncSession):
        # Add a error_log
        error_log1 = await ErrorLogFactory.create_async(session=session)
        # Check if the error_log exists using the manager function
        assert await error_log_manager.exists(error_log1.error_log_id) == True
    @pytest.mark.asyncio
    async def test_exists_with_nonexistent_error_log(self, error_log_manager:ErrorLogManager, session:AsyncSession):
        non_existent_id = 999
        assert await error_log_manager.exists(non_existent_id) == False
    @pytest.mark.asyncio
    async def test_exists_with_invalid_id_type(self, error_log_manager:ErrorLogManager, session:AsyncSession):
        invalid_id = "invalid_id"
        with pytest.raises(Exception):
            await error_log_manager.exists(invalid_id)
        await session.rollback()
#endet
    #browserCode,
    #contextCode,
    #createdUTCDateTime
    #description,
    #isClientSideError,
    #isResolved,
    #PacID
    @pytest.mark.asyncio
    async def test_get_by_pac_id_existing(self, error_log_manager:ErrorLogManager, session:AsyncSession):
        # Add a error_log with a specific pac_id
        error_log1 = await ErrorLogFactory.create_async(session=session)
        # Fetch the error_log using the manager function
        fetched_error_logs = await error_log_manager.get_by_pac_id(error_log1.pac_id)
        assert len(fetched_error_logs) == 1
        assert fetched_error_logs[0].code == error_log1.code
    @pytest.mark.asyncio
    async def test_get_by_pac_id_nonexistent(self, error_log_manager:ErrorLogManager, session:AsyncSession):
        non_existent_id = 999
        fetched_error_logs = await error_log_manager.get_by_pac_id(non_existent_id)
        assert len(fetched_error_logs) == 0
    @pytest.mark.asyncio
    async def test_get_by_pac_id_invalid_type(self, error_log_manager:ErrorLogManager, session:AsyncSession):
        invalid_id = "invalid_id"
        with pytest.raises(Exception):
            await error_log_manager.get_by_pac_id(invalid_id)
        await session.rollback()
    #url,
#endet
##todo test for is_equal
