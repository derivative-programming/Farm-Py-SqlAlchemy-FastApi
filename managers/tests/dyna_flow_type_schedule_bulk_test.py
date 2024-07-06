# models/managers/tests/dyna_flow_type_schedule_test.py  # pylint: disable=duplicate-code
# pylint: disable=protected-access, too-many-public-methods
# pylint: disable=unused-argument
# pylint: disable=unused-import
"""
    This class contains unit tests for the
    `DynaFlowTypeScheduleManager` class.
"""

import logging
import uuid  # noqa: F401

import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

import pytest
from helpers.session_context import SessionContext
from managers.dyna_flow_type_schedule import DynaFlowTypeScheduleManager
from models import DynaFlowTypeSchedule
from models.factory import DynaFlowTypeScheduleFactory


class TestDynaFlowTypeScheduleBulkManager:
    """
    This class contains unit tests for the
    `DynaFlowTypeScheduleManager` class.
    """

    @pytest_asyncio.fixture(scope="function")
    async def obj_manager(self, session: AsyncSession):
        """
        Fixture that returns an instance of
        `DynaFlowTypeScheduleManager` for testing.
        """
        session_context = SessionContext({}, session)
        session_context.customer_code = uuid.uuid4()
        return DynaFlowTypeScheduleManager(session_context)

    @pytest.mark.asyncio
    async def test_add_bulk(
        self,
        obj_manager: DynaFlowTypeScheduleManager,
        session: AsyncSession
    ):
        """
        Test case for the `add_bulk` method of the
        `DynaFlowTypeScheduleManager` class.

        This test case verifies that the `add_bulk`
        method correctly adds multiple
        dyna_flow_type_schedules to the database.

        Steps:
        1. Generate a list of dyna_flow_type_schedule data using the
            `DynaFlowTypeScheduleFactory.build_async` method.
        2. Call the `add_bulk` method of the
            `obj_manager` instance,
            passing in the
            generated dyna_flow_type_schedule data.
        3. Verify that the number of dyna_flow_type_schedules
            returned is
            equal to the number of dyna_flow_type_schedules added.
        4. For each updated dyna_flow_type_schedule, fetch the corresponding
            dyna_flow_type_schedule from the database.
        5. Verify that the fetched dyna_flow_type_schedule
            is an instance of the
            `DynaFlowTypeSchedule` class.
        6. Verify that the insert_user_id and
            last_update_user_id of the fetched
            dyna_flow_type_schedule match the
            customer code of the session context.
        7. Verify that the dyna_flow_type_schedule_id of the fetched
            dyna_flow_type_schedule matches the
            dyna_flow_type_schedule_id of the updated
            dyna_flow_type_schedule.

        """
        dyna_flow_type_schedules_data = [
            await DynaFlowTypeScheduleFactory.build_async(session)
            for _ in range(5)]

        dyna_flow_type_schedules = await obj_manager.add_bulk(
            dyna_flow_type_schedules_data)

        assert len(dyna_flow_type_schedules) == 5

        for updated_obj in dyna_flow_type_schedules:
            result = await session.execute(
                select(DynaFlowTypeSchedule).filter(
                    DynaFlowTypeSchedule._dyna_flow_type_schedule_id == (
                        updated_obj.dyna_flow_type_schedule_id)  # type: ignore
                )
            )
            fetched_obj = result.scalars().first()

            assert isinstance(
                fetched_obj,
                DynaFlowTypeSchedule)

            assert str(fetched_obj.insert_user_id) == (
                str(obj_manager._session_context.customer_code))
            assert str(fetched_obj.last_update_user_id) == (
                str(obj_manager._session_context.customer_code))

            assert fetched_obj.dyna_flow_type_schedule_id == \
                updated_obj.dyna_flow_type_schedule_id

    @pytest.mark.asyncio
    async def test_update_bulk_success(
        self,
        obj_manager: DynaFlowTypeScheduleManager,
        session: AsyncSession
    ):
        """
        Test case for bulk update of dyna_flow_type_schedules.

        This test case verifies the functionality of the
        `update_bulk` method in the
        `DynaFlowTypeScheduleManager` class.
        It creates two dyna_flow_type_schedule instances,
        updates their codes
        using the `update_bulk` method, and then verifies
        that the updates were successful by checking the
        updated codes in the database.

        Steps:
        1. Create two dyna_flow_type_schedule instances using the
            `DynaFlowTypeScheduleFactory.create_async` method.
        2. Generate new codes for the dyna_flow_type_schedules.
        3. Update the dyna_flow_type_schedules' codes
            using the `update_bulk` method.
        4. Verify that the update was successful by checking
            the updated codes in the database.

        Args:
            obj_manager (DynaFlowTypeScheduleManager):
                An instance of the
                `DynaFlowTypeScheduleManager` class.
            session (AsyncSession): An instance of the `AsyncSession` class.

        Returns:
            None
        """
        # Mocking dyna_flow_type_schedule instances
        obj_1 = await DynaFlowTypeScheduleFactory. \
            create_async(
                session=session)
        obj_2 = await DynaFlowTypeScheduleFactory. \
            create_async(
                session=session)
        logging.info(obj_1.__dict__)

        code_updated1 = uuid.uuid4()
        code_updated2 = uuid.uuid4()
        logging.info(code_updated1)
        logging.info(code_updated2)

        # Update dyna_flow_type_schedules
        updates = [
            {
                "dyna_flow_type_schedule_id":
                    obj_1.dyna_flow_type_schedule_id,
                "code": code_updated1
            },
            {
                "dyna_flow_type_schedule_id":
                    obj_2.dyna_flow_type_schedule_id,
                "code": code_updated2
            }
        ]
        updated_dyna_flow_type_schedules = await obj_manager.update_bulk(
            updates)

        logging.info('bulk update results')
        # Assertions
        assert len(updated_dyna_flow_type_schedules) == 2
        logging.info(updated_dyna_flow_type_schedules[0]
                     .__dict__)
        logging.info(updated_dyna_flow_type_schedules[1]
                     .__dict__)

        logging.info('getall')
        dyna_flow_type_schedules = await obj_manager.get_list()
        logging.info(dyna_flow_type_schedules[0]
                     .__dict__)
        logging.info(dyna_flow_type_schedules[1]
                     .__dict__)

        assert updated_dyna_flow_type_schedules[0].code == \
            code_updated1
        assert updated_dyna_flow_type_schedules[1].code == \
            code_updated2

        assert str(updated_dyna_flow_type_schedules[0]
                   .last_update_user_id) == (
            str(obj_manager
                ._session_context.customer_code))

        assert str(updated_dyna_flow_type_schedules[1]
                   .last_update_user_id) == (
            str(obj_manager
                ._session_context.customer_code))

        result = await session.execute(
            select(DynaFlowTypeSchedule).filter(
                DynaFlowTypeSchedule._dyna_flow_type_schedule_id == 1)  # type: ignore
        )
        fetched_obj = result.scalars().first()

        assert isinstance(fetched_obj,
                          DynaFlowTypeSchedule)

        assert fetched_obj.code == code_updated1

        result = await session.execute(
            select(DynaFlowTypeSchedule).filter(
                DynaFlowTypeSchedule._dyna_flow_type_schedule_id == 2)  # type: ignore
        )
        fetched_obj = result.scalars().first()

        assert isinstance(fetched_obj,
                          DynaFlowTypeSchedule)

        assert fetched_obj.code == code_updated2

    @pytest.mark.asyncio
    async def test_update_bulk_missing_dyna_flow_type_schedule_id(
        self,
        obj_manager: DynaFlowTypeScheduleManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of the `update_bulk`
        method when the dyna_flow_type_schedule_id is missing.

        This test case ensures that when the dyna_flow_type_schedule_id is
        missing in the updates list,
        an exception is raised and the session is rolled back.

        Steps:
        1. Prepare the updates list with a missing dyna_flow_type_schedule_id.
        2. Call the `update_bulk` method with the updates list.
        3. Assert that an exception is raised.
        4. Rollback the session to undo any changes made during the test.

        """
        # No dyna_flow_type_schedules to update since
        # dyna_flow_type_schedule_id is missing
        updates = [{"name": "Red Rose"}]

        with pytest.raises(Exception):
            await obj_manager.update_bulk(updates)

        await session.rollback()

    @pytest.mark.asyncio
    async def test_update_bulk_dyna_flow_type_schedule_not_found(
        self,
        obj_manager: DynaFlowTypeScheduleManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of the update_bulk
        method when a dyna_flow_type_schedule is not found.

        This test case performs the following steps:
        1. Defines a list of dyna_flow_type_schedule updates,
            where each update
            contains a dyna_flow_type_schedule_id and a code.
        2. Calls the update_bulk method of the
            obj_manager with the list of updates.
        3. Expects an exception to be raised, indicating that
            the dyna_flow_type_schedule was not found.
        4. Rolls back the session to undo any changes made during the test.

        Note: This test assumes that the update_bulk method
        throws an exception when a
        dyna_flow_type_schedule is not found.

        """

        # Update dyna_flow_type_schedules
        updates = [{"dyna_flow_type_schedule_id": 1, "code": uuid.uuid4()}]

        with pytest.raises(Exception):
            await obj_manager.update_bulk(updates)

        await session.rollback()

    @pytest.mark.asyncio
    async def test_update_bulk_invalid_type(
        self,
        obj_manager: DynaFlowTypeScheduleManager,
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
            DynaFlowTypeScheduleManager class.
        :param session: An instance of the AsyncSession class.
        """

        updates = [{"dyna_flow_type_schedule_id": "2", "code": uuid.uuid4()}]

        with pytest.raises(Exception):
            await obj_manager.update_bulk(updates)

        await session.rollback()

    @pytest.mark.asyncio
    async def test_delete_bulk_success(
        self,
        obj_manager: DynaFlowTypeScheduleManager,
        session: AsyncSession
    ):
        """
        Test case for the delete_bulk method of the
        DynaFlowTypeScheduleManager class.

        This test verifies that the delete_bulk method
        successfully deletes multiple dyna_flow_type_schedules
        from the database.

        Steps:
        1. Create two dyna_flow_type_schedule objects
            using the DynaFlowTypeScheduleFactory.
        2. Delete the dyna_flow_type_schedules using the
            delete_bulk method
            of the obj_manager.
        3. Verify that the delete operation was successful by
            checking if the dyna_flow_type_schedules
            no longer exist in the database.

        Expected Result:
        - The delete_bulk method should return True, indicating
            that the delete operation was successful.
        - The dyna_flow_type_schedules should
            no longer exist in the database.

        """

        obj_1 = await DynaFlowTypeScheduleFactory.create_async(
            session=session)

        obj_2 = await DynaFlowTypeScheduleFactory.create_async(
            session=session)

        # Delete dyna_flow_type_schedules
        dyna_flow_type_schedule_ids = [
            obj_1.dyna_flow_type_schedule_id,
            obj_2.dyna_flow_type_schedule_id
        ]
        result = await obj_manager.delete_bulk(
            dyna_flow_type_schedule_ids)

        assert result is True

        for dyna_flow_type_schedule_id in dyna_flow_type_schedule_ids:
            execute_result = await session.execute(
                select(DynaFlowTypeSchedule).filter(
                    DynaFlowTypeSchedule._dyna_flow_type_schedule_id == (
                        dyna_flow_type_schedule_id))  # type: ignore
            )
            fetched_obj = execute_result.scalars().first()

            assert fetched_obj is None

    @pytest.mark.asyncio
    async def test_delete_bulk_dyna_flow_type_schedules_not_found(
        self,
        obj_manager: DynaFlowTypeScheduleManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of deleting bulk
        dyna_flow_type_schedules when some
        dyna_flow_type_schedules are not found.

        Steps:
        1. Create a dyna_flow_type_schedule using the
            DynaFlowTypeScheduleFactory.
        2. Assert that the created dyna_flow_type_schedule
            is an instance of the
            DynaFlowTypeSchedule class.
        3. Define a list of dyna_flow_type_schedule IDs to delete.
        4. Use pytest.raises to assert that an exception is
            raised when deleting the bulk dyna_flow_type_schedules.
        5. Rollback the session to undo any changes made during the test.

        This test case ensures that the delete_bulk method of the
        DynaFlowTypeScheduleManager raises an exception
        when some dyna_flow_type_schedules with the specified IDs are
        not found in the database.
        """
        obj_1 = await DynaFlowTypeScheduleFactory.create_async(
            session=session)

        assert isinstance(obj_1,
                          DynaFlowTypeSchedule)

        # Delete dyna_flow_type_schedules
        dyna_flow_type_schedule_ids = [1, 2]

        with pytest.raises(Exception):
            await obj_manager.delete_bulk(
                dyna_flow_type_schedule_ids)

        await session.rollback()

    @pytest.mark.asyncio
    async def test_delete_bulk_empty_list(
        self,
        obj_manager: DynaFlowTypeScheduleManager
    ):
        """
        Test case to verify the behavior of deleting
        dyna_flow_type_schedules with an empty list.

        Args:
            obj_manager (DynaFlowTypeScheduleManager): The
                instance of the
                DynaFlowTypeScheduleManager class.

        Returns:
            None

        Raises:
            AssertionError: If the result is not True.
        """

        # Delete dyna_flow_type_schedules with an empty list
        dyna_flow_type_schedule_ids = []
        result = await obj_manager.delete_bulk(
            dyna_flow_type_schedule_ids)

        # Assertions
        assert result is True

    @pytest.mark.asyncio
    async def test_delete_bulk_invalid_type(
        self,
        obj_manager: DynaFlowTypeScheduleManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of the delete_bulk
        method when invalid dyna_flow_type_schedule IDs are provided.

        Args:
            obj_manager (DynaFlowTypeScheduleManager): The
                instance of the
                DynaFlowTypeScheduleManager class.
            session (AsyncSession): The async session object.

        Raises:
            Exception: If an exception is raised during the
                execution of the delete_bulk method.

        Returns:
            None
        """

        dyna_flow_type_schedule_ids = ["1", 2]

        with pytest.raises(Exception):
            await obj_manager.delete_bulk(
                dyna_flow_type_schedule_ids)

        await session.rollback()
