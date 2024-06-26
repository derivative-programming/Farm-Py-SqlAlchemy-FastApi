# models/managers/tests/role_test.py
# pylint: disable=protected-access
# pylint: disable=unused-argument
# pylint: disable=unused-import
"""
    This class contains unit tests for the
    `RoleManager` class.
"""

import logging
import uuid  # noqa: F401

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from helpers.session_context import SessionContext
from managers.role import (
    RoleManager)
from models import Role
from models.factory import (
    RoleFactory)


class TestRoleBulkManager:
    """
    This class contains unit tests for the
    `RoleManager` class.
    """

    @pytest_asyncio.fixture(scope="function")
    async def obj_manager(self, session: AsyncSession):
        """
        Fixture that returns an instance of
        `RoleManager` for testing.
        """
        session_context = SessionContext(dict(), session)
        session_context.customer_code = uuid.uuid4()
        return RoleManager(session_context)

    @pytest.mark.asyncio
    async def test_add_bulk(
        self,
        obj_manager: RoleManager,
        session: AsyncSession
    ):
        """
        Test case for the `add_bulk` method of the
        `RoleManager` class.

        This test case verifies that the `add_bulk`
        method correctly adds multiple
        roles to the database.

        Steps:
        1. Generate a list of role data using the
            `RoleFactory.build_async` method.
        2. Call the `add_bulk` method of the
            `obj_manager` instance,
            passing in the
            generated role data.
        3. Verify that the number of roles
            returned is
            equal to the number of roles added.
        4. For each updated role, fetch the corresponding
            role from the database.
        5. Verify that the fetched role
            is an instance of the
            `Role` class.
        6. Verify that the insert_user_id and
            last_update_user_id of the fetched
            role match the
            customer code of the session context.
        7. Verify that the role_id of the fetched
            role matches the
            role_id of the updated
            role.

        """
        roles_data = [
            await RoleFactory.build_async(session) for _ in range(5)]

        roles = await obj_manager.add_bulk(
            roles_data)

        assert len(roles) == 5

        for updated_obj in roles:
            result = await session.execute(
                select(Role).filter(
                    Role._role_id == (
                        updated_obj.role_id)  # type: ignore
                )
            )
            fetched_obj = result.scalars().first()

            assert isinstance(
                fetched_obj,
                Role)

            assert str(fetched_obj.insert_user_id) == (
                str(obj_manager._session_context.customer_code))
            assert str(fetched_obj.last_update_user_id) == (
                str(obj_manager._session_context.customer_code))

            assert fetched_obj.role_id == \
                updated_obj.role_id

    @pytest.mark.asyncio
    async def test_update_bulk_success(
        self,
        obj_manager: RoleManager,
        session: AsyncSession
    ):
        """
        Test case for bulk update of roles.

        This test case verifies the functionality of the
        `update_bulk` method in the
        `RoleManager` class.
        It creates two role instances,
        updates their codes
        using the `update_bulk` method, and then verifies
        that the updates were successful by checking the
        updated codes in the database.

        Steps:
        1. Create two role instances using the
            `RoleFactory.create_async` method.
        2. Generate new codes for the roles.
        3. Update the roles' codes
            using the `update_bulk` method.
        4. Verify that the update was successful by checking
            the updated codes in the database.

        Args:
            obj_manager (RoleManager):
                An instance of the
                `RoleManager` class.
            session (AsyncSession): An instance of the `AsyncSession` class.

        Returns:
            None
        """
        # Mocking role instances
        obj_1 = await RoleFactory. \
            create_async(
                session=session)
        obj_2 = await RoleFactory. \
            create_async(
                session=session)
        logging.info(obj_1.__dict__)

        code_updated1 = uuid.uuid4()
        code_updated2 = uuid.uuid4()
        logging.info(code_updated1)
        logging.info(code_updated2)

        # Update roles
        updates = [
            {
                "role_id":
                    obj_1.role_id,
                "code": code_updated1
            },
            {
                "role_id":
                    obj_2.role_id,
                "code": code_updated2
            }
        ]
        updated_roles = await obj_manager.update_bulk(
            updates)

        logging.info('bulk update results')
        # Assertions
        assert len(updated_roles) == 2
        logging.info(updated_roles[0]
                     .__dict__)
        logging.info(updated_roles[1]
                     .__dict__)

        logging.info('getall')
        roles = await obj_manager.get_list()
        logging.info(roles[0]
                     .__dict__)
        logging.info(roles[1]
                     .__dict__)

        assert updated_roles[0].code == \
            code_updated1
        assert updated_roles[1].code == \
            code_updated2

        assert str(updated_roles[0]
                   .last_update_user_id) == (
            str(obj_manager
                ._session_context.customer_code))

        assert str(updated_roles[1]
                   .last_update_user_id) == (
            str(obj_manager
                ._session_context.customer_code))

        result = await session.execute(
            select(Role).filter(
                Role._role_id == 1)  # type: ignore
        )
        fetched_obj = result.scalars().first()

        assert isinstance(fetched_obj,
                          Role)

        assert fetched_obj.code == code_updated1

        result = await session.execute(
            select(Role).filter(
                Role._role_id == 2)  # type: ignore
        )
        fetched_obj = result.scalars().first()

        assert isinstance(fetched_obj,
                          Role)

        assert fetched_obj.code == code_updated2

    @pytest.mark.asyncio
    async def test_update_bulk_missing_role_id(
        self,
        obj_manager: RoleManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of the `update_bulk`
        method when the role_id is missing.

        This test case ensures that when the role_id is
        missing in the updates list,
        an exception is raised and the session is rolled back.

        Steps:
        1. Prepare the updates list with a missing role_id.
        2. Call the `update_bulk` method with the updates list.
        3. Assert that an exception is raised.
        4. Rollback the session to undo any changes made during the test.

        """
        # No roles to update since
        # role_id is missing
        updates = [{"name": "Red Rose"}]

        with pytest.raises(Exception):
            await obj_manager.update_bulk(updates)

        await session.rollback()

    @pytest.mark.asyncio
    async def test_update_bulk_role_not_found(
        self,
        obj_manager: RoleManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of the update_bulk
        method when a role is not found.

        This test case performs the following steps:
        1. Defines a list of role updates,
            where each update
            contains a role_id and a code.
        2. Calls the update_bulk method of the
            obj_manager with the list of updates.
        3. Expects an exception to be raised, indicating that
            the role was not found.
        4. Rolls back the session to undo any changes made during the test.

        Note: This test assumes that the update_bulk method
        throws an exception when a
        role is not found.

        """

        # Update roles
        updates = [{"role_id": 1, "code": uuid.uuid4()}]

        with pytest.raises(Exception):
            await obj_manager.update_bulk(updates)

        await session.rollback()

    @pytest.mark.asyncio
    async def test_update_bulk_invalid_type(
        self,
        obj_manager: RoleManager,
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
            RoleManager class.
        :param session: An instance of the AsyncSession class.
        """

        updates = [{"role_id": "2", "code": uuid.uuid4()}]

        with pytest.raises(Exception):
            await obj_manager.update_bulk(updates)

        await session.rollback()

    @pytest.mark.asyncio
    async def test_delete_bulk_success(
        self,
        obj_manager: RoleManager,
        session: AsyncSession
    ):
        """
        Test case for the delete_bulk method of the
        RoleManager class.

        This test verifies that the delete_bulk method
        successfully deletes multiple roles
        from the database.

        Steps:
        1. Create two role objects
            using the RoleFactory.
        2. Delete the roles using the
            delete_bulk method
            of the obj_manager.
        3. Verify that the delete operation was successful by
            checking if the roles
            no longer exist in the database.

        Expected Result:
        - The delete_bulk method should return True, indicating
            that the delete operation was successful.
        - The roles should
            no longer exist in the database.

        """

        obj_1 = await RoleFactory.create_async(
            session=session)

        obj_2 = await RoleFactory.create_async(
            session=session)

        # Delete roles
        role_ids = [
            obj_1.role_id,
            obj_2.role_id
        ]
        result = await obj_manager.delete_bulk(
            role_ids)

        assert result is True

        for role_id in role_ids:
            execute_result = await session.execute(
                select(Role).filter(
                    Role._role_id == (
                        role_id))  # type: ignore
            )
            fetched_obj = execute_result.scalars().first()

            assert fetched_obj is None

    @pytest.mark.asyncio
    async def test_delete_bulk_roles_not_found(
        self,
        obj_manager: RoleManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of deleting bulk
        roles when some
        roles are not found.

        Steps:
        1. Create a role using the
            RoleFactory.
        2. Assert that the created role
            is an instance of the
            Role class.
        3. Define a list of role IDs to delete.
        4. Use pytest.raises to assert that an exception is
            raised when deleting the bulk roles.
        5. Rollback the session to undo any changes made during the test.

        This test case ensures that the delete_bulk method of the
        RoleManager raises an exception
        when some roles with the specified IDs are
        not found in the database.
        """
        obj_1 = await RoleFactory.create_async(
            session=session)

        assert isinstance(obj_1,
                          Role)

        # Delete roles
        role_ids = [1, 2]

        with pytest.raises(Exception):
            await obj_manager.delete_bulk(
                role_ids)

        await session.rollback()

    @pytest.mark.asyncio
    async def test_delete_bulk_empty_list(
        self,
        obj_manager: RoleManager
    ):
        """
        Test case to verify the behavior of deleting
        roles with an empty list.

        Args:
            obj_manager (RoleManager): The
                instance of the
                RoleManager class.

        Returns:
            None

        Raises:
            AssertionError: If the result is not True.
        """

        # Delete roles with an empty list
        role_ids = []
        result = await obj_manager.delete_bulk(
            role_ids)

        # Assertions
        assert result is True

    @pytest.mark.asyncio
    async def test_delete_bulk_invalid_type(
        self,
        obj_manager: RoleManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of the delete_bulk
        method when invalid role IDs are provided.

        Args:
            obj_manager (RoleManager): The
                instance of the
                RoleManager class.
            session (AsyncSession): The async session object.

        Raises:
            Exception: If an exception is raised during the
                execution of the delete_bulk method.

        Returns:
            None
        """

        role_ids = ["1", 2]

        with pytest.raises(Exception):
            await obj_manager.delete_bulk(
                role_ids)

        await session.rollback()
