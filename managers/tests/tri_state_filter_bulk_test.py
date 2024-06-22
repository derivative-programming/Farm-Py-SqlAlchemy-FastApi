# models/managers/tests/tri_state_filter_test.py
# pylint: disable=protected-access
# pylint: disable=unused-argument
"""
    This class contains unit tests for the
    `TriStateFilterManager` class.
"""

import logging
import uuid

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from helpers.session_context import SessionContext
from managers.tri_state_filter import TriStateFilterManager
from models import TriStateFilter
from models.factory import TriStateFilterFactory

class TestTriStateFilterBulkManager:
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
    async def test_add_bulk(
        self,
        tri_state_filter_manager: TriStateFilterManager,
        session: AsyncSession
    ):
        """
        Test case for the `add_bulk` method of the
        `TriStateFilterManager` class.

        This test case verifies that the `add_bulk`
        method correctly adds multiple
        tri_state_filters to the database.

        Steps:
        1. Generate a list of tri_state_filter data using the
            `TriStateFilterFactory.build_async` method.
        2. Call the `add_bulk` method of the
            `tri_state_filter_manager` instance,
            passing in the
            generated tri_state_filter data.
        3. Verify that the number of tri_state_filters
            returned is
            equal to the number of tri_state_filters added.
        4. For each updated tri_state_filter, fetch the corresponding
            tri_state_filter from the database.
        5. Verify that the fetched tri_state_filter
            is an instance of the
            `TriStateFilter` class.
        6. Verify that the insert_user_id and
            last_update_user_id of the fetched
            tri_state_filter match the
            customer code of the session context.
        7. Verify that the tri_state_filter_id of the fetched
            tri_state_filter matches the
            tri_state_filter_id of the updated
            tri_state_filter.

        """
        tri_state_filters_data = [
            await TriStateFilterFactory.build_async(session) for _ in range(5)]

        tri_state_filters = await tri_state_filter_manager.add_bulk(
            tri_state_filters_data)

        assert len(tri_state_filters) == 5

        for updated_tri_state_filter in tri_state_filters:
            result = await session.execute(
                select(TriStateFilter).filter(
                    TriStateFilter._tri_state_filter_id == updated_tri_state_filter.tri_state_filter_id  # type: ignore
                )
            )
            fetched_tri_state_filter = result.scalars().first()

            assert isinstance(
                fetched_tri_state_filter, TriStateFilter)

            assert str(fetched_tri_state_filter.insert_user_id) == (
                str(tri_state_filter_manager._session_context.customer_code))
            assert str(fetched_tri_state_filter.last_update_user_id) == (
                str(tri_state_filter_manager._session_context.customer_code))

            assert fetched_tri_state_filter.tri_state_filter_id == \
                updated_tri_state_filter.tri_state_filter_id

    @pytest.mark.asyncio
    async def test_update_bulk_success(
        self,
        tri_state_filter_manager: TriStateFilterManager,
        session: AsyncSession
    ):
        """
        Test case for bulk update of tri_state_filters.

        This test case verifies the functionality of the
        `update_bulk` method in the
        `TriStateFilterManager` class.
        It creates two tri_state_filter instances,
        updates their codes
        using the `update_bulk` method, and then verifies
        that the updates were successful by checking the
        updated codes in the database.

        Steps:
        1. Create two tri_state_filter instances using the
            `TriStateFilterFactory.create_async` method.
        2. Generate new codes for the tri_state_filters.
        3. Update the tri_state_filters' codes
            using the `update_bulk` method.
        4. Verify that the update was successful by checking
            the updated codes in the database.

        Args:
            tri_state_filter_manager (TriStateFilterManager):
                An instance of the
                `TriStateFilterManager` class.
            session (AsyncSession): An instance of the `AsyncSession` class.

        Returns:
            None
        """
        # Mocking tri_state_filter instances
        tri_state_filter1 = await TriStateFilterFactory. \
            create_async(
                session=session)
        tri_state_filter2 = await TriStateFilterFactory. \
            create_async(
                session=session)
        logging.info(tri_state_filter1.__dict__)

        code_updated1 = uuid.uuid4()
        code_updated2 = uuid.uuid4()
        logging.info(code_updated1)
        logging.info(code_updated2)

        # Update tri_state_filters
        updates = [
            {
                "tri_state_filter_id":
                    tri_state_filter1.tri_state_filter_id,
                "code": code_updated1
            },
            {
                "tri_state_filter_id":
                    tri_state_filter2.tri_state_filter_id,
                "code": code_updated2
            }
        ]
        updated_tri_state_filters = await tri_state_filter_manager.update_bulk(
            updates)

        logging.info('bulk update results')
        # Assertions
        assert len(updated_tri_state_filters) == 2
        logging.info(updated_tri_state_filters[0].__dict__)
        logging.info(updated_tri_state_filters[1].__dict__)

        logging.info('getall')
        tri_state_filters = await tri_state_filter_manager.get_list()
        logging.info(tri_state_filters[0].__dict__)
        logging.info(tri_state_filters[1].__dict__)

        assert updated_tri_state_filters[0].code == code_updated1
        assert updated_tri_state_filters[1].code == code_updated2

        assert str(updated_tri_state_filters[0].last_update_user_id) == (
            str(tri_state_filter_manager._session_context.customer_code))

        assert str(updated_tri_state_filters[1].last_update_user_id) == (
            str(tri_state_filter_manager._session_context.customer_code))

        result = await session.execute(
            select(TriStateFilter).filter(
                TriStateFilter._tri_state_filter_id == 1)  # type: ignore
        )
        fetched_tri_state_filter = result.scalars().first()

        assert isinstance(fetched_tri_state_filter, TriStateFilter)

        assert fetched_tri_state_filter.code == code_updated1

        result = await session.execute(
            select(TriStateFilter).filter(
                TriStateFilter._tri_state_filter_id == 2)  # type: ignore
        )
        fetched_tri_state_filter = result.scalars().first()

        assert isinstance(fetched_tri_state_filter, TriStateFilter)

        assert fetched_tri_state_filter.code == code_updated2

    @pytest.mark.asyncio
    async def test_update_bulk_missing_tri_state_filter_id(
        self,
        tri_state_filter_manager: TriStateFilterManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of the `update_bulk`
        method when the tri_state_filter_id is missing.

        This test case ensures that when the tri_state_filter_id is
        missing in the updates list,
        an exception is raised and the session is rolled back.

        Steps:
        1. Prepare the updates list with a missing tri_state_filter_id.
        2. Call the `update_bulk` method with the updates list.
        3. Assert that an exception is raised.
        4. Rollback the session to undo any changes made during the test.

        """
        # No tri_state_filters to update since tri_state_filter_id is missing
        updates = [{"name": "Red Rose"}]

        with pytest.raises(Exception):
            await tri_state_filter_manager.update_bulk(updates)

        await session.rollback()

    @pytest.mark.asyncio
    async def test_update_bulk_tri_state_filter_not_found(
        self,
        tri_state_filter_manager: TriStateFilterManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of the update_bulk
        method when a tri_state_filter is not found.

        This test case performs the following steps:
        1. Defines a list of tri_state_filter updates,
            where each update
            contains a tri_state_filter_id and a code.
        2. Calls the update_bulk method of the
            tri_state_filter_manager with the list of updates.
        3. Expects an exception to be raised, indicating that
            the tri_state_filter was not found.
        4. Rolls back the session to undo any changes made during the test.

        Note: This test assumes that the update_bulk method
        throws an exception when a
        tri_state_filter is not found.

        """

        # Update tri_state_filters
        updates = [{"tri_state_filter_id": 1, "code": uuid.uuid4()}]

        with pytest.raises(Exception):
            await tri_state_filter_manager.update_bulk(updates)

        await session.rollback()

    @pytest.mark.asyncio
    async def test_update_bulk_invalid_type(
        self,
        tri_state_filter_manager: TriStateFilterManager,
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

        :param tri_state_filter_manager: An instance of the TriStateFilterManager class.
        :param session: An instance of the AsyncSession class.
        """

        updates = [{"tri_state_filter_id": "2", "code": uuid.uuid4()}]

        with pytest.raises(Exception):
            await tri_state_filter_manager.update_bulk(updates)

        await session.rollback()

    @pytest.mark.asyncio
    async def test_delete_bulk_success(
        self,
        tri_state_filter_manager: TriStateFilterManager,
        session: AsyncSession
    ):
        """
        Test case for the delete_bulk method of the
        TriStateFilterManager class.

        This test verifies that the delete_bulk method
        successfully deletes multiple tri_state_filters
        from the database.

        Steps:
        1. Create two tri_state_filter objects
            using the TriStateFilterFactory.
        2. Delete the tri_state_filters using the
            delete_bulk method
            of the tri_state_filter_manager.
        3. Verify that the delete operation was successful by
            checking if the tri_state_filters no longer exist in the database.

        Expected Result:
        - The delete_bulk method should return True, indicating
            that the delete operation was successful.
        - The tri_state_filters should no longer exist in the database.

        """

        tri_state_filter1 = await TriStateFilterFactory.create_async(
            session=session)

        tri_state_filter2 = await TriStateFilterFactory.create_async(
            session=session)

        # Delete tri_state_filters
        tri_state_filter_ids = [tri_state_filter1.tri_state_filter_id, tri_state_filter2.tri_state_filter_id]
        result = await tri_state_filter_manager.delete_bulk(
            tri_state_filter_ids)

        assert result is True

        for tri_state_filter_id in tri_state_filter_ids:
            execute_result = await session.execute(
                select(TriStateFilter).filter(
                    TriStateFilter._tri_state_filter_id == tri_state_filter_id)  # type: ignore
            )
            fetched_tri_state_filter = execute_result.scalars().first()

            assert fetched_tri_state_filter is None

    @pytest.mark.asyncio
    async def test_delete_bulk_tri_state_filters_not_found(
        self,
        tri_state_filter_manager: TriStateFilterManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of deleting bulk
        tri_state_filters when some tri_state_filters are not found.

        Steps:
        1. Create a tri_state_filter using the
            TriStateFilterFactory.
        2. Assert that the created tri_state_filter
            is an instance of the
            TriStateFilter class.
        3. Define a list of tri_state_filter IDs to delete.
        4. Use pytest.raises to assert that an exception is
            raised when deleting the bulk tri_state_filters.
        5. Rollback the session to undo any changes made during the test.

        This test case ensures that the delete_bulk method of the
        TriStateFilterManager raises an exception
        when some tri_state_filters with the specified IDs are
        not found in the database.
        """
        tri_state_filter1 = await TriStateFilterFactory.create_async(
            session=session)

        assert isinstance(tri_state_filter1, TriStateFilter)

        # Delete tri_state_filters
        tri_state_filter_ids = [1, 2]

        with pytest.raises(Exception):
            await tri_state_filter_manager.delete_bulk(
                tri_state_filter_ids)

        await session.rollback()

    @pytest.mark.asyncio
    async def test_delete_bulk_empty_list(
        self,
        tri_state_filter_manager: TriStateFilterManager
    ):
        """
        Test case to verify the behavior of deleting
        tri_state_filters with an empty list.

        Args:
            tri_state_filter_manager (TriStateFilterManager): The
                instance of the
                TriStateFilterManager class.

        Returns:
            None

        Raises:
            AssertionError: If the result is not True.
        """

        # Delete tri_state_filters with an empty list
        tri_state_filter_ids = []
        result = await tri_state_filter_manager.delete_bulk(
            tri_state_filter_ids)

        # Assertions
        assert result is True

    @pytest.mark.asyncio
    async def test_delete_bulk_invalid_type(
        self,
        tri_state_filter_manager: TriStateFilterManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of the delete_bulk
        method when invalid tri_state_filter IDs are provided.

        Args:
            tri_state_filter_manager (TriStateFilterManager): The
                instance of the
                TriStateFilterManager class.
            session (AsyncSession): The async session object.

        Raises:
            Exception: If an exception is raised during the
                execution of the delete_bulk method.

        Returns:
            None
        """

        tri_state_filter_ids = ["1", 2]

        with pytest.raises(Exception):
            await tri_state_filter_manager.delete_bulk(
                tri_state_filter_ids)

        await session.rollback()
