import uuid
import pytest
import factory
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from models.factory import TriStateFilterFactory
from managers.tri_state_filter import TriStateFilterManager
from models.tri_state_filter import Base

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
async def tri_state_filter_manager(async_session):
    return TriStateFilterManager(async_session)

@pytest.mark.asyncio
async def test_add(tri_state_filter_manager):
    tri_state_filter_data = factory.build(dict, FACTORY_CLASS=TriStateFilterFactory)
    added_tri_state_filter = await tri_state_filter_manager.add(**tri_state_filter_data)

    assert added_tri_state_filter
    assert added_tri_state_filter.tri_state_filter_id

@pytest.mark.asyncio
async def test_get_by_id(tri_state_filter_manager):
    tri_state_filter_data = factory.build(dict, FACTORY_CLASS=TriStateFilterFactory)
    added_tri_state_filter = await tri_state_filter_manager.add(**tri_state_filter_data)

    fetched_tri_state_filter = await tri_state_filter_manager.get_by_id(added_tri_state_filter.tri_state_filter_id)
    assert fetched_tri_state_filter.tri_state_filter_id == added_tri_state_filter.tri_state_filter_id

@pytest.mark.asyncio
async def test_get_by_code(tri_state_filter_manager):
    tri_state_filter_data = factory.build(dict, FACTORY_CLASS=TriStateFilterFactory)
    await tri_state_filter_manager.add(**tri_state_filter_data)

    fetched_tri_state_filter = await tri_state_filter_manager.get_by_code(tri_state_filter_data["code"])
    assert fetched_tri_state_filter.code == tri_state_filter_data["code"]

@pytest.mark.asyncio
async def test_update(tri_state_filter_manager):
    tri_state_filter_data = factory.build(dict, FACTORY_CLASS=TriStateFilterFactory)
    added_tri_state_filter = await tri_state_filter_manager.add(**tri_state_filter_data)
    new_code = uuid.uuid4()  # Generate a new UUID
    await tri_state_filter_manager.update(added_tri_state_filter.tri_state_filter_id, code=new_code)

    fetched_tri_state_filter = await tri_state_filter_manager.get_by_id(added_tri_state_filter.tri_state_filter_id)
    assert fetched_tri_state_filter.code == new_code

@pytest.mark.asyncio
async def test_delete(tri_state_filter_manager):
    tri_state_filter_data = factory.build(dict, FACTORY_CLASS=TriStateFilterFactory)
    added_tri_state_filter = await tri_state_filter_manager.add(**tri_state_filter_data)

    await tri_state_filter_manager.delete(added_tri_state_filter.tri_state_filter_id)
    fetched_tri_state_filter = await tri_state_filter_manager.get_by_id(added_tri_state_filter.tri_state_filter_id)
    assert not fetched_tri_state_filter

@pytest.mark.asyncio
async def test_get_list(tri_state_filter_manager):
    for _ in range(5):
        tri_state_filter_data = factory.build(dict, FACTORY_CLASS=TriStateFilterFactory)
        await tri_state_filter_manager.add(**tri_state_filter_data)

    tri_state_filters = await tri_state_filter_manager.get_list()
    assert len(tri_state_filters) == 5

#pac_id
@pytest.mark.asyncio
async def test_get_by_pac_id(tri_state_filter_manager):
    pac_id = 123  # Replace with a valid pac ID from your system, perhaps created using a PacFactory
    tri_state_filter_data = factory.build(dict, FACTORY_CLASS=TriStateFilterFactory, pac_id=pac_id)
    await tri_state_filter_manager.add(**tri_state_filter_data)

    tri_state_filters = await tri_state_filter_manager.get_by_pac_id(pac_id)
    assert len(tri_state_filters) == 1

#flvr_foreign_key_id
@pytest.mark.asyncio
async def test_get_by_flvr_foreign_key_id(tri_state_filter_manager):
    flvr_foreign_key_id = 456  # Replace with a valid flavor ID from your system, perhaps created using a FlavorFactory
    tri_state_filter_data = factory.build(dict, FACTORY_CLASS=TriStateFilterFactory, flvr_foreign_key_id=flvr_foreign_key_id)
    await tri_state_filter_manager.add(**tri_state_filter_data)

    tri_state_filters = await tri_state_filter_manager.get_by_flvr_foreign_key_id(flvr_foreign_key_id)
    assert len(tri_state_filters) == 1

