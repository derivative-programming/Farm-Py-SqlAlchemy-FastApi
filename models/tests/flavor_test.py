import pytest
import uuid
from datetime import datetime
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.future import select
from models import Base, Flavor
from models.factory import FlavorFactory
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
async def test_flavor_creation(session):
    flavor = await FlavorFactory.create_async(session=session)
    assert flavor.flavor_id is not None
@pytest.mark.asyncio
async def test_code_default(session):
    flavor = await FlavorFactory.create_async(session=session)
    assert isinstance(flavor.code, uuid.UUID)
@pytest.mark.asyncio
async def test_last_change_code_default_on_creation(session):
    flavor = await FlavorFactory.create_async(session=session)
    assert isinstance(flavor.last_change_code, uuid.UUID)
@pytest.mark.asyncio
async def test_last_change_code_default_on_update(session):
    flavor = await FlavorFactory.create_async(session=session)
    initial_code = flavor.last_change_code
    flavor.code = uuid.uuid4()
    await session.commit()
    assert flavor.last_change_code != initial_code
@pytest.mark.asyncio
async def test_date_inserted(session):
    flavor = FlavorFactory.build_async(session=session)
    assert flavor.insert_utc_date_time is None
    await session.commit()
    assert isinstance(flavor.insert_utc_date_time, datetime)
@pytest.mark.asyncio
async def test_date_updated(session):
    flavor = await FlavorFactory.create_async(session=session)
    initial_time = flavor.last_update_utc_date_time
    flavor.code = uuid.uuid4()
    await session.commit()
    assert flavor.last_update_utc_date_time > initial_time
# @pytest.mark.asyncio
# async def test_string_length_limits(session):
#     long_string = "a" * 300
#     flavor = FlavorFactory(some_varchar_val=long_string, some_text_val=long_string)
#     session.add(flavor)
#     # Adjust this for the specific DB limit exception you'd expect if these fields are too long
#     with pytest.raises(Exception):
#         await session.commit()
@pytest.mark.asyncio
async def test_model_deletion(session):
    flavor = await FlavorFactory.create_async(session=session)
    session.delete(flavor)
    await session.commit()
    deleted_flavor = await session.get(Flavor, flavor.flavor_id)
    assert deleted_flavor is None
@pytest.mark.asyncio
async def test_data_types(session):
    flavor = await FlavorFactory.create_async(session=session)
    # Check the data types for each property
    assert isinstance(flavor.flavor_id, int)
    assert isinstance(flavor.code, uuid.UUID)
    assert isinstance(flavor.last_change_code, uuid.UUID)
    assert isinstance(flavor.insert_user_id, uuid.UUID)
    assert isinstance(flavor.last_update_user_id, uuid.UUID)
    assert flavor.description == "" or isinstance(flavor.description, str)
    assert isinstance(flavor.display_order, int)
    assert isinstance(flavor.is_active, bool)
    assert flavor.lookup_enum_name == "" or isinstance(flavor.lookup_enum_name, str)
    assert flavor.name == "" or isinstance(flavor.name, str)
    assert isinstance(flavor.pac_id, int)
    # Check for the peek values, assuming they are UUIDs based on your model
    assert isinstance(flavor.flvr_foreign_key_code_peek, uuid.UUID)
    assert isinstance(flavor.pac_code_peek, uuid.UUID)
    assert isinstance(flavor.insert_utc_date_time, datetime.datetime)
    assert isinstance(flavor.last_update_utc_date_time, datetime.datetime)
#endset
@pytest.mark.asyncio
async def test_unique_code_constraint(session):
    flavor_1 = await FlavorFactory.create_async(session=session)
    flavor_2 = await FlavorFactory.create_async(session=session)
    flavor_2.code = flavor_1.code  # Intentionally set the same code
    session.add_all([flavor_1, flavor_2])
    with pytest.raises(Exception):  # Adjust for the specific DB exception you'd expect
        await session.commit()
@pytest.mark.asyncio
async def test_boolean_fields_default(session):
    flavor = await FlavorFactory.create_async(session=session)
    assert flavor.code is not None
    assert flavor.last_change_code is not None
    assert flavor.insert_user_id is not None
    assert flavor.last_update_user_id is not None
    assert flavor.insert_utc_date_time is not None
    assert flavor.last_update_utc_date_time is not None
    assert flavor.description == ""
    assert flavor.display_order == 0
    assert flavor.is_active == False
    assert flavor.lookup_enum_name == ""
    assert flavor.name == ""
    assert isinstance(flavor.pac_code_peek, uuid.UUID) #PacID
    assert flavor.flvr_foreign_key_id > 0
    assert flavor.some_utc_date_time_val == datetime(1753, 1, 1)
    assert flavor.some_varchar_val == ""
#endset
@pytest.mark.asyncio
async def test_last_change_code_concurrency(session):
    # Step 1: Create a Flavor instance and commit
    flavor = await FlavorFactory.create_async(session=session)
    # Store the original last_change_code
    original_last_change_code = flavor.last_change_code
    # Step 2: Fetch the Flavor instance in a new session and modify it
    session_1 = session  # Using the existing session
    flavor_1 = await session_1.execute(select(Flavor).filter_by(flavor_id=flavor.flavor_id))
    flavor_1 = flavor_1.scalar_one()
    flavor_1.code = uuid.uuid4()
    await session_1.commit()
    # Step 3: Fetch the same Flavor instance in another session and modify it
    session_2 = session  # Using the same session object, but it's a new transaction after commit
    flavor_2 = await session_2.execute(select(Flavor).filter_by(flavor_id=flavor.flavor_id))
    flavor_2 = flavor_2.scalar_one()
    flavor_2.code = uuid.uuid4()
    # Step 4: Commit changes in session_2 and check the last_change_code
    await session_2.commit()
    assert flavor_2.last_change_code != original_last_change_code
@pytest.mark.asyncio #FlvrForeignKeyID
async def test_invalid_flvr_foreign_key_id(session):
    flavor = await FlavorFactory.create_async(session=session)
    flavor.flvr_foreign_key_id=99999
    with pytest.raises(Exception):  # Adjust for the specific DB exception you'd expect
        await session.commit()
@pytest.mark.asyncio #PacID
async def test_invalid_pac_id(session):
    flavor = await FlavorFactory.create_async(session=session)
    flavor.pac_id=99999
    with pytest.raises(Exception):  # Adjust for the specific DB exception you'd expect
        await session.commit()
