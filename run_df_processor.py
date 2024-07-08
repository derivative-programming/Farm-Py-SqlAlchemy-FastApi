# run_df_processor.py  # pylint: disable=duplicate-code
"""
This module is responsible for running the data flow processor.

It initializes the database, configures logging,
and runs the DynaFlowProcessor.

Functions:
- init_db: Create the database tables.
- main: Initialize the database and run the DynaFlowProcessor.
"""

import asyncio
import logging

from database import get_db, engine
from helpers.session_context import SessionContext
import current_runtime
from models import Base
from df_processor.dyna_flow_processor import DynaFlowProcessor

# Get the SQLAlchemy logger
sqlalchemy_logger = logging.getLogger('sqlalchemy')
# Set the logging level to WARNING or ERROR to reduce verbosity
sqlalchemy_logger.setLevel(logging.WARNING)  # or logging.ERROR

# Example: Configure logging for the application
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    handlers=[
                        logging.FileHandler("app.log"),
                        logging.StreamHandler()
                    ])


async def init_db():
    """
    Create the database tables.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async for session in get_db():
        session_context = SessionContext({}, session)
        await current_runtime.initialize(session_context)
        await session.commit()
        break


async def main():
    """
    Initialize the database and run the DynaFlowProcessor.
    """
    await init_db()

    processor = DynaFlowProcessor()
    await processor.run()


if __name__ == '__main__':
    asyncio.run(main())
