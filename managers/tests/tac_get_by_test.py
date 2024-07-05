# models/managers/tests/tac_test.py
# pylint: disable=protected-access
# pylint: disable=unused-argument
# pylint: disable=unused-import
"""
    This class contains unit tests for the
    `TacManager` class.
"""

import uuid  # noqa: F401

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

import models
from helpers.session_context import SessionContext
from managers.tac import (
    TacManager)
from models import Tac
from models.factory import (
    TacFactory)


class TestTacGetByManager:
    """
    This class contains unit tests for the
    `TacManager` class.
    """

    @pytest_asyncio.fixture(scope="function")
    async def obj_manager(self, session: AsyncSession):
        """
        Fixture that returns an instance of
        `TacManager` for testing.
        """
        session_context = SessionContext({}, session)
        session_context.customer_code = uuid.uuid4()
        return TacManager(session_context)

    @pytest.mark.asyncio
    async def test_build(
        self,
        obj_manager: TacManager
    ):
        """
        Test case for the `build` method of
        `TacManager`.
        """
        # Define mock data for our tac
        mock_data = {
            "code": uuid.uuid4()
        }

        # Call the build function of the manager
        tac = await \
            obj_manager.build(
                **mock_data)

        # Assert that the returned object is an instance of
        # Tac
        assert isinstance(
            tac,
            Tac)

        # Assert that the attributes of the
        # tac match our mock data
        assert tac.code == mock_data["code"]

    @pytest.mark.asyncio
    async def test_get_by_id(
        self,
        obj_manager: TacManager,
        session: AsyncSession
    ):
        """
        Test case for the `get_by_id` method of
        `TacManager`.
        """
        new_obj = await \
            TacFactory.create_async(
                session)

        tac = await \
            obj_manager.get_by_id(
                new_obj.tac_id)

        assert isinstance(
            tac,
            Tac)

        assert new_obj.tac_id == \
            tac.tac_id
        assert new_obj.code == \
            tac.code

    @pytest.mark.asyncio
    async def test_get_by_id_not_found(
        self,
        obj_manager: TacManager
    ):
        """
        Test case for the `get_by_id` method of
        `TacManager` when the
        tac is not found.
        """

        non_existent_id = 9999  # An ID that's not in the database

        retrieved_tac = await \
            obj_manager.get_by_id(
                non_existent_id)

        assert retrieved_tac is None

    @pytest.mark.asyncio
    async def test_get_by_code_returns_tac(
        self,
        obj_manager: TacManager,
        session: AsyncSession
    ):
        """
        Test case for the `get_by_code` method of
        `TacManager` that checks if
        a tac is
        returned by its code.
        """

        new_obj = await \
            TacFactory.create_async(
                session)

        tac = await \
            obj_manager.get_by_code(
                new_obj.code)

        assert isinstance(
            tac,
            Tac)

        assert new_obj.tac_id == \
            tac.tac_id
        assert new_obj.code == \
            tac.code

    @pytest.mark.asyncio
    async def test_get_by_code_returns_none_for_nonexistent_code(
        self,
        obj_manager: TacManager
    ):
        """
        Test case for the `get_by_code` method of
        `TacManager` when the code does not exist.
        """
        # Generate a random UUID that doesn't correspond to
        # any Tac in the database
        random_code = uuid.uuid4()

        tac = await \
            obj_manager.get_by_code(
                random_code)

        assert tac is None

    # description,
    # displayOrder,
    # isActive,
    # lookupEnumName,
    # name,
    # PacID

    @pytest.mark.asyncio
    async def test_get_by_pac_id_existing(
        self,
        obj_manager: TacManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of the
        `get_by_pac_id` method when
        a tac with
        a specific pac_id exists.

        Steps:
        1. Create a tac using the
            TacFactory.
        2. Fetch the tac using the
            `get_by_pac_id` method of the obj_manager.
        3. Assert that the fetched tacs list contains
            only one tac.
        4. Assert that the fetched tac
            is an instance
            of the Tac class.
        5. Assert that the code of the fetched tac
            matches the code of the created tac.
        6. Fetch the corresponding pac object
            using the pac_id of the created tac.
        7. Assert that the fetched pac object is
            an instance of the Pac class.
        8. Assert that the pac_code_peek of the fetched
            tac matches the
            code of the fetched pac.

        """
        # Add a tac with a specific
        # pac_id
        obj_1 = await TacFactory.create_async(
            session=session)

        # Fetch the tac using
        # the manager function

        fetched_objs = await \
            obj_manager.get_by_pac_id(
                obj_1.pac_id)
        assert len(fetched_objs) == 1
        assert isinstance(fetched_objs[0],
                          Tac)
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
        obj_manager: TacManager
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
        obj_manager: TacManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of the
        `get_by_pac_id` method when an invalid pac ID is provided.

        Args:
            obj_manager (TacManager): An
                instance of the TacManager class.
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
