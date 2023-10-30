import pytest
import uuid
from datetime import datetime
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.future import select
from models import Base, ErrorLog
from models.factory import ErrorLogFactory
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
async def test_error_log_creation(session):
    error_log = await ErrorLogFactory.create_async(session=session)
    assert error_log.error_log_id is not None
@pytest.mark.asyncio
async def test_code_default(session):
    error_log = await ErrorLogFactory.create_async(session=session)
    assert isinstance(error_log.code, uuid.UUID)
@pytest.mark.asyncio
async def test_last_change_code_default_on_creation(session):
    error_log = await ErrorLogFactory.create_async(session=session)
    assert isinstance(error_log.last_change_code, uuid.UUID)
@pytest.mark.asyncio
async def test_last_change_code_default_on_update(session):
    error_log = await ErrorLogFactory.create_async(session=session)
    initial_code = error_log.last_change_code
    error_log.code = uuid.uuid4()
    await session.commit()
    assert error_log.last_change_code != initial_code
@pytest.mark.asyncio
async def test_date_inserted(session):
    error_log = ErrorLogFactory.build_async(session=session)
    assert error_log.insert_utc_date_time is None
    await session.commit()
    assert isinstance(error_log.insert_utc_date_time, datetime)
@pytest.mark.asyncio
async def test_date_updated(session):
    error_log = await ErrorLogFactory.create_async(session=session)
    initial_time = error_log.last_update_utc_date_time
    error_log.code = uuid.uuid4()
    await session.commit()
    assert error_log.last_update_utc_date_time > initial_time
# @pytest.mark.asyncio
# async def test_string_length_limits(session):
#     long_string = "a" * 300
#     error_log = ErrorLogFactory(some_varchar_val=long_string, some_text_val=long_string)
#     session.add(error_log)
#     # Adjust this for the specific DB limit exception you'd expect if these fields are too long
#     with pytest.raises(Exception):
#         await session.commit()
@pytest.mark.asyncio
async def test_model_deletion(session):
    error_log = await ErrorLogFactory.create_async(session=session)
    session.delete(error_log)
    await session.commit()
    deleted_error_log = await session.get(ErrorLog, error_log.error_log_id)
    assert deleted_error_log is None
@pytest.mark.asyncio
async def test_data_types(session):
    error_log = await ErrorLogFactory.create_async(session=session)
    # Check the data types for each property
    assert isinstance(error_log.error_log_id, int)
    assert isinstance(error_log.code, uuid.UUID)
    assert isinstance(error_log.last_change_code, uuid.UUID)
    assert isinstance(error_log.insert_user_id, uuid.UUID)
    assert isinstance(error_log.last_update_user_id, uuid.UUID)
    assert isinstance(error_log.browser_code, uuid.UUID)
    assert isinstance(error_log.context_code, uuid.UUID)
    assert isinstance(error_log.created_utc_date_time, datetime.datetime)
    assert error_log.description == "" or isinstance(error_log.description, str)
    assert isinstance(error_log.is_client_side_error, bool)
    assert isinstance(error_log.is_resolved, bool)
    assert isinstance(error_log.pac_id, int)
    assert error_log.url == "" or isinstance(error_log.url, str)
    # Check for the peek values, assuming they are UUIDs based on your model
    assert isinstance(error_log.flvr_foreign_key_code_peek, uuid.UUID)
    assert isinstance(error_log.pac_code_peek, uuid.UUID)
    assert isinstance(error_log.insert_utc_date_time, datetime.datetime)
    assert isinstance(error_log.last_update_utc_date_time, datetime.datetime)
#endset
@pytest.mark.asyncio
async def test_unique_code_constraint(session):
    error_log_1 = await ErrorLogFactory.create_async(session=session)
    error_log_2 = await ErrorLogFactory.create_async(session=session)
    error_log_2.code = error_log_1.code  # Intentionally set the same code
    session.add_all([error_log_1, error_log_2])
    with pytest.raises(Exception):  # Adjust for the specific DB exception you'd expect
        await session.commit()
@pytest.mark.asyncio
async def test_boolean_fields_default(session):
    error_log = await ErrorLogFactory.create_async(session=session)
    assert error_log.code is not None
    assert error_log.last_change_code is not None
    assert error_log.insert_user_id is not None
    assert error_log.last_update_user_id is not None
    assert error_log.insert_utc_date_time is not None
    assert error_log.last_update_utc_date_time is not None
    assert isinstance(error_log.browser_code, uuid.UUID)
    assert isinstance(error_log.context_code, uuid.UUID)
    assert isinstance(error_log.created_utc_date_time, datetime.datetime)
    assert error_log.description == ""
    assert error_log.is_client_side_error == False
    assert error_log.is_resolved == False
    assert isinstance(error_log.pac_code_peek, uuid.UUID) #PacID
    assert error_log.flvr_foreign_key_id > 0
    assert error_log.url == ""
    assert error_log.some_utc_date_time_val == datetime(1753, 1, 1)
    assert error_log.some_varchar_val == ""
#endset
@pytest.mark.asyncio
async def test_last_change_code_concurrency(session):
    # Step 1: Create a ErrorLog instance and commit
    error_log = await ErrorLogFactory.create_async(session=session)
    # Store the original last_change_code
    original_last_change_code = error_log.last_change_code
    # Step 2: Fetch the ErrorLog instance in a new session and modify it
    session_1 = session  # Using the existing session
    error_log_1 = await session_1.execute(select(ErrorLog).filter_by(error_log_id=error_log.error_log_id))
    error_log_1 = error_log_1.scalar_one()
    error_log_1.code = uuid.uuid4()
    await session_1.commit()
    # Step 3: Fetch the same ErrorLog instance in another session and modify it
    session_2 = session  # Using the same session object, but it's a new transaction after commit
    error_log_2 = await session_2.execute(select(ErrorLog).filter_by(error_log_id=error_log.error_log_id))
    error_log_2 = error_log_2.scalar_one()
    error_log_2.code = uuid.uuid4()
    # Step 4: Commit changes in session_2 and check the last_change_code
    await session_2.commit()
    assert error_log_2.last_change_code != original_last_change_code
@pytest.mark.asyncio #FlvrForeignKeyID
async def test_invalid_flvr_foreign_key_id(session):
    error_log = await ErrorLogFactory.create_async(session=session)
    error_log.flvr_foreign_key_id=99999
    with pytest.raises(Exception):  # Adjust for the specific DB exception you'd expect
        await session.commit()
@pytest.mark.asyncio #PacID
async def test_invalid_pac_id(session):
    error_log = await ErrorLogFactory.create_async(session=session)
    error_log.pac_id=99999
    with pytest.raises(Exception):  # Adjust for the specific DB exception you'd expect
        await session.commit()
