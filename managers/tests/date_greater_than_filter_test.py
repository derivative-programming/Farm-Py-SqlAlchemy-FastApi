import uuid
import pytest
import factory
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from models.factory import DateGreaterThanFilterFactory
from managers.date_greater_than_filter import DateGreaterThanFilterManager
from models.date_greater_than_filter import Base

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
async def date_greater_than_filter_manager(async_session):
    return DateGreaterThanFilterManager(async_session)

@pytest.mark.asyncio
async def test_add(date_greater_than_filter_manager):
    date_greater_than_filter_data = factory.build(dict, FACTORY_CLASS=DateGreaterThanFilterFactory)
    added_date_greater_than_filter = await date_greater_than_filter_manager.add(**date_greater_than_filter_data)

    assert added_date_greater_than_filter
    assert added_date_greater_than_filter.date_greater_than_filter_id

@pytest.mark.asyncio
async def test_get_by_id(date_greater_than_filter_manager):
    date_greater_than_filter_data = factory.build(dict, FACTORY_CLASS=DateGreaterThanFilterFactory)
    added_date_greater_than_filter = await date_greater_than_filter_manager.add(**date_greater_than_filter_data)

    fetched_date_greater_than_filter = await date_greater_than_filter_manager.get_by_id(added_date_greater_than_filter.date_greater_than_filter_id)
    assert fetched_date_greater_than_filter.date_greater_than_filter_id == added_date_greater_than_filter.date_greater_than_filter_id

@pytest.mark.asyncio
async def test_get_by_code(date_greater_than_filter_manager):
    date_greater_than_filter_data = factory.build(dict, FACTORY_CLASS=DateGreaterThanFilterFactory)
    await date_greater_than_filter_manager.add(**date_greater_than_filter_data)

    fetched_date_greater_than_filter = await date_greater_than_filter_manager.get_by_code(date_greater_than_filter_data["code"])
    assert fetched_date_greater_than_filter.code == date_greater_than_filter_data["code"]

@pytest.mark.asyncio
async def test_update(date_greater_than_filter_manager):
    date_greater_than_filter_data = factory.build(dict, FACTORY_CLASS=DateGreaterThanFilterFactory)
    added_date_greater_than_filter = await date_greater_than_filter_manager.add(**date_greater_than_filter_data)
    new_code = uuid.uuid4()  # Generate a new UUID
    await date_greater_than_filter_manager.update(added_date_greater_than_filter.date_greater_than_filter_id, code=new_code)

    fetched_date_greater_than_filter = await date_greater_than_filter_manager.get_by_id(added_date_greater_than_filter.date_greater_than_filter_id)
    assert fetched_date_greater_than_filter.code == new_code

@pytest.mark.asyncio
async def test_delete(date_greater_than_filter_manager):
    date_greater_than_filter_data = factory.build(dict, FACTORY_CLASS=DateGreaterThanFilterFactory)
    added_date_greater_than_filter = await date_greater_than_filter_manager.add(**date_greater_than_filter_data)

    await date_greater_than_filter_manager.delete(added_date_greater_than_filter.date_greater_than_filter_id)
    fetched_date_greater_than_filter = await date_greater_than_filter_manager.get_by_id(added_date_greater_than_filter.date_greater_than_filter_id)
    assert not fetched_date_greater_than_filter

@pytest.mark.asyncio
async def test_get_list(date_greater_than_filter_manager):
    for _ in range(5):
        date_greater_than_filter_data = factory.build(dict, FACTORY_CLASS=DateGreaterThanFilterFactory)
        await date_greater_than_filter_manager.add(**date_greater_than_filter_data)

    date_greater_than_filters = await date_greater_than_filter_manager.get_list()
    assert len(date_greater_than_filters) == 5

#pac_id
@pytest.mark.asyncio
async def test_get_by_pac_id(date_greater_than_filter_manager):
    pac_id = 123  # Replace with a valid pac ID from your system, perhaps created using a PacFactory
    date_greater_than_filter_data = factory.build(dict, FACTORY_CLASS=DateGreaterThanFilterFactory, pac_id=pac_id)
    await date_greater_than_filter_manager.add(**date_greater_than_filter_data)

    date_greater_than_filters = await date_greater_than_filter_manager.get_by_pac_id(pac_id)
    assert len(date_greater_than_filters) == 1

#flvr_foreign_key_id
@pytest.mark.asyncio
async def test_get_by_flvr_foreign_key_id(date_greater_than_filter_manager):
    flvr_foreign_key_id = 456  # Replace with a valid flavor ID from your system, perhaps created using a FlavorFactory
    date_greater_than_filter_data = factory.build(dict, FACTORY_CLASS=DateGreaterThanFilterFactory, flvr_foreign_key_id=flvr_foreign_key_id)
    await date_greater_than_filter_manager.add(**date_greater_than_filter_data)

    date_greater_than_filters = await date_greater_than_filter_manager.get_by_flvr_foreign_key_id(flvr_foreign_key_id)
    assert len(date_greater_than_filters) == 1

