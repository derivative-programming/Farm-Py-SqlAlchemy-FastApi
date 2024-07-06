# models/managers/tests/dyna_flow_task_test.py  # pylint: disable=duplicate-code
# pylint: disable=protected-access, too-many-public-methods
# pylint: disable=unused-argument
# pylint: disable=unused-import
"""
    This class contains unit tests for the
    `DynaFlowTaskManager` class.
"""

import logging
import uuid  # noqa: F401

import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

import pytest
from helpers.session_context import SessionContext
from managers.dyna_flow_task import DynaFlowTaskManager
from models import DynaFlowTask
from models.factory import DynaFlowTaskFactory


class TestDynaFlowTaskBulkManager:
    """
    This class contains unit tests for the
    `DynaFlowTaskManager` class.
    """

    @pytest_asyncio.fixture(scope="function")
    async def obj_manager(self, session: AsyncSession):
        """
        Fixture that returns an instance of
        `DynaFlowTaskManager` for testing.
        """
        session_context = SessionContext({}, session)
        session_context.customer_code = uuid.uuid4()
        return DynaFlowTaskManager(session_context)

    @pytest.mark.asyncio
    async def test_add_bulk(
        self,
        obj_manager: DynaFlowTaskManager,
        session: AsyncSession
    ):
        """
        Test case for the `add_bulk` method of the
        `DynaFlowTaskManager` class.

        This test case verifies that the `add_bulk`
        method correctly adds multiple
        dyna_flow_tasks to the database.

        Steps:
        1. Generate a list of dyna_flow_task data using the
            `DynaFlowTaskFactory.build_async` method.
        2. Call the `add_bulk` method of the
            `obj_manager` instance,
            passing in the
            generated dyna_flow_task data.
        3. Verify that the number of dyna_flow_tasks
            returned is
            equal to the number of dyna_flow_tasks added.
        4. For each updated dyna_flow_task, fetch the corresponding
            dyna_flow_task from the database.
        5. Verify that the fetched dyna_flow_task
            is an instance of the
            `DynaFlowTask` class.
        6. Verify that the insert_user_id and
            last_update_user_id of the fetched
            dyna_flow_task match the
            customer code of the session context.
        7. Verify that the dyna_flow_task_id of the fetched
            dyna_flow_task matches the
            dyna_flow_task_id of the updated
            dyna_flow_task.

        """
        dyna_flow_tasks_data = [
            await DynaFlowTaskFactory.build_async(session)
            for _ in range(5)]

        dyna_flow_tasks = await obj_manager.add_bulk(
            dyna_flow_tasks_data)

        assert len(dyna_flow_tasks) == 5

        for updated_obj in dyna_flow_tasks:
            result = await session.execute(
                select(DynaFlowTask).filter(
                    DynaFlowTask._dyna_flow_task_id == (
                        updated_obj.dyna_flow_task_id)  # type: ignore
                )
            )
            fetched_obj = result.scalars().first()

            assert isinstance(
                fetched_obj,
                DynaFlowTask)

            assert str(fetched_obj.insert_user_id) == (
                str(obj_manager._session_context.customer_code))
            assert str(fetched_obj.last_update_user_id) == (
                str(obj_manager._session_context.customer_code))

            assert fetched_obj.dyna_flow_task_id == \
                updated_obj.dyna_flow_task_id

    @pytest.mark.asyncio
    async def test_update_bulk_success(
        self,
        obj_manager: DynaFlowTaskManager,
        session: AsyncSession
    ):
        """
        Test case for bulk update of dyna_flow_tasks.

        This test case verifies the functionality of the
        `update_bulk` method in the
        `DynaFlowTaskManager` class.
        It creates two dyna_flow_task instances,
        updates their codes
        using the `update_bulk` method, and then verifies
        that the updates were successful by checking the
        updated codes in the database.

        Steps:
        1. Create two dyna_flow_task instances using the
            `DynaFlowTaskFactory.create_async` method.
        2. Generate new codes for the dyna_flow_tasks.
        3. Update the dyna_flow_tasks' codes
            using the `update_bulk` method.
        4. Verify that the update was successful by checking
            the updated codes in the database.

        Args:
            obj_manager (DynaFlowTaskManager):
                An instance of the
                `DynaFlowTaskManager` class.
            session (AsyncSession): An instance of the `AsyncSession` class.

        Returns:
            None
        """
        # Mocking dyna_flow_task instances
        obj_1 = await DynaFlowTaskFactory. \
            create_async(
                session=session)
        obj_2 = await DynaFlowTaskFactory. \
            create_async(
                session=session)
        logging.info(obj_1.__dict__)

        code_updated1 = uuid.uuid4()
        code_updated2 = uuid.uuid4()
        logging.info(code_updated1)
        logging.info(code_updated2)

        # Update dyna_flow_tasks
        updates = [
            {
                "dyna_flow_task_id":
                    obj_1.dyna_flow_task_id,
                "code": code_updated1
            },
            {
                "dyna_flow_task_id":
                    obj_2.dyna_flow_task_id,
                "code": code_updated2
            }
        ]
        updated_dyna_flow_tasks = await obj_manager.update_bulk(
            updates)

        logging.info('bulk update results')
        # Assertions
        assert len(updated_dyna_flow_tasks) == 2
        logging.info(updated_dyna_flow_tasks[0]
                     .__dict__)
        logging.info(updated_dyna_flow_tasks[1]
                     .__dict__)

        logging.info('getall')
        dyna_flow_tasks = await obj_manager.get_list()
        logging.info(dyna_flow_tasks[0]
                     .__dict__)
        logging.info(dyna_flow_tasks[1]
                     .__dict__)

        assert updated_dyna_flow_tasks[0].code == \
            code_updated1
        assert updated_dyna_flow_tasks[1].code == \
            code_updated2

        assert str(updated_dyna_flow_tasks[0]
                   .last_update_user_id) == (
            str(obj_manager
                ._session_context.customer_code))

        assert str(updated_dyna_flow_tasks[1]
                   .last_update_user_id) == (
            str(obj_manager
                ._session_context.customer_code))

        result = await session.execute(
            select(DynaFlowTask).filter(
                DynaFlowTask._dyna_flow_task_id == 1)  # type: ignore
        )
        fetched_obj = result.scalars().first()

        assert isinstance(fetched_obj,
                          DynaFlowTask)

        assert fetched_obj.code == code_updated1

        result = await session.execute(
            select(DynaFlowTask).filter(
                DynaFlowTask._dyna_flow_task_id == 2)  # type: ignore
        )
        fetched_obj = result.scalars().first()

        assert isinstance(fetched_obj,
                          DynaFlowTask)

        assert fetched_obj.code == code_updated2

    @pytest.mark.asyncio
    async def test_update_bulk_missing_dyna_flow_task_id(
        self,
        obj_manager: DynaFlowTaskManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of the `update_bulk`
        method when the dyna_flow_task_id is missing.

        This test case ensures that when the dyna_flow_task_id is
        missing in the updates list,
        an exception is raised and the session is rolled back.

        Steps:
        1. Prepare the updates list with a missing dyna_flow_task_id.
        2. Call the `update_bulk` method with the updates list.
        3. Assert that an exception is raised.
        4. Rollback the session to undo any changes made during the test.

        """
        # No dyna_flow_tasks to update since
        # dyna_flow_task_id is missing
        updates = [{"name": "Red Rose"}]

        with pytest.raises(Exception):
            await obj_manager.update_bulk(updates)

        await session.rollback()

    @pytest.mark.asyncio
    async def test_update_bulk_dyna_flow_task_not_found(
        self,
        obj_manager: DynaFlowTaskManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of the update_bulk
        method when a dyna_flow_task is not found.

        This test case performs the following steps:
        1. Defines a list of dyna_flow_task updates,
            where each update
            contains a dyna_flow_task_id and a code.
        2. Calls the update_bulk method of the
            obj_manager with the list of updates.
        3. Expects an exception to be raised, indicating that
            the dyna_flow_task was not found.
        4. Rolls back the session to undo any changes made during the test.

        Note: This test assumes that the update_bulk method
        throws an exception when a
        dyna_flow_task is not found.

        """

        # Update dyna_flow_tasks
        updates = [{"dyna_flow_task_id": 1, "code": uuid.uuid4()}]

        with pytest.raises(Exception):
            await obj_manager.update_bulk(updates)

        await session.rollback()

    @pytest.mark.asyncio
    async def test_update_bulk_invalid_type(
        self,
        obj_manager: DynaFlowTaskManager,
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
            DynaFlowTaskManager class.
        :param session: An instance of the AsyncSession class.
        """

        updates = [{"dyna_flow_task_id": "2", "code": uuid.uuid4()}]

        with pytest.raises(Exception):
            await obj_manager.update_bulk(updates)

        await session.rollback()

    @pytest.mark.asyncio
    async def test_delete_bulk_success(
        self,
        obj_manager: DynaFlowTaskManager,
        session: AsyncSession
    ):
        """
        Test case for the delete_bulk method of the
        DynaFlowTaskManager class.

        This test verifies that the delete_bulk method
        successfully deletes multiple dyna_flow_tasks
        from the database.

        Steps:
        1. Create two dyna_flow_task objects
            using the DynaFlowTaskFactory.
        2. Delete the dyna_flow_tasks using the
            delete_bulk method
            of the obj_manager.
        3. Verify that the delete operation was successful by
            checking if the dyna_flow_tasks
            no longer exist in the database.

        Expected Result:
        - The delete_bulk method should return True, indicating
            that the delete operation was successful.
        - The dyna_flow_tasks should
            no longer exist in the database.

        """

        obj_1 = await DynaFlowTaskFactory.create_async(
            session=session)

        obj_2 = await DynaFlowTaskFactory.create_async(
            session=session)

        # Delete dyna_flow_tasks
        dyna_flow_task_ids = [
            obj_1.dyna_flow_task_id,
            obj_2.dyna_flow_task_id
        ]
        result = await obj_manager.delete_bulk(
            dyna_flow_task_ids)

        assert result is True

        for dyna_flow_task_id in dyna_flow_task_ids:
            execute_result = await session.execute(
                select(DynaFlowTask).filter(
                    DynaFlowTask._dyna_flow_task_id == (
                        dyna_flow_task_id))  # type: ignore
            )
            fetched_obj = execute_result.scalars().first()

            assert fetched_obj is None

    @pytest.mark.asyncio
    async def test_delete_bulk_dyna_flow_tasks_not_found(
        self,
        obj_manager: DynaFlowTaskManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of deleting bulk
        dyna_flow_tasks when some
        dyna_flow_tasks are not found.

        Steps:
        1. Create a dyna_flow_task using the
            DynaFlowTaskFactory.
        2. Assert that the created dyna_flow_task
            is an instance of the
            DynaFlowTask class.
        3. Define a list of dyna_flow_task IDs to delete.
        4. Use pytest.raises to assert that an exception is
            raised when deleting the bulk dyna_flow_tasks.
        5. Rollback the session to undo any changes made during the test.

        This test case ensures that the delete_bulk method of the
        DynaFlowTaskManager raises an exception
        when some dyna_flow_tasks with the specified IDs are
        not found in the database.
        """
        obj_1 = await DynaFlowTaskFactory.create_async(
            session=session)

        assert isinstance(obj_1,
                          DynaFlowTask)

        # Delete dyna_flow_tasks
        dyna_flow_task_ids = [1, 2]

        with pytest.raises(Exception):
            await obj_manager.delete_bulk(
                dyna_flow_task_ids)

        await session.rollback()

    @pytest.mark.asyncio
    async def test_delete_bulk_empty_list(
        self,
        obj_manager: DynaFlowTaskManager
    ):
        """
        Test case to verify the behavior of deleting
        dyna_flow_tasks with an empty list.

        Args:
            obj_manager (DynaFlowTaskManager): The
                instance of the
                DynaFlowTaskManager class.

        Returns:
            None

        Raises:
            AssertionError: If the result is not True.
        """

        # Delete dyna_flow_tasks with an empty list
        dyna_flow_task_ids = []
        result = await obj_manager.delete_bulk(
            dyna_flow_task_ids)

        # Assertions
        assert result is True

    @pytest.mark.asyncio
    async def test_delete_bulk_invalid_type(
        self,
        obj_manager: DynaFlowTaskManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of the delete_bulk
        method when invalid dyna_flow_task IDs are provided.

        Args:
            obj_manager (DynaFlowTaskManager): The
                instance of the
                DynaFlowTaskManager class.
            session (AsyncSession): The async session object.

        Raises:
            Exception: If an exception is raised during the
                execution of the delete_bulk method.

        Returns:
            None
        """

        dyna_flow_task_ids = ["1", 2]

        with pytest.raises(Exception):
            await obj_manager.delete_bulk(
                dyna_flow_task_ids)

        await session.rollback()
