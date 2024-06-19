# models/factory/base.py

"""
This module contains the base factory class for creating SQLAlchemy sessions.

The factory class provides a sessionmaker object that can be used to create
database sessions for interacting with the database.

Example usage:
    from sqlalchemy.orm import Session
    from models.factory.base import SessionLocal

    # Create a session
    session: Session = SessionLocal()

    # Use the session to interact with the database

"""

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

# Access the DATABASE_URL
DATABASE_URL = "sqlite+aiosqlite:///:memory:"

engine = create_async_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind=engine, class_=AsyncSession)
