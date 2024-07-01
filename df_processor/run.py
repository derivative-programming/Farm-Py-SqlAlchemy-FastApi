
import asyncio

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from database import get_db, engine
from helpers.session_context import SessionContext
import current_runtime
from models import Base
from .dyna_flow_processor import DynaFlowProcessor


async def init_db():
    # Create the database tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async for session in get_db():
        session_context = SessionContext(dict(), session)
        await current_runtime.initialize(session_context)
        await session.commit()
        break


async def main():

    # Initialize the database
    await init_db()

    processor = DynaFlowProcessor()
    await processor.run()


if __name__ == '__main__':
    asyncio.run(main())
