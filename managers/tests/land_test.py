import uuid
import pytest
import factory
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from models.factory import LandFactory
from managers.land import LandManager
from models.land import Base

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
async def land_manager(async_session):
    return LandManager(async_session)

@pytest.mark.asyncio
async def test_add(land_manager):
    land_data = factory.build(dict, FACTORY_CLASS=LandFactory)
    added_land = await land_manager.add(**land_data)

    assert added_land
    assert added_land.land_id

@pytest.mark.asyncio
async def test_get_by_id(land_manager):
    land_data = factory.build(dict, FACTORY_CLASS=LandFactory)
    added_land = await land_manager.add(**land_data)

    fetched_land = await land_manager.get_by_id(added_land.land_id)
    assert fetched_land.land_id == added_land.land_id

@pytest.mark.asyncio
async def test_get_by_code(land_manager):
    land_data = factory.build(dict, FACTORY_CLASS=LandFactory)
    await land_manager.add(**land_data)

    fetched_land = await land_manager.get_by_code(land_data["code"])
    assert fetched_land.code == land_data["code"]

@pytest.mark.asyncio
async def test_update(land_manager):
    land_data = factory.build(dict, FACTORY_CLASS=LandFactory)
    added_land = await land_manager.add(**land_data)
    new_code = uuid.uuid4()  # Generate a new UUID
    await land_manager.update(added_land.land_id, code=new_code)

    fetched_land = await land_manager.get_by_id(added_land.land_id)
    assert fetched_land.code == new_code

@pytest.mark.asyncio
async def test_delete(land_manager):
    land_data = factory.build(dict, FACTORY_CLASS=LandFactory)
    added_land = await land_manager.add(**land_data)

    await land_manager.delete(added_land.land_id)
    fetched_land = await land_manager.get_by_id(added_land.land_id)
    assert not fetched_land

@pytest.mark.asyncio
async def test_get_list(land_manager):
    for _ in range(5):
        land_data = factory.build(dict, FACTORY_CLASS=LandFactory)
        await land_manager.add(**land_data)

    lands = await land_manager.get_list()
    assert len(lands) == 5

#pac_id
@pytest.mark.asyncio
async def test_get_by_pac_id(land_manager):
    pac_id = 123  # Replace with a valid pac ID from your system, perhaps created using a PacFactory
    land_data = factory.build(dict, FACTORY_CLASS=LandFactory, pac_id=pac_id)
    await land_manager.add(**land_data)

    lands = await land_manager.get_by_pac_id(pac_id)
    assert len(lands) == 1

#flvr_foreign_key_id
@pytest.mark.asyncio
async def test_get_by_flvr_foreign_key_id(land_manager):
    flvr_foreign_key_id = 456  # Replace with a valid flavor ID from your system, perhaps created using a FlavorFactory
    land_data = factory.build(dict, FACTORY_CLASS=LandFactory, flvr_foreign_key_id=flvr_foreign_key_id)
    await land_manager.add(**land_data)

    lands = await land_manager.get_by_flvr_foreign_key_id(flvr_foreign_key_id)
    assert len(lands) == 1

