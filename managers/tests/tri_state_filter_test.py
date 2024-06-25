# models/managers/tests/tri_state_filter_test.py
# pylint: disable=protected-access
# pylint: disable=unused-argument
"""
    This class contains unit tests for the
    `TriStateFilterManager` class.
"""

from typing import List
import uuid

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from helpers.session_context import SessionContext
from managers.tri_state_filter import TriStateFilterManager
from models import TriStateFilter
from models.factory import TriStateFilterFactory
from models.serialization_schema.tri_state_filter import TriStateFilterSchema


class TestTriStateFilterManager:
    """
    This class contains unit tests for the
    `TriStateFilterManager` class.
    """

    @pytest_asyncio.fixture(scope="function")
    async def tri_state_filter_manager(self, session: AsyncSession):
        """
        Fixture that returns an instance of
        `TriStateFilterManager` for testing.
        """
        session_context = SessionContext(dict(), session)
        session_context.customer_code = uuid.uuid4()
        return TriStateFilterManager(session_context)

    @pytest.mark.asyncio
    async def test_build(
        self,
        tri_state_filter_manager: TriStateFilterManager
    ):
        """
        Test case for the `build` method of
        `TriStateFilterManager`.
        """
        # Define mock data for our tri_state_filter
        mock_data = {
            "code": uuid.uuid4()
        }

        # Call the build function of the manager
        tri_state_filter = await tri_state_filter_manager.build(
            **mock_data)

        # Assert that the returned object is an instance of TriStateFilter
        assert isinstance(
            tri_state_filter, TriStateFilter)

        # Assert that the attributes of the
        # tri_state_filter match our mock data
        assert tri_state_filter.code == mock_data["code"]

    @pytest.mark.asyncio
    async def test_build_with_missing_data(
        self,
        tri_state_filter_manager: TriStateFilterManager,
        session: AsyncSession
    ):
        """
        Test case for the `build` method of
        `TriStateFilterManager` with missing data.
        """
        # Define mock data with a missing key
        mock_data = {
            "non_existant_property": "Rose"
        }

        # If the build method is expected to raise an exception for
        # missing data, test for that
        with pytest.raises(Exception):
            await tri_state_filter_manager.build(**mock_data)

        await session.rollback()

    @pytest.mark.asyncio
    async def test_add_correctly_adds_tri_state_filter_to_database(
        self,
        tri_state_filter_manager: TriStateFilterManager,
        session: AsyncSession
    ):
        """
        Test case for the `add` method of
        `TriStateFilterManager` that checks if a
        tri_state_filter is correctly added to the database.
        """
        test_tri_state_filter = await TriStateFilterFactory.build_async(
            session)

        assert test_tri_state_filter.tri_state_filter_id == 0

        # Add the tri_state_filter using the
        # manager's add method
        added_tri_state_filter = await tri_state_filter_manager.add(
            tri_state_filter=test_tri_state_filter)

        assert isinstance(added_tri_state_filter, TriStateFilter)

        assert str(added_tri_state_filter.insert_user_id) == (
            str(tri_state_filter_manager._session_context.customer_code))
        assert str(added_tri_state_filter.last_update_user_id) == (
            str(tri_state_filter_manager._session_context.customer_code))

        assert added_tri_state_filter.tri_state_filter_id > 0

        # Fetch the tri_state_filter from
        # the database directly
        result = await session.execute(
            select(TriStateFilter).filter(
                TriStateFilter._tri_state_filter_id == added_tri_state_filter.tri_state_filter_id  # type: ignore
            )
        )
        fetched_tri_state_filter = result.scalars().first()

        # Assert that the fetched tri_state_filter
        # is not None and matches the
        # added tri_state_filter
        assert fetched_tri_state_filter is not None
        assert isinstance(fetched_tri_state_filter, TriStateFilter)
        assert fetched_tri_state_filter.tri_state_filter_id == added_tri_state_filter.tri_state_filter_id

    @pytest.mark.asyncio
    async def test_add_returns_correct_tri_state_filter_object(
        self,
        tri_state_filter_manager: TriStateFilterManager,
        session: AsyncSession
    ):
        """
        Test case for the `add` method of
        `TriStateFilterManager` that checks if the
        correct tri_state_filter object is returned.
        """
        # Create a test tri_state_filter
        # using the TriStateFilterFactory
        # without persisting it to the database
        test_tri_state_filter = await TriStateFilterFactory.build_async(
            session)

        assert test_tri_state_filter.tri_state_filter_id == 0

        test_tri_state_filter.code = uuid.uuid4()

        # Add the tri_state_filter using
        # the manager's add method
        added_tri_state_filter = await tri_state_filter_manager.add(
            tri_state_filter=test_tri_state_filter)

        assert isinstance(added_tri_state_filter, TriStateFilter)

        assert str(added_tri_state_filter.insert_user_id) == (
            str(tri_state_filter_manager._session_context.customer_code))
        assert str(added_tri_state_filter.last_update_user_id) == (
            str(tri_state_filter_manager._session_context.customer_code))

        assert added_tri_state_filter.tri_state_filter_id > 0

        # Assert that the returned
        # tri_state_filter matches the
        # test tri_state_filter
        assert added_tri_state_filter.tri_state_filter_id == \
            test_tri_state_filter.tri_state_filter_id
        assert added_tri_state_filter.code == \
            test_tri_state_filter.code

    @pytest.mark.asyncio
    async def test_update(
        self,
        tri_state_filter_manager: TriStateFilterManager,
        session: AsyncSession
    ):
        """
        Test case for the `update` method
        of `TriStateFilterManager`
        that checks if a tri_state_filter
        is correctly updated.
        """
        test_tri_state_filter = await TriStateFilterFactory.create_async(
            session)

        test_tri_state_filter.code = uuid.uuid4()

        updated_tri_state_filter = await tri_state_filter_manager.update(
            tri_state_filter=test_tri_state_filter)

        assert isinstance(updated_tri_state_filter, TriStateFilter)

        assert str(updated_tri_state_filter.last_update_user_id) == str(
            tri_state_filter_manager._session_context.customer_code)

        assert updated_tri_state_filter.tri_state_filter_id == \
            test_tri_state_filter.tri_state_filter_id
        assert updated_tri_state_filter.code == \
            test_tri_state_filter.code

        result = await session.execute(
            select(TriStateFilter).filter(
                TriStateFilter._tri_state_filter_id == test_tri_state_filter.tri_state_filter_id)  # type: ignore
        )

        fetched_tri_state_filter = result.scalars().first()

        assert updated_tri_state_filter.tri_state_filter_id == \
            fetched_tri_state_filter.tri_state_filter_id
        assert updated_tri_state_filter.code == \
            fetched_tri_state_filter.code

        assert test_tri_state_filter.tri_state_filter_id == \
            fetched_tri_state_filter.tri_state_filter_id
        assert test_tri_state_filter.code == \
            fetched_tri_state_filter.code

    @pytest.mark.asyncio
    async def test_update_via_dict(
        self,
        tri_state_filter_manager: TriStateFilterManager,
        session: AsyncSession
    ):
        """
        Test case for the `update` method
        of `TriStateFilterManager`
        that checks if a tri_state_filter is
        correctly updated using a dictionary.
        """
        test_tri_state_filter = await TriStateFilterFactory.create_async(
            session)

        new_code = uuid.uuid4()

        updated_tri_state_filter = await tri_state_filter_manager.update(
            tri_state_filter=test_tri_state_filter,
            code=new_code
        )

        assert isinstance(updated_tri_state_filter, TriStateFilter)

        assert str(updated_tri_state_filter.last_update_user_id) == str(
            tri_state_filter_manager._session_context.customer_code
        )

        assert updated_tri_state_filter.tri_state_filter_id == \
            test_tri_state_filter.tri_state_filter_id
        assert updated_tri_state_filter.code == new_code

        result = await session.execute(
            select(TriStateFilter).filter(
                TriStateFilter._tri_state_filter_id == test_tri_state_filter.tri_state_filter_id)  # type: ignore
        )

        fetched_tri_state_filter = result.scalars().first()

        assert updated_tri_state_filter.tri_state_filter_id == \
            fetched_tri_state_filter.tri_state_filter_id
        assert updated_tri_state_filter.code == \
            fetched_tri_state_filter.code

        assert test_tri_state_filter.tri_state_filter_id == \
            fetched_tri_state_filter.tri_state_filter_id
        assert new_code == \
            fetched_tri_state_filter.code

    @pytest.mark.asyncio
    async def test_update_invalid_tri_state_filter(
        self,
        tri_state_filter_manager: TriStateFilterManager
    ):
        """
        Test case for the `update` method of `TriStateFilterManager`
        with an invalid tri_state_filter.
        """

        # None tri_state_filter
        tri_state_filter = None

        new_code = uuid.uuid4()

        updated_tri_state_filter = await (
            tri_state_filter_manager.update(
                tri_state_filter, code=new_code))  # type: ignore

        # Assertions
        assert updated_tri_state_filter is None

    @pytest.mark.asyncio
    async def test_update_with_nonexistent_attribute(
        self,
        tri_state_filter_manager: TriStateFilterManager,
        session: AsyncSession
    ):
        """
        Test case for the `update` method of `TriStateFilterManager`
        with a nonexistent attribute.
        """
        test_tri_state_filter = await TriStateFilterFactory.create_async(
            session)

        new_code = uuid.uuid4()

        with pytest.raises(ValueError):
            await tri_state_filter_manager.update(
                tri_state_filter=test_tri_state_filter,
                xxx=new_code
            )

        await session.rollback()

    @pytest.mark.asyncio
    async def test_delete(
        self,
        tri_state_filter_manager: TriStateFilterManager,
        session: AsyncSession
    ):
        """
        Test case for the `delete` method of `TriStateFilterManager`.
        """
        tri_state_filter_data = await TriStateFilterFactory.create_async(
            session)

        result = await session.execute(
            select(TriStateFilter).filter(
                TriStateFilter._tri_state_filter_id == tri_state_filter_data.tri_state_filter_id)  # type: ignore
        )
        fetched_tri_state_filter = result.scalars().first()

        assert isinstance(fetched_tri_state_filter, TriStateFilter)

        assert fetched_tri_state_filter.tri_state_filter_id == \
            tri_state_filter_data.tri_state_filter_id

        await tri_state_filter_manager.delete(
            tri_state_filter_id=tri_state_filter_data.tri_state_filter_id)

        result = await session.execute(
            select(TriStateFilter).filter(
                TriStateFilter._tri_state_filter_id == tri_state_filter_data.tri_state_filter_id)  # type: ignore
        )
        fetched_tri_state_filter = result.scalars().first()

        assert fetched_tri_state_filter is None

    @pytest.mark.asyncio
    async def test_delete_nonexistent(
        self,
        tri_state_filter_manager: TriStateFilterManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of deleting a nonexistent tri_state_filter.

        This test case ensures that when the delete method
        is called with the ID of a nonexistent tri_state_filter,
        an exception is raised. The test also verifies that
        the session is rolled back after the delete operation.

        :param tri_state_filter_manager: The instance of the TriStateFilterManager class.
        :param session: The instance of the AsyncSession class.
        """
        with pytest.raises(Exception):
            await tri_state_filter_manager.delete(999)

        await session.rollback()

    @pytest.mark.asyncio
    async def test_delete_invalid_type(
        self,
        tri_state_filter_manager: TriStateFilterManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of deleting a tri_state_filter
        with an invalid type.

        This test case ensures that when the `delete` method
        of the `tri_state_filter_manager` is called with an invalid type,
        an exception is raised. The test case expects the
        `delete` method to raise an exception, and if it doesn't,
        the test case will fail.

        Args:
            tri_state_filter_manager (TriStateFilterManager): An
                instance of the
                `TriStateFilterManager` class.
            session (AsyncSession): An instance of the `AsyncSession` class.

        Returns:
            None

        Raises:
            Exception: If the `delete` method does not raise an exception.

        """
        with pytest.raises(Exception):
            await tri_state_filter_manager.delete("999")  # type: ignore

        await session.rollback()

    @pytest.mark.asyncio
    async def test_get_list(
        self,
        tri_state_filter_manager: TriStateFilterManager,
        session: AsyncSession
    ):
        """
        Test case for the `get_list` method of the
        `TriStateFilterManager` class.

        This test verifies that the `get_list`
        method returns the correct list of tri_state_filters.

        Steps:
        1. Call the `get_list` method of the
            `tri_state_filter_manager` instance.
        2. Assert that the returned list is empty.
        3. Create 5 tri_state_filter objects using the
            `TriStateFilterFactory.create_async` method.
        4. Assert that the `tri_state_filters_data` variable is of type `List`.
        5. Call the `get_list` method of the
            `tri_state_filter_manager` instance again.
        6. Assert that the returned list contains 5 tri_state_filters.
        7. Assert that all elements in the returned list are
            instances of the `TriStateFilter` class.
        """

        tri_state_filters = await tri_state_filter_manager.get_list()

        assert len(tri_state_filters) == 0

        tri_state_filters_data = (
            [await TriStateFilterFactory.create_async(session) for _ in range(5)])

        assert isinstance(tri_state_filters_data, List)

        tri_state_filters = await tri_state_filter_manager.get_list()

        assert len(tri_state_filters) == 5
        assert all(isinstance(
            tri_state_filter, TriStateFilter) for tri_state_filter in tri_state_filters)

    @pytest.mark.asyncio
    async def test_to_json(
        self,
        tri_state_filter_manager: TriStateFilterManager,
        session: AsyncSession
    ):
        """
        Test the 'to_json' method of the TriStateFilterManager class.

        Args:
            tri_state_filter_manager (TriStateFilterManager): An
                instance of the
                TriStateFilterManager class.
            session (AsyncSession): An instance of the AsyncSession class.

        Returns:
            None

        Raises:
            AssertionError: If the json_data is None.
        """
        tri_state_filter = await TriStateFilterFactory.build_async(
            session)

        json_data = tri_state_filter_manager.to_json(
            tri_state_filter)

        assert json_data is not None

    @pytest.mark.asyncio
    async def test_to_dict(
        self,
        tri_state_filter_manager: TriStateFilterManager,
        session: AsyncSession
    ):
        """
        Test the to_dict method of the TriStateFilterManager class.

        Args:
            tri_state_filter_manager (TriStateFilterManager): An
                instance of the
                TriStateFilterManager class.
            session (AsyncSession): An instance of the AsyncSession class.

        Returns:
            None
        """
        tri_state_filter = await TriStateFilterFactory.build_async(
            session)

        dict_data = tri_state_filter_manager.to_dict(
            tri_state_filter)

        assert dict_data is not None

    @pytest.mark.asyncio
    async def test_from_json(
        self,
        tri_state_filter_manager: TriStateFilterManager,
        session: AsyncSession
    ):
        """
        Test the `from_json` method of the `TriStateFilterManager` class.

        This method tests the functionality of the
        `from_json` method of the `TriStateFilterManager` class.
        It creates a tri_state_filter using
        the `TriStateFilterFactory`
        and converts it to JSON using the `to_json` method.
        Then, it deserializes the JSON data using the
        `from_json` method and asserts that the deserialized
        tri_state_filter is an instance of the
        `TriStateFilter` class and has
        the same code as the original tri_state_filter.

        Args:
            tri_state_filter_manager (TriStateFilterManager): An
            instance of the
                `TriStateFilterManager` class.
            session (AsyncSession): An instance of the `AsyncSession` class.

        Returns:
            None
        """
        tri_state_filter = await TriStateFilterFactory.create_async(
            session)

        json_data = tri_state_filter_manager.to_json(
            tri_state_filter)

        deserialized_tri_state_filter = await tri_state_filter_manager.from_json(json_data)

        assert isinstance(deserialized_tri_state_filter, TriStateFilter)
        assert deserialized_tri_state_filter.code == \
            tri_state_filter.code

    @pytest.mark.asyncio
    async def test_from_dict(
        self,
        tri_state_filter_manager: TriStateFilterManager,
        session: AsyncSession
    ):
        """
        Test the `from_dict` method of the
        `TriStateFilterManager` class.

        This method tests the functionality of the
        `from_dict` method, which is used to deserialize
        a dictionary representation of a
        tri_state_filter object.

        Args:
            tri_state_filter_manager (TriStateFilterManager): An instance
                of the `TriStateFilterManager` class.
            session (AsyncSession): An instance of the `AsyncSession` class.

        Returns:
            None

        Raises:
            AssertionError: If any of the assertions fail.
        """
        tri_state_filter = await TriStateFilterFactory.create_async(
            session)

        schema = TriStateFilterSchema()

        tri_state_filter_data = schema.dump(tri_state_filter)

        assert isinstance(tri_state_filter_data, dict)

        deserialized_tri_state_filter = await tri_state_filter_manager.from_dict(
            tri_state_filter_data)

        assert isinstance(deserialized_tri_state_filter, TriStateFilter)

        assert deserialized_tri_state_filter.code == \
            tri_state_filter.code

    @pytest.mark.asyncio
    async def test_count_basic_functionality(
        self,
        tri_state_filter_manager: TriStateFilterManager,
        session: AsyncSession
    ):
        """
        Test the basic functionality of the count method
        in the TriStateFilterManager class.

        This test case creates 5 tri_state_filter
        objects using the
        TriStateFilterFactory and checks if the count method
        returns the correct count of
        tri_state_filters.

        Steps:
        1. Create 5 tri_state_filter objects using
            the TriStateFilterFactory.
        2. Call the count method of the tri_state_filter_manager.
        3. Assert that the count is equal to 5.

        """
        tri_state_filters_data = (
            [await TriStateFilterFactory.create_async(session) for _ in range(5)])

        assert isinstance(tri_state_filters_data, List)

        count = await tri_state_filter_manager.count()

        assert count == 5

    @pytest.mark.asyncio
    async def test_count_empty_database(
        self,
        tri_state_filter_manager: TriStateFilterManager
    ):
        """
        Test the count method when the database is empty.

        This test case checks if the count method of the
        TriStateFilterManager class returns 0 when the database is empty.

        Args:
            tri_state_filter_manager (TriStateFilterManager): An
                instance of the
                TriStateFilterManager class.

        Returns:
            None
        """

        count = await tri_state_filter_manager.count()

        assert count == 0

    @pytest.mark.asyncio
    async def test_refresh_basic(
        self,
        tri_state_filter_manager: TriStateFilterManager,
        session: AsyncSession
    ):
        """
        Test the basic functionality of refreshing
        a tri_state_filter instance.

        This test performs the following steps:
        1. Creates a tri_state_filter instance using
            the TriStateFilterFactory.
        2. Retrieves the tri_state_filter from th
            database to ensure
            it was added correctly.
        3. Updates the tri_state_filter's code and verifies the update.
        4. Refreshes the original tri_state_filter instance
            and checks if
            it reflects the updated code.

        Args:
            tri_state_filter_manager (TriStateFilterManager): The
                manager responsible
                for tri_state_filter operations.
            session (AsyncSession): The SQLAlchemy asynchronous session.
        """
        # Add a tri_state_filter
        tri_state_filter1 = await TriStateFilterFactory.create_async(
            session=session)

        # Retrieve the tri_state_filter from the database
        result = await session.execute(
            select(TriStateFilter).filter(
                TriStateFilter._tri_state_filter_id == tri_state_filter1.tri_state_filter_id)  # type: ignore
        )  # type: ignore
        tri_state_filter2 = result.scalars().first()

        # Verify that the retrieved tri_state_filter
        # matches the added tri_state_filter
        assert tri_state_filter1.code == \
            tri_state_filter2.code

        # Update the tri_state_filter's code
        updated_code1 = uuid.uuid4()
        tri_state_filter1.code = updated_code1
        updated_tri_state_filter1 = await tri_state_filter_manager.update(
            tri_state_filter1)

        # Verify that the updated tri_state_filter
        # is of type TriStateFilter
        # and has the updated code
        assert isinstance(updated_tri_state_filter1, TriStateFilter)

        assert updated_tri_state_filter1.code == updated_code1

        # Refresh the original tri_state_filter instance
        refreshed_tri_state_filter2 = await tri_state_filter_manager.refresh(
            tri_state_filter2)

        # Verify that the refreshed tri_state_filter
        # reflects the updated code
        assert refreshed_tri_state_filter2.code == updated_code1

    @pytest.mark.asyncio
    async def test_refresh_nonexistent_tri_state_filter(
        self,
        tri_state_filter_manager: TriStateFilterManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of refreshing a nonexistent tri_state_filter.

        Args:
            tri_state_filter_manager (TriStateFilterManager): The
                instance of the
                TriStateFilterManager class.
            session (AsyncSession): The instance of the AsyncSession class.

        Raises:
            Exception: If the tri_state_filter
            refresh operation raises an exception.

        Returns:
            None
        """
        tri_state_filter = TriStateFilter(
            tri_state_filter_id=999)

        with pytest.raises(Exception):
            await tri_state_filter_manager.refresh(
                tri_state_filter)

        await session.rollback()

    @pytest.mark.asyncio
    async def test_exists_with_existing_tri_state_filter(
        self,
        tri_state_filter_manager: TriStateFilterManager,
        session: AsyncSession
    ):
        """
        Test case to check if a tri_state_filter
        exists using the manager function.

        Args:
            tri_state_filter_manager (TriStateFilterManager): The
                tri_state_filter manager instance.
            session (AsyncSession): The async session object.

        Returns:
            None
        """
        # Add a tri_state_filter
        tri_state_filter1 = await TriStateFilterFactory.create_async(
            session=session)

        # Check if the tri_state_filter exists
        # using the manager function
        assert await tri_state_filter_manager.exists(
            tri_state_filter1.tri_state_filter_id) is True

    @pytest.mark.asyncio
    async def test_is_equal_with_existing_tri_state_filter(
        self,
        tri_state_filter_manager: TriStateFilterManager,
        session: AsyncSession
    ):
        """
        Test if the is_equal method of the
        TriStateFilterManager class correctly compares two tri_state_filters.

        Args:
            tri_state_filter_manager (TriStateFilterManager): An
                instance of the
                TriStateFilterManager class.
            session (AsyncSession): An instance of the AsyncSession class.

        Returns:
            None
        """
        # Add a tri_state_filter
        tri_state_filter1 = await \
            TriStateFilterFactory.create_async(
                session=session)

        tri_state_filter2 = await \
            tri_state_filter_manager.get_by_id(
                tri_state_filter_id=tri_state_filter1.tri_state_filter_id)

        assert tri_state_filter_manager.is_equal(
            tri_state_filter1, tri_state_filter2) is True

        tri_state_filter1_dict = tri_state_filter_manager.to_dict(
            tri_state_filter1)

        tri_state_filter3 = await \
            tri_state_filter_manager.from_dict(
                tri_state_filter1_dict)

        assert tri_state_filter_manager.is_equal(
            tri_state_filter1, tri_state_filter3) is True

    @pytest.mark.asyncio
    async def test_exists_with_nonexistent_tri_state_filter(
        self,
        tri_state_filter_manager: TriStateFilterManager
    ):
        """
        Test case to check if a tri_state_filter with a
        non-existent ID exists in the database.

        Args:
            tri_state_filter_manager (TriStateFilterManager): The
                instance of the TriStateFilterManager class.

        Returns:
            bool: True if the tri_state_filter exists,
                False otherwise.
        """
        non_existent_id = 999

        assert await tri_state_filter_manager.exists(non_existent_id) is False

    @pytest.mark.asyncio
    async def test_exists_with_invalid_id_type(
        self,
        tri_state_filter_manager: TriStateFilterManager,
        session: AsyncSession
    ):
        """
        Test case to check if the exists method raises
        an exception when an invalid ID type is provided.

        Args:
            tri_state_filter_manager (TriStateFilterManager): The instance
                of the TriStateFilterManager class.
            session (AsyncSession): The instance of the AsyncSession class.

        Raises:
            Exception: If an exception is not raised by the exists method.

        Returns:
            None
        """
        invalid_id = "invalid_id"

        with pytest.raises(Exception):
            await tri_state_filter_manager.exists(invalid_id)  # type: ignore  # noqa: E501

        await session.rollback()

