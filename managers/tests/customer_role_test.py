# models/managers/tests/customer_role_test.py
# pylint: disable=protected-access
# pylint: disable=unused-argument
"""
    This class contains unit tests for the
    `CustomerRoleManager` class.
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
from managers.customer_role import CustomerRoleManager
from models import CustomerRole
from models.factory import CustomerRoleFactory
from models.serialization_schema.customer_role import CustomerRoleSchema
class TestCustomerRoleManager:
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
    async def test_build(
        self,
        customer_role_manager: CustomerRoleManager
    ):
        """
        Test case for the `build` method of
        `CustomerRoleManager`.
        """
        # Define mock data for our customer_role
        mock_data = {
            "code": uuid.uuid4()
        }
        # Call the build function of the manager
        customer_role = await customer_role_manager.build(**mock_data)
        # Assert that the returned object is an instance of CustomerRole
        assert isinstance(customer_role, CustomerRole)
        # Assert that the attributes of the customer_role match our mock data
        assert customer_role.code == mock_data["code"]
    @pytest.mark.asyncio
    async def test_build_with_missing_data(
        self,
        customer_role_manager: CustomerRoleManager,
        session: AsyncSession
    ):
        """
        Test case for the `build` method of
        `CustomerRoleManager` with missing data.
        """
        # Define mock data with a missing key
        mock_data = {
            "non_existant_property": "Rose"
        }
        # If the build method is expected to raise an exception for
        # missing data, test for that
        with pytest.raises(Exception):
            await customer_role_manager.build(**mock_data)
        await session.rollback()
    @pytest.mark.asyncio
    async def test_add_correctly_adds_customer_role_to_database(
        self,
        customer_role_manager: CustomerRoleManager,
        session: AsyncSession
    ):
        """
        Test case for the `add` method of
        `CustomerRoleManager` that checks if a
        customer_role is correctly added to the database.
        """
        test_customer_role = await CustomerRoleFactory.build_async(session)
        assert test_customer_role.customer_role_id == 0
        # Add the customer_role using the manager's add method
        added_customer_role = await customer_role_manager.add(customer_role=test_customer_role)
        assert isinstance(added_customer_role, CustomerRole)
        assert str(added_customer_role.insert_user_id) == (
            str(customer_role_manager._session_context.customer_code))
        assert str(added_customer_role.last_update_user_id) == (
            str(customer_role_manager._session_context.customer_code))
        assert added_customer_role.customer_role_id > 0
        # Fetch the customer_role from the database directly
        result = await session.execute(
            select(CustomerRole).filter(
                CustomerRole._customer_role_id == added_customer_role.customer_role_id  # type: ignore
            )
        )
        fetched_customer_role = result.scalars().first()
        # Assert that the fetched customer_role is not None and matches the added customer_role
        assert fetched_customer_role is not None
        assert isinstance(fetched_customer_role, CustomerRole)
        assert fetched_customer_role.customer_role_id == added_customer_role.customer_role_id
    @pytest.mark.asyncio
    async def test_add_returns_correct_customer_role_object(
        self,
        customer_role_manager: CustomerRoleManager,
        session: AsyncSession
    ):
        """
        Test case for the `add` method of
        `CustomerRoleManager` that checks if the
        correct customer_role object is returned.
        """
        # Create a test customer_role using the CustomerRoleFactory
        # without persisting it to the database
        test_customer_role = await CustomerRoleFactory.build_async(session)
        assert test_customer_role.customer_role_id == 0
        test_customer_role.code = uuid.uuid4()
        # Add the customer_role using the manager's add method
        added_customer_role = await customer_role_manager.add(customer_role=test_customer_role)
        assert isinstance(added_customer_role, CustomerRole)
        assert str(added_customer_role.insert_user_id) == (
            str(customer_role_manager._session_context.customer_code))
        assert str(added_customer_role.last_update_user_id) == (
            str(customer_role_manager._session_context.customer_code))
        assert added_customer_role.customer_role_id > 0
        # Assert that the returned customer_role matches the test customer_role
        assert added_customer_role.customer_role_id == test_customer_role.customer_role_id
        assert added_customer_role.code == test_customer_role.code
    @pytest.mark.asyncio
    async def test_get_by_id(
        self,
        customer_role_manager: CustomerRoleManager,
        session: AsyncSession
    ):
        """
        Test case for the `get_by_id` method of
        `CustomerRoleManager`.
        """
        test_customer_role = await CustomerRoleFactory.create_async(session)
        customer_role = await customer_role_manager.get_by_id(test_customer_role.customer_role_id)
        assert isinstance(customer_role, CustomerRole)
        assert test_customer_role.customer_role_id == customer_role.customer_role_id
        assert test_customer_role.code == customer_role.code
    @pytest.mark.asyncio
    async def test_get_by_id_not_found(
        self,
        customer_role_manager: CustomerRoleManager
    ):
        """
        Test case for the `get_by_id` method of
        `CustomerRoleManager` when the customer_role is not found.
        """
        non_existent_id = 9999  # An ID that's not in the database
        retrieved_customer_role = await customer_role_manager.get_by_id(non_existent_id)
        assert retrieved_customer_role is None
    @pytest.mark.asyncio
    async def test_get_by_code_returns_customer_role(
        self,
        customer_role_manager: CustomerRoleManager,
        session: AsyncSession
    ):
        """
        Test case for the `get_by_code` method of
        `CustomerRoleManager` that checks if a customer_role is
        returned by its code.
        """
        test_customer_role = await CustomerRoleFactory.create_async(session)
        customer_role = await customer_role_manager.get_by_code(test_customer_role.code)
        assert isinstance(customer_role, CustomerRole)
        assert test_customer_role.customer_role_id == customer_role.customer_role_id
        assert test_customer_role.code == customer_role.code
    @pytest.mark.asyncio
    async def test_get_by_code_returns_none_for_nonexistent_code(
        self,
        customer_role_manager: CustomerRoleManager
    ):
        """
        Test case for the `get_by_code` method of
        `CustomerRoleManager` when the code does not exist.
        """
        # Generate a random UUID that doesn't correspond to
        # any CustomerRole in the database
        random_code = uuid.uuid4()
        customer_role = await customer_role_manager.get_by_code(random_code)
        assert customer_role is None
    @pytest.mark.asyncio
    async def test_update(
        self,
        customer_role_manager: CustomerRoleManager,
        session: AsyncSession
    ):
        """
        Test case for the `update` method of `CustomerRoleManager`
        that checks if a customer_role is correctly updated.
        """
        test_customer_role = await CustomerRoleFactory.create_async(session)
        test_customer_role.code = uuid.uuid4()
        updated_customer_role = await customer_role_manager.update(customer_role=test_customer_role)
        assert isinstance(updated_customer_role, CustomerRole)
        assert str(updated_customer_role.last_update_user_id) == str(
            customer_role_manager._session_context.customer_code)
        assert updated_customer_role.customer_role_id == test_customer_role.customer_role_id
        assert updated_customer_role.code == test_customer_role.code
        result = await session.execute(
            select(CustomerRole).filter(
                CustomerRole._customer_role_id == test_customer_role.customer_role_id)  # type: ignore
        )
        fetched_customer_role = result.scalars().first()
        assert updated_customer_role.customer_role_id == fetched_customer_role.customer_role_id
        assert updated_customer_role.code == fetched_customer_role.code
        assert test_customer_role.customer_role_id == fetched_customer_role.customer_role_id
        assert test_customer_role.code == fetched_customer_role.code
    @pytest.mark.asyncio
    async def test_update_via_dict(
        self,
        customer_role_manager: CustomerRoleManager,
        session: AsyncSession
    ):
        """
        Test case for the `update` method of `CustomerRoleManager`
        that checks if a customer_role is correctly updated using a dictionary.
        """
        test_customer_role = await CustomerRoleFactory.create_async(session)
        new_code = uuid.uuid4()
        updated_customer_role = await customer_role_manager.update(
            customer_role=test_customer_role,
            code=new_code
        )
        assert isinstance(updated_customer_role, CustomerRole)
        assert str(updated_customer_role.last_update_user_id) == str(
            customer_role_manager._session_context.customer_code
        )
        assert updated_customer_role.customer_role_id == test_customer_role.customer_role_id
        assert updated_customer_role.code == new_code
        result = await session.execute(
            select(CustomerRole).filter(
                CustomerRole._customer_role_id == test_customer_role.customer_role_id)  # type: ignore
        )
        fetched_customer_role = result.scalars().first()
        assert updated_customer_role.customer_role_id == fetched_customer_role.customer_role_id
        assert updated_customer_role.code == fetched_customer_role.code
        assert test_customer_role.customer_role_id == fetched_customer_role.customer_role_id
        assert new_code == fetched_customer_role.code
    @pytest.mark.asyncio
    async def test_update_invalid_customer_role(
        self,
        customer_role_manager: CustomerRoleManager
    ):
        """
        Test case for the `update` method of `CustomerRoleManager`
        with an invalid customer_role.
        """
        # None customer_role
        customer_role = None
        new_code = uuid.uuid4()
        updated_customer_role = await (
            customer_role_manager.update(customer_role, code=new_code))  # type: ignore
        # Assertions
        assert updated_customer_role is None
    @pytest.mark.asyncio
    async def test_update_with_nonexistent_attribute(
        self,
        customer_role_manager: CustomerRoleManager,
        session: AsyncSession
    ):
        """
        Test case for the `update` method of `CustomerRoleManager`
        with a nonexistent attribute.
        """
        test_customer_role = await CustomerRoleFactory.create_async(session)
        new_code = uuid.uuid4()
        with pytest.raises(ValueError):
            await customer_role_manager.update(
                customer_role=test_customer_role,
                xxx=new_code
            )
        await session.rollback()
    @pytest.mark.asyncio
    async def test_delete(
        self,
        customer_role_manager: CustomerRoleManager,
        session: AsyncSession
    ):
        """
        Test case for the `delete` method of `CustomerRoleManager`.
        """
        customer_role_data = await CustomerRoleFactory.create_async(session)
        result = await session.execute(
            select(CustomerRole).filter(
                CustomerRole._customer_role_id == customer_role_data.customer_role_id)  # type: ignore
        )
        fetched_customer_role = result.scalars().first()
        assert isinstance(fetched_customer_role, CustomerRole)
        assert fetched_customer_role.customer_role_id == customer_role_data.customer_role_id
        await customer_role_manager.delete(
            customer_role_id=customer_role_data.customer_role_id)
        result = await session.execute(
            select(CustomerRole).filter(
                CustomerRole._customer_role_id == customer_role_data.customer_role_id)  # type: ignore
        )
        fetched_customer_role = result.scalars().first()
        assert fetched_customer_role is None
    @pytest.mark.asyncio
    async def test_delete_nonexistent(
        self,
        customer_role_manager: CustomerRoleManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of deleting a nonexistent customer_role.
        This test case ensures that when the delete method
        is called with the ID of a nonexistent customer_role,
        an exception is raised. The test also verifies that
        the session is rolled back after the delete operation.
        :param customer_role_manager: The instance of the CustomerRoleManager class.
        :param session: The instance of the AsyncSession class.
        """
        with pytest.raises(Exception):
            await customer_role_manager.delete(999)
        await session.rollback()
    @pytest.mark.asyncio
    async def test_delete_invalid_type(
        self,
        customer_role_manager: CustomerRoleManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of deleting a customer_role
        with an invalid type.
        This test case ensures that when the `delete` method
        of the `customer_role_manager` is called with an invalid type,
        an exception is raised. The test case expects the
        `delete` method to raise an exception, and if it doesn't,
        the test case will fail.
        Args:
            customer_role_manager (CustomerRoleManager): An instance of the
                `CustomerRoleManager` class.
            session (AsyncSession): An instance of the `AsyncSession` class.
        Returns:
            None
        Raises:
            Exception: If the `delete` method does not raise an exception.
        """
        with pytest.raises(Exception):
            await customer_role_manager.delete("999")  # type: ignore
        await session.rollback()
    @pytest.mark.asyncio
    async def test_get_list(
        self,
        customer_role_manager: CustomerRoleManager,
        session: AsyncSession
    ):
        """
        Test case for the `get_list` method of the
        `CustomerRoleManager` class.
        This test verifies that the `get_list`
        method returns the correct list of customer_roles.
        Steps:
        1. Call the `get_list` method of the
            `customer_role_manager` instance.
        2. Assert that the returned list is empty.
        3. Create 5 customer_role objects using the
            `CustomerRoleFactory.create_async` method.
        4. Assert that the `customer_roles_data` variable is of type `List`.
        5. Call the `get_list` method of the
            `customer_role_manager` instance again.
        6. Assert that the returned list contains 5 customer_roles.
        7. Assert that all elements in the returned list are
            instances of the `CustomerRole` class.
        """
        customer_roles = await customer_role_manager.get_list()
        assert len(customer_roles) == 0
        customer_roles_data = (
            [await CustomerRoleFactory.create_async(session) for _ in range(5)])
        assert isinstance(customer_roles_data, List)
        customer_roles = await customer_role_manager.get_list()
        assert len(customer_roles) == 5
        assert all(isinstance(customer_role, CustomerRole) for customer_role in customer_roles)
    @pytest.mark.asyncio
    async def test_to_json(
        self,
        customer_role_manager: CustomerRoleManager,
        session: AsyncSession
    ):
        """
        Test the 'to_json' method of the CustomerRoleManager class.
        Args:
            customer_role_manager (CustomerRoleManager): An instance of the
                CustomerRoleManager class.
            session (AsyncSession): An instance of the AsyncSession class.
        Returns:
            None
        Raises:
            AssertionError: If the json_data is None.
        """
        customer_role = await CustomerRoleFactory.build_async(session)
        json_data = customer_role_manager.to_json(customer_role)
        assert json_data is not None
    @pytest.mark.asyncio
    async def test_to_dict(
        self,
        customer_role_manager: CustomerRoleManager,
        session: AsyncSession
    ):
        """
        Test the to_dict method of the CustomerRoleManager class.
        Args:
            customer_role_manager (CustomerRoleManager): An instance of the
                CustomerRoleManager class.
            session (AsyncSession): An instance of the AsyncSession class.
        Returns:
            None
        """
        customer_role = await CustomerRoleFactory.build_async(session)
        dict_data = customer_role_manager.to_dict(customer_role)
        assert dict_data is not None
    @pytest.mark.asyncio
    async def test_from_json(
        self,
        customer_role_manager: CustomerRoleManager,
        session: AsyncSession
    ):
        """
        Test the `from_json` method of the `CustomerRoleManager` class.
        This method tests the functionality of the
        `from_json` method of the `CustomerRoleManager` class.
        It creates a customer_role using the `CustomerRoleFactory`
        and converts it to JSON using the `to_json` method.
        Then, it deserializes the JSON data using the
        `from_json` method and asserts that the deserialized
        customer_role is an instance of the `CustomerRole` class and has
        the same code as the original customer_role.
        Args:
            customer_role_manager (CustomerRoleManager): An instance of the
                `CustomerRoleManager` class.
            session (AsyncSession): An instance of the `AsyncSession` class.
        Returns:
            None
        """
        customer_role = await CustomerRoleFactory.create_async(session)
        json_data = customer_role_manager.to_json(customer_role)
        deserialized_customer_role = customer_role_manager.from_json(json_data)
        assert isinstance(deserialized_customer_role, CustomerRole)
        assert deserialized_customer_role.code == customer_role.code
    @pytest.mark.asyncio
    async def test_from_dict(
        self,
        customer_role_manager: CustomerRoleManager,
        session: AsyncSession
    ):
        """
        Test the `from_dict` method of the
        `CustomerRoleManager` class.
        This method tests the functionality of the
        `from_dict` method, which is used to deserialize
        a dictionary representation of a customer_role object.
        Args:
            customer_role_manager (CustomerRoleManager): An instance
                of the `CustomerRoleManager` class.
            session (AsyncSession): An instance of the `AsyncSession` class.
        Returns:
            None
        Raises:
            AssertionError: If any of the assertions fail.
        """
        customer_role = await CustomerRoleFactory.create_async(session)
        schema = CustomerRoleSchema()
        customer_role_data = schema.dump(customer_role)
        assert isinstance(customer_role_data, dict)
        deserialized_customer_role = customer_role_manager.from_dict(customer_role_data)
        assert isinstance(deserialized_customer_role, CustomerRole)
        assert deserialized_customer_role.code == customer_role.code
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
            `customer_role_manager` instance, passing in the generated customer_role data.
        3. Verify that the number of customer_roles returned is
            equal to the number of customer_roles added.
        4. For each updated customer_role, fetch the corresponding
            customer_role from the database.
        5. Verify that the fetched customer_role is an instance of the
            `CustomerRole` class.
        6. Verify that the insert_user_id and
            last_update_user_id of the fetched customer_role match the
            customer code of the session context.
        7. Verify that the customer_role_id of the fetched
            customer_role matches the customer_role_id of the updated customer_role.
        """
        customer_roles_data = [
            await CustomerRoleFactory.build_async(session) for _ in range(5)]
        customer_roles = await customer_role_manager.add_bulk(customer_roles_data)
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
            assert fetched_customer_role.customer_role_id == updated_customer_role.customer_role_id
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
        It creates two customer_role instances, updates their codes
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
        customer_role1 = await CustomerRoleFactory.create_async(session=session)
        customer_role2 = await CustomerRoleFactory.create_async(session=session)
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
        updated_customer_roles = await customer_role_manager.update_bulk(updates)
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
            select(CustomerRole).filter(CustomerRole._customer_role_id == 1)  # type: ignore
        )
        fetched_customer_role = result.scalars().first()
        assert isinstance(fetched_customer_role, CustomerRole)
        assert fetched_customer_role.code == code_updated1
        result = await session.execute(
            select(CustomerRole).filter(CustomerRole._customer_role_id == 2)  # type: ignore
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
        1. Defines a list of customer_role updates, where each update
            contains a customer_role_id and a code.
        2. Calls the update_bulk method of the
            customer_role_manager with the list of updates.
        3. Expects an exception to be raised, indicating that
            the customer_role was not found.
        4. Rolls back the session to undo any changes made during the test.
        Note: This test assumes that the update_bulk method
        throws an exception when a customer_role is not found.
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
        1. Create two customer_role objects using the CustomerRoleFactory.
        2. Delete the customer_roles using the delete_bulk method
            of the customer_role_manager.
        3. Verify that the delete operation was successful by
            checking if the customer_roles no longer exist in the database.
        Expected Result:
        - The delete_bulk method should return True, indicating
            that the delete operation was successful.
        - The customer_roles should no longer exist in the database.
        """
        customer_role1 = await CustomerRoleFactory.create_async(session=session)
        customer_role2 = await CustomerRoleFactory.create_async(session=session)
        # Delete customer_roles
        customer_role_ids = [customer_role1.customer_role_id, customer_role2.customer_role_id]
        result = await customer_role_manager.delete_bulk(customer_role_ids)
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
        1. Create a customer_role using the CustomerRoleFactory.
        2. Assert that the created customer_role is an instance of the
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
        customer_role1 = await CustomerRoleFactory.create_async(session=session)
        assert isinstance(customer_role1, CustomerRole)
        # Delete customer_roles
        customer_role_ids = [1, 2]
        with pytest.raises(Exception):
            await customer_role_manager.delete_bulk(customer_role_ids)
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
            customer_role_manager (CustomerRoleManager): The instance of the
                CustomerRoleManager class.
        Returns:
            None
        Raises:
            AssertionError: If the result is not True.
        """
        # Delete customer_roles with an empty list
        customer_role_ids = []
        result = await customer_role_manager.delete_bulk(customer_role_ids)
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
            customer_role_manager (CustomerRoleManager): The instance of the
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
            await customer_role_manager.delete_bulk(customer_role_ids)
        await session.rollback()
    @pytest.mark.asyncio
    async def test_count_basic_functionality(
        self,
        customer_role_manager: CustomerRoleManager,
        session: AsyncSession
    ):
        """
        Test the basic functionality of the count method
        in the CustomerRoleManager class.
        This test case creates 5 customer_role objects using the
        CustomerRoleFactory and checks if the count method
        returns the correct count of customer_roles.
        Steps:
        1. Create 5 customer_role objects using the CustomerRoleFactory.
        2. Call the count method of the customer_role_manager.
        3. Assert that the count is equal to 5.
        """
        customer_roles_data = (
            [await CustomerRoleFactory.create_async(session) for _ in range(5)])
        assert isinstance(customer_roles_data, List)
        count = await customer_role_manager.count()
        assert count == 5
    @pytest.mark.asyncio
    async def test_count_empty_database(
        self,
        customer_role_manager: CustomerRoleManager
    ):
        """
        Test the count method when the database is empty.
        This test case checks if the count method of the
        CustomerRoleManager class returns 0 when the database is empty.
        Args:
            customer_role_manager (CustomerRoleManager): An instance of the
                CustomerRoleManager class.
        Returns:
            None
        """
        count = await customer_role_manager.count()
        assert count == 0
    @pytest.mark.asyncio
    async def test_get_sorted_list_basic_sorting(
        self,
        customer_role_manager: CustomerRoleManager,
        session: AsyncSession
    ):
        """
        Test case for the 'get_sorted_list' method with basic sorting.
        This test case verifies that the 'get_sorted_list'
        method returns a list of customer_roles
        sorted by the '_customer_role_id' attribute in ascending order.
        Steps:
        1. Add customer_roles to the database.
        2. Call the 'get_sorted_list' method with the
            sort_by parameter set to '_customer_role_id'.
        3. Verify that the returned list of customer_roles is
            sorted by the '_customer_role_id' attribute.
        """
        # Add customer_roles
        customer_roles_data = (
            [await CustomerRoleFactory.create_async(session) for _ in range(5)])
        assert isinstance(customer_roles_data, List)
        sorted_customer_roles = await customer_role_manager.get_sorted_list(
            sort_by="_customer_role_id")
        assert [customer_role.customer_role_id for customer_role in sorted_customer_roles] == (
            [(i + 1) for i in range(5)])
    @pytest.mark.asyncio
    async def test_get_sorted_list_descending_sorting(
        self,
        customer_role_manager: CustomerRoleManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of the
        'get_sorted_list' method
        when sorting the list of customer_roles in descending order.
        Steps:
        1. Create a list of customer_roles using the CustomerRoleFactory.
        2. Assert that the customer_roles_data is of type List.
        3. Call the 'get_sorted_list' method with
            sort_by="customer_role_id" and order="desc".
        4. Assert that the customer_role_ids of the
            sorted_customer_roles are in descending order.
        """
        # Add customer_roles
        customer_roles_data = (
            [await CustomerRoleFactory.create_async(session) for _ in range(5)])
        assert isinstance(customer_roles_data, List)
        sorted_customer_roles = await customer_role_manager.get_sorted_list(
            sort_by="customer_role_id", order="desc")
        assert [customer_role.customer_role_id for customer_role in sorted_customer_roles] == (
            [(i + 1) for i in reversed(range(5))])
    @pytest.mark.asyncio
    async def test_get_sorted_list_invalid_attribute(
        self,
        customer_role_manager: CustomerRoleManager,
        session: AsyncSession
    ):
        """
        Test case to check if an AttributeError is raised when
        sorting the list by an invalid attribute.
        Args:
            customer_role_manager (CustomerRoleManager): The instance of the
                CustomerRoleManager class.
            session (AsyncSession): The instance of the AsyncSession class.
        Raises:
            AttributeError: If an invalid attribute is used for sorting.
        Returns:
            None
        """
        with pytest.raises(AttributeError):
            await customer_role_manager.get_sorted_list(sort_by="invalid_attribute")
        await session.rollback()
    @pytest.mark.asyncio
    async def test_get_sorted_list_empty_database(
        self,
        customer_role_manager: CustomerRoleManager
    ):
        """
        Test case to verify the behavior of
        `get_sorted_list` method when the database is empty.
        This test ensures that when the database is empty, the
        `get_sorted_list` method returns an empty list.
        Args:
            customer_role_manager (CustomerRoleManager): An instance of the
                CustomerRoleManager class.
        Returns:
            None
        """
        sorted_customer_roles = await customer_role_manager.get_sorted_list(sort_by="customer_role_id")
        assert len(sorted_customer_roles) == 0
    @pytest.mark.asyncio
    async def test_refresh_basic(
        self,
        customer_role_manager: CustomerRoleManager,
        session: AsyncSession
    ):
        """
        Test the basic functionality of refreshing a customer_role instance.
        This test performs the following steps:
        1. Creates a customer_role instance using the CustomerRoleFactory.
        2. Retrieves the customer_role from the database to ensure
            it was added correctly.
        3. Updates the customer_role's code and verifies the update.
        4. Refreshes the original customer_role instance and checks if
            it reflects the updated code.
        Args:
            customer_role_manager (CustomerRoleManager): The manager responsible
                for customer_role operations.
            session (AsyncSession): The SQLAlchemy asynchronous session.
        """
        # Add a customer_role
        customer_role1 = await CustomerRoleFactory.create_async(session=session)
        # Retrieve the customer_role from the database
        result = await session.execute(
            select(CustomerRole).filter(
                CustomerRole._customer_role_id == customer_role1.customer_role_id)  # type: ignore
        )  # type: ignore
        customer_role2 = result.scalars().first()
        # Verify that the retrieved customer_role matches the added customer_role
        assert customer_role1.code == customer_role2.code
        # Update the customer_role's code
        updated_code1 = uuid.uuid4()
        customer_role1.code = updated_code1
        updated_customer_role1 = await customer_role_manager.update(customer_role1)
        # Verify that the updated customer_role is of type CustomerRole
        # and has the updated code
        assert isinstance(updated_customer_role1, CustomerRole)
        assert updated_customer_role1.code == updated_code1
        # Refresh the original customer_role instance
        refreshed_customer_role2 = await customer_role_manager.refresh(customer_role2)
        # Verify that the refreshed customer_role reflects the updated code
        assert refreshed_customer_role2.code == updated_code1
    @pytest.mark.asyncio
    async def test_refresh_nonexistent_customer_role(
        self,
        customer_role_manager: CustomerRoleManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of refreshing a nonexistent customer_role.
        Args:
            customer_role_manager (CustomerRoleManager): The instance of the
                CustomerRoleManager class.
            session (AsyncSession): The instance of the AsyncSession class.
        Raises:
            Exception: If the customer_role refresh operation raises an exception.
        Returns:
            None
        """
        customer_role = CustomerRole(customer_role_id=999)
        with pytest.raises(Exception):
            await customer_role_manager.refresh(customer_role)
        await session.rollback()
    @pytest.mark.asyncio
    async def test_exists_with_existing_customer_role(
        self,
        customer_role_manager: CustomerRoleManager,
        session: AsyncSession
    ):
        """
        Test case to check if a customer_role exists using the manager function.
        Args:
            customer_role_manager (CustomerRoleManager): The customer_role manager instance.
            session (AsyncSession): The async session object.
        Returns:
            None
        """
        # Add a customer_role
        customer_role1 = await CustomerRoleFactory.create_async(session=session)
        # Check if the customer_role exists using the manager function
        assert await customer_role_manager.exists(customer_role1.customer_role_id) is True
    @pytest.mark.asyncio
    async def test_is_equal_with_existing_customer_role(
        self,
        customer_role_manager: CustomerRoleManager,
        session: AsyncSession
    ):
        """
        Test if the is_equal method of the
        CustomerRoleManager class correctly compares two customer_roles.
        Args:
            customer_role_manager (CustomerRoleManager): An instance of the
                CustomerRoleManager class.
            session (AsyncSession): An instance of the AsyncSession class.
        Returns:
            None
        """
        # Add a customer_role
        customer_role1 = await CustomerRoleFactory.create_async(session=session)
        customer_role2 = await customer_role_manager.get_by_id(customer_role_id=customer_role1.customer_role_id)
        assert customer_role_manager.is_equal(customer_role1, customer_role2) is True
        customer_role1_dict = customer_role_manager.to_dict(customer_role1)
        customer_role3 = customer_role_manager.from_dict(customer_role1_dict)
        assert customer_role_manager.is_equal(customer_role1, customer_role3) is True
    @pytest.mark.asyncio
    async def test_exists_with_nonexistent_customer_role(
        self,
        customer_role_manager: CustomerRoleManager
    ):
        """
        Test case to check if a customer_role with a
        non-existent ID exists in the database.
        Args:
            customer_role_manager (CustomerRoleManager): The
                instance of the CustomerRoleManager class.
        Returns:
            bool: True if the customer_role exists, False otherwise.
        """
        non_existent_id = 999
        assert await customer_role_manager.exists(non_existent_id) is False
    @pytest.mark.asyncio
    async def test_exists_with_invalid_id_type(
        self,
        customer_role_manager: CustomerRoleManager,
        session: AsyncSession
    ):
        """
        Test case to check if the exists method raises
        an exception when an invalid ID type is provided.
        Args:
            customer_role_manager (CustomerRoleManager): The instance
                of the CustomerRoleManager class.
            session (AsyncSession): The instance of the AsyncSession class.
        Raises:
            Exception: If an exception is not raised by the exists method.
        Returns:
            None
        """
        invalid_id = "invalid_id"
        with pytest.raises(Exception):
            await customer_role_manager.exists(invalid_id)  # type: ignore  # noqa: E501
        await session.rollback()
# endset
    # CustomerID
    @pytest.mark.asyncio
    async def test_get_by_customer_id_existing(
        self,
        customer_role_manager: CustomerRoleManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of the
        `get_by_customer_id` method when a customer_role with
        a specific customer_id exists.
        Steps:
        1. Create a customer_role using the CustomerRoleFactory.
        2. Fetch the customer_role using the
            `get_by_customer_id` method of the customer_role_manager.
        3. Assert that the fetched customer_roles list contains
            only one customer_role.
        4. Assert that the fetched customer_role is an instance
            of the CustomerRole class.
        5. Assert that the code of the fetched customer_role
            matches the code of the created customer_role.
        6. Fetch the corresponding customer object
            using the customer_id of the created customer_role.
        7. Assert that the fetched customer object is
            an instance of the Customer class.
        8. Assert that the customer_code_peek of the fetched
            customer_role matches the code of the fetched customer.
        """
        # Add a customer_role with a specific customer_id
        customer_role1 = await CustomerRoleFactory.create_async(session=session)
        # Fetch the customer_role using the manager function
        fetched_customer_roles = await customer_role_manager.get_by_customer_id(customer_role1.customer_id)
        assert len(fetched_customer_roles) == 1
        assert isinstance(fetched_customer_roles[0], CustomerRole)
        assert fetched_customer_roles[0].code == customer_role1.code
        stmt = select(models.Customer).where(
            models.Customer._customer_id == customer_role1.customer_id)  # type: ignore  # noqa: E501
        result = await session.execute(stmt)
        customer = result.scalars().first()
        assert isinstance(customer, models.Customer)
        assert fetched_customer_roles[0].customer_code_peek == customer.code
    @pytest.mark.asyncio
    async def test_get_by_customer_id_nonexistent(
        self,
        customer_role_manager: CustomerRoleManager
    ):
        """
        Test case to verify the behavior of the
        get_by_customer_id method when the customer ID does not exist.
        This test case ensures that when a non-existent
        customer ID is provided to the get_by_customer_id method,
        an empty list is returned.
        """
        non_existent_id = 999
        fetched_customer_roles = await customer_role_manager.get_by_customer_id(non_existent_id)
        assert len(fetched_customer_roles) == 0
    @pytest.mark.asyncio
    async def test_get_by_customer_id_invalid_type(
        self,
        customer_role_manager: CustomerRoleManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of the
        `get_by_customer_id` method when an invalid customer ID is provided.
        Args:
            customer_role_manager (CustomerRoleManager): An
                instance of the CustomerRoleManager class.
            session (AsyncSession): An instance
                of the AsyncSession class.
        Raises:
            Exception: If an exception is raised during
            the execution of the `get_by_customer_id` method.
        Returns:
            None
        """
        invalid_id = "invalid_id"
        with pytest.raises(Exception):
            await customer_role_manager.get_by_customer_id(invalid_id)  # type: ignore
        await session.rollback()
    # isPlaceholder,
    # placeholder,
    # RoleID
    @pytest.mark.asyncio
    async def test_get_by_role_id_existing(
        self,
        customer_role_manager: CustomerRoleManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of the
        `get_by_role_id` method
        when a customer_role with a specific role_id exists.
        Steps:
        1. Create a customer_role using the CustomerRoleFactory.
        2. Fetch the customer_role using the
            `get_by_role_id` method of the customer_role_manager.
        3. Assert that the fetched customer_roles list has a length of 1.
        4. Assert that the first element in the fetched
            customer_roles list is an instance of the CustomerRole class.
        5. Assert that the code of the fetched customer_role
            matches the code of the created customer_role.
        6. Execute a select statement to fetch the
            Role object associated with the role_id.
        7. Assert that the fetched role is an instance of the Role class.
        8. Assert that the role_code_peek
            of the fetched customer_role matches the code of the fetched role.
        """
        # Add a customer_role with a specific role_id
        customer_role1 = await CustomerRoleFactory.create_async(session=session)
        # Fetch the customer_role using the manager function
        fetched_customer_roles = await customer_role_manager.get_by_role_id(
            customer_role1.role_id)
        assert len(fetched_customer_roles) == 1
        assert isinstance(fetched_customer_roles[0], CustomerRole)
        assert fetched_customer_roles[0].code == customer_role1.code
        stmt = select(models.Role).where(
            models.Role._role_id == customer_role1.role_id)  # type: ignore  # noqa: E501
        result = await session.execute(stmt)
        role = result.scalars().first()
        assert isinstance(role, models.Role)
        assert fetched_customer_roles[0].role_code_peek == role.code
    @pytest.mark.asyncio
    async def test_get_by_role_id_nonexistent(
        self,
        customer_role_manager: CustomerRoleManager
    ):
        """
        Test case to verify the behavior of the
        'get_by_role_id' method
        when the provided foreign key ID does
        not exist in the database.
        This test ensures that when a non-existent
        foreign key ID is passed to the
        'get_by_role_id' method, it
        returns an empty list.
        Steps:
        1. Set a non-existent foreign key ID.
        2. Call the 'get_by_role_id'
            method with the non-existent ID.
        3. Assert that the returned list of fetched customer_roles is empty.
        """
        non_existent_id = 999
        fetched_customer_roles = (
            await customer_role_manager.get_by_role_id(non_existent_id))
        assert len(fetched_customer_roles) == 0
    @pytest.mark.asyncio
    async def test_get_by_role_id_invalid_type(
        self,
        customer_role_manager: CustomerRoleManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of the
        `get_by_role_id` method
        when an invalid foreign key ID type is provided.
        It ensures that an exception is raised
        when an invalid ID is passed to the method.
        Args:
            customer_role_manager (CustomerRoleManager): The
                instance of the CustomerRoleManager class.
            session (AsyncSession): The instance of the AsyncSession class.
        Raises:
            Exception: If an exception is not
                raised when an invalid ID is passed.
        """
        invalid_id = "invalid_id"
        with pytest.raises(Exception):
            await customer_role_manager.get_by_role_id(invalid_id)  # type: ignore  # noqa: E501
        await session.rollback()
# endset
