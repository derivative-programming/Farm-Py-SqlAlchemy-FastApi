# models/managers/tests/date_greater_than_filter_test.py
# pylint: disable=protected-access
# pylint: disable=unused-argument
"""
    This class contains unit tests for the
    `DateGreaterThanFilterManager` class.
"""

import logging
import uuid

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from helpers.session_context import SessionContext
from managers.date_greater_than_filter import DateGreaterThanFilterManager
from models import DateGreaterThanFilter
from models.factory import DateGreaterThanFilterFactory

class TestDateGreaterThanFilterBulkManager:
    """
    This class contains unit tests for the
    `DateGreaterThanFilterManager` class.
    """

    @pytest_asyncio.fixture(scope="function")
    async def date_greater_than_filter_manager(self, session: AsyncSession):
        """
        Fixture that returns an instance of
        `DateGreaterThanFilterManager` for testing.
        """
        session_context = SessionContext(dict(), session)
        session_context.customer_code = uuid.uuid4()
        return DateGreaterThanFilterManager(session_context)

    @pytest.mark.asyncio
    async def test_add_bulk(
        self,
        date_greater_than_filter_manager: DateGreaterThanFilterManager,
        session: AsyncSession
    ):
        """
        Test case for the `add_bulk` method of the
        `DateGreaterThanFilterManager` class.

        This test case verifies that the `add_bulk`
        method correctly adds multiple date_greater_than_filters to the database.

        Steps:
        1. Generate a list of date_greater_than_filter data using the
            `DateGreaterThanFilterFactory.build_async` method.
        2. Call the `add_bulk` method of the
            `date_greater_than_filter_manager` instance,
            passing in the
            generated date_greater_than_filter data.
        3. Verify that the number of date_greater_than_filters
            returned is
            equal to the number of date_greater_than_filters added.
        4. For each updated date_greater_than_filter, fetch the corresponding
            date_greater_than_filter from the database.
        5. Verify that the fetched date_greater_than_filter
            is an instance of the
            `DateGreaterThanFilter` class.
        6. Verify that the insert_user_id and
            last_update_user_id of the fetched
            date_greater_than_filter match the
            customer code of the session context.
        7. Verify that the date_greater_than_filter_id of the fetched
            date_greater_than_filter matches the
            date_greater_than_filter_id of the updated
            date_greater_than_filter.

        """
        date_greater_than_filters_data = [
            await DateGreaterThanFilterFactory.build_async(session) for _ in range(5)]

        date_greater_than_filters = await date_greater_than_filter_manager.add_bulk(
            date_greater_than_filters_data)

        assert len(date_greater_than_filters) == 5

        for updated_date_greater_than_filter in date_greater_than_filters:
            result = await session.execute(
                select(DateGreaterThanFilter).filter(
                    DateGreaterThanFilter._date_greater_than_filter_id == updated_date_greater_than_filter.date_greater_than_filter_id  # type: ignore
                )
            )
            fetched_date_greater_than_filter = result.scalars().first()

            assert isinstance(fetched_date_greater_than_filter, DateGreaterThanFilter)

            assert str(fetched_date_greater_than_filter.insert_user_id) == (
                str(date_greater_than_filter_manager._session_context.customer_code))
            assert str(fetched_date_greater_than_filter.last_update_user_id) == (
                str(date_greater_than_filter_manager._session_context.customer_code))

            assert fetched_date_greater_than_filter.date_greater_than_filter_id == \
                updated_date_greater_than_filter.date_greater_than_filter_id

    @pytest.mark.asyncio
    async def test_update_bulk_success(
        self,
        date_greater_than_filter_manager: DateGreaterThanFilterManager,
        session: AsyncSession
    ):
        """
        Test case for bulk update of date_greater_than_filters.

        This test case verifies the functionality of the
        `update_bulk` method in the `DateGreaterThanFilterManager` class.
        It creates two date_greater_than_filter instances,
        updates their codes
        using the `update_bulk` method, and then verifies
        that the updates were successful by checking the
        updated codes in the database.

        Steps:
        1. Create two date_greater_than_filter instances using the
            `DateGreaterThanFilterFactory.create_async` method.
        2. Generate new codes for the date_greater_than_filters.
        3. Update the date_greater_than_filters' codes using the `update_bulk` method.
        4. Verify that the update was successful by checking
            the updated codes in the database.

        Args:
            date_greater_than_filter_manager (DateGreaterThanFilterManager): An instance of the
                `DateGreaterThanFilterManager` class.
            session (AsyncSession): An instance of the `AsyncSession` class.

        Returns:
            None
        """
        # Mocking date_greater_than_filter instances
        date_greater_than_filter1 = await DateGreaterThanFilterFactory.create_async(
            session=session)
        date_greater_than_filter2 = await DateGreaterThanFilterFactory.create_async(
            session=session)
        logging.info(date_greater_than_filter1.__dict__)

        code_updated1 = uuid.uuid4()
        code_updated2 = uuid.uuid4()
        logging.info(code_updated1)
        logging.info(code_updated2)

        # Update date_greater_than_filters
        updates = [
            {
                "date_greater_than_filter_id": date_greater_than_filter1.date_greater_than_filter_id,
                "code": code_updated1
            },
            {
                "date_greater_than_filter_id": date_greater_than_filter2.date_greater_than_filter_id,
                "code": code_updated2
            }
        ]
        updated_date_greater_than_filters = await date_greater_than_filter_manager.update_bulk(
            updates)

        logging.info('bulk update results')
        # Assertions
        assert len(updated_date_greater_than_filters) == 2
        logging.info(updated_date_greater_than_filters[0].__dict__)
        logging.info(updated_date_greater_than_filters[1].__dict__)

        logging.info('getall')
        date_greater_than_filters = await date_greater_than_filter_manager.get_list()
        logging.info(date_greater_than_filters[0].__dict__)
        logging.info(date_greater_than_filters[1].__dict__)

        assert updated_date_greater_than_filters[0].code == code_updated1
        assert updated_date_greater_than_filters[1].code == code_updated2

        assert str(updated_date_greater_than_filters[0].last_update_user_id) == (
            str(date_greater_than_filter_manager._session_context.customer_code))

        assert str(updated_date_greater_than_filters[1].last_update_user_id) == (
            str(date_greater_than_filter_manager._session_context.customer_code))

        result = await session.execute(
            select(DateGreaterThanFilter).filter(
                DateGreaterThanFilter._date_greater_than_filter_id == 1)  # type: ignore
        )
        fetched_date_greater_than_filter = result.scalars().first()

        assert isinstance(fetched_date_greater_than_filter, DateGreaterThanFilter)

        assert fetched_date_greater_than_filter.code == code_updated1

        result = await session.execute(
            select(DateGreaterThanFilter).filter(
                DateGreaterThanFilter._date_greater_than_filter_id == 2)  # type: ignore
        )
        fetched_date_greater_than_filter = result.scalars().first()

        assert isinstance(fetched_date_greater_than_filter, DateGreaterThanFilter)

        assert fetched_date_greater_than_filter.code == code_updated2

    @pytest.mark.asyncio
    async def test_update_bulk_missing_date_greater_than_filter_id(
        self,
        date_greater_than_filter_manager: DateGreaterThanFilterManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of the `update_bulk`
        method when the date_greater_than_filter_id is missing.

        This test case ensures that when the date_greater_than_filter_id is
        missing in the updates list,
        an exception is raised and the session is rolled back.

        Steps:
        1. Prepare the updates list with a missing date_greater_than_filter_id.
        2. Call the `update_bulk` method with the updates list.
        3. Assert that an exception is raised.
        4. Rollback the session to undo any changes made during the test.

        """
        # No date_greater_than_filters to update since date_greater_than_filter_id is missing
        updates = [{"name": "Red Rose"}]

        with pytest.raises(Exception):
            await date_greater_than_filter_manager.update_bulk(updates)

        await session.rollback()

    @pytest.mark.asyncio
    async def test_update_bulk_date_greater_than_filter_not_found(
        self,
        date_greater_than_filter_manager: DateGreaterThanFilterManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of the update_bulk
        method when a date_greater_than_filter is not found.

        This test case performs the following steps:
        1. Defines a list of date_greater_than_filter updates,
            where each update
            contains a date_greater_than_filter_id and a code.
        2. Calls the update_bulk method of the
            date_greater_than_filter_manager with the list of updates.
        3. Expects an exception to be raised, indicating that
            the date_greater_than_filter was not found.
        4. Rolls back the session to undo any changes made during the test.

        Note: This test assumes that the update_bulk method
        throws an exception when a
        date_greater_than_filter is not found.

        """

        # Update date_greater_than_filters
        updates = [{"date_greater_than_filter_id": 1, "code": uuid.uuid4()}]

        with pytest.raises(Exception):
            await date_greater_than_filter_manager.update_bulk(updates)

        await session.rollback()

    @pytest.mark.asyncio
    async def test_update_bulk_invalid_type(
        self,
        date_greater_than_filter_manager: DateGreaterThanFilterManager,
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

        :param date_greater_than_filter_manager: An instance of the DateGreaterThanFilterManager class.
        :param session: An instance of the AsyncSession class.
        """

        updates = [{"date_greater_than_filter_id": "2", "code": uuid.uuid4()}]

        with pytest.raises(Exception):
            await date_greater_than_filter_manager.update_bulk(updates)

        await session.rollback()

    @pytest.mark.asyncio
    async def test_delete_bulk_success(
        self,
        date_greater_than_filter_manager: DateGreaterThanFilterManager,
        session: AsyncSession
    ):
        """
        Test case for the delete_bulk method of the
        DateGreaterThanFilterManager class.

        This test verifies that the delete_bulk method
        successfully deletes multiple date_greater_than_filters
        from the database.

        Steps:
        1. Create two date_greater_than_filter objects
            using the DateGreaterThanFilterFactory.
        2. Delete the date_greater_than_filters using the
            delete_bulk method
            of the date_greater_than_filter_manager.
        3. Verify that the delete operation was successful by
            checking if the date_greater_than_filters no longer exist in the database.

        Expected Result:
        - The delete_bulk method should return True, indicating
            that the delete operation was successful.
        - The date_greater_than_filters should no longer exist in the database.

        """

        date_greater_than_filter1 = await DateGreaterThanFilterFactory.create_async(
            session=session)

        date_greater_than_filter2 = await DateGreaterThanFilterFactory.create_async(
            session=session)

        # Delete date_greater_than_filters
        date_greater_than_filter_ids = [date_greater_than_filter1.date_greater_than_filter_id, date_greater_than_filter2.date_greater_than_filter_id]
        result = await date_greater_than_filter_manager.delete_bulk(
            date_greater_than_filter_ids)

        assert result is True

        for date_greater_than_filter_id in date_greater_than_filter_ids:
            execute_result = await session.execute(
                select(DateGreaterThanFilter).filter(
                    DateGreaterThanFilter._date_greater_than_filter_id == date_greater_than_filter_id)  # type: ignore
            )
            fetched_date_greater_than_filter = execute_result.scalars().first()

            assert fetched_date_greater_than_filter is None

    @pytest.mark.asyncio
    async def test_delete_bulk_date_greater_than_filters_not_found(
        self,
        date_greater_than_filter_manager: DateGreaterThanFilterManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of deleting bulk
        date_greater_than_filters when some date_greater_than_filters are not found.

        Steps:
        1. Create a date_greater_than_filter using the
            DateGreaterThanFilterFactory.
        2. Assert that the created date_greater_than_filter
            is an instance of the
            DateGreaterThanFilter class.
        3. Define a list of date_greater_than_filter IDs to delete.
        4. Use pytest.raises to assert that an exception is
            raised when deleting the bulk date_greater_than_filters.
        5. Rollback the session to undo any changes made during the test.

        This test case ensures that the delete_bulk method of the
        DateGreaterThanFilterManager raises an exception
        when some date_greater_than_filters with the specified IDs are
        not found in the database.
        """
        date_greater_than_filter1 = await DateGreaterThanFilterFactory.create_async(
            session=session)

        assert isinstance(date_greater_than_filter1, DateGreaterThanFilter)

        # Delete date_greater_than_filters
        date_greater_than_filter_ids = [1, 2]

        with pytest.raises(Exception):
            await date_greater_than_filter_manager.delete_bulk(
                date_greater_than_filter_ids)

        await session.rollback()

    @pytest.mark.asyncio
    async def test_delete_bulk_empty_list(
        self,
        date_greater_than_filter_manager: DateGreaterThanFilterManager
    ):
        """
        Test case to verify the behavior of deleting
        date_greater_than_filters with an empty list.

        Args:
            date_greater_than_filter_manager (DateGreaterThanFilterManager): The
                instance of the
                DateGreaterThanFilterManager class.

        Returns:
            None

        Raises:
            AssertionError: If the result is not True.
        """

        # Delete date_greater_than_filters with an empty list
        date_greater_than_filter_ids = []
        result = await date_greater_than_filter_manager.delete_bulk(
            date_greater_than_filter_ids)

        # Assertions
        assert result is True

    @pytest.mark.asyncio
    async def test_delete_bulk_invalid_type(
        self,
        date_greater_than_filter_manager: DateGreaterThanFilterManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of the delete_bulk
        method when invalid date_greater_than_filter IDs are provided.

        Args:
            date_greater_than_filter_manager (DateGreaterThanFilterManager): The
                instance of the
                DateGreaterThanFilterManager class.
            session (AsyncSession): The async session object.

        Raises:
            Exception: If an exception is raised during the
                execution of the delete_bulk method.

        Returns:
            None
        """

        date_greater_than_filter_ids = ["1", 2]

        with pytest.raises(Exception):
            await date_greater_than_filter_manager.delete_bulk(
                date_greater_than_filter_ids)

        await session.rollback()
