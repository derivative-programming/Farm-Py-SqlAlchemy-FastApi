# models/managers/tests/customer_role_test.py
# pylint: disable=protected-access
# pylint: disable=unused-argument
# pylint: disable=unused-import
"""
    This class contains unit tests for the
    `CustomerRoleManager` class.
"""

from typing import List
import uuid  # noqa: F401

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

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
        customer_role = await \
            customer_role_manager.build(
                **mock_data)

        # Assert that the returned object is an instance of CustomerRole
        assert isinstance(
            customer_role,
            CustomerRole)

        # Assert that the attributes of the
        # customer_role match our mock data
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
        test_customer_role = await \
            CustomerRoleFactory.build_async(
                session)

        assert test_customer_role.customer_role_id == 0

        # Add the customer_role using the
        # manager's add method
        added_customer_role = await \
            customer_role_manager.add(
                customer_role=test_customer_role)

        assert isinstance(added_customer_role,
                          CustomerRole)

        assert str(added_customer_role.insert_user_id) == (
            str(customer_role_manager._session_context.customer_code))
        assert str(added_customer_role.last_update_user_id) == (
            str(customer_role_manager._session_context.customer_code))

        assert added_customer_role.customer_role_id > 0

        # Fetch the customer_role from
        # the database directly
        result = await session.execute(
            select(CustomerRole).filter(
                CustomerRole._customer_role_id == added_customer_role.customer_role_id  # type: ignore
            )
        )
        fetched_customer_role = result.scalars().first()

        # Assert that the fetched customer_role
        # is not None and matches the
        # added customer_role
        assert fetched_customer_role is not None
        assert isinstance(fetched_customer_role,
                          CustomerRole)
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
        # Create a test customer_role
        # using the CustomerRoleFactory
        # without persisting it to the database
        test_customer_role = await \
            CustomerRoleFactory.build_async(
                session)

        assert test_customer_role.customer_role_id == 0

        test_customer_role.code = uuid.uuid4()

        # Add the customer_role using
        # the manager's add method
        added_customer_role = await \
            customer_role_manager.add(
                customer_role=test_customer_role)

        assert isinstance(added_customer_role,
                          CustomerRole)

        assert str(added_customer_role.insert_user_id) == (
            str(customer_role_manager._session_context.customer_code))
        assert str(added_customer_role.last_update_user_id) == (
            str(customer_role_manager._session_context.customer_code))

        assert added_customer_role.customer_role_id > 0

        # Assert that the returned
        # customer_role matches the
        # test customer_role
        assert added_customer_role.customer_role_id == \
            test_customer_role.customer_role_id
        assert added_customer_role.code == \
            test_customer_role.code

    @pytest.mark.asyncio
    async def test_update(
        self,
        customer_role_manager: CustomerRoleManager,
        session: AsyncSession
    ):
        """
        Test case for the `update` method
        of `CustomerRoleManager`
        that checks if a customer_role
        is correctly updated.
        """
        test_customer_role = await \
            CustomerRoleFactory.create_async(
                session)

        test_customer_role.code = uuid.uuid4()

        updated_customer_role = await \
            customer_role_manager.update(
                customer_role=test_customer_role)

        assert isinstance(updated_customer_role,
                          CustomerRole)

        assert str(updated_customer_role.last_update_user_id) == str(
            customer_role_manager._session_context.customer_code)

        assert updated_customer_role.customer_role_id == \
            test_customer_role.customer_role_id
        assert updated_customer_role.code == \
            test_customer_role.code

        result = await session.execute(
            select(CustomerRole).filter(
                CustomerRole._customer_role_id == test_customer_role.customer_role_id)  # type: ignore
        )

        fetched_customer_role = result.scalars().first()

        assert updated_customer_role.customer_role_id == \
            fetched_customer_role.customer_role_id
        assert updated_customer_role.code == \
            fetched_customer_role.code

        assert test_customer_role.customer_role_id == \
            fetched_customer_role.customer_role_id
        assert test_customer_role.code == \
            fetched_customer_role.code

    @pytest.mark.asyncio
    async def test_update_via_dict(
        self,
        customer_role_manager: CustomerRoleManager,
        session: AsyncSession
    ):
        """
        Test case for the `update` method
        of `CustomerRoleManager`
        that checks if a customer_role is
        correctly updated using a dictionary.
        """
        test_customer_role = await \
            CustomerRoleFactory.create_async(
                session)

        new_code = uuid.uuid4()

        updated_customer_role = await \
            customer_role_manager.update(
                customer_role=test_customer_role,
                code=new_code
            )

        assert isinstance(updated_customer_role,
                          CustomerRole)

        assert str(updated_customer_role.last_update_user_id) == str(
            customer_role_manager._session_context.customer_code
        )

        assert updated_customer_role.customer_role_id == \
            test_customer_role.customer_role_id
        assert updated_customer_role.code == new_code

        result = await session.execute(
            select(CustomerRole).filter(
                CustomerRole._customer_role_id == test_customer_role.customer_role_id)  # type: ignore
        )

        fetched_customer_role = result.scalars().first()

        assert updated_customer_role.customer_role_id == \
            fetched_customer_role.customer_role_id
        assert updated_customer_role.code == \
            fetched_customer_role.code

        assert test_customer_role.customer_role_id == \
            fetched_customer_role.customer_role_id
        assert new_code == \
            fetched_customer_role.code

    @pytest.mark.asyncio
    async def test_update_invalid_customer_role(
        self,
        customer_role_manager: CustomerRoleManager
    ):
        """
        Test case for the `update` method of
        `CustomerRoleManager`
        with an invalid customer_role.
        """

        # None customer_role
        customer_role = None

        new_code = uuid.uuid4()

        updated_customer_role = await (
            customer_role_manager.update(
                customer_role, code=new_code))  # type: ignore

        # Assertions
        assert updated_customer_role is None

    @pytest.mark.asyncio
    async def test_update_with_nonexistent_attribute(
        self,
        customer_role_manager: CustomerRoleManager,
        session: AsyncSession
    ):
        """
        Test case for the `update` method of
        `CustomerRoleManager`
        with a nonexistent attribute.
        """
        test_customer_role = await \
            CustomerRoleFactory.create_async(
                session)

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
        Test case for the `delete` method of
        `CustomerRoleManager`.
        """
        customer_role_data = await CustomerRoleFactory.create_async(
            session)

        result = await session.execute(
            select(CustomerRole).filter(
                CustomerRole._customer_role_id == customer_role_data.customer_role_id)  # type: ignore
        )
        fetched_customer_role = result.scalars().first()

        assert isinstance(fetched_customer_role,
                          CustomerRole)

        assert fetched_customer_role.customer_role_id == \
            customer_role_data.customer_role_id

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

        :param customer_role_manager: The instance of the
            CustomerRoleManager class.
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
            customer_role_manager
            (CustomerRoleManager): An
                instance of the
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
        assert all(isinstance(
            customer_role, CustomerRole) for customer_role in customer_roles)

    @pytest.mark.asyncio
    async def test_to_json(
        self,
        customer_role_manager: CustomerRoleManager,
        session: AsyncSession
    ):
        """
        Test the 'to_json' method of the CustomerRoleManager class.

        Args:
            customer_role_manager
            (CustomerRoleManager): An
                instance of the
                CustomerRoleManager class.
            session (AsyncSession): An instance of the AsyncSession class.

        Returns:
            None

        Raises:
            AssertionError: If the json_data is None.
        """
        customer_role = await \
            CustomerRoleFactory.build_async(
                session)

        json_data = customer_role_manager.to_json(
            customer_role)

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
            customer_role_manager
            (CustomerRoleManager): An
                instance of the
                CustomerRoleManager class.
            session (AsyncSession): An instance of the AsyncSession class.

        Returns:
            None
        """
        customer_role = await \
            CustomerRoleFactory.build_async(
                session)

        dict_data = \
            customer_role_manager.to_dict(
                customer_role)

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
        It creates a customer_role using
        the `CustomerRoleFactory`
        and converts it to JSON using the `to_json` method.
        Then, it deserializes the JSON data using the
        `from_json` method and asserts that the deserialized
        customer_role is an instance of the
        `CustomerRole` class and has
        the same code as the original customer_role.

        Args:
            customer_role_manager
            (CustomerRoleManager): An
                instance of the
                `CustomerRoleManager` class.
            session (AsyncSession): An instance of the `AsyncSession` class.

        Returns:
            None
        """
        customer_role = await \
            CustomerRoleFactory.create_async(
                session)

        json_data = customer_role_manager.to_json(
            customer_role)

        deserialized_customer_role = await \
                customer_role_manager.from_json(json_data)

        assert isinstance(deserialized_customer_role,
                          CustomerRole)
        assert deserialized_customer_role.code == \
            customer_role.code

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
        a dictionary representation of a
        customer_role object.

        Args:
            customer_role_manager
            (CustomerRoleManager): An instance
                of the `CustomerRoleManager` class.
            session (AsyncSession): An instance of the `AsyncSession` class.

        Returns:
            None

        Raises:
            AssertionError: If any of the assertions fail.
        """
        customer_role = await \
            CustomerRoleFactory.create_async(
                session)

        schema = CustomerRoleSchema()

        customer_role_data = schema.dump(customer_role)

        assert isinstance(customer_role_data, dict)

        deserialized_customer_role = await \
            customer_role_manager.from_dict(
                customer_role_data)

        assert isinstance(deserialized_customer_role,
                          CustomerRole)

        assert deserialized_customer_role.code == \
            customer_role.code

    @pytest.mark.asyncio
    async def test_count_basic_functionality(
        self,
        customer_role_manager: CustomerRoleManager,
        session: AsyncSession
    ):
        """
        Test the basic functionality of the count method
        in the CustomerRoleManager class.

        This test case creates 5 customer_role
        objects using the
        CustomerRoleFactory and checks if the count method
        returns the correct count of
        customer_roles.

        Steps:
        1. Create 5 customer_role objects using
            the CustomerRoleFactory.
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
            customer_role_manager
            (CustomerRoleManager): An
                instance of the
                CustomerRoleManager class.

        Returns:
            None
        """

        count = await customer_role_manager.count()

        assert count == 0

    @pytest.mark.asyncio
    async def test_refresh_basic(
        self,
        customer_role_manager: CustomerRoleManager,
        session: AsyncSession
    ):
        """
        Test the basic functionality of refreshing
        a customer_role instance.

        This test performs the following steps:
        1. Creates a customer_role instance using
            the CustomerRoleFactory.
        2. Retrieves the customer_role from th
            database to ensure
            it was added correctly.
        3. Updates the customer_role's code and verifies the update.
        4. Refreshes the original customer_role instance
            and checks if
            it reflects the updated code.

        Args:
            customer_role_manager
            (CustomerRoleManager): The
                manager responsible
                for customer_role operations.
            session (AsyncSession): The SQLAlchemy asynchronous session.
        """
        # Add a customer_role
        customer_role1 = await CustomerRoleFactory.create_async(
            session=session)

        # Retrieve the customer_role from the database
        result = await session.execute(
            select(CustomerRole).filter(
                CustomerRole._customer_role_id == customer_role1.customer_role_id)  # type: ignore
        )  # type: ignore
        customer_role2 = result.scalars().first()

        # Verify that the retrieved customer_role
        # matches the added customer_role
        assert customer_role1.code == \
            customer_role2.code

        # Update the customer_role's code
        updated_code1 = uuid.uuid4()
        customer_role1.code = updated_code1
        updated_customer_role1 = await customer_role_manager.update(
            customer_role1)

        # Verify that the updated customer_role
        # is of type CustomerRole
        # and has the updated code
        assert isinstance(updated_customer_role1,
                          CustomerRole)

        assert updated_customer_role1.code == updated_code1

        # Refresh the original customer_role instance
        refreshed_customer_role2 = await customer_role_manager.refresh(
            customer_role2)

        # Verify that the refreshed customer_role
        # reflects the updated code
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
            customer_role_manager
            (CustomerRoleManager): The
                instance of the
                CustomerRoleManager class.
            session (AsyncSession): The instance of the AsyncSession class.

        Raises:
            Exception: If the customer_role
            refresh operation raises an exception.

        Returns:
            None
        """
        customer_role = CustomerRole(
            customer_role_id=999)

        with pytest.raises(Exception):
            await customer_role_manager.refresh(
                customer_role)

        await session.rollback()

    @pytest.mark.asyncio
    async def test_exists_with_existing_customer_role(
        self,
        customer_role_manager: CustomerRoleManager,
        session: AsyncSession
    ):
        """
        Test case to check if a customer_role
        exists using the manager function.

        Args:
            customer_role_manager
            (CustomerRoleManager): The
                customer_role manager instance.
            session (AsyncSession): The async session object.

        Returns:
            None
        """
        # Add a customer_role
        customer_role1 = await CustomerRoleFactory.create_async(
            session=session)

        # Check if the customer_role exists
        # using the manager function
        assert await customer_role_manager.exists(
            customer_role1.customer_role_id) is True

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
            customer_role_manager
            (CustomerRoleManager): An
                instance of the
                CustomerRoleManager class.
            session (AsyncSession): An instance of the AsyncSession class.

        Returns:
            None
        """
        # Add a customer_role
        customer_role1 = await \
            CustomerRoleFactory.create_async(
                session=session)

        customer_role2 = await \
            customer_role_manager.get_by_id(
                customer_role_id=customer_role1.customer_role_id)

        assert customer_role_manager.is_equal(
            customer_role1, customer_role2) is True

        customer_role1_dict = \
            customer_role_manager.to_dict(
                customer_role1)

        customer_role3 = await \
            customer_role_manager.from_dict(
                customer_role1_dict)

        assert customer_role_manager.is_equal(
            customer_role1, customer_role3) is True

    @pytest.mark.asyncio
    async def test_exists_with_nonexistent_customer_role(
        self,
        customer_role_manager: CustomerRoleManager
    ):
        """
        Test case to check if a customer_role with a
        non-existent ID exists in the database.

        Args:
            customer_role_manager
            (CustomerRoleManager): The
                instance of the CustomerRoleManager class.

        Returns:
            bool: True if the customer_role exists,
                False otherwise.
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
            customer_role_manager
            (CustomerRoleManager): The instance
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

