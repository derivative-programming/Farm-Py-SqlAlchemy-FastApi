# models/managers/tests/flavor_test.py  # pylint: disable=duplicate-code
# pylint: disable=protected-access, too-many-public-methods
# pylint: disable=unused-argument
# pylint: disable=unused-import
"""
    This class contains unit tests for the
    `FlavorManager` class.
"""

import uuid  # noqa: F401

import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

import models
import pytest
from helpers.session_context import SessionContext
from managers.flavor import FlavorManager
from models import Flavor
from models.factory import FlavorFactory


class TestFlavorGetByManager:
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
        session_context = SessionContext({}, session)
        session_context.customer_code = uuid.uuid4()
        return FlavorManager(session_context)

    @pytest.mark.asyncio
    async def test_build(
        self,
        obj_manager: FlavorManager
    ):
        """
        Test case for the `build` method of
        `FlavorManager`.
        """
        # Define mock data for our flavor
        mock_data = {
            "code": uuid.uuid4()
        }

        # Call the build function of the manager
        flavor = await \
            obj_manager.build(
                **mock_data)

        # Assert that the returned object is an instance of
        # Flavor
        assert isinstance(
            flavor,
            Flavor)

        # Assert that the attributes of the
        # flavor match our mock data
        assert flavor.code == mock_data["code"]

    @pytest.mark.asyncio
    async def test_get_by_id(
        self,
        obj_manager: FlavorManager,
        session: AsyncSession
    ):
        """
        Test case for the `get_by_id` method of
        `FlavorManager`.
        """
        new_obj = await \
            FlavorFactory.create_async(
                session)

        flavor = await \
            obj_manager.get_by_id(
                new_obj.flavor_id)

        assert isinstance(
            flavor,
            Flavor)

        assert new_obj.flavor_id == \
            flavor.flavor_id
        assert new_obj.code == \
            flavor.code

    @pytest.mark.asyncio
    async def test_get_by_id_not_found(
        self,
        obj_manager: FlavorManager
    ):
        """
        Test case for the `get_by_id` method of
        `FlavorManager` when the
        flavor is not found.
        """

        non_existent_id = 9999  # An ID that's not in the database

        retrieved_flavor = await \
            obj_manager.get_by_id(
                non_existent_id)

        assert retrieved_flavor is None

    @pytest.mark.asyncio
    async def test_get_by_code_returns_flavor(
        self,
        obj_manager: FlavorManager,
        session: AsyncSession
    ):
        """
        Test case for the `get_by_code` method of
        `FlavorManager` that checks if
        a flavor is
        returned by its code.
        """

        new_obj = await \
            FlavorFactory.create_async(
                session)

        flavor = await \
            obj_manager.get_by_code(
                new_obj.code)

        assert isinstance(
            flavor,
            Flavor)

        assert new_obj.flavor_id == \
            flavor.flavor_id
        assert new_obj.code == \
            flavor.code

    @pytest.mark.asyncio
    async def test_get_by_code_returns_none_for_nonexistent_code(
        self,
        obj_manager: FlavorManager
    ):
        """
        Test case for the `get_by_code` method of
        `FlavorManager` when the code does not exist.
        """
        # Generate a random UUID that doesn't correspond to
        # any Flavor in the database
        random_code = uuid.uuid4()

        flavor = await \
            obj_manager.get_by_code(
                random_code)

        assert flavor is None

    # description,
    # displayOrder,
    # isActive,
    # lookupEnumName,
    # name,
    # PacID

    @pytest.mark.asyncio
    async def test_get_by_pac_id_existing(
        self,
        obj_manager: FlavorManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of the
        `get_by_pac_id` method when
        a flavor with
        a specific pac_id exists.

        Steps:
        1. Create a flavor using the
            FlavorFactory.
        2. Fetch the flavor using the
            `get_by_pac_id` method of the obj_manager.
        3. Assert that the fetched flavors list contains
            only one flavor.
        4. Assert that the fetched flavor
            is an instance
            of the Flavor class.
        5. Assert that the code of the fetched flavor
            matches the code of the created flavor.
        6. Fetch the corresponding pac object
            using the pac_id of the created flavor.
        7. Assert that the fetched pac object is
            an instance of the Pac class.
        8. Assert that the pac_code_peek of the fetched
            flavor matches the
            code of the fetched pac.

        """
        # Add a flavor with a specific
        # pac_id
        obj_1 = await FlavorFactory.create_async(
            session=session)

        # Fetch the flavor using
        # the manager function

        fetched_objs = await \
            obj_manager.get_by_pac_id(
                obj_1.pac_id)
        assert len(fetched_objs) == 1
        assert isinstance(fetched_objs[0],
                          Flavor)
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
        obj_manager: FlavorManager
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
        obj_manager: FlavorManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of the
        `get_by_pac_id` method when an invalid pac ID is provided.

        Args:
            obj_manager (FlavorManager): An
                instance of the FlavorManager class.
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
