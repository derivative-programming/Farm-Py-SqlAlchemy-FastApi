# models/managers/tests/customer_test.py
# pylint: disable=protected-access
# pylint: disable=unused-argument
# pylint: disable=unused-import
"""
    This class contains unit tests for the
    `CustomerManager` class.
"""

import logging
import uuid  # noqa: F401

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from helpers.session_context import SessionContext
from managers.customer import CustomerManager
from models import Customer
from models.factory import CustomerFactory


class TestCustomerBulkManager:
    """
    This class contains unit tests for the
    `CustomerManager` class.
    """

    @pytest_asyncio.fixture(scope="function")
    async def customer_manager(self, session: AsyncSession):
        """
        Fixture that returns an instance of
        `CustomerManager` for testing.
        """
        session_context = SessionContext(dict(), session)
        session_context.customer_code = uuid.uuid4()
        return CustomerManager(session_context)

    @pytest.mark.asyncio
    async def test_add_bulk(
        self,
        customer_manager: CustomerManager,
        session: AsyncSession
    ):
        """
        Test case for the `add_bulk` method of the
        `CustomerManager` class.

        This test case verifies that the `add_bulk`
        method correctly adds multiple
        customers to the database.

        Steps:
        1. Generate a list of customer data using the
            `CustomerFactory.build_async` method.
        2. Call the `add_bulk` method of the
            `customer_manager` instance,
            passing in the
            generated customer data.
        3. Verify that the number of customers
            returned is
            equal to the number of customers added.
        4. For each updated customer, fetch the corresponding
            customer from the database.
        5. Verify that the fetched customer
            is an instance of the
            `Customer` class.
        6. Verify that the insert_user_id and
            last_update_user_id of the fetched
            customer match the
            customer code of the session context.
        7. Verify that the customer_id of the fetched
            customer matches the
            customer_id of the updated
            customer.

        """
        customers_data = [
            await CustomerFactory.build_async(session) for _ in range(5)]

        customers = await customer_manager.add_bulk(
            customers_data)

        assert len(customers) == 5

        for updated_customer in customers:
            result = await session.execute(
                select(Customer).filter(
                    Customer._customer_id == updated_customer.customer_id  # type: ignore
                )
            )
            fetched_customer = result.scalars().first()

            assert isinstance(
                fetched_customer,
                Customer)

            assert str(fetched_customer.insert_user_id) == (
                str(customer_manager._session_context.customer_code))
            assert str(fetched_customer.last_update_user_id) == (
                str(customer_manager._session_context.customer_code))

            assert fetched_customer.customer_id == \
                updated_customer.customer_id

    @pytest.mark.asyncio
    async def test_update_bulk_success(
        self,
        customer_manager: CustomerManager,
        session: AsyncSession
    ):
        """
        Test case for bulk update of customers.

        This test case verifies the functionality of the
        `update_bulk` method in the
        `CustomerManager` class.
        It creates two customer instances,
        updates their codes
        using the `update_bulk` method, and then verifies
        that the updates were successful by checking the
        updated codes in the database.

        Steps:
        1. Create two customer instances using the
            `CustomerFactory.create_async` method.
        2. Generate new codes for the customers.
        3. Update the customers' codes
            using the `update_bulk` method.
        4. Verify that the update was successful by checking
            the updated codes in the database.

        Args:
            customer_manager (CustomerManager):
                An instance of the
                `CustomerManager` class.
            session (AsyncSession): An instance of the `AsyncSession` class.

        Returns:
            None
        """
        # Mocking customer instances
        customer1 = await CustomerFactory. \
            create_async(
                session=session)
        customer2 = await CustomerFactory. \
            create_async(
                session=session)
        logging.info(customer1.__dict__)

        code_updated1 = uuid.uuid4()
        code_updated2 = uuid.uuid4()
        logging.info(code_updated1)
        logging.info(code_updated2)

        # Update customers
        updates = [
            {
                "customer_id":
                    customer1.customer_id,
                "code": code_updated1
            },
            {
                "customer_id":
                    customer2.customer_id,
                "code": code_updated2
            }
        ]
        updated_customers = await customer_manager.update_bulk(
            updates)

        logging.info('bulk update results')
        # Assertions
        assert len(updated_customers) == 2
        logging.info(updated_customers[0]
                     .__dict__)
        logging.info(updated_customers[1]
                     .__dict__)

        logging.info('getall')
        customers = await customer_manager.get_list()
        logging.info(customers[0]
                     .__dict__)
        logging.info(customers[1]
                     .__dict__)

        assert updated_customers[0].code == \
            code_updated1
        assert updated_customers[1].code == \
            code_updated2

        assert str(updated_customers[0]
                   .last_update_user_id) == (
            str(customer_manager
                ._session_context.customer_code))

        assert str(updated_customers[1]
                   .last_update_user_id) == (
            str(customer_manager
                ._session_context.customer_code))

        result = await session.execute(
            select(Customer).filter(
                Customer._customer_id == 1)  # type: ignore
        )
        fetched_customer = result.scalars().first()

        assert isinstance(fetched_customer,
                          Customer)

        assert fetched_customer.code == code_updated1

        result = await session.execute(
            select(Customer).filter(
                Customer._customer_id == 2)  # type: ignore
        )
        fetched_customer = result.scalars().first()

        assert isinstance(fetched_customer,
                          Customer)

        assert fetched_customer.code == code_updated2

    @pytest.mark.asyncio
    async def test_update_bulk_missing_customer_id(
        self,
        customer_manager: CustomerManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of the `update_bulk`
        method when the customer_id is missing.

        This test case ensures that when the customer_id is
        missing in the updates list,
        an exception is raised and the session is rolled back.

        Steps:
        1. Prepare the updates list with a missing customer_id.
        2. Call the `update_bulk` method with the updates list.
        3. Assert that an exception is raised.
        4. Rollback the session to undo any changes made during the test.

        """
        # No customers to update since customer_id is missing
        updates = [{"name": "Red Rose"}]

        with pytest.raises(Exception):
            await customer_manager.update_bulk(updates)

        await session.rollback()

    @pytest.mark.asyncio
    async def test_update_bulk_customer_not_found(
        self,
        customer_manager: CustomerManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of the update_bulk
        method when a customer is not found.

        This test case performs the following steps:
        1. Defines a list of customer updates,
            where each update
            contains a customer_id and a code.
        2. Calls the update_bulk method of the
            customer_manager with the list of updates.
        3. Expects an exception to be raised, indicating that
            the customer was not found.
        4. Rolls back the session to undo any changes made during the test.

        Note: This test assumes that the update_bulk method
        throws an exception when a
        customer is not found.

        """

        # Update customers
        updates = [{"customer_id": 1, "code": uuid.uuid4()}]

        with pytest.raises(Exception):
            await customer_manager.update_bulk(updates)

        await session.rollback()

    @pytest.mark.asyncio
    async def test_update_bulk_invalid_type(
        self,
        customer_manager: CustomerManager,
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

        :param customer_manager: An instance of the
            CustomerManager class.
        :param session: An instance of the AsyncSession class.
        """

        updates = [{"customer_id": "2", "code": uuid.uuid4()}]

        with pytest.raises(Exception):
            await customer_manager.update_bulk(updates)

        await session.rollback()

    @pytest.mark.asyncio
    async def test_delete_bulk_success(
        self,
        customer_manager: CustomerManager,
        session: AsyncSession
    ):
        """
        Test case for the delete_bulk method of the
        CustomerManager class.

        This test verifies that the delete_bulk method
        successfully deletes multiple customers
        from the database.

        Steps:
        1. Create two customer objects
            using the CustomerFactory.
        2. Delete the customers using the
            delete_bulk method
            of the customer_manager.
        3. Verify that the delete operation was successful by
            checking if the customers no longer exist in the database.

        Expected Result:
        - The delete_bulk method should return True, indicating
            that the delete operation was successful.
        - The customers should no longer exist in the database.

        """

        customer1 = await CustomerFactory.create_async(
            session=session)

        customer2 = await CustomerFactory.create_async(
            session=session)

        # Delete customers
        customer_ids = [customer1.customer_id,
                     customer2.customer_id]
        result = await customer_manager.delete_bulk(
            customer_ids)

        assert result is True

        for customer_id in customer_ids:
            execute_result = await session.execute(
                select(Customer).filter(
                    Customer._customer_id == customer_id)  # type: ignore
            )
            fetched_customer = execute_result.scalars().first()

            assert fetched_customer is None

    @pytest.mark.asyncio
    async def test_delete_bulk_customers_not_found(
        self,
        customer_manager: CustomerManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of deleting bulk
        customers when some customers are not found.

        Steps:
        1. Create a customer using the
            CustomerFactory.
        2. Assert that the created customer
            is an instance of the
            Customer class.
        3. Define a list of customer IDs to delete.
        4. Use pytest.raises to assert that an exception is
            raised when deleting the bulk customers.
        5. Rollback the session to undo any changes made during the test.

        This test case ensures that the delete_bulk method of the
        CustomerManager raises an exception
        when some customers with the specified IDs are
        not found in the database.
        """
        customer1 = await CustomerFactory.create_async(
            session=session)

        assert isinstance(customer1,
                          Customer)

        # Delete customers
        customer_ids = [1, 2]

        with pytest.raises(Exception):
            await customer_manager.delete_bulk(
                customer_ids)

        await session.rollback()

    @pytest.mark.asyncio
    async def test_delete_bulk_empty_list(
        self,
        customer_manager: CustomerManager
    ):
        """
        Test case to verify the behavior of deleting
        customers with an empty list.

        Args:
            customer_manager (CustomerManager): The
                instance of the
                CustomerManager class.

        Returns:
            None

        Raises:
            AssertionError: If the result is not True.
        """

        # Delete customers with an empty list
        customer_ids = []
        result = await customer_manager.delete_bulk(
            customer_ids)

        # Assertions
        assert result is True

    @pytest.mark.asyncio
    async def test_delete_bulk_invalid_type(
        self,
        customer_manager: CustomerManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of the delete_bulk
        method when invalid customer IDs are provided.

        Args:
            customer_manager (CustomerManager): The
                instance of the
                CustomerManager class.
            session (AsyncSession): The async session object.

        Raises:
            Exception: If an exception is raised during the
                execution of the delete_bulk method.

        Returns:
            None
        """

        customer_ids = ["1", 2]

        with pytest.raises(Exception):
            await customer_manager.delete_bulk(
                customer_ids)

        await session.rollback()

