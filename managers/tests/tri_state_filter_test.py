# managers/tests/tri_state_filter_test.py
# pylint: disable=protected-access
# pylint: disable=unused-argument
# pylint: disable=unused-import
"""
    This class contains unit tests for the
    `TriStateFilterManager` class.
"""

from typing import List
import uuid  # noqa: F401

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from helpers.session_context import SessionContext
from managers.tri_state_filter import (
    TriStateFilterManager)
from models import TriStateFilter
from models.factory import (
    TriStateFilterFactory)
from models.serialization_schema.tri_state_filter import (
    TriStateFilterSchema)


class TestTriStateFilterManager:
    """
    This class contains unit tests for the
    `TriStateFilterManager` class.
    """

    @pytest_asyncio.fixture(scope="function")
    async def obj_manager(self, session: AsyncSession):
        """
        Fixture that returns an instance of
        `TriStateFilterManager` for testing.
        """
        session_context = SessionContext({}, session)
        session_context.customer_code = uuid.uuid4()
        return TriStateFilterManager(session_context)

    @pytest.mark.asyncio
    async def test_build(
        self,
        obj_manager: TriStateFilterManager
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
        tri_state_filter = await \
            obj_manager.build(
                **mock_data)

        # Assert that the returned object is an
        # instance of TriStateFilter
        assert isinstance(
            tri_state_filter,
            TriStateFilter)

        # Assert that the attributes of the
        # tri_state_filter match our mock data
        assert tri_state_filter.code == mock_data["code"]

    @pytest.mark.asyncio
    async def test_build_with_missing_data(
        self,
        obj_manager: TriStateFilterManager,
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
            await obj_manager.build(**mock_data)

        await session.rollback()

    @pytest.mark.asyncio
    async def test_add_correctly_adds_tri_state_filter_to_database(
        self,
        obj_manager: TriStateFilterManager,
        session: AsyncSession
    ):
        """
        Test case for the `add` method of
        `TriStateFilterManager` that checks if a
        tri_state_filter is correctly added to the database.
        """
        new_obj = await \
            TriStateFilterFactory.build_async(
                session)

        assert new_obj.tri_state_filter_id == 0

        # Add the tri_state_filter using the
        # manager's add method
        added_obj = await \
            obj_manager.add(
                tri_state_filter=new_obj)

        assert isinstance(added_obj,
                          TriStateFilter)

        assert str(added_obj.insert_user_id) == (
            str(obj_manager._session_context.customer_code))
        assert str(added_obj.last_update_user_id) == (
            str(obj_manager._session_context.customer_code))

        assert added_obj.tri_state_filter_id > 0

        # Fetch the tri_state_filter from
        # the database directly
        result = await session.execute(
            select(TriStateFilter).filter(
                TriStateFilter._tri_state_filter_id == (
                    added_obj.tri_state_filter_id)  # type: ignore
            )
        )
        fetched_obj = result.scalars().first()

        # Assert that the fetched tri_state_filter
        # is not None and matches the
        # added tri_state_filter
        assert fetched_obj is not None
        assert isinstance(fetched_obj,
                          TriStateFilter)
        assert fetched_obj.tri_state_filter_id == \
            added_obj.tri_state_filter_id

    @pytest.mark.asyncio
    async def test_add_returns_correct_tri_state_filter_object(
        self,
        obj_manager: TriStateFilterManager,
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
        new_obj = await \
            TriStateFilterFactory.build_async(
                session)

        assert new_obj.tri_state_filter_id == 0

        new_obj.code = uuid.uuid4()

        # Add the tri_state_filter using
        # the manager's add method
        added_obj = await \
            obj_manager.add(
                tri_state_filter=new_obj)

        assert isinstance(added_obj,
                          TriStateFilter)

        assert str(added_obj.insert_user_id) == (
            str(obj_manager._session_context.customer_code))
        assert str(added_obj.last_update_user_id) == (
            str(obj_manager._session_context.customer_code))

        assert added_obj.tri_state_filter_id > 0

        # Assert that the returned
        # tri_state_filter matches the
        # test tri_state_filter
        assert added_obj.tri_state_filter_id == \
            new_obj.tri_state_filter_id
        assert added_obj.code == \
            new_obj.code

    @pytest.mark.asyncio
    async def test_update(
        self,
        obj_manager: TriStateFilterManager,
        session: AsyncSession
    ):
        """
        Test case for the `update` method
        of `TriStateFilterManager`
        that checks if a tri_state_filter
        is correctly updated.
        """
        new_obj = await \
            TriStateFilterFactory.create_async(
                session)

        new_obj.code = uuid.uuid4()

        updated_obj = await \
            obj_manager.update(
                tri_state_filter=new_obj)

        assert isinstance(updated_obj,
                          TriStateFilter)

        assert str(updated_obj.last_update_user_id) == str(
            obj_manager._session_context.customer_code)

        assert updated_obj.tri_state_filter_id == \
            new_obj.tri_state_filter_id
        assert updated_obj.code == \
            new_obj.code

        result = await session.execute(
            select(TriStateFilter).filter(
                TriStateFilter._tri_state_filter_id == (
                    new_obj.tri_state_filter_id))  # type: ignore
        )

        fetched_obj = result.scalars().first()

        assert updated_obj.tri_state_filter_id == \
            fetched_obj.tri_state_filter_id
        assert updated_obj.code == \
            fetched_obj.code

        assert new_obj.tri_state_filter_id == \
            fetched_obj.tri_state_filter_id
        assert new_obj.code == \
            fetched_obj.code

    @pytest.mark.asyncio
    async def test_update_via_dict(
        self,
        obj_manager: TriStateFilterManager,
        session: AsyncSession
    ):
        """
        Test case for the `update` method
        of `TriStateFilterManager`
        that checks if a tri_state_filter is
        correctly updated using a dictionary.
        """
        new_obj = await \
            TriStateFilterFactory.create_async(
                session)

        new_code = uuid.uuid4()

        updated_obj = await \
            obj_manager.update(
                tri_state_filter=new_obj,
                code=new_code
            )

        assert isinstance(updated_obj,
                          TriStateFilter)

        assert str(updated_obj.last_update_user_id) == str(
            obj_manager._session_context.customer_code
        )

        assert updated_obj.tri_state_filter_id == \
            new_obj.tri_state_filter_id
        assert updated_obj.code == new_code

        result = await session.execute(
            select(TriStateFilter).filter(
                TriStateFilter._tri_state_filter_id == (
                    new_obj.tri_state_filter_id))  # type: ignore
        )

        fetched_obj = result.scalars().first()

        assert updated_obj.tri_state_filter_id == \
            fetched_obj.tri_state_filter_id
        assert updated_obj.code == \
            fetched_obj.code

        assert new_obj.tri_state_filter_id == \
            fetched_obj.tri_state_filter_id
        assert new_code == \
            fetched_obj.code

    @pytest.mark.asyncio
    async def test_update_invalid_tri_state_filter(
        self,
        obj_manager: TriStateFilterManager
    ):
        """
        Test case for the `update` method of
        `TriStateFilterManager`
        with an invalid tri_state_filter.
        """

        # None tri_state_filter
        tri_state_filter = None

        new_code = uuid.uuid4()

        updated_obj = await (
            obj_manager.update(
                tri_state_filter, code=new_code))  # type: ignore

        # Assertions
        assert updated_obj is None

    @pytest.mark.asyncio
    async def test_update_with_nonexistent_attribute(
        self,
        obj_manager: TriStateFilterManager,
        session: AsyncSession
    ):
        """
        Test case for the `update` method of
        `TriStateFilterManager`
        with a nonexistent attribute.
        """
        new_obj = await \
            TriStateFilterFactory.create_async(
                session)

        new_code = uuid.uuid4()

        with pytest.raises(ValueError):
            await obj_manager.update(
                tri_state_filter=new_obj,
                xxx=new_code
            )

        await session.rollback()

    @pytest.mark.asyncio
    async def test_delete(
        self,
        obj_manager: TriStateFilterManager,
        session: AsyncSession
    ):
        """
        Test case for the `delete` method of
        `TriStateFilterManager`.
        """
        new_obj = await TriStateFilterFactory.create_async(
            session)

        result = await session.execute(
            select(TriStateFilter).filter(
                TriStateFilter._tri_state_filter_id == (
                    new_obj.tri_state_filter_id))  # type: ignore
        )
        fetched_obj = result.scalars().first()

        assert isinstance(fetched_obj,
                          TriStateFilter)

        assert fetched_obj.tri_state_filter_id == \
            new_obj.tri_state_filter_id

        await obj_manager.delete(
            tri_state_filter_id=new_obj.tri_state_filter_id)

        result = await session.execute(
            select(TriStateFilter).filter(
                TriStateFilter._tri_state_filter_id == (
                    new_obj.tri_state_filter_id))  # type: ignore
        )
        fetched_obj = result.scalars().first()

        assert fetched_obj is None

    @pytest.mark.asyncio
    async def test_delete_nonexistent(
        self,
        obj_manager: TriStateFilterManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of deleting a nonexistent
        tri_state_filter.

        This test case ensures that when the delete method
        is called with the ID of a nonexistent
        tri_state_filter,
        an exception is raised. The test also verifies that
        the session is rolled back after the delete operation.

        :param obj_manager: The instance of the
            TriStateFilterManager class.
        :param session: The instance of the AsyncSession class.
        """
        with pytest.raises(Exception):
            await obj_manager.delete(999)

        await session.rollback()

    @pytest.mark.asyncio
    async def test_delete_invalid_type(
        self,
        obj_manager: TriStateFilterManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of deleting a tri_state_filter
        with an invalid type.

        This test case ensures that when the `delete` method
        of the `obj_manager` is called with an invalid type,
        an exception is raised. The test case expects the
        `delete` method to raise an exception, and if it doesn't,
        the test case will fail.

        Args:
            obj_manager
            (TriStateFilterManager): An
                instance of the
                `TriStateFilterManager` class.
            session (AsyncSession): An instance of the `AsyncSession` class.

        Returns:
            None

        Raises:
            Exception: If the `delete` method does not raise an exception.

        """
        with pytest.raises(Exception):
            await obj_manager.delete("999")  # type: ignore

        await session.rollback()

    @pytest.mark.asyncio
    async def test_get_list(
        self,
        obj_manager: TriStateFilterManager,
        session: AsyncSession
    ):
        """
        Test case for the `get_list` method of the
        `TriStateFilterManager` class.

        This test verifies that the `get_list`
        method returns the correct list of tri_state_filters.

        Steps:
        1. Call the `get_list` method of the
            `obj_manager` instance.
        2. Assert that the returned list is empty.
        3. Create 5 tri_state_filter objects using the
            `TriStateFilterFactory.create_async` method.
        4. Assert that the
            `tri_state_filters_data` variable
            is of type `List`.
        5. Call the `get_list` method of the
            `obj_manager` instance again.
        6. Assert that the returned list contains 5 tri_state_filters.
        7. Assert that all elements in the returned list are
            instances of the
            `TriStateFilter` class.
        """

        tri_state_filters = await obj_manager.get_list()

        assert len(tri_state_filters) == 0

        tri_state_filters_data = (
            [await TriStateFilterFactory.create_async(session)
             for _ in range(5)])

        assert isinstance(tri_state_filters_data, List)

        tri_state_filters = await obj_manager.get_list()

        assert len(tri_state_filters) == 5
        assert all(isinstance(
            tri_state_filter,
            TriStateFilter
        ) for tri_state_filter in tri_state_filters)

    @pytest.mark.asyncio
    async def test_to_json(
        self,
        obj_manager: TriStateFilterManager,
        session: AsyncSession
    ):
        """
        Test the 'to_json' method of the TriStateFilterManager class.

        Args:
            obj_manager
            (TriStateFilterManager): An
                instance of the
                TriStateFilterManager class.
            session (AsyncSession): An instance of the AsyncSession class.

        Returns:
            None

        Raises:
            AssertionError: If the json_data is None.
        """
        tri_state_filter = await \
            TriStateFilterFactory.build_async(
                session)

        json_data = obj_manager.to_json(
            tri_state_filter)

        assert json_data is not None

    @pytest.mark.asyncio
    async def test_to_dict(
        self,
        obj_manager: TriStateFilterManager,
        session: AsyncSession
    ):
        """
        Test the to_dict method of the TriStateFilterManager class.

        Args:
            obj_manager
            (TriStateFilterManager): An
                instance of the
                TriStateFilterManager class.
            session (AsyncSession): An instance of the AsyncSession class.

        Returns:
            None
        """
        tri_state_filter = await \
            TriStateFilterFactory.build_async(
                session)

        dict_data = \
            obj_manager.to_dict(
                tri_state_filter)

        assert dict_data is not None

    @pytest.mark.asyncio
    async def test_from_json(
        self,
        obj_manager: TriStateFilterManager,
        session: AsyncSession
    ):
        """
        Test the `from_json` method of the
        `TriStateFilterManager` class.

        This method tests the functionality of the
        `from_json` method of the
        `TriStateFilterManager` class.
        It creates a tri_state_filter using
        the `TriStateFilterFactory`
        and converts it to JSON using the `to_json` method.
        Then, it deserializes the JSON data using the
        `from_json` method and asserts that the deserialized
        tri_state_filter is an instance of the
        `TriStateFilter` class and has
        the same code as the original tri_state_filter.

        Args:
            obj_manager
            (TriStateFilterManager): An
                instance of the
                `TriStateFilterManager` class.
            session (AsyncSession): An instance of the `AsyncSession` class.

        Returns:
            None
        """
        tri_state_filter = await \
            TriStateFilterFactory.create_async(
                session)

        json_data = obj_manager.to_json(
            tri_state_filter)

        deserialized_tri_state_filter = await \
            obj_manager.from_json(json_data)

        assert isinstance(deserialized_tri_state_filter,
                          TriStateFilter)
        assert deserialized_tri_state_filter.code == \
            tri_state_filter.code

    @pytest.mark.asyncio
    async def test_from_dict(
        self,
        obj_manager: TriStateFilterManager,
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
            obj_manager
            (TriStateFilterManager): An instance
                of the `TriStateFilterManager` class.
            session (AsyncSession): An instance of the
            `AsyncSession` class.

        Returns:
            None

        Raises:
            AssertionError: If any of the assertions fail.
        """
        tri_state_filter = await \
            TriStateFilterFactory.create_async(
                session)

        schema = TriStateFilterSchema()

        new_obj = schema.dump(tri_state_filter)

        assert isinstance(new_obj, dict)

        deserialized_tri_state_filter = await \
            obj_manager.from_dict(
                new_obj)

        assert isinstance(deserialized_tri_state_filter,
                          TriStateFilter)

        assert deserialized_tri_state_filter.code == \
            tri_state_filter.code

    @pytest.mark.asyncio
    async def test_count_basic_functionality(
        self,
        obj_manager: TriStateFilterManager,
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
        2. Call the count method of the obj_manager.
        3. Assert that the count is equal to 5.

        """
        tri_state_filters_data = (
            [await TriStateFilterFactory.create_async(session)
             for _ in range(5)])

        assert isinstance(tri_state_filters_data, List)

        count = await obj_manager.count()

        assert count == 5

    @pytest.mark.asyncio
    async def test_count_empty_database(
        self,
        obj_manager: TriStateFilterManager
    ):
        """
        Test the count method when the database is empty.

        This test case checks if the count method of the
        TriStateFilterManager class
        returns 0 when the database is empty.

        Args:
            obj_manager
            (TriStateFilterManager): An
                instance of the
                TriStateFilterManager class.

        Returns:
            None
        """

        count = await obj_manager.count()

        assert count == 0

    @pytest.mark.asyncio
    async def test_refresh_basic(
        self,
        obj_manager: TriStateFilterManager,
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
            obj_manager
            (TriStateFilterManager): The
                manager responsible
                for tri_state_filter operations.
            session (AsyncSession): The SQLAlchemy asynchronous session.
        """
        # Add a tri_state_filter
        obj_1 = await TriStateFilterFactory.create_async(
            session=session)

        # Retrieve the tri_state_filter from the database
        result = await session.execute(
            select(TriStateFilter).filter(
                TriStateFilter._tri_state_filter_id == (
                    obj_1.tri_state_filter_id))  # type: ignore
        )  # type: ignore
        obj_2 = result.scalars().first()

        # Verify that the retrieved tri_state_filter
        # matches the added tri_state_filter
        assert obj_1.code == \
            obj_2.code

        # Update the tri_state_filter's code
        updated_code1 = uuid.uuid4()
        obj_1.code = updated_code1
        updated_obj_1 = await obj_manager.update(
            obj_1)

        # Verify that the updated tri_state_filter
        # is of type TriStateFilter
        # and has the updated code
        assert isinstance(updated_obj_1,
                          TriStateFilter)

        assert updated_obj_1.code == updated_code1

        # Refresh the original tri_state_filter instance
        refreshed_obj_2 = await obj_manager.refresh(
            obj_2)

        # Verify that the refreshed tri_state_filter
        # reflects the updated code
        assert refreshed_obj_2.code == updated_code1

    @pytest.mark.asyncio
    async def test_refresh_nonexistent_tri_state_filter(
        self,
        obj_manager: TriStateFilterManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of refreshing a
        nonexistent tri_state_filter.

        Args:
            obj_manager
            (TriStateFilterManager): The
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
            await obj_manager.refresh(
                tri_state_filter)

        await session.rollback()

    @pytest.mark.asyncio
    async def test_exists_with_existing_tri_state_filter(
        self,
        obj_manager: TriStateFilterManager,
        session: AsyncSession
    ):
        """
        Test case to check if a tri_state_filter
        exists using the manager function.

        Args:
            obj_manager
            (TriStateFilterManager): The
                tri_state_filter manager instance.
            session (AsyncSession): The async session object.

        Returns:
            None
        """
        # Add a tri_state_filter
        obj_1 = await TriStateFilterFactory.create_async(
            session=session)

        # Check if the tri_state_filter exists
        # using the manager function
        assert await obj_manager.exists(
            obj_1.tri_state_filter_id) is True

    @pytest.mark.asyncio
    async def test_is_equal_with_existing_tri_state_filter(
        self,
        obj_manager: TriStateFilterManager,
        session: AsyncSession
    ):
        """
        Test if the is_equal method of the
        TriStateFilterManager
        class correctly compares two
        tri_state_filters.

        Args:
            obj_manager
            (TriStateFilterManager): An
                instance of the
                TriStateFilterManager class.
            session (AsyncSession): An instance of the AsyncSession class.

        Returns:
            None
        """
        # Add a tri_state_filter
        obj_1 = await \
            TriStateFilterFactory.create_async(
                session=session)

        obj_2 = await \
            obj_manager.get_by_id(
                tri_state_filter_id=obj_1.tri_state_filter_id)

        assert obj_manager.is_equal(
            obj_1, obj_2) is True

        obj_1_dict = \
            obj_manager.to_dict(
                obj_1)

        tri_state_filter3 = await \
            obj_manager.from_dict(
                obj_1_dict)

        assert obj_manager.is_equal(
            obj_1, tri_state_filter3) is True

    @pytest.mark.asyncio
    async def test_exists_with_nonexistent_tri_state_filter(
        self,
        obj_manager: TriStateFilterManager
    ):
        """
        Test case to check if a tri_state_filter with a
        non-existent ID exists in the database.

        Args:
            obj_manager
            (TriStateFilterManager): The
                instance of the TriStateFilterManager class.

        Returns:
            bool: True if the tri_state_filter exists,
                False otherwise.
        """
        non_existent_id = 999

        assert await obj_manager.exists(non_existent_id) is False

    @pytest.mark.asyncio
    async def test_exists_with_invalid_id_type(
        self,
        obj_manager: TriStateFilterManager,
        session: AsyncSession
    ):
        """
        Test case to check if the exists method raises
        an exception when an invalid ID type is provided.

        Args:
            obj_manager
            (TriStateFilterManager): The instance
                of the TriStateFilterManager class.
            session (AsyncSession): The instance of the AsyncSession class.

        Raises:
            Exception: If an exception is not raised by the exists method.

        Returns:
            None
        """
        invalid_id = "invalid_id"

        with pytest.raises(Exception):
            await obj_manager.exists(invalid_id)  # type: ignore  # noqa: E501

        await session.rollback()
