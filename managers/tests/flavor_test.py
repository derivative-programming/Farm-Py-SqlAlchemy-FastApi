import uuid
import pytest
import factory
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from models.factory import FlavorFactory
from managers.flavor import FlavorManager
from models.flavor import Base

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
async def flavor_manager(async_session):
    return FlavorManager(async_session)

@pytest.mark.asyncio
async def test_add(flavor_manager):
    flavor_data = factory.build(dict, FACTORY_CLASS=FlavorFactory)
    added_flavor = await flavor_manager.add(**flavor_data)

    assert added_flavor
    assert added_flavor.flavor_id

@pytest.mark.asyncio
async def test_get_by_id(flavor_manager):
    flavor_data = factory.build(dict, FACTORY_CLASS=FlavorFactory)
    added_flavor = await flavor_manager.add(**flavor_data)

    fetched_flavor = await flavor_manager.get_by_id(added_flavor.flavor_id)
    assert fetched_flavor.flavor_id == added_flavor.flavor_id

@pytest.mark.asyncio
async def test_get_by_code(flavor_manager):
    flavor_data = factory.build(dict, FACTORY_CLASS=FlavorFactory)
    await flavor_manager.add(**flavor_data)

    fetched_flavor = await flavor_manager.get_by_code(flavor_data["code"])
    assert fetched_flavor.code == flavor_data["code"]

@pytest.mark.asyncio
async def test_update(flavor_manager):
    flavor_data = factory.build(dict, FACTORY_CLASS=FlavorFactory)
    added_flavor = await flavor_manager.add(**flavor_data)
    new_code = uuid.uuid4()  # Generate a new UUID
    await flavor_manager.update(added_flavor.flavor_id, code=new_code)

    fetched_flavor = await flavor_manager.get_by_id(added_flavor.flavor_id)
    assert fetched_flavor.code == new_code

@pytest.mark.asyncio
async def test_delete(flavor_manager):
    flavor_data = factory.build(dict, FACTORY_CLASS=FlavorFactory)
    added_flavor = await flavor_manager.add(**flavor_data)

    await flavor_manager.delete(added_flavor.flavor_id)
    fetched_flavor = await flavor_manager.get_by_id(added_flavor.flavor_id)
    assert not fetched_flavor

@pytest.mark.asyncio
async def test_get_list(flavor_manager):
    for _ in range(5):
        flavor_data = factory.build(dict, FACTORY_CLASS=FlavorFactory)
        await flavor_manager.add(**flavor_data)

    flavors = await flavor_manager.get_list()
    assert len(flavors) == 5

#pac_id
@pytest.mark.asyncio
async def test_get_by_pac_id(flavor_manager):
    pac_id = 123  # Replace with a valid pac ID from your system, perhaps created using a PacFactory
    flavor_data = factory.build(dict, FACTORY_CLASS=FlavorFactory, pac_id=pac_id)
    await flavor_manager.add(**flavor_data)

    flavors = await flavor_manager.get_by_pac_id(pac_id)
    assert len(flavors) == 1

#flvr_foreign_key_id
@pytest.mark.asyncio
async def test_get_by_flvr_foreign_key_id(flavor_manager):
    flvr_foreign_key_id = 456  # Replace with a valid flavor ID from your system, perhaps created using a FlavorFactory
    flavor_data = factory.build(dict, FACTORY_CLASS=FlavorFactory, flvr_foreign_key_id=flvr_foreign_key_id)
    await flavor_manager.add(**flavor_data)

    flavors = await flavor_manager.get_by_flvr_foreign_key_id(flvr_foreign_key_id)
    assert len(flavors) == 1

