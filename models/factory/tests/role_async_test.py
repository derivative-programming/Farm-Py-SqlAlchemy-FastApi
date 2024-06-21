# models/factory/tests/role_async_test.py
# pylint: disable=unused-argument
"""
This module contains unit tests for the asynchronous
operations of the RoleFactory class.
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
from models import Base, Role
from models.factory import RoleFactory
DATABASE_URL = "sqlite+aiosqlite:///:memory:"
class TestRoleFactoryAsync:
    """
    This class contains unit tests for the asynchronous
    operations of the RoleFactory class.
    """
    @pytest.fixture(scope="function")
    def event_loop(self) -> asyncio.AbstractEventLoop:
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
    async def test_role_creation(self, session):
        """
        Test case for creating a role
        asynchronously.
        Args:
            session: The database session to use.
        Returns:
            None
        Raises:
            AssertionError: If the role ID
                is None after creation.
        """
        role = await RoleFactory.create_async(
            session=session)
        assert role.role_id is not None
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
        role = await RoleFactory.create_async(
            session=session)
        assert isinstance(role.code, uuid.UUID)
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
        role: Role = await RoleFactory.build_async(
            session=session)
        assert role.last_change_code == 0
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
        role: Role = await RoleFactory.create_async(
            session=session)
        assert role.last_change_code == 1
    @pytest.mark.asyncio
    async def test_last_change_code_default_on_update(self, session):
        """
        Test case for checking the default value of the
        last_change_code attribute after updating the role.
        Args:
            session: The database session to use.
        Returns:
            None
        Raises:
            AssertionError: If the last_change_code attribute is not updated.
        """
        role = await RoleFactory.create_async(
            session=session)
        initial_code = role.last_change_code
        role.code = uuid.uuid4()
        await session.commit()
        assert role.last_change_code != initial_code
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
        role = await RoleFactory.build_async(
            session=session)
        assert role.insert_utc_date_time is not None
        assert isinstance(
            role.insert_utc_date_time, datetime)
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
        role = await RoleFactory.build_async(
            session=session)
        assert role.insert_utc_date_time is not None
        assert isinstance(
            role.insert_utc_date_time, datetime)
        initial_time = datetime.utcnow() + timedelta(days=-1)
        role.code = uuid.uuid4()
        session.add(role)
        await session.commit()
        assert role.insert_utc_date_time > initial_time
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
        role = await RoleFactory.create_async(
            session=session)
        assert role.insert_utc_date_time is not None
        assert isinstance(
            role.insert_utc_date_time, datetime)
        initial_time = role.insert_utc_date_time
        role.code = uuid.uuid4()
        time.sleep(1)
        await session.commit()
        assert role.insert_utc_date_time == initial_time
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
        role = await RoleFactory.build_async(
            session=session)
        assert role.last_update_utc_date_time is not None
        assert isinstance(
            role.last_update_utc_date_time, datetime)
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
        role = await RoleFactory.build_async(
            session=session)
        assert role.last_update_utc_date_time is not None
        assert isinstance(
            role.last_update_utc_date_time, datetime)
        initial_time = datetime.utcnow() + timedelta(days=-1)
        role.code = uuid.uuid4()
        session.add(role)
        await session.commit()
        assert role.last_update_utc_date_time > initial_time
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
        role = await RoleFactory.create_async(
            session=session)
        assert role.last_update_utc_date_time is not None
        assert isinstance(
            role.last_update_utc_date_time, datetime)
        initial_time = role.last_update_utc_date_time
        role.code = uuid.uuid4()
        time.sleep(1)
        await session.commit()
        assert role.last_update_utc_date_time > initial_time
    @pytest.mark.asyncio
    async def test_model_deletion(self, session):
        """
        Test case for deleting a role
        from the database.
        Args:
            session: The database session to use.
        Returns:
            None
        Raises:
            AssertionError: If the deleted
            role is still
            found in the database.
        """
        role = await RoleFactory.create_async(
            session=session)
        await session.delete(role)
        await session.commit()
        # Construct the select statement
        stmt = select(Role).where(
            Role._role_id == role.role_id)  # type: ignore # pylint: disable=protected-access  # noqa: ignore=E501
        # Execute the statement asynchronously
        result = await session.execute(stmt)
        # Fetch all results
        deleted_role = result.scalars().first()
        assert deleted_role is None
    @pytest.mark.asyncio
    async def test_data_types(self, session):
        """
        Test case for checking the data types of
        the role attributes.
        Args:
            session: The database session to use.
        Returns:
            None
        Raises:
            AssertionError: If any of the attribute types are incorrect.
        """
        role = await RoleFactory.create_async(
            session=session)
        assert isinstance(role.role_id, int)
        assert isinstance(role.code, uuid.UUID)
        assert isinstance(role.last_change_code, int)
        assert isinstance(role.insert_user_id, uuid.UUID)
        assert isinstance(role.last_update_user_id, uuid.UUID)
        assert role.description == "" or isinstance(role.description, str)
        assert isinstance(role.display_order, int)
        assert isinstance(role.is_active, bool)
        assert role.lookup_enum_name == "" or isinstance(role.lookup_enum_name, str)
        assert role.name == "" or isinstance(role.name, str)
        assert isinstance(role.pac_id, int)
        # Check for the peek values
# endset
        # description,
        # displayOrder,
        # isActive,
        # lookupEnumName,
        # name,
        # pacID
        assert isinstance(role.pac_code_peek, uuid.UUID)
# endset
        assert isinstance(role.insert_utc_date_time, datetime)
        assert isinstance(role.last_update_utc_date_time, datetime)
    @pytest.mark.asyncio
    async def test_unique_code_constraint(self, session):
        """
        Test case to check the unique code constraint for roles.
        This test creates two role
        instances using
        the RoleFactoryand assigns
        the same code to both roles.
        Then it adds both roles to the session and
        attempts to commit the changes.
        The test expects an exception to be raised,
        indicating that the unique code constraint has been violated.
        Finally, the test rolls back the session to
        ensure no changes are persisted.
        Note: This test assumes that the
        RoleFactory.create_async() method creates unique codes for each role.
        """
        role_1 = await RoleFactory.create_async(
            session=session)
        role_2 = await RoleFactory.create_async(
            session=session)
        role_2.code = role_1.code
        session.add_all([role_1, role_2])
        with pytest.raises(Exception):
            await session.commit()
        await session.rollback()
    @pytest.mark.asyncio
    async def test_fields_default(self):
        """
        Test case to verify the default values of
        the fields in the Role model.
        This test case checks that the default values
        of various fields in the Role
        model are set correctly.
        It asserts that the default values are not None
        or empty, and that the data types of certain fields are correct.
        """
        role = Role()
        assert role.code is not None
        assert role.last_change_code is not None
        assert role.insert_user_id is not None
        assert role.last_update_user_id is not None
        assert role.insert_utc_date_time is not None
        assert role.last_update_utc_date_time is not None
# endset
        # description,
        # displayOrder,
        # isActive,
        # lookupEnumName,
        # name,
        # PacID
        assert isinstance(role.pac_code_peek, uuid.UUID)
# endset
        assert role.description == ""
        assert role.display_order == 0
        assert role.is_active is False
        assert role.lookup_enum_name == ""
        assert role.name == ""
        assert role.pac_id == 0
# endset
    @pytest.mark.asyncio
    async def test_last_change_code_concurrency(self, session):
        """
        Test the concurrency of last_change_code
        in the Role model.
        This test verifies that the last_change_code
        attribute of a Role object
        is updated correctly when multiple instances
        of the object are modified
        concurrently.
        Steps:
        1. Create a new Role object using
            the RoleFactory.
        2. Get the original value of the last_change_code attribute.
        3. Query the database for the Role
            object using the role_id.
        4. Modify the code attribute of the
            retrieved Role object.
        5. Commit the changes to the database.
        6. Query the database again for the
            Role object using the role_id.
        7. Get the modified Role object.
        8. Verify that the last_change_code attribute
            of the modified Role object
            is different from the original value.
        Raises:
            AssertionError: If the last_change_code attribute
                            of the modified Role
                            object is the same as the original value.
        """
        role = await RoleFactory.create_async(
            session=session)
        original_last_change_code = role.last_change_code
        stmt = select(Role).where(
            Role._role_id == role.role_id)  # type: ignore # pylint: disable=protected-access  # noqa: ignore=E501
        result = await session.execute(stmt)
        role_1 = result.scalars().first()
        # role_1 = await session.query(Role).filter_by(
        # role_id=role.role_id).first()
        role_1.code = uuid.uuid4()
        await session.commit()
        stmt = select(Role).where(
            Role._role_id == role.role_id)  # type: ignore # pylint: disable=protected-access  # noqa: ignore=E501
        result = await session.execute(stmt)
        role_2 = result.scalars().first()
        # role_2 = await session.query(Role).filter_by(
        # role_id=role.role_id).first()
        role_2.code = uuid.uuid4()
        await session.commit()
        assert role_2.last_change_code != original_last_change_code
# endset
    # description,
    # displayOrder,
    # isActive,
    # lookupEnumName,
    # name,
    # PacID
    @pytest.mark.asyncio
    async def test_invalid_pac_id(self, session):
        """
        Test case for handling an invalid pac ID.
        This test case creates a role using the
        RoleFactory and sets an invalid pac ID.
        It then asserts that committing the session
        raises an IntegrityError and rolls back the session.
        Args:
            session: The SQLAlchemy session object.
        Raises:
            IntegrityError: If committing the session
            fails due to an integrity constraint violation.
        """
        role = await RoleFactory.create_async(
            session=session)
        role.pac_id = 99999
        with pytest.raises(IntegrityError):
            await session.commit()
        await session.rollback()
# endset
