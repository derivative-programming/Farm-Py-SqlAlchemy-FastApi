import pytest
import pytest_asyncio
from datetime import datetime, date
from sqlalchemy.ext.asyncio import AsyncSession
from models import Organization
from models.factory import OrganizationFactory
from managers.organization import OrganizationManager
from business.organization import OrganizationBusObj
from services.db_config import db_dialect
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
from services.db_config import db_dialect,generate_uuid
from sqlalchemy import String
from services.logging_config import get_logger
import managers as managers_and_enums
import current_runtime

logger = get_logger(__name__)
db_dialect = "sqlite"
# Conditionally set the UUID column type
if db_dialect == 'postgresql':
    UUIDType = UUID(as_uuid=True)
elif db_dialect == 'mssql':
    UUIDType = UNIQUEIDENTIFIER
else:  # This will cover SQLite, MySQL, and other databases
    UUIDType = String(36)
class TestOrganizationBusObj:
    @pytest_asyncio.fixture(scope="function")
    async def organization_manager(self, session:AsyncSession):
        return OrganizationManager(session)
    @pytest_asyncio.fixture(scope="function")
    async def organization_bus_obj(self, session):
        # Assuming that the OrganizationBusObj requires a session object
        return OrganizationBusObj(session)
    @pytest_asyncio.fixture(scope="function")
    async def new_organization(self, session):
        # Use the OrganizationFactory to create a new organization instance
        # Assuming OrganizationFactory.create() is an async function
        return await OrganizationFactory.create_async(session)
    @pytest.mark.asyncio
    async def test_create_organization(self, organization_manager:OrganizationManager, organization_bus_obj:OrganizationBusObj, new_organization:Organization):
        # Test creating a new organization
        assert organization_bus_obj.organization_id is None
        # assert isinstance(organization_bus_obj.organization_id, int)
        if db_dialect == 'postgresql':
            assert isinstance(organization_bus_obj.code, UUID)
        elif db_dialect == 'mssql':
            assert isinstance(organization_bus_obj.code, UNIQUEIDENTIFIER)
        else:  # This will cover SQLite, MySQL, and other databases
            assert isinstance(organization_bus_obj.code, str)
        assert isinstance(organization_bus_obj.last_change_code, int)
        assert organization_bus_obj.insert_user_id is None
        assert organization_bus_obj.last_update_user_id is None
        assert organization_bus_obj.name == "" or isinstance(organization_bus_obj.name, str)
        assert isinstance(organization_bus_obj.tac_id, int)
    @pytest.mark.asyncio
    async def test_load_with_organization_obj(self, organization_manager:OrganizationManager, organization_bus_obj:OrganizationBusObj, new_organization:Organization):
        await organization_bus_obj.load(organization_obj_instance=new_organization)
        assert organization_manager.is_equal(organization_bus_obj.organization,new_organization) == True
    @pytest.mark.asyncio
    async def test_load_with_organization_id(self, organization_manager:OrganizationManager, organization_bus_obj:OrganizationBusObj, new_organization:Organization):
        await organization_bus_obj.load(organization_id=new_organization.organization_id)
        assert organization_manager.is_equal(organization_bus_obj.organization,new_organization)  == True
    @pytest.mark.asyncio
    async def test_load_with_organization_code(self, organization_manager:OrganizationManager, organization_bus_obj:OrganizationBusObj, new_organization:Organization):
        await organization_bus_obj.load(code=new_organization.code)
        assert organization_manager.is_equal(organization_bus_obj.organization,new_organization)  == True
    @pytest.mark.asyncio
    async def test_load_with_organization_json(self, organization_manager:OrganizationManager, organization_bus_obj:OrganizationBusObj, new_organization:Organization):
        organization_json = organization_manager.to_json(new_organization)
        await organization_bus_obj.load(json_data=organization_json)
        assert organization_manager.is_equal(organization_bus_obj.organization,new_organization)  == True
    @pytest.mark.asyncio
    async def test_load_with_organization_dict(self, session, organization_manager:OrganizationManager, organization_bus_obj:OrganizationBusObj, new_organization:Organization):
        logger.info("test_load_with_organization_dict 1")
        organization_dict = organization_manager.to_dict(new_organization)
        logger.info(organization_dict)
        await organization_bus_obj.load(organization_dict=organization_dict)
        assert organization_manager.is_equal(organization_bus_obj.organization,new_organization)  == True
    @pytest.mark.asyncio
    async def test_get_nonexistent_organization(self, organization_manager:OrganizationManager, organization_bus_obj:OrganizationBusObj, new_organization:Organization):
        # Test retrieving a nonexistent organization raises an exception
        assert await organization_bus_obj.load(organization_id=-1) is None # Assuming -1 is an id that wouldn't exist
    @pytest.mark.asyncio
    async def test_update_organization(self, organization_manager:OrganizationManager, organization_bus_obj:OrganizationBusObj, new_organization:Organization):
        # Test updating a organization's data
        new_organization = await organization_manager.get_by_id(new_organization.organization_id)
        new_code = generate_uuid()
        await organization_bus_obj.load(organization_obj_instance=new_organization)
        organization_bus_obj.code = new_code
        await organization_bus_obj.save()
        new_organization = await organization_manager.get_by_id(new_organization.organization_id)
        assert organization_manager.is_equal(organization_bus_obj.organization,new_organization)  == True
    @pytest.mark.asyncio
    async def test_delete_organization(self, organization_manager:OrganizationManager, organization_bus_obj:OrganizationBusObj, new_organization:Organization):
        assert new_organization.organization_id is not None
        assert organization_bus_obj.organization_id is None
        await organization_bus_obj.load(organization_id=new_organization.organization_id)
        assert organization_bus_obj.organization_id is not None
        await organization_bus_obj.delete()
        new_organization = await organization_manager.get_by_id(new_organization.organization_id)
        assert new_organization is None

    @pytest.mark.asyncio
    async def test_build_org_customer(self, organization_manager:OrganizationManager, organization_bus_obj:OrganizationBusObj, new_organization:Organization):

        await current_runtime.initialize(session=organization_manager.session)

        await organization_bus_obj.load(organization_id=new_organization.organization_id)

        org_customer_bus_obj = await organization_bus_obj.build_org_customer()

        assert org_customer_bus_obj.organization_id == organization_bus_obj.organization_id
        assert org_customer_bus_obj.organization_code_peek == organization_bus_obj.code

        await org_customer_bus_obj.save()

        assert org_customer_bus_obj.org_customer_id > 0

    @pytest.mark.asyncio
    async def test_get_all_org_customer(self, organization_manager:OrganizationManager, organization_bus_obj:OrganizationBusObj, new_organization:Organization):

        await current_runtime.initialize(session=organization_manager.session)

        await organization_bus_obj.load(organization_id=new_organization.organization_id)

        org_customer_bus_obj = await organization_bus_obj.build_org_customer()

        await org_customer_bus_obj.save()

        org_customer_list = await organization_bus_obj.get_all_org_customer()

        assert len(org_customer_list) >= 1

        #assert org_customer_list[0].org_customer_id > 0

        #assert org_customer_list[0].org_customer_id == org_customer_bus_obj.org_customer_id

    @pytest.mark.asyncio
    async def test_build_org_api_key(self, organization_manager:OrganizationManager, organization_bus_obj:OrganizationBusObj, new_organization:Organization):

        await current_runtime.initialize(session=organization_manager.session)

        await organization_bus_obj.load(organization_id=new_organization.organization_id)

        org_api_key_bus_obj = await organization_bus_obj.build_org_api_key()

        assert org_api_key_bus_obj.organization_id == organization_bus_obj.organization_id
        assert org_api_key_bus_obj.organization_code_peek == organization_bus_obj.code

        await org_api_key_bus_obj.save()

        assert org_api_key_bus_obj.org_api_key_id > 0

    @pytest.mark.asyncio
    async def test_get_all_org_api_key(self, organization_manager:OrganizationManager, organization_bus_obj:OrganizationBusObj, new_organization:Organization):

        await current_runtime.initialize(session=organization_manager.session)

        await organization_bus_obj.load(organization_id=new_organization.organization_id)

        org_api_key_bus_obj = await organization_bus_obj.build_org_api_key()

        await org_api_key_bus_obj.save()

        org_api_key_list = await organization_bus_obj.get_all_org_api_key()

        assert len(org_api_key_list) >= 1

        #assert org_api_key_list[0].org_api_key_id > 0

        #assert org_api_key_list[0].org_api_key_id == org_api_key_bus_obj.org_api_key_id

