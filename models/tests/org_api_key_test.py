import pytest
import uuid
from datetime import datetime
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.future import select
from models import Base, OrgApiKey
from models.factory import OrgApiKeyFactory
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
async def test_org_api_key_creation(session):
    org_api_key = await OrgApiKeyFactory.create_async(session=session)
    assert org_api_key.org_api_key_id is not None
@pytest.mark.asyncio
async def test_code_default(session):
    org_api_key = await OrgApiKeyFactory.create_async(session=session)
    assert isinstance(org_api_key.code, uuid.UUID)
@pytest.mark.asyncio
async def test_last_change_code_default_on_creation(session):
    org_api_key = await OrgApiKeyFactory.create_async(session=session)
    assert isinstance(org_api_key.last_change_code, uuid.UUID)
@pytest.mark.asyncio
async def test_last_change_code_default_on_update(session):
    org_api_key = await OrgApiKeyFactory.create_async(session=session)
    initial_code = org_api_key.last_change_code
    org_api_key.code = uuid.uuid4()
    await session.commit()
    assert org_api_key.last_change_code != initial_code
@pytest.mark.asyncio
async def test_date_inserted(session):
    org_api_key = OrgApiKeyFactory.build_async(session=session)
    assert org_api_key.insert_utc_date_time is None
    await session.commit()
    assert isinstance(org_api_key.insert_utc_date_time, datetime)
@pytest.mark.asyncio
async def test_date_updated(session):
    org_api_key = await OrgApiKeyFactory.create_async(session=session)
    initial_time = org_api_key.last_update_utc_date_time
    org_api_key.code = uuid.uuid4()
    await session.commit()
    assert org_api_key.last_update_utc_date_time > initial_time
# @pytest.mark.asyncio
# async def test_string_length_limits(session):
#     long_string = "a" * 300
#     org_api_key = OrgApiKeyFactory(some_varchar_val=long_string, some_text_val=long_string)
#     session.add(org_api_key)
#     # Adjust this for the specific DB limit exception you'd expect if these fields are too long
#     with pytest.raises(Exception):
#         await session.commit()
@pytest.mark.asyncio
async def test_model_deletion(session):
    org_api_key = await OrgApiKeyFactory.create_async(session=session)
    session.delete(org_api_key)
    await session.commit()
    deleted_org_api_key = await session.get(OrgApiKey, org_api_key.org_api_key_id)
    assert deleted_org_api_key is None
@pytest.mark.asyncio
async def test_data_types(session):
    org_api_key = await OrgApiKeyFactory.create_async(session=session)
    # Check the data types for each property
    assert isinstance(org_api_key.org_api_key_id, int)
    assert isinstance(org_api_key.code, uuid.UUID)
    assert isinstance(org_api_key.last_change_code, uuid.UUID)
    assert isinstance(org_api_key.insert_user_id, uuid.UUID)
    assert isinstance(org_api_key.last_update_user_id, uuid.UUID)
    assert org_api_key.api_key_value == "" or isinstance(org_api_key.api_key_value, str)
    assert org_api_key.created_by == "" or isinstance(org_api_key.created_by, str)
    assert isinstance(org_api_key.created_utc_date_time, datetime.datetime)
    assert isinstance(org_api_key.expiration_utc_date_time, datetime.datetime)
    assert isinstance(org_api_key.is_active, bool)
    assert isinstance(org_api_key.is_temp_user_key, bool)
    assert org_api_key.name == "" or isinstance(org_api_key.name, str)
    assert isinstance(org_api_key.organization_id, int)
    assert isinstance(org_api_key.org_customer_id, int)
    # Check for the peek values, assuming they are UUIDs based on your model
    assert isinstance(org_api_key.flvr_foreign_key_code_peek, uuid.UUID)
    assert isinstance(org_api_key.organization_code_peek, uuid.UUID)
    assert isinstance(org_api_key.insert_utc_date_time, datetime.datetime)
    assert isinstance(org_api_key.last_update_utc_date_time, datetime.datetime)
#endset
@pytest.mark.asyncio
async def test_unique_code_constraint(session):
    org_api_key_1 = await OrgApiKeyFactory.create_async(session=session)
    org_api_key_2 = await OrgApiKeyFactory.create_async(session=session)
    org_api_key_2.code = org_api_key_1.code  # Intentionally set the same code
    session.add_all([org_api_key_1, org_api_key_2])
    with pytest.raises(Exception):  # Adjust for the specific DB exception you'd expect
        await session.commit()
@pytest.mark.asyncio
async def test_boolean_fields_default(session):
    org_api_key = await OrgApiKeyFactory.create_async(session=session)
    assert org_api_key.code is not None
    assert org_api_key.last_change_code is not None
    assert org_api_key.insert_user_id is not None
    assert org_api_key.last_update_user_id is not None
    assert org_api_key.insert_utc_date_time is not None
    assert org_api_key.last_update_utc_date_time is not None
    assert org_api_key.api_key_value == ""
    assert org_api_key.created_by == ""
    assert isinstance(org_api_key.created_utc_date_time, datetime.datetime)
    assert isinstance(org_api_key.expiration_utc_date_time, datetime.datetime)
    assert org_api_key.is_active == False
    assert org_api_key.is_temp_user_key == False
    assert org_api_key.name == ""
    assert isinstance(org_api_key.organization_code_peek, uuid.UUID) #OrganizationID
    assert org_api_key.flvr_foreign_key_id > 0
    assert isinstance(org_api_key.org_customer_code_peek, uuid.UUID) #OrgCustomerID
    assert org_api_key.some_utc_date_time_val == datetime(1753, 1, 1)
    assert org_api_key.some_varchar_val == ""
#endset
@pytest.mark.asyncio
async def test_last_change_code_concurrency(session):
    # Step 1: Create a OrgApiKey instance and commit
    org_api_key = await OrgApiKeyFactory.create_async(session=session)
    # Store the original last_change_code
    original_last_change_code = org_api_key.last_change_code
    # Step 2: Fetch the OrgApiKey instance in a new session and modify it
    session_1 = session  # Using the existing session
    org_api_key_1 = await session_1.execute(select(OrgApiKey).filter_by(org_api_key_id=org_api_key.org_api_key_id))
    org_api_key_1 = org_api_key_1.scalar_one()
    org_api_key_1.code = uuid.uuid4()
    await session_1.commit()
    # Step 3: Fetch the same OrgApiKey instance in another session and modify it
    session_2 = session  # Using the same session object, but it's a new transaction after commit
    org_api_key_2 = await session_2.execute(select(OrgApiKey).filter_by(org_api_key_id=org_api_key.org_api_key_id))
    org_api_key_2 = org_api_key_2.scalar_one()
    org_api_key_2.code = uuid.uuid4()
    # Step 4: Commit changes in session_2 and check the last_change_code
    await session_2.commit()
    assert org_api_key_2.last_change_code != original_last_change_code
@pytest.mark.asyncio #FlvrForeignKeyID
async def test_invalid_flvr_foreign_key_id(session):
    org_api_key = await OrgApiKeyFactory.create_async(session=session)
    org_api_key.flvr_foreign_key_id=99999
    with pytest.raises(Exception):  # Adjust for the specific DB exception you'd expect
        await session.commit()
@pytest.mark.asyncio #OrganizationID
async def test_invalid_organization_id(session):
    org_api_key = await OrgApiKeyFactory.create_async(session=session)
    org_api_key.organization_id=99999
    with pytest.raises(Exception):  # Adjust for the specific DB exception you'd expect
        await session.commit()
