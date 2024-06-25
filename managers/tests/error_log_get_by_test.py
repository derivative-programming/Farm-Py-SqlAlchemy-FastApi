# models/managers/tests/error_log_test.py
# pylint: disable=protected-access
# pylint: disable=unused-argument
"""
    This class contains unit tests for the
    `ErrorLogManager` class.
"""

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


class TestErrorLogGetByManager:
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
    async def test_build(
        self,
        error_log_manager: ErrorLogManager
    ):
        """
        Test case for the `build` method of
        `ErrorLogManager`.
        """
        # Define mock data for our error_log
        mock_data = {
            "code": uuid.uuid4()
        }

        # Call the build function of the manager
        error_log = await error_log_manager.build(
            **mock_data)

        # Assert that the returned object is an instance of ErrorLog
        assert isinstance(
            error_log, ErrorLog)

        # Assert that the attributes of the
        # error_log match our mock data
        assert error_log.code == mock_data["code"]

    @pytest.mark.asyncio
    async def test_get_by_id(
        self,
        error_log_manager: ErrorLogManager,
        session: AsyncSession
    ):
        """
        Test case for the `get_by_id` method of
        `ErrorLogManager`.
        """
        test_error_log = await ErrorLogFactory.create_async(
            session)

        error_log = await error_log_manager.get_by_id(
            test_error_log.error_log_id)

        assert isinstance(
            error_log, ErrorLog)

        assert test_error_log.error_log_id == \
            error_log.error_log_id
        assert test_error_log.code == \
            error_log.code

    @pytest.mark.asyncio
    async def test_get_by_id_not_found(
        self,
        error_log_manager: ErrorLogManager
    ):
        """
        Test case for the `get_by_id` method of
        `ErrorLogManager` when the
        error_log is not found.
        """

        non_existent_id = 9999  # An ID that's not in the database

        retrieved_error_log = await error_log_manager.get_by_id(
            non_existent_id)

        assert retrieved_error_log is None

    @pytest.mark.asyncio
    async def test_get_by_code_returns_error_log(
        self,
        error_log_manager: ErrorLogManager,
        session: AsyncSession
    ):
        """
        Test case for the `get_by_code` method of
        `ErrorLogManager` that checks if
        a error_log is
        returned by its code.
        """

        test_error_log = await ErrorLogFactory.create_async(
            session)

        error_log = await error_log_manager.get_by_code(
            test_error_log.code)

        assert isinstance(
            error_log, ErrorLog)

        assert test_error_log.error_log_id == \
            error_log.error_log_id
        assert test_error_log.code == \
            error_log.code

    @pytest.mark.asyncio
    async def test_get_by_code_returns_none_for_nonexistent_code(
        self,
        error_log_manager: ErrorLogManager
    ):
        """
        Test case for the `get_by_code` method of
        `ErrorLogManager` when the code does not exist.
        """
        # Generate a random UUID that doesn't correspond to
        # any ErrorLog in the database
        random_code = uuid.uuid4()

        error_log = await error_log_manager.get_by_code(
            random_code)

        assert error_log is None

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
        Test case to verify the behavior of the
        `get_by_pac_id` method when
        a error_log with
        a specific pac_id exists.

        Steps:
        1. Create a error_log using the
            ErrorLogFactory.
        2. Fetch the error_log using the
            `get_by_pac_id` method of the error_log_manager.
        3. Assert that the fetched error_logs list contains
            only one error_log.
        4. Assert that the fetched error_log
            is an instance
            of the ErrorLog class.
        5. Assert that the code of the fetched error_log
            matches the code of the created error_log.
        6. Fetch the corresponding pac object
            using the pac_id of the created error_log.
        7. Assert that the fetched pac object is
            an instance of the Pac class.
        8. Assert that the pac_code_peek of the fetched
            error_log matches the
            code of the fetched pac.

        """
        # Add a error_log with a specific
        # pac_id
        error_log1 = await ErrorLogFactory.create_async(
            session=session)

        # Fetch the error_log using
        # the manager function

        fetched_error_logs = await error_log_manager.get_by_pac_id(
            error_log1.pac_id)
        assert len(fetched_error_logs) == 1
        assert isinstance(fetched_error_logs[0], ErrorLog)
        assert fetched_error_logs[0].code == \
            error_log1.code

        stmt = select(models.Pac).where(
            models.Pac._pac_id == error_log1.pac_id)  # type: ignore  # noqa: E501
        result = await session.execute(stmt)
        pac = result.scalars().first()

        assert isinstance(pac, models.Pac)

        assert fetched_error_logs[0].pac_code_peek == pac.code

    @pytest.mark.asyncio
    async def test_get_by_pac_id_nonexistent(
        self,
        error_log_manager: ErrorLogManager
    ):
        """
        Test case to verify the behavior of the
        get_by_pac_id method when the pac ID does not exist.

        This test case ensures that when a non-existent
        pac ID is provided to the get_by_pac_id method,
        an empty list is returned.
        """

        non_existent_id = 999

        fetched_error_logs = await error_log_manager.get_by_pac_id(
            non_existent_id)
        assert len(fetched_error_logs) == 0

    @pytest.mark.asyncio
    async def test_get_by_pac_id_invalid_type(
        self,
        error_log_manager: ErrorLogManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of the
        `get_by_pac_id` method when an invalid pac ID is provided.

        Args:
            error_log_manager (ErrorLogManager): An
                instance of the ErrorLogManager class.
            session (AsyncSession): An instance
                of the AsyncSession class.

        Raises:
            Exception: If an exception is raised during
            the execution of the `get_by_pac_id` method.

        Returns:
            None
        """

        invalid_id = "invalid_id"

        with pytest.raises(Exception):
            await error_log_manager.get_by_pac_id(
                invalid_id)  # type: ignore

        await session.rollback()
    # url,

