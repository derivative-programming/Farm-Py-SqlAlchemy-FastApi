# models/factory/base.py  # pylint: disable=duplicate-code

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
from config import TEST_DATABASE_URL

engine = create_async_engine(TEST_DATABASE_URL)

SessionLocal = sessionmaker(bind=engine, class_=AsyncSession)
