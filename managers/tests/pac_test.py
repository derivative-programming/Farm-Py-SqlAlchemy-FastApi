import uuid
import pytest
import factory
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from models.factory import PacFactory
from managers.pac import PacManager
from models.pac import Base
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
async def pac_manager(async_session):
    return PacManager(async_session)
@pytest.mark.asyncio
async def test_add(pac_manager):
    pac_data = factory.build(dict, FACTORY_CLASS=PacFactory)
    added_pac = await pac_manager.add(**pac_data)
    assert added_pac
    assert added_pac.id
@pytest.mark.asyncio
async def test_get_by_id(pac_manager):
    pac_data = factory.build(dict, FACTORY_CLASS=PacFactory)
    added_pac = await pac_manager.add(**pac_data)
    fetched_pac = await pac_manager.get_by_id(added_pac.id)
    assert fetched_pac.id == added_pac.id
@pytest.mark.asyncio
async def test_get_by_code(pac_manager):
    pac_data = factory.build(dict, FACTORY_CLASS=PacFactory)
    await pac_manager.add(**pac_data)
    fetched_pac = await pac_manager.get_by_code(pac_data["code"])
    assert fetched_pac.code == pac_data["code"]
@pytest.mark.asyncio
async def test_update(pac_manager):
    pac_data = factory.build(dict, FACTORY_CLASS=PacFactory)
    added_pac = await pac_manager.add(**pac_data)
    new_code = uuid.uuid4()  # Generate a new UUID
    await pac_manager.update(added_pac.id, code=new_code)
    fetched_pac = await pac_manager.get_by_id(added_pac.id)
    assert fetched_pac.code == new_code
@pytest.mark.asyncio
async def test_delete(pac_manager):
    pac_data = factory.build(dict, FACTORY_CLASS=PacFactory)
    added_pac = await pac_manager.add(**pac_data)
    await pac_manager.delete(added_pac.id)
    fetched_pac = await pac_manager.get_by_id(added_pac.id)
    assert not fetched_pac
@pytest.mark.asyncio
async def test_get_list(pac_manager):
    for _ in range(5):
        pac_data = factory.build(dict, FACTORY_CLASS=PacFactory)
        await pac_manager.add(**pac_data)
    pacs = await pac_manager.get_list()
    assert len(pacs) == 5
#_id
@pytest.mark.asyncio
async def test_get_by__id(pac_manager):
    _id = 123  # Replace with a valid  ID from your system, perhaps created using a Factory
    pac_data = factory.build(dict, FACTORY_CLASS=PacFactory, _id=_id)
    await pac_manager.add(**pac_data)
    pacs = await pac_manager.get_by__id(_id)
    assert len(pacs) == 1
#flvr_foreign_key_id
@pytest.mark.asyncio
async def test_get_by_flvr_foreign_key_id(pac_manager):
    flvr_foreign_key_id = 456  # Replace with a valid flavor ID from your system, perhaps created using a FlavorFactory
    pac_data = factory.build(dict, FACTORY_CLASS=PacFactory, flvr_foreign_key_id=flvr_foreign_key_id)
    await pac_manager.add(**pac_data)
    pacs = await pac_manager.get_by_flvr_foreign_key_id(flvr_foreign_key_id)
    assert len(pacs) == 1
#endset
