import uuid
import pytest
import factory
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from models.factory import RoleFactory
from managers.role import RoleManager
from models.role import Base

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
async def role_manager(async_session):
    return RoleManager(async_session)

@pytest.mark.asyncio
async def test_add(role_manager):
    role_data = factory.build(dict, FACTORY_CLASS=RoleFactory)
    added_role = await role_manager.add(**role_data)

    assert added_role
    assert added_role.role_id

@pytest.mark.asyncio
async def test_get_by_id(role_manager):
    role_data = factory.build(dict, FACTORY_CLASS=RoleFactory)
    added_role = await role_manager.add(**role_data)

    fetched_role = await role_manager.get_by_id(added_role.role_id)
    assert fetched_role.role_id == added_role.role_id

@pytest.mark.asyncio
async def test_get_by_code(role_manager):
    role_data = factory.build(dict, FACTORY_CLASS=RoleFactory)
    await role_manager.add(**role_data)

    fetched_role = await role_manager.get_by_code(role_data["code"])
    assert fetched_role.code == role_data["code"]

@pytest.mark.asyncio
async def test_update(role_manager):
    role_data = factory.build(dict, FACTORY_CLASS=RoleFactory)
    added_role = await role_manager.add(**role_data)
    new_code = uuid.uuid4()  # Generate a new UUID
    await role_manager.update(added_role.role_id, code=new_code)

    fetched_role = await role_manager.get_by_id(added_role.role_id)
    assert fetched_role.code == new_code

@pytest.mark.asyncio
async def test_delete(role_manager):
    role_data = factory.build(dict, FACTORY_CLASS=RoleFactory)
    added_role = await role_manager.add(**role_data)

    await role_manager.delete(added_role.role_id)
    fetched_role = await role_manager.get_by_id(added_role.role_id)
    assert not fetched_role

@pytest.mark.asyncio
async def test_get_list(role_manager):
    for _ in range(5):
        role_data = factory.build(dict, FACTORY_CLASS=RoleFactory)
        await role_manager.add(**role_data)

    roles = await role_manager.get_list()
    assert len(roles) == 5

#pac_id
@pytest.mark.asyncio
async def test_get_by_pac_id(role_manager):
    pac_id = 123  # Replace with a valid pac ID from your system, perhaps created using a PacFactory
    role_data = factory.build(dict, FACTORY_CLASS=RoleFactory, pac_id=pac_id)
    await role_manager.add(**role_data)

    roles = await role_manager.get_by_pac_id(pac_id)
    assert len(roles) == 1

#flvr_foreign_key_id
@pytest.mark.asyncio
async def test_get_by_flvr_foreign_key_id(role_manager):
    flvr_foreign_key_id = 456  # Replace with a valid flavor ID from your system, perhaps created using a FlavorFactory
    role_data = factory.build(dict, FACTORY_CLASS=RoleFactory, flvr_foreign_key_id=flvr_foreign_key_id)
    await role_manager.add(**role_data)

    roles = await role_manager.get_by_flvr_foreign_key_id(flvr_foreign_key_id)
    assert len(roles) == 1

