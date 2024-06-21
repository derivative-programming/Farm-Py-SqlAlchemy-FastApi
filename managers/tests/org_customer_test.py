# models/managers/tests/org_customer_test.py
# pylint: disable=protected-access
# pylint: disable=unused-argument
"""
    This class contains unit tests for the
    `OrgCustomerManager` class.
"""
# TODO file too big. split into separate test files
import logging
from typing import List
import uuid
import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
import models
from helpers.session_context import SessionContext
from managers.org_customer import OrgCustomerManager
from models import OrgCustomer
from models.factory import OrgCustomerFactory
from models.serialization_schema.org_customer import OrgCustomerSchema
class TestOrgCustomerManager:
    """
    This class contains unit tests for the
    `OrgCustomerManager` class.
    """
    @pytest_asyncio.fixture(scope="function")
    async def org_customer_manager(self, session: AsyncSession):
        """
        Fixture that returns an instance of
        `OrgCustomerManager` for testing.
        """
        session_context = SessionContext(dict(), session)
        session_context.customer_code = uuid.uuid4()
        return OrgCustomerManager(session_context)
    @pytest.mark.asyncio
    async def test_build(
        self,
        org_customer_manager: OrgCustomerManager
    ):
        """
        Test case for the `build` method of
        `OrgCustomerManager`.
        """
        # Define mock data for our org_customer
        mock_data = {
            "code": uuid.uuid4()
        }
        # Call the build function of the manager
        org_customer = await org_customer_manager.build(
            **mock_data)
        # Assert that the returned object is an instance of OrgCustomer
        assert isinstance(
            org_customer, OrgCustomer)
        # Assert that the attributes of the
        # org_customer match our mock data
        assert org_customer.code == mock_data["code"]
    @pytest.mark.asyncio
    async def test_build_with_missing_data(
        self,
        org_customer_manager: OrgCustomerManager,
        session: AsyncSession
    ):
        """
        Test case for the `build` method of
        `OrgCustomerManager` with missing data.
        """
        # Define mock data with a missing key
        mock_data = {
            "non_existant_property": "Rose"
        }
        # If the build method is expected to raise an exception for
        # missing data, test for that
        with pytest.raises(Exception):
            await org_customer_manager.build(**mock_data)
        await session.rollback()
    @pytest.mark.asyncio
    async def test_add_correctly_adds_org_customer_to_database(
        self,
        org_customer_manager: OrgCustomerManager,
        session: AsyncSession
    ):
        """
        Test case for the `add` method of
        `OrgCustomerManager` that checks if a
        org_customer is correctly added to the database.
        """
        test_org_customer = await OrgCustomerFactory.build_async(
            session)
        assert test_org_customer.org_customer_id == 0
        # Add the org_customer using the
        # manager's add method
        added_org_customer = await org_customer_manager.add(
            org_customer=test_org_customer)
        assert isinstance(added_org_customer, OrgCustomer)
        assert str(added_org_customer.insert_user_id) == (
            str(org_customer_manager._session_context.customer_code))
        assert str(added_org_customer.last_update_user_id) == (
            str(org_customer_manager._session_context.customer_code))
        assert added_org_customer.org_customer_id > 0
        # Fetch the org_customer from
        # the database directly
        result = await session.execute(
            select(OrgCustomer).filter(
                OrgCustomer._org_customer_id == added_org_customer.org_customer_id  # type: ignore
            )
        )
        fetched_org_customer = result.scalars().first()
        # Assert that the fetched org_customer
        # is not None and matches the
        # added org_customer
        assert fetched_org_customer is not None
        assert isinstance(fetched_org_customer, OrgCustomer)
        assert fetched_org_customer.org_customer_id == added_org_customer.org_customer_id
    @pytest.mark.asyncio
    async def test_add_returns_correct_org_customer_object(
        self,
        org_customer_manager: OrgCustomerManager,
        session: AsyncSession
    ):
        """
        Test case for the `add` method of
        `OrgCustomerManager` that checks if the
        correct org_customer object is returned.
        """
        # Create a test org_customer
        # using the OrgCustomerFactory
        # without persisting it to the database
        test_org_customer = await OrgCustomerFactory.build_async(
            session)
        assert test_org_customer.org_customer_id == 0
        test_org_customer.code = uuid.uuid4()
        # Add the org_customer using
        # the manager's add method
        added_org_customer = await org_customer_manager.add(
            org_customer=test_org_customer)
        assert isinstance(added_org_customer, OrgCustomer)
        assert str(added_org_customer.insert_user_id) == (
            str(org_customer_manager._session_context.customer_code))
        assert str(added_org_customer.last_update_user_id) == (
            str(org_customer_manager._session_context.customer_code))
        assert added_org_customer.org_customer_id > 0
        # Assert that the returned
        # org_customer matches the
        # test org_customer
        assert added_org_customer.org_customer_id == \
            test_org_customer.org_customer_id
        assert added_org_customer.code == \
            test_org_customer.code
    @pytest.mark.asyncio
    async def test_get_by_id(
        self,
        org_customer_manager: OrgCustomerManager,
        session: AsyncSession
    ):
        """
        Test case for the `get_by_id` method of
        `OrgCustomerManager`.
        """
        test_org_customer = await OrgCustomerFactory.create_async(
            session)
        org_customer = await org_customer_manager.get_by_id(
            test_org_customer.org_customer_id)
        assert isinstance(
            org_customer, OrgCustomer)
        assert test_org_customer.org_customer_id == \
            org_customer.org_customer_id
        assert test_org_customer.code == \
            org_customer.code
    @pytest.mark.asyncio
    async def test_get_by_id_not_found(
        self,
        org_customer_manager: OrgCustomerManager
    ):
        """
        Test case for the `get_by_id` method of
        `OrgCustomerManager` when the
        org_customer is not found.
        """
        non_existent_id = 9999  # An ID that's not in the database
        retrieved_org_customer = await org_customer_manager.get_by_id(
            non_existent_id)
        assert retrieved_org_customer is None
    @pytest.mark.asyncio
    async def test_get_by_code_returns_org_customer(
        self,
        org_customer_manager: OrgCustomerManager,
        session: AsyncSession
    ):
        """
        Test case for the `get_by_code` method of
        `OrgCustomerManager` that checks if
        a org_customer is
        returned by its code.
        """
        test_org_customer = await OrgCustomerFactory.create_async(
            session)
        org_customer = await org_customer_manager.get_by_code(
            test_org_customer.code)
        assert isinstance(
            org_customer, OrgCustomer)
        assert test_org_customer.org_customer_id == \
            org_customer.org_customer_id
        assert test_org_customer.code == \
            org_customer.code
    @pytest.mark.asyncio
    async def test_get_by_code_returns_none_for_nonexistent_code(
        self,
        org_customer_manager: OrgCustomerManager
    ):
        """
        Test case for the `get_by_code` method of
        `OrgCustomerManager` when the code does not exist.
        """
        # Generate a random UUID that doesn't correspond to
        # any OrgCustomer in the database
        random_code = uuid.uuid4()
        org_customer = await org_customer_manager.get_by_code(
            random_code)
        assert org_customer is None
    @pytest.mark.asyncio
    async def test_update(
        self,
        org_customer_manager: OrgCustomerManager,
        session: AsyncSession
    ):
        """
        Test case for the `update` method
        of `OrgCustomerManager`
        that checks if a org_customer
        is correctly updated.
        """
        test_org_customer = await OrgCustomerFactory.create_async(
            session)
        test_org_customer.code = uuid.uuid4()
        updated_org_customer = await org_customer_manager.update(
            org_customer=test_org_customer)
        assert isinstance(updated_org_customer, OrgCustomer)
        assert str(updated_org_customer.last_update_user_id) == str(
            org_customer_manager._session_context.customer_code)
        assert updated_org_customer.org_customer_id == \
            test_org_customer.org_customer_id
        assert updated_org_customer.code == \
            test_org_customer.code
        result = await session.execute(
            select(OrgCustomer).filter(
                OrgCustomer._org_customer_id == test_org_customer.org_customer_id)  # type: ignore
        )
        fetched_org_customer = result.scalars().first()
        assert updated_org_customer.org_customer_id == \
            fetched_org_customer.org_customer_id
        assert updated_org_customer.code == \
            fetched_org_customer.code
        assert test_org_customer.org_customer_id == \
            fetched_org_customer.org_customer_id
        assert test_org_customer.code == \
            fetched_org_customer.code
    @pytest.mark.asyncio
    async def test_update_via_dict(
        self,
        org_customer_manager: OrgCustomerManager,
        session: AsyncSession
    ):
        """
        Test case for the `update` method
        of `OrgCustomerManager`
        that checks if a org_customer is
        correctly updated using a dictionary.
        """
        test_org_customer = await OrgCustomerFactory.create_async(
            session)
        new_code = uuid.uuid4()
        updated_org_customer = await org_customer_manager.update(
            org_customer=test_org_customer,
            code=new_code
        )
        assert isinstance(updated_org_customer, OrgCustomer)
        assert str(updated_org_customer.last_update_user_id) == str(
            org_customer_manager._session_context.customer_code
        )
        assert updated_org_customer.org_customer_id == \
            test_org_customer.org_customer_id
        assert updated_org_customer.code == new_code
        result = await session.execute(
            select(OrgCustomer).filter(
                OrgCustomer._org_customer_id == test_org_customer.org_customer_id)  # type: ignore
        )
        fetched_org_customer = result.scalars().first()
        assert updated_org_customer.org_customer_id == \
            fetched_org_customer.org_customer_id
        assert updated_org_customer.code == \
            fetched_org_customer.code
        assert test_org_customer.org_customer_id == \
            fetched_org_customer.org_customer_id
        assert new_code == \
            fetched_org_customer.code
    @pytest.mark.asyncio
    async def test_update_invalid_org_customer(
        self,
        org_customer_manager: OrgCustomerManager
    ):
        """
        Test case for the `update` method of `OrgCustomerManager`
        with an invalid org_customer.
        """
        # None org_customer
        org_customer = None
        new_code = uuid.uuid4()
        updated_org_customer = await (
            org_customer_manager.update(
                org_customer, code=new_code))  # type: ignore
        # Assertions
        assert updated_org_customer is None
    @pytest.mark.asyncio
    async def test_update_with_nonexistent_attribute(
        self,
        org_customer_manager: OrgCustomerManager,
        session: AsyncSession
    ):
        """
        Test case for the `update` method of `OrgCustomerManager`
        with a nonexistent attribute.
        """
        test_org_customer = await OrgCustomerFactory.create_async(
            session)
        new_code = uuid.uuid4()
        with pytest.raises(ValueError):
            await org_customer_manager.update(
                org_customer=test_org_customer,
                xxx=new_code
            )
        await session.rollback()
    @pytest.mark.asyncio
    async def test_delete(
        self,
        org_customer_manager: OrgCustomerManager,
        session: AsyncSession
    ):
        """
        Test case for the `delete` method of `OrgCustomerManager`.
        """
        org_customer_data = await OrgCustomerFactory.create_async(
            session)
        result = await session.execute(
            select(OrgCustomer).filter(
                OrgCustomer._org_customer_id == org_customer_data.org_customer_id)  # type: ignore
        )
        fetched_org_customer = result.scalars().first()
        assert isinstance(fetched_org_customer, OrgCustomer)
        assert fetched_org_customer.org_customer_id == \
            org_customer_data.org_customer_id
        await org_customer_manager.delete(
            org_customer_id=org_customer_data.org_customer_id)
        result = await session.execute(
            select(OrgCustomer).filter(
                OrgCustomer._org_customer_id == org_customer_data.org_customer_id)  # type: ignore
        )
        fetched_org_customer = result.scalars().first()
        assert fetched_org_customer is None
    @pytest.mark.asyncio
    async def test_delete_nonexistent(
        self,
        org_customer_manager: OrgCustomerManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of deleting a nonexistent org_customer.
        This test case ensures that when the delete method
        is called with the ID of a nonexistent org_customer,
        an exception is raised. The test also verifies that
        the session is rolled back after the delete operation.
        :param org_customer_manager: The instance of the OrgCustomerManager class.
        :param session: The instance of the AsyncSession class.
        """
        with pytest.raises(Exception):
            await org_customer_manager.delete(999)
        await session.rollback()
    @pytest.mark.asyncio
    async def test_delete_invalid_type(
        self,
        org_customer_manager: OrgCustomerManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of deleting a org_customer
        with an invalid type.
        This test case ensures that when the `delete` method
        of the `org_customer_manager` is called with an invalid type,
        an exception is raised. The test case expects the
        `delete` method to raise an exception, and if it doesn't,
        the test case will fail.
        Args:
            org_customer_manager (OrgCustomerManager): An
                instance of the
                `OrgCustomerManager` class.
            session (AsyncSession): An instance of the `AsyncSession` class.
        Returns:
            None
        Raises:
            Exception: If the `delete` method does not raise an exception.
        """
        with pytest.raises(Exception):
            await org_customer_manager.delete("999")  # type: ignore
        await session.rollback()
    @pytest.mark.asyncio
    async def test_get_list(
        self,
        org_customer_manager: OrgCustomerManager,
        session: AsyncSession
    ):
        """
        Test case for the `get_list` method of the
        `OrgCustomerManager` class.
        This test verifies that the `get_list`
        method returns the correct list of org_customers.
        Steps:
        1. Call the `get_list` method of the
            `org_customer_manager` instance.
        2. Assert that the returned list is empty.
        3. Create 5 org_customer objects using the
            `OrgCustomerFactory.create_async` method.
        4. Assert that the `org_customers_data` variable is of type `List`.
        5. Call the `get_list` method of the
            `org_customer_manager` instance again.
        6. Assert that the returned list contains 5 org_customers.
        7. Assert that all elements in the returned list are
            instances of the `OrgCustomer` class.
        """
        org_customers = await org_customer_manager.get_list()
        assert len(org_customers) == 0
        org_customers_data = (
            [await OrgCustomerFactory.create_async(session) for _ in range(5)])
        assert isinstance(org_customers_data, List)
        org_customers = await org_customer_manager.get_list()
        assert len(org_customers) == 5
        assert all(isinstance(
            org_customer, OrgCustomer) for org_customer in org_customers)
    @pytest.mark.asyncio
    async def test_to_json(
        self,
        org_customer_manager: OrgCustomerManager,
        session: AsyncSession
    ):
        """
        Test the 'to_json' method of the OrgCustomerManager class.
        Args:
            org_customer_manager (OrgCustomerManager): An
                instance of the
                OrgCustomerManager class.
            session (AsyncSession): An instance of the AsyncSession class.
        Returns:
            None
        Raises:
            AssertionError: If the json_data is None.
        """
        org_customer = await OrgCustomerFactory.build_async(
            session)
        json_data = org_customer_manager.to_json(
            org_customer)
        assert json_data is not None
    @pytest.mark.asyncio
    async def test_to_dict(
        self,
        org_customer_manager: OrgCustomerManager,
        session: AsyncSession
    ):
        """
        Test the to_dict method of the OrgCustomerManager class.
        Args:
            org_customer_manager (OrgCustomerManager): An
                instance of the
                OrgCustomerManager class.
            session (AsyncSession): An instance of the AsyncSession class.
        Returns:
            None
        """
        org_customer = await OrgCustomerFactory.build_async(
            session)
        dict_data = org_customer_manager.to_dict(
            org_customer)
        assert dict_data is not None
    @pytest.mark.asyncio
    async def test_from_json(
        self,
        org_customer_manager: OrgCustomerManager,
        session: AsyncSession
    ):
        """
        Test the `from_json` method of the `OrgCustomerManager` class.
        This method tests the functionality of the
        `from_json` method of the `OrgCustomerManager` class.
        It creates a org_customer using
        the `OrgCustomerFactory`
        and converts it to JSON using the `to_json` method.
        Then, it deserializes the JSON data using the
        `from_json` method and asserts that the deserialized
        org_customer is an instance of the
        `OrgCustomer` class and has
        the same code as the original org_customer.
        Args:
            org_customer_manager (OrgCustomerManager): An
            instance of the
                `OrgCustomerManager` class.
            session (AsyncSession): An instance of the `AsyncSession` class.
        Returns:
            None
        """
        org_customer = await OrgCustomerFactory.create_async(
            session)
        json_data = org_customer_manager.to_json(
            org_customer)
        deserialized_org_customer = org_customer_manager.from_json(json_data)
        assert isinstance(deserialized_org_customer, OrgCustomer)
        assert deserialized_org_customer.code == \
            org_customer.code
    @pytest.mark.asyncio
    async def test_from_dict(
        self,
        org_customer_manager: OrgCustomerManager,
        session: AsyncSession
    ):
        """
        Test the `from_dict` method of the
        `OrgCustomerManager` class.
        This method tests the functionality of the
        `from_dict` method, which is used to deserialize
        a dictionary representation of a
        org_customer object.
        Args:
            org_customer_manager (OrgCustomerManager): An instance
                of the `OrgCustomerManager` class.
            session (AsyncSession): An instance of the `AsyncSession` class.
        Returns:
            None
        Raises:
            AssertionError: If any of the assertions fail.
        """
        org_customer = await OrgCustomerFactory.create_async(
            session)
        schema = OrgCustomerSchema()
        org_customer_data = schema.dump(org_customer)
        assert isinstance(org_customer_data, dict)
        deserialized_org_customer = org_customer_manager.from_dict(
            org_customer_data)
        assert isinstance(deserialized_org_customer, OrgCustomer)
        assert deserialized_org_customer.code == \
            org_customer.code
    @pytest.mark.asyncio
    async def test_add_bulk(
        self,
        org_customer_manager: OrgCustomerManager,
        session: AsyncSession
    ):
        """
        Test case for the `add_bulk` method of the
        `OrgCustomerManager` class.
        This test case verifies that the `add_bulk`
        method correctly adds multiple org_customers to the database.
        Steps:
        1. Generate a list of org_customer data using the
            `OrgCustomerFactory.build_async` method.
        2. Call the `add_bulk` method of the
            `org_customer_manager` instance,
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
        org_customers = await org_customer_manager.add_bulk(
            org_customers_data)
        assert len(org_customers) == 5
        for updated_org_customer in org_customers:
            result = await session.execute(
                select(OrgCustomer).filter(
                    OrgCustomer._org_customer_id == updated_org_customer.org_customer_id  # type: ignore
                )
            )
            fetched_org_customer = result.scalars().first()
            assert isinstance(fetched_org_customer, OrgCustomer)
            assert str(fetched_org_customer.insert_user_id) == (
                str(org_customer_manager._session_context.customer_code))
            assert str(fetched_org_customer.last_update_user_id) == (
                str(org_customer_manager._session_context.customer_code))
            assert fetched_org_customer.org_customer_id == \
                updated_org_customer.org_customer_id
    @pytest.mark.asyncio
    async def test_update_bulk_success(
        self,
        org_customer_manager: OrgCustomerManager,
        session: AsyncSession
    ):
        """
        Test case for bulk update of org_customers.
        This test case verifies the functionality of the
        `update_bulk` method in the `OrgCustomerManager` class.
        It creates two org_customer instances,
        updates their codes
        using the `update_bulk` method, and then verifies
        that the updates were successful by checking the
        updated codes in the database.
        Steps:
        1. Create two org_customer instances using the
            `OrgCustomerFactory.create_async` method.
        2. Generate new codes for the org_customers.
        3. Update the org_customers' codes using the `update_bulk` method.
        4. Verify that the update was successful by checking
            the updated codes in the database.
        Args:
            org_customer_manager (OrgCustomerManager): An instance of the
                `OrgCustomerManager` class.
            session (AsyncSession): An instance of the `AsyncSession` class.
        Returns:
            None
        """
        # Mocking org_customer instances
        org_customer1 = await OrgCustomerFactory.create_async(
            session=session)
        org_customer2 = await OrgCustomerFactory.create_async(
            session=session)
        logging.info(org_customer1.__dict__)
        code_updated1 = uuid.uuid4()
        code_updated2 = uuid.uuid4()
        logging.info(code_updated1)
        logging.info(code_updated2)
        # Update org_customers
        updates = [
            {
                "org_customer_id": org_customer1.org_customer_id,
                "code": code_updated1
            },
            {
                "org_customer_id": org_customer2.org_customer_id,
                "code": code_updated2
            }
        ]
        updated_org_customers = await org_customer_manager.update_bulk(
            updates)
        logging.info('bulk update results')
        # Assertions
        assert len(updated_org_customers) == 2
        logging.info(updated_org_customers[0].__dict__)
        logging.info(updated_org_customers[1].__dict__)
        logging.info('getall')
        org_customers = await org_customer_manager.get_list()
        logging.info(org_customers[0].__dict__)
        logging.info(org_customers[1].__dict__)
        assert updated_org_customers[0].code == code_updated1
        assert updated_org_customers[1].code == code_updated2
        assert str(updated_org_customers[0].last_update_user_id) == (
            str(org_customer_manager._session_context.customer_code))
        assert str(updated_org_customers[1].last_update_user_id) == (
            str(org_customer_manager._session_context.customer_code))
        result = await session.execute(
            select(OrgCustomer).filter(
                OrgCustomer._org_customer_id == 1)  # type: ignore
        )
        fetched_org_customer = result.scalars().first()
        assert isinstance(fetched_org_customer, OrgCustomer)
        assert fetched_org_customer.code == code_updated1
        result = await session.execute(
            select(OrgCustomer).filter(
                OrgCustomer._org_customer_id == 2)  # type: ignore
        )
        fetched_org_customer = result.scalars().first()
        assert isinstance(fetched_org_customer, OrgCustomer)
        assert fetched_org_customer.code == code_updated2
    @pytest.mark.asyncio
    async def test_update_bulk_missing_org_customer_id(
        self,
        org_customer_manager: OrgCustomerManager,
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
        # No org_customers to update since org_customer_id is missing
        updates = [{"name": "Red Rose"}]
        with pytest.raises(Exception):
            await org_customer_manager.update_bulk(updates)
        await session.rollback()
    @pytest.mark.asyncio
    async def test_update_bulk_org_customer_not_found(
        self,
        org_customer_manager: OrgCustomerManager,
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
            org_customer_manager with the list of updates.
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
            await org_customer_manager.update_bulk(updates)
        await session.rollback()
    @pytest.mark.asyncio
    async def test_update_bulk_invalid_type(
        self,
        org_customer_manager: OrgCustomerManager,
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
        :param org_customer_manager: An instance of the OrgCustomerManager class.
        :param session: An instance of the AsyncSession class.
        """
        updates = [{"org_customer_id": "2", "code": uuid.uuid4()}]
        with pytest.raises(Exception):
            await org_customer_manager.update_bulk(updates)
        await session.rollback()
    @pytest.mark.asyncio
    async def test_delete_bulk_success(
        self,
        org_customer_manager: OrgCustomerManager,
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
            of the org_customer_manager.
        3. Verify that the delete operation was successful by
            checking if the org_customers no longer exist in the database.
        Expected Result:
        - The delete_bulk method should return True, indicating
            that the delete operation was successful.
        - The org_customers should no longer exist in the database.
        """
        org_customer1 = await OrgCustomerFactory.create_async(
            session=session)
        org_customer2 = await OrgCustomerFactory.create_async(
            session=session)
        # Delete org_customers
        org_customer_ids = [org_customer1.org_customer_id, org_customer2.org_customer_id]
        result = await org_customer_manager.delete_bulk(
            org_customer_ids)
        assert result is True
        for org_customer_id in org_customer_ids:
            execute_result = await session.execute(
                select(OrgCustomer).filter(
                    OrgCustomer._org_customer_id == org_customer_id)  # type: ignore
            )
            fetched_org_customer = execute_result.scalars().first()
            assert fetched_org_customer is None
    @pytest.mark.asyncio
    async def test_delete_bulk_org_customers_not_found(
        self,
        org_customer_manager: OrgCustomerManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of deleting bulk
        org_customers when some org_customers are not found.
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
        org_customer1 = await OrgCustomerFactory.create_async(
            session=session)
        assert isinstance(org_customer1, OrgCustomer)
        # Delete org_customers
        org_customer_ids = [1, 2]
        with pytest.raises(Exception):
            await org_customer_manager.delete_bulk(
                org_customer_ids)
        await session.rollback()
    @pytest.mark.asyncio
    async def test_delete_bulk_empty_list(
        self,
        org_customer_manager: OrgCustomerManager
    ):
        """
        Test case to verify the behavior of deleting
        org_customers with an empty list.
        Args:
            org_customer_manager (OrgCustomerManager): The
                instance of the
                OrgCustomerManager class.
        Returns:
            None
        Raises:
            AssertionError: If the result is not True.
        """
        # Delete org_customers with an empty list
        org_customer_ids = []
        result = await org_customer_manager.delete_bulk(
            org_customer_ids)
        # Assertions
        assert result is True
    @pytest.mark.asyncio
    async def test_delete_bulk_invalid_type(
        self,
        org_customer_manager: OrgCustomerManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of the delete_bulk
        method when invalid org_customer IDs are provided.
        Args:
            org_customer_manager (OrgCustomerManager): The
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
            await org_customer_manager.delete_bulk(
                org_customer_ids)
        await session.rollback()
    @pytest.mark.asyncio
    async def test_count_basic_functionality(
        self,
        org_customer_manager: OrgCustomerManager,
        session: AsyncSession
    ):
        """
        Test the basic functionality of the count method
        in the OrgCustomerManager class.
        This test case creates 5 org_customer
        objects using the
        OrgCustomerFactory and checks if the count method
        returns the correct count of
        org_customers.
        Steps:
        1. Create 5 org_customer objects using
            the OrgCustomerFactory.
        2. Call the count method of the org_customer_manager.
        3. Assert that the count is equal to 5.
        """
        org_customers_data = (
            [await OrgCustomerFactory.create_async(session) for _ in range(5)])
        assert isinstance(org_customers_data, List)
        count = await org_customer_manager.count()
        assert count == 5
    @pytest.mark.asyncio
    async def test_count_empty_database(
        self,
        org_customer_manager: OrgCustomerManager
    ):
        """
        Test the count method when the database is empty.
        This test case checks if the count method of the
        OrgCustomerManager class returns 0 when the database is empty.
        Args:
            org_customer_manager (OrgCustomerManager): An
                instance of the
                OrgCustomerManager class.
        Returns:
            None
        """
        count = await org_customer_manager.count()
        assert count == 0
    @pytest.mark.asyncio
    async def test_get_sorted_list_basic_sorting(
        self,
        org_customer_manager: OrgCustomerManager,
        session: AsyncSession
    ):
        """
        Test case for the 'get_sorted_list' method with basic sorting.
        This test case verifies that the 'get_sorted_list'
        method returns a list of org_customers
        sorted by the '_org_customer_id' attribute in ascending order.
        Steps:
        1. Add org_customers to the database.
        2. Call the 'get_sorted_list' method with the
            sort_by parameter set to '_org_customer_id'.
        3. Verify that the returned list of org_customers is
            sorted by the '_org_customer_id' attribute.
        """
        # Add org_customers
        org_customers_data = (
            [await OrgCustomerFactory.create_async(session) for _ in range(5)])
        assert isinstance(org_customers_data, List)
        sorted_org_customers = await org_customer_manager.get_sorted_list(
            sort_by="_org_customer_id")
        assert [org_customer.org_customer_id for org_customer in sorted_org_customers] == (
            [(i + 1) for i in range(5)])
    @pytest.mark.asyncio
    async def test_get_sorted_list_descending_sorting(
        self,
        org_customer_manager: OrgCustomerManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of the
        'get_sorted_list' method
        when sorting the list of org_customers in descending order.
        Steps:
        1. Create a list of org_customers using the OrgCustomerFactory.
        2. Assert that the org_customers_data is of type List.
        3. Call the 'get_sorted_list' method with
            sort_by="org_customer_id" and order="desc".
        4. Assert that the org_customer_ids of the
            sorted_org_customers are in descending order.
        """
        # Add org_customers
        org_customers_data = (
            [await OrgCustomerFactory.create_async(session) for _ in range(5)])
        assert isinstance(org_customers_data, List)
        sorted_org_customers = await org_customer_manager.get_sorted_list(
            sort_by="org_customer_id", order="desc")
        assert [org_customer.org_customer_id for org_customer in sorted_org_customers] == (
            [(i + 1) for i in reversed(range(5))])
    @pytest.mark.asyncio
    async def test_get_sorted_list_invalid_attribute(
        self,
        org_customer_manager: OrgCustomerManager,
        session: AsyncSession
    ):
        """
        Test case to check if an AttributeError is raised when
        sorting the list by an invalid attribute.
        Args:
            org_customer_manager (OrgCustomerManager): The
                instance of the
                OrgCustomerManager class.
            session (AsyncSession): The instance of the AsyncSession class.
        Raises:
            AttributeError: If an invalid attribute is used for sorting.
        Returns:
            None
        """
        with pytest.raises(AttributeError):
            await org_customer_manager.get_sorted_list(
                sort_by="invalid_attribute")
        await session.rollback()
    @pytest.mark.asyncio
    async def test_get_sorted_list_empty_database(
        self,
        org_customer_manager: OrgCustomerManager
    ):
        """
        Test case to verify the behavior of
        `get_sorted_list` method when the database is empty.
        This test ensures that when the database is empty, the
        `get_sorted_list` method returns an empty list.
        Args:
            org_customer_manager (OrgCustomerManager): An
                instance of the
                OrgCustomerManager class.
        Returns:
            None
        """
        sorted_org_customers = await org_customer_manager.get_sorted_list(
            sort_by="org_customer_id")
        assert len(sorted_org_customers) == 0
    @pytest.mark.asyncio
    async def test_refresh_basic(
        self,
        org_customer_manager: OrgCustomerManager,
        session: AsyncSession
    ):
        """
        Test the basic functionality of refreshing
        a org_customer instance.
        This test performs the following steps:
        1. Creates a org_customer instance using
            the OrgCustomerFactory.
        2. Retrieves the org_customer from th
            database to ensure
            it was added correctly.
        3. Updates the org_customer's code and verifies the update.
        4. Refreshes the original org_customer instance
            and checks if
            it reflects the updated code.
        Args:
            org_customer_manager (OrgCustomerManager): The
                manager responsible
                for org_customer operations.
            session (AsyncSession): The SQLAlchemy asynchronous session.
        """
        # Add a org_customer
        org_customer1 = await OrgCustomerFactory.create_async(
            session=session)
        # Retrieve the org_customer from the database
        result = await session.execute(
            select(OrgCustomer).filter(
                OrgCustomer._org_customer_id == org_customer1.org_customer_id)  # type: ignore
        )  # type: ignore
        org_customer2 = result.scalars().first()
        # Verify that the retrieved org_customer
        # matches the added org_customer
        assert org_customer1.code == \
            org_customer2.code
        # Update the org_customer's code
        updated_code1 = uuid.uuid4()
        org_customer1.code = updated_code1
        updated_org_customer1 = await org_customer_manager.update(
            org_customer1)
        # Verify that the updated org_customer
        # is of type OrgCustomer
        # and has the updated code
        assert isinstance(updated_org_customer1, OrgCustomer)
        assert updated_org_customer1.code == updated_code1
        # Refresh the original org_customer instance
        refreshed_org_customer2 = await org_customer_manager.refresh(
            org_customer2)
        # Verify that the refreshed org_customer
        # reflects the updated code
        assert refreshed_org_customer2.code == updated_code1
    @pytest.mark.asyncio
    async def test_refresh_nonexistent_org_customer(
        self,
        org_customer_manager: OrgCustomerManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of refreshing a nonexistent org_customer.
        Args:
            org_customer_manager (OrgCustomerManager): The
                instance of the
                OrgCustomerManager class.
            session (AsyncSession): The instance of the AsyncSession class.
        Raises:
            Exception: If the org_customer
            refresh operation raises an exception.
        Returns:
            None
        """
        org_customer = OrgCustomer(
            org_customer_id=999)
        with pytest.raises(Exception):
            await org_customer_manager.refresh(
                org_customer)
        await session.rollback()
    @pytest.mark.asyncio
    async def test_exists_with_existing_org_customer(
        self,
        org_customer_manager: OrgCustomerManager,
        session: AsyncSession
    ):
        """
        Test case to check if a org_customer
        exists using the manager function.
        Args:
            org_customer_manager (OrgCustomerManager): The
                org_customer manager instance.
            session (AsyncSession): The async session object.
        Returns:
            None
        """
        # Add a org_customer
        org_customer1 = await OrgCustomerFactory.create_async(
            session=session)
        # Check if the org_customer exists
        # using the manager function
        assert await org_customer_manager.exists(
            org_customer1.org_customer_id) is True
    @pytest.mark.asyncio
    async def test_is_equal_with_existing_org_customer(
        self,
        org_customer_manager: OrgCustomerManager,
        session: AsyncSession
    ):
        """
        Test if the is_equal method of the
        OrgCustomerManager class correctly compares two org_customers.
        Args:
            org_customer_manager (OrgCustomerManager): An
                instance of the
                OrgCustomerManager class.
            session (AsyncSession): An instance of the AsyncSession class.
        Returns:
            None
        """
        # Add a org_customer
        org_customer1 = await OrgCustomerFactory.create_async(
            session=session)
        org_customer2 = await org_customer_manager.get_by_id(
            org_customer_id=org_customer1.org_customer_id)
        assert org_customer_manager.is_equal(
            org_customer1, org_customer2) is True
        org_customer1_dict = org_customer_manager.to_dict(
            org_customer1)
        org_customer3 = org_customer_manager.from_dict(
            org_customer1_dict)
        assert org_customer_manager.is_equal(
            org_customer1, org_customer3) is True
    @pytest.mark.asyncio
    async def test_exists_with_nonexistent_org_customer(
        self,
        org_customer_manager: OrgCustomerManager
    ):
        """
        Test case to check if a org_customer with a
        non-existent ID exists in the database.
        Args:
            org_customer_manager (OrgCustomerManager): The
                instance of the OrgCustomerManager class.
        Returns:
            bool: True if the org_customer exists,
                False otherwise.
        """
        non_existent_id = 999
        assert await org_customer_manager.exists(non_existent_id) is False
    @pytest.mark.asyncio
    async def test_exists_with_invalid_id_type(
        self,
        org_customer_manager: OrgCustomerManager,
        session: AsyncSession
    ):
        """
        Test case to check if the exists method raises
        an exception when an invalid ID type is provided.
        Args:
            org_customer_manager (OrgCustomerManager): The instance
                of the OrgCustomerManager class.
            session (AsyncSession): The instance of the AsyncSession class.
        Raises:
            Exception: If an exception is not raised by the exists method.
        Returns:
            None
        """
        invalid_id = "invalid_id"
        with pytest.raises(Exception):
            await org_customer_manager.exists(invalid_id)  # type: ignore  # noqa: E501
        await session.rollback()
# endset
    # CustomerID
    @pytest.mark.asyncio
    async def test_get_by_customer_id_existing(
        self,
        org_customer_manager: OrgCustomerManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of the
        `get_by_customer_id` method
        when a org_customer with a
        specific customer_id exists.
        Steps:
        1. Create a org_customer using the
            OrgCustomerFactory.
        2. Fetch the org_customer using the
            `get_by_customer_id`
            method of the org_customer_manager.
        3. Assert that the fetched org_customers list has a length of 1.
        4. Assert that the first element in the fetched
            org_customers list is an instance of the
            OrgCustomer class.
        5. Assert that the code of the fetched
            org_customer
            matches the code of the created org_customer.
        6. Execute a select statement to fetch the
            Customer object associated with the
            customer_id.
        7. Assert that the fetched customer is an
            instance of the Customer class.
        8. Assert that the customer_code_peek
            of the fetched org_customer matches
            the code of the fetched customer.
        """
        # Add a org_customer with a specific
        # customer_id
        org_customer1 = await OrgCustomerFactory.create_async(
            session=session)
        # Fetch the org_customer using the
        # manager function
        fetched_org_customers = await org_customer_manager.get_by_customer_id(
            org_customer1.customer_id)
        assert len(fetched_org_customers) == 1
        assert isinstance(fetched_org_customers[0], OrgCustomer)
        assert fetched_org_customers[0].code == \
            org_customer1.code
        stmt = select(models.Customer).where(
            models.Customer._customer_id == org_customer1.customer_id)  # type: ignore  # noqa: E501
        result = await session.execute(stmt)
        customer = result.scalars().first()
        assert isinstance(customer, models.Customer)
        assert fetched_org_customers[0].customer_code_peek == customer.code
    @pytest.mark.asyncio
    async def test_get_by_customer_id_nonexistent(
        self,
        org_customer_manager: OrgCustomerManager
    ):
        """
        Test case to verify the behavior of the
        'get_by_customer_id' method
        when the provided foreign key ID does
        not exist in the database.
        This test ensures that when a non-existent
        foreign key ID is passed to the
        'get_by_customer_id' method, it
        returns an empty list.
        Steps:
        1. Set a non-existent foreign key ID.
        2. Call the 'get_by_customer_id'
            method with the non-existent ID.
        3. Assert that the returned list of fetched org_customers is empty.
        """
        non_existent_id = 999
        fetched_org_customers = (
            await org_customer_manager.get_by_customer_id(
                non_existent_id))
        assert len(fetched_org_customers) == 0
    @pytest.mark.asyncio
    async def test_get_by_customer_id_invalid_type(
        self,
        org_customer_manager: OrgCustomerManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of the
        `get_by_customer_id` method
        when an invalid foreign key ID type is provided.
        It ensures that an exception is raised
        when an invalid ID is passed to the method.
        Args:
            org_customer_manager (OrgCustomerManager): The
                instance of the OrgCustomerManager class.
            session (AsyncSession): The instance of the AsyncSession class.
        Raises:
            Exception: If an exception is not
                raised when an invalid ID is passed.
        """
        invalid_id = "invalid_id"
        with pytest.raises(Exception):
            await org_customer_manager.get_by_customer_id(
                invalid_id)  # type: ignore  # noqa: E501
        await session.rollback()
    # email,
    # OrganizationID
    @pytest.mark.asyncio
    async def test_get_by_organization_id_existing(
        self,
        org_customer_manager: OrgCustomerManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of the
        `get_by_organization_id` method when
        a org_customer with
        a specific organization_id exists.
        Steps:
        1. Create a org_customer using the
            OrgCustomerFactory.
        2. Fetch the org_customer using the
            `get_by_organization_id` method of the org_customer_manager.
        3. Assert that the fetched org_customers list contains
            only one org_customer.
        4. Assert that the fetched org_customer
            is an instance
            of the OrgCustomer class.
        5. Assert that the code of the fetched org_customer
            matches the code of the created org_customer.
        6. Fetch the corresponding organization object
            using the organization_id of the created org_customer.
        7. Assert that the fetched organization object is
            an instance of the Organization class.
        8. Assert that the organization_code_peek of the fetched
            org_customer matches the
            code of the fetched organization.
        """
        # Add a org_customer with a specific
        # organization_id
        org_customer1 = await OrgCustomerFactory.create_async(
            session=session)
        # Fetch the org_customer using
        # the manager function
        fetched_org_customers = await org_customer_manager.get_by_organization_id(
            org_customer1.organization_id)
        assert len(fetched_org_customers) == 1
        assert isinstance(fetched_org_customers[0], OrgCustomer)
        assert fetched_org_customers[0].code == \
            org_customer1.code
        stmt = select(models.Organization).where(
            models.Organization._organization_id == org_customer1.organization_id)  # type: ignore  # noqa: E501
        result = await session.execute(stmt)
        organization = result.scalars().first()
        assert isinstance(organization, models.Organization)
        assert fetched_org_customers[0].organization_code_peek == organization.code
    @pytest.mark.asyncio
    async def test_get_by_organization_id_nonexistent(
        self,
        org_customer_manager: OrgCustomerManager
    ):
        """
        Test case to verify the behavior of the
        get_by_organization_id method when the organization ID does not exist.
        This test case ensures that when a non-existent
        organization ID is provided to the get_by_organization_id method,
        an empty list is returned.
        """
        non_existent_id = 999
        fetched_org_customers = await org_customer_manager.get_by_organization_id(
            non_existent_id)
        assert len(fetched_org_customers) == 0
    @pytest.mark.asyncio
    async def test_get_by_organization_id_invalid_type(
        self,
        org_customer_manager: OrgCustomerManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of the
        `get_by_organization_id` method when an invalid organization ID is provided.
        Args:
            org_customer_manager (OrgCustomerManager): An
                instance of the OrgCustomerManager class.
            session (AsyncSession): An instance
                of the AsyncSession class.
        Raises:
            Exception: If an exception is raised during
            the execution of the `get_by_organization_id` method.
        Returns:
            None
        """
        invalid_id = "invalid_id"
        with pytest.raises(Exception):
            await org_customer_manager.get_by_organization_id(
                invalid_id)  # type: ignore
        await session.rollback()
# endset
