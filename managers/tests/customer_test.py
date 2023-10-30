import uuid
import pytest
import factory
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from models.factory import CustomerFactory
from managers.customer import CustomerManager
from models.customer import Base
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
async def customer_manager(async_session):
    return CustomerManager(async_session)
@pytest.mark.asyncio
async def test_add(customer_manager):
    customer_data = factory.build(dict, FACTORY_CLASS=CustomerFactory)
    added_customer = await customer_manager.add(**customer_data)
    assert added_customer
    assert added_customer.id
@pytest.mark.asyncio
async def test_get_by_id(customer_manager):
    customer_data = factory.build(dict, FACTORY_CLASS=CustomerFactory)
    added_customer = await customer_manager.add(**customer_data)
    fetched_customer = await customer_manager.get_by_id(added_customer.id)
    assert fetched_customer.id == added_customer.id
@pytest.mark.asyncio
async def test_get_by_code(customer_manager):
    customer_data = factory.build(dict, FACTORY_CLASS=CustomerFactory)
    await customer_manager.add(**customer_data)
    fetched_customer = await customer_manager.get_by_code(customer_data["code"])
    assert fetched_customer.code == customer_data["code"]
@pytest.mark.asyncio
async def test_update(customer_manager):
    customer_data = factory.build(dict, FACTORY_CLASS=CustomerFactory)
    added_customer = await customer_manager.add(**customer_data)
    new_code = uuid.uuid4()  # Generate a new UUID
    await customer_manager.update(added_customer.id, code=new_code)
    fetched_customer = await customer_manager.get_by_id(added_customer.id)
    assert fetched_customer.code == new_code
@pytest.mark.asyncio
async def test_delete(customer_manager):
    customer_data = factory.build(dict, FACTORY_CLASS=CustomerFactory)
    added_customer = await customer_manager.add(**customer_data)
    await customer_manager.delete(added_customer.id)
    fetched_customer = await customer_manager.get_by_id(added_customer.id)
    assert not fetched_customer
@pytest.mark.asyncio
async def test_get_list(customer_manager):
    for _ in range(5):
        customer_data = factory.build(dict, FACTORY_CLASS=CustomerFactory)
        await customer_manager.add(**customer_data)
    customers = await customer_manager.get_list()
    assert len(customers) == 5
#tac_id
@pytest.mark.asyncio
async def test_get_by_tac_id(customer_manager):
    tac_id = 123  # Replace with a valid tac ID from your system, perhaps created using a TacFactory
    customer_data = factory.build(dict, FACTORY_CLASS=CustomerFactory, tac_id=tac_id)
    await customer_manager.add(**customer_data)
    customers = await customer_manager.get_by_tac_id(tac_id)
    assert len(customers) == 1
#flvr_foreign_key_id
@pytest.mark.asyncio
async def test_get_by_flvr_foreign_key_id(customer_manager):
    flvr_foreign_key_id = 456  # Replace with a valid flavor ID from your system, perhaps created using a FlavorFactory
    customer_data = factory.build(dict, FACTORY_CLASS=CustomerFactory, flvr_foreign_key_id=flvr_foreign_key_id)
    await customer_manager.add(**customer_data)
    customers = await customer_manager.get_by_flvr_foreign_key_id(flvr_foreign_key_id)
    assert len(customers) == 1
#endset
