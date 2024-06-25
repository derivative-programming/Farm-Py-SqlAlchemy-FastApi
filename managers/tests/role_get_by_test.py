# models/managers/tests/role_test.py
# pylint: disable=protected-access
# pylint: disable=unused-argument
"""
    This class contains unit tests for the
    `RoleManager` class.
"""

import uuid

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

import models
from helpers.session_context import SessionContext
from managers.role import RoleManager
from models import Role
from models.factory import RoleFactory


class TestRoleGetByManager:
    """
    This class contains unit tests for the
    `RoleManager` class.
    """

    @pytest_asyncio.fixture(scope="function")
    async def role_manager(self, session: AsyncSession):
        """
        Fixture that returns an instance of
        `RoleManager` for testing.
        """
        session_context = SessionContext(dict(), session)
        session_context.customer_code = uuid.uuid4()
        return RoleManager(session_context)

    @pytest.mark.asyncio
    async def test_build(
        self,
        role_manager: RoleManager
    ):
        """
        Test case for the `build` method of
        `RoleManager`.
        """
        # Define mock data for our role
        mock_data = {
            "code": uuid.uuid4()
        }

        # Call the build function of the manager
        role = await role_manager.build(
            **mock_data)

        # Assert that the returned object is an instance of Role
        assert isinstance(
            role, Role)

        # Assert that the attributes of the
        # role match our mock data
        assert role.code == mock_data["code"]

    @pytest.mark.asyncio
    async def test_get_by_id(
        self,
        role_manager: RoleManager,
        session: AsyncSession
    ):
        """
        Test case for the `get_by_id` method of
        `RoleManager`.
        """
        test_role = await RoleFactory.create_async(
            session)

        role = await role_manager.get_by_id(
            test_role.role_id)

        assert isinstance(
            role, Role)

        assert test_role.role_id == \
            role.role_id
        assert test_role.code == \
            role.code

    @pytest.mark.asyncio
    async def test_get_by_id_not_found(
        self,
        role_manager: RoleManager
    ):
        """
        Test case for the `get_by_id` method of
        `RoleManager` when the
        role is not found.
        """

        non_existent_id = 9999  # An ID that's not in the database

        retrieved_role = await role_manager.get_by_id(
            non_existent_id)

        assert retrieved_role is None

    @pytest.mark.asyncio
    async def test_get_by_code_returns_role(
        self,
        role_manager: RoleManager,
        session: AsyncSession
    ):
        """
        Test case for the `get_by_code` method of
        `RoleManager` that checks if
        a role is
        returned by its code.
        """

        test_role = await RoleFactory.create_async(
            session)

        role = await role_manager.get_by_code(
            test_role.code)

        assert isinstance(
            role, Role)

        assert test_role.role_id == \
            role.role_id
        assert test_role.code == \
            role.code

    @pytest.mark.asyncio
    async def test_get_by_code_returns_none_for_nonexistent_code(
        self,
        role_manager: RoleManager
    ):
        """
        Test case for the `get_by_code` method of
        `RoleManager` when the code does not exist.
        """
        # Generate a random UUID that doesn't correspond to
        # any Role in the database
        random_code = uuid.uuid4()

        role = await role_manager.get_by_code(
            random_code)

        assert role is None

    # description,
    # displayOrder,
    # isActive,
    # lookupEnumName,
    # name,
    # PacID

    @pytest.mark.asyncio
    async def test_get_by_pac_id_existing(
        self,
        role_manager: RoleManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of the
        `get_by_pac_id` method when
        a role with
        a specific pac_id exists.

        Steps:
        1. Create a role using the
            RoleFactory.
        2. Fetch the role using the
            `get_by_pac_id` method of the role_manager.
        3. Assert that the fetched roles list contains
            only one role.
        4. Assert that the fetched role
            is an instance
            of the Role class.
        5. Assert that the code of the fetched role
            matches the code of the created role.
        6. Fetch the corresponding pac object
            using the pac_id of the created role.
        7. Assert that the fetched pac object is
            an instance of the Pac class.
        8. Assert that the pac_code_peek of the fetched
            role matches the
            code of the fetched pac.

        """
        # Add a role with a specific
        # pac_id
        role1 = await RoleFactory.create_async(
            session=session)

        # Fetch the role using
        # the manager function

        fetched_roles = await role_manager.get_by_pac_id(
            role1.pac_id)
        assert len(fetched_roles) == 1
        assert isinstance(fetched_roles[0], Role)
        assert fetched_roles[0].code == \
            role1.code

        stmt = select(models.Pac).where(
            models.Pac._pac_id == role1.pac_id)  # type: ignore  # noqa: E501
        result = await session.execute(stmt)
        pac = result.scalars().first()

        assert isinstance(pac, models.Pac)

        assert fetched_roles[0].pac_code_peek == pac.code

    @pytest.mark.asyncio
    async def test_get_by_pac_id_nonexistent(
        self,
        role_manager: RoleManager
    ):
        """
        Test case to verify the behavior of the
        get_by_pac_id method when the pac ID does not exist.

        This test case ensures that when a non-existent
        pac ID is provided to the get_by_pac_id method,
        an empty list is returned.
        """

        non_existent_id = 999

        fetched_roles = await role_manager.get_by_pac_id(
            non_existent_id)
        assert len(fetched_roles) == 0

    @pytest.mark.asyncio
    async def test_get_by_pac_id_invalid_type(
        self,
        role_manager: RoleManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of the
        `get_by_pac_id` method when an invalid pac ID is provided.

        Args:
            role_manager (RoleManager): An
                instance of the RoleManager class.
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
            await role_manager.get_by_pac_id(
                invalid_id)  # type: ignore

        await session.rollback()

