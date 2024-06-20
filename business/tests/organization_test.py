# business/tests/organization_test.py
# pylint: disable=unused-import
"""
This module contains unit tests for the OrganizationBusObj class.
"""
from decimal import Decimal
import uuid
from datetime import datetime, date  # noqa: F401
from sqlalchemy.ext.asyncio import AsyncSession
import pytest
import pytest_asyncio
from helpers.session_context import SessionContext
from models import Organization
from models.factory import OrganizationFactory
from managers.organization import OrganizationManager
from business.organization import OrganizationBusObj
from services.logging_config import get_logger
import current_runtime  # noqa: F401

logger = get_logger(__name__)
class TestOrganizationBusObj:
    """
    Unit tests for the OrganizationBusObj class.
    """
    @pytest_asyncio.fixture(scope="function")
    async def organization_manager(self, session: AsyncSession):
        """
        Fixture that returns an instance of the OrganizationManager class.
        """
        session_context = SessionContext(dict(), session)
        return OrganizationManager(session_context)
    @pytest_asyncio.fixture(scope="function")
    async def organization_bus_obj(self, session):
        """
        Fixture that returns an instance of the OrganizationBusObj class.
        """
        session_context = SessionContext(dict(), session)
        return OrganizationBusObj(session_context)
    @pytest_asyncio.fixture(scope="function")
    async def new_organization(self, session):
        """
        Fixture that returns a new instance of the Organization class.
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
        Test case for creating a new organization.
        """
        # Test creating a new organization
        assert organization_bus_obj.organization_id == 0
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
        Test case for loading data from a organization object instance.
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
        Test case for loading data from a organization ID.
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
        Test case for loading data from a organization code.
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
        Test case for loading data from a organization JSON.
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
        Test case for loading data from a organization dictionary.
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
        Test case for retrieving a nonexistent organization.
        """
        # Test retrieving a nonexistent organization raises an exception
        await organization_bus_obj.load_from_id(-1)
        # Assuming -1 is an id that wouldn't exist
        assert organization_bus_obj.is_valid() is False
    @pytest.mark.asyncio
    async def test_update_organization(
        self,
        organization_manager: OrganizationManager,
        organization_bus_obj: OrganizationBusObj,
        new_organization: Organization
    ):
        """
        Test case for updating a organization's data.
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
        Test case for deleting a organization.
        """
        assert new_organization.organization_id is not None
        assert organization_bus_obj.organization_id == 0
        new_organization_organization_id_value = new_organization.organization_id
        await organization_bus_obj.load_from_id(new_organization_organization_id_value)
        assert organization_bus_obj.organization_id is not None
        await organization_bus_obj.delete()
        new_organization_organization_id_value = new_organization.organization_id
        new_organization = await organization_manager.get_by_id(new_organization_organization_id_value)
        assert new_organization is None

