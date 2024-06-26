# managers/tests/date_greater_than_filter_test.py
# pylint: disable=protected-access
# pylint: disable=unused-argument
# pylint: disable=unused-import
"""
    This class contains unit tests for the
    `DateGreaterThanFilterManager` class.
"""

from typing import List
import uuid  # noqa: F401

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from helpers.session_context import SessionContext
from managers.date_greater_than_filter import (
    DateGreaterThanFilterManager)
from models import DateGreaterThanFilter
from models.factory import (
    DateGreaterThanFilterFactory)
from models.serialization_schema.date_greater_than_filter import (
    DateGreaterThanFilterSchema)


class TestDateGreaterThanFilterManager:
    """
    This class contains unit tests for the
    `DateGreaterThanFilterManager` class.
    """

    @pytest_asyncio.fixture(scope="function")
    async def obj_manager(self, session: AsyncSession):
        """
        Fixture that returns an instance of
        `DateGreaterThanFilterManager` for testing.
        """
        session_context = SessionContext(dict(), session)
        session_context.customer_code = uuid.uuid4()
        return DateGreaterThanFilterManager(session_context)

    @pytest.mark.asyncio
    async def test_build(
        self,
        obj_manager: DateGreaterThanFilterManager
    ):
        """
        Test case for the `build` method of
        `DateGreaterThanFilterManager`.
        """
        # Define mock data for our date_greater_than_filter
        mock_data = {
            "code": uuid.uuid4()
        }

        # Call the build function of the manager
        date_greater_than_filter = await \
            obj_manager.build(
                **mock_data)

        # Assert that the returned object is an
        # instance of DateGreaterThanFilter
        assert isinstance(
            date_greater_than_filter,
            DateGreaterThanFilter)

        # Assert that the attributes of the
        # date_greater_than_filter match our mock data
        assert date_greater_than_filter.code == mock_data["code"]

    @pytest.mark.asyncio
    async def test_build_with_missing_data(
        self,
        obj_manager: DateGreaterThanFilterManager,
        session: AsyncSession
    ):
        """
        Test case for the `build` method of
        `DateGreaterThanFilterManager` with missing data.
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
    async def test_add_correctly_adds_date_greater_than_filter_to_database(
        self,
        obj_manager: DateGreaterThanFilterManager,
        session: AsyncSession
    ):
        """
        Test case for the `add` method of
        `DateGreaterThanFilterManager` that checks if a
        date_greater_than_filter is correctly added to the database.
        """
        new_obj = await \
            DateGreaterThanFilterFactory.build_async(
                session)

        assert new_obj.date_greater_than_filter_id == 0

        # Add the date_greater_than_filter using the
        # manager's add method
        added_obj = await \
            obj_manager.add(
                date_greater_than_filter=new_obj)

        assert isinstance(added_obj,
                          DateGreaterThanFilter)

        assert str(added_obj.insert_user_id) == (
            str(obj_manager._session_context.customer_code))
        assert str(added_obj.last_update_user_id) == (
            str(obj_manager._session_context.customer_code))

        assert added_obj.date_greater_than_filter_id > 0

        # Fetch the date_greater_than_filter from
        # the database directly
        result = await session.execute(
            select(DateGreaterThanFilter).filter(
                DateGreaterThanFilter._date_greater_than_filter_id == (
                    added_obj.date_greater_than_filter_id)  # type: ignore
            )
        )
        fetched_obj = result.scalars().first()

        # Assert that the fetched date_greater_than_filter
        # is not None and matches the
        # added date_greater_than_filter
        assert fetched_obj is not None
        assert isinstance(fetched_obj,
                          DateGreaterThanFilter)
        assert fetched_obj.date_greater_than_filter_id == \
            added_obj.date_greater_than_filter_id

    @pytest.mark.asyncio
    async def test_add_returns_correct_date_greater_than_filter_object(
        self,
        obj_manager: DateGreaterThanFilterManager,
        session: AsyncSession
    ):
        """
        Test case for the `add` method of
        `DateGreaterThanFilterManager` that checks if the
        correct date_greater_than_filter object is returned.
        """
        # Create a test date_greater_than_filter
        # using the DateGreaterThanFilterFactory
        # without persisting it to the database
        new_obj = await \
            DateGreaterThanFilterFactory.build_async(
                session)

        assert new_obj.date_greater_than_filter_id == 0

        new_obj.code = uuid.uuid4()

        # Add the date_greater_than_filter using
        # the manager's add method
        added_obj = await \
            obj_manager.add(
                date_greater_than_filter=new_obj)

        assert isinstance(added_obj,
                          DateGreaterThanFilter)

        assert str(added_obj.insert_user_id) == (
            str(obj_manager._session_context.customer_code))
        assert str(added_obj.last_update_user_id) == (
            str(obj_manager._session_context.customer_code))

        assert added_obj.date_greater_than_filter_id > 0

        # Assert that the returned
        # date_greater_than_filter matches the
        # test date_greater_than_filter
        assert added_obj.date_greater_than_filter_id == \
            new_obj.date_greater_than_filter_id
        assert added_obj.code == \
            new_obj.code

    @pytest.mark.asyncio
    async def test_update(
        self,
        obj_manager: DateGreaterThanFilterManager,
        session: AsyncSession
    ):
        """
        Test case for the `update` method
        of `DateGreaterThanFilterManager`
        that checks if a date_greater_than_filter
        is correctly updated.
        """
        new_obj = await \
            DateGreaterThanFilterFactory.create_async(
                session)

        new_obj.code = uuid.uuid4()

        updated_obj = await \
            obj_manager.update(
                date_greater_than_filter=new_obj)

        assert isinstance(updated_obj,
                          DateGreaterThanFilter)

        assert str(updated_obj.last_update_user_id) == str(
            obj_manager._session_context.customer_code)

        assert updated_obj.date_greater_than_filter_id == \
            new_obj.date_greater_than_filter_id
        assert updated_obj.code == \
            new_obj.code

        result = await session.execute(
            select(DateGreaterThanFilter).filter(
                DateGreaterThanFilter._date_greater_than_filter_id == (
                    new_obj.date_greater_than_filter_id))  # type: ignore
        )

        fetched_obj = result.scalars().first()

        assert updated_obj.date_greater_than_filter_id == \
            fetched_obj.date_greater_than_filter_id
        assert updated_obj.code == \
            fetched_obj.code

        assert new_obj.date_greater_than_filter_id == \
            fetched_obj.date_greater_than_filter_id
        assert new_obj.code == \
            fetched_obj.code

    @pytest.mark.asyncio
    async def test_update_via_dict(
        self,
        obj_manager: DateGreaterThanFilterManager,
        session: AsyncSession
    ):
        """
        Test case for the `update` method
        of `DateGreaterThanFilterManager`
        that checks if a date_greater_than_filter is
        correctly updated using a dictionary.
        """
        new_obj = await \
            DateGreaterThanFilterFactory.create_async(
                session)

        new_code = uuid.uuid4()

        updated_obj = await \
            obj_manager.update(
                date_greater_than_filter=new_obj,
                code=new_code
            )

        assert isinstance(updated_obj,
                          DateGreaterThanFilter)

        assert str(updated_obj.last_update_user_id) == str(
            obj_manager._session_context.customer_code
        )

        assert updated_obj.date_greater_than_filter_id == \
            new_obj.date_greater_than_filter_id
        assert updated_obj.code == new_code

        result = await session.execute(
            select(DateGreaterThanFilter).filter(
                DateGreaterThanFilter._date_greater_than_filter_id == (
                    new_obj.date_greater_than_filter_id))  # type: ignore
        )

        fetched_obj = result.scalars().first()

        assert updated_obj.date_greater_than_filter_id == \
            fetched_obj.date_greater_than_filter_id
        assert updated_obj.code == \
            fetched_obj.code

        assert new_obj.date_greater_than_filter_id == \
            fetched_obj.date_greater_than_filter_id
        assert new_code == \
            fetched_obj.code

    @pytest.mark.asyncio
    async def test_update_invalid_date_greater_than_filter(
        self,
        obj_manager: DateGreaterThanFilterManager
    ):
        """
        Test case for the `update` method of
        `DateGreaterThanFilterManager`
        with an invalid date_greater_than_filter.
        """

        # None date_greater_than_filter
        date_greater_than_filter = None

        new_code = uuid.uuid4()

        updated_obj = await (
            obj_manager.update(
                date_greater_than_filter, code=new_code))  # type: ignore

        # Assertions
        assert updated_obj is None

    @pytest.mark.asyncio
    async def test_update_with_nonexistent_attribute(
        self,
        obj_manager: DateGreaterThanFilterManager,
        session: AsyncSession
    ):
        """
        Test case for the `update` method of
        `DateGreaterThanFilterManager`
        with a nonexistent attribute.
        """
        new_obj = await \
            DateGreaterThanFilterFactory.create_async(
                session)

        new_code = uuid.uuid4()

        with pytest.raises(ValueError):
            await obj_manager.update(
                date_greater_than_filter=new_obj,
                xxx=new_code
            )

        await session.rollback()

    @pytest.mark.asyncio
    async def test_delete(
        self,
        obj_manager: DateGreaterThanFilterManager,
        session: AsyncSession
    ):
        """
        Test case for the `delete` method of
        `DateGreaterThanFilterManager`.
        """
        new_obj = await DateGreaterThanFilterFactory.create_async(
            session)

        result = await session.execute(
            select(DateGreaterThanFilter).filter(
                DateGreaterThanFilter._date_greater_than_filter_id == (
                    new_obj.date_greater_than_filter_id))  # type: ignore
        )
        fetched_obj = result.scalars().first()

        assert isinstance(fetched_obj,
                          DateGreaterThanFilter)

        assert fetched_obj.date_greater_than_filter_id == \
            new_obj.date_greater_than_filter_id

        await obj_manager.delete(
            date_greater_than_filter_id=new_obj.date_greater_than_filter_id)

        result = await session.execute(
            select(DateGreaterThanFilter).filter(
                DateGreaterThanFilter._date_greater_than_filter_id == (
                    new_obj.date_greater_than_filter_id))  # type: ignore
        )
        fetched_obj = result.scalars().first()

        assert fetched_obj is None

    @pytest.mark.asyncio
    async def test_delete_nonexistent(
        self,
        obj_manager: DateGreaterThanFilterManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of deleting a nonexistent
        date_greater_than_filter.

        This test case ensures that when the delete method
        is called with the ID of a nonexistent
        date_greater_than_filter,
        an exception is raised. The test also verifies that
        the session is rolled back after the delete operation.

        :param obj_manager: The instance of the
            DateGreaterThanFilterManager class.
        :param session: The instance of the AsyncSession class.
        """
        with pytest.raises(Exception):
            await obj_manager.delete(999)

        await session.rollback()

    @pytest.mark.asyncio
    async def test_delete_invalid_type(
        self,
        obj_manager: DateGreaterThanFilterManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of deleting a date_greater_than_filter
        with an invalid type.

        This test case ensures that when the `delete` method
        of the `obj_manager` is called with an invalid type,
        an exception is raised. The test case expects the
        `delete` method to raise an exception, and if it doesn't,
        the test case will fail.

        Args:
            obj_manager
            (DateGreaterThanFilterManager): An
                instance of the
                `DateGreaterThanFilterManager` class.
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
        obj_manager: DateGreaterThanFilterManager,
        session: AsyncSession
    ):
        """
        Test case for the `get_list` method of the
        `DateGreaterThanFilterManager` class.

        This test verifies that the `get_list`
        method returns the correct list of date_greater_than_filters.

        Steps:
        1. Call the `get_list` method of the
            `obj_manager` instance.
        2. Assert that the returned list is empty.
        3. Create 5 date_greater_than_filter objects using the
            `DateGreaterThanFilterFactory.create_async` method.
        4. Assert that the
            `date_greater_than_filters_data` variable
            is of type `List`.
        5. Call the `get_list` method of the
            `obj_manager` instance again.
        6. Assert that the returned list contains 5 date_greater_than_filters.
        7. Assert that all elements in the returned list are
            instances of the
            `DateGreaterThanFilter` class.
        """

        date_greater_than_filters = await obj_manager.get_list()

        assert len(date_greater_than_filters) == 0

        date_greater_than_filters_data = (
            [await DateGreaterThanFilterFactory.create_async(session)
             for _ in range(5)])

        assert isinstance(date_greater_than_filters_data, List)

        date_greater_than_filters = await obj_manager.get_list()

        assert len(date_greater_than_filters) == 5
        assert all(isinstance(
            date_greater_than_filter,
            DateGreaterThanFilter
        ) for date_greater_than_filter in date_greater_than_filters)

    @pytest.mark.asyncio
    async def test_to_json(
        self,
        obj_manager: DateGreaterThanFilterManager,
        session: AsyncSession
    ):
        """
        Test the 'to_json' method of the DateGreaterThanFilterManager class.

        Args:
            obj_manager
            (DateGreaterThanFilterManager): An
                instance of the
                DateGreaterThanFilterManager class.
            session (AsyncSession): An instance of the AsyncSession class.

        Returns:
            None

        Raises:
            AssertionError: If the json_data is None.
        """
        date_greater_than_filter = await \
            DateGreaterThanFilterFactory.build_async(
                session)

        json_data = obj_manager.to_json(
            date_greater_than_filter)

        assert json_data is not None

    @pytest.mark.asyncio
    async def test_to_dict(
        self,
        obj_manager: DateGreaterThanFilterManager,
        session: AsyncSession
    ):
        """
        Test the to_dict method of the DateGreaterThanFilterManager class.

        Args:
            obj_manager
            (DateGreaterThanFilterManager): An
                instance of the
                DateGreaterThanFilterManager class.
            session (AsyncSession): An instance of the AsyncSession class.

        Returns:
            None
        """
        date_greater_than_filter = await \
            DateGreaterThanFilterFactory.build_async(
                session)

        dict_data = \
            obj_manager.to_dict(
                date_greater_than_filter)

        assert dict_data is not None

    @pytest.mark.asyncio
    async def test_from_json(
        self,
        obj_manager: DateGreaterThanFilterManager,
        session: AsyncSession
    ):
        """
        Test the `from_json` method of the
        `DateGreaterThanFilterManager` class.

        This method tests the functionality of the
        `from_json` method of the
        `DateGreaterThanFilterManager` class.
        It creates a date_greater_than_filter using
        the `DateGreaterThanFilterFactory`
        and converts it to JSON using the `to_json` method.
        Then, it deserializes the JSON data using the
        `from_json` method and asserts that the deserialized
        date_greater_than_filter is an instance of the
        `DateGreaterThanFilter` class and has
        the same code as the original date_greater_than_filter.

        Args:
            obj_manager
            (DateGreaterThanFilterManager): An
                instance of the
                `DateGreaterThanFilterManager` class.
            session (AsyncSession): An instance of the `AsyncSession` class.

        Returns:
            None
        """
        date_greater_than_filter = await \
            DateGreaterThanFilterFactory.create_async(
                session)

        json_data = obj_manager.to_json(
            date_greater_than_filter)

        deserialized_date_greater_than_filter = await \
            obj_manager.from_json(json_data)

        assert isinstance(deserialized_date_greater_than_filter,
                          DateGreaterThanFilter)
        assert deserialized_date_greater_than_filter.code == \
            date_greater_than_filter.code

    @pytest.mark.asyncio
    async def test_from_dict(
        self,
        obj_manager: DateGreaterThanFilterManager,
        session: AsyncSession
    ):
        """
        Test the `from_dict` method of the
        `DateGreaterThanFilterManager` class.

        This method tests the functionality of the
        `from_dict` method, which is used to deserialize
        a dictionary representation of a
        date_greater_than_filter object.

        Args:
            obj_manager
            (DateGreaterThanFilterManager): An instance
                of the `DateGreaterThanFilterManager` class.
            session (AsyncSession): An instance of the
            `AsyncSession` class.

        Returns:
            None

        Raises:
            AssertionError: If any of the assertions fail.
        """
        date_greater_than_filter = await \
            DateGreaterThanFilterFactory.create_async(
                session)

        schema = DateGreaterThanFilterSchema()

        new_obj = schema.dump(date_greater_than_filter)

        assert isinstance(new_obj, dict)

        deserialized_date_greater_than_filter = await \
            obj_manager.from_dict(
                new_obj)

        assert isinstance(deserialized_date_greater_than_filter,
                          DateGreaterThanFilter)

        assert deserialized_date_greater_than_filter.code == \
            date_greater_than_filter.code

    @pytest.mark.asyncio
    async def test_count_basic_functionality(
        self,
        obj_manager: DateGreaterThanFilterManager,
        session: AsyncSession
    ):
        """
        Test the basic functionality of the count method
        in the DateGreaterThanFilterManager class.

        This test case creates 5 date_greater_than_filter
        objects using the
        DateGreaterThanFilterFactory and checks if the count method
        returns the correct count of
        date_greater_than_filters.

        Steps:
        1. Create 5 date_greater_than_filter objects using
            the DateGreaterThanFilterFactory.
        2. Call the count method of the obj_manager.
        3. Assert that the count is equal to 5.

        """
        date_greater_than_filters_data = (
            [await DateGreaterThanFilterFactory.create_async(session)
             for _ in range(5)])

        assert isinstance(date_greater_than_filters_data, List)

        count = await obj_manager.count()

        assert count == 5

    @pytest.mark.asyncio
    async def test_count_empty_database(
        self,
        obj_manager: DateGreaterThanFilterManager
    ):
        """
        Test the count method when the database is empty.

        This test case checks if the count method of the
        DateGreaterThanFilterManager class
        returns 0 when the database is empty.

        Args:
            obj_manager
            (DateGreaterThanFilterManager): An
                instance of the
                DateGreaterThanFilterManager class.

        Returns:
            None
        """

        count = await obj_manager.count()

        assert count == 0

    @pytest.mark.asyncio
    async def test_refresh_basic(
        self,
        obj_manager: DateGreaterThanFilterManager,
        session: AsyncSession
    ):
        """
        Test the basic functionality of refreshing
        a date_greater_than_filter instance.

        This test performs the following steps:
        1. Creates a date_greater_than_filter instance using
            the DateGreaterThanFilterFactory.
        2. Retrieves the date_greater_than_filter from th
            database to ensure
            it was added correctly.
        3. Updates the date_greater_than_filter's code and verifies the update.
        4. Refreshes the original date_greater_than_filter instance
            and checks if
            it reflects the updated code.

        Args:
            obj_manager
            (DateGreaterThanFilterManager): The
                manager responsible
                for date_greater_than_filter operations.
            session (AsyncSession): The SQLAlchemy asynchronous session.
        """
        # Add a date_greater_than_filter
        obj_1 = await DateGreaterThanFilterFactory.create_async(
            session=session)

        # Retrieve the date_greater_than_filter from the database
        result = await session.execute(
            select(DateGreaterThanFilter).filter(
                DateGreaterThanFilter._date_greater_than_filter_id == (
                    obj_1.date_greater_than_filter_id))  # type: ignore
        )  # type: ignore
        obj_2 = result.scalars().first()

        # Verify that the retrieved date_greater_than_filter
        # matches the added date_greater_than_filter
        assert obj_1.code == \
            obj_2.code

        # Update the date_greater_than_filter's code
        updated_code1 = uuid.uuid4()
        obj_1.code = updated_code1
        updated_obj_1 = await obj_manager.update(
            obj_1)

        # Verify that the updated date_greater_than_filter
        # is of type DateGreaterThanFilter
        # and has the updated code
        assert isinstance(updated_obj_1,
                          DateGreaterThanFilter)

        assert updated_obj_1.code == updated_code1

        # Refresh the original date_greater_than_filter instance
        refreshed_obj_2 = await obj_manager.refresh(
            obj_2)

        # Verify that the refreshed date_greater_than_filter
        # reflects the updated code
        assert refreshed_obj_2.code == updated_code1

    @pytest.mark.asyncio
    async def test_refresh_nonexistent_date_greater_than_filter(
        self,
        obj_manager: DateGreaterThanFilterManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of refreshing a
        nonexistent date_greater_than_filter.

        Args:
            obj_manager
            (DateGreaterThanFilterManager): The
                instance of the
                DateGreaterThanFilterManager class.
            session (AsyncSession): The instance of the AsyncSession class.

        Raises:
            Exception: If the date_greater_than_filter
            refresh operation raises an exception.

        Returns:
            None
        """
        date_greater_than_filter = DateGreaterThanFilter(
            date_greater_than_filter_id=999)

        with pytest.raises(Exception):
            await obj_manager.refresh(
                date_greater_than_filter)

        await session.rollback()

    @pytest.mark.asyncio
    async def test_exists_with_existing_date_greater_than_filter(
        self,
        obj_manager: DateGreaterThanFilterManager,
        session: AsyncSession
    ):
        """
        Test case to check if a date_greater_than_filter
        exists using the manager function.

        Args:
            obj_manager
            (DateGreaterThanFilterManager): The
                date_greater_than_filter manager instance.
            session (AsyncSession): The async session object.

        Returns:
            None
        """
        # Add a date_greater_than_filter
        obj_1 = await DateGreaterThanFilterFactory.create_async(
            session=session)

        # Check if the date_greater_than_filter exists
        # using the manager function
        assert await obj_manager.exists(
            obj_1.date_greater_than_filter_id) is True

    @pytest.mark.asyncio
    async def test_is_equal_with_existing_date_greater_than_filter(
        self,
        obj_manager: DateGreaterThanFilterManager,
        session: AsyncSession
    ):
        """
        Test if the is_equal method of the
        DateGreaterThanFilterManager
        class correctly compares two
        date_greater_than_filters.

        Args:
            obj_manager
            (DateGreaterThanFilterManager): An
                instance of the
                DateGreaterThanFilterManager class.
            session (AsyncSession): An instance of the AsyncSession class.

        Returns:
            None
        """
        # Add a date_greater_than_filter
        obj_1 = await \
            DateGreaterThanFilterFactory.create_async(
                session=session)

        obj_2 = await \
            obj_manager.get_by_id(
                date_greater_than_filter_id=obj_1.date_greater_than_filter_id)

        assert obj_manager.is_equal(
            obj_1, obj_2) is True

        obj_1_dict = \
            obj_manager.to_dict(
                obj_1)

        date_greater_than_filter3 = await \
            obj_manager.from_dict(
                obj_1_dict)

        assert obj_manager.is_equal(
            obj_1, date_greater_than_filter3) is True

    @pytest.mark.asyncio
    async def test_exists_with_nonexistent_date_greater_than_filter(
        self,
        obj_manager: DateGreaterThanFilterManager
    ):
        """
        Test case to check if a date_greater_than_filter with a
        non-existent ID exists in the database.

        Args:
            obj_manager
            (DateGreaterThanFilterManager): The
                instance of the DateGreaterThanFilterManager class.

        Returns:
            bool: True if the date_greater_than_filter exists,
                False otherwise.
        """
        non_existent_id = 999

        assert await obj_manager.exists(non_existent_id) is False

    @pytest.mark.asyncio
    async def test_exists_with_invalid_id_type(
        self,
        obj_manager: DateGreaterThanFilterManager,
        session: AsyncSession
    ):
        """
        Test case to check if the exists method raises
        an exception when an invalid ID type is provided.

        Args:
            obj_manager
            (DateGreaterThanFilterManager): The instance
                of the DateGreaterThanFilterManager class.
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
