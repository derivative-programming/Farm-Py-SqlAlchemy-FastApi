# models/managers/tests/organization_test.py  # pylint: disable=duplicate-code
# pylint: disable=protected-access, too-many-public-methods
# pylint: disable=unused-argument
# pylint: disable=unused-import
"""
    This class contains unit tests for the
    `OrganizationManager` class.
"""

import uuid  # noqa: F401

import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

import models
import pytest
from helpers.session_context import SessionContext
from managers.organization import OrganizationManager
from models import Organization
from models.factory import OrganizationFactory


class TestOrganizationGetByManager:
    """
    This class contains unit tests for the
    `OrganizationManager` class.
    """

    @pytest_asyncio.fixture(scope="function")
    async def obj_manager(self, session: AsyncSession):
        """
        Fixture that returns an instance of
        `OrganizationManager` for testing.
        """
        session_context = SessionContext({}, session)
        session_context.customer_code = uuid.uuid4()
        return OrganizationManager(session_context)

    @pytest.mark.asyncio
    async def test_build(
        self,
        obj_manager: OrganizationManager
    ):
        """
        Test case for the `build` method of
        `OrganizationManager`.
        """
        # Define mock data for our organization
        mock_data = {
            "code": uuid.uuid4()
        }

        # Call the build function of the manager
        organization = await \
            obj_manager.build(
                **mock_data)

        # Assert that the returned object is an instance of
        # Organization
        assert isinstance(
            organization,
            Organization)

        # Assert that the attributes of the
        # organization match our mock data
        assert organization.code == mock_data["code"]

    @pytest.mark.asyncio
    async def test_get_by_id(
        self,
        obj_manager: OrganizationManager,
        session: AsyncSession
    ):
        """
        Test case for the `get_by_id` method of
        `OrganizationManager`.
        """
        new_obj = await \
            OrganizationFactory.create_async(
                session)

        organization = await \
            obj_manager.get_by_id(
                new_obj.organization_id)

        assert isinstance(
            organization,
            Organization)

        assert new_obj.organization_id == \
            organization.organization_id
        assert new_obj.code == \
            organization.code

    @pytest.mark.asyncio
    async def test_get_by_id_not_found(
        self,
        obj_manager: OrganizationManager
    ):
        """
        Test case for the `get_by_id` method of
        `OrganizationManager` when the
        organization is not found.
        """

        non_existent_id = 9999  # An ID that's not in the database

        retrieved_organization = await \
            obj_manager.get_by_id(
                non_existent_id)

        assert retrieved_organization is None

    @pytest.mark.asyncio
    async def test_get_by_code_returns_organization(
        self,
        obj_manager: OrganizationManager,
        session: AsyncSession
    ):
        """
        Test case for the `get_by_code` method of
        `OrganizationManager` that checks if
        a organization is
        returned by its code.
        """

        new_obj = await \
            OrganizationFactory.create_async(
                session)

        organization = await \
            obj_manager.get_by_code(
                new_obj.code)

        assert isinstance(
            organization,
            Organization)

        assert new_obj.organization_id == \
            organization.organization_id
        assert new_obj.code == \
            organization.code

    @pytest.mark.asyncio
    async def test_get_by_code_returns_none_for_nonexistent_code(
        self,
        obj_manager: OrganizationManager
    ):
        """
        Test case for the `get_by_code` method of
        `OrganizationManager` when the code does not exist.
        """
        # Generate a random UUID that doesn't correspond to
        # any Organization in the database
        random_code = uuid.uuid4()

        organization = await \
            obj_manager.get_by_code(
                random_code)

        assert organization is None

    # name,
    # TacID

    @pytest.mark.asyncio
    async def test_get_by_tac_id_existing(
        self,
        obj_manager: OrganizationManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of the
        `get_by_tac_id` method when
        a organization with
        a specific tac_id exists.

        Steps:
        1. Create a organization using the
            OrganizationFactory.
        2. Fetch the organization using the
            `get_by_tac_id` method of the obj_manager.
        3. Assert that the fetched organizations list contains
            only one organization.
        4. Assert that the fetched organization
            is an instance
            of the Organization class.
        5. Assert that the code of the fetched organization
            matches the code of the created organization.
        6. Fetch the corresponding tac object
            using the tac_id of the created organization.
        7. Assert that the fetched tac object is
            an instance of the Tac class.
        8. Assert that the tac_code_peek of the fetched
            organization matches the
            code of the fetched tac.

        """
        # Add a organization with a specific
        # tac_id
        obj_1 = await OrganizationFactory.create_async(
            session=session)

        # Fetch the organization using
        # the manager function

        fetched_objs = await \
            obj_manager.get_by_tac_id(
                obj_1.tac_id)
        assert len(fetched_objs) == 1
        assert isinstance(fetched_objs[0],
                          Organization)
        assert fetched_objs[0].code == \
            obj_1.code

        stmt = select(models.Tac).where(
            models.Tac._tac_id == obj_1.tac_id)  # type: ignore  # noqa: E501
        result = await session.execute(stmt)
        tac = result.scalars().first()

        assert isinstance(tac, models.Tac)

        assert fetched_objs[0].tac_code_peek == tac.code

    @pytest.mark.asyncio
    async def test_get_by_tac_id_nonexistent(
        self,
        obj_manager: OrganizationManager
    ):
        """
        Test case to verify the behavior of the
        get_by_tac_id method when the tac ID does not exist.

        This test case ensures that when a non-existent
        tac ID is provided to the get_by_tac_id method,
        an empty list is returned.
        """

        non_existent_id = 999

        fetched_objs = await \
            obj_manager.get_by_tac_id(
                non_existent_id)
        assert len(fetched_objs) == 0

    @pytest.mark.asyncio
    async def test_get_by_tac_id_invalid_type(
        self,
        obj_manager: OrganizationManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of the
        `get_by_tac_id` method when an invalid tac ID is provided.

        Args:
            obj_manager (OrganizationManager): An
                instance of the OrganizationManager class.
            session (AsyncSession): An instance
                of the AsyncSession class.

        Raises:
            Exception: If an exception is raised during
            the execution of the `get_by_tac_id` method.

        Returns:
            None
        """

        invalid_id = "invalid_id"

        with pytest.raises(Exception):
            await obj_manager.get_by_tac_id(
                invalid_id)  # type: ignore

        await session.rollback()
