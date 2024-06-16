# models/managers/tests/organization_test.py
"""
    #TODO add comment
"""
import logging
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
    #TODO add comment
    """
    @pytest_asyncio.fixture(scope="function")
    async def organization_manager(self, session: AsyncSession):
        """
            #TODO add comment
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
            #TODO add comment
        """
        # Define mock data for our organization
        mock_data = {
            "code": uuid.uuid4()
        }
        # Call the build function of the manager
        organization = await organization_manager.build(**mock_data)
        # Assert that the returned object is an instance of Organization
        assert isinstance(organization, Organization)
        # Assert that the attributes of the organization match our mock data
        assert organization.code == mock_data["code"]
    @pytest.mark.asyncio
    async def test_build_with_missing_data(
        self,
        organization_manager: OrganizationManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        # Define mock data with a missing key
        mock_data = {
            "non_existant_property": "Rose"
        }
        # If the build method is expected to raise an exception for missing data, test for that
        with pytest.raises(Exception):
            await organization_manager.build_async(**mock_data)
        await session.rollback()
    @pytest.mark.asyncio
    async def test_add_correctly_adds_organization_to_database(
        self,
        organization_manager: OrganizationManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        test_organization = await OrganizationFactory.build_async(session)
        assert test_organization.organization_id is None
        # Add the organization using the manager's add method
        added_organization = await organization_manager.add(organization=test_organization)
        assert isinstance(added_organization, Organization)
        assert str(added_organization.insert_user_id) == (
            str(organization_manager._session_context.customer_code))
        assert str(added_organization.last_update_user_id) == (
            str(organization_manager._session_context.customer_code))
        assert added_organization.organization_id > 0
        # Fetch the organization from the database directly
        result = await session.execute(
            select(Organization).filter(Organization.organization_id == added_organization.organization_id))
        fetched_organization = result.scalars().first()
        # Assert that the fetched organization is not None and matches the added organization
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
            #TODO add comment
        """
        # Create a test organization using the OrganizationFactory without persisting it to the database
        test_organization = await OrganizationFactory.build_async(session)
        assert test_organization.organization_id is None
        test_organization.code = uuid.uuid4()
        # Add the organization using the manager's add method
        added_organization = await organization_manager.add(organization=test_organization)
        assert isinstance(added_organization, Organization)
        assert str(added_organization.insert_user_id) == (
            str(organization_manager._session_context.customer_code))
        assert str(added_organization.last_update_user_id) == (
            str(organization_manager._session_context.customer_code))
        assert added_organization.organization_id > 0
        # Assert that the returned organization matches the test organization
        assert added_organization.organization_id == test_organization.organization_id
        assert added_organization.code == test_organization.code
    @pytest.mark.asyncio
    async def test_get_by_id(
        self,
        organization_manager: OrganizationManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        test_organization = await OrganizationFactory.create_async(session)
        organization = await organization_manager.get_by_id(test_organization.organization_id)
        assert isinstance(organization, Organization)
        assert test_organization.organization_id == organization.organization_id
        assert test_organization.code == organization.code
    @pytest.mark.asyncio
    async def test_get_by_id_not_found(
        self,
        organization_manager: OrganizationManager
    ):
        """
            #TODO add comment
        """
        non_existent_id = 9999  # An ID that's not in the database
        retrieved_organization = await organization_manager.get_by_id(non_existent_id)
        assert retrieved_organization is None
    @pytest.mark.asyncio
    async def test_get_by_code_returns_organization(
        self,
        organization_manager: OrganizationManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        test_organization = await OrganizationFactory.create_async(session)
        organization = await organization_manager.get_by_code(test_organization.code)
        assert isinstance(organization, Organization)
        assert test_organization.organization_id == organization.organization_id
        assert test_organization.code == organization.code
    @pytest.mark.asyncio
    async def test_get_by_code_returns_none_for_nonexistent_code(
        self,
        organization_manager: OrganizationManager
    ):
        """
            #TODO add comment
        """
        # Generate a random UUID that doesn't correspond to
        # any Organization in the database
        random_code = uuid.uuid4()
        organization = await organization_manager.get_by_code(random_code)
        assert organization is None
    @pytest.mark.asyncio
    async def test_update(
        self,
        organization_manager: OrganizationManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        test_organization = await OrganizationFactory.create_async(session)
        test_organization.code = uuid.uuid4()
        updated_organization = await organization_manager.update(organization=test_organization)
        assert isinstance(updated_organization, Organization)
        assert str(updated_organization.last_update_user_id) == str(
            organization_manager._session_context.customer_code)
        assert updated_organization.organization_id == test_organization.organization_id
        assert updated_organization.code == test_organization.code
        result = await session.execute(
            select(Organization).filter(
                Organization.organization_id == test_organization.organization_id)
        )
        fetched_organization = result.scalars().first()
        assert updated_organization.organization_id == fetched_organization.organization_id
        assert updated_organization.code == fetched_organization.code
        assert test_organization.organization_id == fetched_organization.organization_id
        assert test_organization.code == fetched_organization.code
    @pytest.mark.asyncio
    async def test_update_via_dict(
        self,
        organization_manager: OrganizationManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        test_organization = await OrganizationFactory.create_async(session)
        new_code = uuid.uuid4()
        updated_organization = await organization_manager.update(
            organization=test_organization,
            code=new_code
        )
        assert isinstance(updated_organization, Organization)
        assert str(updated_organization.last_update_user_id) == str(
            organization_manager._session_context.customer_code
        )
        assert updated_organization.organization_id == test_organization.organization_id
        assert updated_organization.code == new_code
        result = await session.execute(
            select(Organization).filter(
                Organization.organization_id == test_organization.organization_id)
        )
        fetched_organization = result.scalars().first()
        assert updated_organization.organization_id == fetched_organization.organization_id
        assert updated_organization.code == fetched_organization.code
        assert test_organization.organization_id == fetched_organization.organization_id
        assert new_code == fetched_organization.code
    @pytest.mark.asyncio
    async def test_update_invalid_organization(self, organization_manager: OrganizationManager):
        """
            #TODO add comment
        """
        # None organization
        organization = None
        new_code = uuid.uuid4()
        updated_organization = await organization_manager.update(organization, code=new_code)
        # Assertions
        assert updated_organization is None
    @pytest.mark.asyncio
    async def test_update_with_nonexistent_attribute(
        self,
        organization_manager: OrganizationManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        test_organization = await OrganizationFactory.create_async(session)
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
            #TODO add comment
        """
        organization_data = await OrganizationFactory.create_async(session)
        result = await session.execute(
            select(Organization).filter(Organization.organization_id == organization_data.organization_id))
        fetched_organization = result.scalars().first()
        assert isinstance(fetched_organization, Organization)
        assert fetched_organization.organization_id == organization_data.organization_id
        deleted_organization = await organization_manager.delete(
            organization_id=organization_data.organization_id)
        result = await session.execute(
            select(Organization).filter(Organization.organization_id == organization_data.organization_id))
        fetched_organization = result.scalars().first()
        assert fetched_organization is None
    @pytest.mark.asyncio
    async def test_delete_nonexistent(
        self,
        organization_manager: OrganizationManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
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
            #TODO add comment
        """
        with pytest.raises(Exception):
            await organization_manager.delete("999")
        await session.rollback()
    @pytest.mark.asyncio
    async def test_get_list(
        self,
        organization_manager: OrganizationManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        organizations = await organization_manager.get_list()
        assert len(organizations) == 0
        organizations_data = (
            [await OrganizationFactory.create_async(session) for _ in range(5)])
        organizations = await organization_manager.get_list()
        assert len(organizations) == 5
        assert all(isinstance(organization, Organization) for organization in organizations)
    @pytest.mark.asyncio
    async def test_to_json(
        self,
        organization_manager: OrganizationManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        organization = await OrganizationFactory.build_async(session)
        json_data = organization_manager.to_json(organization)
        assert json_data is not None
    @pytest.mark.asyncio
    async def test_to_dict(
        self,
        organization_manager: OrganizationManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        organization = await OrganizationFactory.build_async(session)
        dict_data = organization_manager.to_dict(organization)
        assert dict_data is not None
    @pytest.mark.asyncio
    async def test_from_json(
        self,
        organization_manager: OrganizationManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        organization = await OrganizationFactory.create_async(session)
        json_data = organization_manager.to_json(organization)
        deserialized_organization = organization_manager.from_json(json_data)
        assert isinstance(deserialized_organization, Organization)
        assert deserialized_organization.code == organization.code
    @pytest.mark.asyncio
    async def test_from_dict(
        self,
        organization_manager: OrganizationManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        organization = await OrganizationFactory.create_async(session)
        schema = OrganizationSchema()
        organization_data = schema.dump(organization)
        deserialized_organization = organization_manager.from_dict(organization_data)
        assert isinstance(deserialized_organization, Organization)
        assert deserialized_organization.code == organization.code
    @pytest.mark.asyncio
    async def test_add_bulk(
        self,
        organization_manager: OrganizationManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        organizations_data = [await OrganizationFactory.build_async(session) for _ in range(5)]
        organizations = await organization_manager.add_bulk(organizations_data)
        assert len(organizations) == 5
        for updated_organization in organizations:
            result = await session.execute(
                select(Organization).filter(
                    Organization.organization_id == updated_organization.organization_id
                )
            )
            fetched_organization = result.scalars().first()
            assert isinstance(fetched_organization, Organization)
            assert str(fetched_organization.insert_user_id) == (
                str(organization_manager._session_context.customer_code))
            assert str(fetched_organization.last_update_user_id) == (
                str(organization_manager._session_context.customer_code))
            assert fetched_organization.organization_id == updated_organization.organization_id
    @pytest.mark.asyncio
    async def test_update_bulk_success(
        self,
        organization_manager: OrganizationManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        # Mocking organization instances
        organization1 = await OrganizationFactory.create_async(session=session)
        organization2 = await OrganizationFactory.create_async(session=session)
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
        updated_organizations = await organization_manager.update_bulk(updates)
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
            select(Organization).filter(Organization.organization_id == 1)
        )
        fetched_organization = result.scalars().first()
        assert isinstance(fetched_organization, Organization)
        assert fetched_organization.code == code_updated1
        result = await session.execute(
            select(Organization).filter(Organization.organization_id == 2)
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
            #TODO add comment
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
            #TODO add comment
        """
        # Update organizations
        updates = [{"organization_id": 1, "code": uuid.uuid4()}]
        with pytest.raises(Exception):
            updated_organizations = await organization_manager.update_bulk(updates)
        await session.rollback()
    @pytest.mark.asyncio
    async def test_update_bulk_invalid_type(
        self,
        organization_manager: OrganizationManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
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
            #TODO add comment
        """
        organization1 = await OrganizationFactory.create_async(session=session)
        organization2 = await OrganizationFactory.create_async(session=session)
        # Delete organizations
        organization_ids = [organization1.organization_id, organization2.organization_id]
        result = await organization_manager.delete_bulk(organization_ids)
        assert result is True
        for organization_id in organization_ids:
            execute_result = await session.execute(
                select(Organization).filter(Organization.organization_id == organization_id))
            fetched_organization = execute_result.scalars().first()
            assert fetched_organization is None
    @pytest.mark.asyncio
    async def test_delete_bulk_organizations_not_found(
        self,
        organization_manager: OrganizationManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        organization1 = await OrganizationFactory.create_async(session=session)
        # Delete organizations
        organization_ids = [1, 2]
        with pytest.raises(Exception):
            await organization_manager.delete_bulk(organization_ids)
        await session.rollback()
    @pytest.mark.asyncio
    async def test_delete_bulk_empty_list(
        self,
        organization_manager: OrganizationManager
    ):
        """
            #TODO add comment
        """
        # Delete organizations with an empty list
        organization_ids = []
        result = await organization_manager.delete_bulk(organization_ids)
        # Assertions
        assert result is True
    @pytest.mark.asyncio
    async def test_delete_bulk_invalid_type(
        self,
        organization_manager: OrganizationManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        organization_ids = ["1", 2]
        with pytest.raises(Exception):
            await organization_manager.delete_bulk(organization_ids)
        await session.rollback()
    @pytest.mark.asyncio
    async def test_count_basic_functionality(
        self,
        organization_manager: OrganizationManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        organizations_data = (
            [await OrganizationFactory.create_async(session) for _ in range(5)])
        count = await organization_manager.count()
        assert count == 5
    @pytest.mark.asyncio
    async def test_count_empty_database(
        self,
        organization_manager: OrganizationManager
    ):
        """
            #TODO add comment
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
            #TODO add comment
        """
        # Add organizations
        organizations_data = (
            [await OrganizationFactory.create_async(session) for _ in range(5)])
        sorted_organizations = await organization_manager.get_sorted_list(sort_by="organization_id")
        assert [organization.organization_id for organization in sorted_organizations] == (
            [(i + 1) for i in range(5)])
    @pytest.mark.asyncio
    async def test_get_sorted_list_descending_sorting(
        self,
        organization_manager: OrganizationManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        # Add organizations
        organizations_data = (
            [await OrganizationFactory.create_async(session) for _ in range(5)])
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
            #TODO add comment
        """
        with pytest.raises(AttributeError):
            await organization_manager.get_sorted_list(sort_by="invalid_attribute")
        await session.rollback()
    @pytest.mark.asyncio
    async def test_get_sorted_list_empty_database(
        self,
        organization_manager: OrganizationManager
    ):
        """
            #TODO add comment
        """
        sorted_organizations = await organization_manager.get_sorted_list(sort_by="organization_id")
        assert len(sorted_organizations) == 0
    @pytest.mark.asyncio
    async def test_refresh_basic(
        self,
        organization_manager: OrganizationManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        # Add a organization
        organization1 = await OrganizationFactory.create_async(session=session)
        result = await session.execute(select(Organization).filter(Organization.organization_id == organization1.organization_id))
        organization2 = result.scalars().first()
        assert organization1.code == organization2.code
        updated_code1 = uuid.uuid4()
        organization1.code = updated_code1
        updated_organization1 = await organization_manager.update(organization1)
        assert updated_organization1.code == updated_code1
        refreshed_organization2 = await organization_manager.refresh(organization2)
        assert refreshed_organization2.code == updated_code1
    @pytest.mark.asyncio
    async def test_refresh_nonexistent_organization(
        self,
        organization_manager: OrganizationManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        organization = Organization(organization_id=999)
        with pytest.raises(Exception):
            await organization_manager.refresh(organization)
        await session.rollback()
    @pytest.mark.asyncio
    async def test_exists_with_existing_organization(
        self,
        organization_manager: OrganizationManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        # Add a organization
        organization1 = await OrganizationFactory.create_async(session=session)
        # Check if the organization exists using the manager function
        assert await organization_manager.exists(organization1.organization_id) is True
    @pytest.mark.asyncio
    async def test_is_equal_with_existing_organization(
        self,
        organization_manager: OrganizationManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        # Add a organization
        organization1 = await OrganizationFactory.create_async(session=session)
        organization2 = await organization_manager.get_by_id(organization_id=organization1.organization_id)
        assert organization_manager.is_equal(organization1, organization2) is True
        organization1_dict = organization_manager.to_dict(organization1)
        organization3 = organization_manager.from_dict(organization1_dict)
        assert organization_manager.is_equal(organization1, organization3) is True
    @pytest.mark.asyncio
    async def test_exists_with_nonexistent_organization(
        self,
        organization_manager: OrganizationManager
    ):
        """
            #TODO add comment
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
            #TODO add comment
        """
        invalid_id = "invalid_id"
        with pytest.raises(Exception):
            await organization_manager.exists(invalid_id)
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
            #TODO add comment
        """
        # Add a organization with a specific tac_id
        organization1 = await OrganizationFactory.create_async(session=session)
        # Fetch the organization using the manager function
        fetched_organizations = await organization_manager.get_by_tac_id(organization1.tac_id)
        assert len(fetched_organizations) == 1
        assert isinstance(fetched_organizations[0], Organization)
        assert fetched_organizations[0].code == organization1.code
    @pytest.mark.asyncio
    async def test_get_by_tac_id_nonexistent(
        self,
        organization_manager: OrganizationManager
    ):
        """
            #TODO add comment
        """
        non_existent_id = 999
        fetched_organizations = await organization_manager.get_by_tac_id(non_existent_id)
        assert len(fetched_organizations) == 0
    @pytest.mark.asyncio
    async def test_get_by_tac_id_invalid_type(
        self,
        organization_manager: OrganizationManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        invalid_id = "invalid_id"
        with pytest.raises(Exception):
            await organization_manager.get_by_tac_id(invalid_id)
        await session.rollback()
# endset
