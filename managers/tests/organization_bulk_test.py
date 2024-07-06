# models/managers/tests/organization_test.py  # pylint: disable=duplicate-code
# pylint: disable=protected-access, too-many-public-methods
# pylint: disable=unused-argument
# pylint: disable=unused-import
"""
    This class contains unit tests for the
    `OrganizationManager` class.
"""

import logging
import uuid  # noqa: F401

import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

import pytest
from helpers.session_context import SessionContext
from managers.organization import OrganizationManager
from models import Organization
from models.factory import OrganizationFactory


class TestOrganizationBulkManager:
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
    async def test_add_bulk(
        self,
        obj_manager: OrganizationManager,
        session: AsyncSession
    ):
        """
        Test case for the `add_bulk` method of the
        `OrganizationManager` class.

        This test case verifies that the `add_bulk`
        method correctly adds multiple
        organizations to the database.

        Steps:
        1. Generate a list of organization data using the
            `OrganizationFactory.build_async` method.
        2. Call the `add_bulk` method of the
            `obj_manager` instance,
            passing in the
            generated organization data.
        3. Verify that the number of organizations
            returned is
            equal to the number of organizations added.
        4. For each updated organization, fetch the corresponding
            organization from the database.
        5. Verify that the fetched organization
            is an instance of the
            `Organization` class.
        6. Verify that the insert_user_id and
            last_update_user_id of the fetched
            organization match the
            customer code of the session context.
        7. Verify that the organization_id of the fetched
            organization matches the
            organization_id of the updated
            organization.

        """
        organizations_data = [
            await OrganizationFactory.build_async(session)
            for _ in range(5)]

        organizations = await obj_manager.add_bulk(
            organizations_data)

        assert len(organizations) == 5

        for updated_obj in organizations:
            result = await session.execute(
                select(Organization).filter(
                    Organization._organization_id == (
                        updated_obj.organization_id)  # type: ignore
                )
            )
            fetched_obj = result.scalars().first()

            assert isinstance(
                fetched_obj,
                Organization)

            assert str(fetched_obj.insert_user_id) == (
                str(obj_manager._session_context.customer_code))
            assert str(fetched_obj.last_update_user_id) == (
                str(obj_manager._session_context.customer_code))

            assert fetched_obj.organization_id == \
                updated_obj.organization_id

    @pytest.mark.asyncio
    async def test_update_bulk_success(
        self,
        obj_manager: OrganizationManager,
        session: AsyncSession
    ):
        """
        Test case for bulk update of organizations.

        This test case verifies the functionality of the
        `update_bulk` method in the
        `OrganizationManager` class.
        It creates two organization instances,
        updates their codes
        using the `update_bulk` method, and then verifies
        that the updates were successful by checking the
        updated codes in the database.

        Steps:
        1. Create two organization instances using the
            `OrganizationFactory.create_async` method.
        2. Generate new codes for the organizations.
        3. Update the organizations' codes
            using the `update_bulk` method.
        4. Verify that the update was successful by checking
            the updated codes in the database.

        Args:
            obj_manager (OrganizationManager):
                An instance of the
                `OrganizationManager` class.
            session (AsyncSession): An instance of the `AsyncSession` class.

        Returns:
            None
        """
        # Mocking organization instances
        obj_1 = await OrganizationFactory. \
            create_async(
                session=session)
        obj_2 = await OrganizationFactory. \
            create_async(
                session=session)
        logging.info(obj_1.__dict__)

        code_updated1 = uuid.uuid4()
        code_updated2 = uuid.uuid4()
        logging.info(code_updated1)
        logging.info(code_updated2)

        # Update organizations
        updates = [
            {
                "organization_id":
                    obj_1.organization_id,
                "code": code_updated1
            },
            {
                "organization_id":
                    obj_2.organization_id,
                "code": code_updated2
            }
        ]
        updated_organizations = await obj_manager.update_bulk(
            updates)

        logging.info('bulk update results')
        # Assertions
        assert len(updated_organizations) == 2
        logging.info(updated_organizations[0]
                     .__dict__)
        logging.info(updated_organizations[1]
                     .__dict__)

        logging.info('getall')
        organizations = await obj_manager.get_list()
        logging.info(organizations[0]
                     .__dict__)
        logging.info(organizations[1]
                     .__dict__)

        assert updated_organizations[0].code == \
            code_updated1
        assert updated_organizations[1].code == \
            code_updated2

        assert str(updated_organizations[0]
                   .last_update_user_id) == (
            str(obj_manager
                ._session_context.customer_code))

        assert str(updated_organizations[1]
                   .last_update_user_id) == (
            str(obj_manager
                ._session_context.customer_code))

        result = await session.execute(
            select(Organization).filter(
                Organization._organization_id == 1)  # type: ignore
        )
        fetched_obj = result.scalars().first()

        assert isinstance(fetched_obj,
                          Organization)

        assert fetched_obj.code == code_updated1

        result = await session.execute(
            select(Organization).filter(
                Organization._organization_id == 2)  # type: ignore
        )
        fetched_obj = result.scalars().first()

        assert isinstance(fetched_obj,
                          Organization)

        assert fetched_obj.code == code_updated2

    @pytest.mark.asyncio
    async def test_update_bulk_missing_organization_id(
        self,
        obj_manager: OrganizationManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of the `update_bulk`
        method when the organization_id is missing.

        This test case ensures that when the organization_id is
        missing in the updates list,
        an exception is raised and the session is rolled back.

        Steps:
        1. Prepare the updates list with a missing organization_id.
        2. Call the `update_bulk` method with the updates list.
        3. Assert that an exception is raised.
        4. Rollback the session to undo any changes made during the test.

        """
        # No organizations to update since
        # organization_id is missing
        updates = [{"name": "Red Rose"}]

        with pytest.raises(Exception):
            await obj_manager.update_bulk(updates)

        await session.rollback()

    @pytest.mark.asyncio
    async def test_update_bulk_organization_not_found(
        self,
        obj_manager: OrganizationManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of the update_bulk
        method when a organization is not found.

        This test case performs the following steps:
        1. Defines a list of organization updates,
            where each update
            contains a organization_id and a code.
        2. Calls the update_bulk method of the
            obj_manager with the list of updates.
        3. Expects an exception to be raised, indicating that
            the organization was not found.
        4. Rolls back the session to undo any changes made during the test.

        Note: This test assumes that the update_bulk method
        throws an exception when a
        organization is not found.

        """

        # Update organizations
        updates = [{"organization_id": 1, "code": uuid.uuid4()}]

        with pytest.raises(Exception):
            await obj_manager.update_bulk(updates)

        await session.rollback()

    @pytest.mark.asyncio
    async def test_update_bulk_invalid_type(
        self,
        obj_manager: OrganizationManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of the
        update_bulk method when invalid data types are provided.

        This test case verifies that when the update_bulk method
        is called with a list of updates containing invalid data types,
        an exception is raised. The test case also ensures
        that the session is rolled back after the test
        to maintain data integrity.

        :param obj_manager: An instance of the
            OrganizationManager class.
        :param session: An instance of the AsyncSession class.
        """

        updates = [{"organization_id": "2", "code": uuid.uuid4()}]

        with pytest.raises(Exception):
            await obj_manager.update_bulk(updates)

        await session.rollback()

    @pytest.mark.asyncio
    async def test_delete_bulk_success(
        self,
        obj_manager: OrganizationManager,
        session: AsyncSession
    ):
        """
        Test case for the delete_bulk method of the
        OrganizationManager class.

        This test verifies that the delete_bulk method
        successfully deletes multiple organizations
        from the database.

        Steps:
        1. Create two organization objects
            using the OrganizationFactory.
        2. Delete the organizations using the
            delete_bulk method
            of the obj_manager.
        3. Verify that the delete operation was successful by
            checking if the organizations
            no longer exist in the database.

        Expected Result:
        - The delete_bulk method should return True, indicating
            that the delete operation was successful.
        - The organizations should
            no longer exist in the database.

        """

        obj_1 = await OrganizationFactory.create_async(
            session=session)

        obj_2 = await OrganizationFactory.create_async(
            session=session)

        # Delete organizations
        organization_ids = [
            obj_1.organization_id,
            obj_2.organization_id
        ]
        result = await obj_manager.delete_bulk(
            organization_ids)

        assert result is True

        for organization_id in organization_ids:
            execute_result = await session.execute(
                select(Organization).filter(
                    Organization._organization_id == (
                        organization_id))  # type: ignore
            )
            fetched_obj = execute_result.scalars().first()

            assert fetched_obj is None

    @pytest.mark.asyncio
    async def test_delete_bulk_organizations_not_found(
        self,
        obj_manager: OrganizationManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of deleting bulk
        organizations when some
        organizations are not found.

        Steps:
        1. Create a organization using the
            OrganizationFactory.
        2. Assert that the created organization
            is an instance of the
            Organization class.
        3. Define a list of organization IDs to delete.
        4. Use pytest.raises to assert that an exception is
            raised when deleting the bulk organizations.
        5. Rollback the session to undo any changes made during the test.

        This test case ensures that the delete_bulk method of the
        OrganizationManager raises an exception
        when some organizations with the specified IDs are
        not found in the database.
        """
        obj_1 = await OrganizationFactory.create_async(
            session=session)

        assert isinstance(obj_1,
                          Organization)

        # Delete organizations
        organization_ids = [1, 2]

        with pytest.raises(Exception):
            await obj_manager.delete_bulk(
                organization_ids)

        await session.rollback()

    @pytest.mark.asyncio
    async def test_delete_bulk_empty_list(
        self,
        obj_manager: OrganizationManager
    ):
        """
        Test case to verify the behavior of deleting
        organizations with an empty list.

        Args:
            obj_manager (OrganizationManager): The
                instance of the
                OrganizationManager class.

        Returns:
            None

        Raises:
            AssertionError: If the result is not True.
        """

        # Delete organizations with an empty list
        organization_ids = []
        result = await obj_manager.delete_bulk(
            organization_ids)

        # Assertions
        assert result is True

    @pytest.mark.asyncio
    async def test_delete_bulk_invalid_type(
        self,
        obj_manager: OrganizationManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of the delete_bulk
        method when invalid organization IDs are provided.

        Args:
            obj_manager (OrganizationManager): The
                instance of the
                OrganizationManager class.
            session (AsyncSession): The async session object.

        Raises:
            Exception: If an exception is raised during the
                execution of the delete_bulk method.

        Returns:
            None
        """

        organization_ids = ["1", 2]

        with pytest.raises(Exception):
            await obj_manager.delete_bulk(
                organization_ids)

        await session.rollback()
