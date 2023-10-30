import pytest
import uuid
from datetime import datetime
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.future import select
from models import Base, Tac
from models.factory import TacFactory
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
async def test_tac_creation(session):
    tac = await TacFactory.create_async(session=session)
    assert tac.tac_id is not None
@pytest.mark.asyncio
async def test_code_default(session):
    tac = await TacFactory.create_async(session=session)
    assert isinstance(tac.code, uuid.UUID)
@pytest.mark.asyncio
async def test_last_change_code_default_on_creation(session):
    tac = await TacFactory.create_async(session=session)
    assert isinstance(tac.last_change_code, uuid.UUID)
@pytest.mark.asyncio
async def test_last_change_code_default_on_update(session):
    tac = await TacFactory.create_async(session=session)
    initial_code = tac.last_change_code
    tac.code = uuid.uuid4()
    await session.commit()
    assert tac.last_change_code != initial_code
@pytest.mark.asyncio
async def test_date_inserted(session):
    tac = TacFactory.build_async(session=session)
    assert tac.insert_utc_date_time is None
    await session.commit()
    assert isinstance(tac.insert_utc_date_time, datetime)
@pytest.mark.asyncio
async def test_date_updated(session):
    tac = await TacFactory.create_async(session=session)
    initial_time = tac.last_update_utc_date_time
    tac.code = uuid.uuid4()
    await session.commit()
    assert tac.last_update_utc_date_time > initial_time
# @pytest.mark.asyncio
# async def test_string_length_limits(session):
#     long_string = "a" * 300
#     tac = TacFactory(some_varchar_val=long_string, some_text_val=long_string)
#     session.add(tac)
#     # Adjust this for the specific DB limit exception you'd expect if these fields are too long
#     with pytest.raises(Exception):
#         await session.commit()
@pytest.mark.asyncio
async def test_model_deletion(session):
    tac = await TacFactory.create_async(session=session)
    session.delete(tac)
    await session.commit()
    deleted_tac = await session.get(Tac, tac.tac_id)
    assert deleted_tac is None
@pytest.mark.asyncio
async def test_data_types(session):
    tac = await TacFactory.create_async(session=session)
    # Check the data types for each property
    assert isinstance(tac.tac_id, int)
    assert isinstance(tac.code, uuid.UUID)
    assert isinstance(tac.last_change_code, uuid.UUID)
    assert isinstance(tac.insert_user_id, uuid.UUID)
    assert isinstance(tac.last_update_user_id, uuid.UUID)
    assert tac.description == "" or isinstance(tac.description, str)
    assert isinstance(tac.display_order, int)
    assert isinstance(tac.is_active, bool)
    assert tac.lookup_enum_name == "" or isinstance(tac.lookup_enum_name, str)
    assert tac.name == "" or isinstance(tac.name, str)
    assert isinstance(tac.pac_id, int)
    # Check for the peek values, assuming they are UUIDs based on your model
    assert isinstance(tac.flvr_foreign_key_code_peek, uuid.UUID)
    assert isinstance(tac.pac_code_peek, uuid.UUID)
    assert isinstance(tac.insert_utc_date_time, datetime.datetime)
    assert isinstance(tac.last_update_utc_date_time, datetime.datetime)
#endset
@pytest.mark.asyncio
async def test_unique_code_constraint(session):
    tac_1 = await TacFactory.create_async(session=session)
    tac_2 = await TacFactory.create_async(session=session)
    tac_2.code = tac_1.code  # Intentionally set the same code
    session.add_all([tac_1, tac_2])
    with pytest.raises(Exception):  # Adjust for the specific DB exception you'd expect
        await session.commit()
@pytest.mark.asyncio
async def test_boolean_fields_default(session):
    tac = await TacFactory.create_async(session=session)
    assert tac.code is not None
    assert tac.last_change_code is not None
    assert tac.insert_user_id is not None
    assert tac.last_update_user_id is not None
    assert tac.insert_utc_date_time is not None
    assert tac.last_update_utc_date_time is not None
    assert tac.description == ""
    assert tac.display_order == 0
    assert tac.is_active == False
    assert tac.lookup_enum_name == ""
    assert tac.name == ""
    assert isinstance(tac.pac_code_peek, uuid.UUID) #PacID
    assert tac.flvr_foreign_key_id > 0
    assert tac.some_utc_date_time_val == datetime(1753, 1, 1)
    assert tac.some_varchar_val == ""
#endset
@pytest.mark.asyncio
async def test_last_change_code_concurrency(session):
    # Step 1: Create a Tac instance and commit
    tac = await TacFactory.create_async(session=session)
    # Store the original last_change_code
    original_last_change_code = tac.last_change_code
    # Step 2: Fetch the Tac instance in a new session and modify it
    session_1 = session  # Using the existing session
    tac_1 = await session_1.execute(select(Tac).filter_by(tac_id=tac.tac_id))
    tac_1 = tac_1.scalar_one()
    tac_1.code = uuid.uuid4()
    await session_1.commit()
    # Step 3: Fetch the same Tac instance in another session and modify it
    session_2 = session  # Using the same session object, but it's a new transaction after commit
    tac_2 = await session_2.execute(select(Tac).filter_by(tac_id=tac.tac_id))
    tac_2 = tac_2.scalar_one()
    tac_2.code = uuid.uuid4()
    # Step 4: Commit changes in session_2 and check the last_change_code
    await session_2.commit()
    assert tac_2.last_change_code != original_last_change_code
@pytest.mark.asyncio #FlvrForeignKeyID
async def test_invalid_flvr_foreign_key_id(session):
    tac = await TacFactory.create_async(session=session)
    tac.flvr_foreign_key_id=99999
    with pytest.raises(Exception):  # Adjust for the specific DB exception you'd expect
        await session.commit()
@pytest.mark.asyncio #PacID
async def test_invalid_pac_id(session):
    tac = await TacFactory.create_async(session=session)
    tac.pac_id=99999
    with pytest.raises(Exception):  # Adjust for the specific DB exception you'd expect
        await session.commit()
