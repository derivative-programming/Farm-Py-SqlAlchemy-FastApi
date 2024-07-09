# models/managers/tests/df_maintenance_test.py  # pylint: disable=duplicate-code # noqa: E501
# pylint: disable=protected-access, too-many-public-methods
# pylint: disable=unused-argument
# pylint: disable=unused-import
"""
    This class contains unit tests for the
    `DFMaintenanceManager` class.
"""

import uuid  # noqa: F401

import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

import models
import pytest
from helpers.session_context import SessionContext
from managers.df_maintenance import DFMaintenanceManager
from models import DFMaintenance
from models.factory import DFMaintenanceFactory


class TestDFMaintenanceGetByManager:
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
    async def test_build(
        self,
        obj_manager: DFMaintenanceManager
    ):
        """
        Test case for the `build` method of
        `DFMaintenanceManager`.
        """
        # Define mock data for our df_maintenance
        mock_data = {
            "code": uuid.uuid4()
        }

        # Call the build function of the manager
        df_maintenance = await \
            obj_manager.build(
                **mock_data)

        # Assert that the returned object is an instance of
        # DFMaintenance
        assert isinstance(
            df_maintenance,
            DFMaintenance)

        # Assert that the attributes of the
        # df_maintenance match our mock data
        assert df_maintenance.code == mock_data["code"]

    @pytest.mark.asyncio
    async def test_get_by_id(
        self,
        obj_manager: DFMaintenanceManager,
        session: AsyncSession
    ):
        """
        Test case for the `get_by_id` method of
        `DFMaintenanceManager`.
        """
        new_obj = await \
            DFMaintenanceFactory.create_async(
                session)

        df_maintenance = await \
            obj_manager.get_by_id(
                new_obj.df_maintenance_id)

        assert isinstance(
            df_maintenance,
            DFMaintenance)

        assert new_obj.df_maintenance_id == \
            df_maintenance.df_maintenance_id
        assert new_obj.code == \
            df_maintenance.code

    @pytest.mark.asyncio
    async def test_get_by_id_not_found(
        self,
        obj_manager: DFMaintenanceManager
    ):
        """
        Test case for the `get_by_id` method of
        `DFMaintenanceManager` when the
        df_maintenance is not found.
        """

        non_existent_id = 9999  # An ID that's not in the database

        retrieved_df_maintenance = await \
            obj_manager.get_by_id(
                non_existent_id)

        assert retrieved_df_maintenance is None

    @pytest.mark.asyncio
    async def test_get_by_code_returns_df_maintenance(
        self,
        obj_manager: DFMaintenanceManager,
        session: AsyncSession
    ):
        """
        Test case for the `get_by_code` method of
        `DFMaintenanceManager` that checks if
        a df_maintenance is
        returned by its code.
        """

        new_obj = await \
            DFMaintenanceFactory.create_async(
                session)

        df_maintenance = await \
            obj_manager.get_by_code(
                new_obj.code)

        assert isinstance(
            df_maintenance,
            DFMaintenance)

        assert new_obj.df_maintenance_id == \
            df_maintenance.df_maintenance_id
        assert new_obj.code == \
            df_maintenance.code

    @pytest.mark.asyncio
    async def test_get_by_code_returns_none_for_nonexistent_code(
        self,
        obj_manager: DFMaintenanceManager
    ):
        """
        Test case for the `get_by_code` method of
        `DFMaintenanceManager` when the code does not exist.
        """
        # Generate a random UUID that doesn't correspond to
        # any DFMaintenance in the database
        random_code = uuid.uuid4()

        df_maintenance = await \
            obj_manager.get_by_code(
                random_code)

        assert df_maintenance is None

    # isPaused
    # isScheduledDFProcessRequestCompleted
    # isScheduledDFProcessRequestStarted
    # lastScheduledDFProcessRequestUTCDateTime
    # nextScheduledDFProcessRequestUTCDateTime
    # PacID

    @pytest.mark.asyncio
    async def test_get_by_pac_id_existing(
        self,
        obj_manager: DFMaintenanceManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of the
        `get_by_pac_id` method when
        a df_maintenance with
        a specific pac_id exists.

        Steps:
        1. Create a df_maintenance using the
            DFMaintenanceFactory.
        2. Fetch the df_maintenance using the
            `get_by_pac_id` method of the obj_manager.
        3. Assert that the fetched df_maintenances list contains
            only one df_maintenance.
        4. Assert that the fetched df_maintenance
            is an instance
            of the DFMaintenance class.
        5. Assert that the code of the fetched df_maintenance
            matches the code of the created df_maintenance.
        6. Fetch the corresponding pac object
            using the pac_id of the created df_maintenance.
        7. Assert that the fetched pac object is
            an instance of the Pac class.
        8. Assert that the pac_code_peek of the fetched
            df_maintenance matches the
            code of the fetched pac.

        """
        # Add a df_maintenance with a specific
        # pac_id
        obj_1 = await DFMaintenanceFactory.create_async(
            session=session)

        # Fetch the df_maintenance using
        # the manager function

        fetched_objs = await \
            obj_manager.get_by_pac_id(
                obj_1.pac_id)
        assert len(fetched_objs) == 1
        assert isinstance(fetched_objs[0],
                          DFMaintenance)
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
        obj_manager: DFMaintenanceManager
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
        obj_manager: DFMaintenanceManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of the
        `get_by_pac_id` method when an invalid pac ID is provided.

        Args:
            obj_manager (DFMaintenanceManager): An
                instance of the DFMaintenanceManager class.
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
    # pausedByUsername
    # pausedUTCDateTime
    # scheduledDFProcessRequestProcessorIdentifier
