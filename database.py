# database.py
from sqlalchemy.ext.asyncio import AsyncSession,create_async_engine
from sqlalchemy.orm import sessionmaker
from config import DATABASE_URL
# import configparser
  
# # Initialize the parser
# config = configparser.ConfigParser()
# config.read('config.ini')

# # Access the DATABASE_URL
# DATABASE_URL = config['database']['DATABASE_URL']


engine = create_async_engine(DATABASE_URL, echo=True) 

AsyncSessionLocal = sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)

async def get_db():
    async with AsyncSessionLocal() as db:
        yield db