import pytest
import uuid
from datetime import datetime
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.future import select
from models import Base, DateGreaterThanFilter
from models.factory import DateGreaterThanFilterFactory
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
async def test_date_greater_than_filter_creation(session):
    date_greater_than_filter = DateGreaterThanFilterFactory(session=session)
    assert date_greater_than_filter.date_greater_than_filter_id is not None
@pytest.mark.asyncio
async def test_code_default(session):
    date_greater_than_filter = DateGreaterThanFilterFactory(session=session)
    assert isinstance(date_greater_than_filter.code, uuid.UUID)
@pytest.mark.asyncio
async def test_last_change_code_default(session):
    date_greater_than_filter = DateGreaterThanFilterFactory(session=session)
    assert isinstance(date_greater_than_filter.last_change_code, uuid.UUID)
@pytest.mark.asyncio
async def test_last_change_code_changes_on_update(session):
    # Create a date_greater_than_filter and commit it to the database
    date_greater_than_filter = DateGreaterThanFilterFactory(session=session)
    # Store the initial last_change_code
    initial_last_change_code = date_greater_than_filter.last_change_code
    # Update the code property of the date_greater_than_filter
    date_greater_than_filter.code = uuid.uuid4()  # Generating a new UUID for the code
    # Commit the update
    await session.commit()
    # Assert that the last_change_code has changed after the update
    assert date_greater_than_filter.last_change_code != initial_last_change_code
    assert isinstance(date_greater_than_filter.last_change_code, uuid.UUID)
@pytest.mark.asyncio
async def test_date_inserted(session):
    date_greater_than_filter = DateGreaterThanFilterFactory(session=session).build()
    assert date_greater_than_filter.insert_utc_date_time is None
    session.add(date_greater_than_filter)
    await session.commit()
    assert isinstance(date_greater_than_filter.insert_utc_date_time, datetime)
@pytest.mark.asyncio
async def test_date_updated(session):
    date_greater_than_filter = DateGreaterThanFilterFactory(session=session)
    initial_time = date_greater_than_filter.last_update_utc_date_time
    assert date_greater_than_filter.day_count == 0
    assert date_greater_than_filter.description == ""
    assert date_greater_than_filter.display_order == 0
    assert date_greater_than_filter.is_active == False
    assert date_greater_than_filter.lookup_enum_name == ""
    assert date_greater_than_filter.name == ""
    assert date_greater_than_filter.pac_id > 0
# @pytest.mark.asyncio
# async def test_string_length_limits(session):
#     long_string = "a" * 300
#     date_greater_than_filter = DateGreaterThanFilterFactory(some_varchar_val=long_string, some_text_val=long_string)
#     session.add(date_greater_than_filter)
#     # Adjust this for the specific DB limit exception you'd expect if these fields are too long
#     with pytest.raises(Exception):
#         await session.commit()
@pytest.mark.asyncio
async def test_model_deletion(session):
    date_greater_than_filter = DateGreaterThanFilterFactory(session=session)
    session.delete(date_greater_than_filter)
    await session.commit()
    deleted_date_greater_than_filter = await session.get(DateGreaterThanFilter, date_greater_than_filter.date_greater_than_filter_id)
    assert deleted_date_greater_than_filter is None
@pytest.mark.asyncio
async def test_data_types(session):
    date_greater_than_filter = DateGreaterThanFilterFactory(session=session,some_int_val="12345", some_float_val="123.45")
    # Check the data types for each property
    assert isinstance(date_greater_than_filter.date_greater_than_filter_id, int)
    assert isinstance(date_greater_than_filter.code, uuid.UUID)
    assert isinstance(date_greater_than_filter.last_change_code, uuid.UUID)
    assert isinstance(date_greater_than_filter.insert_user_id, uuid.UUID)
    assert isinstance(date_greater_than_filter.last_update_user_id, uuid.UUID)
    assert isinstance(date_greater_than_filter.insert_utc_date_time, datetime.datetime)
    assert isinstance(date_greater_than_filter.last_update_utc_date_time, datetime.datetime)
    assert isinstance(date_greater_than_filter.pac_id, int)
    assert date_greater_than_filter.other_flavor == "" or isinstance(date_greater_than_filter.other_flavor, str)
    assert isinstance(date_greater_than_filter.some_big_int_val, int)
    date_greater_than_filter.some_varchar_val = "Changed"
    await session.commit()
    assert date_greater_than_filter.last_update_utc_date_time > initial_time
@pytest.mark.asyncio
async def test_unique_code_constraint(session):
    date_greater_than_filter_1 = DateGreaterThanFilterFactory(session=session)
    date_greater_than_filter_2 = DateGreaterThanFilterFactory(session=session)
    date_greater_than_filter_2.code = date_greater_than_filter_1.code  # Intentionally set the same code
    session.add_all([date_greater_than_filter_1, date_greater_than_filter_2])
    with pytest.raises(Exception):  # Adjust for the specific DB exception you'd expect
        await session.commit()
@pytest.mark.asyncio
async def test_boolean_fields_default(session):
    date_greater_than_filter = DateGreaterThanFilterFactory(session=session)
    assert date_greater_than_filter.code is not None
    assert date_greater_than_filter.last_change_code is not None
    assert date_greater_than_filter.insert_user_id is not None
    assert date_greater_than_filter.last_update_user_id is not None
    assert date_greater_than_filter.insert_utc_date_time is not None
    assert date_greater_than_filter.last_update_utc_date_time is not None
    assert isinstance(date_greater_than_filter.some_utc_date_time_val, datetime.datetime)
    assert date_greater_than_filter.some_varchar_val == "" or isinstance(date_greater_than_filter.some_varchar_val, str)
    assert isinstance(date_greater_than_filter.pac_code_peek, uuid.UUID) #PacID
@pytest.mark.asyncio
async def test_last_change_code_concurrency(session):
    # Step 1: Create a DateGreaterThanFilter instance and commit
    date_greater_than_filter = DateGreaterThanFilterFactory(session=session)
    # Store the original last_change_code
    original_last_change_code = date_greater_than_filter.last_change_code
    # Step 2: Fetch the DateGreaterThanFilter instance in a new session and modify it
    session_1 = session  # Using the existing session
    date_greater_than_filter_1 = await session_1.execute(select(DateGreaterThanFilter).filter_by(date_greater_than_filter_id=date_greater_than_filter.date_greater_than_filter_id))
    date_greater_than_filter_1 = date_greater_than_filter_1.scalar_one()
    date_greater_than_filter_1.some_varchar_val = "Change1"
    await session_1.commit()
    # Step 3: Fetch the same DateGreaterThanFilter instance in another session and modify it
    session_2 = session  # Using the same session object, but it's a new transaction after commit
    date_greater_than_filter_2 = await session_2.execute(select(DateGreaterThanFilter).filter_by(date_greater_than_filter_id=date_greater_than_filter.date_greater_than_filter_id))
    date_greater_than_filter_2 = date_greater_than_filter_2.scalar_one()
    date_greater_than_filter_2.some_varchar_val = "Change2"
    # Step 4: Commit changes in session_2 and check the last_change_code
    await session_2.commit()
    assert date_greater_than_filter_2.last_change_code != original_last_change_code
@pytest.mark.asyncio #FlvrForeignKeyID
async def test_invalid_flvr_foreign_key_id(session):
    date_greater_than_filter = DateGreaterThanFilterFactory(session=session,flvr_foreign_key_id=99999)  # Assume no Flavor with ID 99999
    session.add(date_greater_than_filter)
    with pytest.raises(Exception):  # Adjust for the specific DB exception you'd expect
        await session.commit()
@pytest.mark.asyncio #PacID
async def test_invalid_pac_id(session):
    date_greater_than_filter = DateGreaterThanFilterFactory(session=session,pac_id=99999)  # Assume no Pac with ID 99999
    session.add(date_greater_than_filter)
    with pytest.raises(Exception):  # Adjust for the specific DB exception you'd expect
        await session.commit()
