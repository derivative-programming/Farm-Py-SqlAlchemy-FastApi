# models/managers/tests/error_log_test.py
# pylint: disable=protected-access
# pylint: disable=unused-argument
"""
    #TODO add comment
    #TODO file too big. split into separate test files
"""
import logging
from typing import List
import uuid
import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
import models
from helpers.session_context import SessionContext
from managers.error_log import ErrorLogManager
from models import ErrorLog
from models.factory import ErrorLogFactory
from models.serialization_schema.error_log import ErrorLogSchema
class TestErrorLogManager:
    """
    #TODO add comment
    """
    @pytest_asyncio.fixture(scope="function")
    async def error_log_manager(self, session: AsyncSession):
        """
            #TODO add comment
        """
        session_context = SessionContext(dict(), session)
        session_context.customer_code = uuid.uuid4()
        return ErrorLogManager(session_context)
    @pytest.mark.asyncio
    async def test_build(
        self,
        error_log_manager: ErrorLogManager
    ):
        """
            #TODO add comment
        """
        # Define mock data for our error_log
        mock_data = {
            "code": uuid.uuid4()
        }
        # Call the build function of the manager
        error_log = await error_log_manager.build(**mock_data)
        # Assert that the returned object is an instance of ErrorLog
        assert isinstance(error_log, ErrorLog)
        # Assert that the attributes of the error_log match our mock data
        assert error_log.code == mock_data["code"]
    @pytest.mark.asyncio
    async def test_build_with_missing_data(
        self,
        error_log_manager: ErrorLogManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        # Define mock data with a missing key
        mock_data = {
            "non_existant_property": "Rose"
        }
        # If the build method is expected to raise an exception for
        # missing data, test for that
        with pytest.raises(Exception):
            await error_log_manager.build(**mock_data)
        await session.rollback()
    @pytest.mark.asyncio
    async def test_add_correctly_adds_error_log_to_database(
        self,
        error_log_manager: ErrorLogManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        test_error_log = await ErrorLogFactory.build_async(session)
        assert test_error_log.error_log_id == 0
        # Add the error_log using the manager's add method
        added_error_log = await error_log_manager.add(error_log=test_error_log)
        assert isinstance(added_error_log, ErrorLog)
        assert str(added_error_log.insert_user_id) == (
            str(error_log_manager._session_context.customer_code))
        assert str(added_error_log.last_update_user_id) == (
            str(error_log_manager._session_context.customer_code))
        assert added_error_log.error_log_id > 0
        # Fetch the error_log from the database directly
        result = await session.execute(
            select(ErrorLog).filter(
                ErrorLog._error_log_id == added_error_log.error_log_id  # type: ignore
            )
        )
        fetched_error_log = result.scalars().first()
        # Assert that the fetched error_log is not None and matches the added error_log
        assert fetched_error_log is not None
        assert isinstance(fetched_error_log, ErrorLog)
        assert fetched_error_log.error_log_id == added_error_log.error_log_id
    @pytest.mark.asyncio
    async def test_add_returns_correct_error_log_object(
        self,
        error_log_manager: ErrorLogManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        # Create a test error_log using the ErrorLogFactory
        # without persisting it to the database
        test_error_log = await ErrorLogFactory.build_async(session)
        assert test_error_log.error_log_id == 0
        test_error_log.code = uuid.uuid4()
        # Add the error_log using the manager's add method
        added_error_log = await error_log_manager.add(error_log=test_error_log)
        assert isinstance(added_error_log, ErrorLog)
        assert str(added_error_log.insert_user_id) == (
            str(error_log_manager._session_context.customer_code))
        assert str(added_error_log.last_update_user_id) == (
            str(error_log_manager._session_context.customer_code))
        assert added_error_log.error_log_id > 0
        # Assert that the returned error_log matches the test error_log
        assert added_error_log.error_log_id == test_error_log.error_log_id
        assert added_error_log.code == test_error_log.code
    @pytest.mark.asyncio
    async def test_get_by_id(
        self,
        error_log_manager: ErrorLogManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        test_error_log = await ErrorLogFactory.create_async(session)
        error_log = await error_log_manager.get_by_id(test_error_log.error_log_id)
        assert isinstance(error_log, ErrorLog)
        assert test_error_log.error_log_id == error_log.error_log_id
        assert test_error_log.code == error_log.code
    @pytest.mark.asyncio
    async def test_get_by_id_not_found(
        self,
        error_log_manager: ErrorLogManager
    ):
        """
            #TODO add comment
        """
        non_existent_id = 9999  # An ID that's not in the database
        retrieved_error_log = await error_log_manager.get_by_id(non_existent_id)
        assert retrieved_error_log is None
    @pytest.mark.asyncio
    async def test_get_by_code_returns_error_log(
        self,
        error_log_manager: ErrorLogManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        test_error_log = await ErrorLogFactory.create_async(session)
        error_log = await error_log_manager.get_by_code(test_error_log.code)
        assert isinstance(error_log, ErrorLog)
        assert test_error_log.error_log_id == error_log.error_log_id
        assert test_error_log.code == error_log.code
    @pytest.mark.asyncio
    async def test_get_by_code_returns_none_for_nonexistent_code(
        self,
        error_log_manager: ErrorLogManager
    ):
        """
            #TODO add comment
        """
        # Generate a random UUID that doesn't correspond to
        # any ErrorLog in the database
        random_code = uuid.uuid4()
        error_log = await error_log_manager.get_by_code(random_code)
        assert error_log is None
    @pytest.mark.asyncio
    async def test_update(
        self,
        error_log_manager: ErrorLogManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        test_error_log = await ErrorLogFactory.create_async(session)
        test_error_log.code = uuid.uuid4()
        updated_error_log = await error_log_manager.update(error_log=test_error_log)
        assert isinstance(updated_error_log, ErrorLog)
        assert str(updated_error_log.last_update_user_id) == str(
            error_log_manager._session_context.customer_code)
        assert updated_error_log.error_log_id == test_error_log.error_log_id
        assert updated_error_log.code == test_error_log.code
        result = await session.execute(
            select(ErrorLog).filter(
                ErrorLog._error_log_id == test_error_log.error_log_id)  # type: ignore
        )
        fetched_error_log = result.scalars().first()
        assert updated_error_log.error_log_id == fetched_error_log.error_log_id
        assert updated_error_log.code == fetched_error_log.code
        assert test_error_log.error_log_id == fetched_error_log.error_log_id
        assert test_error_log.code == fetched_error_log.code
    @pytest.mark.asyncio
    async def test_update_via_dict(
        self,
        error_log_manager: ErrorLogManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        test_error_log = await ErrorLogFactory.create_async(session)
        new_code = uuid.uuid4()
        updated_error_log = await error_log_manager.update(
            error_log=test_error_log,
            code=new_code
        )
        assert isinstance(updated_error_log, ErrorLog)
        assert str(updated_error_log.last_update_user_id) == str(
            error_log_manager._session_context.customer_code
        )
        assert updated_error_log.error_log_id == test_error_log.error_log_id
        assert updated_error_log.code == new_code
        result = await session.execute(
            select(ErrorLog).filter(
                ErrorLog._error_log_id == test_error_log.error_log_id)  # type: ignore
        )
        fetched_error_log = result.scalars().first()
        assert updated_error_log.error_log_id == fetched_error_log.error_log_id
        assert updated_error_log.code == fetched_error_log.code
        assert test_error_log.error_log_id == fetched_error_log.error_log_id
        assert new_code == fetched_error_log.code
    @pytest.mark.asyncio
    async def test_update_invalid_error_log(
        self,
        error_log_manager: ErrorLogManager
    ):
        """
            #TODO add comment
        """
        # None error_log
        error_log = None
        new_code = uuid.uuid4()
        updated_error_log = await (
            error_log_manager.update(error_log, code=new_code))  # type: ignore
        # Assertions
        assert updated_error_log is None
    @pytest.mark.asyncio
    async def test_update_with_nonexistent_attribute(
        self,
        error_log_manager: ErrorLogManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        test_error_log = await ErrorLogFactory.create_async(session)
        new_code = uuid.uuid4()
        with pytest.raises(ValueError):
            await error_log_manager.update(
                error_log=test_error_log,
                xxx=new_code
            )
        await session.rollback()
    @pytest.mark.asyncio
    async def test_delete(
        self,
        error_log_manager: ErrorLogManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        error_log_data = await ErrorLogFactory.create_async(session)
        result = await session.execute(
            select(ErrorLog).filter(
                ErrorLog._error_log_id == error_log_data.error_log_id)  # type: ignore
        )
        fetched_error_log = result.scalars().first()
        assert isinstance(fetched_error_log, ErrorLog)
        assert fetched_error_log.error_log_id == error_log_data.error_log_id
        await error_log_manager.delete(
            error_log_id=error_log_data.error_log_id)
        result = await session.execute(
            select(ErrorLog).filter(
                ErrorLog._error_log_id == error_log_data.error_log_id)  # type: ignore
        )
        fetched_error_log = result.scalars().first()
        assert fetched_error_log is None
    @pytest.mark.asyncio
    async def test_delete_nonexistent(
        self,
        error_log_manager: ErrorLogManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        with pytest.raises(Exception):
            await error_log_manager.delete(999)
        await session.rollback()
    @pytest.mark.asyncio
    async def test_delete_invalid_type(
        self,
        error_log_manager: ErrorLogManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        with pytest.raises(Exception):
            await error_log_manager.delete("999")
        await session.rollback()
    @pytest.mark.asyncio
    async def test_get_list(
        self,
        error_log_manager: ErrorLogManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        error_logs = await error_log_manager.get_list()
        assert len(error_logs) == 0
        error_logs_data = (
            [await ErrorLogFactory.create_async(session) for _ in range(5)])
        assert isinstance(error_logs_data, List)
        error_logs = await error_log_manager.get_list()
        assert len(error_logs) == 5
        assert all(isinstance(error_log, ErrorLog) for error_log in error_logs)
    @pytest.mark.asyncio
    async def test_to_json(
        self,
        error_log_manager: ErrorLogManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        error_log = await ErrorLogFactory.build_async(session)
        json_data = error_log_manager.to_json(error_log)
        assert json_data is not None
    @pytest.mark.asyncio
    async def test_to_dict(
        self,
        error_log_manager: ErrorLogManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        error_log = await ErrorLogFactory.build_async(session)
        dict_data = error_log_manager.to_dict(error_log)
        assert dict_data is not None
    @pytest.mark.asyncio
    async def test_from_json(
        self,
        error_log_manager: ErrorLogManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        error_log = await ErrorLogFactory.create_async(session)
        json_data = error_log_manager.to_json(error_log)
        deserialized_error_log = error_log_manager.from_json(json_data)
        assert isinstance(deserialized_error_log, ErrorLog)
        assert deserialized_error_log.code == error_log.code
    @pytest.mark.asyncio
    async def test_from_dict(
        self,
        error_log_manager: ErrorLogManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        error_log = await ErrorLogFactory.create_async(session)
        schema = ErrorLogSchema()
        error_log_data = schema.dump(error_log)
        deserialized_error_log = error_log_manager.from_dict(error_log_data)
        assert isinstance(deserialized_error_log, ErrorLog)
        assert deserialized_error_log.code == error_log.code
    @pytest.mark.asyncio
    async def test_add_bulk(
        self,
        error_log_manager: ErrorLogManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        error_logs_data = [
            await ErrorLogFactory.build_async(session) for _ in range(5)]
        error_logs = await error_log_manager.add_bulk(error_logs_data)
        assert len(error_logs) == 5
        for updated_error_log in error_logs:
            result = await session.execute(
                select(ErrorLog).filter(
                    ErrorLog._error_log_id == updated_error_log.error_log_id  # type: ignore
                )
            )
            fetched_error_log = result.scalars().first()
            assert isinstance(fetched_error_log, ErrorLog)
            assert str(fetched_error_log.insert_user_id) == (
                str(error_log_manager._session_context.customer_code))
            assert str(fetched_error_log.last_update_user_id) == (
                str(error_log_manager._session_context.customer_code))
            assert fetched_error_log.error_log_id == updated_error_log.error_log_id
    @pytest.mark.asyncio
    async def test_update_bulk_success(
        self,
        error_log_manager: ErrorLogManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        # Mocking error_log instances
        error_log1 = await ErrorLogFactory.create_async(session=session)
        error_log2 = await ErrorLogFactory.create_async(session=session)
        logging.info(error_log1.__dict__)
        code_updated1 = uuid.uuid4()
        code_updated2 = uuid.uuid4()
        logging.info(code_updated1)
        logging.info(code_updated2)
        # Update error_logs
        updates = [
            {
                "error_log_id": error_log1.error_log_id,
                "code": code_updated1
            },
            {
                "error_log_id": error_log2.error_log_id,
                "code": code_updated2
            }
        ]
        updated_error_logs = await error_log_manager.update_bulk(updates)
        logging.info('bulk update results')
        # Assertions
        assert len(updated_error_logs) == 2
        logging.info(updated_error_logs[0].__dict__)
        logging.info(updated_error_logs[1].__dict__)
        logging.info('getall')
        error_logs = await error_log_manager.get_list()
        logging.info(error_logs[0].__dict__)
        logging.info(error_logs[1].__dict__)
        assert updated_error_logs[0].code == code_updated1
        assert updated_error_logs[1].code == code_updated2
        assert str(updated_error_logs[0].last_update_user_id) == (
            str(error_log_manager._session_context.customer_code))
        assert str(updated_error_logs[1].last_update_user_id) == (
            str(error_log_manager._session_context.customer_code))
        result = await session.execute(
            select(ErrorLog).filter(ErrorLog._error_log_id == 1)  # type: ignore
        )
        fetched_error_log = result.scalars().first()
        assert isinstance(fetched_error_log, ErrorLog)
        assert fetched_error_log.code == code_updated1
        result = await session.execute(
            select(ErrorLog).filter(ErrorLog._error_log_id == 2)  # type: ignore
        )
        fetched_error_log = result.scalars().first()
        assert isinstance(fetched_error_log, ErrorLog)
        assert fetched_error_log.code == code_updated2
    @pytest.mark.asyncio
    async def test_update_bulk_missing_error_log_id(
        self,
        error_log_manager: ErrorLogManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        # No error_logs to update since error_log_id is missing
        updates = [{"name": "Red Rose"}]
        with pytest.raises(Exception):
            await error_log_manager.update_bulk(updates)
        await session.rollback()
    @pytest.mark.asyncio
    async def test_update_bulk_error_log_not_found(
        self,
        error_log_manager: ErrorLogManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        # Update error_logs
        updates = [{"error_log_id": 1, "code": uuid.uuid4()}]
        with pytest.raises(Exception):
            await error_log_manager.update_bulk(updates)
        await session.rollback()
    @pytest.mark.asyncio
    async def test_update_bulk_invalid_type(
        self,
        error_log_manager: ErrorLogManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        updates = [{"error_log_id": "2", "code": uuid.uuid4()}]
        with pytest.raises(Exception):
            await error_log_manager.update_bulk(updates)
        await session.rollback()
    @pytest.mark.asyncio
    async def test_delete_bulk_success(
        self,
        error_log_manager: ErrorLogManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        error_log1 = await ErrorLogFactory.create_async(session=session)
        error_log2 = await ErrorLogFactory.create_async(session=session)
        # Delete error_logs
        error_log_ids = [error_log1.error_log_id, error_log2.error_log_id]
        result = await error_log_manager.delete_bulk(error_log_ids)
        assert result is True
        for error_log_id in error_log_ids:
            execute_result = await session.execute(
                select(ErrorLog).filter(
                    ErrorLog._error_log_id == error_log_id)  # type: ignore
            )
            fetched_error_log = execute_result.scalars().first()
            assert fetched_error_log is None
    @pytest.mark.asyncio
    async def test_delete_bulk_error_logs_not_found(
        self,
        error_log_manager: ErrorLogManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        error_log1 = await ErrorLogFactory.create_async(session=session)
        assert isinstance(error_log1, ErrorLog)
        # Delete error_logs
        error_log_ids = [1, 2]
        with pytest.raises(Exception):
            await error_log_manager.delete_bulk(error_log_ids)
        await session.rollback()
    @pytest.mark.asyncio
    async def test_delete_bulk_empty_list(
        self,
        error_log_manager: ErrorLogManager
    ):
        """
            #TODO add comment
        """
        # Delete error_logs with an empty list
        error_log_ids = []
        result = await error_log_manager.delete_bulk(error_log_ids)
        # Assertions
        assert result is True
    @pytest.mark.asyncio
    async def test_delete_bulk_invalid_type(
        self,
        error_log_manager: ErrorLogManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        error_log_ids = ["1", 2]
        with pytest.raises(Exception):
            await error_log_manager.delete_bulk(error_log_ids)
        await session.rollback()
    @pytest.mark.asyncio
    async def test_count_basic_functionality(
        self,
        error_log_manager: ErrorLogManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        error_logs_data = (
            [await ErrorLogFactory.create_async(session) for _ in range(5)])
        assert isinstance(error_logs_data, List)
        count = await error_log_manager.count()
        assert count == 5
    @pytest.mark.asyncio
    async def test_count_empty_database(
        self,
        error_log_manager: ErrorLogManager
    ):
        """
            #TODO add comment
        """
        count = await error_log_manager.count()
        assert count == 0
    @pytest.mark.asyncio
    async def test_get_sorted_list_basic_sorting(
        self,
        error_log_manager: ErrorLogManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        # Add error_logs
        error_logs_data = (
            [await ErrorLogFactory.create_async(session) for _ in range(5)])
        assert isinstance(error_logs_data, List)
        sorted_error_logs = await error_log_manager.get_sorted_list(
            sort_by="_error_log_id")
        assert [error_log.error_log_id for error_log in sorted_error_logs] == (
            [(i + 1) for i in range(5)])
    @pytest.mark.asyncio
    async def test_get_sorted_list_descending_sorting(
        self,
        error_log_manager: ErrorLogManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        # Add error_logs
        error_logs_data = (
            [await ErrorLogFactory.create_async(session) for _ in range(5)])
        assert isinstance(error_logs_data, List)
        sorted_error_logs = await error_log_manager.get_sorted_list(
            sort_by="error_log_id", order="desc")
        assert [error_log.error_log_id for error_log in sorted_error_logs] == (
            [(i + 1) for i in reversed(range(5))])
    @pytest.mark.asyncio
    async def test_get_sorted_list_invalid_attribute(
        self,
        error_log_manager: ErrorLogManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        with pytest.raises(AttributeError):
            await error_log_manager.get_sorted_list(sort_by="invalid_attribute")
        await session.rollback()
    @pytest.mark.asyncio
    async def test_get_sorted_list_empty_database(
        self,
        error_log_manager: ErrorLogManager
    ):
        """
            #TODO add comment
        """
        sorted_error_logs = await error_log_manager.get_sorted_list(sort_by="error_log_id")
        assert len(sorted_error_logs) == 0
    @pytest.mark.asyncio
    async def test_refresh_basic(
        self,
        error_log_manager: ErrorLogManager,
        session: AsyncSession
    ):
        """
        Test the basic functionality of refreshing a error_log instance.
        This test performs the following steps:
        1. Creates a error_log instance using the ErrorLogFactory.
        2. Retrieves the error_log from the database to ensure
            it was added correctly.
        3. Updates the error_log's code and verifies the update.
        4. Refreshes the original error_log instance and checks if
            it reflects the updated code.
        Args:
            error_log_manager (ErrorLogManager): The manager responsible
                for error_log operations.
            session (AsyncSession): The SQLAlchemy asynchronous session.
        """
        # Add a error_log
        error_log1 = await ErrorLogFactory.create_async(session=session)
        # Retrieve the error_log from the database
        result = await session.execute(
            select(ErrorLog).filter(
                ErrorLog._error_log_id == error_log1.error_log_id)  # type: ignore
        )  # type: ignore
        error_log2 = result.scalars().first()
        # Verify that the retrieved error_log matches the added error_log
        assert error_log1.code == error_log2.code
        # Update the error_log's code
        updated_code1 = uuid.uuid4()
        error_log1.code = updated_code1
        updated_error_log1 = await error_log_manager.update(error_log1)
        # Verify that the updated error_log is of type ErrorLog
        # and has the updated code
        assert isinstance(updated_error_log1, ErrorLog)
        assert updated_error_log1.code == updated_code1
        # Refresh the original error_log instance
        refreshed_error_log2 = await error_log_manager.refresh(error_log2)
        # Verify that the refreshed error_log reflects the updated code
        assert refreshed_error_log2.code == updated_code1
    @pytest.mark.asyncio
    async def test_refresh_nonexistent_error_log(
        self,
        error_log_manager: ErrorLogManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        error_log = ErrorLog(error_log_id=999)
        with pytest.raises(Exception):
            await error_log_manager.refresh(error_log)
        await session.rollback()
    @pytest.mark.asyncio
    async def test_exists_with_existing_error_log(
        self,
        error_log_manager: ErrorLogManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        # Add a error_log
        error_log1 = await ErrorLogFactory.create_async(session=session)
        # Check if the error_log exists using the manager function
        assert await error_log_manager.exists(error_log1.error_log_id) is True
    @pytest.mark.asyncio
    async def test_is_equal_with_existing_error_log(
        self,
        error_log_manager: ErrorLogManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        # Add a error_log
        error_log1 = await ErrorLogFactory.create_async(session=session)
        error_log2 = await error_log_manager.get_by_id(error_log_id=error_log1.error_log_id)
        assert error_log_manager.is_equal(error_log1, error_log2) is True
        error_log1_dict = error_log_manager.to_dict(error_log1)
        error_log3 = error_log_manager.from_dict(error_log1_dict)
        assert error_log_manager.is_equal(error_log1, error_log3) is True
    @pytest.mark.asyncio
    async def test_exists_with_nonexistent_error_log(
        self,
        error_log_manager: ErrorLogManager
    ):
        """
            #TODO add comment
        """
        non_existent_id = 999
        assert await error_log_manager.exists(non_existent_id) is False
    @pytest.mark.asyncio
    async def test_exists_with_invalid_id_type(
        self,
        error_log_manager: ErrorLogManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        invalid_id = "invalid_id"
        with pytest.raises(Exception):
            await error_log_manager.exists(invalid_id)
        await session.rollback()
# endset
    # browserCode,
    # contextCode,
    # createdUTCDateTime
    # description,
    # isClientSideError,
    # isResolved,
    # PacID
    @pytest.mark.asyncio
    async def test_get_by_pac_id_existing(
        self,
        error_log_manager: ErrorLogManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        # Add a error_log with a specific pac_id
        error_log1 = await ErrorLogFactory.create_async(session=session)
        # Fetch the error_log using the manager function
        fetched_error_logs = await error_log_manager.get_by_pac_id(error_log1.pac_id)
        assert len(fetched_error_logs) == 1
        assert isinstance(fetched_error_logs[0], ErrorLog)
        assert fetched_error_logs[0].code == error_log1.code
    @pytest.mark.asyncio
    async def test_get_by_pac_id_nonexistent(
        self,
        error_log_manager: ErrorLogManager
    ):
        """
            #TODO add comment
        """
        non_existent_id = 999
        fetched_error_logs = await error_log_manager.get_by_pac_id(non_existent_id)
        assert len(fetched_error_logs) == 0
    @pytest.mark.asyncio
    async def test_get_by_pac_id_invalid_type(
        self,
        error_log_manager: ErrorLogManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        invalid_id = "invalid_id"
        with pytest.raises(Exception):
            await error_log_manager.get_by_pac_id(invalid_id)
        await session.rollback()
    # url,
# endset
