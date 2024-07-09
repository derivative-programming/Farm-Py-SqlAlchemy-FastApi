# models/managers/tests/dyna_flow_task_test.py  # pylint: disable=duplicate-code # noqa: E501
# pylint: disable=protected-access, too-many-public-methods
# pylint: disable=unused-argument
# pylint: disable=unused-import
"""
    This class contains unit tests for the
    `DynaFlowTaskManager` class.
"""

import uuid  # noqa: F401

import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

import models
import pytest
from helpers.session_context import SessionContext
from managers.dyna_flow_task import DynaFlowTaskManager
from models import DynaFlowTask
from models.factory import DynaFlowTaskFactory


class TestDynaFlowTaskGetByManager:
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
    async def test_build(
        self,
        obj_manager: DynaFlowTaskManager
    ):
        """
        Test case for the `build` method of
        `DynaFlowTaskManager`.
        """
        # Define mock data for our dyna_flow_task
        mock_data = {
            "code": uuid.uuid4()
        }

        # Call the build function of the manager
        dyna_flow_task = await \
            obj_manager.build(
                **mock_data)

        # Assert that the returned object is an instance of
        # DynaFlowTask
        assert isinstance(
            dyna_flow_task,
            DynaFlowTask)

        # Assert that the attributes of the
        # dyna_flow_task match our mock data
        assert dyna_flow_task.code == mock_data["code"]

    @pytest.mark.asyncio
    async def test_get_by_id(
        self,
        obj_manager: DynaFlowTaskManager,
        session: AsyncSession
    ):
        """
        Test case for the `get_by_id` method of
        `DynaFlowTaskManager`.
        """
        new_obj = await \
            DynaFlowTaskFactory.create_async(
                session)

        dyna_flow_task = await \
            obj_manager.get_by_id(
                new_obj.dyna_flow_task_id)

        assert isinstance(
            dyna_flow_task,
            DynaFlowTask)

        assert new_obj.dyna_flow_task_id == \
            dyna_flow_task.dyna_flow_task_id
        assert new_obj.code == \
            dyna_flow_task.code

    @pytest.mark.asyncio
    async def test_get_by_id_not_found(
        self,
        obj_manager: DynaFlowTaskManager
    ):
        """
        Test case for the `get_by_id` method of
        `DynaFlowTaskManager` when the
        dyna_flow_task is not found.
        """

        non_existent_id = 9999  # An ID that's not in the database

        retrieved_dyna_flow_task = await \
            obj_manager.get_by_id(
                non_existent_id)

        assert retrieved_dyna_flow_task is None

    @pytest.mark.asyncio
    async def test_get_by_code_returns_dyna_flow_task(
        self,
        obj_manager: DynaFlowTaskManager,
        session: AsyncSession
    ):
        """
        Test case for the `get_by_code` method of
        `DynaFlowTaskManager` that checks if
        a dyna_flow_task is
        returned by its code.
        """

        new_obj = await \
            DynaFlowTaskFactory.create_async(
                session)

        dyna_flow_task = await \
            obj_manager.get_by_code(
                new_obj.code)

        assert isinstance(
            dyna_flow_task,
            DynaFlowTask)

        assert new_obj.dyna_flow_task_id == \
            dyna_flow_task.dyna_flow_task_id
        assert new_obj.code == \
            dyna_flow_task.code

    @pytest.mark.asyncio
    async def test_get_by_code_returns_none_for_nonexistent_code(
        self,
        obj_manager: DynaFlowTaskManager
    ):
        """
        Test case for the `get_by_code` method of
        `DynaFlowTaskManager` when the code does not exist.
        """
        # Generate a random UUID that doesn't correspond to
        # any DynaFlowTask in the database
        random_code = uuid.uuid4()

        dyna_flow_task = await \
            obj_manager.get_by_code(
                random_code)

        assert dyna_flow_task is None

    # completedUTCDateTime
    # dependencyDynaFlowTaskID
    # description
    # DynaFlowID

    @pytest.mark.asyncio
    async def test_get_by_dyna_flow_id_existing(
        self,
        obj_manager: DynaFlowTaskManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of the
        `get_by_dyna_flow_id` method when
        a dyna_flow_task with
        a specific dyna_flow_id exists.

        Steps:
        1. Create a dyna_flow_task using the
            DynaFlowTaskFactory.
        2. Fetch the dyna_flow_task using the
            `get_by_dyna_flow_id` method of the obj_manager.
        3. Assert that the fetched dyna_flow_tasks list contains
            only one dyna_flow_task.
        4. Assert that the fetched dyna_flow_task
            is an instance
            of the DynaFlowTask class.
        5. Assert that the code of the fetched dyna_flow_task
            matches the code of the created dyna_flow_task.
        6. Fetch the corresponding dyna_flow object
            using the dyna_flow_id of the created dyna_flow_task.
        7. Assert that the fetched dyna_flow object is
            an instance of the DynaFlow class.
        8. Assert that the dyna_flow_code_peek of the fetched
            dyna_flow_task matches the
            code of the fetched dyna_flow.

        """
        # Add a dyna_flow_task with a specific
        # dyna_flow_id
        obj_1 = await DynaFlowTaskFactory.create_async(
            session=session)

        # Fetch the dyna_flow_task using
        # the manager function

        fetched_objs = await \
            obj_manager.get_by_dyna_flow_id(
                obj_1.dyna_flow_id)
        assert len(fetched_objs) == 1
        assert isinstance(fetched_objs[0],
                          DynaFlowTask)
        assert fetched_objs[0].code == \
            obj_1.code

        stmt = select(models.DynaFlow).where(
            models.DynaFlow._dyna_flow_id == obj_1.dyna_flow_id)  # type: ignore  # noqa: E501
        result = await session.execute(stmt)
        dyna_flow = result.scalars().first()

        assert isinstance(dyna_flow, models.DynaFlow)

        assert fetched_objs[0].dyna_flow_code_peek == dyna_flow.code

    @pytest.mark.asyncio
    async def test_get_by_dyna_flow_id_nonexistent(
        self,
        obj_manager: DynaFlowTaskManager
    ):
        """
        Test case to verify the behavior of the
        get_by_dyna_flow_id method when the dyna_flow ID does not exist.

        This test case ensures that when a non-existent
        dyna_flow ID is provided to the get_by_dyna_flow_id method,
        an empty list is returned.
        """

        non_existent_id = 999

        fetched_objs = await \
            obj_manager.get_by_dyna_flow_id(
                non_existent_id)
        assert len(fetched_objs) == 0

    @pytest.mark.asyncio
    async def test_get_by_dyna_flow_id_invalid_type(
        self,
        obj_manager: DynaFlowTaskManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of the
        `get_by_dyna_flow_id` method when an invalid dyna_flow ID is provided.

        Args:
            obj_manager (DynaFlowTaskManager): An
                instance of the DynaFlowTaskManager class.
            session (AsyncSession): An instance
                of the AsyncSession class.

        Raises:
            Exception: If an exception is raised during
            the execution of the `get_by_dyna_flow_id` method.

        Returns:
            None
        """

        invalid_id = "invalid_id"

        with pytest.raises(Exception):
            await obj_manager.get_by_dyna_flow_id(
                invalid_id)  # type: ignore

        await session.rollback()
    # dynaFlowSubjectCode
    # DynaFlowTaskTypeID

    @pytest.mark.asyncio
    async def test_get_by_dyna_flow_task_type_id_existing(
        self,
        obj_manager: DynaFlowTaskManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of the
        `get_by_dyna_flow_task_type_id` method
        when a dyna_flow_task with a
        specific dyna_flow_task_type_id exists.

        Steps:
        1. Create a dyna_flow_task using the
            DynaFlowTaskFactory.
        2. Fetch the dyna_flow_task using the
            `get_by_dyna_flow_task_type_id`
            method of the obj_manager.
        3. Assert that the fetched dyna_flow_tasks list has a length of 1.
        4. Assert that the first element in the fetched
            dyna_flow_tasks list is an instance of the
            DynaFlowTask class.
        5. Assert that the code of the fetched
            dyna_flow_task
            matches the code of the created dyna_flow_task.
        6. Execute a select statement to fetch the
            DynaFlowTaskType object associated with the
            dyna_flow_task_type_id.
        7. Assert that the fetched dyna_flow_task_type is an
            instance of the DynaFlowTaskType class.
        8. Assert that the dyna_flow_task_type_code_peek
            of the fetched dyna_flow_task matches
            the code of the fetched dyna_flow_task_type.
        """
        # Add a dyna_flow_task with a specific
        # dyna_flow_task_type_id
        obj_1 = await DynaFlowTaskFactory.create_async(
            session=session)

        # Fetch the dyna_flow_task using the
        # manager function

        fetched_objs = await \
            obj_manager.get_by_dyna_flow_task_type_id(
                obj_1.dyna_flow_task_type_id)
        assert len(fetched_objs) == 1
        assert isinstance(fetched_objs[0],
                          DynaFlowTask)
        assert fetched_objs[0].code == \
            obj_1.code

        stmt = select(models.DynaFlowTaskType).where(
            models.DynaFlowTaskType._dyna_flow_task_type_id == obj_1.dyna_flow_task_type_id)  # type: ignore  # noqa: E501
        result = await session.execute(stmt)
        dyna_flow_task_type = result.scalars().first()

        assert isinstance(dyna_flow_task_type, models.DynaFlowTaskType)

        assert fetched_objs[0].dyna_flow_task_type_code_peek == dyna_flow_task_type.code

    @pytest.mark.asyncio
    async def test_get_by_dyna_flow_task_type_id_nonexistent(
        self,
        obj_manager: DynaFlowTaskManager
    ):
        """
        Test case to verify the behavior of the
        'get_by_dyna_flow_task_type_id' method
        when the provided foreign key ID does
        not exist in the database.

        This test ensures that when a non-existent
        foreign key ID is passed to the
        'get_by_dyna_flow_task_type_id' method, it
        returns an empty list.

        Steps:
        1. Set a non-existent foreign key ID.
        2. Call the 'get_by_dyna_flow_task_type_id'
            method with the non-existent ID.
        3. Assert that the returned list of fetched dyna_flow_tasks is empty.

        """
        non_existent_id = 999

        fetched_objs = (
            await obj_manager.get_by_dyna_flow_task_type_id(
                non_existent_id))
        assert len(fetched_objs) == 0

    @pytest.mark.asyncio
    async def test_get_by_dyna_flow_task_type_id_invalid_type(
        self,
        obj_manager: DynaFlowTaskManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of the
        `get_by_dyna_flow_task_type_id` method
        when an invalid foreign key ID type is provided.

        It ensures that an exception is raised
        when an invalid ID is passed to the method.

        Args:
            obj_manager (DynaFlowTaskManager): The
                instance of the DynaFlowTaskManager class.
            session (AsyncSession): The instance of the AsyncSession class.

        Raises:
            Exception: If an exception is not
                raised when an invalid ID is passed.

        """
        invalid_id = "invalid_id"

        with pytest.raises(Exception):
            await obj_manager.get_by_dyna_flow_task_type_id(
                invalid_id)  # type: ignore  # noqa: E501

        await session.rollback()
    # isCanceled
    # isCancelRequested
    # isCompleted
    # isParallelRunAllowed
    # isRunTaskDebugRequired
    # isStarted
    # isSuccessful
    # maxRetryCount
    # minStartUTCDateTime
    # param1
    # param2
    # processorIdentifier
    # requestedUTCDateTime
    # resultValue
    # retryCount
    # startedUTCDateTime
