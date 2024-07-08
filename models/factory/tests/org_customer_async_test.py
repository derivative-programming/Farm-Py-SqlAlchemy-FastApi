# models/factory/tests/org_customer_async_test.py  # pylint: disable=duplicate-code
# pylint: disable=unused-argument, too-many-public-methods
# pylint: disable=unused-import

"""
This module contains unit tests for the asynchronous
operations of the OrgCustomerFactory class.
"""

import asyncio
import math  # noqa: F401
import time
import uuid  # noqa: F401
from datetime import date, datetime, timedelta, timezone  # noqa: F401
from decimal import Decimal  # noqa: F401
from typing import AsyncGenerator, Generator

import pytest_asyncio
from sqlalchemy import event
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.future import select
from sqlalchemy.orm import sessionmaker

import pytest
from models import Base, OrgCustomer
from models.factory import OrgCustomerFactory

TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"


class TestOrgCustomerFactoryAsync:
    """
    This class contains unit tests for the asynchronous
    operations of the OrgCustomerFactory class.
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
        engine = create_async_engine(TEST_DATABASE_URL, echo=False)
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
            testing_session_local = sessionmaker(  # pylint: disable=invalid-name
                expire_on_commit=False,
                class_=AsyncSession,
                bind=engine,
            )
            async with testing_session_local(bind=connection) as session:  # type: ignore # noqa: E501
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
    async def test_org_customer_creation(self, session):
        """
        Test case for creating a org_customer
        asynchronously.

        Args:
            session: The database session to use.

        Returns:
            None

        Raises:
            AssertionError: If the org_customer ID
                is None after creation.
        """
        org_customer = await \
            OrgCustomerFactory.create_async(
                session=session)
        assert org_customer.org_customer_id is not None

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
        org_customer = await \
            OrgCustomerFactory.create_async(
                session=session)
        assert isinstance(org_customer.code, uuid.UUID)

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
        org_customer: OrgCustomer = await \
            OrgCustomerFactory.build_async(
                session=session)
        assert org_customer.last_change_code == 0

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
        org_customer: OrgCustomer = await \
            OrgCustomerFactory.create_async(
                session=session)
        assert org_customer.last_change_code == 1

    @pytest.mark.asyncio
    async def test_last_change_code_default_on_update(self, session):
        """
        Test case for checking the default value of the
        last_change_code attribute after updating the org_customer.

        Args:
            session: The database session to use.

        Returns:
            None

        Raises:
            AssertionError: If the last_change_code attribute is not updated.
        """
        org_customer = await \
            OrgCustomerFactory.create_async(
                session=session)
        initial_code = org_customer.last_change_code
        org_customer.code = uuid.uuid4()
        await session.commit()
        assert org_customer.last_change_code != initial_code

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
        org_customer = await \
            OrgCustomerFactory.build_async(
                session=session)
        assert org_customer.insert_utc_date_time is not None
        assert isinstance(
            org_customer.insert_utc_date_time, datetime)

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
        org_customer = await \
            OrgCustomerFactory.build_async(
                session=session)
        assert org_customer.insert_utc_date_time is not None
        assert isinstance(
            org_customer.insert_utc_date_time, datetime)
        initial_time = datetime.now(timezone.utc) + timedelta(days=-1)
        org_customer.code = uuid.uuid4()
        session.add(org_customer)
        await session.commit()
        assert org_customer.insert_utc_date_time > \
            initial_time

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
        org_customer = await \
            OrgCustomerFactory.create_async(
                session=session)
        assert org_customer.insert_utc_date_time is not None
        assert isinstance(
            org_customer.insert_utc_date_time, datetime)
        initial_time = org_customer.insert_utc_date_time
        org_customer.code = uuid.uuid4()
        time.sleep(1)
        await session.commit()
        assert org_customer.insert_utc_date_time == \
            initial_time

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
        org_customer = await \
            OrgCustomerFactory.build_async(
                session=session)
        assert org_customer.last_update_utc_date_time is not None
        assert isinstance(
            org_customer.last_update_utc_date_time, datetime)

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
        org_customer = await \
            OrgCustomerFactory.build_async(
                session=session)
        assert org_customer.last_update_utc_date_time is not None
        assert isinstance(
            org_customer.last_update_utc_date_time, datetime)
        initial_time = datetime.now(timezone.utc) + timedelta(days=-1)
        org_customer.code = uuid.uuid4()
        session.add(org_customer)
        await session.commit()
        assert org_customer.last_update_utc_date_time > \
            initial_time

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
        org_customer = await \
            OrgCustomerFactory.create_async(
                session=session)
        assert org_customer.last_update_utc_date_time is not None
        assert isinstance(
            org_customer.last_update_utc_date_time, datetime)
        initial_time = org_customer.last_update_utc_date_time
        org_customer.code = uuid.uuid4()
        time.sleep(1)
        await session.commit()
        assert org_customer.last_update_utc_date_time > \
            initial_time

    @pytest.mark.asyncio
    async def test_model_deletion(self, session):
        """
        Test case for deleting a org_customer
        from the database.

        Args:
            session: The database session to use.

        Returns:
            None

        Raises:
            AssertionError: If the deleted
            org_customer is still
            found in the database.
        """
        org_customer = await \
            OrgCustomerFactory.create_async(
                session=session)
        await session.delete(org_customer)
        await session.commit()

        # Construct the select statement
        stmt = select(OrgCustomer).where(
            OrgCustomer._org_customer_id == (  # type: ignore # pylint: disable=protected-access  # noqa: ignore=E501
                org_customer.org_customer_id))

        # Execute the statement asynchronously
        result = await session.execute(stmt)

        # Fetch all results
        deleted_org_customer = result.scalars().first()

        assert deleted_org_customer is None

    @pytest.mark.asyncio
    async def test_data_types(self, session):
        """
        Test case for checking the data types of
        the org_customer attributes.

        Args:
            session: The database session to use.

        Returns:
            None

        Raises:
            AssertionError: If any of the attribute types are incorrect.
        """
        obj = await \
            OrgCustomerFactory.create_async(
                session=session)
        assert isinstance(obj.org_customer_id, int)
        assert isinstance(obj.code, uuid.UUID)
        assert isinstance(obj.last_change_code, int)
        assert isinstance(obj.insert_user_id, uuid.UUID)
        assert isinstance(obj.last_update_user_id, uuid.UUID)
        assert isinstance(obj.customer_id, int)
        assert obj.email == "" or isinstance(
            obj.email, str)
        assert isinstance(obj.organization_id, int)
        # Check for the peek values
        # customerID

        assert isinstance(obj.customer_code_peek, uuid.UUID)
        # email
        # organizationID

        assert isinstance(obj.organization_code_peek, uuid.UUID)

        assert isinstance(obj.insert_utc_date_time, datetime)
        assert isinstance(obj.last_update_utc_date_time, datetime)

    @pytest.mark.asyncio
    async def test_unique_code_constraint(self, session):
        """
        Test case to check the unique code constraint
        for org_customers.

        This test creates two org_customer
        instances using
        the OrgCustomerFactoryand assigns
        the same code to both org_customers.
        Then it adds both org_customers to the session and
        attempts to commit the changes.
        The test expects an exception to be raised,
        indicating that the unique code constraint has been violated.
        Finally, the test rolls back the session to
        ensure no changes are persisted.

        Note: This test assumes that the
        OrgCustomerFactory.create_async()
        method creates unique codes for
        each org_customer.
        """

        obj_1 = await OrgCustomerFactory.create_async(
            session=session)
        obj_2 = await OrgCustomerFactory.create_async(
            session=session)
        obj_2.code = obj_1.code
        session.add_all([obj_1,
                         obj_2])
        with pytest.raises(Exception):
            await session.commit()
        await session.rollback()

    @pytest.mark.asyncio
    async def test_fields_default(self):
        """
        Test case to verify the default values of
        the fields in the OrgCustomer model.

        This test case checks that the default values
        of various fields in the OrgCustomer
        model are set correctly.
        It asserts that the default values are not None
        or empty, and that the data types of certain fields are correct.
        """

        new_obj = OrgCustomer()
        assert new_obj.code is not None
        assert new_obj.last_change_code is not None
        assert new_obj.insert_user_id is not None
        assert new_obj.last_update_user_id is not None
        assert new_obj.insert_utc_date_time is not None
        assert new_obj.last_update_utc_date_time is not None

        # CustomerID

        assert isinstance(new_obj.customer_code_peek, uuid.UUID)
        # email
        # OrganizationID

        assert isinstance(new_obj.organization_code_peek, uuid.UUID)
        assert new_obj.customer_id == 0
        assert new_obj.email == ""
        assert new_obj.organization_id == 0

    @pytest.mark.asyncio
    async def test_last_change_code_concurrency(self, session):
        """
        Test the concurrency of last_change_code
        in the OrgCustomer model.

        This test verifies that the last_change_code
        attribute of a OrgCustomer object
        is updated correctly when multiple instances
        of the object are modified
        concurrently.

        Steps:
        1. Create a new
            OrgCustomer object using
            the OrgCustomerFactory.
        2. Get the original value of the
            last_change_code attribute.
        3. Query the database for the OrgCustomer
            object using the
            org_customer_id.
        4. Modify the code attribute of the
            retrieved OrgCustomer object.
        5. Commit the changes to the database.
        6. Query the database again for the
            OrgCustomer object using the
            org_customer_id.
        7. Get the modified OrgCustomer object.
        8. Verify that the last_change_code attribute
            of the modified OrgCustomer object
            is different from the original value.

        Raises:
            AssertionError: If the last_change_code attribute
                            of the modified OrgCustomer
                            object is the same as the original value.
        """
        org_customer = await \
            OrgCustomerFactory.create_async(
                session=session)
        original_last_change_code = org_customer.last_change_code

        stmt = select(OrgCustomer).where(
            OrgCustomer._org_customer_id == (  # type: ignore # pylint: disable=protected-access  # noqa: ignore=E501
                org_customer.org_customer_id))
        result = await session.execute(stmt)
        obj_1 = result.scalars().first()

        obj_1.code = uuid.uuid4()
        await session.commit()

        stmt = select(OrgCustomer).where(
            OrgCustomer._org_customer_id == (  # type: ignore # pylint: disable=protected-access  # noqa: ignore=E501
                org_customer.org_customer_id))
        result = await session.execute(stmt)
        obj_2 = result.scalars().first()

        obj_2.code = uuid.uuid4()
        await session.commit()
        assert obj_2.last_change_code != original_last_change_code
    # CustomerID

    @pytest.mark.asyncio
    async def test_invalid_customer_id(self, session):
        """
        Test case for handling an invalid customer ID.

        This test case creates a org_customer using the
        OrgCustomerFactory and sets an invalid customer ID.
        It then asserts that committing the session
        raises an IntegrityError and rolls back the session.

        Args:
            session: The SQLAlchemy session object.

        Raises:
            IntegrityError: If committing the session
            fails due to an integrity constraint violation.
        """
        org_customer = await \
            OrgCustomerFactory.create_async(
                session=session)
        org_customer.customer_id = 99999
        with pytest.raises(IntegrityError):
            await session.commit()
        await session.rollback()
    # email
    # OrganizationID

    @pytest.mark.asyncio
    async def test_invalid_organization_id(self, session):
        """
        Test case for handling an invalid organization ID.

        This test case creates a org_customer using the
        OrgCustomerFactory and sets an invalid organization ID.
        It then asserts that committing the session
        raises an IntegrityError and rolls back the session.

        Args:
            session: The SQLAlchemy session object.

        Raises:
            IntegrityError: If committing the session
            fails due to an integrity constraint violation.
        """
        org_customer = await \
            OrgCustomerFactory.create_async(
                session=session)
        org_customer.organization_id = 99999
        with pytest.raises(IntegrityError):
            await session.commit()
        await session.rollback()
