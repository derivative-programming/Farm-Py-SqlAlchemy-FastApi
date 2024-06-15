# business/tests/organization_test.py
"""
    #TODO add comment
"""
import uuid
from datetime import datetime, date  # pylint: disable=unused-import
from sqlalchemy.ext.asyncio import AsyncSession
import pytest
import pytest_asyncio
from helpers.session_context import SessionContext
from models import Organization
from models.factory import OrganizationFactory
from managers.organization import OrganizationManager
from business.organization import OrganizationBusObj
from services.logging_config import get_logger
import current_runtime  # pylint: disable=unused-import

logger = get_logger(__name__)
class TestOrganizationBusObj:
    """
        #TODO add comment
    """
    @pytest_asyncio.fixture(scope="function")
    async def organization_manager(self, session: AsyncSession):
        """
            #TODO add comment
        """
        session_context = SessionContext(dict(), session)
        return OrganizationManager(session_context)
    @pytest_asyncio.fixture(scope="function")
    async def organization_bus_obj(self, session):
        """
            #TODO add comment
        """
        session_context = SessionContext(dict(), session)
        return OrganizationBusObj(session_context)
    @pytest_asyncio.fixture(scope="function")
    async def new_organization(self, session):
        """
            #TODO add comment
        """
        # Use the OrganizationFactory to create a new organization instance
        # Assuming OrganizationFactory.create() is an async function
        return await OrganizationFactory.create_async(session)
    @pytest.mark.asyncio
    async def test_create_organization(
        self,
        organization_bus_obj: OrganizationBusObj
    ):
        """
            #TODO add comment
        """
        # Test creating a new organization
        assert organization_bus_obj.organization_id is None
        # assert isinstance(organization_bus_obj.organization_id, int)
        assert isinstance(organization_bus_obj.code, uuid.UUID)
        assert isinstance(organization_bus_obj.last_change_code, int)
        assert organization_bus_obj.insert_user_id == uuid.UUID(int=0)
        assert organization_bus_obj.last_update_user_id == uuid.UUID(int=0)
        assert isinstance(organization_bus_obj.name, str)
        assert isinstance(organization_bus_obj.tac_id, int)
    @pytest.mark.asyncio
    async def test_load_with_organization_obj(
        self,
        organization_manager: OrganizationManager,
        organization_bus_obj: OrganizationBusObj,
        new_organization: Organization
    ):
        """
            #TODO add comment
        """
        await organization_bus_obj.load_from_obj_instance(new_organization)
        assert organization_manager.is_equal(organization_bus_obj.organization, new_organization) is True
    @pytest.mark.asyncio
    async def test_load_with_organization_id(
        self,
        organization_manager: OrganizationManager,
        organization_bus_obj: OrganizationBusObj,
        new_organization: Organization
    ):
        """
            #TODO add comment
        """
        new_organization_organization_id = new_organization.organization_id
        await organization_bus_obj.load_from_id(new_organization_organization_id)
        assert organization_manager.is_equal(organization_bus_obj.organization, new_organization) is True
    @pytest.mark.asyncio
    async def test_load_with_organization_code(
        self,
        organization_manager: OrganizationManager,
        organization_bus_obj: OrganizationBusObj,
        new_organization: Organization
    ):
        """
            #TODO add comment
        """
        await organization_bus_obj.load_from_code(new_organization.code)
        assert organization_manager.is_equal(organization_bus_obj.organization, new_organization) is True
    @pytest.mark.asyncio
    async def test_load_with_organization_json(
        self,
        organization_manager: OrganizationManager,
        organization_bus_obj: OrganizationBusObj,
        new_organization: Organization
    ):
        """
            #TODO add comment
        """
        organization_json = organization_manager.to_json(new_organization)
        await organization_bus_obj.load_from_json(organization_json)
        assert organization_manager.is_equal(organization_bus_obj.organization, new_organization) is True
    @pytest.mark.asyncio
    async def test_load_with_organization_dict(
        self,
        organization_manager: OrganizationManager,
        organization_bus_obj: OrganizationBusObj,
        new_organization: Organization
    ):
        """
            #TODO add comment
        """
        logger.info("test_load_with_organization_dict 1")
        organization_dict = organization_manager.to_dict(new_organization)
        logger.info(organization_dict)
        await organization_bus_obj.load_from_dict(organization_dict)
        assert organization_manager.is_equal(
            organization_bus_obj.organization,
            new_organization) is True
    @pytest.mark.asyncio
    async def test_get_nonexistent_organization(
        self,
        organization_bus_obj: OrganizationBusObj
    ):
        """
            #TODO add comment
        """
        # Test retrieving a nonexistent organization raises an exception
        await organization_bus_obj.load_from_id(-1)
        assert organization_bus_obj.is_valid() is False  # Assuming -1 is an id that wouldn't exist
    @pytest.mark.asyncio
    async def test_update_organization(
        self,
        organization_manager: OrganizationManager,
        organization_bus_obj: OrganizationBusObj,
        new_organization: Organization
    ):
        """
            #TODO add comment
        """
        # Test updating a organization's data
        new_organization_organization_id_value = new_organization.organization_id
        new_organization = await organization_manager.get_by_id(new_organization_organization_id_value)
        assert isinstance(new_organization, Organization)
        new_code = uuid.uuid4()
        await organization_bus_obj.load_from_obj_instance(new_organization)
        organization_bus_obj.code = new_code
        await organization_bus_obj.save()
        new_organization_organization_id_value = new_organization.organization_id
        new_organization = await organization_manager.get_by_id(new_organization_organization_id_value)
        assert organization_manager.is_equal(
            organization_bus_obj.organization,
            new_organization) is True
    @pytest.mark.asyncio
    async def test_delete_organization(
        self,
        organization_manager: OrganizationManager,
        organization_bus_obj: OrganizationBusObj,
        new_organization: Organization
    ):
        """
            #TODO add comment
        """
        assert new_organization.organization_id is not None
        assert organization_bus_obj.organization_id is None
        new_organization_organization_id_value = new_organization.organization_id
        await organization_bus_obj.load_from_id(new_organization_organization_id_value)
        assert organization_bus_obj.organization_id is not None
        await organization_bus_obj.delete()
        new_organization_organization_id_value = new_organization.organization_id
        new_organization = await organization_manager.get_by_id(new_organization_organization_id_value)
        assert new_organization is None

