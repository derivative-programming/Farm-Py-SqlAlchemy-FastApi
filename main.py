from fastapi import FastAPI 
from sqlalchemy.ext.asyncio import AsyncSession,create_async_engine
from sqlalchemy.orm import sessionmaker 
from managers import LandManager
from managers import FlavorManager
from models import Plant
import configparser


# Initialize the parser
config = configparser.ConfigParser()
config.read('config.ini')

# Access the DATABASE_URL
DATABASE_URL = config['database']['DATABASE_URL']


app = FastAPI()

engine = create_async_engine(DATABASE_URL, echo=True) 
AsyncSessionLocal = sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)

@app.router.on_startup.append
async def startup_event():
    async with AsyncSessionLocal() as session:
        land_manager = LandManager(session)
        flavor_manager = FlavorManager(session)
        await land_manager.create()
        await flavor_manager.create(name='unknown')
        await flavor_manager.create(name='sweet')
        await flavor_manager.create(name='sour')
