# models/managers/tests/organization_test.py
# pylint: disable=protected-access
# pylint: disable=unused-argument
"""
    This class contains unit tests for the
    `OrganizationManager` class.
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
    async def organization_manager(self, session: AsyncSession):
        """
        Fixture that returns an instance of
        `OrganizationManager` for testing.
        """
        session_context = SessionContext(dict(), session)
        session_context.customer_code = uuid.uuid4()
        return OrganizationManager(session_context)
    @pytest.mark.asyncio
    async def test_build(
        self,
        organization_manager: OrganizationManager
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
        organization = await organization_manager.build(
            **mock_data)
        # Assert that the returned object is an instance of Organization
        assert isinstance(
            organization, Organization)
        # Assert that the attributes of the
        # organization match our mock data
        assert organization.code == mock_data["code"]
    @pytest.mark.asyncio
    async def test_build_with_missing_data(
        self,
        organization_manager: OrganizationManager,
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
            await organization_manager.build(**mock_data)
        await session.rollback()
    @pytest.mark.asyncio
    async def test_add_correctly_adds_organization_to_database(
        self,
        organization_manager: OrganizationManager,
        session: AsyncSession
    ):
        """
        Test case for the `add` method of
        `OrganizationManager` that checks if a
        organization is correctly added to the database.
        """
        test_organization = await OrganizationFactory.build_async(
            session)
        assert test_organization.organization_id == 0
        # Add the organization using the
        # manager's add method
        added_organization = await organization_manager.add(
            organization=test_organization)
        assert isinstance(added_organization, Organization)
        assert str(added_organization.insert_user_id) == (
            str(organization_manager._session_context.customer_code))
        assert str(added_organization.last_update_user_id) == (
            str(organization_manager._session_context.customer_code))
        assert added_organization.organization_id > 0
        # Fetch the organization from
        # the database directly
        result = await session.execute(
            select(Organization).filter(
                Organization._organization_id == added_organization.organization_id  # type: ignore
            )
        )
        fetched_organization = result.scalars().first()
        # Assert that the fetched organization
        # is not None and matches the
        # added organization
        assert fetched_organization is not None
        assert isinstance(fetched_organization, Organization)
        assert fetched_organization.organization_id == added_organization.organization_id
    @pytest.mark.asyncio
    async def test_add_returns_correct_organization_object(
        self,
        organization_manager: OrganizationManager,
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
        test_organization = await OrganizationFactory.build_async(
            session)
        assert test_organization.organization_id == 0
        test_organization.code = uuid.uuid4()
        # Add the organization using
        # the manager's add method
        added_organization = await organization_manager.add(
            organization=test_organization)
        assert isinstance(added_organization, Organization)
        assert str(added_organization.insert_user_id) == (
            str(organization_manager._session_context.customer_code))
        assert str(added_organization.last_update_user_id) == (
            str(organization_manager._session_context.customer_code))
        assert added_organization.organization_id > 0
        # Assert that the returned
        # organization matches the
        # test organization
        assert added_organization.organization_id == \
            test_organization.organization_id
        assert added_organization.code == \
            test_organization.code
    @pytest.mark.asyncio
    async def test_get_by_id(
        self,
        organization_manager: OrganizationManager,
        session: AsyncSession
    ):
        """
        Test case for the `get_by_id` method of
        `OrganizationManager`.
        """
        test_organization = await OrganizationFactory.create_async(
            session)
        organization = await organization_manager.get_by_id(
            test_organization.organization_id)
        assert isinstance(
            organization, Organization)
        assert test_organization.organization_id == \
            organization.organization_id
        assert test_organization.code == \
            organization.code
    @pytest.mark.asyncio
    async def test_get_by_id_not_found(
        self,
        organization_manager: OrganizationManager
    ):
        """
        Test case for the `get_by_id` method of
        `OrganizationManager` when the
        organization is not found.
        """
        non_existent_id = 9999  # An ID that's not in the database
        retrieved_organization = await organization_manager.get_by_id(
            non_existent_id)
        assert retrieved_organization is None
    @pytest.mark.asyncio
    async def test_get_by_code_returns_organization(
        self,
        organization_manager: OrganizationManager,
        session: AsyncSession
    ):
        """
        Test case for the `get_by_code` method of
        `OrganizationManager` that checks if
        a organization is
        returned by its code.
        """
        test_organization = await OrganizationFactory.create_async(
            session)
        organization = await organization_manager.get_by_code(
            test_organization.code)
        assert isinstance(
            organization, Organization)
        assert test_organization.organization_id == \
            organization.organization_id
        assert test_organization.code == \
            organization.code
    @pytest.mark.asyncio
    async def test_get_by_code_returns_none_for_nonexistent_code(
        self,
        organization_manager: OrganizationManager
    ):
        """
        Test case for the `get_by_code` method of
        `OrganizationManager` when the code does not exist.
        """
        # Generate a random UUID that doesn't correspond to
        # any Organization in the database
        random_code = uuid.uuid4()
        organization = await organization_manager.get_by_code(
            random_code)
        assert organization is None
    @pytest.mark.asyncio
    async def test_update(
        self,
        organization_manager: OrganizationManager,
        session: AsyncSession
    ):
        """
        Test case for the `update` method
        of `OrganizationManager`
        that checks if a organization
        is correctly updated.
        """
        test_organization = await OrganizationFactory.create_async(
            session)
        test_organization.code = uuid.uuid4()
        updated_organization = await organization_manager.update(
            organization=test_organization)
        assert isinstance(updated_organization, Organization)
        assert str(updated_organization.last_update_user_id) == str(
            organization_manager._session_context.customer_code)
        assert updated_organization.organization_id == \
            test_organization.organization_id
        assert updated_organization.code == \
            test_organization.code
        result = await session.execute(
            select(Organization).filter(
                Organization._organization_id == test_organization.organization_id)  # type: ignore
        )
        fetched_organization = result.scalars().first()
        assert updated_organization.organization_id == \
            fetched_organization.organization_id
        assert updated_organization.code == \
            fetched_organization.code
        assert test_organization.organization_id == \
            fetched_organization.organization_id
        assert test_organization.code == \
            fetched_organization.code
    @pytest.mark.asyncio
    async def test_update_via_dict(
        self,
        organization_manager: OrganizationManager,
        session: AsyncSession
    ):
        """
        Test case for the `update` method
        of `OrganizationManager`
        that checks if a organization is
        correctly updated using a dictionary.
        """
        test_organization = await OrganizationFactory.create_async(
            session)
        new_code = uuid.uuid4()
        updated_organization = await organization_manager.update(
            organization=test_organization,
            code=new_code
        )
        assert isinstance(updated_organization, Organization)
        assert str(updated_organization.last_update_user_id) == str(
            organization_manager._session_context.customer_code
        )
        assert updated_organization.organization_id == \
            test_organization.organization_id
        assert updated_organization.code == new_code
        result = await session.execute(
            select(Organization).filter(
                Organization._organization_id == test_organization.organization_id)  # type: ignore
        )
        fetched_organization = result.scalars().first()
        assert updated_organization.organization_id == \
            fetched_organization.organization_id
        assert updated_organization.code == \
            fetched_organization.code
        assert test_organization.organization_id == \
            fetched_organization.organization_id
        assert new_code == \
            fetched_organization.code
    @pytest.mark.asyncio
    async def test_update_invalid_organization(
        self,
        organization_manager: OrganizationManager
    ):
        """
        Test case for the `update` method of `OrganizationManager`
        with an invalid organization.
        """
        # None organization
        organization = None
        new_code = uuid.uuid4()
        updated_organization = await (
            organization_manager.update(
                organization, code=new_code))  # type: ignore
        # Assertions
        assert updated_organization is None
    @pytest.mark.asyncio
    async def test_update_with_nonexistent_attribute(
        self,
        organization_manager: OrganizationManager,
        session: AsyncSession
    ):
        """
        Test case for the `update` method of `OrganizationManager`
        with a nonexistent attribute.
        """
        test_organization = await OrganizationFactory.create_async(
            session)
        new_code = uuid.uuid4()
        with pytest.raises(ValueError):
            await organization_manager.update(
                organization=test_organization,
                xxx=new_code
            )
        await session.rollback()
    @pytest.mark.asyncio
    async def test_delete(
        self,
        organization_manager: OrganizationManager,
        session: AsyncSession
    ):
        """
        Test case for the `delete` method of `OrganizationManager`.
        """
        organization_data = await OrganizationFactory.create_async(
            session)
        result = await session.execute(
            select(Organization).filter(
                Organization._organization_id == organization_data.organization_id)  # type: ignore
        )
        fetched_organization = result.scalars().first()
        assert isinstance(fetched_organization, Organization)
        assert fetched_organization.organization_id == \
            organization_data.organization_id
        await organization_manager.delete(
            organization_id=organization_data.organization_id)
        result = await session.execute(
            select(Organization).filter(
                Organization._organization_id == organization_data.organization_id)  # type: ignore
        )
        fetched_organization = result.scalars().first()
        assert fetched_organization is None
    @pytest.mark.asyncio
    async def test_delete_nonexistent(
        self,
        organization_manager: OrganizationManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of deleting a nonexistent organization.
        This test case ensures that when the delete method
        is called with the ID of a nonexistent organization,
        an exception is raised. The test also verifies that
        the session is rolled back after the delete operation.
        :param organization_manager: The instance of the OrganizationManager class.
        :param session: The instance of the AsyncSession class.
        """
        with pytest.raises(Exception):
            await organization_manager.delete(999)
        await session.rollback()
    @pytest.mark.asyncio
    async def test_delete_invalid_type(
        self,
        organization_manager: OrganizationManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of deleting a organization
        with an invalid type.
        This test case ensures that when the `delete` method
        of the `organization_manager` is called with an invalid type,
        an exception is raised. The test case expects the
        `delete` method to raise an exception, and if it doesn't,
        the test case will fail.
        Args:
            organization_manager (OrganizationManager): An
                instance of the
                `OrganizationManager` class.
            session (AsyncSession): An instance of the `AsyncSession` class.
        Returns:
            None
        Raises:
            Exception: If the `delete` method does not raise an exception.
        """
        with pytest.raises(Exception):
            await organization_manager.delete("999")  # type: ignore
        await session.rollback()
    @pytest.mark.asyncio
    async def test_get_list(
        self,
        organization_manager: OrganizationManager,
        session: AsyncSession
    ):
        """
        Test case for the `get_list` method of the
        `OrganizationManager` class.
        This test verifies that the `get_list`
        method returns the correct list of organizations.
        Steps:
        1. Call the `get_list` method of the
            `organization_manager` instance.
        2. Assert that the returned list is empty.
        3. Create 5 organization objects using the
            `OrganizationFactory.create_async` method.
        4. Assert that the `organizations_data` variable is of type `List`.
        5. Call the `get_list` method of the
            `organization_manager` instance again.
        6. Assert that the returned list contains 5 organizations.
        7. Assert that all elements in the returned list are
            instances of the `Organization` class.
        """
        organizations = await organization_manager.get_list()
        assert len(organizations) == 0
        organizations_data = (
            [await OrganizationFactory.create_async(session) for _ in range(5)])
        assert isinstance(organizations_data, List)
        organizations = await organization_manager.get_list()
        assert len(organizations) == 5
        assert all(isinstance(
            organization, Organization) for organization in organizations)
    @pytest.mark.asyncio
    async def test_to_json(
        self,
        organization_manager: OrganizationManager,
        session: AsyncSession
    ):
        """
        Test the 'to_json' method of the OrganizationManager class.
        Args:
            organization_manager (OrganizationManager): An
                instance of the
                OrganizationManager class.
            session (AsyncSession): An instance of the AsyncSession class.
        Returns:
            None
        Raises:
            AssertionError: If the json_data is None.
        """
        organization = await OrganizationFactory.build_async(
            session)
        json_data = organization_manager.to_json(
            organization)
        assert json_data is not None
    @pytest.mark.asyncio
    async def test_to_dict(
        self,
        organization_manager: OrganizationManager,
        session: AsyncSession
    ):
        """
        Test the to_dict method of the OrganizationManager class.
        Args:
            organization_manager (OrganizationManager): An
                instance of the
                OrganizationManager class.
            session (AsyncSession): An instance of the AsyncSession class.
        Returns:
            None
        """
        organization = await OrganizationFactory.build_async(
            session)
        dict_data = organization_manager.to_dict(
            organization)
        assert dict_data is not None
    @pytest.mark.asyncio
    async def test_from_json(
        self,
        organization_manager: OrganizationManager,
        session: AsyncSession
    ):
        """
        Test the `from_json` method of the `OrganizationManager` class.
        This method tests the functionality of the
        `from_json` method of the `OrganizationManager` class.
        It creates a organization using
        the `OrganizationFactory`
        and converts it to JSON using the `to_json` method.
        Then, it deserializes the JSON data using the
        `from_json` method and asserts that the deserialized
        organization is an instance of the
        `Organization` class and has
        the same code as the original organization.
        Args:
            organization_manager (OrganizationManager): An
            instance of the
                `OrganizationManager` class.
            session (AsyncSession): An instance of the `AsyncSession` class.
        Returns:
            None
        """
        organization = await OrganizationFactory.create_async(
            session)
        json_data = organization_manager.to_json(
            organization)
        deserialized_organization = organization_manager.from_json(json_data)
        assert isinstance(deserialized_organization, Organization)
        assert deserialized_organization.code == \
            organization.code
    @pytest.mark.asyncio
    async def test_from_dict(
        self,
        organization_manager: OrganizationManager,
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
            organization_manager (OrganizationManager): An instance
                of the `OrganizationManager` class.
            session (AsyncSession): An instance of the `AsyncSession` class.
        Returns:
            None
        Raises:
            AssertionError: If any of the assertions fail.
        """
        organization = await OrganizationFactory.create_async(
            session)
        schema = OrganizationSchema()
        organization_data = schema.dump(organization)
        assert isinstance(organization_data, dict)
        deserialized_organization = organization_manager.from_dict(
            organization_data)
        assert isinstance(deserialized_organization, Organization)
        assert deserialized_organization.code == \
            organization.code
    @pytest.mark.asyncio
    async def test_add_bulk(
        self,
        organization_manager: OrganizationManager,
        session: AsyncSession
    ):
        """
        Test case for the `add_bulk` method of the
        `OrganizationManager` class.
        This test case verifies that the `add_bulk`
        method correctly adds multiple organizations to the database.
        Steps:
        1. Generate a list of organization data using the
            `OrganizationFactory.build_async` method.
        2. Call the `add_bulk` method of the
            `organization_manager` instance,
            passing in the
            generated organization data.
        3. Verify that the number of organizations
            returned is
            equal to the number of organizations added.
        4. For each updated organization, fetch the corresponding
            organization from the database.
        5. Verify that the fetched organization
            is an instance of the
            `Organization` class.
        6. Verify that the insert_user_id and
            last_update_user_id of the fetched
            organization match the
            customer code of the session context.
        7. Verify that the organization_id of the fetched
            organization matches the
            organization_id of the updated
            organization.
        """
        organizations_data = [
            await OrganizationFactory.build_async(session) for _ in range(5)]
        organizations = await organization_manager.add_bulk(
            organizations_data)
        assert len(organizations) == 5
        for updated_organization in organizations:
            result = await session.execute(
                select(Organization).filter(
                    Organization._organization_id == updated_organization.organization_id  # type: ignore
                )
            )
            fetched_organization = result.scalars().first()
            assert isinstance(fetched_organization, Organization)
            assert str(fetched_organization.insert_user_id) == (
                str(organization_manager._session_context.customer_code))
            assert str(fetched_organization.last_update_user_id) == (
                str(organization_manager._session_context.customer_code))
            assert fetched_organization.organization_id == \
                updated_organization.organization_id
    @pytest.mark.asyncio
    async def test_update_bulk_success(
        self,
        organization_manager: OrganizationManager,
        session: AsyncSession
    ):
        """
        Test case for bulk update of organizations.
        This test case verifies the functionality of the
        `update_bulk` method in the `OrganizationManager` class.
        It creates two organization instances,
        updates their codes
        using the `update_bulk` method, and then verifies
        that the updates were successful by checking the
        updated codes in the database.
        Steps:
        1. Create two organization instances using the
            `OrganizationFactory.create_async` method.
        2. Generate new codes for the organizations.
        3. Update the organizations' codes using the `update_bulk` method.
        4. Verify that the update was successful by checking
            the updated codes in the database.
        Args:
            organization_manager (OrganizationManager): An instance of the
                `OrganizationManager` class.
            session (AsyncSession): An instance of the `AsyncSession` class.
        Returns:
            None
        """
        # Mocking organization instances
        organization1 = await OrganizationFactory.create_async(
            session=session)
        organization2 = await OrganizationFactory.create_async(
            session=session)
        logging.info(organization1.__dict__)
        code_updated1 = uuid.uuid4()
        code_updated2 = uuid.uuid4()
        logging.info(code_updated1)
        logging.info(code_updated2)
        # Update organizations
        updates = [
            {
                "organization_id": organization1.organization_id,
                "code": code_updated1
            },
            {
                "organization_id": organization2.organization_id,
                "code": code_updated2
            }
        ]
        updated_organizations = await organization_manager.update_bulk(
            updates)
        logging.info('bulk update results')
        # Assertions
        assert len(updated_organizations) == 2
        logging.info(updated_organizations[0].__dict__)
        logging.info(updated_organizations[1].__dict__)
        logging.info('getall')
        organizations = await organization_manager.get_list()
        logging.info(organizations[0].__dict__)
        logging.info(organizations[1].__dict__)
        assert updated_organizations[0].code == code_updated1
        assert updated_organizations[1].code == code_updated2
        assert str(updated_organizations[0].last_update_user_id) == (
            str(organization_manager._session_context.customer_code))
        assert str(updated_organizations[1].last_update_user_id) == (
            str(organization_manager._session_context.customer_code))
        result = await session.execute(
            select(Organization).filter(
                Organization._organization_id == 1)  # type: ignore
        )
        fetched_organization = result.scalars().first()
        assert isinstance(fetched_organization, Organization)
        assert fetched_organization.code == code_updated1
        result = await session.execute(
            select(Organization).filter(
                Organization._organization_id == 2)  # type: ignore
        )
        fetched_organization = result.scalars().first()
        assert isinstance(fetched_organization, Organization)
        assert fetched_organization.code == code_updated2
    @pytest.mark.asyncio
    async def test_update_bulk_missing_organization_id(
        self,
        organization_manager: OrganizationManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of the `update_bulk`
        method when the organization_id is missing.
        This test case ensures that when the organization_id is
        missing in the updates list,
        an exception is raised and the session is rolled back.
        Steps:
        1. Prepare the updates list with a missing organization_id.
        2. Call the `update_bulk` method with the updates list.
        3. Assert that an exception is raised.
        4. Rollback the session to undo any changes made during the test.
        """
        # No organizations to update since organization_id is missing
        updates = [{"name": "Red Rose"}]
        with pytest.raises(Exception):
            await organization_manager.update_bulk(updates)
        await session.rollback()
    @pytest.mark.asyncio
    async def test_update_bulk_organization_not_found(
        self,
        organization_manager: OrganizationManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of the update_bulk
        method when a organization is not found.
        This test case performs the following steps:
        1. Defines a list of organization updates,
            where each update
            contains a organization_id and a code.
        2. Calls the update_bulk method of the
            organization_manager with the list of updates.
        3. Expects an exception to be raised, indicating that
            the organization was not found.
        4. Rolls back the session to undo any changes made during the test.
        Note: This test assumes that the update_bulk method
        throws an exception when a
        organization is not found.
        """
        # Update organizations
        updates = [{"organization_id": 1, "code": uuid.uuid4()}]
        with pytest.raises(Exception):
            await organization_manager.update_bulk(updates)
        await session.rollback()
    @pytest.mark.asyncio
    async def test_update_bulk_invalid_type(
        self,
        organization_manager: OrganizationManager,
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
        :param organization_manager: An instance of the OrganizationManager class.
        :param session: An instance of the AsyncSession class.
        """
        updates = [{"organization_id": "2", "code": uuid.uuid4()}]
        with pytest.raises(Exception):
            await organization_manager.update_bulk(updates)
        await session.rollback()
    @pytest.mark.asyncio
    async def test_delete_bulk_success(
        self,
        organization_manager: OrganizationManager,
        session: AsyncSession
    ):
        """
        Test case for the delete_bulk method of the
        OrganizationManager class.
        This test verifies that the delete_bulk method
        successfully deletes multiple organizations
        from the database.
        Steps:
        1. Create two organization objects
            using the OrganizationFactory.
        2. Delete the organizations using the
            delete_bulk method
            of the organization_manager.
        3. Verify that the delete operation was successful by
            checking if the organizations no longer exist in the database.
        Expected Result:
        - The delete_bulk method should return True, indicating
            that the delete operation was successful.
        - The organizations should no longer exist in the database.
        """
        organization1 = await OrganizationFactory.create_async(
            session=session)
        organization2 = await OrganizationFactory.create_async(
            session=session)
        # Delete organizations
        organization_ids = [organization1.organization_id, organization2.organization_id]
        result = await organization_manager.delete_bulk(
            organization_ids)
        assert result is True
        for organization_id in organization_ids:
            execute_result = await session.execute(
                select(Organization).filter(
                    Organization._organization_id == organization_id)  # type: ignore
            )
            fetched_organization = execute_result.scalars().first()
            assert fetched_organization is None
    @pytest.mark.asyncio
    async def test_delete_bulk_organizations_not_found(
        self,
        organization_manager: OrganizationManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of deleting bulk
        organizations when some organizations are not found.
        Steps:
        1. Create a organization using the
            OrganizationFactory.
        2. Assert that the created organization
            is an instance of the
            Organization class.
        3. Define a list of organization IDs to delete.
        4. Use pytest.raises to assert that an exception is
            raised when deleting the bulk organizations.
        5. Rollback the session to undo any changes made during the test.
        This test case ensures that the delete_bulk method of the
        OrganizationManager raises an exception
        when some organizations with the specified IDs are
        not found in the database.
        """
        organization1 = await OrganizationFactory.create_async(
            session=session)
        assert isinstance(organization1, Organization)
        # Delete organizations
        organization_ids = [1, 2]
        with pytest.raises(Exception):
            await organization_manager.delete_bulk(
                organization_ids)
        await session.rollback()
    @pytest.mark.asyncio
    async def test_delete_bulk_empty_list(
        self,
        organization_manager: OrganizationManager
    ):
        """
        Test case to verify the behavior of deleting
        organizations with an empty list.
        Args:
            organization_manager (OrganizationManager): The
                instance of the
                OrganizationManager class.
        Returns:
            None
        Raises:
            AssertionError: If the result is not True.
        """
        # Delete organizations with an empty list
        organization_ids = []
        result = await organization_manager.delete_bulk(
            organization_ids)
        # Assertions
        assert result is True
    @pytest.mark.asyncio
    async def test_delete_bulk_invalid_type(
        self,
        organization_manager: OrganizationManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of the delete_bulk
        method when invalid organization IDs are provided.
        Args:
            organization_manager (OrganizationManager): The
                instance of the
                OrganizationManager class.
            session (AsyncSession): The async session object.
        Raises:
            Exception: If an exception is raised during the
                execution of the delete_bulk method.
        Returns:
            None
        """
        organization_ids = ["1", 2]
        with pytest.raises(Exception):
            await organization_manager.delete_bulk(
                organization_ids)
        await session.rollback()
    @pytest.mark.asyncio
    async def test_count_basic_functionality(
        self,
        organization_manager: OrganizationManager,
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
        2. Call the count method of the organization_manager.
        3. Assert that the count is equal to 5.
        """
        organizations_data = (
            [await OrganizationFactory.create_async(session) for _ in range(5)])
        assert isinstance(organizations_data, List)
        count = await organization_manager.count()
        assert count == 5
    @pytest.mark.asyncio
    async def test_count_empty_database(
        self,
        organization_manager: OrganizationManager
    ):
        """
        Test the count method when the database is empty.
        This test case checks if the count method of the
        OrganizationManager class returns 0 when the database is empty.
        Args:
            organization_manager (OrganizationManager): An
                instance of the
                OrganizationManager class.
        Returns:
            None
        """
        count = await organization_manager.count()
        assert count == 0
    @pytest.mark.asyncio
    async def test_get_sorted_list_basic_sorting(
        self,
        organization_manager: OrganizationManager,
        session: AsyncSession
    ):
        """
        Test case for the 'get_sorted_list' method with basic sorting.
        This test case verifies that the 'get_sorted_list'
        method returns a list of organizations
        sorted by the '_organization_id' attribute in ascending order.
        Steps:
        1. Add organizations to the database.
        2. Call the 'get_sorted_list' method with the
            sort_by parameter set to '_organization_id'.
        3. Verify that the returned list of organizations is
            sorted by the '_organization_id' attribute.
        """
        # Add organizations
        organizations_data = (
            [await OrganizationFactory.create_async(session) for _ in range(5)])
        assert isinstance(organizations_data, List)
        sorted_organizations = await organization_manager.get_sorted_list(
            sort_by="_organization_id")
        assert [organization.organization_id for organization in sorted_organizations] == (
            [(i + 1) for i in range(5)])
    @pytest.mark.asyncio
    async def test_get_sorted_list_descending_sorting(
        self,
        organization_manager: OrganizationManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of the
        'get_sorted_list' method
        when sorting the list of organizations in descending order.
        Steps:
        1. Create a list of organizations using the OrganizationFactory.
        2. Assert that the organizations_data is of type List.
        3. Call the 'get_sorted_list' method with
            sort_by="organization_id" and order="desc".
        4. Assert that the organization_ids of the
            sorted_organizations are in descending order.
        """
        # Add organizations
        organizations_data = (
            [await OrganizationFactory.create_async(session) for _ in range(5)])
        assert isinstance(organizations_data, List)
        sorted_organizations = await organization_manager.get_sorted_list(
            sort_by="organization_id", order="desc")
        assert [organization.organization_id for organization in sorted_organizations] == (
            [(i + 1) for i in reversed(range(5))])
    @pytest.mark.asyncio
    async def test_get_sorted_list_invalid_attribute(
        self,
        organization_manager: OrganizationManager,
        session: AsyncSession
    ):
        """
        Test case to check if an AttributeError is raised when
        sorting the list by an invalid attribute.
        Args:
            organization_manager (OrganizationManager): The
                instance of the
                OrganizationManager class.
            session (AsyncSession): The instance of the AsyncSession class.
        Raises:
            AttributeError: If an invalid attribute is used for sorting.
        Returns:
            None
        """
        with pytest.raises(AttributeError):
            await organization_manager.get_sorted_list(
                sort_by="invalid_attribute")
        await session.rollback()
    @pytest.mark.asyncio
    async def test_get_sorted_list_empty_database(
        self,
        organization_manager: OrganizationManager
    ):
        """
        Test case to verify the behavior of
        `get_sorted_list` method when the database is empty.
        This test ensures that when the database is empty, the
        `get_sorted_list` method returns an empty list.
        Args:
            organization_manager (OrganizationManager): An
                instance of the
                OrganizationManager class.
        Returns:
            None
        """
        sorted_organizations = await organization_manager.get_sorted_list(
            sort_by="organization_id")
        assert len(sorted_organizations) == 0
    @pytest.mark.asyncio
    async def test_refresh_basic(
        self,
        organization_manager: OrganizationManager,
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
            organization_manager (OrganizationManager): The
                manager responsible
                for organization operations.
            session (AsyncSession): The SQLAlchemy asynchronous session.
        """
        # Add a organization
        organization1 = await OrganizationFactory.create_async(
            session=session)
        # Retrieve the organization from the database
        result = await session.execute(
            select(Organization).filter(
                Organization._organization_id == organization1.organization_id)  # type: ignore
        )  # type: ignore
        organization2 = result.scalars().first()
        # Verify that the retrieved organization
        # matches the added organization
        assert organization1.code == \
            organization2.code
        # Update the organization's code
        updated_code1 = uuid.uuid4()
        organization1.code = updated_code1
        updated_organization1 = await organization_manager.update(
            organization1)
        # Verify that the updated organization
        # is of type Organization
        # and has the updated code
        assert isinstance(updated_organization1, Organization)
        assert updated_organization1.code == updated_code1
        # Refresh the original organization instance
        refreshed_organization2 = await organization_manager.refresh(
            organization2)
        # Verify that the refreshed organization
        # reflects the updated code
        assert refreshed_organization2.code == updated_code1
    @pytest.mark.asyncio
    async def test_refresh_nonexistent_organization(
        self,
        organization_manager: OrganizationManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of refreshing a nonexistent organization.
        Args:
            organization_manager (OrganizationManager): The
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
            await organization_manager.refresh(
                organization)
        await session.rollback()
    @pytest.mark.asyncio
    async def test_exists_with_existing_organization(
        self,
        organization_manager: OrganizationManager,
        session: AsyncSession
    ):
        """
        Test case to check if a organization
        exists using the manager function.
        Args:
            organization_manager (OrganizationManager): The
                organization manager instance.
            session (AsyncSession): The async session object.
        Returns:
            None
        """
        # Add a organization
        organization1 = await OrganizationFactory.create_async(
            session=session)
        # Check if the organization exists
        # using the manager function
        assert await organization_manager.exists(
            organization1.organization_id) is True
    @pytest.mark.asyncio
    async def test_is_equal_with_existing_organization(
        self,
        organization_manager: OrganizationManager,
        session: AsyncSession
    ):
        """
        Test if the is_equal method of the
        OrganizationManager class correctly compares two organizations.
        Args:
            organization_manager (OrganizationManager): An
                instance of the
                OrganizationManager class.
            session (AsyncSession): An instance of the AsyncSession class.
        Returns:
            None
        """
        # Add a organization
        organization1 = await OrganizationFactory.create_async(
            session=session)
        organization2 = await organization_manager.get_by_id(
            organization_id=organization1.organization_id)
        assert organization_manager.is_equal(
            organization1, organization2) is True
        organization1_dict = organization_manager.to_dict(
            organization1)
        organization3 = organization_manager.from_dict(
            organization1_dict)
        assert organization_manager.is_equal(
            organization1, organization3) is True
    @pytest.mark.asyncio
    async def test_exists_with_nonexistent_organization(
        self,
        organization_manager: OrganizationManager
    ):
        """
        Test case to check if a organization with a
        non-existent ID exists in the database.
        Args:
            organization_manager (OrganizationManager): The
                instance of the OrganizationManager class.
        Returns:
            bool: True if the organization exists,
                False otherwise.
        """
        non_existent_id = 999
        assert await organization_manager.exists(non_existent_id) is False
    @pytest.mark.asyncio
    async def test_exists_with_invalid_id_type(
        self,
        organization_manager: OrganizationManager,
        session: AsyncSession
    ):
        """
        Test case to check if the exists method raises
        an exception when an invalid ID type is provided.
        Args:
            organization_manager (OrganizationManager): The instance
                of the OrganizationManager class.
            session (AsyncSession): The instance of the AsyncSession class.
        Raises:
            Exception: If an exception is not raised by the exists method.
        Returns:
            None
        """
        invalid_id = "invalid_id"
        with pytest.raises(Exception):
            await organization_manager.exists(invalid_id)  # type: ignore  # noqa: E501
        await session.rollback()
# endset
    # name,
    # TacID
    @pytest.mark.asyncio
    async def test_get_by_tac_id_existing(
        self,
        organization_manager: OrganizationManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of the
        `get_by_tac_id` method when
        a organization with
        a specific tac_id exists.
        Steps:
        1. Create a organization using the
            OrganizationFactory.
        2. Fetch the organization using the
            `get_by_tac_id` method of the organization_manager.
        3. Assert that the fetched organizations list contains
            only one organization.
        4. Assert that the fetched organization
            is an instance
            of the Organization class.
        5. Assert that the code of the fetched organization
            matches the code of the created organization.
        6. Fetch the corresponding tac object
            using the tac_id of the created organization.
        7. Assert that the fetched tac object is
            an instance of the Tac class.
        8. Assert that the tac_code_peek of the fetched
            organization matches the
            code of the fetched tac.
        """
        # Add a organization with a specific
        # tac_id
        organization1 = await OrganizationFactory.create_async(
            session=session)
        # Fetch the organization using
        # the manager function
        fetched_organizations = await organization_manager.get_by_tac_id(
            organization1.tac_id)
        assert len(fetched_organizations) == 1
        assert isinstance(fetched_organizations[0], Organization)
        assert fetched_organizations[0].code == \
            organization1.code
        stmt = select(models.Tac).where(
            models.Tac._tac_id == organization1.tac_id)  # type: ignore  # noqa: E501
        result = await session.execute(stmt)
        tac = result.scalars().first()
        assert isinstance(tac, models.Tac)
        assert fetched_organizations[0].tac_code_peek == tac.code
    @pytest.mark.asyncio
    async def test_get_by_tac_id_nonexistent(
        self,
        organization_manager: OrganizationManager
    ):
        """
        Test case to verify the behavior of the
        get_by_tac_id method when the tac ID does not exist.
        This test case ensures that when a non-existent
        tac ID is provided to the get_by_tac_id method,
        an empty list is returned.
        """
        non_existent_id = 999
        fetched_organizations = await organization_manager.get_by_tac_id(
            non_existent_id)
        assert len(fetched_organizations) == 0
    @pytest.mark.asyncio
    async def test_get_by_tac_id_invalid_type(
        self,
        organization_manager: OrganizationManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of the
        `get_by_tac_id` method when an invalid tac ID is provided.
        Args:
            organization_manager (OrganizationManager): An
                instance of the OrganizationManager class.
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
            await organization_manager.get_by_tac_id(
                invalid_id)  # type: ignore
        await session.rollback()
# endset
