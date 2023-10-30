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
    land = LandFactory(session=session)
    assert land.land_id is not None
@pytest.mark.asyncio
async def test_code_default(session):
    land = LandFactory(session=session)
    assert isinstance(land.code, uuid.UUID)
@pytest.mark.asyncio
async def test_last_change_code_default(session):
    land = LandFactory(session=session)
    assert isinstance(land.last_change_code, uuid.UUID)
@pytest.mark.asyncio
async def test_last_change_code_changes_on_update(session):
    # Create a land and commit it to the database
    land = LandFactory(session=session)
    # Store the initial last_change_code
    initial_last_change_code = land.last_change_code
    # Update the code property of the land
    land.code = uuid.uuid4()  # Generating a new UUID for the code
    # Commit the update
    await session.commit()
    # Assert that the last_change_code has changed after the update
    assert land.last_change_code != initial_last_change_code
    assert isinstance(land.last_change_code, uuid.UUID)
@pytest.mark.asyncio
async def test_date_inserted(session):
    land = LandFactory(session=session).build()
    assert land.insert_utc_date_time is None
    session.add(land)
    await session.commit()
    assert isinstance(land.insert_utc_date_time, datetime)
@pytest.mark.asyncio
async def test_date_updated(session):
    land = LandFactory(session=session)
    initial_time = land.last_update_utc_date_time
    assert land.description == ""
    assert land.display_order == 0
    assert land.is_active == False
    assert land.lookup_enum_name == ""
    assert land.name == ""
    assert land.pac_id > 0
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
    land = LandFactory(session=session)
    session.delete(land)
    await session.commit()
    deleted_land = await session.get(Land, land.land_id)
    assert deleted_land is None
@pytest.mark.asyncio
async def test_data_types(session):
    land = LandFactory(session=session,some_int_val="12345", some_float_val="123.45")
    # Check the data types for each property
    assert isinstance(land.land_id, int)
    assert isinstance(land.code, uuid.UUID)
    assert isinstance(land.last_change_code, uuid.UUID)
    assert isinstance(land.insert_user_id, uuid.UUID)
    assert isinstance(land.last_update_user_id, uuid.UUID)
    assert isinstance(land.insert_utc_date_time, datetime.datetime)
    assert isinstance(land.last_update_utc_date_time, datetime.datetime)
    assert isinstance(land.pac_id, int)
    assert land.other_flavor == "" or isinstance(land.other_flavor, str)
    assert isinstance(land.some_big_int_val, int)
    land.some_varchar_val = "Changed"
    await session.commit()
    assert land.last_update_utc_date_time > initial_time
@pytest.mark.asyncio
async def test_unique_code_constraint(session):
    land_1 = LandFactory(session=session)
    land_2 = LandFactory(session=session)
    land_2.code = land_1.code  # Intentionally set the same code
    session.add_all([land_1, land_2])
    with pytest.raises(Exception):  # Adjust for the specific DB exception you'd expect
        await session.commit()
@pytest.mark.asyncio
async def test_boolean_fields_default(session):
    land = LandFactory(session=session)
    assert land.code is not None
    assert land.last_change_code is not None
    assert land.insert_user_id is not None
    assert land.last_update_user_id is not None
    assert land.insert_utc_date_time is not None
    assert land.last_update_utc_date_time is not None
    assert isinstance(land.some_utc_date_time_val, datetime.datetime)
    assert land.some_varchar_val == "" or isinstance(land.some_varchar_val, str)
    assert isinstance(land.pac_code_peek, uuid.UUID) #PacID
@pytest.mark.asyncio
async def test_last_change_code_concurrency(session):
    # Step 1: Create a Land instance and commit
    land = LandFactory(session=session)
    # Store the original last_change_code
    original_last_change_code = land.last_change_code
    # Step 2: Fetch the Land instance in a new session and modify it
    session_1 = session  # Using the existing session
    land_1 = await session_1.execute(select(Land).filter_by(land_id=land.land_id))
    land_1 = land_1.scalar_one()
    land_1.some_varchar_val = "Change1"
    await session_1.commit()
    # Step 3: Fetch the same Land instance in another session and modify it
    session_2 = session  # Using the same session object, but it's a new transaction after commit
    land_2 = await session_2.execute(select(Land).filter_by(land_id=land.land_id))
    land_2 = land_2.scalar_one()
    land_2.some_varchar_val = "Change2"
    # Step 4: Commit changes in session_2 and check the last_change_code
    await session_2.commit()
    assert land_2.last_change_code != original_last_change_code
@pytest.mark.asyncio #FlvrForeignKeyID
async def test_invalid_flvr_foreign_key_id(session):
    land = LandFactory(session=session,flvr_foreign_key_id=99999)  # Assume no Flavor with ID 99999
    session.add(land)
    with pytest.raises(Exception):  # Adjust for the specific DB exception you'd expect
        await session.commit()
@pytest.mark.asyncio #PacID
async def test_invalid_pac_id(session):
    land = LandFactory(session=session,pac_id=99999)  # Assume no Pac with ID 99999
    session.add(land)
    with pytest.raises(Exception):  # Adjust for the specific DB exception you'd expect
        await session.commit()
