import uuid
import pytest
import factory
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker 
from models.factory import PlantFactory
from managers.plant import PlantManager
from models.plant import Base

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
async def plant_manager(async_session):
    return PlantManager(async_session)

@pytest.mark.asyncio
async def test_add(plant_manager):
    plant_data = factory.build(dict, FACTORY_CLASS=PlantFactory)
    added_plant = await plant_manager.add(**plant_data)
    
    assert added_plant
    assert added_plant.id

@pytest.mark.asyncio
async def test_get_by_id(plant_manager):
    plant_data = factory.build(dict, FACTORY_CLASS=PlantFactory)
    added_plant = await plant_manager.add(**plant_data)

    fetched_plant = await plant_manager.get_by_id(added_plant.id)
    assert fetched_plant.id == added_plant.id

@pytest.mark.asyncio
async def test_get_by_code(plant_manager):
    plant_data = factory.build(dict, FACTORY_CLASS=PlantFactory)
    await plant_manager.add(**plant_data)
    
    fetched_plant = await plant_manager.get_by_code(plant_data["code"])
    assert fetched_plant.code == plant_data["code"]

@pytest.mark.asyncio
async def test_update(plant_manager):
    plant_data = factory.build(dict, FACTORY_CLASS=PlantFactory)
    added_plant = await plant_manager.add(**plant_data)
    new_code = uuid.uuid4()  # Generate a new UUID
    await plant_manager.update(added_plant.id, code=new_code)
    
    fetched_plant = await plant_manager.get_by_id(added_plant.id)
    assert fetched_plant.code == new_code

@pytest.mark.asyncio
async def test_delete(plant_manager):
    plant_data = factory.build(dict, FACTORY_CLASS=PlantFactory)
    added_plant = await plant_manager.add(**plant_data)

    await plant_manager.delete(added_plant.id)
    fetched_plant = await plant_manager.get_by_id(added_plant.id)
    assert not fetched_plant

@pytest.mark.asyncio
async def test_get_list(plant_manager):
    for _ in range(5):
        plant_data = factory.build(dict, FACTORY_CLASS=PlantFactory)
        await plant_manager.add(**plant_data)
    
    plants = await plant_manager.get_list()
    assert len(plants) == 5

#land_id
@pytest.mark.asyncio
async def test_get_by_land_id(plant_manager):
    land_id = 123  # Replace with a valid land ID from your system, perhaps created using a LandFactory
    plant_data = factory.build(dict, FACTORY_CLASS=PlantFactory, land_id=land_id)
    await plant_manager.add(**plant_data)

    plants = await plant_manager.get_by_land_id(land_id)
    assert len(plants) == 1

#flvr_foreign_key_id
@pytest.mark.asyncio
async def test_get_by_flvr_foreign_key_id(plant_manager):
    flvr_foreign_key_id = 456  # Replace with a valid flavor ID from your system, perhaps created using a FlavorFactory
    plant_data = factory.build(dict, FACTORY_CLASS=PlantFactory, flvr_foreign_key_id=flvr_foreign_key_id)
    await plant_manager.add(**plant_data)

    plants = await plant_manager.get_by_flvr_foreign_key_id(flvr_foreign_key_id)
    assert len(plants) == 1

#endset
