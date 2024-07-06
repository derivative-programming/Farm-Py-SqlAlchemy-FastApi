# managers/tests/organization_test.py  # pylint: disable=duplicate-code
# pylint: disable=protected-access, too-many-public-methods
# pylint: disable=unused-argument
# pylint: disable=unused-import
"""
    This class contains unit tests for the
    `OrganizationManager` class.
"""

import uuid  # noqa: F401
from typing import List

import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

import pytest
from helpers.session_context import SessionContext
from managers.organization import OrganizationManager
from models import Organization
from models.factory import OrganizationFactory
from models.serialization_schema.organization import OrganizationSchema


class TestOrganizationManager:
    """
    This class contains unit tests for the
    `OrganizationManager` class.
    """

    @pytest_asyncio.fixture(scope="function")
    async def obj_manager(self, session: AsyncSession):
        """
        Fixture that returns an instance of
        `OrganizationManager` for testing.
        """
        session_context = SessionContext({}, session)
        session_context.customer_code = uuid.uuid4()
        return OrganizationManager(session_context)

    @pytest.mark.asyncio
    async def test_build(
        self,
        obj_manager: OrganizationManager
    ):
        """
        Test case for the `build` method of
        `OrganizationManager`.
        """
        # Define mock data for our organization
        mock_data = {
            "code": uuid.uuid4()
        }

        # Call the build function of the manager
        organization = await \
            obj_manager.build(
                **mock_data)

        # Assert that the returned object is an
        # instance of Organization
        assert isinstance(
            organization,
            Organization)

        # Assert that the attributes of the
        # organization match our mock data
        assert organization.code == mock_data["code"]

    @pytest.mark.asyncio
    async def test_build_with_missing_data(
        self,
        obj_manager: OrganizationManager,
        session: AsyncSession
    ):
        """
        Test case for the `build` method of
        `OrganizationManager` with missing data.
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
    async def test_add_correctly_adds_organization_to_database(
        self,
        obj_manager: OrganizationManager,
        session: AsyncSession
    ):
        """
        Test case for the `add` method of
        `OrganizationManager` that checks if a
        organization is correctly added to the database.
        """
        new_obj = await \
            OrganizationFactory.build_async(
                session)

        assert new_obj.organization_id == 0

        # Add the organization using the
        # manager's add method
        added_obj = await \
            obj_manager.add(
                organization=new_obj)

        assert isinstance(added_obj,
                          Organization)

        assert str(added_obj.insert_user_id) == (
            str(obj_manager._session_context.customer_code))
        assert str(added_obj.last_update_user_id) == (
            str(obj_manager._session_context.customer_code))

        assert added_obj.organization_id > 0

        # Fetch the organization from
        # the database directly
        result = await session.execute(
            select(Organization).filter(
                Organization._organization_id == (
                    added_obj.organization_id)  # type: ignore
            )
        )
        fetched_obj = result.scalars().first()

        # Assert that the fetched organization
        # is not None and matches the
        # added organization
        assert fetched_obj is not None
        assert isinstance(fetched_obj,
                          Organization)
        assert fetched_obj.organization_id == \
            added_obj.organization_id

    @pytest.mark.asyncio
    async def test_add_returns_correct_organization_object(
        self,
        obj_manager: OrganizationManager,
        session: AsyncSession
    ):
        """
        Test case for the `add` method of
        `OrganizationManager` that checks if the
        correct organization object is returned.
        """
        # Create a test organization
        # using the OrganizationFactory
        # without persisting it to the database
        new_obj = await \
            OrganizationFactory.build_async(
                session)

        assert new_obj.organization_id == 0

        new_obj.code = uuid.uuid4()

        # Add the organization using
        # the manager's add method
        added_obj = await \
            obj_manager.add(
                organization=new_obj)

        assert isinstance(added_obj,
                          Organization)

        assert str(added_obj.insert_user_id) == (
            str(obj_manager._session_context.customer_code))
        assert str(added_obj.last_update_user_id) == (
            str(obj_manager._session_context.customer_code))

        assert added_obj.organization_id > 0

        # Assert that the returned
        # organization matches the
        # test organization
        assert added_obj.organization_id == \
            new_obj.organization_id
        assert added_obj.code == \
            new_obj.code

    @pytest.mark.asyncio
    async def test_update(
        self,
        obj_manager: OrganizationManager,
        session: AsyncSession
    ):
        """
        Test case for the `update` method
        of `OrganizationManager`
        that checks if a organization
        is correctly updated.
        """
        new_obj = await \
            OrganizationFactory.create_async(
                session)

        new_obj.code = uuid.uuid4()

        updated_obj = await \
            obj_manager.update(
                organization=new_obj)

        assert isinstance(updated_obj,
                          Organization)

        assert str(updated_obj.last_update_user_id) == str(
            obj_manager._session_context.customer_code)

        assert updated_obj.organization_id == \
            new_obj.organization_id
        assert updated_obj.code == \
            new_obj.code

        result = await session.execute(
            select(Organization).filter(
                Organization._organization_id == (
                    new_obj.organization_id))  # type: ignore
        )

        fetched_obj = result.scalars().first()

        assert updated_obj.organization_id == \
            fetched_obj.organization_id
        assert updated_obj.code == \
            fetched_obj.code

        assert new_obj.organization_id == \
            fetched_obj.organization_id
        assert new_obj.code == \
            fetched_obj.code

    @pytest.mark.asyncio
    async def test_update_via_dict(
        self,
        obj_manager: OrganizationManager,
        session: AsyncSession
    ):
        """
        Test case for the `update` method
        of `OrganizationManager`
        that checks if a organization is
        correctly updated using a dictionary.
        """
        new_obj = await \
            OrganizationFactory.create_async(
                session)

        new_code = uuid.uuid4()

        updated_obj = await \
            obj_manager.update(
                organization=new_obj,
                code=new_code
            )

        assert isinstance(updated_obj,
                          Organization)

        assert str(updated_obj.last_update_user_id) == str(
            obj_manager._session_context.customer_code
        )

        assert updated_obj.organization_id == \
            new_obj.organization_id
        assert updated_obj.code == new_code

        result = await session.execute(
            select(Organization).filter(
                Organization._organization_id == (
                    new_obj.organization_id))  # type: ignore
        )

        fetched_obj = result.scalars().first()

        assert updated_obj.organization_id == \
            fetched_obj.organization_id
        assert updated_obj.code == \
            fetched_obj.code

        assert new_obj.organization_id == \
            fetched_obj.organization_id
        assert new_code == \
            fetched_obj.code

    @pytest.mark.asyncio
    async def test_update_invalid_organization(
        self,
        obj_manager: OrganizationManager
    ):
        """
        Test case for the `update` method of
        `OrganizationManager`
        with an invalid organization.
        """

        # None organization
        organization = None

        new_code = uuid.uuid4()

        updated_obj = await (
            obj_manager.update(
                organization, code=new_code))  # type: ignore

        # Assertions
        assert updated_obj is None

    @pytest.mark.asyncio
    async def test_update_with_nonexistent_attribute(
        self,
        obj_manager: OrganizationManager,
        session: AsyncSession
    ):
        """
        Test case for the `update` method of
        `OrganizationManager`
        with a nonexistent attribute.
        """
        new_obj = await \
            OrganizationFactory.create_async(
                session)

        new_code = uuid.uuid4()

        with pytest.raises(ValueError):
            await obj_manager.update(
                organization=new_obj,
                xxx=new_code
            )

        await session.rollback()

    @pytest.mark.asyncio
    async def test_delete(
        self,
        obj_manager: OrganizationManager,
        session: AsyncSession
    ):
        """
        Test case for the `delete` method of
        `OrganizationManager`.
        """
        new_obj = await OrganizationFactory.create_async(
            session)

        result = await session.execute(
            select(Organization).filter(
                Organization._organization_id == (
                    new_obj.organization_id))  # type: ignore
        )
        fetched_obj = result.scalars().first()

        assert isinstance(fetched_obj,
                          Organization)

        assert fetched_obj.organization_id == \
            new_obj.organization_id

        await obj_manager.delete(
            organization_id=new_obj.organization_id)

        result = await session.execute(
            select(Organization).filter(
                Organization._organization_id == (
                    new_obj.organization_id))  # type: ignore
        )
        fetched_obj = result.scalars().first()

        assert fetched_obj is None

    @pytest.mark.asyncio
    async def test_delete_nonexistent(
        self,
        obj_manager: OrganizationManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of deleting a nonexistent
        organization.

        This test case ensures that when the delete method
        is called with the ID of a nonexistent
        organization,
        an exception is raised. The test also verifies that
        the session is rolled back after the delete operation.

        :param obj_manager: The instance of the
            OrganizationManager class.
        :param session: The instance of the AsyncSession class.
        """
        with pytest.raises(Exception):
            await obj_manager.delete(999)

        await session.rollback()

    @pytest.mark.asyncio
    async def test_delete_invalid_type(
        self,
        obj_manager: OrganizationManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of deleting a organization
        with an invalid type.

        This test case ensures that when the `delete` method
        of the `obj_manager` is called with an invalid type,
        an exception is raised. The test case expects the
        `delete` method to raise an exception, and if it doesn't,
        the test case will fail.

        Args:
            obj_manager
            (OrganizationManager): An
                instance of the
                `OrganizationManager` class.
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
        obj_manager: OrganizationManager,
        session: AsyncSession
    ):
        """
        Test case for the `get_list` method of the
        `OrganizationManager` class.

        This test verifies that the `get_list`
        method returns the correct list of organizations.

        Steps:
        1. Call the `get_list` method of the
            `obj_manager` instance.
        2. Assert that the returned list is empty.
        3. Create 5 organization objects using the
            `OrganizationFactory.create_async` method.
        4. Assert that the
            `organizations_data` variable
            is of type `List`.
        5. Call the `get_list` method of the
            `obj_manager` instance again.
        6. Assert that the returned list contains 5 organizations.
        7. Assert that all elements in the returned list are
            instances of the
            `Organization` class.
        """

        organizations = await obj_manager.get_list()

        assert len(organizations) == 0

        organizations_data = (
            [await OrganizationFactory.create_async(session)
             for _ in range(5)])

        assert isinstance(organizations_data, List)

        organizations = await obj_manager.get_list()

        assert len(organizations) == 5
        assert all(isinstance(
            organization,
            Organization
        ) for organization in organizations)

    @pytest.mark.asyncio
    async def test_to_json(
        self,
        obj_manager: OrganizationManager,
        session: AsyncSession
    ):
        """
        Test the 'to_json' method of the OrganizationManager class.

        Args:
            obj_manager
            (OrganizationManager): An
                instance of the
                OrganizationManager class.
            session (AsyncSession): An instance of the AsyncSession class.

        Returns:
            None

        Raises:
            AssertionError: If the json_data is None.
        """
        organization = await \
            OrganizationFactory.build_async(
                session)

        json_data = obj_manager.to_json(
            organization)

        assert json_data is not None

    @pytest.mark.asyncio
    async def test_to_dict(
        self,
        obj_manager: OrganizationManager,
        session: AsyncSession
    ):
        """
        Test the to_dict method of the OrganizationManager class.

        Args:
            obj_manager
            (OrganizationManager): An
                instance of the
                OrganizationManager class.
            session (AsyncSession): An instance of the AsyncSession class.

        Returns:
            None
        """
        organization = await \
            OrganizationFactory.build_async(
                session)

        dict_data = \
            obj_manager.to_dict(
                organization)

        assert dict_data is not None

    @pytest.mark.asyncio
    async def test_from_json(
        self,
        obj_manager: OrganizationManager,
        session: AsyncSession
    ):
        """
        Test the `from_json` method of the
        `OrganizationManager` class.

        This method tests the functionality of the
        `from_json` method of the
        `OrganizationManager` class.
        It creates a organization using
        the `OrganizationFactory`
        and converts it to JSON using the `to_json` method.
        Then, it deserializes the JSON data using the
        `from_json` method and asserts that the deserialized
        organization is an instance of the
        `Organization` class and has
        the same code as the original organization.

        Args:
            obj_manager
            (OrganizationManager): An
                instance of the
                `OrganizationManager` class.
            session (AsyncSession): An instance of the `AsyncSession` class.

        Returns:
            None
        """
        organization = await \
            OrganizationFactory.create_async(
                session)

        json_data = obj_manager.to_json(
            organization)

        deserialized_organization = await \
            obj_manager.from_json(json_data)

        assert isinstance(deserialized_organization,
                          Organization)
        assert deserialized_organization.code == \
            organization.code

    @pytest.mark.asyncio
    async def test_from_dict(
        self,
        obj_manager: OrganizationManager,
        session: AsyncSession
    ):
        """
        Test the `from_dict` method of the
        `OrganizationManager` class.

        This method tests the functionality of the
        `from_dict` method, which is used to deserialize
        a dictionary representation of a
        organization object.

        Args:
            obj_manager
            (OrganizationManager): An instance
                of the `OrganizationManager` class.
            session (AsyncSession): An instance of the
            `AsyncSession` class.

        Returns:
            None

        Raises:
            AssertionError: If any of the assertions fail.
        """
        organization = await \
            OrganizationFactory.create_async(
                session)

        schema = OrganizationSchema()

        new_obj = schema.dump(organization)

        assert isinstance(new_obj, dict)

        deserialized_organization = await \
            obj_manager.from_dict(
                new_obj)

        assert isinstance(deserialized_organization,
                          Organization)

        assert deserialized_organization.code == \
            organization.code

    @pytest.mark.asyncio
    async def test_count_basic_functionality(
        self,
        obj_manager: OrganizationManager,
        session: AsyncSession
    ):
        """
        Test the basic functionality of the count method
        in the OrganizationManager class.

        This test case creates 5 organization
        objects using the
        OrganizationFactory and checks if the count method
        returns the correct count of
        organizations.

        Steps:
        1. Create 5 organization objects using
            the OrganizationFactory.
        2. Call the count method of the obj_manager.
        3. Assert that the count is equal to 5.

        """
        organizations_data = (
            [await OrganizationFactory.create_async(session)
             for _ in range(5)])

        assert isinstance(organizations_data, List)

        count = await obj_manager.count()

        assert count == 5

    @pytest.mark.asyncio
    async def test_count_empty_database(
        self,
        obj_manager: OrganizationManager
    ):
        """
        Test the count method when the database is empty.

        This test case checks if the count method of the
        OrganizationManager class
        returns 0 when the database is empty.

        Args:
            obj_manager
            (OrganizationManager): An
                instance of the
                OrganizationManager class.

        Returns:
            None
        """

        count = await obj_manager.count()

        assert count == 0

    @pytest.mark.asyncio
    async def test_refresh_basic(
        self,
        obj_manager: OrganizationManager,
        session: AsyncSession
    ):
        """
        Test the basic functionality of refreshing
        a organization instance.

        This test performs the following steps:
        1. Creates a organization instance using
            the OrganizationFactory.
        2. Retrieves the organization from th
            database to ensure
            it was added correctly.
        3. Updates the organization's code and verifies the update.
        4. Refreshes the original organization instance
            and checks if
            it reflects the updated code.

        Args:
            obj_manager
            (OrganizationManager): The
                manager responsible
                for organization operations.
            session (AsyncSession): The SQLAlchemy asynchronous session.
        """
        # Add a organization
        obj_1 = await OrganizationFactory.create_async(
            session=session)

        # Retrieve the organization from the database
        result = await session.execute(
            select(Organization).filter(
                Organization._organization_id == (
                    obj_1.organization_id))  # type: ignore
        )  # type: ignore
        obj_2 = result.scalars().first()

        # Verify that the retrieved organization
        # matches the added organization
        assert obj_1.code == \
            obj_2.code

        # Update the organization's code
        updated_code1 = uuid.uuid4()
        obj_1.code = updated_code1
        updated_obj_1 = await obj_manager.update(
            obj_1)

        # Verify that the updated organization
        # is of type Organization
        # and has the updated code
        assert isinstance(updated_obj_1,
                          Organization)

        assert updated_obj_1.code == updated_code1

        # Refresh the original organization instance
        refreshed_obj_2 = await obj_manager.refresh(
            obj_2)

        # Verify that the refreshed organization
        # reflects the updated code
        assert refreshed_obj_2.code == updated_code1

    @pytest.mark.asyncio
    async def test_refresh_nonexistent_organization(
        self,
        obj_manager: OrganizationManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of refreshing a
        nonexistent organization.

        Args:
            obj_manager
            (OrganizationManager): The
                instance of the
                OrganizationManager class.
            session (AsyncSession): The instance of the AsyncSession class.

        Raises:
            Exception: If the organization
            refresh operation raises an exception.

        Returns:
            None
        """
        organization = Organization(
            organization_id=999)

        with pytest.raises(Exception):
            await obj_manager.refresh(
                organization)

        await session.rollback()

    @pytest.mark.asyncio
    async def test_exists_with_existing_organization(
        self,
        obj_manager: OrganizationManager,
        session: AsyncSession
    ):
        """
        Test case to check if a organization
        exists using the manager function.

        Args:
            obj_manager
            (OrganizationManager): The
                organization manager instance.
            session (AsyncSession): The async session object.

        Returns:
            None
        """
        # Add a organization
        obj_1 = await OrganizationFactory.create_async(
            session=session)

        # Check if the organization exists
        # using the manager function
        assert await obj_manager.exists(
            obj_1.organization_id) is True

    @pytest.mark.asyncio
    async def test_is_equal_with_existing_organization(
        self,
        obj_manager: OrganizationManager,
        session: AsyncSession
    ):
        """
        Test if the is_equal method of the
        OrganizationManager
        class correctly compares two
        organizations.

        Args:
            obj_manager
            (OrganizationManager): An
                instance of the
                OrganizationManager class.
            session (AsyncSession): An instance of the AsyncSession class.

        Returns:
            None
        """
        # Add a organization
        obj_1 = await \
            OrganizationFactory.create_async(
                session=session)

        obj_2 = await \
            obj_manager.get_by_id(
                organization_id=obj_1.organization_id)

        assert obj_manager.is_equal(
            obj_1, obj_2) is True

        obj_1_dict = \
            obj_manager.to_dict(
                obj_1)

        organization3 = await \
            obj_manager.from_dict(
                obj_1_dict)

        assert obj_manager.is_equal(
            obj_1, organization3) is True

    @pytest.mark.asyncio
    async def test_exists_with_nonexistent_organization(
        self,
        obj_manager: OrganizationManager
    ):
        """
        Test case to check if a organization with a
        non-existent ID exists in the database.

        Args:
            obj_manager
            (OrganizationManager): The
                instance of the OrganizationManager class.

        Returns:
            bool: True if the organization exists,
                False otherwise.
        """
        non_existent_id = 999

        assert await obj_manager.exists(non_existent_id) is False

    @pytest.mark.asyncio
    async def test_exists_with_invalid_id_type(
        self,
        obj_manager: OrganizationManager,
        session: AsyncSession
    ):
        """
        Test case to check if the exists method raises
        an exception when an invalid ID type is provided.

        Args:
            obj_manager
            (OrganizationManager): The instance
                of the OrganizationManager class.
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
