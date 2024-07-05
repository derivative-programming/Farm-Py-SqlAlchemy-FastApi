# models/managers/tests/pac_test.py
# pylint: disable=protected-access
# pylint: disable=unused-argument
# pylint: disable=unused-import
"""
    This class contains unit tests for the
    `PacManager` class.
"""

import logging
import uuid  # noqa: F401

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from helpers.session_context import SessionContext
from managers.pac import (
    PacManager)
from models import Pac
from models.factory import (
    PacFactory)


class TestPacBulkManager:
    """
    This class contains unit tests for the
    `PacManager` class.
    """

    @pytest_asyncio.fixture(scope="function")
    async def obj_manager(self, session: AsyncSession):
        """
        Fixture that returns an instance of
        `PacManager` for testing.
        """
        session_context = SessionContext({}, session)
        session_context.customer_code = uuid.uuid4()
        return PacManager(session_context)

    @pytest.mark.asyncio
    async def test_add_bulk(
        self,
        obj_manager: PacManager,
        session: AsyncSession
    ):
        """
        Test case for the `add_bulk` method of the
        `PacManager` class.

        This test case verifies that the `add_bulk`
        method correctly adds multiple
        pacs to the database.

        Steps:
        1. Generate a list of pac data using the
            `PacFactory.build_async` method.
        2. Call the `add_bulk` method of the
            `obj_manager` instance,
            passing in the
            generated pac data.
        3. Verify that the number of pacs
            returned is
            equal to the number of pacs added.
        4. For each updated pac, fetch the corresponding
            pac from the database.
        5. Verify that the fetched pac
            is an instance of the
            `Pac` class.
        6. Verify that the insert_user_id and
            last_update_user_id of the fetched
            pac match the
            customer code of the session context.
        7. Verify that the pac_id of the fetched
            pac matches the
            pac_id of the updated
            pac.

        """
        pacs_data = [
            await PacFactory.build_async(session)
            for _ in range(5)]

        pacs = await obj_manager.add_bulk(
            pacs_data)

        assert len(pacs) == 5

        for updated_obj in pacs:
            result = await session.execute(
                select(Pac).filter(
                    Pac._pac_id == (
                        updated_obj.pac_id)  # type: ignore
                )
            )
            fetched_obj = result.scalars().first()

            assert isinstance(
                fetched_obj,
                Pac)

            assert str(fetched_obj.insert_user_id) == (
                str(obj_manager._session_context.customer_code))
            assert str(fetched_obj.last_update_user_id) == (
                str(obj_manager._session_context.customer_code))

            assert fetched_obj.pac_id == \
                updated_obj.pac_id

    @pytest.mark.asyncio
    async def test_update_bulk_success(
        self,
        obj_manager: PacManager,
        session: AsyncSession
    ):
        """
        Test case for bulk update of pacs.

        This test case verifies the functionality of the
        `update_bulk` method in the
        `PacManager` class.
        It creates two pac instances,
        updates their codes
        using the `update_bulk` method, and then verifies
        that the updates were successful by checking the
        updated codes in the database.

        Steps:
        1. Create two pac instances using the
            `PacFactory.create_async` method.
        2. Generate new codes for the pacs.
        3. Update the pacs' codes
            using the `update_bulk` method.
        4. Verify that the update was successful by checking
            the updated codes in the database.

        Args:
            obj_manager (PacManager):
                An instance of the
                `PacManager` class.
            session (AsyncSession): An instance of the `AsyncSession` class.

        Returns:
            None
        """
        # Mocking pac instances
        obj_1 = await PacFactory. \
            create_async(
                session=session)
        obj_2 = await PacFactory. \
            create_async(
                session=session)
        logging.info(obj_1.__dict__)

        code_updated1 = uuid.uuid4()
        code_updated2 = uuid.uuid4()
        logging.info(code_updated1)
        logging.info(code_updated2)

        # Update pacs
        updates = [
            {
                "pac_id":
                    obj_1.pac_id,
                "code": code_updated1
            },
            {
                "pac_id":
                    obj_2.pac_id,
                "code": code_updated2
            }
        ]
        updated_pacs = await obj_manager.update_bulk(
            updates)

        logging.info('bulk update results')
        # Assertions
        assert len(updated_pacs) == 2
        logging.info(updated_pacs[0]
                     .__dict__)
        logging.info(updated_pacs[1]
                     .__dict__)

        logging.info('getall')
        pacs = await obj_manager.get_list()
        logging.info(pacs[0]
                     .__dict__)
        logging.info(pacs[1]
                     .__dict__)

        assert updated_pacs[0].code == \
            code_updated1
        assert updated_pacs[1].code == \
            code_updated2

        assert str(updated_pacs[0]
                   .last_update_user_id) == (
            str(obj_manager
                ._session_context.customer_code))

        assert str(updated_pacs[1]
                   .last_update_user_id) == (
            str(obj_manager
                ._session_context.customer_code))

        result = await session.execute(
            select(Pac).filter(
                Pac._pac_id == 1)  # type: ignore
        )
        fetched_obj = result.scalars().first()

        assert isinstance(fetched_obj,
                          Pac)

        assert fetched_obj.code == code_updated1

        result = await session.execute(
            select(Pac).filter(
                Pac._pac_id == 2)  # type: ignore
        )
        fetched_obj = result.scalars().first()

        assert isinstance(fetched_obj,
                          Pac)

        assert fetched_obj.code == code_updated2

    @pytest.mark.asyncio
    async def test_update_bulk_missing_pac_id(
        self,
        obj_manager: PacManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of the `update_bulk`
        method when the pac_id is missing.

        This test case ensures that when the pac_id is
        missing in the updates list,
        an exception is raised and the session is rolled back.

        Steps:
        1. Prepare the updates list with a missing pac_id.
        2. Call the `update_bulk` method with the updates list.
        3. Assert that an exception is raised.
        4. Rollback the session to undo any changes made during the test.

        """
        # No pacs to update since
        # pac_id is missing
        updates = [{"name": "Red Rose"}]

        with pytest.raises(Exception):
            await obj_manager.update_bulk(updates)

        await session.rollback()

    @pytest.mark.asyncio
    async def test_update_bulk_pac_not_found(
        self,
        obj_manager: PacManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of the update_bulk
        method when a pac is not found.

        This test case performs the following steps:
        1. Defines a list of pac updates,
            where each update
            contains a pac_id and a code.
        2. Calls the update_bulk method of the
            obj_manager with the list of updates.
        3. Expects an exception to be raised, indicating that
            the pac was not found.
        4. Rolls back the session to undo any changes made during the test.

        Note: This test assumes that the update_bulk method
        throws an exception when a
        pac is not found.

        """

        # Update pacs
        updates = [{"pac_id": 1, "code": uuid.uuid4()}]

        with pytest.raises(Exception):
            await obj_manager.update_bulk(updates)

        await session.rollback()

    @pytest.mark.asyncio
    async def test_update_bulk_invalid_type(
        self,
        obj_manager: PacManager,
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

        :param obj_manager: An instance of the
            PacManager class.
        :param session: An instance of the AsyncSession class.
        """

        updates = [{"pac_id": "2", "code": uuid.uuid4()}]

        with pytest.raises(Exception):
            await obj_manager.update_bulk(updates)

        await session.rollback()

    @pytest.mark.asyncio
    async def test_delete_bulk_success(
        self,
        obj_manager: PacManager,
        session: AsyncSession
    ):
        """
        Test case for the delete_bulk method of the
        PacManager class.

        This test verifies that the delete_bulk method
        successfully deletes multiple pacs
        from the database.

        Steps:
        1. Create two pac objects
            using the PacFactory.
        2. Delete the pacs using the
            delete_bulk method
            of the obj_manager.
        3. Verify that the delete operation was successful by
            checking if the pacs
            no longer exist in the database.

        Expected Result:
        - The delete_bulk method should return True, indicating
            that the delete operation was successful.
        - The pacs should
            no longer exist in the database.

        """

        obj_1 = await PacFactory.create_async(
            session=session)

        obj_2 = await PacFactory.create_async(
            session=session)

        # Delete pacs
        pac_ids = [
            obj_1.pac_id,
            obj_2.pac_id
        ]
        result = await obj_manager.delete_bulk(
            pac_ids)

        assert result is True

        for pac_id in pac_ids:
            execute_result = await session.execute(
                select(Pac).filter(
                    Pac._pac_id == (
                        pac_id))  # type: ignore
            )
            fetched_obj = execute_result.scalars().first()

            assert fetched_obj is None

    @pytest.mark.asyncio
    async def test_delete_bulk_pacs_not_found(
        self,
        obj_manager: PacManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of deleting bulk
        pacs when some
        pacs are not found.

        Steps:
        1. Create a pac using the
            PacFactory.
        2. Assert that the created pac
            is an instance of the
            Pac class.
        3. Define a list of pac IDs to delete.
        4. Use pytest.raises to assert that an exception is
            raised when deleting the bulk pacs.
        5. Rollback the session to undo any changes made during the test.

        This test case ensures that the delete_bulk method of the
        PacManager raises an exception
        when some pacs with the specified IDs are
        not found in the database.
        """
        obj_1 = await PacFactory.create_async(
            session=session)

        assert isinstance(obj_1,
                          Pac)

        # Delete pacs
        pac_ids = [1, 2]

        with pytest.raises(Exception):
            await obj_manager.delete_bulk(
                pac_ids)

        await session.rollback()

    @pytest.mark.asyncio
    async def test_delete_bulk_empty_list(
        self,
        obj_manager: PacManager
    ):
        """
        Test case to verify the behavior of deleting
        pacs with an empty list.

        Args:
            obj_manager (PacManager): The
                instance of the
                PacManager class.

        Returns:
            None

        Raises:
            AssertionError: If the result is not True.
        """

        # Delete pacs with an empty list
        pac_ids = []
        result = await obj_manager.delete_bulk(
            pac_ids)

        # Assertions
        assert result is True

    @pytest.mark.asyncio
    async def test_delete_bulk_invalid_type(
        self,
        obj_manager: PacManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of the delete_bulk
        method when invalid pac IDs are provided.

        Args:
            obj_manager (PacManager): The
                instance of the
                PacManager class.
            session (AsyncSession): The async session object.

        Raises:
            Exception: If an exception is raised during the
                execution of the delete_bulk method.

        Returns:
            None
        """

        pac_ids = ["1", 2]

        with pytest.raises(Exception):
            await obj_manager.delete_bulk(
                pac_ids)

        await session.rollback()
