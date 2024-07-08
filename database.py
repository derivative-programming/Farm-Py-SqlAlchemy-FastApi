# database.py  # pylint: disable=duplicate-code
"""
This module provides functions for interacting with the database.
"""
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from config import DATABASE_URL


engine = create_async_engine(DATABASE_URL, echo=False)

async_session_local = sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)


async def get_db():
    """
    Returns an asynchronous context manager for the database session.

    Usage:
        async with get_db() as db:
            # Use the database session here

    Returns:
        AsyncGenerator[AsyncSession, None]: An
        asynchronous generator that yields the database session.

    """
    async with async_session_local() as db:  # type: ignore # noqa: E501
        yield db
