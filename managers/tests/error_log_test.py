# models/managers/tests/error_log_test.py
# pylint: disable=protected-access
# pylint: disable=unused-argument
"""
    This class contains unit tests for the
    `ErrorLogManager` class.
"""

from typing import List
import uuid

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from helpers.session_context import SessionContext
from managers.error_log import ErrorLogManager
from models import ErrorLog
from models.factory import ErrorLogFactory
from models.serialization_schema.error_log import ErrorLogSchema

class TestErrorLogManager:
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
    async def test_build_with_missing_data(
        self,
        error_log_manager: ErrorLogManager,
        session: AsyncSession
    ):
        """
        Test case for the `build` method of
        `ErrorLogManager` with missing data.
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
        Test case for the `add` method of
        `ErrorLogManager` that checks if a
        error_log is correctly added to the database.
        """
        test_error_log = await ErrorLogFactory.build_async(
            session)

        assert test_error_log.error_log_id == 0

        # Add the error_log using the
        # manager's add method
        added_error_log = await error_log_manager.add(
            error_log=test_error_log)

        assert isinstance(added_error_log, ErrorLog)

        assert str(added_error_log.insert_user_id) == (
            str(error_log_manager._session_context.customer_code))
        assert str(added_error_log.last_update_user_id) == (
            str(error_log_manager._session_context.customer_code))

        assert added_error_log.error_log_id > 0

        # Fetch the error_log from
        # the database directly
        result = await session.execute(
            select(ErrorLog).filter(
                ErrorLog._error_log_id == added_error_log.error_log_id  # type: ignore
            )
        )
        fetched_error_log = result.scalars().first()

        # Assert that the fetched error_log
        # is not None and matches the
        # added error_log
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
        Test case for the `add` method of
        `ErrorLogManager` that checks if the
        correct error_log object is returned.
        """
        # Create a test error_log
        # using the ErrorLogFactory
        # without persisting it to the database
        test_error_log = await ErrorLogFactory.build_async(
            session)

        assert test_error_log.error_log_id == 0

        test_error_log.code = uuid.uuid4()

        # Add the error_log using
        # the manager's add method
        added_error_log = await error_log_manager.add(
            error_log=test_error_log)

        assert isinstance(added_error_log, ErrorLog)

        assert str(added_error_log.insert_user_id) == (
            str(error_log_manager._session_context.customer_code))
        assert str(added_error_log.last_update_user_id) == (
            str(error_log_manager._session_context.customer_code))

        assert added_error_log.error_log_id > 0

        # Assert that the returned
        # error_log matches the
        # test error_log
        assert added_error_log.error_log_id == \
            test_error_log.error_log_id
        assert added_error_log.code == \
            test_error_log.code

    @pytest.mark.asyncio
    async def test_update(
        self,
        error_log_manager: ErrorLogManager,
        session: AsyncSession
    ):
        """
        Test case for the `update` method
        of `ErrorLogManager`
        that checks if a error_log
        is correctly updated.
        """
        test_error_log = await ErrorLogFactory.create_async(
            session)

        test_error_log.code = uuid.uuid4()

        updated_error_log = await error_log_manager.update(
            error_log=test_error_log)

        assert isinstance(updated_error_log, ErrorLog)

        assert str(updated_error_log.last_update_user_id) == str(
            error_log_manager._session_context.customer_code)

        assert updated_error_log.error_log_id == \
            test_error_log.error_log_id
        assert updated_error_log.code == \
            test_error_log.code

        result = await session.execute(
            select(ErrorLog).filter(
                ErrorLog._error_log_id == test_error_log.error_log_id)  # type: ignore
        )

        fetched_error_log = result.scalars().first()

        assert updated_error_log.error_log_id == \
            fetched_error_log.error_log_id
        assert updated_error_log.code == \
            fetched_error_log.code

        assert test_error_log.error_log_id == \
            fetched_error_log.error_log_id
        assert test_error_log.code == \
            fetched_error_log.code

    @pytest.mark.asyncio
    async def test_update_via_dict(
        self,
        error_log_manager: ErrorLogManager,
        session: AsyncSession
    ):
        """
        Test case for the `update` method
        of `ErrorLogManager`
        that checks if a error_log is
        correctly updated using a dictionary.
        """
        test_error_log = await ErrorLogFactory.create_async(
            session)

        new_code = uuid.uuid4()

        updated_error_log = await error_log_manager.update(
            error_log=test_error_log,
            code=new_code
        )

        assert isinstance(updated_error_log, ErrorLog)

        assert str(updated_error_log.last_update_user_id) == str(
            error_log_manager._session_context.customer_code
        )

        assert updated_error_log.error_log_id == \
            test_error_log.error_log_id
        assert updated_error_log.code == new_code

        result = await session.execute(
            select(ErrorLog).filter(
                ErrorLog._error_log_id == test_error_log.error_log_id)  # type: ignore
        )

        fetched_error_log = result.scalars().first()

        assert updated_error_log.error_log_id == \
            fetched_error_log.error_log_id
        assert updated_error_log.code == \
            fetched_error_log.code

        assert test_error_log.error_log_id == \
            fetched_error_log.error_log_id
        assert new_code == \
            fetched_error_log.code

    @pytest.mark.asyncio
    async def test_update_invalid_error_log(
        self,
        error_log_manager: ErrorLogManager
    ):
        """
        Test case for the `update` method of `ErrorLogManager`
        with an invalid error_log.
        """

        # None error_log
        error_log = None

        new_code = uuid.uuid4()

        updated_error_log = await (
            error_log_manager.update(
                error_log, code=new_code))  # type: ignore

        # Assertions
        assert updated_error_log is None

    @pytest.mark.asyncio
    async def test_update_with_nonexistent_attribute(
        self,
        error_log_manager: ErrorLogManager,
        session: AsyncSession
    ):
        """
        Test case for the `update` method of `ErrorLogManager`
        with a nonexistent attribute.
        """
        test_error_log = await ErrorLogFactory.create_async(
            session)

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
        Test case for the `delete` method of `ErrorLogManager`.
        """
        error_log_data = await ErrorLogFactory.create_async(
            session)

        result = await session.execute(
            select(ErrorLog).filter(
                ErrorLog._error_log_id == error_log_data.error_log_id)  # type: ignore
        )
        fetched_error_log = result.scalars().first()

        assert isinstance(fetched_error_log, ErrorLog)

        assert fetched_error_log.error_log_id == \
            error_log_data.error_log_id

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
        Test case to verify the behavior of deleting a nonexistent error_log.

        This test case ensures that when the delete method
        is called with the ID of a nonexistent error_log,
        an exception is raised. The test also verifies that
        the session is rolled back after the delete operation.

        :param error_log_manager: The instance of the ErrorLogManager class.
        :param session: The instance of the AsyncSession class.
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
        Test case to verify the behavior of deleting a error_log
        with an invalid type.

        This test case ensures that when the `delete` method
        of the `error_log_manager` is called with an invalid type,
        an exception is raised. The test case expects the
        `delete` method to raise an exception, and if it doesn't,
        the test case will fail.

        Args:
            error_log_manager (ErrorLogManager): An
                instance of the
                `ErrorLogManager` class.
            session (AsyncSession): An instance of the `AsyncSession` class.

        Returns:
            None

        Raises:
            Exception: If the `delete` method does not raise an exception.

        """
        with pytest.raises(Exception):
            await error_log_manager.delete("999")  # type: ignore

        await session.rollback()

    @pytest.mark.asyncio
    async def test_get_list(
        self,
        error_log_manager: ErrorLogManager,
        session: AsyncSession
    ):
        """
        Test case for the `get_list` method of the
        `ErrorLogManager` class.

        This test verifies that the `get_list`
        method returns the correct list of error_logs.

        Steps:
        1. Call the `get_list` method of the
            `error_log_manager` instance.
        2. Assert that the returned list is empty.
        3. Create 5 error_log objects using the
            `ErrorLogFactory.create_async` method.
        4. Assert that the `error_logs_data` variable is of type `List`.
        5. Call the `get_list` method of the
            `error_log_manager` instance again.
        6. Assert that the returned list contains 5 error_logs.
        7. Assert that all elements in the returned list are
            instances of the `ErrorLog` class.
        """

        error_logs = await error_log_manager.get_list()

        assert len(error_logs) == 0

        error_logs_data = (
            [await ErrorLogFactory.create_async(session) for _ in range(5)])

        assert isinstance(error_logs_data, List)

        error_logs = await error_log_manager.get_list()

        assert len(error_logs) == 5
        assert all(isinstance(
            error_log, ErrorLog) for error_log in error_logs)

    @pytest.mark.asyncio
    async def test_to_json(
        self,
        error_log_manager: ErrorLogManager,
        session: AsyncSession
    ):
        """
        Test the 'to_json' method of the ErrorLogManager class.

        Args:
            error_log_manager (ErrorLogManager): An
                instance of the
                ErrorLogManager class.
            session (AsyncSession): An instance of the AsyncSession class.

        Returns:
            None

        Raises:
            AssertionError: If the json_data is None.
        """
        error_log = await ErrorLogFactory.build_async(
            session)

        json_data = error_log_manager.to_json(
            error_log)

        assert json_data is not None

    @pytest.mark.asyncio
    async def test_to_dict(
        self,
        error_log_manager: ErrorLogManager,
        session: AsyncSession
    ):
        """
        Test the to_dict method of the ErrorLogManager class.

        Args:
            error_log_manager (ErrorLogManager): An
                instance of the
                ErrorLogManager class.
            session (AsyncSession): An instance of the AsyncSession class.

        Returns:
            None
        """
        error_log = await ErrorLogFactory.build_async(
            session)

        dict_data = error_log_manager.to_dict(
            error_log)

        assert dict_data is not None

    @pytest.mark.asyncio
    async def test_from_json(
        self,
        error_log_manager: ErrorLogManager,
        session: AsyncSession
    ):
        """
        Test the `from_json` method of the `ErrorLogManager` class.

        This method tests the functionality of the
        `from_json` method of the `ErrorLogManager` class.
        It creates a error_log using
        the `ErrorLogFactory`
        and converts it to JSON using the `to_json` method.
        Then, it deserializes the JSON data using the
        `from_json` method and asserts that the deserialized
        error_log is an instance of the
        `ErrorLog` class and has
        the same code as the original error_log.

        Args:
            error_log_manager (ErrorLogManager): An
            instance of the
                `ErrorLogManager` class.
            session (AsyncSession): An instance of the `AsyncSession` class.

        Returns:
            None
        """
        error_log = await ErrorLogFactory.create_async(
            session)

        json_data = error_log_manager.to_json(
            error_log)

        deserialized_error_log = error_log_manager.from_json(json_data)

        assert isinstance(deserialized_error_log, ErrorLog)
        assert deserialized_error_log.code == \
            error_log.code

    @pytest.mark.asyncio
    async def test_from_dict(
        self,
        error_log_manager: ErrorLogManager,
        session: AsyncSession
    ):
        """
        Test the `from_dict` method of the
        `ErrorLogManager` class.

        This method tests the functionality of the
        `from_dict` method, which is used to deserialize
        a dictionary representation of a
        error_log object.

        Args:
            error_log_manager (ErrorLogManager): An instance
                of the `ErrorLogManager` class.
            session (AsyncSession): An instance of the `AsyncSession` class.

        Returns:
            None

        Raises:
            AssertionError: If any of the assertions fail.
        """
        error_log = await ErrorLogFactory.create_async(
            session)

        schema = ErrorLogSchema()

        error_log_data = schema.dump(error_log)

        assert isinstance(error_log_data, dict)

        deserialized_error_log = error_log_manager.from_dict(
            error_log_data)

        assert isinstance(deserialized_error_log, ErrorLog)

        assert deserialized_error_log.code == \
            error_log.code

    @pytest.mark.asyncio
    async def test_count_basic_functionality(
        self,
        error_log_manager: ErrorLogManager,
        session: AsyncSession
    ):
        """
        Test the basic functionality of the count method
        in the ErrorLogManager class.

        This test case creates 5 error_log
        objects using the
        ErrorLogFactory and checks if the count method
        returns the correct count of
        error_logs.

        Steps:
        1. Create 5 error_log objects using
            the ErrorLogFactory.
        2. Call the count method of the error_log_manager.
        3. Assert that the count is equal to 5.

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
        Test the count method when the database is empty.

        This test case checks if the count method of the
        ErrorLogManager class returns 0 when the database is empty.

        Args:
            error_log_manager (ErrorLogManager): An
                instance of the
                ErrorLogManager class.

        Returns:
            None
        """

        count = await error_log_manager.count()

        assert count == 0

    @pytest.mark.asyncio
    async def test_refresh_basic(
        self,
        error_log_manager: ErrorLogManager,
        session: AsyncSession
    ):
        """
        Test the basic functionality of refreshing
        a error_log instance.

        This test performs the following steps:
        1. Creates a error_log instance using
            the ErrorLogFactory.
        2. Retrieves the error_log from th
            database to ensure
            it was added correctly.
        3. Updates the error_log's code and verifies the update.
        4. Refreshes the original error_log instance
            and checks if
            it reflects the updated code.

        Args:
            error_log_manager (ErrorLogManager): The
                manager responsible
                for error_log operations.
            session (AsyncSession): The SQLAlchemy asynchronous session.
        """
        # Add a error_log
        error_log1 = await ErrorLogFactory.create_async(
            session=session)

        # Retrieve the error_log from the database
        result = await session.execute(
            select(ErrorLog).filter(
                ErrorLog._error_log_id == error_log1.error_log_id)  # type: ignore
        )  # type: ignore
        error_log2 = result.scalars().first()

        # Verify that the retrieved error_log
        # matches the added error_log
        assert error_log1.code == \
            error_log2.code

        # Update the error_log's code
        updated_code1 = uuid.uuid4()
        error_log1.code = updated_code1
        updated_error_log1 = await error_log_manager.update(
            error_log1)

        # Verify that the updated error_log
        # is of type ErrorLog
        # and has the updated code
        assert isinstance(updated_error_log1, ErrorLog)

        assert updated_error_log1.code == updated_code1

        # Refresh the original error_log instance
        refreshed_error_log2 = await error_log_manager.refresh(
            error_log2)

        # Verify that the refreshed error_log
        # reflects the updated code
        assert refreshed_error_log2.code == updated_code1

    @pytest.mark.asyncio
    async def test_refresh_nonexistent_error_log(
        self,
        error_log_manager: ErrorLogManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of refreshing a nonexistent error_log.

        Args:
            error_log_manager (ErrorLogManager): The
                instance of the
                ErrorLogManager class.
            session (AsyncSession): The instance of the AsyncSession class.

        Raises:
            Exception: If the error_log
            refresh operation raises an exception.

        Returns:
            None
        """
        error_log = ErrorLog(
            error_log_id=999)

        with pytest.raises(Exception):
            await error_log_manager.refresh(
                error_log)

        await session.rollback()

    @pytest.mark.asyncio
    async def test_exists_with_existing_error_log(
        self,
        error_log_manager: ErrorLogManager,
        session: AsyncSession
    ):
        """
        Test case to check if a error_log
        exists using the manager function.

        Args:
            error_log_manager (ErrorLogManager): The
                error_log manager instance.
            session (AsyncSession): The async session object.

        Returns:
            None
        """
        # Add a error_log
        error_log1 = await ErrorLogFactory.create_async(
            session=session)

        # Check if the error_log exists
        # using the manager function
        assert await error_log_manager.exists(
            error_log1.error_log_id) is True

    @pytest.mark.asyncio
    async def test_is_equal_with_existing_error_log(
        self,
        error_log_manager: ErrorLogManager,
        session: AsyncSession
    ):
        """
        Test if the is_equal method of the
        ErrorLogManager class correctly compares two error_logs.

        Args:
            error_log_manager (ErrorLogManager): An
                instance of the
                ErrorLogManager class.
            session (AsyncSession): An instance of the AsyncSession class.

        Returns:
            None
        """
        # Add a error_log
        error_log1 = await ErrorLogFactory.create_async(
            session=session)

        error_log2 = await error_log_manager.get_by_id(
            error_log_id=error_log1.error_log_id)

        assert error_log_manager.is_equal(
            error_log1, error_log2) is True

        error_log1_dict = error_log_manager.to_dict(
            error_log1)

        error_log3 = error_log_manager.from_dict(
            error_log1_dict)

        assert error_log_manager.is_equal(
            error_log1, error_log3) is True

    @pytest.mark.asyncio
    async def test_exists_with_nonexistent_error_log(
        self,
        error_log_manager: ErrorLogManager
    ):
        """
        Test case to check if a error_log with a
        non-existent ID exists in the database.

        Args:
            error_log_manager (ErrorLogManager): The
                instance of the ErrorLogManager class.

        Returns:
            bool: True if the error_log exists,
                False otherwise.
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
        Test case to check if the exists method raises
        an exception when an invalid ID type is provided.

        Args:
            error_log_manager (ErrorLogManager): The instance
                of the ErrorLogManager class.
            session (AsyncSession): The instance of the AsyncSession class.

        Raises:
            Exception: If an exception is not raised by the exists method.

        Returns:
            None
        """
        invalid_id = "invalid_id"

        with pytest.raises(Exception):
            await error_log_manager.exists(invalid_id)  # type: ignore  # noqa: E501

        await session.rollback()
# endset
