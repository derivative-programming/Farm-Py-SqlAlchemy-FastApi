# models/managers/tests/pac_test.py
# pylint: disable=protected-access
# pylint: disable=unused-argument
"""
    This class contains unit tests for the
    `PacManager` class.
"""

import uuid

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

import models
from helpers.session_context import SessionContext
from managers.pac import PacManager
from models import Pac
from models.factory import PacFactory


class TestPacGetByManager:
    """
    This class contains unit tests for the
    `PacManager` class.
    """

    @pytest_asyncio.fixture(scope="function")
    async def pac_manager(self, session: AsyncSession):
        """
        Fixture that returns an instance of
        `PacManager` for testing.
        """
        session_context = SessionContext(dict(), session)
        session_context.customer_code = uuid.uuid4()
        return PacManager(session_context)

    @pytest.mark.asyncio
    async def test_build(
        self,
        pac_manager: PacManager
    ):
        """
        Test case for the `build` method of
        `PacManager`.
        """
        # Define mock data for our pac
        mock_data = {
            "code": uuid.uuid4()
        }

        # Call the build function of the manager
        pac = await pac_manager.build(
            **mock_data)

        # Assert that the returned object is an instance of Pac
        assert isinstance(
            pac, Pac)

        # Assert that the attributes of the
        # pac match our mock data
        assert pac.code == mock_data["code"]

    @pytest.mark.asyncio
    async def test_get_by_id(
        self,
        pac_manager: PacManager,
        session: AsyncSession
    ):
        """
        Test case for the `get_by_id` method of
        `PacManager`.
        """
        test_pac = await PacFactory.create_async(
            session)

        pac = await \
            pac_manager.get_by_id(
                test_pac.pac_id)

        assert isinstance(
            pac, Pac)

        assert test_pac.pac_id == \
            pac.pac_id
        assert test_pac.code == \
            pac.code

    @pytest.mark.asyncio
    async def test_get_by_id_not_found(
        self,
        pac_manager: PacManager
    ):
        """
        Test case for the `get_by_id` method of
        `PacManager` when the
        pac is not found.
        """

        non_existent_id = 9999  # An ID that's not in the database

        retrieved_pac = await \
            pac_manager.get_by_id(
                non_existent_id)

        assert retrieved_pac is None

    @pytest.mark.asyncio
    async def test_get_by_code_returns_pac(
        self,
        pac_manager: PacManager,
        session: AsyncSession
    ):
        """
        Test case for the `get_by_code` method of
        `PacManager` that checks if
        a pac is
        returned by its code.
        """

        test_pac = await PacFactory.create_async(
            session)

        pac = await \
            pac_manager.get_by_code(
                test_pac.code)

        assert isinstance(
            pac, Pac)

        assert test_pac.pac_id == \
            pac.pac_id
        assert test_pac.code == \
            pac.code

    @pytest.mark.asyncio
    async def test_get_by_code_returns_none_for_nonexistent_code(
        self,
        pac_manager: PacManager
    ):
        """
        Test case for the `get_by_code` method of
        `PacManager` when the code does not exist.
        """
        # Generate a random UUID that doesn't correspond to
        # any Pac in the database
        random_code = uuid.uuid4()

        pac = await \
            pac_manager.get_by_code(
                random_code)

        assert pac is None

    # description,
    # displayOrder,
    # isActive,
    # lookupEnumName,
    # name,

