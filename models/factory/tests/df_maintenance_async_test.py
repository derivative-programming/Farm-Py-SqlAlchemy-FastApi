# models/factory/tests/df_maintenance_async_test.py  # pylint: disable=duplicate-code # noqa: E501
# pylint: disable=unused-argument, too-many-public-methods
# pylint: disable=unused-import

"""
This module contains unit tests for the asynchronous
operations of the DFMaintenanceFactory class.
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
from models import Base, DFMaintenance
from models.factory import DFMaintenanceFactory

TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"


class TestDFMaintenanceFactoryAsync:
    """
    This class contains unit tests for the asynchronous
    operations of the DFMaintenanceFactory class.
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
            testing_session_local = sessionmaker(
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
    async def test_df_maintenance_creation(self, session):
        """
        Test case for creating a df_maintenance
        asynchronously.

        Args:
            session: The database session to use.

        Returns:
            None

        Raises:
            AssertionError: If the df_maintenance ID
                is None after creation.
        """
        df_maintenance = await \
            DFMaintenanceFactory.create_async(
                session=session)
        assert df_maintenance.df_maintenance_id is not None

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
        df_maintenance = await \
            DFMaintenanceFactory.create_async(
                session=session)
        assert isinstance(df_maintenance.code, uuid.UUID)

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
        df_maintenance: DFMaintenance = await \
            DFMaintenanceFactory.build_async(
                session=session)
        assert df_maintenance.last_change_code == 0

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
        df_maintenance: DFMaintenance = await \
            DFMaintenanceFactory.create_async(
                session=session)
        assert df_maintenance.last_change_code == 1

    @pytest.mark.asyncio
    async def test_last_change_code_default_on_update(self, session):
        """
        Test case for checking the default value of the
        last_change_code attribute after updating the df_maintenance.

        Args:
            session: The database session to use.

        Returns:
            None

        Raises:
            AssertionError: If the last_change_code attribute is not updated.
        """
        df_maintenance = await \
            DFMaintenanceFactory.create_async(
                session=session)
        initial_code = df_maintenance.last_change_code
        df_maintenance.code = uuid.uuid4()
        await session.commit()
        assert df_maintenance.last_change_code != initial_code

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
        df_maintenance = await \
            DFMaintenanceFactory.build_async(
                session=session)
        assert df_maintenance.insert_utc_date_time is not None
        assert isinstance(
            df_maintenance.insert_utc_date_time, datetime)

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
        df_maintenance = await \
            DFMaintenanceFactory.build_async(
                session=session)
        assert df_maintenance.insert_utc_date_time is not None
        assert isinstance(
            df_maintenance.insert_utc_date_time, datetime)
        initial_time = datetime.now(timezone.utc) + timedelta(days=-1)
        df_maintenance.code = uuid.uuid4()
        session.add(df_maintenance)
        await session.commit()
        assert df_maintenance.insert_utc_date_time > \
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
        df_maintenance = await \
            DFMaintenanceFactory.create_async(
                session=session)
        assert df_maintenance.insert_utc_date_time is not None
        assert isinstance(
            df_maintenance.insert_utc_date_time, datetime)
        initial_time = df_maintenance.insert_utc_date_time
        df_maintenance.code = uuid.uuid4()
        time.sleep(1)
        await session.commit()
        assert df_maintenance.insert_utc_date_time == \
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
        df_maintenance = await \
            DFMaintenanceFactory.build_async(
                session=session)
        assert df_maintenance.last_update_utc_date_time is not None
        assert isinstance(
            df_maintenance.last_update_utc_date_time, datetime)

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
        df_maintenance = await \
            DFMaintenanceFactory.build_async(
                session=session)
        assert df_maintenance.last_update_utc_date_time is not None
        assert isinstance(
            df_maintenance.last_update_utc_date_time, datetime)
        initial_time = datetime.now(timezone.utc) + timedelta(days=-1)
        df_maintenance.code = uuid.uuid4()
        session.add(df_maintenance)
        await session.commit()
        assert df_maintenance.last_update_utc_date_time > \
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
        df_maintenance = await \
            DFMaintenanceFactory.create_async(
                session=session)
        assert df_maintenance.last_update_utc_date_time is not None
        assert isinstance(
            df_maintenance.last_update_utc_date_time, datetime)
        initial_time = df_maintenance.last_update_utc_date_time
        df_maintenance.code = uuid.uuid4()
        time.sleep(1)
        await session.commit()
        assert df_maintenance.last_update_utc_date_time > \
            initial_time

    @pytest.mark.asyncio
    async def test_model_deletion(self, session):
        """
        Test case for deleting a df_maintenance
        from the database.

        Args:
            session: The database session to use.

        Returns:
            None

        Raises:
            AssertionError: If the deleted
            df_maintenance is still
            found in the database.
        """
        df_maintenance = await \
            DFMaintenanceFactory.create_async(
                session=session)
        await session.delete(df_maintenance)
        await session.commit()

        # Construct the select statement
        stmt = select(DFMaintenance).where(
            DFMaintenance._df_maintenance_id == (  # type: ignore # pylint: disable=protected-access  # noqa: ignore=E501
                df_maintenance.df_maintenance_id))

        # Execute the statement asynchronously
        result = await session.execute(stmt)

        # Fetch all results
        deleted_df_maintenance = result.scalars().first()

        assert deleted_df_maintenance is None

    @pytest.mark.asyncio
    async def test_data_types(self, session):
        """
        Test case for checking the data types of
        the df_maintenance attributes.

        Args:
            session: The database session to use.

        Returns:
            None

        Raises:
            AssertionError: If any of the attribute types are incorrect.
        """
        obj = await \
            DFMaintenanceFactory.create_async(
                session=session)
        assert isinstance(obj.df_maintenance_id, int)
        assert isinstance(obj.code, uuid.UUID)
        assert isinstance(obj.last_change_code, int)
        assert isinstance(obj.insert_user_id, uuid.UUID)
        assert isinstance(obj.last_update_user_id, uuid.UUID)
        assert isinstance(obj.is_paused, bool)
        assert isinstance(obj.is_scheduled_df_process_request_completed, bool)
        assert isinstance(obj.is_scheduled_df_process_request_started, bool)
        assert isinstance(obj.last_scheduled_df_process_request_utc_date_time, datetime)
        assert isinstance(obj.next_scheduled_df_process_request_utc_date_time, datetime)
        assert isinstance(obj.pac_id, int)
        assert obj.paused_by_username == "" or isinstance(
            obj.paused_by_username, str)
        assert isinstance(obj.paused_utc_date_time, datetime)
        assert obj.scheduled_df_process_request_processor_identifier == "" or isinstance(
            obj.scheduled_df_process_request_processor_identifier, str)
        # Check for the peek values
        # isPaused
        # isScheduledDFProcessRequestCompleted
        # isScheduledDFProcessRequestStarted
        # lastScheduledDFProcessRequestUTCDateTime
        # nextScheduledDFProcessRequestUTCDateTime
        # pacID

        assert isinstance(obj.pac_code_peek, uuid.UUID)
        # pausedByUsername
        # pausedUTCDateTime
        # scheduledDFProcessRequestProcessorIdentifier

        assert isinstance(obj.insert_utc_date_time, datetime)
        assert isinstance(obj.last_update_utc_date_time, datetime)

    @pytest.mark.asyncio
    async def test_unique_code_constraint(self, session):
        """
        Test case to check the unique code constraint
        for df_maintenances.

        This test creates two df_maintenance
        instances using
        the DFMaintenanceFactoryand assigns
        the same code to both df_maintenances.
        Then it adds both df_maintenances to the session and
        attempts to commit the changes.
        The test expects an exception to be raised,
        indicating that the unique code constraint has been violated.
        Finally, the test rolls back the session to
        ensure no changes are persisted.

        Note: This test assumes that the
        DFMaintenanceFactory.create_async()
        method creates unique codes for
        each df_maintenance.
        """

        obj_1 = await DFMaintenanceFactory.create_async(
            session=session)
        obj_2 = await DFMaintenanceFactory.create_async(
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
        the fields in the DFMaintenance model.

        This test case checks that the default values
        of various fields in the DFMaintenance
        model are set correctly.
        It asserts that the default values are not None
        or empty, and that the data types of certain fields are correct.
        """

        new_obj = DFMaintenance()
        assert new_obj.code is not None
        assert new_obj.last_change_code is not None
        assert new_obj.insert_user_id is not None
        assert new_obj.last_update_user_id is not None
        assert new_obj.insert_utc_date_time is not None
        assert new_obj.last_update_utc_date_time is not None

        # isPaused
        # isScheduledDFProcessRequestCompleted
        # isScheduledDFProcessRequestStarted
        # lastScheduledDFProcessRequestUTCDateTime
        # nextScheduledDFProcessRequestUTCDateTime
        # PacID

        assert isinstance(new_obj.pac_code_peek, uuid.UUID)
        # pausedByUsername
        # pausedUTCDateTime
        # scheduledDFProcessRequestProcessorIdentifier
        assert new_obj.is_paused is False
        assert new_obj.is_scheduled_df_process_request_completed is False
        assert new_obj.is_scheduled_df_process_request_started is False
        assert new_obj.last_scheduled_df_process_request_utc_date_time == \
            datetime(1753, 1, 1, 0, 0, tzinfo=timezone.utc)
        assert new_obj.next_scheduled_df_process_request_utc_date_time == \
            datetime(1753, 1, 1, 0, 0, tzinfo=timezone.utc)
        assert new_obj.pac_id == 0
        assert new_obj.paused_by_username == ""
        assert new_obj.paused_utc_date_time == \
            datetime(1753, 1, 1, 0, 0, tzinfo=timezone.utc)
        assert new_obj.scheduled_df_process_request_processor_identifier == ""

    @pytest.mark.asyncio
    async def test_last_change_code_concurrency(self, session):
        """
        Test the concurrency of last_change_code
        in the DFMaintenance model.

        This test verifies that the last_change_code
        attribute of a DFMaintenance object
        is updated correctly when multiple instances
        of the object are modified
        concurrently.

        Steps:
        1. Create a new
            DFMaintenance object using
            the DFMaintenanceFactory.
        2. Get the original value of the
            last_change_code attribute.
        3. Query the database for the DFMaintenance
            object using the
            df_maintenance_id.
        4. Modify the code attribute of the
            retrieved DFMaintenance object.
        5. Commit the changes to the database.
        6. Query the database again for the
            DFMaintenance object using the
            df_maintenance_id.
        7. Get the modified DFMaintenance object.
        8. Verify that the last_change_code attribute
            of the modified DFMaintenance object
            is different from the original value.

        Raises:
            AssertionError: If the last_change_code attribute
                            of the modified DFMaintenance
                            object is the same as the original value.
        """
        df_maintenance = await \
            DFMaintenanceFactory.create_async(
                session=session)
        original_last_change_code = df_maintenance.last_change_code

        stmt = select(DFMaintenance).where(
            DFMaintenance._df_maintenance_id == (  # type: ignore # pylint: disable=protected-access  # noqa: ignore=E501
                df_maintenance.df_maintenance_id))
        result = await session.execute(stmt)
        obj_1 = result.scalars().first()

        obj_1.code = uuid.uuid4()
        await session.commit()

        stmt = select(DFMaintenance).where(
            DFMaintenance._df_maintenance_id == (  # type: ignore # pylint: disable=protected-access  # noqa: ignore=E501
                df_maintenance.df_maintenance_id))
        result = await session.execute(stmt)
        obj_2 = result.scalars().first()

        obj_2.code = uuid.uuid4()
        await session.commit()
        assert obj_2.last_change_code != original_last_change_code
    # isPaused
    # isScheduledDFProcessRequestCompleted
    # isScheduledDFProcessRequestStarted
    # lastScheduledDFProcessRequestUTCDateTime
    # nextScheduledDFProcessRequestUTCDateTime
    # PacID

    @pytest.mark.asyncio
    async def test_invalid_pac_id(self, session):
        """
        Test case for handling an invalid pac ID.

        This test case creates a df_maintenance using the
        DFMaintenanceFactory and sets an invalid pac ID.
        It then asserts that committing the session
        raises an IntegrityError and rolls back the session.

        Args:
            session: The SQLAlchemy session object.

        Raises:
            IntegrityError: If committing the session
            fails due to an integrity constraint violation.
        """
        df_maintenance = await \
            DFMaintenanceFactory.create_async(
                session=session)
        df_maintenance.pac_id = 99999
        with pytest.raises(IntegrityError):
            await session.commit()
        await session.rollback()
    # pausedByUsername
    # pausedUTCDateTime
    # scheduledDFProcessRequestProcessorIdentifier
