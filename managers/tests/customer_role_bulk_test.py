# models/managers/tests/customer_role_test.py
# pylint: disable=protected-access
# pylint: disable=unused-argument
"""
    This class contains unit tests for the
    `CustomerRoleManager` class.
"""

import logging
import uuid

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from helpers.session_context import SessionContext
from managers.customer_role import CustomerRoleManager
from models import CustomerRole
from models.factory import CustomerRoleFactory

class TestCustomerRoleBulkManager:
    """
    This class contains unit tests for the
    `CustomerRoleManager` class.
    """

    @pytest_asyncio.fixture(scope="function")
    async def customer_role_manager(self, session: AsyncSession):
        """
        Fixture that returns an instance of
        `CustomerRoleManager` for testing.
        """
        session_context = SessionContext(dict(), session)
        session_context.customer_code = uuid.uuid4()
        return CustomerRoleManager(session_context)

    @pytest.mark.asyncio
    async def test_add_bulk(
        self,
        customer_role_manager: CustomerRoleManager,
        session: AsyncSession
    ):
        """
        Test case for the `add_bulk` method of the
        `CustomerRoleManager` class.

        This test case verifies that the `add_bulk`
        method correctly adds multiple customer_roles to the database.

        Steps:
        1. Generate a list of customer_role data using the
            `CustomerRoleFactory.build_async` method.
        2. Call the `add_bulk` method of the
            `customer_role_manager` instance,
            passing in the
            generated customer_role data.
        3. Verify that the number of customer_roles
            returned is
            equal to the number of customer_roles added.
        4. For each updated customer_role, fetch the corresponding
            customer_role from the database.
        5. Verify that the fetched customer_role
            is an instance of the
            `CustomerRole` class.
        6. Verify that the insert_user_id and
            last_update_user_id of the fetched
            customer_role match the
            customer code of the session context.
        7. Verify that the customer_role_id of the fetched
            customer_role matches the
            customer_role_id of the updated
            customer_role.

        """
        customer_roles_data = [
            await CustomerRoleFactory.build_async(session) for _ in range(5)]

        customer_roles = await customer_role_manager.add_bulk(
            customer_roles_data)

        assert len(customer_roles) == 5

        for updated_customer_role in customer_roles:
            result = await session.execute(
                select(CustomerRole).filter(
                    CustomerRole._customer_role_id == updated_customer_role.customer_role_id  # type: ignore
                )
            )
            fetched_customer_role = result.scalars().first()

            assert isinstance(fetched_customer_role, CustomerRole)

            assert str(fetched_customer_role.insert_user_id) == (
                str(customer_role_manager._session_context.customer_code))
            assert str(fetched_customer_role.last_update_user_id) == (
                str(customer_role_manager._session_context.customer_code))

            assert fetched_customer_role.customer_role_id == \
                updated_customer_role.customer_role_id

    @pytest.mark.asyncio
    async def test_update_bulk_success(
        self,
        customer_role_manager: CustomerRoleManager,
        session: AsyncSession
    ):
        """
        Test case for bulk update of customer_roles.

        This test case verifies the functionality of the
        `update_bulk` method in the `CustomerRoleManager` class.
        It creates two customer_role instances,
        updates their codes
        using the `update_bulk` method, and then verifies
        that the updates were successful by checking the
        updated codes in the database.

        Steps:
        1. Create two customer_role instances using the
            `CustomerRoleFactory.create_async` method.
        2. Generate new codes for the customer_roles.
        3. Update the customer_roles' codes using the `update_bulk` method.
        4. Verify that the update was successful by checking
            the updated codes in the database.

        Args:
            customer_role_manager (CustomerRoleManager): An instance of the
                `CustomerRoleManager` class.
            session (AsyncSession): An instance of the `AsyncSession` class.

        Returns:
            None
        """
        # Mocking customer_role instances
        customer_role1 = await CustomerRoleFactory.create_async(
            session=session)
        customer_role2 = await CustomerRoleFactory.create_async(
            session=session)
        logging.info(customer_role1.__dict__)

        code_updated1 = uuid.uuid4()
        code_updated2 = uuid.uuid4()
        logging.info(code_updated1)
        logging.info(code_updated2)

        # Update customer_roles
        updates = [
            {
                "customer_role_id": customer_role1.customer_role_id,
                "code": code_updated1
            },
            {
                "customer_role_id": customer_role2.customer_role_id,
                "code": code_updated2
            }
        ]
        updated_customer_roles = await customer_role_manager.update_bulk(
            updates)

        logging.info('bulk update results')
        # Assertions
        assert len(updated_customer_roles) == 2
        logging.info(updated_customer_roles[0].__dict__)
        logging.info(updated_customer_roles[1].__dict__)

        logging.info('getall')
        customer_roles = await customer_role_manager.get_list()
        logging.info(customer_roles[0].__dict__)
        logging.info(customer_roles[1].__dict__)

        assert updated_customer_roles[0].code == code_updated1
        assert updated_customer_roles[1].code == code_updated2

        assert str(updated_customer_roles[0].last_update_user_id) == (
            str(customer_role_manager._session_context.customer_code))

        assert str(updated_customer_roles[1].last_update_user_id) == (
            str(customer_role_manager._session_context.customer_code))

        result = await session.execute(
            select(CustomerRole).filter(
                CustomerRole._customer_role_id == 1)  # type: ignore
        )
        fetched_customer_role = result.scalars().first()

        assert isinstance(fetched_customer_role, CustomerRole)

        assert fetched_customer_role.code == code_updated1

        result = await session.execute(
            select(CustomerRole).filter(
                CustomerRole._customer_role_id == 2)  # type: ignore
        )
        fetched_customer_role = result.scalars().first()

        assert isinstance(fetched_customer_role, CustomerRole)

        assert fetched_customer_role.code == code_updated2

    @pytest.mark.asyncio
    async def test_update_bulk_missing_customer_role_id(
        self,
        customer_role_manager: CustomerRoleManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of the `update_bulk`
        method when the customer_role_id is missing.

        This test case ensures that when the customer_role_id is
        missing in the updates list,
        an exception is raised and the session is rolled back.

        Steps:
        1. Prepare the updates list with a missing customer_role_id.
        2. Call the `update_bulk` method with the updates list.
        3. Assert that an exception is raised.
        4. Rollback the session to undo any changes made during the test.

        """
        # No customer_roles to update since customer_role_id is missing
        updates = [{"name": "Red Rose"}]

        with pytest.raises(Exception):
            await customer_role_manager.update_bulk(updates)

        await session.rollback()

    @pytest.mark.asyncio
    async def test_update_bulk_customer_role_not_found(
        self,
        customer_role_manager: CustomerRoleManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of the update_bulk
        method when a customer_role is not found.

        This test case performs the following steps:
        1. Defines a list of customer_role updates,
            where each update
            contains a customer_role_id and a code.
        2. Calls the update_bulk method of the
            customer_role_manager with the list of updates.
        3. Expects an exception to be raised, indicating that
            the customer_role was not found.
        4. Rolls back the session to undo any changes made during the test.

        Note: This test assumes that the update_bulk method
        throws an exception when a
        customer_role is not found.

        """

        # Update customer_roles
        updates = [{"customer_role_id": 1, "code": uuid.uuid4()}]

        with pytest.raises(Exception):
            await customer_role_manager.update_bulk(updates)

        await session.rollback()

    @pytest.mark.asyncio
    async def test_update_bulk_invalid_type(
        self,
        customer_role_manager: CustomerRoleManager,
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

        :param customer_role_manager: An instance of the CustomerRoleManager class.
        :param session: An instance of the AsyncSession class.
        """

        updates = [{"customer_role_id": "2", "code": uuid.uuid4()}]

        with pytest.raises(Exception):
            await customer_role_manager.update_bulk(updates)

        await session.rollback()

    @pytest.mark.asyncio
    async def test_delete_bulk_success(
        self,
        customer_role_manager: CustomerRoleManager,
        session: AsyncSession
    ):
        """
        Test case for the delete_bulk method of the
        CustomerRoleManager class.

        This test verifies that the delete_bulk method
        successfully deletes multiple customer_roles
        from the database.

        Steps:
        1. Create two customer_role objects
            using the CustomerRoleFactory.
        2. Delete the customer_roles using the
            delete_bulk method
            of the customer_role_manager.
        3. Verify that the delete operation was successful by
            checking if the customer_roles no longer exist in the database.

        Expected Result:
        - The delete_bulk method should return True, indicating
            that the delete operation was successful.
        - The customer_roles should no longer exist in the database.

        """

        customer_role1 = await CustomerRoleFactory.create_async(
            session=session)

        customer_role2 = await CustomerRoleFactory.create_async(
            session=session)

        # Delete customer_roles
        customer_role_ids = [customer_role1.customer_role_id, customer_role2.customer_role_id]
        result = await customer_role_manager.delete_bulk(
            customer_role_ids)

        assert result is True

        for customer_role_id in customer_role_ids:
            execute_result = await session.execute(
                select(CustomerRole).filter(
                    CustomerRole._customer_role_id == customer_role_id)  # type: ignore
            )
            fetched_customer_role = execute_result.scalars().first()

            assert fetched_customer_role is None

    @pytest.mark.asyncio
    async def test_delete_bulk_customer_roles_not_found(
        self,
        customer_role_manager: CustomerRoleManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of deleting bulk
        customer_roles when some customer_roles are not found.

        Steps:
        1. Create a customer_role using the
            CustomerRoleFactory.
        2. Assert that the created customer_role
            is an instance of the
            CustomerRole class.
        3. Define a list of customer_role IDs to delete.
        4. Use pytest.raises to assert that an exception is
            raised when deleting the bulk customer_roles.
        5. Rollback the session to undo any changes made during the test.

        This test case ensures that the delete_bulk method of the
        CustomerRoleManager raises an exception
        when some customer_roles with the specified IDs are
        not found in the database.
        """
        customer_role1 = await CustomerRoleFactory.create_async(
            session=session)

        assert isinstance(customer_role1, CustomerRole)

        # Delete customer_roles
        customer_role_ids = [1, 2]

        with pytest.raises(Exception):
            await customer_role_manager.delete_bulk(
                customer_role_ids)

        await session.rollback()

    @pytest.mark.asyncio
    async def test_delete_bulk_empty_list(
        self,
        customer_role_manager: CustomerRoleManager
    ):
        """
        Test case to verify the behavior of deleting
        customer_roles with an empty list.

        Args:
            customer_role_manager (CustomerRoleManager): The
                instance of the
                CustomerRoleManager class.

        Returns:
            None

        Raises:
            AssertionError: If the result is not True.
        """

        # Delete customer_roles with an empty list
        customer_role_ids = []
        result = await customer_role_manager.delete_bulk(
            customer_role_ids)

        # Assertions
        assert result is True

    @pytest.mark.asyncio
    async def test_delete_bulk_invalid_type(
        self,
        customer_role_manager: CustomerRoleManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of the delete_bulk
        method when invalid customer_role IDs are provided.

        Args:
            customer_role_manager (CustomerRoleManager): The
                instance of the
                CustomerRoleManager class.
            session (AsyncSession): The async session object.

        Raises:
            Exception: If an exception is raised during the
                execution of the delete_bulk method.

        Returns:
            None
        """

        customer_role_ids = ["1", 2]

        with pytest.raises(Exception):
            await customer_role_manager.delete_bulk(
                customer_role_ids)

        await session.rollback()
