# models/managers/tests/org_customer_test.py
# pylint: disable=protected-access
# pylint: disable=unused-argument
# pylint: disable=unused-import
"""
    This class contains unit tests for the
    `OrgCustomerManager` class.
"""

import logging
import uuid  # noqa: F401

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from helpers.session_context import SessionContext
from managers.org_customer import (
    OrgCustomerManager)
from models import OrgCustomer
from models.factory import (
    OrgCustomerFactory)


class TestOrgCustomerBulkManager:
    """
    This class contains unit tests for the
    `OrgCustomerManager` class.
    """

    @pytest_asyncio.fixture(scope="function")
    async def obj_manager(self, session: AsyncSession):
        """
        Fixture that returns an instance of
        `OrgCustomerManager` for testing.
        """
        session_context = SessionContext(dict(), session)
        session_context.customer_code = uuid.uuid4()
        return OrgCustomerManager(session_context)

    @pytest.mark.asyncio
    async def test_add_bulk(
        self,
        obj_manager: OrgCustomerManager,
        session: AsyncSession
    ):
        """
        Test case for the `add_bulk` method of the
        `OrgCustomerManager` class.

        This test case verifies that the `add_bulk`
        method correctly adds multiple
        org_customers to the database.

        Steps:
        1. Generate a list of org_customer data using the
            `OrgCustomerFactory.build_async` method.
        2. Call the `add_bulk` method of the
            `obj_manager` instance,
            passing in the
            generated org_customer data.
        3. Verify that the number of org_customers
            returned is
            equal to the number of org_customers added.
        4. For each updated org_customer, fetch the corresponding
            org_customer from the database.
        5. Verify that the fetched org_customer
            is an instance of the
            `OrgCustomer` class.
        6. Verify that the insert_user_id and
            last_update_user_id of the fetched
            org_customer match the
            customer code of the session context.
        7. Verify that the org_customer_id of the fetched
            org_customer matches the
            org_customer_id of the updated
            org_customer.

        """
        org_customers_data = [
            await OrgCustomerFactory.build_async(session) for _ in range(5)]

        org_customers = await obj_manager.add_bulk(
            org_customers_data)

        assert len(org_customers) == 5

        for updated_obj in org_customers:
            result = await session.execute(
                select(OrgCustomer).filter(
                    OrgCustomer._org_customer_id == (
                        updated_obj.org_customer_id)  # type: ignore
                )
            )
            fetched_obj = result.scalars().first()

            assert isinstance(
                fetched_obj,
                OrgCustomer)

            assert str(fetched_obj.insert_user_id) == (
                str(obj_manager._session_context.customer_code))
            assert str(fetched_obj.last_update_user_id) == (
                str(obj_manager._session_context.customer_code))

            assert fetched_obj.org_customer_id == \
                updated_obj.org_customer_id

    @pytest.mark.asyncio
    async def test_update_bulk_success(
        self,
        obj_manager: OrgCustomerManager,
        session: AsyncSession
    ):
        """
        Test case for bulk update of org_customers.

        This test case verifies the functionality of the
        `update_bulk` method in the
        `OrgCustomerManager` class.
        It creates two org_customer instances,
        updates their codes
        using the `update_bulk` method, and then verifies
        that the updates were successful by checking the
        updated codes in the database.

        Steps:
        1. Create two org_customer instances using the
            `OrgCustomerFactory.create_async` method.
        2. Generate new codes for the org_customers.
        3. Update the org_customers' codes
            using the `update_bulk` method.
        4. Verify that the update was successful by checking
            the updated codes in the database.

        Args:
            obj_manager (OrgCustomerManager):
                An instance of the
                `OrgCustomerManager` class.
            session (AsyncSession): An instance of the `AsyncSession` class.

        Returns:
            None
        """
        # Mocking org_customer instances
        obj_1 = await OrgCustomerFactory. \
            create_async(
                session=session)
        obj_2 = await OrgCustomerFactory. \
            create_async(
                session=session)
        logging.info(obj_1.__dict__)

        code_updated1 = uuid.uuid4()
        code_updated2 = uuid.uuid4()
        logging.info(code_updated1)
        logging.info(code_updated2)

        # Update org_customers
        updates = [
            {
                "org_customer_id":
                    obj_1.org_customer_id,
                "code": code_updated1
            },
            {
                "org_customer_id":
                    obj_2.org_customer_id,
                "code": code_updated2
            }
        ]
        updated_org_customers = await obj_manager.update_bulk(
            updates)

        logging.info('bulk update results')
        # Assertions
        assert len(updated_org_customers) == 2
        logging.info(updated_org_customers[0]
                     .__dict__)
        logging.info(updated_org_customers[1]
                     .__dict__)

        logging.info('getall')
        org_customers = await obj_manager.get_list()
        logging.info(org_customers[0]
                     .__dict__)
        logging.info(org_customers[1]
                     .__dict__)

        assert updated_org_customers[0].code == \
            code_updated1
        assert updated_org_customers[1].code == \
            code_updated2

        assert str(updated_org_customers[0]
                   .last_update_user_id) == (
            str(obj_manager
                ._session_context.customer_code))

        assert str(updated_org_customers[1]
                   .last_update_user_id) == (
            str(obj_manager
                ._session_context.customer_code))

        result = await session.execute(
            select(OrgCustomer).filter(
                OrgCustomer._org_customer_id == 1)  # type: ignore
        )
        fetched_obj = result.scalars().first()

        assert isinstance(fetched_obj,
                          OrgCustomer)

        assert fetched_obj.code == code_updated1

        result = await session.execute(
            select(OrgCustomer).filter(
                OrgCustomer._org_customer_id == 2)  # type: ignore
        )
        fetched_obj = result.scalars().first()

        assert isinstance(fetched_obj,
                          OrgCustomer)

        assert fetched_obj.code == code_updated2

    @pytest.mark.asyncio
    async def test_update_bulk_missing_org_customer_id(
        self,
        obj_manager: OrgCustomerManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of the `update_bulk`
        method when the org_customer_id is missing.

        This test case ensures that when the org_customer_id is
        missing in the updates list,
        an exception is raised and the session is rolled back.

        Steps:
        1. Prepare the updates list with a missing org_customer_id.
        2. Call the `update_bulk` method with the updates list.
        3. Assert that an exception is raised.
        4. Rollback the session to undo any changes made during the test.

        """
        # No org_customers to update since
        # org_customer_id is missing
        updates = [{"name": "Red Rose"}]

        with pytest.raises(Exception):
            await obj_manager.update_bulk(updates)

        await session.rollback()

    @pytest.mark.asyncio
    async def test_update_bulk_org_customer_not_found(
        self,
        obj_manager: OrgCustomerManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of the update_bulk
        method when a org_customer is not found.

        This test case performs the following steps:
        1. Defines a list of org_customer updates,
            where each update
            contains a org_customer_id and a code.
        2. Calls the update_bulk method of the
            obj_manager with the list of updates.
        3. Expects an exception to be raised, indicating that
            the org_customer was not found.
        4. Rolls back the session to undo any changes made during the test.

        Note: This test assumes that the update_bulk method
        throws an exception when a
        org_customer is not found.

        """

        # Update org_customers
        updates = [{"org_customer_id": 1, "code": uuid.uuid4()}]

        with pytest.raises(Exception):
            await obj_manager.update_bulk(updates)

        await session.rollback()

    @pytest.mark.asyncio
    async def test_update_bulk_invalid_type(
        self,
        obj_manager: OrgCustomerManager,
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
            OrgCustomerManager class.
        :param session: An instance of the AsyncSession class.
        """

        updates = [{"org_customer_id": "2", "code": uuid.uuid4()}]

        with pytest.raises(Exception):
            await obj_manager.update_bulk(updates)

        await session.rollback()

    @pytest.mark.asyncio
    async def test_delete_bulk_success(
        self,
        obj_manager: OrgCustomerManager,
        session: AsyncSession
    ):
        """
        Test case for the delete_bulk method of the
        OrgCustomerManager class.

        This test verifies that the delete_bulk method
        successfully deletes multiple org_customers
        from the database.

        Steps:
        1. Create two org_customer objects
            using the OrgCustomerFactory.
        2. Delete the org_customers using the
            delete_bulk method
            of the obj_manager.
        3. Verify that the delete operation was successful by
            checking if the org_customers
            no longer exist in the database.

        Expected Result:
        - The delete_bulk method should return True, indicating
            that the delete operation was successful.
        - The org_customers should
            no longer exist in the database.

        """

        obj_1 = await OrgCustomerFactory.create_async(
            session=session)

        obj_2 = await OrgCustomerFactory.create_async(
            session=session)

        # Delete org_customers
        org_customer_ids = [
            obj_1.org_customer_id,
            obj_2.org_customer_id
        ]
        result = await obj_manager.delete_bulk(
            org_customer_ids)

        assert result is True

        for org_customer_id in org_customer_ids:
            execute_result = await session.execute(
                select(OrgCustomer).filter(
                    OrgCustomer._org_customer_id == (
                        org_customer_id))  # type: ignore
            )
            fetched_obj = execute_result.scalars().first()

            assert fetched_obj is None

    @pytest.mark.asyncio
    async def test_delete_bulk_org_customers_not_found(
        self,
        obj_manager: OrgCustomerManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of deleting bulk
        org_customers when some
        org_customers are not found.

        Steps:
        1. Create a org_customer using the
            OrgCustomerFactory.
        2. Assert that the created org_customer
            is an instance of the
            OrgCustomer class.
        3. Define a list of org_customer IDs to delete.
        4. Use pytest.raises to assert that an exception is
            raised when deleting the bulk org_customers.
        5. Rollback the session to undo any changes made during the test.

        This test case ensures that the delete_bulk method of the
        OrgCustomerManager raises an exception
        when some org_customers with the specified IDs are
        not found in the database.
        """
        obj_1 = await OrgCustomerFactory.create_async(
            session=session)

        assert isinstance(obj_1,
                          OrgCustomer)

        # Delete org_customers
        org_customer_ids = [1, 2]

        with pytest.raises(Exception):
            await obj_manager.delete_bulk(
                org_customer_ids)

        await session.rollback()

    @pytest.mark.asyncio
    async def test_delete_bulk_empty_list(
        self,
        obj_manager: OrgCustomerManager
    ):
        """
        Test case to verify the behavior of deleting
        org_customers with an empty list.

        Args:
            obj_manager (OrgCustomerManager): The
                instance of the
                OrgCustomerManager class.

        Returns:
            None

        Raises:
            AssertionError: If the result is not True.
        """

        # Delete org_customers with an empty list
        org_customer_ids = []
        result = await obj_manager.delete_bulk(
            org_customer_ids)

        # Assertions
        assert result is True

    @pytest.mark.asyncio
    async def test_delete_bulk_invalid_type(
        self,
        obj_manager: OrgCustomerManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of the delete_bulk
        method when invalid org_customer IDs are provided.

        Args:
            obj_manager (OrgCustomerManager): The
                instance of the
                OrgCustomerManager class.
            session (AsyncSession): The async session object.

        Raises:
            Exception: If an exception is raised during the
                execution of the delete_bulk method.

        Returns:
            None
        """

        org_customer_ids = ["1", 2]

        with pytest.raises(Exception):
            await obj_manager.delete_bulk(
                org_customer_ids)

        await session.rollback()
