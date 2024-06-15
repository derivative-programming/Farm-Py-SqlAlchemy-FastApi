# apis/fs_farm_api/v1_0/endpoints/tests/conftest.py

"""
    #TODO add comment
"""

import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

import business
import current_runtime
import models.factory as model_factorys
from helpers.api_token import ApiToken
from helpers.session_context import SessionContext
from models import Base

# Define your in-memory SQLite test database URL
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"


@pytest_asyncio.fixture(scope="function")
async def overridden_get_db():
    """
        #TODO create comment
    """
    # Create the async engine for the in-memory SQLite database
    engine = create_async_engine(TEST_DATABASE_URL, echo=False)

    # Create the tables in the database
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Create a sessionmaker
    AsyncSessionLocal = sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False
    )

    # Create a new session for the test
    async with AsyncSessionLocal() as session:
        yield session

    # After the test is done, drop all the tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    # Dispose the engine
    await engine.dispose()


@pytest_asyncio.fixture(scope="function")
async def old_api_key_fixture(overridden_get_db: AsyncSession):
    """
        Build a test api key for unit testing
    """

    session_context = SessionContext(dict(), overridden_get_db)

    await current_runtime.initialize(session_context)

    customer = await model_factorys.CustomerFactory.create_async(
        overridden_get_db)

    customer_bus_obj = business.CustomerBusObj(session_context)

    await customer_bus_obj.load_from_obj_instance(customer)

    tac_bus_obj = business.TacBusObj(session_context)

    await tac_bus_obj.load_from_id(customer_bus_obj.tac_id)

    pac_bus_obj = business.PacBusObj(session_context)

    await pac_bus_obj.load_from_id(tac_bus_obj.pac_id)

    api_dict = {'CustomerCode': str(customer_bus_obj.code),
                'TacCode': str(tac_bus_obj.code),
                'PacCode': str(pac_bus_obj.code),
                'UserName': customer.email}
    test_api_key = ApiToken.create_token(api_dict, 1)
    return test_api_key


@pytest_asyncio.fixture(scope="function")
async def api_key_fixture(overridden_get_db: AsyncSession):
    """
        Build a test api key for unit testing
    """

    session_context = SessionContext(dict(), overridden_get_db)

    await current_runtime.initialize(session_context)

    # customer = await model_factorys.CustomerFactory.create_async(
    #     overridden_get_db)

    # customer_bus_obj = business.CustomerBusObj(session_context)

    # await customer_bus_obj.load_from_obj_instance(customer)

    # tac_bus_obj = business.TacBusObj(session_context)

    # await tac_bus_obj.load_from_id(customer_bus_obj.tac_id)

    # pac_bus_obj = business.PacBusObj(session_context)

    # await pac_bus_obj.load_from_id(tac_bus_obj.pac_id)

    api_dict = {}
    test_api_key = ApiToken.create_token(api_dict, 1)
    return test_api_key
