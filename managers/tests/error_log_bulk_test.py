# models/managers/tests/error_log_test.py
# pylint: disable=protected-access
# pylint: disable=unused-argument
# pylint: disable=unused-import
"""
    This class contains unit tests for the
    `ErrorLogManager` class.
"""

import logging
import uuid  # noqa: F401

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from helpers.session_context import SessionContext
from managers.error_log import ErrorLogManager
from models import ErrorLog
from models.factory import ErrorLogFactory


class TestErrorLogBulkManager:
    """
    This class contains unit tests for the
    `ErrorLogManager` class.
    """

    @pytest_asyncio.fixture(scope="function")
    async def error_log_manager(self, session: AsyncSession):
        """
        Fixture that returns an instance of
        `ErrorLogManager` for testing.
        """
        session_context = SessionContext(dict(), session)
        session_context.customer_code = uuid.uuid4()
        return ErrorLogManager(session_context)

    @pytest.mark.asyncio
    async def test_add_bulk(
        self,
        error_log_manager: ErrorLogManager,
        session: AsyncSession
    ):
        """
        Test case for the `add_bulk` method of the
        `ErrorLogManager` class.

        This test case verifies that the `add_bulk`
        method correctly adds multiple
        error_logs to the database.

        Steps:
        1. Generate a list of error_log data using the
            `ErrorLogFactory.build_async` method.
        2. Call the `add_bulk` method of the
            `error_log_manager` instance,
            passing in the
            generated error_log data.
        3. Verify that the number of error_logs
            returned is
            equal to the number of error_logs added.
        4. For each updated error_log, fetch the corresponding
            error_log from the database.
        5. Verify that the fetched error_log
            is an instance of the
            `ErrorLog` class.
        6. Verify that the insert_user_id and
            last_update_user_id of the fetched
            error_log match the
            customer code of the session context.
        7. Verify that the error_log_id of the fetched
            error_log matches the
            error_log_id of the updated
            error_log.

        """
        error_logs_data = [
            await ErrorLogFactory.build_async(session) for _ in range(5)]

        error_logs = await error_log_manager.add_bulk(
            error_logs_data)

        assert len(error_logs) == 5

        for updated_error_log in error_logs:
            result = await session.execute(
                select(ErrorLog).filter(
                    ErrorLog._error_log_id == updated_error_log.error_log_id  # type: ignore
                )
            )
            fetched_error_log = result.scalars().first()

            assert isinstance(
                fetched_error_log,
                ErrorLog)

            assert str(fetched_error_log.insert_user_id) == (
                str(error_log_manager._session_context.customer_code))
            assert str(fetched_error_log.last_update_user_id) == (
                str(error_log_manager._session_context.customer_code))

            assert fetched_error_log.error_log_id == \
                updated_error_log.error_log_id

    @pytest.mark.asyncio
    async def test_update_bulk_success(
        self,
        error_log_manager: ErrorLogManager,
        session: AsyncSession
    ):
        """
        Test case for bulk update of error_logs.

        This test case verifies the functionality of the
        `update_bulk` method in the
        `ErrorLogManager` class.
        It creates two error_log instances,
        updates their codes
        using the `update_bulk` method, and then verifies
        that the updates were successful by checking the
        updated codes in the database.

        Steps:
        1. Create two error_log instances using the
            `ErrorLogFactory.create_async` method.
        2. Generate new codes for the error_logs.
        3. Update the error_logs' codes
            using the `update_bulk` method.
        4. Verify that the update was successful by checking
            the updated codes in the database.

        Args:
            error_log_manager (ErrorLogManager):
                An instance of the
                `ErrorLogManager` class.
            session (AsyncSession): An instance of the `AsyncSession` class.

        Returns:
            None
        """
        # Mocking error_log instances
        error_log1 = await ErrorLogFactory. \
            create_async(
                session=session)
        error_log2 = await ErrorLogFactory. \
            create_async(
                session=session)
        logging.info(error_log1.__dict__)

        code_updated1 = uuid.uuid4()
        code_updated2 = uuid.uuid4()
        logging.info(code_updated1)
        logging.info(code_updated2)

        # Update error_logs
        updates = [
            {
                "error_log_id":
                    error_log1.error_log_id,
                "code": code_updated1
            },
            {
                "error_log_id":
                    error_log2.error_log_id,
                "code": code_updated2
            }
        ]
        updated_error_logs = await error_log_manager.update_bulk(
            updates)

        logging.info('bulk update results')
        # Assertions
        assert len(updated_error_logs) == 2
        logging.info(updated_error_logs[0]
                     .__dict__)
        logging.info(updated_error_logs[1]
                     .__dict__)

        logging.info('getall')
        error_logs = await error_log_manager.get_list()
        logging.info(error_logs[0]
                     .__dict__)
        logging.info(error_logs[1]
                     .__dict__)

        assert updated_error_logs[0].code == \
            code_updated1
        assert updated_error_logs[1].code == \
            code_updated2

        assert str(updated_error_logs[0]
                   .last_update_user_id) == (
            str(error_log_manager
                ._session_context.customer_code))

        assert str(updated_error_logs[1]
                   .last_update_user_id) == (
            str(error_log_manager
                ._session_context.customer_code))

        result = await session.execute(
            select(ErrorLog).filter(
                ErrorLog._error_log_id == 1)  # type: ignore
        )
        fetched_error_log = result.scalars().first()

        assert isinstance(fetched_error_log,
                          ErrorLog)

        assert fetched_error_log.code == code_updated1

        result = await session.execute(
            select(ErrorLog).filter(
                ErrorLog._error_log_id == 2)  # type: ignore
        )
        fetched_error_log = result.scalars().first()

        assert isinstance(fetched_error_log,
                          ErrorLog)

        assert fetched_error_log.code == code_updated2

    @pytest.mark.asyncio
    async def test_update_bulk_missing_error_log_id(
        self,
        error_log_manager: ErrorLogManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of the `update_bulk`
        method when the error_log_id is missing.

        This test case ensures that when the error_log_id is
        missing in the updates list,
        an exception is raised and the session is rolled back.

        Steps:
        1. Prepare the updates list with a missing error_log_id.
        2. Call the `update_bulk` method with the updates list.
        3. Assert that an exception is raised.
        4. Rollback the session to undo any changes made during the test.

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
        Test case to verify the behavior of the update_bulk
        method when a error_log is not found.

        This test case performs the following steps:
        1. Defines a list of error_log updates,
            where each update
            contains a error_log_id and a code.
        2. Calls the update_bulk method of the
            error_log_manager with the list of updates.
        3. Expects an exception to be raised, indicating that
            the error_log was not found.
        4. Rolls back the session to undo any changes made during the test.

        Note: This test assumes that the update_bulk method
        throws an exception when a
        error_log is not found.

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
        Test case to verify the behavior of the
        update_bulk method when invalid data types are provided.

        This test case verifies that when the update_bulk method
        is called with a list of updates containing invalid data types,
        an exception is raised. The test case also ensures
        that the session is rolled back after the test
        to maintain data integrity.

        :param error_log_manager: An instance of the
            ErrorLogManager class.
        :param session: An instance of the AsyncSession class.
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
        Test case for the delete_bulk method of the
        ErrorLogManager class.

        This test verifies that the delete_bulk method
        successfully deletes multiple error_logs
        from the database.

        Steps:
        1. Create two error_log objects
            using the ErrorLogFactory.
        2. Delete the error_logs using the
            delete_bulk method
            of the error_log_manager.
        3. Verify that the delete operation was successful by
            checking if the error_logs no longer exist in the database.

        Expected Result:
        - The delete_bulk method should return True, indicating
            that the delete operation was successful.
        - The error_logs should no longer exist in the database.

        """

        error_log1 = await ErrorLogFactory.create_async(
            session=session)

        error_log2 = await ErrorLogFactory.create_async(
            session=session)

        # Delete error_logs
        error_log_ids = [error_log1.error_log_id,
                     error_log2.error_log_id]
        result = await error_log_manager.delete_bulk(
            error_log_ids)

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
        Test case to verify the behavior of deleting bulk
        error_logs when some error_logs are not found.

        Steps:
        1. Create a error_log using the
            ErrorLogFactory.
        2. Assert that the created error_log
            is an instance of the
            ErrorLog class.
        3. Define a list of error_log IDs to delete.
        4. Use pytest.raises to assert that an exception is
            raised when deleting the bulk error_logs.
        5. Rollback the session to undo any changes made during the test.

        This test case ensures that the delete_bulk method of the
        ErrorLogManager raises an exception
        when some error_logs with the specified IDs are
        not found in the database.
        """
        error_log1 = await ErrorLogFactory.create_async(
            session=session)

        assert isinstance(error_log1,
                          ErrorLog)

        # Delete error_logs
        error_log_ids = [1, 2]

        with pytest.raises(Exception):
            await error_log_manager.delete_bulk(
                error_log_ids)

        await session.rollback()

    @pytest.mark.asyncio
    async def test_delete_bulk_empty_list(
        self,
        error_log_manager: ErrorLogManager
    ):
        """
        Test case to verify the behavior of deleting
        error_logs with an empty list.

        Args:
            error_log_manager (ErrorLogManager): The
                instance of the
                ErrorLogManager class.

        Returns:
            None

        Raises:
            AssertionError: If the result is not True.
        """

        # Delete error_logs with an empty list
        error_log_ids = []
        result = await error_log_manager.delete_bulk(
            error_log_ids)

        # Assertions
        assert result is True

    @pytest.mark.asyncio
    async def test_delete_bulk_invalid_type(
        self,
        error_log_manager: ErrorLogManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of the delete_bulk
        method when invalid error_log IDs are provided.

        Args:
            error_log_manager (ErrorLogManager): The
                instance of the
                ErrorLogManager class.
            session (AsyncSession): The async session object.

        Raises:
            Exception: If an exception is raised during the
                execution of the delete_bulk method.

        Returns:
            None
        """

        error_log_ids = ["1", 2]

        with pytest.raises(Exception):
            await error_log_manager.delete_bulk(
                error_log_ids)

        await session.rollback()

