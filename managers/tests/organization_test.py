import uuid
import pytest
import factory
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from models.factory import OrganizationFactory
from managers.organization import OrganizationManager
from models.organization import Base

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
async def organization_manager(async_session):
    return OrganizationManager(async_session)

@pytest.mark.asyncio
async def test_add(organization_manager):
    organization_data = factory.build(dict, FACTORY_CLASS=OrganizationFactory)
    added_organization = await organization_manager.add(**organization_data)

    assert added_organization
    assert added_organization.organization_id

@pytest.mark.asyncio
async def test_get_by_id(organization_manager):
    organization_data = factory.build(dict, FACTORY_CLASS=OrganizationFactory)
    added_organization = await organization_manager.add(**organization_data)

    fetched_organization = await organization_manager.get_by_id(added_organization.organization_id)
    assert fetched_organization.organization_id == added_organization.organization_id

@pytest.mark.asyncio
async def test_get_by_code(organization_manager):
    organization_data = factory.build(dict, FACTORY_CLASS=OrganizationFactory)
    await organization_manager.add(**organization_data)

    fetched_organization = await organization_manager.get_by_code(organization_data["code"])
    assert fetched_organization.code == organization_data["code"]

@pytest.mark.asyncio
async def test_update(organization_manager):
    organization_data = factory.build(dict, FACTORY_CLASS=OrganizationFactory)
    added_organization = await organization_manager.add(**organization_data)
    new_code = uuid.uuid4()  # Generate a new UUID
    await organization_manager.update(added_organization.organization_id, code=new_code)

    fetched_organization = await organization_manager.get_by_id(added_organization.organization_id)
    assert fetched_organization.code == new_code

@pytest.mark.asyncio
async def test_delete(organization_manager):
    organization_data = factory.build(dict, FACTORY_CLASS=OrganizationFactory)
    added_organization = await organization_manager.add(**organization_data)

    await organization_manager.delete(added_organization.organization_id)
    fetched_organization = await organization_manager.get_by_id(added_organization.organization_id)
    assert not fetched_organization

@pytest.mark.asyncio
async def test_get_list(organization_manager):
    for _ in range(5):
        organization_data = factory.build(dict, FACTORY_CLASS=OrganizationFactory)
        await organization_manager.add(**organization_data)

    organizations = await organization_manager.get_list()
    assert len(organizations) == 5

#tac_id
@pytest.mark.asyncio
async def test_get_by_tac_id(organization_manager):
    tac_id = 123  # Replace with a valid tac ID from your system, perhaps created using a TacFactory
    organization_data = factory.build(dict, FACTORY_CLASS=OrganizationFactory, tac_id=tac_id)
    await organization_manager.add(**organization_data)

    organizations = await organization_manager.get_by_tac_id(tac_id)
    assert len(organizations) == 1

#flvr_foreign_key_id
@pytest.mark.asyncio
async def test_get_by_flvr_foreign_key_id(organization_manager):
    flvr_foreign_key_id = 456  # Replace with a valid flavor ID from your system, perhaps created using a FlavorFactory
    organization_data = factory.build(dict, FACTORY_CLASS=OrganizationFactory, flvr_foreign_key_id=flvr_foreign_key_id)
    await organization_manager.add(**organization_data)

    organizations = await organization_manager.get_by_flvr_foreign_key_id(flvr_foreign_key_id)
    assert len(organizations) == 1

