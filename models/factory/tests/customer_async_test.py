# models/factory/tests/customer_async_test.py
# pylint: disable=unused-argument
"""
This module contains unit tests for the asynchronous
operations of the CustomerFactory class.
"""
import asyncio
import math
import time
import uuid
from datetime import date, datetime, timedelta
from decimal import Decimal
from typing import AsyncGenerator, Generator
import pytest
import pytest_asyncio
from sqlalchemy import event
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.future import select
from sqlalchemy.orm import sessionmaker
from models import Base, Customer
from models.factory import CustomerFactory
DATABASE_URL = "sqlite+aiosqlite:///:memory:"
class TestCustomerFactoryAsync:
    """
    This class contains unit tests for the asynchronous
    operations of the CustomerFactory class.
    """
    @pytest.fixture(scope="function")
    def event_loop(self) -> Generator[asyncio.AbstractEventLoop, None, None]:
        """
        Fixture that returns an asyncio event loop for the test functions.
        """
        loop = asyncio.get_event_loop_policy().new_event_loop()
        yield loop
        loop.close()
    @pytest.fixture(scope="function")
    def engine(self):
        """
        Fixture that returns an async engine for the test functions.
        """
        engine = create_async_engine(DATABASE_URL, echo=False)
        yield engine
        engine.sync_engine.dispose()
    @pytest_asyncio.fixture(scope="function")
    async def session(self, engine) -> AsyncGenerator[AsyncSession, None]:
        """
        Fixture that returns an async session for the test functions.
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
            TestingSessionLocal = sessionmaker(  # pylint: disable=invalid-name
                expire_on_commit=False,
                class_=AsyncSession,
                bind=engine,
            )
            async with TestingSessionLocal(bind=connection) as session:  # type: ignore # noqa: E501
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
        Test case for creating a customer
        asynchronously.
        Args:
            session: The database session to use.
        Returns:
            None
        Raises:
            AssertionError: If the customer ID
                is None after creation.
        """
        customer = await CustomerFactory.create_async(
            session=session)
        assert customer.customer_id is not None
    @pytest.mark.asyncio
    async def test_code_default(self, session):
        """
        Test case for checking the default value of the code attribute.
        Args:
            session: The database session to use.
        Returns:
            None
        Raises:
            AssertionError: If the code attribute is not
                an instance of uuid.UUID.
        """
        customer = await CustomerFactory.create_async(
            session=session)
        assert isinstance(customer.code, uuid.UUID)
    @pytest.mark.asyncio
    async def test_last_change_code_default_on_build(self, session):
        """
        Test case for checking the default value of the
        last_change_code attribute when using the build_async method.
        Args:
            session: The database session to use.
        Returns:
            None
        Raises:
            AssertionError: If the last_change_code attribute is not 0.
        """
        customer: Customer = await CustomerFactory.build_async(
            session=session)
        assert customer.last_change_code == 0
    @pytest.mark.asyncio
    async def test_last_change_code_default_on_creation(self, session):
        """
        Test case for checking the default value of the
        last_change_code attribute when using the create_async method.
        Args:
            session: The database session to use.
        Returns:
            None
        Raises:
            AssertionError: If the last_change_code attribute is not 1.
        """
        customer: Customer = await CustomerFactory.create_async(
            session=session)
        assert customer.last_change_code == 1
    @pytest.mark.asyncio
    async def test_last_change_code_default_on_update(self, session):
        """
        Test case for checking the default value of the
        last_change_code attribute after updating the customer.
        Args:
            session: The database session to use.
        Returns:
            None
        Raises:
            AssertionError: If the last_change_code attribute is not updated.
        """
        customer = await CustomerFactory.create_async(
            session=session)
        initial_code = customer.last_change_code
        customer.code = uuid.uuid4()
        await session.commit()
        assert customer.last_change_code != initial_code
    @pytest.mark.asyncio
    async def test_date_inserted_on_build(self, session):
        """
        Test case for checking the value of the insert_utc_date_time
        attribute when using the build_async method.
        Args:
            session: The database session to use.
        Returns:
            None
        Raises:
            AssertionError: If the insert_utc_date_time attribute
            is None or not an instance of datetime.
        """
        customer = await CustomerFactory.build_async(
            session=session)
        assert customer.insert_utc_date_time is not None
        assert isinstance(
            customer.insert_utc_date_time, datetime)
    @pytest.mark.asyncio
    async def test_date_inserted_on_initial_save(self, session):
        """
        Test case for checking the value of the
        insert_utc_date_time attribute after the initial save.
        Args:
            session: The database session to use.
        Returns:
            None
        Raises:
            AssertionError: If the insert_utc_date_time
            attribute is None or not an instance of datetime.
        """
        customer = await CustomerFactory.build_async(
            session=session)
        assert customer.insert_utc_date_time is not None
        assert isinstance(
            customer.insert_utc_date_time, datetime)
        initial_time = datetime.utcnow() + timedelta(days=-1)
        customer.code = uuid.uuid4()
        session.add(customer)
        await session.commit()
        assert customer.insert_utc_date_time > initial_time
    @pytest.mark.asyncio
    async def test_date_inserted_on_second_save(self, session):
        """
        Test case for checking the value of the
        insert_utc_date_time attribute after the second save.
        Args:
            session: The database session to use.
        Returns:
            None
        Raises:
            AssertionError: If the insert_utc_date_time
            attribute is not the same as the initial time.
        """
        customer = await CustomerFactory.create_async(
            session=session)
        assert customer.insert_utc_date_time is not None
        assert isinstance(
            customer.insert_utc_date_time, datetime)
        initial_time = customer.insert_utc_date_time
        customer.code = uuid.uuid4()
        time.sleep(1)
        await session.commit()
        assert customer.insert_utc_date_time == initial_time
    @pytest.mark.asyncio
    async def test_date_updated_on_build(self, session):
        """
        Test case for checking the value of the
        last_update_utc_date_time attribute when using
        the build_async method.
        Args:
            session: The database session to use.
        Returns:
            None
        Raises:
            AssertionError: If the last_update_utc_date_time
            attribute is None or not an instance of datetime.
        """
        customer = await CustomerFactory.build_async(
            session=session)
        assert customer.last_update_utc_date_time is not None
        assert isinstance(
            customer.last_update_utc_date_time, datetime)
    @pytest.mark.asyncio
    async def test_date_updated_on_initial_save(self, session):
        """
        Test case for checking the value of the
        last_update_utc_date_time attribute after the initial save.
        Args:
            session: The database session to use.
        Returns:
            None
        Raises:
            AssertionError: If the last_update_utc_date_time
            attribute is None or not an instance of datetime.
        """
        customer = await CustomerFactory.build_async(
            session=session)
        assert customer.last_update_utc_date_time is not None
        assert isinstance(
            customer.last_update_utc_date_time, datetime)
        initial_time = datetime.utcnow() + timedelta(days=-1)
        customer.code = uuid.uuid4()
        session.add(customer)
        await session.commit()
        assert customer.last_update_utc_date_time > initial_time
    @pytest.mark.asyncio
    async def test_date_updated_on_second_save(self, session):
        """
        Test case for checking the value of the
        last_update_utc_date_time attribute after the second save.
        Args:
            session: The database session to use.
        Returns:
            None
        Raises:
            AssertionError: If the last_update_utc_date_time
            attribute is not greater than the initial time.
        """
        customer = await CustomerFactory.create_async(
            session=session)
        assert customer.last_update_utc_date_time is not None
        assert isinstance(
            customer.last_update_utc_date_time, datetime)
        initial_time = customer.last_update_utc_date_time
        customer.code = uuid.uuid4()
        time.sleep(1)
        await session.commit()
        assert customer.last_update_utc_date_time > initial_time
    @pytest.mark.asyncio
    async def test_model_deletion(self, session):
        """
        Test case for deleting a customer
        from the database.
        Args:
            session: The database session to use.
        Returns:
            None
        Raises:
            AssertionError: If the deleted
            customer is still
            found in the database.
        """
        customer = await CustomerFactory.create_async(
            session=session)
        await session.delete(customer)
        await session.commit()
        # Construct the select statement
        stmt = select(Customer).where(
            Customer._customer_id == customer.customer_id)  # type: ignore # pylint: disable=protected-access  # noqa: ignore=E501
        # Execute the statement asynchronously
        result = await session.execute(stmt)
        # Fetch all results
        deleted_customer = result.scalars().first()
        assert deleted_customer is None
    @pytest.mark.asyncio
    async def test_data_types(self, session):
        """
        Test case for checking the data types of
        the customer attributes.
        Args:
            session: The database session to use.
        Returns:
            None
        Raises:
            AssertionError: If any of the attribute types are incorrect.
        """
        customer = await CustomerFactory.create_async(
            session=session)
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
        Test case to check the unique code constraint for customers.
        This test creates two customer
        instances using
        the CustomerFactoryand assigns
        the same code to both customers.
        Then it adds both customers to the session and
        attempts to commit the changes.
        The test expects an exception to be raised,
        indicating that the unique code constraint has been violated.
        Finally, the test rolls back the session to
        ensure no changes are persisted.
        Note: This test assumes that the
        CustomerFactory.create_async() method creates unique codes for each customer.
        """
        customer_1 = await CustomerFactory.create_async(
            session=session)
        customer_2 = await CustomerFactory.create_async(
            session=session)
        customer_2.code = customer_1.code
        session.add_all([customer_1, customer_2])
        with pytest.raises(Exception):
            await session.commit()
        await session.rollback()
    @pytest.mark.asyncio
    async def test_fields_default(self):
        """
        Test case to verify the default values of
        the fields in the Customer model.
        This test case checks that the default values
        of various fields in the Customer
        model are set correctly.
        It asserts that the default values are not None
        or empty, and that the data types of certain fields are correct.
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
        Test the concurrency of last_change_code
        in the Customer model.
        This test verifies that the last_change_code
        attribute of a Customer object
        is updated correctly when multiple instances
        of the object are modified
        concurrently.
        Steps:
        1. Create a new Customer object using
            the CustomerFactory.
        2. Get the original value of the last_change_code attribute.
        3. Query the database for the Customer
            object using the customer_id.
        4. Modify the code attribute of the
            retrieved Customer object.
        5. Commit the changes to the database.
        6. Query the database again for the
            Customer object using the customer_id.
        7. Get the modified Customer object.
        8. Verify that the last_change_code attribute
            of the modified Customer object
            is different from the original value.
        Raises:
            AssertionError: If the last_change_code attribute
                            of the modified Customer
                            object is the same as the original value.
        """
        customer = await CustomerFactory.create_async(
            session=session)
        original_last_change_code = customer.last_change_code
        stmt = select(Customer).where(
            Customer._customer_id == customer.customer_id)  # type: ignore # pylint: disable=protected-access  # noqa: ignore=E501
        result = await session.execute(stmt)
        customer_1 = result.scalars().first()
        # customer_1 = await session.query(Customer).filter_by(
        # customer_id=customer.customer_id).first()
        customer_1.code = uuid.uuid4()
        await session.commit()
        stmt = select(Customer).where(
            Customer._customer_id == customer.customer_id)  # type: ignore # pylint: disable=protected-access  # noqa: ignore=E501
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
        Test case for handling an invalid tac ID.
        This test case creates a customer using the
        CustomerFactory and sets an invalid tac ID.
        It then asserts that committing the session
        raises an IntegrityError and rolls back the session.
        Args:
            session: The SQLAlchemy session object.
        Raises:
            IntegrityError: If committing the session
            fails due to an integrity constraint violation.
        """
        customer = await CustomerFactory.create_async(
            session=session)
        customer.tac_id = 99999
        with pytest.raises(IntegrityError):
            await session.commit()
        await session.rollback()
    # uTCOffsetInMinutes,
    # zip,
# endset
