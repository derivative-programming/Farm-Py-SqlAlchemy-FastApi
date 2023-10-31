import uuid
import pytest
import factory
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from models.factory import CustomerRoleFactory
from managers.customer_role import CustomerRoleManager
from models.customer_role import Base

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
async def customer_role_manager(async_session):
    return CustomerRoleManager(async_session)

@pytest.mark.asyncio
async def test_add(customer_role_manager):
    customer_role_data = factory.build(dict, FACTORY_CLASS=CustomerRoleFactory)
    added_customer_role = await customer_role_manager.add(**customer_role_data)

    assert added_customer_role
    assert added_customer_role.customer_role_id

@pytest.mark.asyncio
async def test_get_by_id(customer_role_manager):
    customer_role_data = factory.build(dict, FACTORY_CLASS=CustomerRoleFactory)
    added_customer_role = await customer_role_manager.add(**customer_role_data)

    fetched_customer_role = await customer_role_manager.get_by_id(added_customer_role.customer_role_id)
    assert fetched_customer_role.customer_role_id == added_customer_role.customer_role_id

@pytest.mark.asyncio
async def test_get_by_code(customer_role_manager):
    customer_role_data = factory.build(dict, FACTORY_CLASS=CustomerRoleFactory)
    await customer_role_manager.add(**customer_role_data)

    fetched_customer_role = await customer_role_manager.get_by_code(customer_role_data["code"])
    assert fetched_customer_role.code == customer_role_data["code"]

@pytest.mark.asyncio
async def test_update(customer_role_manager):
    customer_role_data = factory.build(dict, FACTORY_CLASS=CustomerRoleFactory)
    added_customer_role = await customer_role_manager.add(**customer_role_data)
    new_code = uuid.uuid4()  # Generate a new UUID
    await customer_role_manager.update(added_customer_role.customer_role_id, code=new_code)

    fetched_customer_role = await customer_role_manager.get_by_id(added_customer_role.customer_role_id)
    assert fetched_customer_role.code == new_code

@pytest.mark.asyncio
async def test_delete(customer_role_manager):
    customer_role_data = factory.build(dict, FACTORY_CLASS=CustomerRoleFactory)
    added_customer_role = await customer_role_manager.add(**customer_role_data)

    await customer_role_manager.delete(added_customer_role.customer_role_id)
    fetched_customer_role = await customer_role_manager.get_by_id(added_customer_role.customer_role_id)
    assert not fetched_customer_role

@pytest.mark.asyncio
async def test_get_list(customer_role_manager):
    for _ in range(5):
        customer_role_data = factory.build(dict, FACTORY_CLASS=CustomerRoleFactory)
        await customer_role_manager.add(**customer_role_data)

    customer_roles = await customer_role_manager.get_list()
    assert len(customer_roles) == 5

#customer_id
@pytest.mark.asyncio
async def test_get_by_customer_id(customer_role_manager):
    customer_id = 123  # Replace with a valid customer ID from your system, perhaps created using a CustomerFactory
    customer_role_data = factory.build(dict, FACTORY_CLASS=CustomerRoleFactory, customer_id=customer_id)
    await customer_role_manager.add(**customer_role_data)

    customer_roles = await customer_role_manager.get_by_customer_id(customer_id)
    assert len(customer_roles) == 1

#flvr_foreign_key_id
@pytest.mark.asyncio
async def test_get_by_flvr_foreign_key_id(customer_role_manager):
    flvr_foreign_key_id = 456  # Replace with a valid flavor ID from your system, perhaps created using a FlavorFactory
    customer_role_data = factory.build(dict, FACTORY_CLASS=CustomerRoleFactory, flvr_foreign_key_id=flvr_foreign_key_id)
    await customer_role_manager.add(**customer_role_data)

    customer_roles = await customer_role_manager.get_by_flvr_foreign_key_id(flvr_foreign_key_id)
    assert len(customer_roles) == 1

