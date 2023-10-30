import pytest
import uuid
from datetime import datetime
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.future import select
from models import Base, Customer
from models.factory import CustomerFactory
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
async def test_customer_creation(session):
    customer = await CustomerFactory.create_async(session=session)
    assert customer.customer_id is not None
@pytest.mark.asyncio
async def test_code_default(session):
    customer = await CustomerFactory.create_async(session=session)
    assert isinstance(customer.code, uuid.UUID)
@pytest.mark.asyncio
async def test_last_change_code_default_on_creation(session):
    customer = await CustomerFactory.create_async(session=session)
    assert isinstance(customer.last_change_code, uuid.UUID)
@pytest.mark.asyncio
async def test_last_change_code_default_on_update(session):
    customer = await CustomerFactory.create_async(session=session)
    initial_code = customer.last_change_code
    customer.code = uuid.uuid4()
    await session.commit()
    assert customer.last_change_code != initial_code
@pytest.mark.asyncio
async def test_date_inserted(session):
    customer = CustomerFactory.build_async(session=session)
    assert customer.insert_utc_date_time is None
    await session.commit()
    assert isinstance(customer.insert_utc_date_time, datetime)
@pytest.mark.asyncio
async def test_date_updated(session):
    customer = await CustomerFactory.create_async(session=session)
    initial_time = customer.last_update_utc_date_time
    customer.code = uuid.uuid4()
    await session.commit()
    assert customer.last_update_utc_date_time > initial_time
# @pytest.mark.asyncio
# async def test_string_length_limits(session):
#     long_string = "a" * 300
#     customer = CustomerFactory(some_varchar_val=long_string, some_text_val=long_string)
#     session.add(customer)
#     # Adjust this for the specific DB limit exception you'd expect if these fields are too long
#     with pytest.raises(Exception):
#         await session.commit()
@pytest.mark.asyncio
async def test_model_deletion(session):
    customer = await CustomerFactory.create_async(session=session)
    session.delete(customer)
    await session.commit()
    deleted_customer = await session.get(Customer, customer.customer_id)
    assert deleted_customer is None
@pytest.mark.asyncio
async def test_data_types(session):
    customer = await CustomerFactory.create_async(session=session)
    # Check the data types for each property
    assert isinstance(customer.customer_id, int)
    assert isinstance(customer.code, uuid.UUID)
    assert isinstance(customer.last_change_code, uuid.UUID)
    assert isinstance(customer.insert_user_id, uuid.UUID)
    assert isinstance(customer.last_update_user_id, uuid.UUID)
    assert isinstance(customer.active_organization_id, int)
    assert customer.email == "" or isinstance(customer.email, str)
    assert isinstance(customer.email_confirmed_utc_date_time, datetime.datetime)
    assert customer.first_name == "" or isinstance(customer.first_name, str)
    assert isinstance(customer.forgot_password_key_expiration_utc_date_time, datetime.datetime)
    assert customer.forgot_password_key_value == "" or isinstance(customer.forgot_password_key_value, str)
    assert isinstance(customer.fs_user_code_value, uuid.UUID)
    assert isinstance(customer.is_active, bool)
    assert isinstance(customer.is_email_allowed, bool)
    assert isinstance(customer.is_email_confirmed, bool)
    assert isinstance(customer.is_email_marketing_allowed, bool)
    assert isinstance(customer.is_locked, bool)
    assert isinstance(customer.is_multiple_organizations_allowed, bool)
    assert isinstance(customer.is_verbose_logging_forced, bool)
    assert isinstance(customer.last_login_utc_date_time, datetime.datetime)
    assert customer.last_name == "" or isinstance(customer.last_name, str)
    assert customer.password == "" or isinstance(customer.password, str)
    assert customer.phone == "" or isinstance(customer.phone, str)
    assert customer.province == "" or isinstance(customer.province, str)
    assert isinstance(customer.registration_utc_date_time, datetime.datetime)
    assert isinstance(customer.tac_id, int)
    assert isinstance(customer.utc_offset_in_minutes, int)
    assert customer.zip == "" or isinstance(customer.zip, str)
    # Check for the peek values, assuming they are UUIDs based on your model
    assert isinstance(customer.flvr_foreign_key_code_peek, uuid.UUID)
    assert isinstance(customer.tac_code_peek, uuid.UUID)
    assert isinstance(customer.insert_utc_date_time, datetime.datetime)
    assert isinstance(customer.last_update_utc_date_time, datetime.datetime)
#endset
@pytest.mark.asyncio
async def test_unique_code_constraint(session):
    customer_1 = await CustomerFactory.create_async(session=session)
    customer_2 = await CustomerFactory.create_async(session=session)
    customer_2.code = customer_1.code  # Intentionally set the same code
    session.add_all([customer_1, customer_2])
    with pytest.raises(Exception):  # Adjust for the specific DB exception you'd expect
        await session.commit()
@pytest.mark.asyncio
async def test_boolean_fields_default(session):
    customer = await CustomerFactory.create_async(session=session)
    assert customer.code is not None
    assert customer.last_change_code is not None
    assert customer.insert_user_id is not None
    assert customer.last_update_user_id is not None
    assert customer.insert_utc_date_time is not None
    assert customer.last_update_utc_date_time is not None
    assert customer.active_organization_id == 0
    assert customer.email == ""
    assert isinstance(customer.email_confirmed_utc_date_time, datetime.datetime)
    assert customer.first_name == ""
    assert isinstance(customer.forgot_password_key_expiration_utc_date_time, datetime.datetime)
    assert customer.forgot_password_key_value == ""
    assert isinstance(customer.fs_user_code_value, uuid.UUID)
    assert customer.is_active == False
    assert customer.is_email_allowed == False
    assert customer.is_email_confirmed == False
    assert customer.is_email_marketing_allowed == False
    assert customer.is_locked == False
    assert customer.is_multiple_organizations_allowed == False
    assert customer.is_verbose_logging_forced == False
    assert isinstance(customer.last_login_utc_date_time, datetime.datetime)
    assert customer.last_name == ""
    assert customer.password == ""
    assert customer.phone == ""
    assert customer.province == ""
    assert isinstance(customer.registration_utc_date_time, datetime.datetime)
    assert isinstance(customer.tac_code_peek, uuid.UUID) #TacID
    assert customer.flvr_foreign_key_id > 0
    assert customer.utc_offset_in_minutes == 0
    assert customer.zip == ""
    assert customer.some_utc_date_time_val == datetime(1753, 1, 1)
    assert customer.some_varchar_val == ""
#endset
@pytest.mark.asyncio
async def test_last_change_code_concurrency(session):
    # Step 1: Create a Customer instance and commit
    customer = await CustomerFactory.create_async(session=session)
    # Store the original last_change_code
    original_last_change_code = customer.last_change_code
    # Step 2: Fetch the Customer instance in a new session and modify it
    session_1 = session  # Using the existing session
    customer_1 = await session_1.execute(select(Customer).filter_by(customer_id=customer.customer_id))
    customer_1 = customer_1.scalar_one()
    customer_1.code = uuid.uuid4()
    await session_1.commit()
    # Step 3: Fetch the same Customer instance in another session and modify it
    session_2 = session  # Using the same session object, but it's a new transaction after commit
    customer_2 = await session_2.execute(select(Customer).filter_by(customer_id=customer.customer_id))
    customer_2 = customer_2.scalar_one()
    customer_2.code = uuid.uuid4()
    # Step 4: Commit changes in session_2 and check the last_change_code
    await session_2.commit()
    assert customer_2.last_change_code != original_last_change_code
@pytest.mark.asyncio #FlvrForeignKeyID
async def test_invalid_flvr_foreign_key_id(session):
    customer = await CustomerFactory.create_async(session=session)
    customer.flvr_foreign_key_id=99999
    with pytest.raises(Exception):  # Adjust for the specific DB exception you'd expect
        await session.commit()
@pytest.mark.asyncio #TacID
async def test_invalid_tac_id(session):
    customer = await CustomerFactory.create_async(session=session)
    customer.tac_id=99999
    with pytest.raises(Exception):  # Adjust for the specific DB exception you'd expect
        await session.commit()
