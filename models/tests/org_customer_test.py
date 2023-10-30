import pytest
import uuid
from datetime import datetime
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.future import select
from models import Base, OrgCustomer
from models.factory import OrgCustomerFactory
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
async def test_org_customer_creation(session):
    org_customer = OrgCustomerFactory(session=session)
    assert org_customer.org_customer_id is not None
@pytest.mark.asyncio
async def test_code_default(session):
    org_customer = OrgCustomerFactory(session=session)
    assert isinstance(org_customer.code, uuid.UUID)
@pytest.mark.asyncio
async def test_last_change_code_default(session):
    org_customer = OrgCustomerFactory(session=session)
    assert isinstance(org_customer.last_change_code, uuid.UUID)
@pytest.mark.asyncio
async def test_last_change_code_changes_on_update(session):
    # Create a org_customer and commit it to the database
    org_customer = OrgCustomerFactory(session=session)
    # Store the initial last_change_code
    initial_last_change_code = org_customer.last_change_code
    # Update the code property of the org_customer
    org_customer.code = uuid.uuid4()  # Generating a new UUID for the code
    # Commit the update
    await session.commit()
    # Assert that the last_change_code has changed after the update
    assert org_customer.last_change_code != initial_last_change_code
    assert isinstance(org_customer.last_change_code, uuid.UUID)
@pytest.mark.asyncio
async def test_date_inserted(session):
    org_customer = OrgCustomerFactory(session=session).build()
    assert org_customer.insert_utc_date_time is None
    session.add(org_customer)
    await session.commit()
    assert isinstance(org_customer.insert_utc_date_time, datetime)
@pytest.mark.asyncio
async def test_date_updated(session):
    org_customer = OrgCustomerFactory(session=session)
    initial_time = org_customer.last_update_utc_date_time
    assert org_customer.customer_id > 0
    assert org_customer.email == ""
    assert org_customer.organization_id > 0
# @pytest.mark.asyncio
# async def test_string_length_limits(session):
#     long_string = "a" * 300
#     org_customer = OrgCustomerFactory(some_varchar_val=long_string, some_text_val=long_string)
#     session.add(org_customer)
#     # Adjust this for the specific DB limit exception you'd expect if these fields are too long
#     with pytest.raises(Exception):
#         await session.commit()
@pytest.mark.asyncio
async def test_model_deletion(session):
    org_customer = OrgCustomerFactory(session=session)
    session.delete(org_customer)
    await session.commit()
    deleted_org_customer = await session.get(OrgCustomer, org_customer.org_customer_id)
    assert deleted_org_customer is None
@pytest.mark.asyncio
async def test_data_types(session):
    org_customer = OrgCustomerFactory(session=session,some_int_val="12345", some_float_val="123.45")
    # Check the data types for each property
    assert isinstance(org_customer.org_customer_id, int)
    assert isinstance(org_customer.code, uuid.UUID)
    assert isinstance(org_customer.last_change_code, uuid.UUID)
    assert isinstance(org_customer.insert_user_id, uuid.UUID)
    assert isinstance(org_customer.last_update_user_id, uuid.UUID)
    assert isinstance(org_customer.insert_utc_date_time, datetime.datetime)
    assert isinstance(org_customer.last_update_utc_date_time, datetime.datetime)
    assert isinstance(org_customer.customer_id, int)
    assert isinstance(org_customer.is_delete_allowed, bool)
    assert isinstance(org_customer.is_edit_allowed, bool)
    assert isinstance(org_customer.organization_id, int)
    assert org_customer.other_flavor == "" or isinstance(org_customer.other_flavor, str)
    assert isinstance(org_customer.some_big_int_val, int)
    org_customer.some_varchar_val = "Changed"
    await session.commit()
    assert org_customer.last_update_utc_date_time > initial_time
@pytest.mark.asyncio
async def test_unique_code_constraint(session):
    org_customer_1 = OrgCustomerFactory(session=session)
    org_customer_2 = OrgCustomerFactory(session=session)
    org_customer_2.code = org_customer_1.code  # Intentionally set the same code
    session.add_all([org_customer_1, org_customer_2])
    with pytest.raises(Exception):  # Adjust for the specific DB exception you'd expect
        await session.commit()
@pytest.mark.asyncio
async def test_boolean_fields_default(session):
    org_customer = OrgCustomerFactory(session=session)
    assert org_customer.code is not None
    assert org_customer.last_change_code is not None
    assert org_customer.insert_user_id is not None
    assert org_customer.last_update_user_id is not None
    assert org_customer.insert_utc_date_time is not None
    assert org_customer.last_update_utc_date_time is not None
    assert isinstance(org_customer.some_utc_date_time_val, datetime.datetime)
    assert org_customer.some_varchar_val == "" or isinstance(org_customer.some_varchar_val, str)
    assert isinstance(org_customer.customer_code_peek, uuid.UUID) #CustomerID
    assert isinstance(org_customer.organization_code_peek, uuid.UUID) #OrganizationID
@pytest.mark.asyncio
async def test_last_change_code_concurrency(session):
    # Step 1: Create a OrgCustomer instance and commit
    org_customer = OrgCustomerFactory(session=session)
    # Store the original last_change_code
    original_last_change_code = org_customer.last_change_code
    # Step 2: Fetch the OrgCustomer instance in a new session and modify it
    session_1 = session  # Using the existing session
    org_customer_1 = await session_1.execute(select(OrgCustomer).filter_by(org_customer_id=org_customer.org_customer_id))
    org_customer_1 = org_customer_1.scalar_one()
    org_customer_1.some_varchar_val = "Change1"
    await session_1.commit()
    # Step 3: Fetch the same OrgCustomer instance in another session and modify it
    session_2 = session  # Using the same session object, but it's a new transaction after commit
    org_customer_2 = await session_2.execute(select(OrgCustomer).filter_by(org_customer_id=org_customer.org_customer_id))
    org_customer_2 = org_customer_2.scalar_one()
    org_customer_2.some_varchar_val = "Change2"
    # Step 4: Commit changes in session_2 and check the last_change_code
    await session_2.commit()
    assert org_customer_2.last_change_code != original_last_change_code
@pytest.mark.asyncio #FlvrForeignKeyID
async def test_invalid_flvr_foreign_key_id(session):
    org_customer = OrgCustomerFactory(session=session,flvr_foreign_key_id=99999)  # Assume no Flavor with ID 99999
    session.add(org_customer)
    with pytest.raises(Exception):  # Adjust for the specific DB exception you'd expect
        await session.commit()
@pytest.mark.asyncio #OrganizationID
async def test_invalid_organization_id(session):
    org_customer = OrgCustomerFactory(session=session,organization_id=99999)  # Assume no Organization with ID 99999
    session.add(org_customer)
    with pytest.raises(Exception):  # Adjust for the specific DB exception you'd expect
        await session.commit()
