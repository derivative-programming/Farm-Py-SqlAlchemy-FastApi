# models/factory/base.py

"""
    #TODO add comment
"""

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

# Access the DATABASE_URL
DATABASE_URL = "sqlite+aiosqlite:///:memory:"

engine = create_async_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind=engine, class_=AsyncSession)
