# models/managers/tests/customer_role_test.py
# pylint: disable=protected-access
# pylint: disable=unused-argument
# pylint: disable=unused-import
"""
    This class contains unit tests for the
    `CustomerRoleManager` class.
"""

import uuid  # noqa: F401

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

import models
from helpers.session_context import SessionContext
from managers.customer_role import (
    CustomerRoleManager)
from models import CustomerRole
from models.factory import (
    CustomerRoleFactory)


class TestCustomerRoleGetByManager:
    """
    This class contains unit tests for the
    `CustomerRoleManager` class.
    """

    @pytest_asyncio.fixture(scope="function")
    async def obj_manager(self, session: AsyncSession):
        """
        Fixture that returns an instance of
        `CustomerRoleManager` for testing.
        """
        session_context = SessionContext({}, session)
        session_context.customer_code = uuid.uuid4()
        return CustomerRoleManager(session_context)

    @pytest.mark.asyncio
    async def test_build(
        self,
        obj_manager: CustomerRoleManager
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
            obj_manager.build(
                **mock_data)

        # Assert that the returned object is an instance of
        # CustomerRole
        assert isinstance(
            customer_role,
            CustomerRole)

        # Assert that the attributes of the
        # customer_role match our mock data
        assert customer_role.code == mock_data["code"]

    @pytest.mark.asyncio
    async def test_get_by_id(
        self,
        obj_manager: CustomerRoleManager,
        session: AsyncSession
    ):
        """
        Test case for the `get_by_id` method of
        `CustomerRoleManager`.
        """
        new_obj = await \
            CustomerRoleFactory.create_async(
                session)

        customer_role = await \
            obj_manager.get_by_id(
                new_obj.customer_role_id)

        assert isinstance(
            customer_role,
            CustomerRole)

        assert new_obj.customer_role_id == \
            customer_role.customer_role_id
        assert new_obj.code == \
            customer_role.code

    @pytest.mark.asyncio
    async def test_get_by_id_not_found(
        self,
        obj_manager: CustomerRoleManager
    ):
        """
        Test case for the `get_by_id` method of
        `CustomerRoleManager` when the
        customer_role is not found.
        """

        non_existent_id = 9999  # An ID that's not in the database

        retrieved_customer_role = await \
            obj_manager.get_by_id(
                non_existent_id)

        assert retrieved_customer_role is None

    @pytest.mark.asyncio
    async def test_get_by_code_returns_customer_role(
        self,
        obj_manager: CustomerRoleManager,
        session: AsyncSession
    ):
        """
        Test case for the `get_by_code` method of
        `CustomerRoleManager` that checks if
        a customer_role is
        returned by its code.
        """

        new_obj = await \
            CustomerRoleFactory.create_async(
                session)

        customer_role = await \
            obj_manager.get_by_code(
                new_obj.code)

        assert isinstance(
            customer_role,
            CustomerRole)

        assert new_obj.customer_role_id == \
            customer_role.customer_role_id
        assert new_obj.code == \
            customer_role.code

    @pytest.mark.asyncio
    async def test_get_by_code_returns_none_for_nonexistent_code(
        self,
        obj_manager: CustomerRoleManager
    ):
        """
        Test case for the `get_by_code` method of
        `CustomerRoleManager` when the code does not exist.
        """
        # Generate a random UUID that doesn't correspond to
        # any CustomerRole in the database
        random_code = uuid.uuid4()

        customer_role = await \
            obj_manager.get_by_code(
                random_code)

        assert customer_role is None

    # CustomerID

    @pytest.mark.asyncio
    async def test_get_by_customer_id_existing(
        self,
        obj_manager: CustomerRoleManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of the
        `get_by_customer_id` method when
        a customer_role with
        a specific customer_id exists.

        Steps:
        1. Create a customer_role using the
            CustomerRoleFactory.
        2. Fetch the customer_role using the
            `get_by_customer_id` method of the obj_manager.
        3. Assert that the fetched customer_roles list contains
            only one customer_role.
        4. Assert that the fetched customer_role
            is an instance
            of the CustomerRole class.
        5. Assert that the code of the fetched customer_role
            matches the code of the created customer_role.
        6. Fetch the corresponding customer object
            using the customer_id of the created customer_role.
        7. Assert that the fetched customer object is
            an instance of the Customer class.
        8. Assert that the customer_code_peek of the fetched
            customer_role matches the
            code of the fetched customer.

        """
        # Add a customer_role with a specific
        # customer_id
        obj_1 = await CustomerRoleFactory.create_async(
            session=session)

        # Fetch the customer_role using
        # the manager function

        fetched_objs = await \
            obj_manager.get_by_customer_id(
                obj_1.customer_id)
        assert len(fetched_objs) == 1
        assert isinstance(fetched_objs[0],
                          CustomerRole)
        assert fetched_objs[0].code == \
            obj_1.code

        stmt = select(models.Customer).where(
            models.Customer._customer_id == obj_1.customer_id)  # type: ignore  # noqa: E501
        result = await session.execute(stmt)
        customer = result.scalars().first()

        assert isinstance(customer, models.Customer)

        assert fetched_objs[0].customer_code_peek == customer.code

    @pytest.mark.asyncio
    async def test_get_by_customer_id_nonexistent(
        self,
        obj_manager: CustomerRoleManager
    ):
        """
        Test case to verify the behavior of the
        get_by_customer_id method when the customer ID does not exist.

        This test case ensures that when a non-existent
        customer ID is provided to the get_by_customer_id method,
        an empty list is returned.
        """

        non_existent_id = 999

        fetched_objs = await \
            obj_manager.get_by_customer_id(
                non_existent_id)
        assert len(fetched_objs) == 0

    @pytest.mark.asyncio
    async def test_get_by_customer_id_invalid_type(
        self,
        obj_manager: CustomerRoleManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of the
        `get_by_customer_id` method when an invalid customer ID is provided.

        Args:
            obj_manager (CustomerRoleManager): An
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
            await obj_manager.get_by_customer_id(
                invalid_id)  # type: ignore

        await session.rollback()
    # isPlaceholder,
    # placeholder,
    # RoleID

    @pytest.mark.asyncio
    async def test_get_by_role_id_existing(
        self,
        obj_manager: CustomerRoleManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of the
        `get_by_role_id` method
        when a customer_role with a
        specific role_id exists.

        Steps:
        1. Create a customer_role using the
            CustomerRoleFactory.
        2. Fetch the customer_role using the
            `get_by_role_id`
            method of the obj_manager.
        3. Assert that the fetched customer_roles list has a length of 1.
        4. Assert that the first element in the fetched
            customer_roles list is an instance of the
            CustomerRole class.
        5. Assert that the code of the fetched
            customer_role
            matches the code of the created customer_role.
        6. Execute a select statement to fetch the
            Role object associated with the
            role_id.
        7. Assert that the fetched role is an
            instance of the Role class.
        8. Assert that the role_code_peek
            of the fetched customer_role matches
            the code of the fetched role.
        """
        # Add a customer_role with a specific
        # role_id
        obj_1 = await CustomerRoleFactory.create_async(
            session=session)

        # Fetch the customer_role using the
        # manager function

        fetched_objs = await \
            obj_manager.get_by_role_id(
                obj_1.role_id)
        assert len(fetched_objs) == 1
        assert isinstance(fetched_objs[0],
                          CustomerRole)
        assert fetched_objs[0].code == \
            obj_1.code

        stmt = select(models.Role).where(
            models.Role._role_id == obj_1.role_id)  # type: ignore  # noqa: E501
        result = await session.execute(stmt)
        role = result.scalars().first()

        assert isinstance(role, models.Role)

        assert fetched_objs[0].role_code_peek == role.code

    @pytest.mark.asyncio
    async def test_get_by_role_id_nonexistent(
        self,
        obj_manager: CustomerRoleManager
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

        fetched_objs = (
            await obj_manager.get_by_role_id(
                non_existent_id))
        assert len(fetched_objs) == 0

    @pytest.mark.asyncio
    async def test_get_by_role_id_invalid_type(
        self,
        obj_manager: CustomerRoleManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of the
        `get_by_role_id` method
        when an invalid foreign key ID type is provided.

        It ensures that an exception is raised
        when an invalid ID is passed to the method.

        Args:
            obj_manager (CustomerRoleManager): The
                instance of the CustomerRoleManager class.
            session (AsyncSession): The instance of the AsyncSession class.

        Raises:
            Exception: If an exception is not
                raised when an invalid ID is passed.

        """
        invalid_id = "invalid_id"

        with pytest.raises(Exception):
            await obj_manager.get_by_role_id(
                invalid_id)  # type: ignore  # noqa: E501

        await session.rollback()
