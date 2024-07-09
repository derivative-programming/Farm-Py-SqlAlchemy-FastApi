# managers/tests/customer_test.py  # pylint: disable=duplicate-code # noqa: E501
# pylint: disable=protected-access, too-many-public-methods
# pylint: disable=unused-argument
# pylint: disable=unused-import
"""
    This class contains unit tests for the
    `CustomerManager` class.
"""

import uuid  # noqa: F401
from typing import List

import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

import pytest
from helpers.session_context import SessionContext
from managers.customer import CustomerManager
from models import Customer
from models.factory import CustomerFactory
from models.serialization_schema.customer import CustomerSchema


class TestCustomerManager:
    """
    This class contains unit tests for the
    `CustomerManager` class.
    """

    @pytest_asyncio.fixture(scope="function")
    async def obj_manager(self, session: AsyncSession):
        """
        Fixture that returns an instance of
        `CustomerManager` for testing.
        """
        session_context = SessionContext({}, session)
        session_context.customer_code = uuid.uuid4()
        return CustomerManager(session_context)

    @pytest.mark.asyncio
    async def test_build(
        self,
        obj_manager: CustomerManager
    ):
        """
        Test case for the `build` method of
        `CustomerManager`.
        """
        # Define mock data for our customer
        mock_data = {
            "code": uuid.uuid4()
        }

        # Call the build function of the manager
        customer = await \
            obj_manager.build(
                **mock_data)

        # Assert that the returned object is an
        # instance of Customer
        assert isinstance(
            customer,
            Customer)

        # Assert that the attributes of the
        # customer match our mock data
        assert customer.code == mock_data["code"]

    @pytest.mark.asyncio
    async def test_build_with_missing_data(
        self,
        obj_manager: CustomerManager,
        session: AsyncSession
    ):
        """
        Test case for the `build` method of
        `CustomerManager` with missing data.
        """
        # Define mock data with a missing key
        mock_data = {
            "non_existant_property": "Rose"
        }

        # If the build method is expected to raise an exception for
        # missing data, test for that
        with pytest.raises(Exception):
            await obj_manager.build(**mock_data)

        await session.rollback()

    @pytest.mark.asyncio
    async def test_add_correctly_adds_customer_to_database(
        self,
        obj_manager: CustomerManager,
        session: AsyncSession
    ):
        """
        Test case for the `add` method of
        `CustomerManager` that checks if a
        customer is correctly added to the database.
        """
        new_obj = await \
            CustomerFactory.build_async(
                session)

        assert new_obj.customer_id == 0

        # Add the customer using the
        # manager's add method
        added_obj = await \
            obj_manager.add(
                customer=new_obj)

        assert isinstance(added_obj,
                          Customer)

        assert str(added_obj.insert_user_id) == (
            str(obj_manager._session_context.customer_code))
        assert str(added_obj.last_update_user_id) == (
            str(obj_manager._session_context.customer_code))

        assert added_obj.customer_id > 0

        # Fetch the customer from
        # the database directly
        result = await session.execute(
            select(Customer).filter(
                Customer._customer_id == (
                    added_obj.customer_id)  # type: ignore
            )
        )
        fetched_obj = result.scalars().first()

        # Assert that the fetched customer
        # is not None and matches the
        # added customer
        assert fetched_obj is not None
        assert isinstance(fetched_obj,
                          Customer)
        assert fetched_obj.customer_id == \
            added_obj.customer_id

    @pytest.mark.asyncio
    async def test_add_returns_correct_customer_object(
        self,
        obj_manager: CustomerManager,
        session: AsyncSession
    ):
        """
        Test case for the `add` method of
        `CustomerManager` that checks if the
        correct customer object is returned.
        """
        # Create a test customer
        # using the CustomerFactory
        # without persisting it to the database
        new_obj = await \
            CustomerFactory.build_async(
                session)

        assert new_obj.customer_id == 0

        new_obj.code = uuid.uuid4()

        # Add the customer using
        # the manager's add method
        added_obj = await \
            obj_manager.add(
                customer=new_obj)

        assert isinstance(added_obj,
                          Customer)

        assert str(added_obj.insert_user_id) == (
            str(obj_manager._session_context.customer_code))
        assert str(added_obj.last_update_user_id) == (
            str(obj_manager._session_context.customer_code))

        assert added_obj.customer_id > 0

        # Assert that the returned
        # customer matches the
        # test customer
        assert added_obj.customer_id == \
            new_obj.customer_id
        assert added_obj.code == \
            new_obj.code

    @pytest.mark.asyncio
    async def test_update(
        self,
        obj_manager: CustomerManager,
        session: AsyncSession
    ):
        """
        Test case for the `update` method
        of `CustomerManager`
        that checks if a customer
        is correctly updated.
        """
        new_obj = await \
            CustomerFactory.create_async(
                session)

        new_obj.code = uuid.uuid4()

        updated_obj = await \
            obj_manager.update(
                customer=new_obj)

        assert isinstance(updated_obj,
                          Customer)

        assert str(updated_obj.last_update_user_id) == str(
            obj_manager._session_context.customer_code)

        assert updated_obj.customer_id == \
            new_obj.customer_id
        assert updated_obj.code == \
            new_obj.code

        result = await session.execute(
            select(Customer).filter(
                Customer._customer_id == (
                    new_obj.customer_id))  # type: ignore
        )

        fetched_obj = result.scalars().first()

        assert updated_obj.customer_id == \
            fetched_obj.customer_id
        assert updated_obj.code == \
            fetched_obj.code

        assert new_obj.customer_id == \
            fetched_obj.customer_id
        assert new_obj.code == \
            fetched_obj.code

    @pytest.mark.asyncio
    async def test_update_via_dict(
        self,
        obj_manager: CustomerManager,
        session: AsyncSession
    ):
        """
        Test case for the `update` method
        of `CustomerManager`
        that checks if a customer is
        correctly updated using a dictionary.
        """
        new_obj = await \
            CustomerFactory.create_async(
                session)

        new_code = uuid.uuid4()

        updated_obj = await \
            obj_manager.update(
                customer=new_obj,
                code=new_code
            )

        assert isinstance(updated_obj,
                          Customer)

        assert str(updated_obj.last_update_user_id) == str(
            obj_manager._session_context.customer_code
        )

        assert updated_obj.customer_id == \
            new_obj.customer_id
        assert updated_obj.code == new_code

        result = await session.execute(
            select(Customer).filter(
                Customer._customer_id == (
                    new_obj.customer_id))  # type: ignore
        )

        fetched_obj = result.scalars().first()

        assert updated_obj.customer_id == \
            fetched_obj.customer_id
        assert updated_obj.code == \
            fetched_obj.code

        assert new_obj.customer_id == \
            fetched_obj.customer_id
        assert new_code == \
            fetched_obj.code

    @pytest.mark.asyncio
    async def test_update_invalid_customer(
        self,
        obj_manager: CustomerManager
    ):
        """
        Test case for the `update` method of
        `CustomerManager`
        with an invalid customer.
        """

        # None customer
        customer = None

        new_code = uuid.uuid4()

        updated_obj = await (
            obj_manager.update(
                customer, code=new_code))  # type: ignore

        # Assertions
        assert updated_obj is None

    @pytest.mark.asyncio
    async def test_update_with_nonexistent_attribute(
        self,
        obj_manager: CustomerManager,
        session: AsyncSession
    ):
        """
        Test case for the `update` method of
        `CustomerManager`
        with a nonexistent attribute.
        """
        new_obj = await \
            CustomerFactory.create_async(
                session)

        new_code = uuid.uuid4()

        with pytest.raises(ValueError):
            await obj_manager.update(
                customer=new_obj,
                xxx=new_code
            )

        await session.rollback()

    @pytest.mark.asyncio
    async def test_delete(
        self,
        obj_manager: CustomerManager,
        session: AsyncSession
    ):
        """
        Test case for the `delete` method of
        `CustomerManager`.
        """
        new_obj = await CustomerFactory.create_async(
            session)

        result = await session.execute(
            select(Customer).filter(
                Customer._customer_id == (
                    new_obj.customer_id))  # type: ignore
        )
        fetched_obj = result.scalars().first()

        assert isinstance(fetched_obj,
                          Customer)

        assert fetched_obj.customer_id == \
            new_obj.customer_id

        await obj_manager.delete(
            customer_id=new_obj.customer_id)

        result = await session.execute(
            select(Customer).filter(
                Customer._customer_id == (
                    new_obj.customer_id))  # type: ignore
        )
        fetched_obj = result.scalars().first()

        assert fetched_obj is None

    @pytest.mark.asyncio
    async def test_delete_nonexistent(
        self,
        obj_manager: CustomerManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of deleting a nonexistent
        customer.

        This test case ensures that when the delete method
        is called with the ID of a nonexistent
        customer,
        an exception is raised. The test also verifies that
        the session is rolled back after the delete operation.

        :param obj_manager: The instance of the
            CustomerManager class.
        :param session: The instance of the AsyncSession class.
        """
        with pytest.raises(Exception):
            await obj_manager.delete(999)

        await session.rollback()

    @pytest.mark.asyncio
    async def test_delete_invalid_type(
        self,
        obj_manager: CustomerManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of deleting a customer
        with an invalid type.

        This test case ensures that when the `delete` method
        of the `obj_manager` is called with an invalid type,
        an exception is raised. The test case expects the
        `delete` method to raise an exception, and if it doesn't,
        the test case will fail.

        Args:
            obj_manager
            (CustomerManager): An
                instance of the
                `CustomerManager` class.
            session (AsyncSession): An instance of the `AsyncSession` class.

        Returns:
            None

        Raises:
            Exception: If the `delete` method does not raise an exception.

        """
        with pytest.raises(Exception):
            await obj_manager.delete("999")  # type: ignore

        await session.rollback()

    @pytest.mark.asyncio
    async def test_get_list(
        self,
        obj_manager: CustomerManager,
        session: AsyncSession
    ):
        """
        Test case for the `get_list` method of the
        `CustomerManager` class.

        This test verifies that the `get_list`
        method returns the correct list of customers.

        Steps:
        1. Call the `get_list` method of the
            `obj_manager` instance.
        2. Assert that the returned list is empty.
        3. Create 5 customer objects using the
            `CustomerFactory.create_async` method.
        4. Assert that the
            `customers_data` variable
            is of type `List`.
        5. Call the `get_list` method of the
            `obj_manager` instance again.
        6. Assert that the returned list contains 5 customers.
        7. Assert that all elements in the returned list are
            instances of the
            `Customer` class.
        """

        customers = await obj_manager.get_list()

        assert len(customers) == 0

        customers_data = (
            [await CustomerFactory.create_async(session)
             for _ in range(5)])

        assert isinstance(customers_data, List)

        customers = await obj_manager.get_list()

        assert len(customers) == 5
        assert all(isinstance(
            customer,
            Customer
        ) for customer in customers)

    @pytest.mark.asyncio
    async def test_to_json(
        self,
        obj_manager: CustomerManager,
        session: AsyncSession
    ):
        """
        Test the 'to_json' method of the CustomerManager class.

        Args:
            obj_manager
            (CustomerManager): An
                instance of the
                CustomerManager class.
            session (AsyncSession): An instance of the AsyncSession class.

        Returns:
            None

        Raises:
            AssertionError: If the json_data is None.
        """
        customer = await \
            CustomerFactory.build_async(
                session)

        json_data = obj_manager.to_json(
            customer)

        assert json_data is not None

    @pytest.mark.asyncio
    async def test_to_dict(
        self,
        obj_manager: CustomerManager,
        session: AsyncSession
    ):
        """
        Test the to_dict method of the CustomerManager class.

        Args:
            obj_manager
            (CustomerManager): An
                instance of the
                CustomerManager class.
            session (AsyncSession): An instance of the AsyncSession class.

        Returns:
            None
        """
        customer = await \
            CustomerFactory.build_async(
                session)

        dict_data = \
            obj_manager.to_dict(
                customer)

        assert dict_data is not None

    @pytest.mark.asyncio
    async def test_from_json(
        self,
        obj_manager: CustomerManager,
        session: AsyncSession
    ):
        """
        Test the `from_json` method of the
        `CustomerManager` class.

        This method tests the functionality of the
        `from_json` method of the
        `CustomerManager` class.
        It creates a customer using
        the `CustomerFactory`
        and converts it to JSON using the `to_json` method.
        Then, it deserializes the JSON data using the
        `from_json` method and asserts that the deserialized
        customer is an instance of the
        `Customer` class and has
        the same code as the original customer.

        Args:
            obj_manager
            (CustomerManager): An
                instance of the
                `CustomerManager` class.
            session (AsyncSession): An instance of the `AsyncSession` class.

        Returns:
            None
        """
        customer = await \
            CustomerFactory.create_async(
                session)

        json_data = obj_manager.to_json(
            customer)

        deserialized_customer = await \
            obj_manager.from_json(json_data)

        assert isinstance(deserialized_customer,
                          Customer)
        assert deserialized_customer.code == \
            customer.code

    @pytest.mark.asyncio
    async def test_from_dict(
        self,
        obj_manager: CustomerManager,
        session: AsyncSession
    ):
        """
        Test the `from_dict` method of the
        `CustomerManager` class.

        This method tests the functionality of the
        `from_dict` method, which is used to deserialize
        a dictionary representation of a
        customer object.

        Args:
            obj_manager
            (CustomerManager): An instance
                of the `CustomerManager` class.
            session (AsyncSession): An instance of the
            `AsyncSession` class.

        Returns:
            None

        Raises:
            AssertionError: If any of the assertions fail.
        """
        customer = await \
            CustomerFactory.create_async(
                session)

        schema = CustomerSchema()

        new_obj = schema.dump(customer)

        assert isinstance(new_obj, dict)

        deserialized_customer = await \
            obj_manager.from_dict(
                new_obj)

        assert isinstance(deserialized_customer,
                          Customer)

        assert deserialized_customer.code == \
            customer.code

    @pytest.mark.asyncio
    async def test_count_basic_functionality(
        self,
        obj_manager: CustomerManager,
        session: AsyncSession
    ):
        """
        Test the basic functionality of the count method
        in the CustomerManager class.

        This test case creates 5 customer
        objects using the
        CustomerFactory and checks if the count method
        returns the correct count of
        customers.

        Steps:
        1. Create 5 customer objects using
            the CustomerFactory.
        2. Call the count method of the obj_manager.
        3. Assert that the count is equal to 5.

        """
        customers_data = (
            [await CustomerFactory.create_async(session)
             for _ in range(5)])

        assert isinstance(customers_data, List)

        count = await obj_manager.count()

        assert count == 5

    @pytest.mark.asyncio
    async def test_count_empty_database(
        self,
        obj_manager: CustomerManager
    ):
        """
        Test the count method when the database is empty.

        This test case checks if the count method of the
        CustomerManager class
        returns 0 when the database is empty.

        Args:
            obj_manager
            (CustomerManager): An
                instance of the
                CustomerManager class.

        Returns:
            None
        """

        count = await obj_manager.count()

        assert count == 0

    @pytest.mark.asyncio
    async def test_refresh_basic(
        self,
        obj_manager: CustomerManager,
        session: AsyncSession
    ):
        """
        Test the basic functionality of refreshing
        a customer instance.

        This test performs the following steps:
        1. Creates a customer instance using
            the CustomerFactory.
        2. Retrieves the customer from th
            database to ensure
            it was added correctly.
        3. Updates the customer's code and verifies the update.
        4. Refreshes the original customer instance
            and checks if
            it reflects the updated code.

        Args:
            obj_manager
            (CustomerManager): The
                manager responsible
                for customer operations.
            session (AsyncSession): The SQLAlchemy asynchronous session.
        """
        # Add a customer
        obj_1 = await CustomerFactory.create_async(
            session=session)

        # Retrieve the customer from the database
        result = await session.execute(
            select(Customer).filter(
                Customer._customer_id == (
                    obj_1.customer_id))  # type: ignore
        )  # type: ignore
        obj_2 = result.scalars().first()

        # Verify that the retrieved customer
        # matches the added customer
        assert obj_1.code == \
            obj_2.code

        # Update the customer's code
        updated_code1 = uuid.uuid4()
        obj_1.code = updated_code1
        updated_obj_1 = await obj_manager.update(
            obj_1)

        # Verify that the updated customer
        # is of type Customer
        # and has the updated code
        assert isinstance(updated_obj_1,
                          Customer)

        assert updated_obj_1.code == updated_code1

        # Refresh the original customer instance
        refreshed_obj_2 = await obj_manager.refresh(
            obj_2)

        # Verify that the refreshed customer
        # reflects the updated code
        assert refreshed_obj_2.code == updated_code1

    @pytest.mark.asyncio
    async def test_refresh_nonexistent_customer(
        self,
        obj_manager: CustomerManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of refreshing a
        nonexistent customer.

        Args:
            obj_manager
            (CustomerManager): The
                instance of the
                CustomerManager class.
            session (AsyncSession): The instance of the AsyncSession class.

        Raises:
            Exception: If the customer
            refresh operation raises an exception.

        Returns:
            None
        """
        customer = Customer(
            customer_id=999)

        with pytest.raises(Exception):
            await obj_manager.refresh(
                customer)

        await session.rollback()

    @pytest.mark.asyncio
    async def test_exists_with_existing_customer(
        self,
        obj_manager: CustomerManager,
        session: AsyncSession
    ):
        """
        Test case to check if a customer
        exists using the manager function.

        Args:
            obj_manager
            (CustomerManager): The
                customer manager instance.
            session (AsyncSession): The async session object.

        Returns:
            None
        """
        # Add a customer
        obj_1 = await CustomerFactory.create_async(
            session=session)

        # Check if the customer exists
        # using the manager function
        assert await obj_manager.exists(
            obj_1.customer_id) is True

    @pytest.mark.asyncio
    async def test_is_equal_with_existing_customer(
        self,
        obj_manager: CustomerManager,
        session: AsyncSession
    ):
        """
        Test if the is_equal method of the
        CustomerManager
        class correctly compares two
        customers.

        Args:
            obj_manager
            (CustomerManager): An
                instance of the
                CustomerManager class.
            session (AsyncSession): An instance of the AsyncSession class.

        Returns:
            None
        """
        # Add a customer
        obj_1 = await \
            CustomerFactory.create_async(
                session=session)

        obj_2 = await \
            obj_manager.get_by_id(
                customer_id=obj_1.customer_id)

        assert obj_manager.is_equal(
            obj_1, obj_2) is True

        obj_1_dict = \
            obj_manager.to_dict(
                obj_1)

        customer3 = await \
            obj_manager.from_dict(
                obj_1_dict)

        assert obj_manager.is_equal(
            obj_1, customer3) is True

    @pytest.mark.asyncio
    async def test_exists_with_nonexistent_customer(
        self,
        obj_manager: CustomerManager
    ):
        """
        Test case to check if a customer with a
        non-existent ID exists in the database.

        Args:
            obj_manager
            (CustomerManager): The
                instance of the CustomerManager class.

        Returns:
            bool: True if the customer exists,
                False otherwise.
        """
        non_existent_id = 999

        assert await obj_manager.exists(non_existent_id) is False

    @pytest.mark.asyncio
    async def test_exists_with_invalid_id_type(
        self,
        obj_manager: CustomerManager,
        session: AsyncSession
    ):
        """
        Test case to check if the exists method raises
        an exception when an invalid ID type is provided.

        Args:
            obj_manager
            (CustomerManager): The instance
                of the CustomerManager class.
            session (AsyncSession): The instance of the AsyncSession class.

        Raises:
            Exception: If an exception is not raised by the exists method.

        Returns:
            None
        """
        invalid_id = "invalid_id"

        with pytest.raises(Exception):
            await obj_manager.exists(invalid_id)  # type: ignore  # noqa: E501

        await session.rollback()
