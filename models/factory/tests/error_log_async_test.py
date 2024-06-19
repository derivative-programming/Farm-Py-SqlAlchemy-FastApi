# models/factory/tests/error_log_async_test.py
# pylint: disable=unused-argument
"""
This module contains unit tests for the asynchronous
operations of the ErrorLogFactory class.
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
from models import Base, ErrorLog
from models.factory import ErrorLogFactory
DATABASE_URL = "sqlite+aiosqlite:///:memory:"
class TestErrorLogFactoryAsync:
    """
    This class contains unit tests for the asynchronous
    operations of the ErrorLogFactory class.
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
    async def test_error_log_creation(self, session):
        """
        Test case for creating a error_log asynchronously.
        Args:
            session: The database session to use.
        Returns:
            None
        Raises:
            AssertionError: If the error_log ID is None after creation.
        """
        error_log = await ErrorLogFactory.create_async(session=session)
        assert error_log.error_log_id is not None
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
        error_log = await ErrorLogFactory.create_async(session=session)
        assert isinstance(error_log.code, uuid.UUID)
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
        error_log: ErrorLog = await ErrorLogFactory.build_async(session=session)
        assert error_log.last_change_code == 0
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
        error_log: ErrorLog = await ErrorLogFactory.create_async(session=session)
        assert error_log.last_change_code == 1
    @pytest.mark.asyncio
    async def test_last_change_code_default_on_update(self, session):
        """
        Test case for checking the default value of the
        last_change_code attribute after updating the error_log.
        Args:
            session: The database session to use.
        Returns:
            None
        Raises:
            AssertionError: If the last_change_code attribute is not updated.
        """
        error_log = await ErrorLogFactory.create_async(session=session)
        initial_code = error_log.last_change_code
        error_log.code = uuid.uuid4()
        await session.commit()
        assert error_log.last_change_code != initial_code
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
        error_log = await ErrorLogFactory.build_async(session=session)
        assert error_log.insert_utc_date_time is not None
        assert isinstance(error_log.insert_utc_date_time, datetime)
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
        error_log = await ErrorLogFactory.build_async(session=session)
        assert error_log.insert_utc_date_time is not None
        assert isinstance(error_log.insert_utc_date_time, datetime)
        initial_time = datetime.utcnow() + timedelta(days=-1)
        error_log.code = uuid.uuid4()
        session.add(error_log)
        await session.commit()
        assert error_log.insert_utc_date_time > initial_time
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
        error_log = await ErrorLogFactory.create_async(session=session)
        assert error_log.insert_utc_date_time is not None
        assert isinstance(error_log.insert_utc_date_time, datetime)
        initial_time = error_log.insert_utc_date_time
        error_log.code = uuid.uuid4()
        time.sleep(1)
        await session.commit()
        assert error_log.insert_utc_date_time == initial_time
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
        error_log = await ErrorLogFactory.build_async(session=session)
        assert error_log.last_update_utc_date_time is not None
        assert isinstance(error_log.last_update_utc_date_time, datetime)
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
        error_log = await ErrorLogFactory.build_async(session=session)
        assert error_log.last_update_utc_date_time is not None
        assert isinstance(error_log.last_update_utc_date_time, datetime)
        initial_time = datetime.utcnow() + timedelta(days=-1)
        error_log.code = uuid.uuid4()
        session.add(error_log)
        await session.commit()
        assert error_log.last_update_utc_date_time > initial_time
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
        error_log = await ErrorLogFactory.create_async(session=session)
        assert error_log.last_update_utc_date_time is not None
        assert isinstance(error_log.last_update_utc_date_time, datetime)
        initial_time = error_log.last_update_utc_date_time
        error_log.code = uuid.uuid4()
        time.sleep(1)
        await session.commit()
        assert error_log.last_update_utc_date_time > initial_time
    @pytest.mark.asyncio
    async def test_model_deletion(self, session):
        """
        Test case for deleting a error_log from the database.
        Args:
            session: The database session to use.
        Returns:
            None
        Raises:
            AssertionError: If the deleted error_log is still
            found in the database.
        """
        error_log = await ErrorLogFactory.create_async(session=session)
        await session.delete(error_log)
        await session.commit()
        # Construct the select statement
        stmt = select(ErrorLog).where(
            ErrorLog._error_log_id == error_log.error_log_id)  # type: ignore # pylint: disable=protected-access  # noqa: ignore=E501
        # Execute the statement asynchronously
        result = await session.execute(stmt)
        # Fetch all results
        deleted_error_log = result.scalars().first()
        assert deleted_error_log is None
    @pytest.mark.asyncio
    async def test_data_types(self, session):
        """
        Test case for checking the data types of the error_log attributes.
        Args:
            session: The database session to use.
        Returns:
            None
        Raises:
            AssertionError: If any of the attribute types are incorrect.
        """
        error_log = await ErrorLogFactory.create_async(session=session)
        assert isinstance(error_log.error_log_id, int)
        assert isinstance(error_log.code, uuid.UUID)
        assert isinstance(error_log.last_change_code, int)
        assert isinstance(error_log.insert_user_id, uuid.UUID)
        assert isinstance(error_log.last_update_user_id, uuid.UUID)
        assert isinstance(error_log.browser_code, uuid.UUID)
        assert isinstance(error_log.context_code, uuid.UUID)
        assert isinstance(error_log.created_utc_date_time, datetime)
        assert error_log.description == "" or isinstance(error_log.description, str)
        assert isinstance(error_log.is_client_side_error, bool)
        assert isinstance(error_log.is_resolved, bool)
        assert isinstance(error_log.pac_id, int)
        assert error_log.url == "" or isinstance(error_log.url, str)
        # Check for the peek values
# endset
        # browserCode,
        # contextCode,
        # createdUTCDateTime
        # description,
        # isClientSideError,
        # isResolved,
        # pacID
        assert isinstance(error_log.pac_code_peek, uuid.UUID)
        # url,
# endset
        assert isinstance(error_log.insert_utc_date_time, datetime)
        assert isinstance(error_log.last_update_utc_date_time, datetime)
    @pytest.mark.asyncio
    async def test_unique_code_constraint(self, session):
        """
        Test case to check the unique code constraint for error_logs.
        This test creates two error_log instances using
        the ErrorLogFactoryand assigns the same code to both error_logs.
        Then it adds both error_logs to the session and
        attempts to commit the changes.
        The test expects an exception to be raised,
        indicating that the unique code constraint has been violated.
        Finally, the test rolls back the session to
        ensure no changes are persisted.
        Note: This test assumes that the
        ErrorLogFactory.create_async() method creates unique codes for each error_log.
        """
        error_log_1 = await ErrorLogFactory.create_async(session=session)
        error_log_2 = await ErrorLogFactory.create_async(session=session)
        error_log_2.code = error_log_1.code
        session.add_all([error_log_1, error_log_2])
        with pytest.raises(Exception):
            await session.commit()
        await session.rollback()
    @pytest.mark.asyncio
    async def test_fields_default(self):
        """
        Test case to verify the default values of
        the fields in the ErrorLog model.
        This test case checks that the default values
        of various fields in the ErrorLog model are set correctly.
        It asserts that the default values are not None
        or empty, and that the data types of certain fields are correct.
        """
        error_log = ErrorLog()
        assert error_log.code is not None
        assert error_log.last_change_code is not None
        assert error_log.insert_user_id is not None
        assert error_log.last_update_user_id is not None
        assert error_log.insert_utc_date_time is not None
        assert error_log.last_update_utc_date_time is not None
# endset
        # browserCode,
        # contextCode,
        # createdUTCDateTime
        # description,
        # isClientSideError,
        # isResolved,
        # PacID
        assert isinstance(error_log.pac_code_peek, uuid.UUID)
        # url,
# endset
        assert isinstance(error_log.browser_code, uuid.UUID)
        assert isinstance(error_log.context_code, uuid.UUID)
        assert error_log.created_utc_date_time == datetime(1753, 1, 1)
        assert error_log.description == ""
        assert error_log.is_client_side_error is False
        assert error_log.is_resolved is False
        assert error_log.pac_id == 0
        assert error_log.url == ""
# endset
    @pytest.mark.asyncio
    async def test_last_change_code_concurrency(self, session):
        """
        Test the concurrency of last_change_code in the ErrorLog model.
        This test verifies that the last_change_code
        attribute of a ErrorLog object
        is updated correctly when multiple instances
        of the object are modified
        concurrently.
        Steps:
        1. Create a new ErrorLog object using the ErrorLogFactory.
        2. Get the original value of the last_change_code attribute.
        3. Query the database for the ErrorLog object using the error_log_id.
        4. Modify the code attribute of the retrieved ErrorLog object.
        5. Commit the changes to the database.
        6. Query the database again for the ErrorLog object using the error_log_id.
        7. Get the modified ErrorLog object.
        8. Verify that the last_change_code attribute
            of the modified ErrorLog object
            is different from the original value.
        Raises:
            AssertionError: If the last_change_code attribute
                            of the modified ErrorLog
                            object is the same as the original value.
        """
        error_log = await ErrorLogFactory.create_async(session=session)
        original_last_change_code = error_log.last_change_code
        stmt = select(ErrorLog).where(
            ErrorLog._error_log_id == error_log.error_log_id)  # type: ignore # pylint: disable=protected-access  # noqa: ignore=E501
        result = await session.execute(stmt)
        error_log_1 = result.scalars().first()
        # error_log_1 = await session.query(ErrorLog).filter_by(
        # error_log_id=error_log.error_log_id).first()
        error_log_1.code = uuid.uuid4()
        await session.commit()
        stmt = select(ErrorLog).where(
            ErrorLog._error_log_id == error_log.error_log_id)  # type: ignore # pylint: disable=protected-access  # noqa: ignore=E501
        result = await session.execute(stmt)
        error_log_2 = result.scalars().first()
        # error_log_2 = await session.query(ErrorLog).filter_by(
        # error_log_id=error_log.error_log_id).first()
        error_log_2.code = uuid.uuid4()
        await session.commit()
        assert error_log_2.last_change_code != original_last_change_code
# endset
    # browserCode,
    # contextCode,
    # createdUTCDateTime
    # description,
    # isClientSideError,
    # isResolved,
    # PacID
    @pytest.mark.asyncio
    async def test_invalid_pac_id(self, session):
        """
        Test case for handling an invalid pac ID.
        This test case creates a error_log using the
        ErrorLogFactory and sets an invalid pac ID.
        It then asserts that committing the session
        raises an IntegrityError and rolls back the session.
        Args:
            session: The SQLAlchemy session object.
        Raises:
            IntegrityError: If committing the session
            fails due to an integrity constraint violation.
        """
        error_log = await ErrorLogFactory.create_async(session=session)
        error_log.pac_id = 99999
        with pytest.raises(IntegrityError):
            await session.commit()
        await session.rollback()
    # url,
# endset
