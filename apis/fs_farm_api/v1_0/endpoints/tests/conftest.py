# conftest.py
import pytest
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from database import AsyncSessionLocal
from models import Base
import pytest_asyncio 

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

 