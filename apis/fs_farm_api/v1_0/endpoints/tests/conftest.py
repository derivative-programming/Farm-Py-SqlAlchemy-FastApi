# conftest.py 
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from helpers.session_context import SessionContext 
from models import Base
import models.factory as model_factorys
import pytest_asyncio 
from helpers.api_token import ApiToken
import business

# Define your in-memory SQLite test database URL
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

@pytest_asyncio.fixture(scope="function")
async def overridden_get_db():  
   
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
async def api_key_fixture(overridden_get_db: AsyncSession):  
    session_context = SessionContext(dict(),overridden_get_db)
    customer = await model_factorys.CustomerFactory.create_async(overridden_get_db)
    customer_bus_obj = await business.CustomerBusObj.get(session_context,customer_obj_instance=customer)
    tac_bus_obj = await business.TacBusObj.get(session_context,tac_id=customer.tac_id) 
    pac_bus_obj = await business.PacBusObj.get(session_context,pac_id=tac_bus_obj.pac_id)
    api_dict = {'CustomerCode': str(customer.code),
                'TacCode': str(tac_bus_obj.code),
                'PacCode': str(pac_bus_obj.code),
                'UserName': customer.email}
    test_api_key = ApiToken.create_token(api_dict, 1)
    return test_api_key