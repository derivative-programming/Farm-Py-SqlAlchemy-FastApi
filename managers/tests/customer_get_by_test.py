# models/managers/tests/customer_test.py  # pylint: disable=duplicate-code # noqa: E501
# pylint: disable=protected-access, too-many-public-methods
# pylint: disable=unused-argument
# pylint: disable=unused-import
"""
    This class contains unit tests for the
    `CustomerManager` class.
"""

import uuid  # noqa: F401

import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

import models
import pytest
from helpers.session_context import SessionContext
from managers.customer import CustomerManager
from models import Customer
from models.factory import CustomerFactory


class TestCustomerGetByManager:
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

        # Assert that the returned object is an instance of
        # Customer
        assert isinstance(
            customer,
            Customer)

        # Assert that the attributes of the
        # customer match our mock data
        assert customer.code == mock_data["code"]

    @pytest.mark.asyncio
    async def test_get_by_id(
        self,
        obj_manager: CustomerManager,
        session: AsyncSession
    ):
        """
        Test case for the `get_by_id` method of
        `CustomerManager`.
        """
        new_obj = await \
            CustomerFactory.create_async(
                session)

        customer = await \
            obj_manager.get_by_id(
                new_obj.customer_id)

        assert isinstance(
            customer,
            Customer)

        assert new_obj.customer_id == \
            customer.customer_id
        assert new_obj.code == \
            customer.code

    @pytest.mark.asyncio
    async def test_get_by_id_not_found(
        self,
        obj_manager: CustomerManager
    ):
        """
        Test case for the `get_by_id` method of
        `CustomerManager` when the
        customer is not found.
        """

        non_existent_id = 9999  # An ID that's not in the database

        retrieved_customer = await \
            obj_manager.get_by_id(
                non_existent_id)

        assert retrieved_customer is None

    @pytest.mark.asyncio
    async def test_get_by_code_returns_customer(
        self,
        obj_manager: CustomerManager,
        session: AsyncSession
    ):
        """
        Test case for the `get_by_code` method of
        `CustomerManager` that checks if
        a customer is
        returned by its code.
        """

        new_obj = await \
            CustomerFactory.create_async(
                session)

        customer = await \
            obj_manager.get_by_code(
                new_obj.code)

        assert isinstance(
            customer,
            Customer)

        assert new_obj.customer_id == \
            customer.customer_id
        assert new_obj.code == \
            customer.code

    @pytest.mark.asyncio
    async def test_get_by_code_returns_none_for_nonexistent_code(
        self,
        obj_manager: CustomerManager
    ):
        """
        Test case for the `get_by_code` method of
        `CustomerManager` when the code does not exist.
        """
        # Generate a random UUID that doesn't correspond to
        # any Customer in the database
        random_code = uuid.uuid4()

        customer = await \
            obj_manager.get_by_code(
                random_code)

        assert customer is None

    # activeOrganizationID
    # email
    # emailConfirmedUTCDateTime
    # firstName
    # forgotPasswordKeyExpirationUTCDateTime
    # forgotPasswordKeyValue
    # fSUserCodeValue
    # isActive
    # isEmailAllowed
    # isEmailConfirmed
    # isEmailMarketingAllowed
    # isLocked
    # isMultipleOrganizationsAllowed
    # isVerboseLoggingForced
    # lastLoginUTCDateTime
    # lastName
    # password
    # phone
    # province
    # registrationUTCDateTime
    # TacID

    @pytest.mark.asyncio
    async def test_get_by_tac_id_existing(
        self,
        obj_manager: CustomerManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of the
        `get_by_tac_id` method when
        a customer with
        a specific tac_id exists.

        Steps:
        1. Create a customer using the
            CustomerFactory.
        2. Fetch the customer using the
            `get_by_tac_id` method of the obj_manager.
        3. Assert that the fetched customers list contains
            only one customer.
        4. Assert that the fetched customer
            is an instance
            of the Customer class.
        5. Assert that the code of the fetched customer
            matches the code of the created customer.
        6. Fetch the corresponding tac object
            using the tac_id of the created customer.
        7. Assert that the fetched tac object is
            an instance of the Tac class.
        8. Assert that the tac_code_peek of the fetched
            customer matches the
            code of the fetched tac.

        """
        # Add a customer with a specific
        # tac_id
        obj_1 = await CustomerFactory.create_async(
            session=session)

        # Fetch the customer using
        # the manager function

        fetched_objs = await \
            obj_manager.get_by_tac_id(
                obj_1.tac_id)
        assert len(fetched_objs) == 1
        assert isinstance(fetched_objs[0],
                          Customer)
        assert fetched_objs[0].code == \
            obj_1.code

        stmt = select(models.Tac).where(
            models.Tac._tac_id == obj_1.tac_id)  # type: ignore  # noqa: E501
        result = await session.execute(stmt)
        tac = result.scalars().first()

        assert isinstance(tac, models.Tac)

        assert fetched_objs[0].tac_code_peek == tac.code

    @pytest.mark.asyncio
    async def test_get_by_tac_id_nonexistent(
        self,
        obj_manager: CustomerManager
    ):
        """
        Test case to verify the behavior of the
        get_by_tac_id method when the tac ID does not exist.

        This test case ensures that when a non-existent
        tac ID is provided to the get_by_tac_id method,
        an empty list is returned.
        """

        non_existent_id = 999

        fetched_objs = await \
            obj_manager.get_by_tac_id(
                non_existent_id)
        assert len(fetched_objs) == 0

    @pytest.mark.asyncio
    async def test_get_by_tac_id_invalid_type(
        self,
        obj_manager: CustomerManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of the
        `get_by_tac_id` method when an invalid tac ID is provided.

        Args:
            obj_manager (CustomerManager): An
                instance of the CustomerManager class.
            session (AsyncSession): An instance
                of the AsyncSession class.

        Raises:
            Exception: If an exception is raised during
            the execution of the `get_by_tac_id` method.

        Returns:
            None
        """

        invalid_id = "invalid_id"

        with pytest.raises(Exception):
            await obj_manager.get_by_tac_id(
                invalid_id)  # type: ignore

        await session.rollback()
    # uTCOffsetInMinutes
    # zip
