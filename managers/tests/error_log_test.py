import uuid
import pytest
import factory
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from models.factory import ErrorLogFactory
from managers.error_log import ErrorLogManager
from models.error_log import Base
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
async def error_log_manager(async_session):
    return ErrorLogManager(async_session)
@pytest.mark.asyncio
async def test_add(error_log_manager):
    error_log_data = factory.build(dict, FACTORY_CLASS=ErrorLogFactory)
    added_error_log = await error_log_manager.add(**error_log_data)
    assert added_error_log
    assert added_error_log.id
@pytest.mark.asyncio
async def test_get_by_id(error_log_manager):
    error_log_data = factory.build(dict, FACTORY_CLASS=ErrorLogFactory)
    added_error_log = await error_log_manager.add(**error_log_data)
    fetched_error_log = await error_log_manager.get_by_id(added_error_log.id)
    assert fetched_error_log.id == added_error_log.id
@pytest.mark.asyncio
async def test_get_by_code(error_log_manager):
    error_log_data = factory.build(dict, FACTORY_CLASS=ErrorLogFactory)
    await error_log_manager.add(**error_log_data)
    fetched_error_log = await error_log_manager.get_by_code(error_log_data["code"])
    assert fetched_error_log.code == error_log_data["code"]
@pytest.mark.asyncio
async def test_update(error_log_manager):
    error_log_data = factory.build(dict, FACTORY_CLASS=ErrorLogFactory)
    added_error_log = await error_log_manager.add(**error_log_data)
    new_code = uuid.uuid4()  # Generate a new UUID
    await error_log_manager.update(added_error_log.id, code=new_code)
    fetched_error_log = await error_log_manager.get_by_id(added_error_log.id)
    assert fetched_error_log.code == new_code
@pytest.mark.asyncio
async def test_delete(error_log_manager):
    error_log_data = factory.build(dict, FACTORY_CLASS=ErrorLogFactory)
    added_error_log = await error_log_manager.add(**error_log_data)
    await error_log_manager.delete(added_error_log.id)
    fetched_error_log = await error_log_manager.get_by_id(added_error_log.id)
    assert not fetched_error_log
@pytest.mark.asyncio
async def test_get_list(error_log_manager):
    for _ in range(5):
        error_log_data = factory.build(dict, FACTORY_CLASS=ErrorLogFactory)
        await error_log_manager.add(**error_log_data)
    error_logs = await error_log_manager.get_list()
    assert len(error_logs) == 5
#pac_id
@pytest.mark.asyncio
async def test_get_by_pac_id(error_log_manager):
    pac_id = 123  # Replace with a valid pac ID from your system, perhaps created using a PacFactory
    error_log_data = factory.build(dict, FACTORY_CLASS=ErrorLogFactory, pac_id=pac_id)
    await error_log_manager.add(**error_log_data)
    error_logs = await error_log_manager.get_by_pac_id(pac_id)
    assert len(error_logs) == 1
#flvr_foreign_key_id
@pytest.mark.asyncio
async def test_get_by_flvr_foreign_key_id(error_log_manager):
    flvr_foreign_key_id = 456  # Replace with a valid flavor ID from your system, perhaps created using a FlavorFactory
    error_log_data = factory.build(dict, FACTORY_CLASS=ErrorLogFactory, flvr_foreign_key_id=flvr_foreign_key_id)
    await error_log_manager.add(**error_log_data)
    error_logs = await error_log_manager.get_by_flvr_foreign_key_id(flvr_foreign_key_id)
    assert len(error_logs) == 1
#endset
