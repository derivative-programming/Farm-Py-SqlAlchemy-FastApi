import uuid
import pytest
import factory
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from models.factory import OrgCustomerFactory
from managers.org_customer import OrgCustomerManager
from models.org_customer import Base

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
async def org_customer_manager(async_session):
    return OrgCustomerManager(async_session)

@pytest.mark.asyncio
async def test_add(org_customer_manager):
    org_customer_data = factory.build(dict, FACTORY_CLASS=OrgCustomerFactory)
    added_org_customer = await org_customer_manager.add(**org_customer_data)

    assert added_org_customer
    assert added_org_customer.org_customer_id

@pytest.mark.asyncio
async def test_get_by_id(org_customer_manager):
    org_customer_data = factory.build(dict, FACTORY_CLASS=OrgCustomerFactory)
    added_org_customer = await org_customer_manager.add(**org_customer_data)

    fetched_org_customer = await org_customer_manager.get_by_id(added_org_customer.org_customer_id)
    assert fetched_org_customer.org_customer_id == added_org_customer.org_customer_id

@pytest.mark.asyncio
async def test_get_by_code(org_customer_manager):
    org_customer_data = factory.build(dict, FACTORY_CLASS=OrgCustomerFactory)
    await org_customer_manager.add(**org_customer_data)

    fetched_org_customer = await org_customer_manager.get_by_code(org_customer_data["code"])
    assert fetched_org_customer.code == org_customer_data["code"]

@pytest.mark.asyncio
async def test_update(org_customer_manager):
    org_customer_data = factory.build(dict, FACTORY_CLASS=OrgCustomerFactory)
    added_org_customer = await org_customer_manager.add(**org_customer_data)
    new_code = uuid.uuid4()  # Generate a new UUID
    await org_customer_manager.update(added_org_customer.org_customer_id, code=new_code)

    fetched_org_customer = await org_customer_manager.get_by_id(added_org_customer.org_customer_id)
    assert fetched_org_customer.code == new_code

@pytest.mark.asyncio
async def test_delete(org_customer_manager):
    org_customer_data = factory.build(dict, FACTORY_CLASS=OrgCustomerFactory)
    added_org_customer = await org_customer_manager.add(**org_customer_data)

    await org_customer_manager.delete(added_org_customer.org_customer_id)
    fetched_org_customer = await org_customer_manager.get_by_id(added_org_customer.org_customer_id)
    assert not fetched_org_customer

@pytest.mark.asyncio
async def test_get_list(org_customer_manager):
    for _ in range(5):
        org_customer_data = factory.build(dict, FACTORY_CLASS=OrgCustomerFactory)
        await org_customer_manager.add(**org_customer_data)

    org_customers = await org_customer_manager.get_list()
    assert len(org_customers) == 5

#organization_id
@pytest.mark.asyncio
async def test_get_by_organization_id(org_customer_manager):
    organization_id = 123  # Replace with a valid organization ID from your system, perhaps created using a OrganizationFactory
    org_customer_data = factory.build(dict, FACTORY_CLASS=OrgCustomerFactory, organization_id=organization_id)
    await org_customer_manager.add(**org_customer_data)

    org_customers = await org_customer_manager.get_by_organization_id(organization_id)
    assert len(org_customers) == 1

#flvr_foreign_key_id
@pytest.mark.asyncio
async def test_get_by_flvr_foreign_key_id(org_customer_manager):
    flvr_foreign_key_id = 456  # Replace with a valid flavor ID from your system, perhaps created using a FlavorFactory
    org_customer_data = factory.build(dict, FACTORY_CLASS=OrgCustomerFactory, flvr_foreign_key_id=flvr_foreign_key_id)
    await org_customer_manager.add(**org_customer_data)

    org_customers = await org_customer_manager.get_by_flvr_foreign_key_id(flvr_foreign_key_id)
    assert len(org_customers) == 1

