# models/managers/tests/tac_test.py
# pylint: disable=protected-access
# pylint: disable=unused-argument
"""
    This class contains unit tests for the
    `TacManager` class.
"""

import logging
import uuid

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from helpers.session_context import SessionContext
from managers.tac import TacManager
from models import Tac
from models.factory import TacFactory

class TestTacBulkManager:
    """
    This class contains unit tests for the
    `TacManager` class.
    """

    @pytest_asyncio.fixture(scope="function")
    async def tac_manager(self, session: AsyncSession):
        """
        Fixture that returns an instance of
        `TacManager` for testing.
        """
        session_context = SessionContext(dict(), session)
        session_context.customer_code = uuid.uuid4()
        return TacManager(session_context)

    @pytest.mark.asyncio
    async def test_add_bulk(
        self,
        tac_manager: TacManager,
        session: AsyncSession
    ):
        """
        Test case for the `add_bulk` method of the
        `TacManager` class.

        This test case verifies that the `add_bulk`
        method correctly adds multiple tacs to the database.

        Steps:
        1. Generate a list of tac data using the
            `TacFactory.build_async` method.
        2. Call the `add_bulk` method of the
            `tac_manager` instance,
            passing in the
            generated tac data.
        3. Verify that the number of tacs
            returned is
            equal to the number of tacs added.
        4. For each updated tac, fetch the corresponding
            tac from the database.
        5. Verify that the fetched tac
            is an instance of the
            `Tac` class.
        6. Verify that the insert_user_id and
            last_update_user_id of the fetched
            tac match the
            customer code of the session context.
        7. Verify that the tac_id of the fetched
            tac matches the
            tac_id of the updated
            tac.

        """
        tacs_data = [
            await TacFactory.build_async(session) for _ in range(5)]

        tacs = await tac_manager.add_bulk(
            tacs_data)

        assert len(tacs) == 5

        for updated_tac in tacs:
            result = await session.execute(
                select(Tac).filter(
                    Tac._tac_id == updated_tac.tac_id  # type: ignore
                )
            )
            fetched_tac = result.scalars().first()

            assert isinstance(fetched_tac, Tac)

            assert str(fetched_tac.insert_user_id) == (
                str(tac_manager._session_context.customer_code))
            assert str(fetched_tac.last_update_user_id) == (
                str(tac_manager._session_context.customer_code))

            assert fetched_tac.tac_id == \
                updated_tac.tac_id

    @pytest.mark.asyncio
    async def test_update_bulk_success(
        self,
        tac_manager: TacManager,
        session: AsyncSession
    ):
        """
        Test case for bulk update of tacs.

        This test case verifies the functionality of the
        `update_bulk` method in the `TacManager` class.
        It creates two tac instances,
        updates their codes
        using the `update_bulk` method, and then verifies
        that the updates were successful by checking the
        updated codes in the database.

        Steps:
        1. Create two tac instances using the
            `TacFactory.create_async` method.
        2. Generate new codes for the tacs.
        3. Update the tacs' codes using the `update_bulk` method.
        4. Verify that the update was successful by checking
            the updated codes in the database.

        Args:
            tac_manager (TacManager): An instance of the
                `TacManager` class.
            session (AsyncSession): An instance of the `AsyncSession` class.

        Returns:
            None
        """
        # Mocking tac instances
        tac1 = await TacFactory.create_async(
            session=session)
        tac2 = await TacFactory.create_async(
            session=session)
        logging.info(tac1.__dict__)

        code_updated1 = uuid.uuid4()
        code_updated2 = uuid.uuid4()
        logging.info(code_updated1)
        logging.info(code_updated2)

        # Update tacs
        updates = [
            {
                "tac_id": tac1.tac_id,
                "code": code_updated1
            },
            {
                "tac_id": tac2.tac_id,
                "code": code_updated2
            }
        ]
        updated_tacs = await tac_manager.update_bulk(
            updates)

        logging.info('bulk update results')
        # Assertions
        assert len(updated_tacs) == 2
        logging.info(updated_tacs[0].__dict__)
        logging.info(updated_tacs[1].__dict__)

        logging.info('getall')
        tacs = await tac_manager.get_list()
        logging.info(tacs[0].__dict__)
        logging.info(tacs[1].__dict__)

        assert updated_tacs[0].code == code_updated1
        assert updated_tacs[1].code == code_updated2

        assert str(updated_tacs[0].last_update_user_id) == (
            str(tac_manager._session_context.customer_code))

        assert str(updated_tacs[1].last_update_user_id) == (
            str(tac_manager._session_context.customer_code))

        result = await session.execute(
            select(Tac).filter(
                Tac._tac_id == 1)  # type: ignore
        )
        fetched_tac = result.scalars().first()

        assert isinstance(fetched_tac, Tac)

        assert fetched_tac.code == code_updated1

        result = await session.execute(
            select(Tac).filter(
                Tac._tac_id == 2)  # type: ignore
        )
        fetched_tac = result.scalars().first()

        assert isinstance(fetched_tac, Tac)

        assert fetched_tac.code == code_updated2

    @pytest.mark.asyncio
    async def test_update_bulk_missing_tac_id(
        self,
        tac_manager: TacManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of the `update_bulk`
        method when the tac_id is missing.

        This test case ensures that when the tac_id is
        missing in the updates list,
        an exception is raised and the session is rolled back.

        Steps:
        1. Prepare the updates list with a missing tac_id.
        2. Call the `update_bulk` method with the updates list.
        3. Assert that an exception is raised.
        4. Rollback the session to undo any changes made during the test.

        """
        # No tacs to update since tac_id is missing
        updates = [{"name": "Red Rose"}]

        with pytest.raises(Exception):
            await tac_manager.update_bulk(updates)

        await session.rollback()

    @pytest.mark.asyncio
    async def test_update_bulk_tac_not_found(
        self,
        tac_manager: TacManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of the update_bulk
        method when a tac is not found.

        This test case performs the following steps:
        1. Defines a list of tac updates,
            where each update
            contains a tac_id and a code.
        2. Calls the update_bulk method of the
            tac_manager with the list of updates.
        3. Expects an exception to be raised, indicating that
            the tac was not found.
        4. Rolls back the session to undo any changes made during the test.

        Note: This test assumes that the update_bulk method
        throws an exception when a
        tac is not found.

        """

        # Update tacs
        updates = [{"tac_id": 1, "code": uuid.uuid4()}]

        with pytest.raises(Exception):
            await tac_manager.update_bulk(updates)

        await session.rollback()

    @pytest.mark.asyncio
    async def test_update_bulk_invalid_type(
        self,
        tac_manager: TacManager,
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

        :param tac_manager: An instance of the TacManager class.
        :param session: An instance of the AsyncSession class.
        """

        updates = [{"tac_id": "2", "code": uuid.uuid4()}]

        with pytest.raises(Exception):
            await tac_manager.update_bulk(updates)

        await session.rollback()

    @pytest.mark.asyncio
    async def test_delete_bulk_success(
        self,
        tac_manager: TacManager,
        session: AsyncSession
    ):
        """
        Test case for the delete_bulk method of the
        TacManager class.

        This test verifies that the delete_bulk method
        successfully deletes multiple tacs
        from the database.

        Steps:
        1. Create two tac objects
            using the TacFactory.
        2. Delete the tacs using the
            delete_bulk method
            of the tac_manager.
        3. Verify that the delete operation was successful by
            checking if the tacs no longer exist in the database.

        Expected Result:
        - The delete_bulk method should return True, indicating
            that the delete operation was successful.
        - The tacs should no longer exist in the database.

        """

        tac1 = await TacFactory.create_async(
            session=session)

        tac2 = await TacFactory.create_async(
            session=session)

        # Delete tacs
        tac_ids = [tac1.tac_id, tac2.tac_id]
        result = await tac_manager.delete_bulk(
            tac_ids)

        assert result is True

        for tac_id in tac_ids:
            execute_result = await session.execute(
                select(Tac).filter(
                    Tac._tac_id == tac_id)  # type: ignore
            )
            fetched_tac = execute_result.scalars().first()

            assert fetched_tac is None

    @pytest.mark.asyncio
    async def test_delete_bulk_tacs_not_found(
        self,
        tac_manager: TacManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of deleting bulk
        tacs when some tacs are not found.

        Steps:
        1. Create a tac using the
            TacFactory.
        2. Assert that the created tac
            is an instance of the
            Tac class.
        3. Define a list of tac IDs to delete.
        4. Use pytest.raises to assert that an exception is
            raised when deleting the bulk tacs.
        5. Rollback the session to undo any changes made during the test.

        This test case ensures that the delete_bulk method of the
        TacManager raises an exception
        when some tacs with the specified IDs are
        not found in the database.
        """
        tac1 = await TacFactory.create_async(
            session=session)

        assert isinstance(tac1, Tac)

        # Delete tacs
        tac_ids = [1, 2]

        with pytest.raises(Exception):
            await tac_manager.delete_bulk(
                tac_ids)

        await session.rollback()

    @pytest.mark.asyncio
    async def test_delete_bulk_empty_list(
        self,
        tac_manager: TacManager
    ):
        """
        Test case to verify the behavior of deleting
        tacs with an empty list.

        Args:
            tac_manager (TacManager): The
                instance of the
                TacManager class.

        Returns:
            None

        Raises:
            AssertionError: If the result is not True.
        """

        # Delete tacs with an empty list
        tac_ids = []
        result = await tac_manager.delete_bulk(
            tac_ids)

        # Assertions
        assert result is True

    @pytest.mark.asyncio
    async def test_delete_bulk_invalid_type(
        self,
        tac_manager: TacManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of the delete_bulk
        method when invalid tac IDs are provided.

        Args:
            tac_manager (TacManager): The
                instance of the
                TacManager class.
            session (AsyncSession): The async session object.

        Raises:
            Exception: If an exception is raised during the
                execution of the delete_bulk method.

        Returns:
            None
        """

        tac_ids = ["1", 2]

        with pytest.raises(Exception):
            await tac_manager.delete_bulk(
                tac_ids)

        await session.rollback()