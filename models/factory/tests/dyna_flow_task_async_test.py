# models/factory/tests/dyna_flow_task_async_test.py  # pylint: disable=duplicate-code
# pylint: disable=unused-argument, too-many-public-methods
# pylint: disable=unused-import

"""
This module contains unit tests for the asynchronous
operations of the DynaFlowTaskFactory class.
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
from models import Base, DynaFlowTask
from models.factory import DynaFlowTaskFactory

TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"


class TestDynaFlowTaskFactoryAsync:
    """
    This class contains unit tests for the asynchronous
    operations of the DynaFlowTaskFactory class.
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
    async def test_dyna_flow_task_creation(self, session):
        """
        Test case for creating a dyna_flow_task
        asynchronously.

        Args:
            session: The database session to use.

        Returns:
            None

        Raises:
            AssertionError: If the dyna_flow_task ID
                is None after creation.
        """
        dyna_flow_task = await \
            DynaFlowTaskFactory.create_async(
                session=session)
        assert dyna_flow_task.dyna_flow_task_id is not None

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
        dyna_flow_task = await \
            DynaFlowTaskFactory.create_async(
                session=session)
        assert isinstance(dyna_flow_task.code, uuid.UUID)

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
        dyna_flow_task: DynaFlowTask = await \
            DynaFlowTaskFactory.build_async(
                session=session)
        assert dyna_flow_task.last_change_code == 0

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
        dyna_flow_task: DynaFlowTask = await \
            DynaFlowTaskFactory.create_async(
                session=session)
        assert dyna_flow_task.last_change_code == 1

    @pytest.mark.asyncio
    async def test_last_change_code_default_on_update(self, session):
        """
        Test case for checking the default value of the
        last_change_code attribute after updating the dyna_flow_task.

        Args:
            session: The database session to use.

        Returns:
            None

        Raises:
            AssertionError: If the last_change_code attribute is not updated.
        """
        dyna_flow_task = await \
            DynaFlowTaskFactory.create_async(
                session=session)
        initial_code = dyna_flow_task.last_change_code
        dyna_flow_task.code = uuid.uuid4()
        await session.commit()
        assert dyna_flow_task.last_change_code != initial_code

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
        dyna_flow_task = await \
            DynaFlowTaskFactory.build_async(
                session=session)
        assert dyna_flow_task.insert_utc_date_time is not None
        assert isinstance(
            dyna_flow_task.insert_utc_date_time, datetime)

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
        dyna_flow_task = await \
            DynaFlowTaskFactory.build_async(
                session=session)
        assert dyna_flow_task.insert_utc_date_time is not None
        assert isinstance(
            dyna_flow_task.insert_utc_date_time, datetime)
        initial_time = datetime.now(timezone.utc) + timedelta(days=-1)
        dyna_flow_task.code = uuid.uuid4()
        session.add(dyna_flow_task)
        await session.commit()
        assert dyna_flow_task.insert_utc_date_time > \
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
        dyna_flow_task = await \
            DynaFlowTaskFactory.create_async(
                session=session)
        assert dyna_flow_task.insert_utc_date_time is not None
        assert isinstance(
            dyna_flow_task.insert_utc_date_time, datetime)
        initial_time = dyna_flow_task.insert_utc_date_time
        dyna_flow_task.code = uuid.uuid4()
        time.sleep(1)
        await session.commit()
        assert dyna_flow_task.insert_utc_date_time == \
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
        dyna_flow_task = await \
            DynaFlowTaskFactory.build_async(
                session=session)
        assert dyna_flow_task.last_update_utc_date_time is not None
        assert isinstance(
            dyna_flow_task.last_update_utc_date_time, datetime)

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
        dyna_flow_task = await \
            DynaFlowTaskFactory.build_async(
                session=session)
        assert dyna_flow_task.last_update_utc_date_time is not None
        assert isinstance(
            dyna_flow_task.last_update_utc_date_time, datetime)
        initial_time = datetime.now(timezone.utc) + timedelta(days=-1)
        dyna_flow_task.code = uuid.uuid4()
        session.add(dyna_flow_task)
        await session.commit()
        assert dyna_flow_task.last_update_utc_date_time > \
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
        dyna_flow_task = await \
            DynaFlowTaskFactory.create_async(
                session=session)
        assert dyna_flow_task.last_update_utc_date_time is not None
        assert isinstance(
            dyna_flow_task.last_update_utc_date_time, datetime)
        initial_time = dyna_flow_task.last_update_utc_date_time
        dyna_flow_task.code = uuid.uuid4()
        time.sleep(1)
        await session.commit()
        assert dyna_flow_task.last_update_utc_date_time > \
            initial_time

    @pytest.mark.asyncio
    async def test_model_deletion(self, session):
        """
        Test case for deleting a dyna_flow_task
        from the database.

        Args:
            session: The database session to use.

        Returns:
            None

        Raises:
            AssertionError: If the deleted
            dyna_flow_task is still
            found in the database.
        """
        dyna_flow_task = await \
            DynaFlowTaskFactory.create_async(
                session=session)
        await session.delete(dyna_flow_task)
        await session.commit()

        # Construct the select statement
        stmt = select(DynaFlowTask).where(
            DynaFlowTask._dyna_flow_task_id == (  # type: ignore # pylint: disable=protected-access  # noqa: ignore=E501
                dyna_flow_task.dyna_flow_task_id))

        # Execute the statement asynchronously
        result = await session.execute(stmt)

        # Fetch all results
        deleted_dyna_flow_task = result.scalars().first()

        assert deleted_dyna_flow_task is None

    @pytest.mark.asyncio
    async def test_data_types(self, session):
        """
        Test case for checking the data types of
        the dyna_flow_task attributes.

        Args:
            session: The database session to use.

        Returns:
            None

        Raises:
            AssertionError: If any of the attribute types are incorrect.
        """
        obj = await \
            DynaFlowTaskFactory.create_async(
                session=session)
        assert isinstance(obj.dyna_flow_task_id, int)
        assert isinstance(obj.code, uuid.UUID)
        assert isinstance(obj.last_change_code, int)
        assert isinstance(obj.insert_user_id, uuid.UUID)
        assert isinstance(obj.last_update_user_id, uuid.UUID)
        assert isinstance(obj.completed_utc_date_time, datetime)
        assert isinstance(obj.dependency_dyna_flow_task_id, int)
        assert obj.description == "" or isinstance(
            obj.description, str)
        assert isinstance(obj.dyna_flow_id, int)
        assert isinstance(obj.dyna_flow_subject_code, uuid.UUID)
        assert isinstance(obj.dyna_flow_task_type_id, int)
        assert isinstance(obj.is_canceled, bool)
        assert isinstance(obj.is_cancel_requested, bool)
        assert isinstance(obj.is_completed, bool)
        assert isinstance(obj.is_parallel_run_allowed, bool)
        assert isinstance(obj.is_run_task_debug_required, bool)
        assert isinstance(obj.is_started, bool)
        assert isinstance(obj.is_successful, bool)
        assert isinstance(obj.max_retry_count, int)
        assert isinstance(obj.min_start_utc_date_time, datetime)
        assert obj.param_1 == "" or isinstance(
            obj.param_1, str)
        assert obj.param_2 == "" or isinstance(
            obj.param_2, str)
        assert obj.processor_identifier == "" or isinstance(
            obj.processor_identifier, str)
        assert isinstance(obj.requested_utc_date_time, datetime)
        assert obj.result_value == "" or isinstance(
            obj.result_value, str)
        assert isinstance(obj.retry_count, int)
        assert isinstance(obj.started_utc_date_time, datetime)
        # Check for the peek values
        # completedUTCDateTime
        # dependencyDynaFlowTaskID,
        # description,
        # dynaFlowID

        assert isinstance(obj.dyna_flow_code_peek, uuid.UUID)
        # dynaFlowSubjectCode,
        # dynaFlowTaskTypeID

        assert isinstance(obj.dyna_flow_task_type_code_peek, uuid.UUID)
        # isCanceled,
        # isCancelRequested,
        # isCompleted,
        # isParallelRunAllowed,
        # isRunTaskDebugRequired,
        # isStarted,
        # isSuccessful,
        # maxRetryCount,
        # minStartUTCDateTime
        # param1,
        # param2,
        # processorIdentifier,
        # requestedUTCDateTime
        # resultValue,
        # retryCount,
        # startedUTCDateTime

        assert isinstance(obj.insert_utc_date_time, datetime)
        assert isinstance(obj.last_update_utc_date_time, datetime)

    @pytest.mark.asyncio
    async def test_unique_code_constraint(self, session):
        """
        Test case to check the unique code constraint
        for dyna_flow_tasks.

        This test creates two dyna_flow_task
        instances using
        the DynaFlowTaskFactoryand assigns
        the same code to both dyna_flow_tasks.
        Then it adds both dyna_flow_tasks to the session and
        attempts to commit the changes.
        The test expects an exception to be raised,
        indicating that the unique code constraint has been violated.
        Finally, the test rolls back the session to
        ensure no changes are persisted.

        Note: This test assumes that the
        DynaFlowTaskFactory.create_async()
        method creates unique codes for
        each dyna_flow_task.
        """

        obj_1 = await DynaFlowTaskFactory.create_async(
            session=session)
        obj_2 = await DynaFlowTaskFactory.create_async(
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
        the fields in the DynaFlowTask model.

        This test case checks that the default values
        of various fields in the DynaFlowTask
        model are set correctly.
        It asserts that the default values are not None
        or empty, and that the data types of certain fields are correct.
        """

        new_obj = DynaFlowTask()
        assert new_obj.code is not None
        assert new_obj.last_change_code is not None
        assert new_obj.insert_user_id is not None
        assert new_obj.last_update_user_id is not None
        assert new_obj.insert_utc_date_time is not None
        assert new_obj.last_update_utc_date_time is not None

        # completedUTCDateTime
        # dependencyDynaFlowTaskID,
        # description,
        # DynaFlowID

        assert isinstance(new_obj.dyna_flow_code_peek, uuid.UUID)
        # dynaFlowSubjectCode,
        # DynaFlowTaskTypeID

        assert isinstance(new_obj.dyna_flow_task_type_code_peek, uuid.UUID)
        # isCanceled,
        # isCancelRequested,
        # isCompleted,
        # isParallelRunAllowed,
        # isRunTaskDebugRequired,
        # isStarted,
        # isSuccessful,
        # maxRetryCount,
        # minStartUTCDateTime
        # param1,
        # param2,
        # processorIdentifier,
        # requestedUTCDateTime
        # resultValue,
        # retryCount,
        # startedUTCDateTime
        assert new_obj.completed_utc_date_time == datetime(1753, 1, 1, 0, 0, tzinfo=timezone.utc)
        assert new_obj.dependency_dyna_flow_task_id == 0
        assert new_obj.description == ""
        assert new_obj.dyna_flow_id == 0
        assert isinstance(new_obj.dyna_flow_subject_code, uuid.UUID)
        assert new_obj.dyna_flow_task_type_id == 0
        assert new_obj.is_canceled is False
        assert new_obj.is_cancel_requested is False
        assert new_obj.is_completed is False
        assert new_obj.is_parallel_run_allowed is False
        assert new_obj.is_run_task_debug_required is False
        assert new_obj.is_started is False
        assert new_obj.is_successful is False
        assert new_obj.max_retry_count == 0
        assert new_obj.min_start_utc_date_time == datetime(1753, 1, 1, 0, 0, tzinfo=timezone.utc)
        assert new_obj.param_1 == ""
        assert new_obj.param_2 == ""
        assert new_obj.processor_identifier == ""
        assert new_obj.requested_utc_date_time == datetime(1753, 1, 1, 0, 0, tzinfo=timezone.utc)
        assert new_obj.result_value == ""
        assert new_obj.retry_count == 0
        assert new_obj.started_utc_date_time == datetime(1753, 1, 1, 0, 0, tzinfo=timezone.utc)

    @pytest.mark.asyncio
    async def test_last_change_code_concurrency(self, session):
        """
        Test the concurrency of last_change_code
        in the DynaFlowTask model.

        This test verifies that the last_change_code
        attribute of a DynaFlowTask object
        is updated correctly when multiple instances
        of the object are modified
        concurrently.

        Steps:
        1. Create a new
            DynaFlowTask object using
            the DynaFlowTaskFactory.
        2. Get the original value of the
            last_change_code attribute.
        3. Query the database for the DynaFlowTask
            object using the
            dyna_flow_task_id.
        4. Modify the code attribute of the
            retrieved DynaFlowTask object.
        5. Commit the changes to the database.
        6. Query the database again for the
            DynaFlowTask object using the
            dyna_flow_task_id.
        7. Get the modified DynaFlowTask object.
        8. Verify that the last_change_code attribute
            of the modified DynaFlowTask object
            is different from the original value.

        Raises:
            AssertionError: If the last_change_code attribute
                            of the modified DynaFlowTask
                            object is the same as the original value.
        """
        dyna_flow_task = await \
            DynaFlowTaskFactory.create_async(
                session=session)
        original_last_change_code = dyna_flow_task.last_change_code

        stmt = select(DynaFlowTask).where(
            DynaFlowTask._dyna_flow_task_id == (  # type: ignore # pylint: disable=protected-access  # noqa: ignore=E501
                dyna_flow_task.dyna_flow_task_id))
        result = await session.execute(stmt)
        obj_1 = result.scalars().first()

        # obj_1 = await session.query(DynaFlowTask).filter_by(
        # dyna_flow_task_id=dyna_flow_task.dyna_flow_task_id).first()
        obj_1.code = uuid.uuid4()
        await session.commit()

        stmt = select(DynaFlowTask).where(
            DynaFlowTask._dyna_flow_task_id == (  # type: ignore # pylint: disable=protected-access  # noqa: ignore=E501
                dyna_flow_task.dyna_flow_task_id))
        result = await session.execute(stmt)
        obj_2 = result.scalars().first()

        # obj_2 = await session.query(DynaFlowTask).filter_by(
        # dyna_flow_task_id=dyna_flow_task.dyna_flow_task_id).first()
        obj_2.code = uuid.uuid4()
        await session.commit()
        assert obj_2.last_change_code != original_last_change_code
    # completedUTCDateTime
    # dependencyDynaFlowTaskID,
    # description,
    # DynaFlowID

    @pytest.mark.asyncio
    async def test_invalid_dyna_flow_id(self, session):
        """
        Test case for handling an invalid dyna_flow ID.

        This test case creates a dyna_flow_task using the
        DynaFlowTaskFactory and sets an invalid dyna_flow ID.
        It then asserts that committing the session
        raises an IntegrityError and rolls back the session.

        Args:
            session: The SQLAlchemy session object.

        Raises:
            IntegrityError: If committing the session
            fails due to an integrity constraint violation.
        """
        dyna_flow_task = await \
            DynaFlowTaskFactory.create_async(
                session=session)
        dyna_flow_task.dyna_flow_id = 99999
        with pytest.raises(IntegrityError):
            await session.commit()
        await session.rollback()
    # dynaFlowSubjectCode,
    # DynaFlowTaskTypeID

    @pytest.mark.asyncio
    async def test_invalid_dyna_flow_task_type_id(self, session):
        """
        Test case for handling an invalid dyna_flow_task_type ID.

        This test case creates a dyna_flow_task using the
        DynaFlowTaskFactory and sets an invalid dyna_flow_task_type ID.
        It then asserts that committing the session
        raises an IntegrityError and rolls back the session.

        Args:
            session: The SQLAlchemy session object.

        Raises:
            IntegrityError: If committing the session
            fails due to an integrity constraint violation.
        """
        dyna_flow_task = await \
            DynaFlowTaskFactory.create_async(
                session=session)
        dyna_flow_task.dyna_flow_task_type_id = 99999
        with pytest.raises(IntegrityError):
            await session.commit()
        await session.rollback()
    # isCanceled,
    # isCancelRequested,
    # isCompleted,
    # isParallelRunAllowed,
    # isRunTaskDebugRequired,
    # isStarted,
    # isSuccessful,
    # maxRetryCount,
    # minStartUTCDateTime
    # param1,
    # param2,
    # processorIdentifier,
    # requestedUTCDateTime
    # resultValue,
    # retryCount,
    # startedUTCDateTime
