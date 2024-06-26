# models/managers/tests/flavor_test.py
# pylint: disable=protected-access
# pylint: disable=unused-argument
# pylint: disable=unused-import
"""
    This class contains unit tests for the
    `FlavorManager` class.
"""

import logging
import uuid  # noqa: F401

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from helpers.session_context import SessionContext
from managers.flavor import (
    FlavorManager)
from models import Flavor
from models.factory import (
    FlavorFactory)


class TestFlavorBulkManager:
    """
    This class contains unit tests for the
    `FlavorManager` class.
    """

    @pytest_asyncio.fixture(scope="function")
    async def obj_manager(self, session: AsyncSession):
        """
        Fixture that returns an instance of
        `FlavorManager` for testing.
        """
        session_context = SessionContext(dict(), session)
        session_context.customer_code = uuid.uuid4()
        return FlavorManager(session_context)

    @pytest.mark.asyncio
    async def test_add_bulk(
        self,
        obj_manager: FlavorManager,
        session: AsyncSession
    ):
        """
        Test case for the `add_bulk` method of the
        `FlavorManager` class.

        This test case verifies that the `add_bulk`
        method correctly adds multiple
        flavors to the database.

        Steps:
        1. Generate a list of flavor data using the
            `FlavorFactory.build_async` method.
        2. Call the `add_bulk` method of the
            `obj_manager` instance,
            passing in the
            generated flavor data.
        3. Verify that the number of flavors
            returned is
            equal to the number of flavors added.
        4. For each updated flavor, fetch the corresponding
            flavor from the database.
        5. Verify that the fetched flavor
            is an instance of the
            `Flavor` class.
        6. Verify that the insert_user_id and
            last_update_user_id of the fetched
            flavor match the
            customer code of the session context.
        7. Verify that the flavor_id of the fetched
            flavor matches the
            flavor_id of the updated
            flavor.

        """
        flavors_data = [
            await FlavorFactory.build_async(session)
            for _ in range(5)]

        flavors = await obj_manager.add_bulk(
            flavors_data)

        assert len(flavors) == 5

        for updated_obj in flavors:
            result = await session.execute(
                select(Flavor).filter(
                    Flavor._flavor_id == (
                        updated_obj.flavor_id)  # type: ignore
                )
            )
            fetched_obj = result.scalars().first()

            assert isinstance(
                fetched_obj,
                Flavor)

            assert str(fetched_obj.insert_user_id) == (
                str(obj_manager._session_context.customer_code))
            assert str(fetched_obj.last_update_user_id) == (
                str(obj_manager._session_context.customer_code))

            assert fetched_obj.flavor_id == \
                updated_obj.flavor_id

    @pytest.mark.asyncio
    async def test_update_bulk_success(
        self,
        obj_manager: FlavorManager,
        session: AsyncSession
    ):
        """
        Test case for bulk update of flavors.

        This test case verifies the functionality of the
        `update_bulk` method in the
        `FlavorManager` class.
        It creates two flavor instances,
        updates their codes
        using the `update_bulk` method, and then verifies
        that the updates were successful by checking the
        updated codes in the database.

        Steps:
        1. Create two flavor instances using the
            `FlavorFactory.create_async` method.
        2. Generate new codes for the flavors.
        3. Update the flavors' codes
            using the `update_bulk` method.
        4. Verify that the update was successful by checking
            the updated codes in the database.

        Args:
            obj_manager (FlavorManager):
                An instance of the
                `FlavorManager` class.
            session (AsyncSession): An instance of the `AsyncSession` class.

        Returns:
            None
        """
        # Mocking flavor instances
        obj_1 = await FlavorFactory. \
            create_async(
                session=session)
        obj_2 = await FlavorFactory. \
            create_async(
                session=session)
        logging.info(obj_1.__dict__)

        code_updated1 = uuid.uuid4()
        code_updated2 = uuid.uuid4()
        logging.info(code_updated1)
        logging.info(code_updated2)

        # Update flavors
        updates = [
            {
                "flavor_id":
                    obj_1.flavor_id,
                "code": code_updated1
            },
            {
                "flavor_id":
                    obj_2.flavor_id,
                "code": code_updated2
            }
        ]
        updated_flavors = await obj_manager.update_bulk(
            updates)

        logging.info('bulk update results')
        # Assertions
        assert len(updated_flavors) == 2
        logging.info(updated_flavors[0]
                     .__dict__)
        logging.info(updated_flavors[1]
                     .__dict__)

        logging.info('getall')
        flavors = await obj_manager.get_list()
        logging.info(flavors[0]
                     .__dict__)
        logging.info(flavors[1]
                     .__dict__)

        assert updated_flavors[0].code == \
            code_updated1
        assert updated_flavors[1].code == \
            code_updated2

        assert str(updated_flavors[0]
                   .last_update_user_id) == (
            str(obj_manager
                ._session_context.customer_code))

        assert str(updated_flavors[1]
                   .last_update_user_id) == (
            str(obj_manager
                ._session_context.customer_code))

        result = await session.execute(
            select(Flavor).filter(
                Flavor._flavor_id == 1)  # type: ignore
        )
        fetched_obj = result.scalars().first()

        assert isinstance(fetched_obj,
                          Flavor)

        assert fetched_obj.code == code_updated1

        result = await session.execute(
            select(Flavor).filter(
                Flavor._flavor_id == 2)  # type: ignore
        )
        fetched_obj = result.scalars().first()

        assert isinstance(fetched_obj,
                          Flavor)

        assert fetched_obj.code == code_updated2

    @pytest.mark.asyncio
    async def test_update_bulk_missing_flavor_id(
        self,
        obj_manager: FlavorManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of the `update_bulk`
        method when the flavor_id is missing.

        This test case ensures that when the flavor_id is
        missing in the updates list,
        an exception is raised and the session is rolled back.

        Steps:
        1. Prepare the updates list with a missing flavor_id.
        2. Call the `update_bulk` method with the updates list.
        3. Assert that an exception is raised.
        4. Rollback the session to undo any changes made during the test.

        """
        # No flavors to update since
        # flavor_id is missing
        updates = [{"name": "Red Rose"}]

        with pytest.raises(Exception):
            await obj_manager.update_bulk(updates)

        await session.rollback()

    @pytest.mark.asyncio
    async def test_update_bulk_flavor_not_found(
        self,
        obj_manager: FlavorManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of the update_bulk
        method when a flavor is not found.

        This test case performs the following steps:
        1. Defines a list of flavor updates,
            where each update
            contains a flavor_id and a code.
        2. Calls the update_bulk method of the
            obj_manager with the list of updates.
        3. Expects an exception to be raised, indicating that
            the flavor was not found.
        4. Rolls back the session to undo any changes made during the test.

        Note: This test assumes that the update_bulk method
        throws an exception when a
        flavor is not found.

        """

        # Update flavors
        updates = [{"flavor_id": 1, "code": uuid.uuid4()}]

        with pytest.raises(Exception):
            await obj_manager.update_bulk(updates)

        await session.rollback()

    @pytest.mark.asyncio
    async def test_update_bulk_invalid_type(
        self,
        obj_manager: FlavorManager,
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
            FlavorManager class.
        :param session: An instance of the AsyncSession class.
        """

        updates = [{"flavor_id": "2", "code": uuid.uuid4()}]

        with pytest.raises(Exception):
            await obj_manager.update_bulk(updates)

        await session.rollback()

    @pytest.mark.asyncio
    async def test_delete_bulk_success(
        self,
        obj_manager: FlavorManager,
        session: AsyncSession
    ):
        """
        Test case for the delete_bulk method of the
        FlavorManager class.

        This test verifies that the delete_bulk method
        successfully deletes multiple flavors
        from the database.

        Steps:
        1. Create two flavor objects
            using the FlavorFactory.
        2. Delete the flavors using the
            delete_bulk method
            of the obj_manager.
        3. Verify that the delete operation was successful by
            checking if the flavors
            no longer exist in the database.

        Expected Result:
        - The delete_bulk method should return True, indicating
            that the delete operation was successful.
        - The flavors should
            no longer exist in the database.

        """

        obj_1 = await FlavorFactory.create_async(
            session=session)

        obj_2 = await FlavorFactory.create_async(
            session=session)

        # Delete flavors
        flavor_ids = [
            obj_1.flavor_id,
            obj_2.flavor_id
        ]
        result = await obj_manager.delete_bulk(
            flavor_ids)

        assert result is True

        for flavor_id in flavor_ids:
            execute_result = await session.execute(
                select(Flavor).filter(
                    Flavor._flavor_id == (
                        flavor_id))  # type: ignore
            )
            fetched_obj = execute_result.scalars().first()

            assert fetched_obj is None

    @pytest.mark.asyncio
    async def test_delete_bulk_flavors_not_found(
        self,
        obj_manager: FlavorManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of deleting bulk
        flavors when some
        flavors are not found.

        Steps:
        1. Create a flavor using the
            FlavorFactory.
        2. Assert that the created flavor
            is an instance of the
            Flavor class.
        3. Define a list of flavor IDs to delete.
        4. Use pytest.raises to assert that an exception is
            raised when deleting the bulk flavors.
        5. Rollback the session to undo any changes made during the test.

        This test case ensures that the delete_bulk method of the
        FlavorManager raises an exception
        when some flavors with the specified IDs are
        not found in the database.
        """
        obj_1 = await FlavorFactory.create_async(
            session=session)

        assert isinstance(obj_1,
                          Flavor)

        # Delete flavors
        flavor_ids = [1, 2]

        with pytest.raises(Exception):
            await obj_manager.delete_bulk(
                flavor_ids)

        await session.rollback()

    @pytest.mark.asyncio
    async def test_delete_bulk_empty_list(
        self,
        obj_manager: FlavorManager
    ):
        """
        Test case to verify the behavior of deleting
        flavors with an empty list.

        Args:
            obj_manager (FlavorManager): The
                instance of the
                FlavorManager class.

        Returns:
            None

        Raises:
            AssertionError: If the result is not True.
        """

        # Delete flavors with an empty list
        flavor_ids = []
        result = await obj_manager.delete_bulk(
            flavor_ids)

        # Assertions
        assert result is True

    @pytest.mark.asyncio
    async def test_delete_bulk_invalid_type(
        self,
        obj_manager: FlavorManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of the delete_bulk
        method when invalid flavor IDs are provided.

        Args:
            obj_manager (FlavorManager): The
                instance of the
                FlavorManager class.
            session (AsyncSession): The async session object.

        Raises:
            Exception: If an exception is raised during the
                execution of the delete_bulk method.

        Returns:
            None
        """

        flavor_ids = ["1", 2]

        with pytest.raises(Exception):
            await obj_manager.delete_bulk(
                flavor_ids)

        await session.rollback()
