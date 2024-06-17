# models/factory/tests/customer_async_test.py
"""
    #TODO add comment
"""
import uuid
import asyncio
import time
import math
from decimal import Decimal
from datetime import datetime, date, timedelta
from typing import AsyncGenerator
from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select
from sqlalchemy import event
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
import pytest
import pytest_asyncio
from models import Base, Customer
from models.factory import CustomerFactory
DATABASE_URL = "sqlite+aiosqlite:///:memory:"
class TestCustomerFactoryAsync:
    """
    #TODO add comment
    """
    @pytest.fixture(scope="function")
    def event_loop(self) -> asyncio.AbstractEventLoop:
        """
        #TODO add comment
        """
        loop = asyncio.get_event_loop_policy().new_event_loop()
        yield loop
        loop.close()
    @pytest.fixture(scope="function")
    def engine(self):
        """
        #TODO add comment
        """
        engine = create_async_engine(DATABASE_URL, echo=False)
        yield engine
        engine.sync_engine.dispose()
    @pytest_asyncio.fixture(scope="function")
    async def session(self, engine) -> AsyncGenerator[AsyncSession, None]:
        """
        #TODO add comment
        """
        @event.listens_for(engine.sync_engine, "connect")
        def set_sqlite_pragma(dbapi_connection, connection_record):
            cursor = dbapi_connection.cursor()
            cursor.execute("PRAGMA foreign_keys=ON")
            cursor.close()
        async with engine.begin() as connection:
            await connection.begin_nested()
            await connection.run_sync(Base.metadata.drop_all)
            await connection.run_sync(Base.metadata.create_all)
            TestingSessionLocal = sessionmaker(
                expire_on_commit=False,
                class_=AsyncSession,
                bind=engine,
            )
            async with TestingSessionLocal(bind=connection) as session:
                @event.listens_for(
                    session.sync_session, "after_transaction_end"
                )
                def end_savepoint(session, transaction):
                    if connection.closed:
                        return
                    if not connection.in_nested_transaction():
                        connection.sync_connection.begin_nested()
                yield session
                await session.flush()
                await session.rollback()
    @pytest.mark.asyncio
    async def test_customer_creation(self, session):
        """
        #TODO add comment
        """
        customer = await CustomerFactory.create_async(session=session)
        assert customer.customer_id is not None
    @pytest.mark.asyncio
    async def test_code_default(self, session):
        """
        #TODO add comment
        """
        customer = await CustomerFactory.create_async(session=session)
        assert isinstance(customer.code, uuid.UUID)
    @pytest.mark.asyncio
    async def test_last_change_code_default_on_build(self, session):
        """
        #TODO add comment
        """
        customer: Customer = await CustomerFactory.build_async(session=session)
        assert customer.last_change_code == 0
    @pytest.mark.asyncio
    async def test_last_change_code_default_on_creation(self, session):
        """
        #TODO add comment
        """
        customer: Customer = await CustomerFactory.create_async(session=session)
        assert customer.last_change_code == 1
    @pytest.mark.asyncio
    async def test_last_change_code_default_on_update(self, session):
        """
        #TODO add comment
        """
        customer = await CustomerFactory.create_async(session=session)
        initial_code = customer.last_change_code
        customer.code = uuid.uuid4()
        await session.commit()
        assert customer.last_change_code != initial_code
    @pytest.mark.asyncio
    async def test_date_inserted_on_build(self, session):
        """
        #TODO add comment
        """
        customer = await CustomerFactory.build_async(session=session)
        assert customer.insert_utc_date_time is not None
        assert isinstance(customer.insert_utc_date_time, datetime)
    @pytest.mark.asyncio
    async def test_date_inserted_on_initial_save(self, session):
        """
        #TODO add comment
        """
        customer = await CustomerFactory.build_async(session=session)
        assert customer.insert_utc_date_time is not None
        assert isinstance(customer.insert_utc_date_time, datetime)
        initial_time = datetime.utcnow() + timedelta(days=-1)
        customer.code = uuid.uuid4()
        session.add(customer)
        await session.commit()
        assert customer.insert_utc_date_time > initial_time
    @pytest.mark.asyncio
    async def test_date_inserted_on_second_save(self, session):
        """
        #TODO add comment
        """
        customer = await CustomerFactory.create_async(session=session)
        assert customer.insert_utc_date_time is not None
        assert isinstance(customer.insert_utc_date_time, datetime)
        initial_time = customer.insert_utc_date_time
        customer.code = uuid.uuid4()
        time.sleep(1)
        await session.commit()
        assert customer.insert_utc_date_time == initial_time
    @pytest.mark.asyncio
    async def test_date_updated_on_build(self, session):
        """
        #TODO add comment
        """
        customer = await CustomerFactory.build_async(session=session)
        assert customer.last_update_utc_date_time is not None
        assert isinstance(customer.last_update_utc_date_time, datetime)
    @pytest.mark.asyncio
    async def test_date_updated_on_initial_save(self, session):
        """
        #TODO add comment
        """
        customer = await CustomerFactory.build_async(session=session)
        assert customer.last_update_utc_date_time is not None
        assert isinstance(customer.last_update_utc_date_time, datetime)
        initial_time = datetime.utcnow() + timedelta(days=-1)
        customer.code = uuid.uuid4()
        session.add(customer)
        await session.commit()
        assert customer.last_update_utc_date_time > initial_time
    @pytest.mark.asyncio
    async def test_date_updated_on_second_save(self, session):
        """
        #TODO add comment
        """
        customer = await CustomerFactory.create_async(session=session)
        assert customer.last_update_utc_date_time is not None
        assert isinstance(customer.last_update_utc_date_time, datetime)
        initial_time = customer.last_update_utc_date_time
        customer.code = uuid.uuid4()
        time.sleep(1)
        await session.commit()
        assert customer.last_update_utc_date_time > initial_time
    @pytest.mark.asyncio
    async def test_model_deletion(self, session):
        """
        #TODO add comment
        """
        customer = await CustomerFactory.create_async(session=session)
        await session.delete(customer)
        await session.commit()
        # Construct the select statement
        stmt = select(Customer).where(
            Customer._customer_id == customer.customer_id)  # pylint: disable=protected-access
        # Execute the statement asynchronously
        result = await session.execute(stmt)
        # Fetch all results
        deleted_customer = result.scalars().first()
        # deleted_customer = await session.query(Customer).filter_by(
        # customer_id=customer.customer_id).first()
        assert deleted_customer is None
    @pytest.mark.asyncio
    async def test_data_types(self, session):
        """
        #TODO add comment
        """
        customer = await CustomerFactory.create_async(session=session)
        assert isinstance(customer.customer_id, int)
        assert isinstance(customer.code, uuid.UUID)
        assert isinstance(customer.last_change_code, int)
        assert isinstance(customer.insert_user_id, uuid.UUID)
        assert isinstance(customer.last_update_user_id, uuid.UUID)
        assert isinstance(customer.active_organization_id, int)
        assert customer.email == "" or isinstance(
            customer.email, str)
        assert isinstance(customer.email_confirmed_utc_date_time, datetime)
        assert customer.first_name == "" or isinstance(customer.first_name, str)
        assert isinstance(customer.forgot_password_key_expiration_utc_date_time, datetime)
        assert customer.forgot_password_key_value == "" or isinstance(customer.forgot_password_key_value, str)
        assert isinstance(customer.fs_user_code_value, uuid.UUID)
        assert isinstance(customer.is_active, bool)
        assert isinstance(customer.is_email_allowed, bool)
        assert isinstance(customer.is_email_confirmed, bool)
        assert isinstance(customer.is_email_marketing_allowed, bool)
        assert isinstance(customer.is_locked, bool)
        assert isinstance(customer.is_multiple_organizations_allowed, bool)
        assert isinstance(customer.is_verbose_logging_forced, bool)
        assert isinstance(customer.last_login_utc_date_time, datetime)
        assert customer.last_name == "" or isinstance(customer.last_name, str)
        assert customer.password == "" or isinstance(customer.password, str)
        assert customer.phone == "" or isinstance(
            customer.phone, str)
        assert customer.province == "" or isinstance(customer.province, str)
        assert isinstance(customer.registration_utc_date_time, datetime)
        assert isinstance(customer.tac_id, int)
        assert isinstance(customer.utc_offset_in_minutes, int)
        assert customer.zip == "" or isinstance(customer.zip, str)
        # Check for the peek values
# endset
        # activeOrganizationID,
        # email,
        # emailConfirmedUTCDateTime
        # firstName,
        # forgotPasswordKeyExpirationUTCDateTime
        # forgotPasswordKeyValue,
        # fSUserCodeValue,
        # isActive,
        # isEmailAllowed,
        # isEmailConfirmed,
        # isEmailMarketingAllowed,
        # isLocked,
        # isMultipleOrganizationsAllowed,
        # isVerboseLoggingForced,
        # lastLoginUTCDateTime
        # lastName,
        # password,
        # phone,
        # province,
        # registrationUTCDateTime
        # tacID
        assert isinstance(customer.tac_code_peek, uuid.UUID)
        # uTCOffsetInMinutes,
        # zip,
# endset
        assert isinstance(customer.insert_utc_date_time, datetime)
        assert isinstance(customer.last_update_utc_date_time, datetime)
    @pytest.mark.asyncio
    async def test_unique_code_constraint(self, session):
        """
        #TODO add comment
        """
        customer_1 = await CustomerFactory.create_async(session=session)
        customer_2 = await CustomerFactory.create_async(session=session)
        customer_2.code = customer_1.code
        session.add_all([customer_1, customer_2])
        with pytest.raises(Exception):
            await session.commit()
        await session.rollback()
    @pytest.mark.asyncio
    async def test_fields_default(self):
        """
        #TODO add comment
        """
        customer = Customer()
        assert customer.code is not None
        assert customer.last_change_code is not None
        assert customer.insert_user_id is not None
        assert customer.last_update_user_id is not None
        assert customer.insert_utc_date_time is not None
        assert customer.last_update_utc_date_time is not None
# endset
        # activeOrganizationID,
        # email,
        # emailConfirmedUTCDateTime
        # firstName,
        # forgotPasswordKeyExpirationUTCDateTime
        # forgotPasswordKeyValue,
        # fSUserCodeValue,
        # isActive,
        # isEmailAllowed,
        # isEmailConfirmed,
        # isEmailMarketingAllowed,
        # isLocked,
        # isMultipleOrganizationsAllowed,
        # isVerboseLoggingForced,
        # lastLoginUTCDateTime
        # lastName,
        # password,
        # phone,
        # province,
        # registrationUTCDateTime
        # TacID
        assert isinstance(customer.tac_code_peek, uuid.UUID)
        # uTCOffsetInMinutes,
        # zip,
# endset
        assert customer.active_organization_id == 0
        assert customer.email == ""
        assert customer.email_confirmed_utc_date_time == datetime(1753, 1, 1)
        assert customer.first_name == ""
        assert customer.forgot_password_key_expiration_utc_date_time == datetime(1753, 1, 1)
        assert customer.forgot_password_key_value == ""
        assert isinstance(customer.fs_user_code_value, uuid.UUID)
        assert customer.is_active is False
        assert customer.is_email_allowed is False
        assert customer.is_email_confirmed is False
        assert customer.is_email_marketing_allowed is False
        assert customer.is_locked is False
        assert customer.is_multiple_organizations_allowed is False
        assert customer.is_verbose_logging_forced is False
        assert customer.last_login_utc_date_time == datetime(1753, 1, 1)
        assert customer.last_name == ""
        assert customer.password == ""
        assert customer.phone == ""
        assert customer.province == ""
        assert customer.registration_utc_date_time == datetime(1753, 1, 1)
        assert customer.tac_id == 0
        assert customer.utc_offset_in_minutes == 0
        assert customer.zip == ""
# endset
    @pytest.mark.asyncio
    async def test_last_change_code_concurrency(self, session):
        """
        #TODO add comment
        """
        customer = await CustomerFactory.create_async(session=session)
        original_last_change_code = customer.last_change_code
        stmt = select(Customer).where(
            Customer._customer_id == customer.customer_id)  # pylint: disable=protected-access
        result = await session.execute(stmt)
        customer_1 = result.scalars().first()
        # customer_1 = await session.query(Customer).filter_by(
        # customer_id=customer.customer_id).first()
        customer_1.code = uuid.uuid4()
        await session.commit()
        stmt = select(Customer).where(
            Customer._customer_id == customer.customer_id)  # pylint: disable=protected-access
        result = await session.execute(stmt)
        customer_2 = result.scalars().first()
        # customer_2 = await session.query(Customer).filter_by(
        # customer_id=customer.customer_id).first()
        customer_2.code = uuid.uuid4()
        await session.commit()
        assert customer_2.last_change_code != original_last_change_code
# endset
    # activeOrganizationID,
    # email,
    # emailConfirmedUTCDateTime
    # firstName,
    # forgotPasswordKeyExpirationUTCDateTime
    # forgotPasswordKeyValue,
    # fSUserCodeValue,
    # isActive,
    # isEmailAllowed,
    # isEmailConfirmed,
    # isEmailMarketingAllowed,
    # isLocked,
    # isMultipleOrganizationsAllowed,
    # isVerboseLoggingForced,
    # lastLoginUTCDateTime
    # lastName,
    # password,
    # phone,
    # province,
    # registrationUTCDateTime
    # TacID
    @pytest.mark.asyncio
    async def test_invalid_tac_id(self, session):
        """
        #TODO add comment
        """
        customer = await CustomerFactory.create_async(session=session)
        customer.tac_id = 99999
        with pytest.raises(IntegrityError):
            await session.commit()
        await session.rollback()
    # uTCOffsetInMinutes,
    # zip,
# endset
