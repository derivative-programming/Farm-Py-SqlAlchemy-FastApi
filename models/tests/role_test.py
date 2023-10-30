import pytest
import uuid
from datetime import datetime
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.future import select
from models import Base, Role
from models.factory import RoleFactory
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
async def test_role_creation(session):
    role = await RoleFactory.create_async(session=session)
    assert role.role_id is not None
@pytest.mark.asyncio
async def test_code_default(session):
    role = await RoleFactory.create_async(session=session)
    assert isinstance(role.code, uuid.UUID)
@pytest.mark.asyncio
async def test_last_change_code_default_on_creation(session):
    role = await RoleFactory.create_async(session=session)
    assert isinstance(role.last_change_code, uuid.UUID)
@pytest.mark.asyncio
async def test_last_change_code_default_on_update(session):
    role = await RoleFactory.create_async(session=session)
    initial_code = role.last_change_code
    role.code = uuid.uuid4()
    await session.commit()
    assert role.last_change_code != initial_code
@pytest.mark.asyncio
async def test_date_inserted(session):
    role = RoleFactory.build_async(session=session)
    assert role.insert_utc_date_time is None
    await session.commit()
    assert isinstance(role.insert_utc_date_time, datetime)
@pytest.mark.asyncio
async def test_date_updated(session):
    role = await RoleFactory.create_async(session=session)
    initial_time = role.last_update_utc_date_time
    role.code = uuid.uuid4()
    await session.commit()
    assert role.last_update_utc_date_time > initial_time
# @pytest.mark.asyncio
# async def test_string_length_limits(session):
#     long_string = "a" * 300
#     role = RoleFactory(some_varchar_val=long_string, some_text_val=long_string)
#     session.add(role)
#     # Adjust this for the specific DB limit exception you'd expect if these fields are too long
#     with pytest.raises(Exception):
#         await session.commit()
@pytest.mark.asyncio
async def test_model_deletion(session):
    role = await RoleFactory.create_async(session=session)
    session.delete(role)
    await session.commit()
    deleted_role = await session.get(Role, role.role_id)
    assert deleted_role is None
@pytest.mark.asyncio
async def test_data_types(session):
    role = await RoleFactory.create_async(session=session)
    # Check the data types for each property
    assert isinstance(role.role_id, int)
    assert isinstance(role.code, uuid.UUID)
    assert isinstance(role.last_change_code, uuid.UUID)
    assert isinstance(role.insert_user_id, uuid.UUID)
    assert isinstance(role.last_update_user_id, uuid.UUID)
    assert role.description == "" or isinstance(role.description, str)
    assert isinstance(role.display_order, int)
    assert isinstance(role.is_active, bool)
    assert role.lookup_enum_name == "" or isinstance(role.lookup_enum_name, str)
    assert role.name == "" or isinstance(role.name, str)
    assert isinstance(role.pac_id, int)
    # Check for the peek values, assuming they are UUIDs based on your model
    assert isinstance(role.flvr_foreign_key_code_peek, uuid.UUID)
    assert isinstance(role.pac_code_peek, uuid.UUID)
    assert isinstance(role.insert_utc_date_time, datetime.datetime)
    assert isinstance(role.last_update_utc_date_time, datetime.datetime)
#endset
@pytest.mark.asyncio
async def test_unique_code_constraint(session):
    role_1 = await RoleFactory.create_async(session=session)
    role_2 = await RoleFactory.create_async(session=session)
    role_2.code = role_1.code  # Intentionally set the same code
    session.add_all([role_1, role_2])
    with pytest.raises(Exception):  # Adjust for the specific DB exception you'd expect
        await session.commit()
@pytest.mark.asyncio
async def test_boolean_fields_default(session):
    role = await RoleFactory.create_async(session=session)
    assert role.code is not None
    assert role.last_change_code is not None
    assert role.insert_user_id is not None
    assert role.last_update_user_id is not None
    assert role.insert_utc_date_time is not None
    assert role.last_update_utc_date_time is not None
    assert role.description == ""
    assert role.display_order == 0
    assert role.is_active == False
    assert role.lookup_enum_name == ""
    assert role.name == ""
    assert isinstance(role.pac_code_peek, uuid.UUID) #PacID
    assert role.flvr_foreign_key_id > 0
    assert role.some_utc_date_time_val == datetime(1753, 1, 1)
    assert role.some_varchar_val == ""
#endset
@pytest.mark.asyncio
async def test_last_change_code_concurrency(session):
    # Step 1: Create a Role instance and commit
    role = await RoleFactory.create_async(session=session)
    # Store the original last_change_code
    original_last_change_code = role.last_change_code
    # Step 2: Fetch the Role instance in a new session and modify it
    session_1 = session  # Using the existing session
    role_1 = await session_1.execute(select(Role).filter_by(role_id=role.role_id))
    role_1 = role_1.scalar_one()
    role_1.code = uuid.uuid4()
    await session_1.commit()
    # Step 3: Fetch the same Role instance in another session and modify it
    session_2 = session  # Using the same session object, but it's a new transaction after commit
    role_2 = await session_2.execute(select(Role).filter_by(role_id=role.role_id))
    role_2 = role_2.scalar_one()
    role_2.code = uuid.uuid4()
    # Step 4: Commit changes in session_2 and check the last_change_code
    await session_2.commit()
    assert role_2.last_change_code != original_last_change_code
@pytest.mark.asyncio #FlvrForeignKeyID
async def test_invalid_flvr_foreign_key_id(session):
    role = await RoleFactory.create_async(session=session)
    role.flvr_foreign_key_id=99999
    with pytest.raises(Exception):  # Adjust for the specific DB exception you'd expect
        await session.commit()
@pytest.mark.asyncio #PacID
async def test_invalid_pac_id(session):
    role = await RoleFactory.create_async(session=session)
    role.pac_id=99999
    with pytest.raises(Exception):  # Adjust for the specific DB exception you'd expect
        await session.commit()
