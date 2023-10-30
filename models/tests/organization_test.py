import pytest
import uuid
from datetime import datetime
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.future import select
from models import Base, Organization
from models.factory import OrganizationFactory
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
async def test_organization_creation(session):
    organization = OrganizationFactory(session=session)
    assert organization.organization_id is not None
@pytest.mark.asyncio
async def test_code_default(session):
    organization = OrganizationFactory(session=session)
    assert isinstance(organization.code, uuid.UUID)
@pytest.mark.asyncio
async def test_last_change_code_default(session):
    organization = OrganizationFactory(session=session)
    assert isinstance(organization.last_change_code, uuid.UUID)
@pytest.mark.asyncio
async def test_last_change_code_changes_on_update(session):
    # Create a organization and commit it to the database
    organization = OrganizationFactory(session=session)
    # Store the initial last_change_code
    initial_last_change_code = organization.last_change_code
    # Update the code property of the organization
    organization.code = uuid.uuid4()  # Generating a new UUID for the code
    # Commit the update
    await session.commit()
    # Assert that the last_change_code has changed after the update
    assert organization.last_change_code != initial_last_change_code
    assert isinstance(organization.last_change_code, uuid.UUID)
@pytest.mark.asyncio
async def test_date_inserted(session):
    organization = OrganizationFactory(session=session).build()
    assert organization.insert_utc_date_time is None
    session.add(organization)
    await session.commit()
    assert isinstance(organization.insert_utc_date_time, datetime)
@pytest.mark.asyncio
async def test_date_updated(session):
    organization = OrganizationFactory(session=session)
    initial_time = organization.last_update_utc_date_time
    assert organization.name == ""
    assert organization.tac_id > 0
# @pytest.mark.asyncio
# async def test_string_length_limits(session):
#     long_string = "a" * 300
#     organization = OrganizationFactory(some_varchar_val=long_string, some_text_val=long_string)
#     session.add(organization)
#     # Adjust this for the specific DB limit exception you'd expect if these fields are too long
#     with pytest.raises(Exception):
#         await session.commit()
@pytest.mark.asyncio
async def test_model_deletion(session):
    organization = OrganizationFactory(session=session)
    session.delete(organization)
    await session.commit()
    deleted_organization = await session.get(Organization, organization.organization_id)
    assert deleted_organization is None
@pytest.mark.asyncio
async def test_data_types(session):
    organization = OrganizationFactory(session=session,some_int_val="12345", some_float_val="123.45")
    # Check the data types for each property
    assert isinstance(organization.organization_id, int)
    assert isinstance(organization.code, uuid.UUID)
    assert isinstance(organization.last_change_code, uuid.UUID)
    assert isinstance(organization.insert_user_id, uuid.UUID)
    assert isinstance(organization.last_update_user_id, uuid.UUID)
    assert isinstance(organization.insert_utc_date_time, datetime.datetime)
    assert isinstance(organization.last_update_utc_date_time, datetime.datetime)
    assert isinstance(organization.tac_id, int)
    assert organization.other_flavor == "" or isinstance(organization.other_flavor, str)
    assert isinstance(organization.some_big_int_val, int)
    organization.some_varchar_val = "Changed"
    await session.commit()
    assert organization.last_update_utc_date_time > initial_time
@pytest.mark.asyncio
async def test_unique_code_constraint(session):
    organization_1 = OrganizationFactory(session=session)
    organization_2 = OrganizationFactory(session=session)
    organization_2.code = organization_1.code  # Intentionally set the same code
    session.add_all([organization_1, organization_2])
    with pytest.raises(Exception):  # Adjust for the specific DB exception you'd expect
        await session.commit()
@pytest.mark.asyncio
async def test_boolean_fields_default(session):
    organization = OrganizationFactory(session=session)
    assert organization.code is not None
    assert organization.last_change_code is not None
    assert organization.insert_user_id is not None
    assert organization.last_update_user_id is not None
    assert organization.insert_utc_date_time is not None
    assert organization.last_update_utc_date_time is not None
    assert isinstance(organization.some_utc_date_time_val, datetime.datetime)
    assert organization.some_varchar_val == "" or isinstance(organization.some_varchar_val, str)
    assert isinstance(organization.tac_code_peek, uuid.UUID) #TacID
@pytest.mark.asyncio
async def test_last_change_code_concurrency(session):
    # Step 1: Create a Organization instance and commit
    organization = OrganizationFactory(session=session)
    # Store the original last_change_code
    original_last_change_code = organization.last_change_code
    # Step 2: Fetch the Organization instance in a new session and modify it
    session_1 = session  # Using the existing session
    organization_1 = await session_1.execute(select(Organization).filter_by(organization_id=organization.organization_id))
    organization_1 = organization_1.scalar_one()
    organization_1.some_varchar_val = "Change1"
    await session_1.commit()
    # Step 3: Fetch the same Organization instance in another session and modify it
    session_2 = session  # Using the same session object, but it's a new transaction after commit
    organization_2 = await session_2.execute(select(Organization).filter_by(organization_id=organization.organization_id))
    organization_2 = organization_2.scalar_one()
    organization_2.some_varchar_val = "Change2"
    # Step 4: Commit changes in session_2 and check the last_change_code
    await session_2.commit()
    assert organization_2.last_change_code != original_last_change_code
@pytest.mark.asyncio #FlvrForeignKeyID
async def test_invalid_flvr_foreign_key_id(session):
    organization = OrganizationFactory(session=session,flvr_foreign_key_id=99999)  # Assume no Flavor with ID 99999
    session.add(organization)
    with pytest.raises(Exception):  # Adjust for the specific DB exception you'd expect
        await session.commit()
@pytest.mark.asyncio #TacID
async def test_invalid_tac_id(session):
    organization = OrganizationFactory(session=session,tac_id=99999)  # Assume no Tac with ID 99999
    session.add(organization)
    with pytest.raises(Exception):  # Adjust for the specific DB exception you'd expect
        await session.commit()
