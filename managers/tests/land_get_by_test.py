# models/managers/tests/land_test.py  # pylint: disable=duplicate-code # noqa: E501
# pylint: disable=protected-access, too-many-public-methods
# pylint: disable=unused-argument
# pylint: disable=unused-import
"""
    This class contains unit tests for the
    `LandManager` class.
"""

import uuid  # noqa: F401

import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

import models
import pytest
from helpers.session_context import SessionContext
from managers.land import LandManager
from models import Land
from models.factory import LandFactory


class TestLandGetByManager:
    """
    This class contains unit tests for the
    `LandManager` class.
    """

    @pytest_asyncio.fixture(scope="function")
    async def obj_manager(self, session: AsyncSession):
        """
        Fixture that returns an instance of
        `LandManager` for testing.
        """
        session_context = SessionContext({}, session)
        session_context.customer_code = uuid.uuid4()
        return LandManager(session_context)

    @pytest.mark.asyncio
    async def test_build(
        self,
        obj_manager: LandManager
    ):
        """
        Test case for the `build` method of
        `LandManager`.
        """
        # Define mock data for our land
        mock_data = {
            "code": uuid.uuid4()
        }

        # Call the build function of the manager
        land = await \
            obj_manager.build(
                **mock_data)

        # Assert that the returned object is an instance of
        # Land
        assert isinstance(
            land,
            Land)

        # Assert that the attributes of the
        # land match our mock data
        assert land.code == mock_data["code"]

    @pytest.mark.asyncio
    async def test_get_by_id(
        self,
        obj_manager: LandManager,
        session: AsyncSession
    ):
        """
        Test case for the `get_by_id` method of
        `LandManager`.
        """
        new_obj = await \
            LandFactory.create_async(
                session)

        land = await \
            obj_manager.get_by_id(
                new_obj.land_id)

        assert isinstance(
            land,
            Land)

        assert new_obj.land_id == \
            land.land_id
        assert new_obj.code == \
            land.code

    @pytest.mark.asyncio
    async def test_get_by_id_not_found(
        self,
        obj_manager: LandManager
    ):
        """
        Test case for the `get_by_id` method of
        `LandManager` when the
        land is not found.
        """

        non_existent_id = 9999  # An ID that's not in the database

        retrieved_land = await \
            obj_manager.get_by_id(
                non_existent_id)

        assert retrieved_land is None

    @pytest.mark.asyncio
    async def test_get_by_code_returns_land(
        self,
        obj_manager: LandManager,
        session: AsyncSession
    ):
        """
        Test case for the `get_by_code` method of
        `LandManager` that checks if
        a land is
        returned by its code.
        """

        new_obj = await \
            LandFactory.create_async(
                session)

        land = await \
            obj_manager.get_by_code(
                new_obj.code)

        assert isinstance(
            land,
            Land)

        assert new_obj.land_id == \
            land.land_id
        assert new_obj.code == \
            land.code

    @pytest.mark.asyncio
    async def test_get_by_code_returns_none_for_nonexistent_code(
        self,
        obj_manager: LandManager
    ):
        """
        Test case for the `get_by_code` method of
        `LandManager` when the code does not exist.
        """
        # Generate a random UUID that doesn't correspond to
        # any Land in the database
        random_code = uuid.uuid4()

        land = await \
            obj_manager.get_by_code(
                random_code)

        assert land is None

    # description
    # displayOrder
    # isActive
    # lookupEnumName
    # name
    # PacID

    @pytest.mark.asyncio
    async def test_get_by_pac_id_existing(
        self,
        obj_manager: LandManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of the
        `get_by_pac_id` method when
        a land with
        a specific pac_id exists.

        Steps:
        1. Create a land using the
            LandFactory.
        2. Fetch the land using the
            `get_by_pac_id` method of the obj_manager.
        3. Assert that the fetched lands list contains
            only one land.
        4. Assert that the fetched land
            is an instance
            of the Land class.
        5. Assert that the code of the fetched land
            matches the code of the created land.
        6. Fetch the corresponding pac object
            using the pac_id of the created land.
        7. Assert that the fetched pac object is
            an instance of the Pac class.
        8. Assert that the pac_code_peek of the fetched
            land matches the
            code of the fetched pac.

        """
        # Add a land with a specific
        # pac_id
        obj_1 = await LandFactory.create_async(
            session=session)

        # Fetch the land using
        # the manager function

        fetched_objs = await \
            obj_manager.get_by_pac_id(
                obj_1.pac_id)
        assert len(fetched_objs) == 1
        assert isinstance(fetched_objs[0],
                          Land)
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
        obj_manager: LandManager
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
        obj_manager: LandManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of the
        `get_by_pac_id` method when an invalid pac ID is provided.

        Args:
            obj_manager (LandManager): An
                instance of the LandManager class.
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
