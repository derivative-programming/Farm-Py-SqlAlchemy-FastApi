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
    organization = await OrganizationFactory.create_async(session=session)
    assert organization.organization_id is not None
@pytest.mark.asyncio
async def test_code_default(session):
    organization = await OrganizationFactory.create_async(session=session)
    assert isinstance(organization.code, uuid.UUID)
@pytest.mark.asyncio
async def test_last_change_code_default_on_creation(session):
    organization = await OrganizationFactory.create_async(session=session)
    assert isinstance(organization.last_change_code, uuid.UUID)
@pytest.mark.asyncio
async def test_last_change_code_default_on_update(session):
    organization = await OrganizationFactory.create_async(session=session)
    initial_code = organization.last_change_code
    organization.code = uuid.uuid4()
    await session.commit()
    assert organization.last_change_code != initial_code
@pytest.mark.asyncio
async def test_date_inserted(session):
    organization = OrganizationFactory.build_async(session=session)
    assert organization.insert_utc_date_time is None
    await session.commit()
    assert isinstance(organization.insert_utc_date_time, datetime)
@pytest.mark.asyncio
async def test_date_updated(session):
    organization = await OrganizationFactory.create_async(session=session)
    initial_time = organization.last_update_utc_date_time
    organization.code = uuid.uuid4()
    await session.commit()
    assert organization.last_update_utc_date_time > initial_time
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
    organization = await OrganizationFactory.create_async(session=session)
    session.delete(organization)
    await session.commit()
    deleted_organization = await session.get(Organization, organization.organization_id)
    assert deleted_organization is None
@pytest.mark.asyncio
async def test_data_types(session):
    organization = await OrganizationFactory.create_async(session=session)
    # Check the data types for each property
    assert isinstance(organization.organization_id, int)
    assert isinstance(organization.code, uuid.UUID)
    assert isinstance(organization.last_change_code, uuid.UUID)
    assert isinstance(organization.insert_user_id, uuid.UUID)
    assert isinstance(organization.last_update_user_id, uuid.UUID)
    assert organization.name == "" or isinstance(organization.name, str)
    assert isinstance(organization.tac_id, int)
    # Check for the peek values, assuming they are UUIDs based on your model
    assert isinstance(organization.flvr_foreign_key_code_peek, uuid.UUID)
    assert isinstance(organization.tac_code_peek, uuid.UUID)
    assert isinstance(organization.insert_utc_date_time, datetime.datetime)
    assert isinstance(organization.last_update_utc_date_time, datetime.datetime)
#endset
@pytest.mark.asyncio
async def test_unique_code_constraint(session):
    organization_1 = await OrganizationFactory.create_async(session=session)
    organization_2 = await OrganizationFactory.create_async(session=session)
    organization_2.code = organization_1.code  # Intentionally set the same code
    session.add_all([organization_1, organization_2])
    with pytest.raises(Exception):  # Adjust for the specific DB exception you'd expect
        await session.commit()
@pytest.mark.asyncio
async def test_boolean_fields_default(session):
    organization = await OrganizationFactory.create_async(session=session)
    assert organization.code is not None
    assert organization.last_change_code is not None
    assert organization.insert_user_id is not None
    assert organization.last_update_user_id is not None
    assert organization.insert_utc_date_time is not None
    assert organization.last_update_utc_date_time is not None
    assert organization.name == ""
    assert isinstance(organization.tac_code_peek, uuid.UUID) #TacID
    assert organization.flvr_foreign_key_id > 0
    assert organization.some_utc_date_time_val == datetime(1753, 1, 1)
    assert organization.some_varchar_val == ""
#endset
@pytest.mark.asyncio
async def test_last_change_code_concurrency(session):
    # Step 1: Create a Organization instance and commit
    organization = await OrganizationFactory.create_async(session=session)
    # Store the original last_change_code
    original_last_change_code = organization.last_change_code
    # Step 2: Fetch the Organization instance in a new session and modify it
    session_1 = session  # Using the existing session
    organization_1 = await session_1.execute(select(Organization).filter_by(organization_id=organization.organization_id))
    organization_1 = organization_1.scalar_one()
    organization_1.code = uuid.uuid4()
    await session_1.commit()
    # Step 3: Fetch the same Organization instance in another session and modify it
    session_2 = session  # Using the same session object, but it's a new transaction after commit
    organization_2 = await session_2.execute(select(Organization).filter_by(organization_id=organization.organization_id))
    organization_2 = organization_2.scalar_one()
    organization_2.code = uuid.uuid4()
    # Step 4: Commit changes in session_2 and check the last_change_code
    await session_2.commit()
    assert organization_2.last_change_code != original_last_change_code
@pytest.mark.asyncio #FlvrForeignKeyID
async def test_invalid_flvr_foreign_key_id(session):
    organization = await OrganizationFactory.create_async(session=session)
    organization.flvr_foreign_key_id=99999
    with pytest.raises(Exception):  # Adjust for the specific DB exception you'd expect
        await session.commit()
@pytest.mark.asyncio #TacID
async def test_invalid_tac_id(session):
    organization = await OrganizationFactory.create_async(session=session)
    organization.tac_id=99999
    with pytest.raises(Exception):  # Adjust for the specific DB exception you'd expect
        await session.commit()
