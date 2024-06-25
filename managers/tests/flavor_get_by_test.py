# models/managers/tests/flavor_test.py
# pylint: disable=protected-access
# pylint: disable=unused-argument
"""
    This class contains unit tests for the
    `FlavorManager` class.
"""

import uuid

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

import models
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
    async def flavor_manager(self, session: AsyncSession):
        """
        Fixture that returns an instance of
        `FlavorManager` for testing.
        """
        session_context = SessionContext(dict(), session)
        session_context.customer_code = uuid.uuid4()
        return FlavorManager(session_context)

    @pytest.mark.asyncio
    async def test_build(
        self,
        flavor_manager: FlavorManager
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
        flavor = await flavor_manager.build(
            **mock_data)

        # Assert that the returned object is an instance of Flavor
        assert isinstance(
            flavor, Flavor)

        # Assert that the attributes of the
        # flavor match our mock data
        assert flavor.code == mock_data["code"]

    @pytest.mark.asyncio
    async def test_get_by_id(
        self,
        flavor_manager: FlavorManager,
        session: AsyncSession
    ):
        """
        Test case for the `get_by_id` method of
        `FlavorManager`.
        """
        test_flavor = await FlavorFactory.create_async(
            session)

        flavor = await \
            flavor_manager.get_by_id(
                test_flavor.flavor_id)

        assert isinstance(
            flavor, Flavor)

        assert test_flavor.flavor_id == \
            flavor.flavor_id
        assert test_flavor.code == \
            flavor.code

    @pytest.mark.asyncio
    async def test_get_by_id_not_found(
        self,
        flavor_manager: FlavorManager
    ):
        """
        Test case for the `get_by_id` method of
        `FlavorManager` when the
        flavor is not found.
        """

        non_existent_id = 9999  # An ID that's not in the database

        retrieved_flavor = await \
            flavor_manager.get_by_id(
                non_existent_id)

        assert retrieved_flavor is None

    @pytest.mark.asyncio
    async def test_get_by_code_returns_flavor(
        self,
        flavor_manager: FlavorManager,
        session: AsyncSession
    ):
        """
        Test case for the `get_by_code` method of
        `FlavorManager` that checks if
        a flavor is
        returned by its code.
        """

        test_flavor = await FlavorFactory.create_async(
            session)

        flavor = await \
            flavor_manager.get_by_code(
                test_flavor.code)

        assert isinstance(
            flavor, Flavor)

        assert test_flavor.flavor_id == \
            flavor.flavor_id
        assert test_flavor.code == \
            flavor.code

    @pytest.mark.asyncio
    async def test_get_by_code_returns_none_for_nonexistent_code(
        self,
        flavor_manager: FlavorManager
    ):
        """
        Test case for the `get_by_code` method of
        `FlavorManager` when the code does not exist.
        """
        # Generate a random UUID that doesn't correspond to
        # any Flavor in the database
        random_code = uuid.uuid4()

        flavor = await \
            flavor_manager.get_by_code(
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
        flavor_manager: FlavorManager,
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
            `get_by_pac_id` method of the flavor_manager.
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
        flavor1 = await FlavorFactory.create_async(
            session=session)

        # Fetch the flavor using
        # the manager function

        fetched_flavors = await \
            flavor_manager.get_by_pac_id(
                flavor1.pac_id)
        assert len(fetched_flavors) == 1
        assert isinstance(fetched_flavors[0], Flavor)
        assert fetched_flavors[0].code == \
            flavor1.code

        stmt = select(models.Pac).where(
            models.Pac._pac_id == flavor1.pac_id)  # type: ignore  # noqa: E501
        result = await session.execute(stmt)
        pac = result.scalars().first()

        assert isinstance(pac, models.Pac)

        assert fetched_flavors[0].pac_code_peek == pac.code

    @pytest.mark.asyncio
    async def test_get_by_pac_id_nonexistent(
        self,
        flavor_manager: FlavorManager
    ):
        """
        Test case to verify the behavior of the
        get_by_pac_id method when the pac ID does not exist.

        This test case ensures that when a non-existent
        pac ID is provided to the get_by_pac_id method,
        an empty list is returned.
        """

        non_existent_id = 999

        fetched_flavors = await \
            flavor_manager.get_by_pac_id(
                non_existent_id)
        assert len(fetched_flavors) == 0

    @pytest.mark.asyncio
    async def test_get_by_pac_id_invalid_type(
        self,
        flavor_manager: FlavorManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of the
        `get_by_pac_id` method when an invalid pac ID is provided.

        Args:
            flavor_manager (FlavorManager): An
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
            await flavor_manager.get_by_pac_id(
                invalid_id)  # type: ignore

        await session.rollback()

