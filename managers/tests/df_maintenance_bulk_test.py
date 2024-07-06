# models/managers/tests/df_maintenance_test.py  # pylint: disable=duplicate-code
# pylint: disable=protected-access, too-many-public-methods
# pylint: disable=unused-argument
# pylint: disable=unused-import
"""
    This class contains unit tests for the
    `DFMaintenanceManager` class.
"""

import logging
import uuid  # noqa: F401

import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

import pytest
from helpers.session_context import SessionContext
from managers.df_maintenance import DFMaintenanceManager
from models import DFMaintenance
from models.factory import DFMaintenanceFactory


class TestDFMaintenanceBulkManager:
    """
    This class contains unit tests for the
    `DFMaintenanceManager` class.
    """

    @pytest_asyncio.fixture(scope="function")
    async def obj_manager(self, session: AsyncSession):
        """
        Fixture that returns an instance of
        `DFMaintenanceManager` for testing.
        """
        session_context = SessionContext({}, session)
        session_context.customer_code = uuid.uuid4()
        return DFMaintenanceManager(session_context)

    @pytest.mark.asyncio
    async def test_add_bulk(
        self,
        obj_manager: DFMaintenanceManager,
        session: AsyncSession
    ):
        """
        Test case for the `add_bulk` method of the
        `DFMaintenanceManager` class.

        This test case verifies that the `add_bulk`
        method correctly adds multiple
        df_maintenances to the database.

        Steps:
        1. Generate a list of df_maintenance data using the
            `DFMaintenanceFactory.build_async` method.
        2. Call the `add_bulk` method of the
            `obj_manager` instance,
            passing in the
            generated df_maintenance data.
        3. Verify that the number of df_maintenances
            returned is
            equal to the number of df_maintenances added.
        4. For each updated df_maintenance, fetch the corresponding
            df_maintenance from the database.
        5. Verify that the fetched df_maintenance
            is an instance of the
            `DFMaintenance` class.
        6. Verify that the insert_user_id and
            last_update_user_id of the fetched
            df_maintenance match the
            customer code of the session context.
        7. Verify that the df_maintenance_id of the fetched
            df_maintenance matches the
            df_maintenance_id of the updated
            df_maintenance.

        """
        df_maintenances_data = [
            await DFMaintenanceFactory.build_async(session)
            for _ in range(5)]

        df_maintenances = await obj_manager.add_bulk(
            df_maintenances_data)

        assert len(df_maintenances) == 5

        for updated_obj in df_maintenances:
            result = await session.execute(
                select(DFMaintenance).filter(
                    DFMaintenance._df_maintenance_id == (
                        updated_obj.df_maintenance_id)  # type: ignore
                )
            )
            fetched_obj = result.scalars().first()

            assert isinstance(
                fetched_obj,
                DFMaintenance)

            assert str(fetched_obj.insert_user_id) == (
                str(obj_manager._session_context.customer_code))
            assert str(fetched_obj.last_update_user_id) == (
                str(obj_manager._session_context.customer_code))

            assert fetched_obj.df_maintenance_id == \
                updated_obj.df_maintenance_id

    @pytest.mark.asyncio
    async def test_update_bulk_success(
        self,
        obj_manager: DFMaintenanceManager,
        session: AsyncSession
    ):
        """
        Test case for bulk update of df_maintenances.

        This test case verifies the functionality of the
        `update_bulk` method in the
        `DFMaintenanceManager` class.
        It creates two df_maintenance instances,
        updates their codes
        using the `update_bulk` method, and then verifies
        that the updates were successful by checking the
        updated codes in the database.

        Steps:
        1. Create two df_maintenance instances using the
            `DFMaintenanceFactory.create_async` method.
        2. Generate new codes for the df_maintenances.
        3. Update the df_maintenances' codes
            using the `update_bulk` method.
        4. Verify that the update was successful by checking
            the updated codes in the database.

        Args:
            obj_manager (DFMaintenanceManager):
                An instance of the
                `DFMaintenanceManager` class.
            session (AsyncSession): An instance of the `AsyncSession` class.

        Returns:
            None
        """
        # Mocking df_maintenance instances
        obj_1 = await DFMaintenanceFactory. \
            create_async(
                session=session)
        obj_2 = await DFMaintenanceFactory. \
            create_async(
                session=session)
        logging.info(obj_1.__dict__)

        code_updated1 = uuid.uuid4()
        code_updated2 = uuid.uuid4()
        logging.info(code_updated1)
        logging.info(code_updated2)

        # Update df_maintenances
        updates = [
            {
                "df_maintenance_id":
                    obj_1.df_maintenance_id,
                "code": code_updated1
            },
            {
                "df_maintenance_id":
                    obj_2.df_maintenance_id,
                "code": code_updated2
            }
        ]
        updated_df_maintenances = await obj_manager.update_bulk(
            updates)

        logging.info('bulk update results')
        # Assertions
        assert len(updated_df_maintenances) == 2
        logging.info(updated_df_maintenances[0]
                     .__dict__)
        logging.info(updated_df_maintenances[1]
                     .__dict__)

        logging.info('getall')
        df_maintenances = await obj_manager.get_list()
        logging.info(df_maintenances[0]
                     .__dict__)
        logging.info(df_maintenances[1]
                     .__dict__)

        assert updated_df_maintenances[0].code == \
            code_updated1
        assert updated_df_maintenances[1].code == \
            code_updated2

        assert str(updated_df_maintenances[0]
                   .last_update_user_id) == (
            str(obj_manager
                ._session_context.customer_code))

        assert str(updated_df_maintenances[1]
                   .last_update_user_id) == (
            str(obj_manager
                ._session_context.customer_code))

        result = await session.execute(
            select(DFMaintenance).filter(
                DFMaintenance._df_maintenance_id == 1)  # type: ignore
        )
        fetched_obj = result.scalars().first()

        assert isinstance(fetched_obj,
                          DFMaintenance)

        assert fetched_obj.code == code_updated1

        result = await session.execute(
            select(DFMaintenance).filter(
                DFMaintenance._df_maintenance_id == 2)  # type: ignore
        )
        fetched_obj = result.scalars().first()

        assert isinstance(fetched_obj,
                          DFMaintenance)

        assert fetched_obj.code == code_updated2

    @pytest.mark.asyncio
    async def test_update_bulk_missing_df_maintenance_id(
        self,
        obj_manager: DFMaintenanceManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of the `update_bulk`
        method when the df_maintenance_id is missing.

        This test case ensures that when the df_maintenance_id is
        missing in the updates list,
        an exception is raised and the session is rolled back.

        Steps:
        1. Prepare the updates list with a missing df_maintenance_id.
        2. Call the `update_bulk` method with the updates list.
        3. Assert that an exception is raised.
        4. Rollback the session to undo any changes made during the test.

        """
        # No df_maintenances to update since
        # df_maintenance_id is missing
        updates = [{"name": "Red Rose"}]

        with pytest.raises(Exception):
            await obj_manager.update_bulk(updates)

        await session.rollback()

    @pytest.mark.asyncio
    async def test_update_bulk_df_maintenance_not_found(
        self,
        obj_manager: DFMaintenanceManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of the update_bulk
        method when a df_maintenance is not found.

        This test case performs the following steps:
        1. Defines a list of df_maintenance updates,
            where each update
            contains a df_maintenance_id and a code.
        2. Calls the update_bulk method of the
            obj_manager with the list of updates.
        3. Expects an exception to be raised, indicating that
            the df_maintenance was not found.
        4. Rolls back the session to undo any changes made during the test.

        Note: This test assumes that the update_bulk method
        throws an exception when a
        df_maintenance is not found.

        """

        # Update df_maintenances
        updates = [{"df_maintenance_id": 1, "code": uuid.uuid4()}]

        with pytest.raises(Exception):
            await obj_manager.update_bulk(updates)

        await session.rollback()

    @pytest.mark.asyncio
    async def test_update_bulk_invalid_type(
        self,
        obj_manager: DFMaintenanceManager,
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
            DFMaintenanceManager class.
        :param session: An instance of the AsyncSession class.
        """

        updates = [{"df_maintenance_id": "2", "code": uuid.uuid4()}]

        with pytest.raises(Exception):
            await obj_manager.update_bulk(updates)

        await session.rollback()

    @pytest.mark.asyncio
    async def test_delete_bulk_success(
        self,
        obj_manager: DFMaintenanceManager,
        session: AsyncSession
    ):
        """
        Test case for the delete_bulk method of the
        DFMaintenanceManager class.

        This test verifies that the delete_bulk method
        successfully deletes multiple df_maintenances
        from the database.

        Steps:
        1. Create two df_maintenance objects
            using the DFMaintenanceFactory.
        2. Delete the df_maintenances using the
            delete_bulk method
            of the obj_manager.
        3. Verify that the delete operation was successful by
            checking if the df_maintenances
            no longer exist in the database.

        Expected Result:
        - The delete_bulk method should return True, indicating
            that the delete operation was successful.
        - The df_maintenances should
            no longer exist in the database.

        """

        obj_1 = await DFMaintenanceFactory.create_async(
            session=session)

        obj_2 = await DFMaintenanceFactory.create_async(
            session=session)

        # Delete df_maintenances
        df_maintenance_ids = [
            obj_1.df_maintenance_id,
            obj_2.df_maintenance_id
        ]
        result = await obj_manager.delete_bulk(
            df_maintenance_ids)

        assert result is True

        for df_maintenance_id in df_maintenance_ids:
            execute_result = await session.execute(
                select(DFMaintenance).filter(
                    DFMaintenance._df_maintenance_id == (
                        df_maintenance_id))  # type: ignore
            )
            fetched_obj = execute_result.scalars().first()

            assert fetched_obj is None

    @pytest.mark.asyncio
    async def test_delete_bulk_df_maintenances_not_found(
        self,
        obj_manager: DFMaintenanceManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of deleting bulk
        df_maintenances when some
        df_maintenances are not found.

        Steps:
        1. Create a df_maintenance using the
            DFMaintenanceFactory.
        2. Assert that the created df_maintenance
            is an instance of the
            DFMaintenance class.
        3. Define a list of df_maintenance IDs to delete.
        4. Use pytest.raises to assert that an exception is
            raised when deleting the bulk df_maintenances.
        5. Rollback the session to undo any changes made during the test.

        This test case ensures that the delete_bulk method of the
        DFMaintenanceManager raises an exception
        when some df_maintenances with the specified IDs are
        not found in the database.
        """
        obj_1 = await DFMaintenanceFactory.create_async(
            session=session)

        assert isinstance(obj_1,
                          DFMaintenance)

        # Delete df_maintenances
        df_maintenance_ids = [1, 2]

        with pytest.raises(Exception):
            await obj_manager.delete_bulk(
                df_maintenance_ids)

        await session.rollback()

    @pytest.mark.asyncio
    async def test_delete_bulk_empty_list(
        self,
        obj_manager: DFMaintenanceManager
    ):
        """
        Test case to verify the behavior of deleting
        df_maintenances with an empty list.

        Args:
            obj_manager (DFMaintenanceManager): The
                instance of the
                DFMaintenanceManager class.

        Returns:
            None

        Raises:
            AssertionError: If the result is not True.
        """

        # Delete df_maintenances with an empty list
        df_maintenance_ids = []
        result = await obj_manager.delete_bulk(
            df_maintenance_ids)

        # Assertions
        assert result is True

    @pytest.mark.asyncio
    async def test_delete_bulk_invalid_type(
        self,
        obj_manager: DFMaintenanceManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of the delete_bulk
        method when invalid df_maintenance IDs are provided.

        Args:
            obj_manager (DFMaintenanceManager): The
                instance of the
                DFMaintenanceManager class.
            session (AsyncSession): The async session object.

        Raises:
            Exception: If an exception is raised during the
                execution of the delete_bulk method.

        Returns:
            None
        """

        df_maintenance_ids = ["1", 2]

        with pytest.raises(Exception):
            await obj_manager.delete_bulk(
                df_maintenance_ids)

        await session.rollback()
