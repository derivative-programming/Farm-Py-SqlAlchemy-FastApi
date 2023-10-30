import pytest
import uuid
from datetime import datetime
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.future import select
from models import Base, TriStateFilter
from models.factory import TriStateFilterFactory
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
async def test_tri_state_filter_creation(session):
    tri_state_filter = TriStateFilterFactory(session=session)
    assert tri_state_filter.tri_state_filter_id is not None
@pytest.mark.asyncio
async def test_code_default(session):
    tri_state_filter = TriStateFilterFactory(session=session)
    assert isinstance(tri_state_filter.code, uuid.UUID)
@pytest.mark.asyncio
async def test_last_change_code_default(session):
    tri_state_filter = TriStateFilterFactory(session=session)
    assert isinstance(tri_state_filter.last_change_code, uuid.UUID)
@pytest.mark.asyncio
async def test_last_change_code_changes_on_update(session):
    # Create a tri_state_filter and commit it to the database
    tri_state_filter = TriStateFilterFactory(session=session)
    # Store the initial last_change_code
    initial_last_change_code = tri_state_filter.last_change_code
    # Update the code property of the tri_state_filter
    tri_state_filter.code = uuid.uuid4()  # Generating a new UUID for the code
    # Commit the update
    await session.commit()
    # Assert that the last_change_code has changed after the update
    assert tri_state_filter.last_change_code != initial_last_change_code
    assert isinstance(tri_state_filter.last_change_code, uuid.UUID)
@pytest.mark.asyncio
async def test_date_inserted(session):
    tri_state_filter = TriStateFilterFactory(session=session).build()
    assert tri_state_filter.insert_utc_date_time is None
    session.add(tri_state_filter)
    await session.commit()
    assert isinstance(tri_state_filter.insert_utc_date_time, datetime)
@pytest.mark.asyncio
async def test_date_updated(session):
    tri_state_filter = TriStateFilterFactory(session=session)
    initial_time = tri_state_filter.last_update_utc_date_time
    assert tri_state_filter.description == ""
    assert tri_state_filter.display_order == 0
    assert tri_state_filter.is_active == False
    assert tri_state_filter.lookup_enum_name == ""
    assert tri_state_filter.name == ""
    assert tri_state_filter.pac_id > 0
    assert tri_state_filter.state_int_value == 0
# @pytest.mark.asyncio
# async def test_string_length_limits(session):
#     long_string = "a" * 300
#     tri_state_filter = TriStateFilterFactory(some_varchar_val=long_string, some_text_val=long_string)
#     session.add(tri_state_filter)
#     # Adjust this for the specific DB limit exception you'd expect if these fields are too long
#     with pytest.raises(Exception):
#         await session.commit()
@pytest.mark.asyncio
async def test_model_deletion(session):
    tri_state_filter = TriStateFilterFactory(session=session)
    session.delete(tri_state_filter)
    await session.commit()
    deleted_tri_state_filter = await session.get(TriStateFilter, tri_state_filter.tri_state_filter_id)
    assert deleted_tri_state_filter is None
@pytest.mark.asyncio
async def test_data_types(session):
    tri_state_filter = TriStateFilterFactory(session=session,some_int_val="12345", some_float_val="123.45")
    # Check the data types for each property
    assert isinstance(tri_state_filter.tri_state_filter_id, int)
    assert isinstance(tri_state_filter.code, uuid.UUID)
    assert isinstance(tri_state_filter.last_change_code, uuid.UUID)
    assert isinstance(tri_state_filter.insert_user_id, uuid.UUID)
    assert isinstance(tri_state_filter.last_update_user_id, uuid.UUID)
    assert isinstance(tri_state_filter.insert_utc_date_time, datetime.datetime)
    assert isinstance(tri_state_filter.last_update_utc_date_time, datetime.datetime)
    assert isinstance(tri_state_filter.pac_id, int)
    assert tri_state_filter.other_flavor == "" or isinstance(tri_state_filter.other_flavor, str)
    assert isinstance(tri_state_filter.some_big_int_val, int)
    tri_state_filter.some_varchar_val = "Changed"
    await session.commit()
    assert tri_state_filter.last_update_utc_date_time > initial_time
@pytest.mark.asyncio
async def test_unique_code_constraint(session):
    tri_state_filter_1 = TriStateFilterFactory(session=session)
    tri_state_filter_2 = TriStateFilterFactory(session=session)
    tri_state_filter_2.code = tri_state_filter_1.code  # Intentionally set the same code
    session.add_all([tri_state_filter_1, tri_state_filter_2])
    with pytest.raises(Exception):  # Adjust for the specific DB exception you'd expect
        await session.commit()
@pytest.mark.asyncio
async def test_boolean_fields_default(session):
    tri_state_filter = TriStateFilterFactory(session=session)
    assert tri_state_filter.code is not None
    assert tri_state_filter.last_change_code is not None
    assert tri_state_filter.insert_user_id is not None
    assert tri_state_filter.last_update_user_id is not None
    assert tri_state_filter.insert_utc_date_time is not None
    assert tri_state_filter.last_update_utc_date_time is not None
    assert isinstance(tri_state_filter.some_utc_date_time_val, datetime.datetime)
    assert tri_state_filter.some_varchar_val == "" or isinstance(tri_state_filter.some_varchar_val, str)
    assert isinstance(tri_state_filter.pac_code_peek, uuid.UUID) #PacID
@pytest.mark.asyncio
async def test_last_change_code_concurrency(session):
    # Step 1: Create a TriStateFilter instance and commit
    tri_state_filter = TriStateFilterFactory(session=session)
    # Store the original last_change_code
    original_last_change_code = tri_state_filter.last_change_code
    # Step 2: Fetch the TriStateFilter instance in a new session and modify it
    session_1 = session  # Using the existing session
    tri_state_filter_1 = await session_1.execute(select(TriStateFilter).filter_by(tri_state_filter_id=tri_state_filter.tri_state_filter_id))
    tri_state_filter_1 = tri_state_filter_1.scalar_one()
    tri_state_filter_1.some_varchar_val = "Change1"
    await session_1.commit()
    # Step 3: Fetch the same TriStateFilter instance in another session and modify it
    session_2 = session  # Using the same session object, but it's a new transaction after commit
    tri_state_filter_2 = await session_2.execute(select(TriStateFilter).filter_by(tri_state_filter_id=tri_state_filter.tri_state_filter_id))
    tri_state_filter_2 = tri_state_filter_2.scalar_one()
    tri_state_filter_2.some_varchar_val = "Change2"
    # Step 4: Commit changes in session_2 and check the last_change_code
    await session_2.commit()
    assert tri_state_filter_2.last_change_code != original_last_change_code
@pytest.mark.asyncio #FlvrForeignKeyID
async def test_invalid_flvr_foreign_key_id(session):
    tri_state_filter = TriStateFilterFactory(session=session,flvr_foreign_key_id=99999)  # Assume no Flavor with ID 99999
    session.add(tri_state_filter)
    with pytest.raises(Exception):  # Adjust for the specific DB exception you'd expect
        await session.commit()
@pytest.mark.asyncio #PacID
async def test_invalid_pac_id(session):
    tri_state_filter = TriStateFilterFactory(session=session,pac_id=99999)  # Assume no Pac with ID 99999
    session.add(tri_state_filter)
    with pytest.raises(Exception):  # Adjust for the specific DB exception you'd expect
        await session.commit()
