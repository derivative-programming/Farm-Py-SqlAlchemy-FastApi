# models/managers/tests/dft_dependency_test.py  # pylint: disable=duplicate-code
# pylint: disable=protected-access, too-many-public-methods
# pylint: disable=unused-argument
# pylint: disable=unused-import
"""
    This class contains unit tests for the
    `DFTDependencyManager` class.
"""

import uuid  # noqa: F401

import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

import models
import pytest
from helpers.session_context import SessionContext
from managers.dft_dependency import DFTDependencyManager
from models import DFTDependency
from models.factory import DFTDependencyFactory


class TestDFTDependencyGetByManager:
    """
    This class contains unit tests for the
    `DFTDependencyManager` class.
    """

    @pytest_asyncio.fixture(scope="function")
    async def obj_manager(self, session: AsyncSession):
        """
        Fixture that returns an instance of
        `DFTDependencyManager` for testing.
        """
        session_context = SessionContext({}, session)
        session_context.customer_code = uuid.uuid4()
        return DFTDependencyManager(session_context)

    @pytest.mark.asyncio
    async def test_build(
        self,
        obj_manager: DFTDependencyManager
    ):
        """
        Test case for the `build` method of
        `DFTDependencyManager`.
        """
        # Define mock data for our dft_dependency
        mock_data = {
            "code": uuid.uuid4()
        }

        # Call the build function of the manager
        dft_dependency = await \
            obj_manager.build(
                **mock_data)

        # Assert that the returned object is an instance of
        # DFTDependency
        assert isinstance(
            dft_dependency,
            DFTDependency)

        # Assert that the attributes of the
        # dft_dependency match our mock data
        assert dft_dependency.code == mock_data["code"]

    @pytest.mark.asyncio
    async def test_get_by_id(
        self,
        obj_manager: DFTDependencyManager,
        session: AsyncSession
    ):
        """
        Test case for the `get_by_id` method of
        `DFTDependencyManager`.
        """
        new_obj = await \
            DFTDependencyFactory.create_async(
                session)

        dft_dependency = await \
            obj_manager.get_by_id(
                new_obj.dft_dependency_id)

        assert isinstance(
            dft_dependency,
            DFTDependency)

        assert new_obj.dft_dependency_id == \
            dft_dependency.dft_dependency_id
        assert new_obj.code == \
            dft_dependency.code

    @pytest.mark.asyncio
    async def test_get_by_id_not_found(
        self,
        obj_manager: DFTDependencyManager
    ):
        """
        Test case for the `get_by_id` method of
        `DFTDependencyManager` when the
        dft_dependency is not found.
        """

        non_existent_id = 9999  # An ID that's not in the database

        retrieved_dft_dependency = await \
            obj_manager.get_by_id(
                non_existent_id)

        assert retrieved_dft_dependency is None

    @pytest.mark.asyncio
    async def test_get_by_code_returns_dft_dependency(
        self,
        obj_manager: DFTDependencyManager,
        session: AsyncSession
    ):
        """
        Test case for the `get_by_code` method of
        `DFTDependencyManager` that checks if
        a dft_dependency is
        returned by its code.
        """

        new_obj = await \
            DFTDependencyFactory.create_async(
                session)

        dft_dependency = await \
            obj_manager.get_by_code(
                new_obj.code)

        assert isinstance(
            dft_dependency,
            DFTDependency)

        assert new_obj.dft_dependency_id == \
            dft_dependency.dft_dependency_id
        assert new_obj.code == \
            dft_dependency.code

    @pytest.mark.asyncio
    async def test_get_by_code_returns_none_for_nonexistent_code(
        self,
        obj_manager: DFTDependencyManager
    ):
        """
        Test case for the `get_by_code` method of
        `DFTDependencyManager` when the code does not exist.
        """
        # Generate a random UUID that doesn't correspond to
        # any DFTDependency in the database
        random_code = uuid.uuid4()

        dft_dependency = await \
            obj_manager.get_by_code(
                random_code)

        assert dft_dependency is None

    # dependencyDFTaskID,
    # DynaFlowTaskID

    @pytest.mark.asyncio
    async def test_get_by_dyna_flow_task_id_existing(
        self,
        obj_manager: DFTDependencyManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of the
        `get_by_dyna_flow_task_id` method when
        a dft_dependency with
        a specific dyna_flow_task_id exists.

        Steps:
        1. Create a dft_dependency using the
            DFTDependencyFactory.
        2. Fetch the dft_dependency using the
            `get_by_dyna_flow_task_id` method of the obj_manager.
        3. Assert that the fetched dft_dependencys list contains
            only one dft_dependency.
        4. Assert that the fetched dft_dependency
            is an instance
            of the DFTDependency class.
        5. Assert that the code of the fetched dft_dependency
            matches the code of the created dft_dependency.
        6. Fetch the corresponding dyna_flow_task object
            using the dyna_flow_task_id of the created dft_dependency.
        7. Assert that the fetched dyna_flow_task object is
            an instance of the DynaFlowTask class.
        8. Assert that the dyna_flow_task_code_peek of the fetched
            dft_dependency matches the
            code of the fetched dyna_flow_task.

        """
        # Add a dft_dependency with a specific
        # dyna_flow_task_id
        obj_1 = await DFTDependencyFactory.create_async(
            session=session)

        # Fetch the dft_dependency using
        # the manager function

        fetched_objs = await \
            obj_manager.get_by_dyna_flow_task_id(
                obj_1.dyna_flow_task_id)
        assert len(fetched_objs) == 1
        assert isinstance(fetched_objs[0],
                          DFTDependency)
        assert fetched_objs[0].code == \
            obj_1.code

        stmt = select(models.DynaFlowTask).where(
            models.DynaFlowTask._dyna_flow_task_id == obj_1.dyna_flow_task_id)  # type: ignore  # noqa: E501
        result = await session.execute(stmt)
        dyna_flow_task = result.scalars().first()

        assert isinstance(dyna_flow_task, models.DynaFlowTask)

        assert fetched_objs[0].dyna_flow_task_code_peek == dyna_flow_task.code

    @pytest.mark.asyncio
    async def test_get_by_dyna_flow_task_id_nonexistent(
        self,
        obj_manager: DFTDependencyManager
    ):
        """
        Test case to verify the behavior of the
        get_by_dyna_flow_task_id method when the dyna_flow_task ID does not exist.

        This test case ensures that when a non-existent
        dyna_flow_task ID is provided to the get_by_dyna_flow_task_id method,
        an empty list is returned.
        """

        non_existent_id = 999

        fetched_objs = await \
            obj_manager.get_by_dyna_flow_task_id(
                non_existent_id)
        assert len(fetched_objs) == 0

    @pytest.mark.asyncio
    async def test_get_by_dyna_flow_task_id_invalid_type(
        self,
        obj_manager: DFTDependencyManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of the
        `get_by_dyna_flow_task_id` method when an invalid dyna_flow_task ID is provided.

        Args:
            obj_manager (DFTDependencyManager): An
                instance of the DFTDependencyManager class.
            session (AsyncSession): An instance
                of the AsyncSession class.

        Raises:
            Exception: If an exception is raised during
            the execution of the `get_by_dyna_flow_task_id` method.

        Returns:
            None
        """

        invalid_id = "invalid_id"

        with pytest.raises(Exception):
            await obj_manager.get_by_dyna_flow_task_id(
                invalid_id)  # type: ignore

        await session.rollback()
    # isPlaceholder,
