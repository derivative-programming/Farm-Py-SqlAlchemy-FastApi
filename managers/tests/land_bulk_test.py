# models/managers/tests/land_test.py
# pylint: disable=protected-access
# pylint: disable=unused-argument
"""
    This class contains unit tests for the
    `LandManager` class.
"""

import logging
import uuid

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from helpers.session_context import SessionContext
from managers.land import LandManager
from models import Land
from models.factory import LandFactory

class TestLandBulkManager:
    """
    This class contains unit tests for the
    `LandManager` class.
    """

    @pytest_asyncio.fixture(scope="function")
    async def land_manager(self, session: AsyncSession):
        """
        Fixture that returns an instance of
        `LandManager` for testing.
        """
        session_context = SessionContext(dict(), session)
        session_context.customer_code = uuid.uuid4()
        return LandManager(session_context)

    @pytest.mark.asyncio
    async def test_add_bulk(
        self,
        land_manager: LandManager,
        session: AsyncSession
    ):
        """
        Test case for the `add_bulk` method of the
        `LandManager` class.

        This test case verifies that the `add_bulk`
        method correctly adds multiple
        lands to the database.

        Steps:
        1. Generate a list of land data using the
            `LandFactory.build_async` method.
        2. Call the `add_bulk` method of the
            `land_manager` instance,
            passing in the
            generated land data.
        3. Verify that the number of lands
            returned is
            equal to the number of lands added.
        4. For each updated land, fetch the corresponding
            land from the database.
        5. Verify that the fetched land
            is an instance of the
            `Land` class.
        6. Verify that the insert_user_id and
            last_update_user_id of the fetched
            land match the
            customer code of the session context.
        7. Verify that the land_id of the fetched
            land matches the
            land_id of the updated
            land.

        """
        lands_data = [
            await LandFactory.build_async(session) for _ in range(5)]

        lands = await land_manager.add_bulk(
            lands_data)

        assert len(lands) == 5

        for updated_land in lands:
            result = await session.execute(
                select(Land).filter(
                    Land._land_id == updated_land.land_id  # type: ignore
                )
            )
            fetched_land = result.scalars().first()

            assert isinstance(
                fetched_land, Land)

            assert str(fetched_land.insert_user_id) == (
                str(land_manager._session_context.customer_code))
            assert str(fetched_land.last_update_user_id) == (
                str(land_manager._session_context.customer_code))

            assert fetched_land.land_id == \
                updated_land.land_id

    @pytest.mark.asyncio
    async def test_update_bulk_success(
        self,
        land_manager: LandManager,
        session: AsyncSession
    ):
        """
        Test case for bulk update of lands.

        This test case verifies the functionality of the
        `update_bulk` method in the
        `LandManager` class.
        It creates two land instances,
        updates their codes
        using the `update_bulk` method, and then verifies
        that the updates were successful by checking the
        updated codes in the database.

        Steps:
        1. Create two land instances using the
            `LandFactory.create_async` method.
        2. Generate new codes for the lands.
        3. Update the lands' codes
            using the `update_bulk` method.
        4. Verify that the update was successful by checking
            the updated codes in the database.

        Args:
            land_manager (LandManager):
                An instance of the
                `LandManager` class.
            session (AsyncSession): An instance of the `AsyncSession` class.

        Returns:
            None
        """
        # Mocking land instances
        land1 = await LandFactory. \
            create_async(
                session=session)
        land2 = await LandFactory. \
            create_async(
                session=session)
        logging.info(land1.__dict__)

        code_updated1 = uuid.uuid4()
        code_updated2 = uuid.uuid4()
        logging.info(code_updated1)
        logging.info(code_updated2)

        # Update lands
        updates = [
            {
                "land_id":
                    land1.land_id,
                "code": code_updated1
            },
            {
                "land_id":
                    land2.land_id,
                "code": code_updated2
            }
        ]
        updated_lands = await land_manager.update_bulk(
            updates)

        logging.info('bulk update results')
        # Assertions
        assert len(updated_lands) == 2
        logging.info(updated_lands[0].__dict__)
        logging.info(updated_lands[1].__dict__)

        logging.info('getall')
        lands = await land_manager.get_list()
        logging.info(lands[0].__dict__)
        logging.info(lands[1].__dict__)

        assert updated_lands[0].code == code_updated1
        assert updated_lands[1].code == code_updated2

        assert str(updated_lands[0].last_update_user_id) == (
            str(land_manager._session_context.customer_code))

        assert str(updated_lands[1].last_update_user_id) == (
            str(land_manager._session_context.customer_code))

        result = await session.execute(
            select(Land).filter(
                Land._land_id == 1)  # type: ignore
        )
        fetched_land = result.scalars().first()

        assert isinstance(fetched_land, Land)

        assert fetched_land.code == code_updated1

        result = await session.execute(
            select(Land).filter(
                Land._land_id == 2)  # type: ignore
        )
        fetched_land = result.scalars().first()

        assert isinstance(fetched_land, Land)

        assert fetched_land.code == code_updated2

    @pytest.mark.asyncio
    async def test_update_bulk_missing_land_id(
        self,
        land_manager: LandManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of the `update_bulk`
        method when the land_id is missing.

        This test case ensures that when the land_id is
        missing in the updates list,
        an exception is raised and the session is rolled back.

        Steps:
        1. Prepare the updates list with a missing land_id.
        2. Call the `update_bulk` method with the updates list.
        3. Assert that an exception is raised.
        4. Rollback the session to undo any changes made during the test.

        """
        # No lands to update since land_id is missing
        updates = [{"name": "Red Rose"}]

        with pytest.raises(Exception):
            await land_manager.update_bulk(updates)

        await session.rollback()

    @pytest.mark.asyncio
    async def test_update_bulk_land_not_found(
        self,
        land_manager: LandManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of the update_bulk
        method when a land is not found.

        This test case performs the following steps:
        1. Defines a list of land updates,
            where each update
            contains a land_id and a code.
        2. Calls the update_bulk method of the
            land_manager with the list of updates.
        3. Expects an exception to be raised, indicating that
            the land was not found.
        4. Rolls back the session to undo any changes made during the test.

        Note: This test assumes that the update_bulk method
        throws an exception when a
        land is not found.

        """

        # Update lands
        updates = [{"land_id": 1, "code": uuid.uuid4()}]

        with pytest.raises(Exception):
            await land_manager.update_bulk(updates)

        await session.rollback()

    @pytest.mark.asyncio
    async def test_update_bulk_invalid_type(
        self,
        land_manager: LandManager,
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

        :param land_manager: An instance of the LandManager class.
        :param session: An instance of the AsyncSession class.
        """

        updates = [{"land_id": "2", "code": uuid.uuid4()}]

        with pytest.raises(Exception):
            await land_manager.update_bulk(updates)

        await session.rollback()

    @pytest.mark.asyncio
    async def test_delete_bulk_success(
        self,
        land_manager: LandManager,
        session: AsyncSession
    ):
        """
        Test case for the delete_bulk method of the
        LandManager class.

        This test verifies that the delete_bulk method
        successfully deletes multiple lands
        from the database.

        Steps:
        1. Create two land objects
            using the LandFactory.
        2. Delete the lands using the
            delete_bulk method
            of the land_manager.
        3. Verify that the delete operation was successful by
            checking if the lands no longer exist in the database.

        Expected Result:
        - The delete_bulk method should return True, indicating
            that the delete operation was successful.
        - The lands should no longer exist in the database.

        """

        land1 = await LandFactory.create_async(
            session=session)

        land2 = await LandFactory.create_async(
            session=session)

        # Delete lands
        land_ids = [land1.land_id, land2.land_id]
        result = await land_manager.delete_bulk(
            land_ids)

        assert result is True

        for land_id in land_ids:
            execute_result = await session.execute(
                select(Land).filter(
                    Land._land_id == land_id)  # type: ignore
            )
            fetched_land = execute_result.scalars().first()

            assert fetched_land is None

    @pytest.mark.asyncio
    async def test_delete_bulk_lands_not_found(
        self,
        land_manager: LandManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of deleting bulk
        lands when some lands are not found.

        Steps:
        1. Create a land using the
            LandFactory.
        2. Assert that the created land
            is an instance of the
            Land class.
        3. Define a list of land IDs to delete.
        4. Use pytest.raises to assert that an exception is
            raised when deleting the bulk lands.
        5. Rollback the session to undo any changes made during the test.

        This test case ensures that the delete_bulk method of the
        LandManager raises an exception
        when some lands with the specified IDs are
        not found in the database.
        """
        land1 = await LandFactory.create_async(
            session=session)

        assert isinstance(land1, Land)

        # Delete lands
        land_ids = [1, 2]

        with pytest.raises(Exception):
            await land_manager.delete_bulk(
                land_ids)

        await session.rollback()

    @pytest.mark.asyncio
    async def test_delete_bulk_empty_list(
        self,
        land_manager: LandManager
    ):
        """
        Test case to verify the behavior of deleting
        lands with an empty list.

        Args:
            land_manager (LandManager): The
                instance of the
                LandManager class.

        Returns:
            None

        Raises:
            AssertionError: If the result is not True.
        """

        # Delete lands with an empty list
        land_ids = []
        result = await land_manager.delete_bulk(
            land_ids)

        # Assertions
        assert result is True

    @pytest.mark.asyncio
    async def test_delete_bulk_invalid_type(
        self,
        land_manager: LandManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of the delete_bulk
        method when invalid land IDs are provided.

        Args:
            land_manager (LandManager): The
                instance of the
                LandManager class.
            session (AsyncSession): The async session object.

        Raises:
            Exception: If an exception is raised during the
                execution of the delete_bulk method.

        Returns:
            None
        """

        land_ids = ["1", 2]

        with pytest.raises(Exception):
            await land_manager.delete_bulk(
                land_ids)

        await session.rollback()
