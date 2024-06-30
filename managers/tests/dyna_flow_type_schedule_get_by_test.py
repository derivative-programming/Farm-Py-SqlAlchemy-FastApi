# models/managers/tests/dyna_flow_type_schedule_test.py
# pylint: disable=protected-access
# pylint: disable=unused-argument
# pylint: disable=unused-import
"""
    This class contains unit tests for the
    `DynaFlowTypeScheduleManager` class.
"""

import uuid  # noqa: F401

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

import models
from helpers.session_context import SessionContext
from managers.dyna_flow_type_schedule import (
    DynaFlowTypeScheduleManager)
from models import DynaFlowTypeSchedule
from models.factory import (
    DynaFlowTypeScheduleFactory)


class TestDynaFlowTypeScheduleGetByManager:
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
        session_context = SessionContext(dict(), session)
        session_context.customer_code = uuid.uuid4()
        return DynaFlowTypeScheduleManager(session_context)

    @pytest.mark.asyncio
    async def test_build(
        self,
        obj_manager: DynaFlowTypeScheduleManager
    ):
        """
        Test case for the `build` method of
        `DynaFlowTypeScheduleManager`.
        """
        # Define mock data for our dyna_flow_type_schedule
        mock_data = {
            "code": uuid.uuid4()
        }

        # Call the build function of the manager
        dyna_flow_type_schedule = await \
            obj_manager.build(
                **mock_data)

        # Assert that the returned object is an instance of
        # DynaFlowTypeSchedule
        assert isinstance(
            dyna_flow_type_schedule,
            DynaFlowTypeSchedule)

        # Assert that the attributes of the
        # dyna_flow_type_schedule match our mock data
        assert dyna_flow_type_schedule.code == mock_data["code"]

    @pytest.mark.asyncio
    async def test_get_by_id(
        self,
        obj_manager: DynaFlowTypeScheduleManager,
        session: AsyncSession
    ):
        """
        Test case for the `get_by_id` method of
        `DynaFlowTypeScheduleManager`.
        """
        new_obj = await \
            DynaFlowTypeScheduleFactory.create_async(
                session)

        dyna_flow_type_schedule = await \
            obj_manager.get_by_id(
                new_obj.dyna_flow_type_schedule_id)

        assert isinstance(
            dyna_flow_type_schedule,
            DynaFlowTypeSchedule)

        assert new_obj.dyna_flow_type_schedule_id == \
            dyna_flow_type_schedule.dyna_flow_type_schedule_id
        assert new_obj.code == \
            dyna_flow_type_schedule.code

    @pytest.mark.asyncio
    async def test_get_by_id_not_found(
        self,
        obj_manager: DynaFlowTypeScheduleManager
    ):
        """
        Test case for the `get_by_id` method of
        `DynaFlowTypeScheduleManager` when the
        dyna_flow_type_schedule is not found.
        """

        non_existent_id = 9999  # An ID that's not in the database

        retrieved_dyna_flow_type_schedule = await \
            obj_manager.get_by_id(
                non_existent_id)

        assert retrieved_dyna_flow_type_schedule is None

    @pytest.mark.asyncio
    async def test_get_by_code_returns_dyna_flow_type_schedule(
        self,
        obj_manager: DynaFlowTypeScheduleManager,
        session: AsyncSession
    ):
        """
        Test case for the `get_by_code` method of
        `DynaFlowTypeScheduleManager` that checks if
        a dyna_flow_type_schedule is
        returned by its code.
        """

        new_obj = await \
            DynaFlowTypeScheduleFactory.create_async(
                session)

        dyna_flow_type_schedule = await \
            obj_manager.get_by_code(
                new_obj.code)

        assert isinstance(
            dyna_flow_type_schedule,
            DynaFlowTypeSchedule)

        assert new_obj.dyna_flow_type_schedule_id == \
            dyna_flow_type_schedule.dyna_flow_type_schedule_id
        assert new_obj.code == \
            dyna_flow_type_schedule.code

    @pytest.mark.asyncio
    async def test_get_by_code_returns_none_for_nonexistent_code(
        self,
        obj_manager: DynaFlowTypeScheduleManager
    ):
        """
        Test case for the `get_by_code` method of
        `DynaFlowTypeScheduleManager` when the code does not exist.
        """
        # Generate a random UUID that doesn't correspond to
        # any DynaFlowTypeSchedule in the database
        random_code = uuid.uuid4()

        dyna_flow_type_schedule = await \
            obj_manager.get_by_code(
                random_code)

        assert dyna_flow_type_schedule is None

    # DynaFlowTypeID

    @pytest.mark.asyncio
    async def test_get_by_dyna_flow_type_id_existing(
        self,
        obj_manager: DynaFlowTypeScheduleManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of the
        `get_by_dyna_flow_type_id` method
        when a dyna_flow_type_schedule with a
        specific dyna_flow_type_id exists.

        Steps:
        1. Create a dyna_flow_type_schedule using the
            DynaFlowTypeScheduleFactory.
        2. Fetch the dyna_flow_type_schedule using the
            `get_by_dyna_flow_type_id`
            method of the obj_manager.
        3. Assert that the fetched dyna_flow_type_schedules list has a length of 1.
        4. Assert that the first element in the fetched
            dyna_flow_type_schedules list is an instance of the
            DynaFlowTypeSchedule class.
        5. Assert that the code of the fetched
            dyna_flow_type_schedule
            matches the code of the created dyna_flow_type_schedule.
        6. Execute a select statement to fetch the
            DynaFlowType object associated with the
            dyna_flow_type_id.
        7. Assert that the fetched dyna_flow_type is an
            instance of the DynaFlowType class.
        8. Assert that the dyna_flow_type_code_peek
            of the fetched dyna_flow_type_schedule matches
            the code of the fetched dyna_flow_type.
        """
        # Add a dyna_flow_type_schedule with a specific
        # dyna_flow_type_id
        obj_1 = await DynaFlowTypeScheduleFactory.create_async(
            session=session)

        # Fetch the dyna_flow_type_schedule using the
        # manager function

        fetched_objs = await \
            obj_manager.get_by_dyna_flow_type_id(
                obj_1.dyna_flow_type_id)
        assert len(fetched_objs) == 1
        assert isinstance(fetched_objs[0],
                          DynaFlowTypeSchedule)
        assert fetched_objs[0].code == \
            obj_1.code

        stmt = select(models.DynaFlowType).where(
            models.DynaFlowType._dyna_flow_type_id == obj_1.dyna_flow_type_id)  # type: ignore  # noqa: E501
        result = await session.execute(stmt)
        dyna_flow_type = result.scalars().first()

        assert isinstance(dyna_flow_type, models.DynaFlowType)

        assert fetched_objs[0].dyna_flow_type_code_peek == dyna_flow_type.code

    @pytest.mark.asyncio
    async def test_get_by_dyna_flow_type_id_nonexistent(
        self,
        obj_manager: DynaFlowTypeScheduleManager
    ):
        """
        Test case to verify the behavior of the
        'get_by_dyna_flow_type_id' method
        when the provided foreign key ID does
        not exist in the database.

        This test ensures that when a non-existent
        foreign key ID is passed to the
        'get_by_dyna_flow_type_id' method, it
        returns an empty list.

        Steps:
        1. Set a non-existent foreign key ID.
        2. Call the 'get_by_dyna_flow_type_id'
            method with the non-existent ID.
        3. Assert that the returned list of fetched dyna_flow_type_schedules is empty.

        """
        non_existent_id = 999

        fetched_objs = (
            await obj_manager.get_by_dyna_flow_type_id(
                non_existent_id))
        assert len(fetched_objs) == 0

    @pytest.mark.asyncio
    async def test_get_by_dyna_flow_type_id_invalid_type(
        self,
        obj_manager: DynaFlowTypeScheduleManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of the
        `get_by_dyna_flow_type_id` method
        when an invalid foreign key ID type is provided.

        It ensures that an exception is raised
        when an invalid ID is passed to the method.

        Args:
            obj_manager (DynaFlowTypeScheduleManager): The
                instance of the DynaFlowTypeScheduleManager class.
            session (AsyncSession): The instance of the AsyncSession class.

        Raises:
            Exception: If an exception is not
                raised when an invalid ID is passed.

        """
        invalid_id = "invalid_id"

        with pytest.raises(Exception):
            await obj_manager.get_by_dyna_flow_type_id(
                invalid_id)  # type: ignore  # noqa: E501

        await session.rollback()
    # frequencyInHours,
    # isActive,
    # lastUTCDateTime
    # nextUTCDateTime
    # PacID

    @pytest.mark.asyncio
    async def test_get_by_pac_id_existing(
        self,
        obj_manager: DynaFlowTypeScheduleManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of the
        `get_by_pac_id` method when
        a dyna_flow_type_schedule with
        a specific pac_id exists.

        Steps:
        1. Create a dyna_flow_type_schedule using the
            DynaFlowTypeScheduleFactory.
        2. Fetch the dyna_flow_type_schedule using the
            `get_by_pac_id` method of the obj_manager.
        3. Assert that the fetched dyna_flow_type_schedules list contains
            only one dyna_flow_type_schedule.
        4. Assert that the fetched dyna_flow_type_schedule
            is an instance
            of the DynaFlowTypeSchedule class.
        5. Assert that the code of the fetched dyna_flow_type_schedule
            matches the code of the created dyna_flow_type_schedule.
        6. Fetch the corresponding pac object
            using the pac_id of the created dyna_flow_type_schedule.
        7. Assert that the fetched pac object is
            an instance of the Pac class.
        8. Assert that the pac_code_peek of the fetched
            dyna_flow_type_schedule matches the
            code of the fetched pac.

        """
        # Add a dyna_flow_type_schedule with a specific
        # pac_id
        obj_1 = await DynaFlowTypeScheduleFactory.create_async(
            session=session)

        # Fetch the dyna_flow_type_schedule using
        # the manager function

        fetched_objs = await \
            obj_manager.get_by_pac_id(
                obj_1.pac_id)
        assert len(fetched_objs) == 1
        assert isinstance(fetched_objs[0],
                          DynaFlowTypeSchedule)
        assert fetched_objs[0].code == \
            obj_1.code

        stmt = select(models.Pac).where(
            models.Pac._pac_id == obj_1.pac_id)  # type: ignore  # noqa: E501
        result = await session.execute(stmt)
        pac = result.scalars().first()

        assert isinstance(pac, models.Pac)

        assert fetched_objs[0].pac_code_peek == pac.code

    @pytest.mark.asyncio
    async def test_get_by_pac_id_nonexistent(
        self,
        obj_manager: DynaFlowTypeScheduleManager
    ):
        """
        Test case to verify the behavior of the
        get_by_pac_id method when the pac ID does not exist.

        This test case ensures that when a non-existent
        pac ID is provided to the get_by_pac_id method,
        an empty list is returned.
        """

        non_existent_id = 999

        fetched_objs = await \
            obj_manager.get_by_pac_id(
                non_existent_id)
        assert len(fetched_objs) == 0

    @pytest.mark.asyncio
    async def test_get_by_pac_id_invalid_type(
        self,
        obj_manager: DynaFlowTypeScheduleManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of the
        `get_by_pac_id` method when an invalid pac ID is provided.

        Args:
            obj_manager (DynaFlowTypeScheduleManager): An
                instance of the DynaFlowTypeScheduleManager class.
            session (AsyncSession): An instance
                of the AsyncSession class.

        Raises:
            Exception: If an exception is raised during
            the execution of the `get_by_pac_id` method.

        Returns:
            None
        """

        invalid_id = "invalid_id"

        with pytest.raises(Exception):
            await obj_manager.get_by_pac_id(
                invalid_id)  # type: ignore

        await session.rollback()
