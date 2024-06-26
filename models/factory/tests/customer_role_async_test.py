# models/factory/tests/customer_role_async_test.py
# pylint: disable=unused-argument
# pylint: disable=unused-import

"""
This module contains unit tests for the asynchronous
operations of the CustomerRoleFactory class.
"""

import asyncio
import math  # noqa: F401
import time
import uuid  # noqa: F401
from datetime import date, datetime, timedelta  # noqa: F401
from decimal import Decimal  # noqa: F401
from typing import AsyncGenerator, Generator

import pytest
import pytest_asyncio
from sqlalchemy import event
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.future import select
from sqlalchemy.orm import sessionmaker

from models import Base, CustomerRole
from models.factory import CustomerRoleFactory

DATABASE_URL = "sqlite+aiosqlite:///:memory:"


class TestCustomerRoleFactoryAsync:
    """
    This class contains unit tests for the asynchronous
    operations of the CustomerRoleFactory class.
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
    async def test_customer_role_creation(self, session):
        """
        Test case for creating a customer_role
        asynchronously.

        Args:
            session: The database session to use.

        Returns:
            None

        Raises:
            AssertionError: If the customer_role ID
                is None after creation.
        """
        customer_role = await \
            CustomerRoleFactory.create_async(
                session=session)
        assert customer_role.customer_role_id is not None

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
        customer_role = await \
            CustomerRoleFactory.create_async(
                session=session)
        assert isinstance(customer_role.code, uuid.UUID)

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
        customer_role: CustomerRole = await \
            CustomerRoleFactory.build_async(
                session=session)
        assert customer_role.last_change_code == 0

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
        customer_role: CustomerRole = await \
            CustomerRoleFactory.create_async(
                session=session)
        assert customer_role.last_change_code == 1

    @pytest.mark.asyncio
    async def test_last_change_code_default_on_update(self, session):
        """
        Test case for checking the default value of the
        last_change_code attribute after updating the customer_role.

        Args:
            session: The database session to use.

        Returns:
            None

        Raises:
            AssertionError: If the last_change_code attribute is not updated.
        """
        customer_role = await \
            CustomerRoleFactory.create_async(
                session=session)
        initial_code = customer_role.last_change_code
        customer_role.code = uuid.uuid4()
        await session.commit()
        assert customer_role.last_change_code != initial_code

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
        customer_role = await \
            CustomerRoleFactory.build_async(
                session=session)
        assert customer_role.insert_utc_date_time is not None
        assert isinstance(
            customer_role.insert_utc_date_time, datetime)

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
        customer_role = await \
            CustomerRoleFactory.build_async(
                session=session)
        assert customer_role.insert_utc_date_time is not None
        assert isinstance(
            customer_role.insert_utc_date_time, datetime)
        initial_time = datetime.utcnow() + timedelta(days=-1)
        customer_role.code = uuid.uuid4()
        session.add(customer_role)
        await session.commit()
        assert customer_role.insert_utc_date_time > \
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
        customer_role = await \
            CustomerRoleFactory.create_async(
                session=session)
        assert customer_role.insert_utc_date_time is not None
        assert isinstance(
            customer_role.insert_utc_date_time, datetime)
        initial_time = customer_role.insert_utc_date_time
        customer_role.code = uuid.uuid4()
        time.sleep(1)
        await session.commit()
        assert customer_role.insert_utc_date_time == \
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
        customer_role = await \
            CustomerRoleFactory.build_async(
                session=session)
        assert customer_role.last_update_utc_date_time is not None
        assert isinstance(
            customer_role.last_update_utc_date_time, datetime)

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
        customer_role = await \
            CustomerRoleFactory.build_async(
                session=session)
        assert customer_role.last_update_utc_date_time is not None
        assert isinstance(
            customer_role.last_update_utc_date_time, datetime)
        initial_time = datetime.utcnow() + timedelta(days=-1)
        customer_role.code = uuid.uuid4()
        session.add(customer_role)
        await session.commit()
        assert customer_role.last_update_utc_date_time > \
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
        customer_role = await \
            CustomerRoleFactory.create_async(
                session=session)
        assert customer_role.last_update_utc_date_time is not None
        assert isinstance(
            customer_role.last_update_utc_date_time, datetime)
        initial_time = customer_role.last_update_utc_date_time
        customer_role.code = uuid.uuid4()
        time.sleep(1)
        await session.commit()
        assert customer_role.last_update_utc_date_time > \
            initial_time

    @pytest.mark.asyncio
    async def test_model_deletion(self, session):
        """
        Test case for deleting a customer_role
        from the database.

        Args:
            session: The database session to use.

        Returns:
            None

        Raises:
            AssertionError: If the deleted
            customer_role is still
            found in the database.
        """
        customer_role = await \
            CustomerRoleFactory.create_async(
                session=session)
        await session.delete(customer_role)
        await session.commit()

        # Construct the select statement
        stmt = select(CustomerRole).where(
            CustomerRole._customer_role_id == (  # type: ignore # pylint: disable=protected-access  # noqa: ignore=E501
                customer_role.customer_role_id))

        # Execute the statement asynchronously
        result = await session.execute(stmt)

        # Fetch all results
        deleted_customer_role = result.scalars().first()

        assert deleted_customer_role is None

    @pytest.mark.asyncio
    async def test_data_types(self, session):
        """
        Test case for checking the data types of
        the customer_role attributes.

        Args:
            session: The database session to use.

        Returns:
            None

        Raises:
            AssertionError: If any of the attribute types are incorrect.
        """
        obj = await \
            CustomerRoleFactory.create_async(
                session=session)
        assert isinstance(obj.customer_role_id, int)
        assert isinstance(obj.code, uuid.UUID)
        assert isinstance(obj.last_change_code, int)
        assert isinstance(obj.insert_user_id, uuid.UUID)
        assert isinstance(obj.last_update_user_id, uuid.UUID)
        assert isinstance(obj.customer_id, int)
        assert isinstance(obj.is_placeholder, bool)
        assert isinstance(obj.placeholder, bool)
        assert isinstance(obj.role_id, int)
        # Check for the peek values
        # customerID

        assert isinstance(obj.customer_code_peek, uuid.UUID)
        # isPlaceholder,
        # placeholder,
        # roleID

        assert isinstance(obj.role_code_peek, uuid.UUID)

        assert isinstance(obj.insert_utc_date_time, datetime)
        assert isinstance(obj.last_update_utc_date_time, datetime)

    @pytest.mark.asyncio
    async def test_unique_code_constraint(self, session):
        """
        Test case to check the unique code constraint
        for customer_roles.

        This test creates two customer_role
        instances using
        the CustomerRoleFactoryand assigns
        the same code to both customer_roles.
        Then it adds both customer_roles to the session and
        attempts to commit the changes.
        The test expects an exception to be raised,
        indicating that the unique code constraint has been violated.
        Finally, the test rolls back the session to
        ensure no changes are persisted.

        Note: This test assumes that the
        CustomerRoleFactory.create_async()
        method creates unique codes for
        each customer_role.
        """

        obj_1 = await CustomerRoleFactory.create_async(
            session=session)
        obj_2 = await CustomerRoleFactory.create_async(
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
        the fields in the CustomerRole model.

        This test case checks that the default values
        of various fields in the CustomerRole
        model are set correctly.
        It asserts that the default values are not None
        or empty, and that the data types of certain fields are correct.
        """

        new_obj = CustomerRole()
        assert new_obj.code is not None
        assert new_obj.last_change_code is not None
        assert new_obj.insert_user_id is not None
        assert new_obj.last_update_user_id is not None
        assert new_obj.insert_utc_date_time is not None
        assert new_obj.last_update_utc_date_time is not None

        # CustomerID

        assert isinstance(new_obj.customer_code_peek, uuid.UUID)
        # isPlaceholder,
        # placeholder,
        # RoleID

        assert isinstance(new_obj.role_code_peek, uuid.UUID)
        assert new_obj.customer_id == 0
        assert new_obj.is_placeholder is False
        assert new_obj.placeholder is False
        assert new_obj.role_id == 0

    @pytest.mark.asyncio
    async def test_last_change_code_concurrency(self, session):
        """
        Test the concurrency of last_change_code
        in the CustomerRole model.

        This test verifies that the last_change_code
        attribute of a CustomerRole object
        is updated correctly when multiple instances
        of the object are modified
        concurrently.

        Steps:
        1. Create a new
            CustomerRole object using
            the CustomerRoleFactory.
        2. Get the original value of the
            last_change_code attribute.
        3. Query the database for the CustomerRole
            object using the
            customer_role_id.
        4. Modify the code attribute of the
            retrieved CustomerRole object.
        5. Commit the changes to the database.
        6. Query the database again for the
            CustomerRole object using the
            customer_role_id.
        7. Get the modified CustomerRole object.
        8. Verify that the last_change_code attribute
            of the modified CustomerRole object
            is different from the original value.

        Raises:
            AssertionError: If the last_change_code attribute
                            of the modified CustomerRole
                            object is the same as the original value.
        """
        customer_role = await \
            CustomerRoleFactory.create_async(
                session=session)
        original_last_change_code = customer_role.last_change_code

        stmt = select(CustomerRole).where(
            CustomerRole._customer_role_id == (  # type: ignore # pylint: disable=protected-access  # noqa: ignore=E501
                customer_role.customer_role_id))
        result = await session.execute(stmt)
        obj_1 = result.scalars().first()

        # obj_1 = await session.query(CustomerRole).filter_by(
        # customer_role_id=customer_role.customer_role_id).first()
        obj_1.code = uuid.uuid4()
        await session.commit()

        stmt = select(CustomerRole).where(
            CustomerRole._customer_role_id == (  # type: ignore # pylint: disable=protected-access  # noqa: ignore=E501
                customer_role.customer_role_id))
        result = await session.execute(stmt)
        obj_2 = result.scalars().first()

        # obj_2 = await session.query(CustomerRole).filter_by(
        # customer_role_id=customer_role.customer_role_id).first()
        obj_2.code = uuid.uuid4()
        await session.commit()
        assert obj_2.last_change_code != original_last_change_code
    # CustomerID

    @pytest.mark.asyncio
    async def test_invalid_customer_id(self, session):
        """
        Test case for handling an invalid customer ID.

        This test case creates a customer_role using the
        CustomerRoleFactory and sets an invalid customer ID.
        It then asserts that committing the session
        raises an IntegrityError and rolls back the session.

        Args:
            session: The SQLAlchemy session object.

        Raises:
            IntegrityError: If committing the session
            fails due to an integrity constraint violation.
        """
        customer_role = await \
            CustomerRoleFactory.create_async(
                session=session)
        customer_role.customer_id = 99999
        with pytest.raises(IntegrityError):
            await session.commit()
        await session.rollback()
    # isPlaceholder,
    # placeholder,
    # RoleID

    @pytest.mark.asyncio
    async def test_invalid_role_id(self, session):
        """
        Test case for handling an invalid role ID.

        This test case creates a customer_role using the
        CustomerRoleFactory and sets an invalid role ID.
        It then asserts that committing the session
        raises an IntegrityError and rolls back the session.

        Args:
            session: The SQLAlchemy session object.

        Raises:
            IntegrityError: If committing the session
            fails due to an integrity constraint violation.
        """
        customer_role = await \
            CustomerRoleFactory.create_async(
                session=session)
        customer_role.role_id = 99999
        with pytest.raises(IntegrityError):
            await session.commit()
        await session.rollback()
