import uuid
import pytest
import factory
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from models.factory import OrgApiKeyFactory
from managers.org_api_key import OrgApiKeyManager
from models.org_api_key import Base
DATABASE_URL = "sqlite+aiosqlite:///:memory:"  # in-memory SQLite database for testing
@pytest.fixture(scope='module')
async def db_engine():
    engine = create_async_engine(DATABASE_URL, echo=True)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    await engine.dispose()
@pytest.fixture
async def async_session(db_engine):
    SessionLocal = sessionmaker(
        bind=db_engine, class_=AsyncSession, expire_on_commit=False
    )
    async with SessionLocal() as session:
        yield session
@pytest.fixture
async def org_api_key_manager(async_session):
    return OrgApiKeyManager(async_session)
@pytest.mark.asyncio
async def test_add(org_api_key_manager):
    org_api_key_data = factory.build(dict, FACTORY_CLASS=OrgApiKeyFactory)
    added_org_api_key = await org_api_key_manager.add(**org_api_key_data)
    assert added_org_api_key
    assert added_org_api_key.id
@pytest.mark.asyncio
async def test_get_by_id(org_api_key_manager):
    org_api_key_data = factory.build(dict, FACTORY_CLASS=OrgApiKeyFactory)
    added_org_api_key = await org_api_key_manager.add(**org_api_key_data)
    fetched_org_api_key = await org_api_key_manager.get_by_id(added_org_api_key.id)
    assert fetched_org_api_key.id == added_org_api_key.id
@pytest.mark.asyncio
async def test_get_by_code(org_api_key_manager):
    org_api_key_data = factory.build(dict, FACTORY_CLASS=OrgApiKeyFactory)
    await org_api_key_manager.add(**org_api_key_data)
    fetched_org_api_key = await org_api_key_manager.get_by_code(org_api_key_data["code"])
    assert fetched_org_api_key.code == org_api_key_data["code"]
@pytest.mark.asyncio
async def test_update(org_api_key_manager):
    org_api_key_data = factory.build(dict, FACTORY_CLASS=OrgApiKeyFactory)
    added_org_api_key = await org_api_key_manager.add(**org_api_key_data)
    new_code = uuid.uuid4()  # Generate a new UUID
    await org_api_key_manager.update(added_org_api_key.id, code=new_code)
    fetched_org_api_key = await org_api_key_manager.get_by_id(added_org_api_key.id)
    assert fetched_org_api_key.code == new_code
@pytest.mark.asyncio
async def test_delete(org_api_key_manager):
    org_api_key_data = factory.build(dict, FACTORY_CLASS=OrgApiKeyFactory)
    added_org_api_key = await org_api_key_manager.add(**org_api_key_data)
    await org_api_key_manager.delete(added_org_api_key.id)
    fetched_org_api_key = await org_api_key_manager.get_by_id(added_org_api_key.id)
    assert not fetched_org_api_key
@pytest.mark.asyncio
async def test_get_list(org_api_key_manager):
    for _ in range(5):
        org_api_key_data = factory.build(dict, FACTORY_CLASS=OrgApiKeyFactory)
        await org_api_key_manager.add(**org_api_key_data)
    org_api_keys = await org_api_key_manager.get_list()
    assert len(org_api_keys) == 5
#organization_id
@pytest.mark.asyncio
async def test_get_by_organization_id(org_api_key_manager):
    organization_id = 123  # Replace with a valid organization ID from your system, perhaps created using a OrganizationFactory
    org_api_key_data = factory.build(dict, FACTORY_CLASS=OrgApiKeyFactory, organization_id=organization_id)
    await org_api_key_manager.add(**org_api_key_data)
    org_api_keys = await org_api_key_manager.get_by_organization_id(organization_id)
    assert len(org_api_keys) == 1
#flvr_foreign_key_id
@pytest.mark.asyncio
async def test_get_by_flvr_foreign_key_id(org_api_key_manager):
    flvr_foreign_key_id = 456  # Replace with a valid flavor ID from your system, perhaps created using a FlavorFactory
    org_api_key_data = factory.build(dict, FACTORY_CLASS=OrgApiKeyFactory, flvr_foreign_key_id=flvr_foreign_key_id)
    await org_api_key_manager.add(**org_api_key_data)
    org_api_keys = await org_api_key_manager.get_by_flvr_foreign_key_id(flvr_foreign_key_id)
    assert len(org_api_keys) == 1
#endset
