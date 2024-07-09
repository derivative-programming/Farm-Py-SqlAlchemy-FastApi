# models/managers/tests/dyna_flow_type_test.py  # pylint: disable=duplicate-code # noqa: E501
# pylint: disable=protected-access, too-many-public-methods
# pylint: disable=unused-argument
# pylint: disable=unused-import
"""
    This class contains unit tests for the
    `DynaFlowTypeManager` class.
"""

import uuid  # noqa: F401

import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

import models
import pytest
from helpers.session_context import SessionContext
from managers.dyna_flow_type import DynaFlowTypeManager
from models import DynaFlowType
from models.factory import DynaFlowTypeFactory


class TestDynaFlowTypeGetByManager:
    """
    This class contains unit tests for the
    `DynaFlowTypeManager` class.
    """

    @pytest_asyncio.fixture(scope="function")
    async def obj_manager(self, session: AsyncSession):
        """
        Fixture that returns an instance of
        `DynaFlowTypeManager` for testing.
        """
        session_context = SessionContext({}, session)
        session_context.customer_code = uuid.uuid4()
        return DynaFlowTypeManager(session_context)

    @pytest.mark.asyncio
    async def test_build(
        self,
        obj_manager: DynaFlowTypeManager
    ):
        """
        Test case for the `build` method of
        `DynaFlowTypeManager`.
        """
        # Define mock data for our dyna_flow_type
        mock_data = {
            "code": uuid.uuid4()
        }

        # Call the build function of the manager
        dyna_flow_type = await \
            obj_manager.build(
                **mock_data)

        # Assert that the returned object is an instance of
        # DynaFlowType
        assert isinstance(
            dyna_flow_type,
            DynaFlowType)

        # Assert that the attributes of the
        # dyna_flow_type match our mock data
        assert dyna_flow_type.code == mock_data["code"]

    @pytest.mark.asyncio
    async def test_get_by_id(
        self,
        obj_manager: DynaFlowTypeManager,
        session: AsyncSession
    ):
        """
        Test case for the `get_by_id` method of
        `DynaFlowTypeManager`.
        """
        new_obj = await \
            DynaFlowTypeFactory.create_async(
                session)

        dyna_flow_type = await \
            obj_manager.get_by_id(
                new_obj.dyna_flow_type_id)

        assert isinstance(
            dyna_flow_type,
            DynaFlowType)

        assert new_obj.dyna_flow_type_id == \
            dyna_flow_type.dyna_flow_type_id
        assert new_obj.code == \
            dyna_flow_type.code

    @pytest.mark.asyncio
    async def test_get_by_id_not_found(
        self,
        obj_manager: DynaFlowTypeManager
    ):
        """
        Test case for the `get_by_id` method of
        `DynaFlowTypeManager` when the
        dyna_flow_type is not found.
        """

        non_existent_id = 9999  # An ID that's not in the database

        retrieved_dyna_flow_type = await \
            obj_manager.get_by_id(
                non_existent_id)

        assert retrieved_dyna_flow_type is None

    @pytest.mark.asyncio
    async def test_get_by_code_returns_dyna_flow_type(
        self,
        obj_manager: DynaFlowTypeManager,
        session: AsyncSession
    ):
        """
        Test case for the `get_by_code` method of
        `DynaFlowTypeManager` that checks if
        a dyna_flow_type is
        returned by its code.
        """

        new_obj = await \
            DynaFlowTypeFactory.create_async(
                session)

        dyna_flow_type = await \
            obj_manager.get_by_code(
                new_obj.code)

        assert isinstance(
            dyna_flow_type,
            DynaFlowType)

        assert new_obj.dyna_flow_type_id == \
            dyna_flow_type.dyna_flow_type_id
        assert new_obj.code == \
            dyna_flow_type.code

    @pytest.mark.asyncio
    async def test_get_by_code_returns_none_for_nonexistent_code(
        self,
        obj_manager: DynaFlowTypeManager
    ):
        """
        Test case for the `get_by_code` method of
        `DynaFlowTypeManager` when the code does not exist.
        """
        # Generate a random UUID that doesn't correspond to
        # any DynaFlowType in the database
        random_code = uuid.uuid4()

        dyna_flow_type = await \
            obj_manager.get_by_code(
                random_code)

        assert dyna_flow_type is None

    # description
    # displayOrder
    # isActive
    # lookupEnumName
    # name
    # PacID

    @pytest.mark.asyncio
    async def test_get_by_pac_id_existing(
        self,
        obj_manager: DynaFlowTypeManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of the
        `get_by_pac_id` method when
        a dyna_flow_type with
        a specific pac_id exists.

        Steps:
        1. Create a dyna_flow_type using the
            DynaFlowTypeFactory.
        2. Fetch the dyna_flow_type using the
            `get_by_pac_id` method of the obj_manager.
        3. Assert that the fetched dyna_flow_types list contains
            only one dyna_flow_type.
        4. Assert that the fetched dyna_flow_type
            is an instance
            of the DynaFlowType class.
        5. Assert that the code of the fetched dyna_flow_type
            matches the code of the created dyna_flow_type.
        6. Fetch the corresponding pac object
            using the pac_id of the created dyna_flow_type.
        7. Assert that the fetched pac object is
            an instance of the Pac class.
        8. Assert that the pac_code_peek of the fetched
            dyna_flow_type matches the
            code of the fetched pac.

        """
        # Add a dyna_flow_type with a specific
        # pac_id
        obj_1 = await DynaFlowTypeFactory.create_async(
            session=session)

        # Fetch the dyna_flow_type using
        # the manager function

        fetched_objs = await \
            obj_manager.get_by_pac_id(
                obj_1.pac_id)
        assert len(fetched_objs) == 1
        assert isinstance(fetched_objs[0],
                          DynaFlowType)
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
        obj_manager: DynaFlowTypeManager
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
        obj_manager: DynaFlowTypeManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of the
        `get_by_pac_id` method when an invalid pac ID is provided.

        Args:
            obj_manager (DynaFlowTypeManager): An
                instance of the DynaFlowTypeManager class.
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
    # priorityLevel
