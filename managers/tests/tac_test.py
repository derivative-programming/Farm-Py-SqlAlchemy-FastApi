import uuid
import pytest
import factory
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from models.factory import TacFactory
from managers.tac import TacManager
from models.tac import Base
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
async def tac_manager(async_session):
    return TacManager(async_session)
@pytest.mark.asyncio
async def test_add(tac_manager):
    tac_data = factory.build(dict, FACTORY_CLASS=TacFactory)
    added_tac = await tac_manager.add(**tac_data)
    assert added_tac
    assert added_tac.id
@pytest.mark.asyncio
async def test_get_by_id(tac_manager):
    tac_data = factory.build(dict, FACTORY_CLASS=TacFactory)
    added_tac = await tac_manager.add(**tac_data)
    fetched_tac = await tac_manager.get_by_id(added_tac.id)
    assert fetched_tac.id == added_tac.id
@pytest.mark.asyncio
async def test_get_by_code(tac_manager):
    tac_data = factory.build(dict, FACTORY_CLASS=TacFactory)
    await tac_manager.add(**tac_data)
    fetched_tac = await tac_manager.get_by_code(tac_data["code"])
    assert fetched_tac.code == tac_data["code"]
@pytest.mark.asyncio
async def test_update(tac_manager):
    tac_data = factory.build(dict, FACTORY_CLASS=TacFactory)
    added_tac = await tac_manager.add(**tac_data)
    new_code = uuid.uuid4()  # Generate a new UUID
    await tac_manager.update(added_tac.id, code=new_code)
    fetched_tac = await tac_manager.get_by_id(added_tac.id)
    assert fetched_tac.code == new_code
@pytest.mark.asyncio
async def test_delete(tac_manager):
    tac_data = factory.build(dict, FACTORY_CLASS=TacFactory)
    added_tac = await tac_manager.add(**tac_data)
    await tac_manager.delete(added_tac.id)
    fetched_tac = await tac_manager.get_by_id(added_tac.id)
    assert not fetched_tac
@pytest.mark.asyncio
async def test_get_list(tac_manager):
    for _ in range(5):
        tac_data = factory.build(dict, FACTORY_CLASS=TacFactory)
        await tac_manager.add(**tac_data)
    tacs = await tac_manager.get_list()
    assert len(tacs) == 5
#pac_id
@pytest.mark.asyncio
async def test_get_by_pac_id(tac_manager):
    pac_id = 123  # Replace with a valid pac ID from your system, perhaps created using a PacFactory
    tac_data = factory.build(dict, FACTORY_CLASS=TacFactory, pac_id=pac_id)
    await tac_manager.add(**tac_data)
    tacs = await tac_manager.get_by_pac_id(pac_id)
    assert len(tacs) == 1
#flvr_foreign_key_id
@pytest.mark.asyncio
async def test_get_by_flvr_foreign_key_id(tac_manager):
    flvr_foreign_key_id = 456  # Replace with a valid flavor ID from your system, perhaps created using a FlavorFactory
    tac_data = factory.build(dict, FACTORY_CLASS=TacFactory, flvr_foreign_key_id=flvr_foreign_key_id)
    await tac_manager.add(**tac_data)
    tacs = await tac_manager.get_by_flvr_foreign_key_id(flvr_foreign_key_id)
    assert len(tacs) == 1
#endset
