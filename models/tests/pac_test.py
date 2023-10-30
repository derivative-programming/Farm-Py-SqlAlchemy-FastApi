import pytest
import uuid
from datetime import datetime
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.future import select
from models import Base, Pac
from models.factory import PacFactory
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
async def test_pac_creation(session):
    pac = await PacFactory.create_async(session=session)
    assert pac.pac_id is not None
@pytest.mark.asyncio
async def test_code_default(session):
    pac = await PacFactory.create_async(session=session)
    assert isinstance(pac.code, uuid.UUID)
@pytest.mark.asyncio
async def test_last_change_code_default_on_creation(session):
    pac = await PacFactory.create_async(session=session)
    assert isinstance(pac.last_change_code, uuid.UUID)
@pytest.mark.asyncio
async def test_last_change_code_default_on_update(session):
    pac = await PacFactory.create_async(session=session)
    initial_code = pac.last_change_code
    pac.code = uuid.uuid4()
    await session.commit()
    assert pac.last_change_code != initial_code
@pytest.mark.asyncio
async def test_date_inserted(session):
    pac = PacFactory.build_async(session=session)
    assert pac.insert_utc_date_time is None
    await session.commit()
    assert isinstance(pac.insert_utc_date_time, datetime)
@pytest.mark.asyncio
async def test_date_updated(session):
    pac = await PacFactory.create_async(session=session)
    initial_time = pac.last_update_utc_date_time
    pac.code = uuid.uuid4()
    await session.commit()
    assert pac.last_update_utc_date_time > initial_time
# @pytest.mark.asyncio
# async def test_string_length_limits(session):
#     long_string = "a" * 300
#     pac = PacFactory(some_varchar_val=long_string, some_text_val=long_string)
#     session.add(pac)
#     # Adjust this for the specific DB limit exception you'd expect if these fields are too long
#     with pytest.raises(Exception):
#         await session.commit()
@pytest.mark.asyncio
async def test_model_deletion(session):
    pac = await PacFactory.create_async(session=session)
    session.delete(pac)
    await session.commit()
    deleted_pac = await session.get(Pac, pac.pac_id)
    assert deleted_pac is None
@pytest.mark.asyncio
async def test_data_types(session):
    pac = await PacFactory.create_async(session=session)
    # Check the data types for each property
    assert isinstance(pac.pac_id, int)
    assert isinstance(pac.code, uuid.UUID)
    assert isinstance(pac.last_change_code, uuid.UUID)
    assert isinstance(pac.insert_user_id, uuid.UUID)
    assert isinstance(pac.last_update_user_id, uuid.UUID)
    assert pac.description == "" or isinstance(pac.description, str)
    assert isinstance(pac.display_order, int)
    assert isinstance(pac.is_active, bool)
    assert pac.lookup_enum_name == "" or isinstance(pac.lookup_enum_name, str)
    assert pac.name == "" or isinstance(pac.name, str)
    # Check for the peek values, assuming they are UUIDs based on your model
    assert isinstance(pac.flvr_foreign_key_code_peek, uuid.UUID)
    assert isinstance(pac._code_peek, uuid.UUID)
    assert isinstance(pac.insert_utc_date_time, datetime.datetime)
    assert isinstance(pac.last_update_utc_date_time, datetime.datetime)
#endset
@pytest.mark.asyncio
async def test_unique_code_constraint(session):
    pac_1 = await PacFactory.create_async(session=session)
    pac_2 = await PacFactory.create_async(session=session)
    pac_2.code = pac_1.code  # Intentionally set the same code
    session.add_all([pac_1, pac_2])
    with pytest.raises(Exception):  # Adjust for the specific DB exception you'd expect
        await session.commit()
@pytest.mark.asyncio
async def test_boolean_fields_default(session):
    pac = await PacFactory.create_async(session=session)
    assert pac.code is not None
    assert pac.last_change_code is not None
    assert pac.insert_user_id is not None
    assert pac.last_update_user_id is not None
    assert pac.insert_utc_date_time is not None
    assert pac.last_update_utc_date_time is not None
    assert pac.description == ""
    assert pac.display_order == 0
    assert pac.is_active == False
    assert pac.lookup_enum_name == ""
    assert pac.name == ""
    assert pac.some_utc_date_time_val == datetime(1753, 1, 1)
    assert pac.some_varchar_val == ""
#endset
@pytest.mark.asyncio
async def test_last_change_code_concurrency(session):
    # Step 1: Create a Pac instance and commit
    pac = await PacFactory.create_async(session=session)
    # Store the original last_change_code
    original_last_change_code = pac.last_change_code
    # Step 2: Fetch the Pac instance in a new session and modify it
    session_1 = session  # Using the existing session
    pac_1 = await session_1.execute(select(Pac).filter_by(pac_id=pac.pac_id))
    pac_1 = pac_1.scalar_one()
    pac_1.code = uuid.uuid4()
    await session_1.commit()
    # Step 3: Fetch the same Pac instance in another session and modify it
    session_2 = session  # Using the same session object, but it's a new transaction after commit
    pac_2 = await session_2.execute(select(Pac).filter_by(pac_id=pac.pac_id))
    pac_2 = pac_2.scalar_one()
    pac_2.code = uuid.uuid4()
    # Step 4: Commit changes in session_2 and check the last_change_code
    await session_2.commit()
    assert pac_2.last_change_code != original_last_change_code
@pytest.mark.asyncio #FlvrForeignKeyID
async def test_invalid_flvr_foreign_key_id(session):
    pac = await PacFactory.create_async(session=session)
    pac.flvr_foreign_key_id=99999
    with pytest.raises(Exception):  # Adjust for the specific DB exception you'd expect
        await session.commit()
@pytest.mark.asyncio #ID
async def test_invalid__id(session):
    pac = await PacFactory.create_async(session=session)
    pac._id=99999
    with pytest.raises(Exception):  # Adjust for the specific DB exception you'd expect
        await session.commit()
