# models/managers/tests/org_customer_test.py  # pylint: disable=duplicate-code # noqa: E501
# pylint: disable=protected-access, too-many-public-methods
# pylint: disable=unused-argument
# pylint: disable=unused-import
"""
    This class contains unit tests for the
    `OrgCustomerManager` class.
"""

import uuid  # noqa: F401

import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

import models
import pytest
from helpers.session_context import SessionContext
from managers.org_customer import OrgCustomerManager
from models import OrgCustomer
from models.factory import OrgCustomerFactory


class TestOrgCustomerGetByManager:
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
        session_context = SessionContext({}, session)
        session_context.customer_code = uuid.uuid4()
        return OrgCustomerManager(session_context)

    @pytest.mark.asyncio
    async def test_build(
        self,
        obj_manager: OrgCustomerManager
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
        org_customer = await \
            obj_manager.build(
                **mock_data)

        # Assert that the returned object is an instance of
        # OrgCustomer
        assert isinstance(
            org_customer,
            OrgCustomer)

        # Assert that the attributes of the
        # org_customer match our mock data
        assert org_customer.code == mock_data["code"]

    @pytest.mark.asyncio
    async def test_get_by_id(
        self,
        obj_manager: OrgCustomerManager,
        session: AsyncSession
    ):
        """
        Test case for the `get_by_id` method of
        `OrgCustomerManager`.
        """
        new_obj = await \
            OrgCustomerFactory.create_async(
                session)

        org_customer = await \
            obj_manager.get_by_id(
                new_obj.org_customer_id)

        assert isinstance(
            org_customer,
            OrgCustomer)

        assert new_obj.org_customer_id == \
            org_customer.org_customer_id
        assert new_obj.code == \
            org_customer.code

    @pytest.mark.asyncio
    async def test_get_by_id_not_found(
        self,
        obj_manager: OrgCustomerManager
    ):
        """
        Test case for the `get_by_id` method of
        `OrgCustomerManager` when the
        org_customer is not found.
        """

        non_existent_id = 9999  # An ID that's not in the database

        retrieved_org_customer = await \
            obj_manager.get_by_id(
                non_existent_id)

        assert retrieved_org_customer is None

    @pytest.mark.asyncio
    async def test_get_by_code_returns_org_customer(
        self,
        obj_manager: OrgCustomerManager,
        session: AsyncSession
    ):
        """
        Test case for the `get_by_code` method of
        `OrgCustomerManager` that checks if
        a org_customer is
        returned by its code.
        """

        new_obj = await \
            OrgCustomerFactory.create_async(
                session)

        org_customer = await \
            obj_manager.get_by_code(
                new_obj.code)

        assert isinstance(
            org_customer,
            OrgCustomer)

        assert new_obj.org_customer_id == \
            org_customer.org_customer_id
        assert new_obj.code == \
            org_customer.code

    @pytest.mark.asyncio
    async def test_get_by_code_returns_none_for_nonexistent_code(
        self,
        obj_manager: OrgCustomerManager
    ):
        """
        Test case for the `get_by_code` method of
        `OrgCustomerManager` when the code does not exist.
        """
        # Generate a random UUID that doesn't correspond to
        # any OrgCustomer in the database
        random_code = uuid.uuid4()

        org_customer = await \
            obj_manager.get_by_code(
                random_code)

        assert org_customer is None

    # CustomerID

    @pytest.mark.asyncio
    async def test_get_by_customer_id_existing(
        self,
        obj_manager: OrgCustomerManager,
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
            method of the obj_manager.
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
        obj_1 = await OrgCustomerFactory.create_async(
            session=session)

        # Fetch the org_customer using the
        # manager function

        fetched_objs = await \
            obj_manager.get_by_customer_id(
                obj_1.customer_id)
        assert len(fetched_objs) == 1
        assert isinstance(fetched_objs[0],
                          OrgCustomer)
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
        obj_manager: OrgCustomerManager
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

        fetched_objs = (
            await obj_manager.get_by_customer_id(
                non_existent_id))
        assert len(fetched_objs) == 0

    @pytest.mark.asyncio
    async def test_get_by_customer_id_invalid_type(
        self,
        obj_manager: OrgCustomerManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of the
        `get_by_customer_id` method
        when an invalid foreign key ID type is provided.

        It ensures that an exception is raised
        when an invalid ID is passed to the method.

        Args:
            obj_manager (OrgCustomerManager): The
                instance of the OrgCustomerManager class.
            session (AsyncSession): The instance of the AsyncSession class.

        Raises:
            Exception: If an exception is not
                raised when an invalid ID is passed.

        """
        invalid_id = "invalid_id"

        with pytest.raises(Exception):
            await obj_manager.get_by_customer_id(
                invalid_id)  # type: ignore  # noqa: E501

        await session.rollback()
    # email
    # OrganizationID

    @pytest.mark.asyncio
    async def test_get_by_organization_id_existing(
        self,
        obj_manager: OrgCustomerManager,
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
            `get_by_organization_id` method of the obj_manager.
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
        obj_1 = await OrgCustomerFactory.create_async(
            session=session)

        # Fetch the org_customer using
        # the manager function

        fetched_objs = await \
            obj_manager.get_by_organization_id(
                obj_1.organization_id)
        assert len(fetched_objs) == 1
        assert isinstance(fetched_objs[0],
                          OrgCustomer)
        assert fetched_objs[0].code == \
            obj_1.code

        stmt = select(models.Organization).where(
            models.Organization._organization_id == obj_1.organization_id)  # type: ignore  # noqa: E501
        result = await session.execute(stmt)
        organization = result.scalars().first()

        assert isinstance(organization, models.Organization)

        assert fetched_objs[0].organization_code_peek == organization.code

    @pytest.mark.asyncio
    async def test_get_by_organization_id_nonexistent(
        self,
        obj_manager: OrgCustomerManager
    ):
        """
        Test case to verify the behavior of the
        get_by_organization_id method when the organization ID does not exist.

        This test case ensures that when a non-existent
        organization ID is provided to the get_by_organization_id method,
        an empty list is returned.
        """

        non_existent_id = 999

        fetched_objs = await \
            obj_manager.get_by_organization_id(
                non_existent_id)
        assert len(fetched_objs) == 0

    @pytest.mark.asyncio
    async def test_get_by_organization_id_invalid_type(
        self,
        obj_manager: OrgCustomerManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of the
        `get_by_organization_id` method when an invalid organization ID is provided.

        Args:
            obj_manager (OrgCustomerManager): An
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
            await obj_manager.get_by_organization_id(
                invalid_id)  # type: ignore

        await session.rollback()
