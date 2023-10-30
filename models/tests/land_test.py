import pytest
import uuid
from datetime import datetime
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.future import select
from models import Base, Land
from models.factory import LandFactory
DATABASE_URL = "sqlite+aiosqlite:///:memory:"
@pytest.fixture(scope="module")
async def async_engine():
    engine = create_async_engine(DATABASE_URL, echo=True)
    yield engine
    await engine.dispose()
@pytest.fixture
async def session(async_engine):
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    SessionLocal = sessionmaker(
        bind=async_engine, class_=AsyncSession, expire_on_commit=False
    )
    async with SessionLocal() as session:
        yield session
@pytest.mark.asyncio
async def test_land_creation(session):
    land = await LandFactory.create_async(session=session)
    assert land.land_id is not None
@pytest.mark.asyncio
async def test_code_default(session):
    land = await LandFactory.create_async(session=session)
    assert isinstance(land.code, uuid.UUID)
@pytest.mark.asyncio
async def test_last_change_code_default_on_creation(session):
    land = await LandFactory.create_async(session=session)
    assert isinstance(land.last_change_code, uuid.UUID)
@pytest.mark.asyncio
async def test_last_change_code_default_on_update(session):
    land = await LandFactory.create_async(session=session)
    initial_code = land.last_change_code
    land.code = uuid.uuid4()
    await session.commit()
    assert land.last_change_code != initial_code
@pytest.mark.asyncio
async def test_date_inserted(session):
    land = LandFactory.build_async(session=session)
    assert land.insert_utc_date_time is None
    await session.commit()
    assert isinstance(land.insert_utc_date_time, datetime)
@pytest.mark.asyncio
async def test_date_updated(session):
    land = await LandFactory.create_async(session=session)
    initial_time = land.last_update_utc_date_time
    land.code = uuid.uuid4()
    await session.commit()
    assert land.last_update_utc_date_time > initial_time
# @pytest.mark.asyncio
# async def test_string_length_limits(session):
#     long_string = "a" * 300
#     land = LandFactory(some_varchar_val=long_string, some_text_val=long_string)
#     session.add(land)
#     # Adjust this for the specific DB limit exception you'd expect if these fields are too long
#     with pytest.raises(Exception):
#         await session.commit()
@pytest.mark.asyncio
async def test_model_deletion(session):
    land = await LandFactory.create_async(session=session)
    session.delete(land)
    await session.commit()
    deleted_land = await session.get(Land, land.land_id)
    assert deleted_land is None
@pytest.mark.asyncio
async def test_data_types(session):
    land = await LandFactory.create_async(session=session)
    # Check the data types for each property
    assert isinstance(land.land_id, int)
    assert isinstance(land.code, uuid.UUID)
    assert isinstance(land.last_change_code, uuid.UUID)
    assert isinstance(land.insert_user_id, uuid.UUID)
    assert isinstance(land.last_update_user_id, uuid.UUID)
    assert land.description == "" or isinstance(land.description, str)
    assert isinstance(land.display_order, int)
    assert isinstance(land.is_active, bool)
    assert land.lookup_enum_name == "" or isinstance(land.lookup_enum_name, str)
    assert land.name == "" or isinstance(land.name, str)
    assert isinstance(land.pac_id, int)
    # Check for the peek values, assuming they are UUIDs based on your model
    assert isinstance(land.flvr_foreign_key_code_peek, uuid.UUID)
    assert isinstance(land.pac_code_peek, uuid.UUID)
    assert isinstance(land.insert_utc_date_time, datetime.datetime)
    assert isinstance(land.last_update_utc_date_time, datetime.datetime)
#endset
@pytest.mark.asyncio
async def test_unique_code_constraint(session):
    land_1 = await LandFactory.create_async(session=session)
    land_2 = await LandFactory.create_async(session=session)
    land_2.code = land_1.code  # Intentionally set the same code
    session.add_all([land_1, land_2])
    with pytest.raises(Exception):  # Adjust for the specific DB exception you'd expect
        await session.commit()
@pytest.mark.asyncio
async def test_boolean_fields_default(session):
    land = await LandFactory.create_async(session=session)
    assert land.code is not None
    assert land.last_change_code is not None
    assert land.insert_user_id is not None
    assert land.last_update_user_id is not None
    assert land.insert_utc_date_time is not None
    assert land.last_update_utc_date_time is not None
    assert land.description == ""
    assert land.display_order == 0
    assert land.is_active == False
    assert land.lookup_enum_name == ""
    assert land.name == ""
    assert isinstance(land.pac_code_peek, uuid.UUID) #PacID
    assert land.flvr_foreign_key_id > 0
    assert land.some_utc_date_time_val == datetime(1753, 1, 1)
    assert land.some_varchar_val == ""
#endset
@pytest.mark.asyncio
async def test_last_change_code_concurrency(session):
    # Step 1: Create a Land instance and commit
    land = await LandFactory.create_async(session=session)
    # Store the original last_change_code
    original_last_change_code = land.last_change_code
    # Step 2: Fetch the Land instance in a new session and modify it
    session_1 = session  # Using the existing session
    land_1 = await session_1.execute(select(Land).filter_by(land_id=land.land_id))
    land_1 = land_1.scalar_one()
    land_1.code = uuid.uuid4()
    await session_1.commit()
    # Step 3: Fetch the same Land instance in another session and modify it
    session_2 = session  # Using the same session object, but it's a new transaction after commit
    land_2 = await session_2.execute(select(Land).filter_by(land_id=land.land_id))
    land_2 = land_2.scalar_one()
    land_2.code = uuid.uuid4()
    # Step 4: Commit changes in session_2 and check the last_change_code
    await session_2.commit()
    assert land_2.last_change_code != original_last_change_code
@pytest.mark.asyncio #FlvrForeignKeyID
async def test_invalid_flvr_foreign_key_id(session):
    land = await LandFactory.create_async(session=session)
    land.flvr_foreign_key_id=99999
    with pytest.raises(Exception):  # Adjust for the specific DB exception you'd expect
        await session.commit()
@pytest.mark.asyncio #PacID
async def test_invalid_pac_id(session):
    land = await LandFactory.create_async(session=session)
    land.pac_id=99999
    with pytest.raises(Exception):  # Adjust for the specific DB exception you'd expect
        await session.commit()
