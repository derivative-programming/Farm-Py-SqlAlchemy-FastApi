# models/factory/tests/dyna_flow_async_test.py  # pylint: disable=duplicate-code
# pylint: disable=unused-argument, too-many-public-methods
# pylint: disable=unused-import

"""
This module contains unit tests for the asynchronous
operations of the DynaFlowFactory class.
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
from models import Base, DynaFlow
from models.factory import DynaFlowFactory

TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"


class TestDynaFlowFactoryAsync:
    """
    This class contains unit tests for the asynchronous
    operations of the DynaFlowFactory class.
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
    async def test_dyna_flow_creation(self, session):
        """
        Test case for creating a dyna_flow
        asynchronously.

        Args:
            session: The database session to use.

        Returns:
            None

        Raises:
            AssertionError: If the dyna_flow ID
                is None after creation.
        """
        dyna_flow = await \
            DynaFlowFactory.create_async(
                session=session)
        assert dyna_flow.dyna_flow_id is not None

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
        dyna_flow = await \
            DynaFlowFactory.create_async(
                session=session)
        assert isinstance(dyna_flow.code, uuid.UUID)

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
        dyna_flow: DynaFlow = await \
            DynaFlowFactory.build_async(
                session=session)
        assert dyna_flow.last_change_code == 0

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
        dyna_flow: DynaFlow = await \
            DynaFlowFactory.create_async(
                session=session)
        assert dyna_flow.last_change_code == 1

    @pytest.mark.asyncio
    async def test_last_change_code_default_on_update(self, session):
        """
        Test case for checking the default value of the
        last_change_code attribute after updating the dyna_flow.

        Args:
            session: The database session to use.

        Returns:
            None

        Raises:
            AssertionError: If the last_change_code attribute is not updated.
        """
        dyna_flow = await \
            DynaFlowFactory.create_async(
                session=session)
        initial_code = dyna_flow.last_change_code
        dyna_flow.code = uuid.uuid4()
        await session.commit()
        assert dyna_flow.last_change_code != initial_code

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
        dyna_flow = await \
            DynaFlowFactory.build_async(
                session=session)
        assert dyna_flow.insert_utc_date_time is not None
        assert isinstance(
            dyna_flow.insert_utc_date_time, datetime)

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
        dyna_flow = await \
            DynaFlowFactory.build_async(
                session=session)
        assert dyna_flow.insert_utc_date_time is not None
        assert isinstance(
            dyna_flow.insert_utc_date_time, datetime)
        initial_time = datetime.now(timezone.utc) + timedelta(days=-1)
        dyna_flow.code = uuid.uuid4()
        session.add(dyna_flow)
        await session.commit()
        assert dyna_flow.insert_utc_date_time > \
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
        dyna_flow = await \
            DynaFlowFactory.create_async(
                session=session)
        assert dyna_flow.insert_utc_date_time is not None
        assert isinstance(
            dyna_flow.insert_utc_date_time, datetime)
        initial_time = dyna_flow.insert_utc_date_time
        dyna_flow.code = uuid.uuid4()
        time.sleep(1)
        await session.commit()
        assert dyna_flow.insert_utc_date_time == \
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
        dyna_flow = await \
            DynaFlowFactory.build_async(
                session=session)
        assert dyna_flow.last_update_utc_date_time is not None
        assert isinstance(
            dyna_flow.last_update_utc_date_time, datetime)

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
        dyna_flow = await \
            DynaFlowFactory.build_async(
                session=session)
        assert dyna_flow.last_update_utc_date_time is not None
        assert isinstance(
            dyna_flow.last_update_utc_date_time, datetime)
        initial_time = datetime.now(timezone.utc) + timedelta(days=-1)
        dyna_flow.code = uuid.uuid4()
        session.add(dyna_flow)
        await session.commit()
        assert dyna_flow.last_update_utc_date_time > \
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
        dyna_flow = await \
            DynaFlowFactory.create_async(
                session=session)
        assert dyna_flow.last_update_utc_date_time is not None
        assert isinstance(
            dyna_flow.last_update_utc_date_time, datetime)
        initial_time = dyna_flow.last_update_utc_date_time
        dyna_flow.code = uuid.uuid4()
        time.sleep(1)
        await session.commit()
        assert dyna_flow.last_update_utc_date_time > \
            initial_time

    @pytest.mark.asyncio
    async def test_model_deletion(self, session):
        """
        Test case for deleting a dyna_flow
        from the database.

        Args:
            session: The database session to use.

        Returns:
            None

        Raises:
            AssertionError: If the deleted
            dyna_flow is still
            found in the database.
        """
        dyna_flow = await \
            DynaFlowFactory.create_async(
                session=session)
        await session.delete(dyna_flow)
        await session.commit()

        # Construct the select statement
        stmt = select(DynaFlow).where(
            DynaFlow._dyna_flow_id == (  # type: ignore # pylint: disable=protected-access  # noqa: ignore=E501
                dyna_flow.dyna_flow_id))

        # Execute the statement asynchronously
        result = await session.execute(stmt)

        # Fetch all results
        deleted_dyna_flow = result.scalars().first()

        assert deleted_dyna_flow is None

    @pytest.mark.asyncio
    async def test_data_types(self, session):
        """
        Test case for checking the data types of
        the dyna_flow attributes.

        Args:
            session: The database session to use.

        Returns:
            None

        Raises:
            AssertionError: If any of the attribute types are incorrect.
        """
        obj = await \
            DynaFlowFactory.create_async(
                session=session)
        assert isinstance(obj.dyna_flow_id, int)
        assert isinstance(obj.code, uuid.UUID)
        assert isinstance(obj.last_change_code, int)
        assert isinstance(obj.insert_user_id, uuid.UUID)
        assert isinstance(obj.last_update_user_id, uuid.UUID)
        assert isinstance(obj.completed_utc_date_time, datetime)
        assert isinstance(obj.dependency_dyna_flow_id, int)
        assert obj.description == "" or isinstance(
            obj.description, str)
        assert isinstance(obj.dyna_flow_type_id, int)
        assert isinstance(obj.is_build_task_debug_required, bool)
        assert isinstance(obj.is_canceled, bool)
        assert isinstance(obj.is_cancel_requested, bool)
        assert isinstance(obj.is_completed, bool)
        assert isinstance(obj.is_paused, bool)
        assert isinstance(obj.is_resubmitted, bool)
        assert isinstance(obj.is_run_task_debug_required, bool)
        assert isinstance(obj.is_started, bool)
        assert isinstance(obj.is_successful, bool)
        assert isinstance(obj.is_task_creation_started, bool)
        assert isinstance(obj.is_tasks_created, bool)
        assert isinstance(obj.min_start_utc_date_time, datetime)
        assert isinstance(obj.pac_id, int)
        assert obj.param_1 == "" or isinstance(
            obj.param_1, str)
        assert isinstance(obj.parent_dyna_flow_id, int)
        assert isinstance(obj.priority_level, int)
        assert isinstance(obj.requested_utc_date_time, datetime)
        assert obj.result_value == "" or isinstance(
            obj.result_value, str)
        assert isinstance(obj.root_dyna_flow_id, int)
        assert isinstance(obj.started_utc_date_time, datetime)
        assert isinstance(obj.subject_code, uuid.UUID)
        assert obj.task_creation_processor_identifier == "" or isinstance(
            obj.task_creation_processor_identifier, str)
        # Check for the peek values
        # completedUTCDateTime
        # dependencyDynaFlowID
        # description
        # dynaFlowTypeID

        assert isinstance(obj.dyna_flow_type_code_peek, uuid.UUID)
        # isBuildTaskDebugRequired
        # isCanceled
        # isCancelRequested
        # isCompleted
        # isPaused
        # isResubmitted
        # isRunTaskDebugRequired
        # isStarted
        # isSuccessful
        # isTaskCreationStarted
        # isTasksCreated
        # minStartUTCDateTime
        # pacID

        assert isinstance(obj.pac_code_peek, uuid.UUID)
        # param1
        # parentDynaFlowID
        # priorityLevel
        # requestedUTCDateTime
        # resultValue
        # rootDynaFlowID
        # startedUTCDateTime
        # subjectCode
        # taskCreationProcessorIdentifier

        assert isinstance(obj.insert_utc_date_time, datetime)
        assert isinstance(obj.last_update_utc_date_time, datetime)

    @pytest.mark.asyncio
    async def test_unique_code_constraint(self, session):
        """
        Test case to check the unique code constraint
        for dyna_flows.

        This test creates two dyna_flow
        instances using
        the DynaFlowFactoryand assigns
        the same code to both dyna_flows.
        Then it adds both dyna_flows to the session and
        attempts to commit the changes.
        The test expects an exception to be raised,
        indicating that the unique code constraint has been violated.
        Finally, the test rolls back the session to
        ensure no changes are persisted.

        Note: This test assumes that the
        DynaFlowFactory.create_async()
        method creates unique codes for
        each dyna_flow.
        """

        obj_1 = await DynaFlowFactory.create_async(
            session=session)
        obj_2 = await DynaFlowFactory.create_async(
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
        the fields in the DynaFlow model.

        This test case checks that the default values
        of various fields in the DynaFlow
        model are set correctly.
        It asserts that the default values are not None
        or empty, and that the data types of certain fields are correct.
        """

        new_obj = DynaFlow()
        assert new_obj.code is not None
        assert new_obj.last_change_code is not None
        assert new_obj.insert_user_id is not None
        assert new_obj.last_update_user_id is not None
        assert new_obj.insert_utc_date_time is not None
        assert new_obj.last_update_utc_date_time is not None

        # completedUTCDateTime
        # dependencyDynaFlowID
        # description
        # DynaFlowTypeID

        assert isinstance(new_obj.dyna_flow_type_code_peek, uuid.UUID)
        # isBuildTaskDebugRequired
        # isCanceled
        # isCancelRequested
        # isCompleted
        # isPaused
        # isResubmitted
        # isRunTaskDebugRequired
        # isStarted
        # isSuccessful
        # isTaskCreationStarted
        # isTasksCreated
        # minStartUTCDateTime
        # PacID

        assert isinstance(new_obj.pac_code_peek, uuid.UUID)
        # param1
        # parentDynaFlowID
        # priorityLevel
        # requestedUTCDateTime
        # resultValue
        # rootDynaFlowID
        # startedUTCDateTime
        # subjectCode
        # taskCreationProcessorIdentifier
        assert new_obj.completed_utc_date_time == datetime(1753, 1, 1, 0, 0, tzinfo=timezone.utc)
        assert new_obj.dependency_dyna_flow_id == 0
        assert new_obj.description == ""
        assert new_obj.dyna_flow_type_id == 0
        assert new_obj.is_build_task_debug_required is False
        assert new_obj.is_canceled is False
        assert new_obj.is_cancel_requested is False
        assert new_obj.is_completed is False
        assert new_obj.is_paused is False
        assert new_obj.is_resubmitted is False
        assert new_obj.is_run_task_debug_required is False
        assert new_obj.is_started is False
        assert new_obj.is_successful is False
        assert new_obj.is_task_creation_started is False
        assert new_obj.is_tasks_created is False
        assert new_obj.min_start_utc_date_time == datetime(1753, 1, 1, 0, 0, tzinfo=timezone.utc)
        assert new_obj.pac_id == 0
        assert new_obj.param_1 == ""
        assert new_obj.parent_dyna_flow_id == 0
        assert new_obj.priority_level == 0
        assert new_obj.requested_utc_date_time == datetime(1753, 1, 1, 0, 0, tzinfo=timezone.utc)
        assert new_obj.result_value == ""
        assert new_obj.root_dyna_flow_id == 0
        assert new_obj.started_utc_date_time == datetime(1753, 1, 1, 0, 0, tzinfo=timezone.utc)
        assert isinstance(new_obj.subject_code, uuid.UUID)
        assert new_obj.task_creation_processor_identifier == ""

    @pytest.mark.asyncio
    async def test_last_change_code_concurrency(self, session):
        """
        Test the concurrency of last_change_code
        in the DynaFlow model.

        This test verifies that the last_change_code
        attribute of a DynaFlow object
        is updated correctly when multiple instances
        of the object are modified
        concurrently.

        Steps:
        1. Create a new
            DynaFlow object using
            the DynaFlowFactory.
        2. Get the original value of the
            last_change_code attribute.
        3. Query the database for the DynaFlow
            object using the
            dyna_flow_id.
        4. Modify the code attribute of the
            retrieved DynaFlow object.
        5. Commit the changes to the database.
        6. Query the database again for the
            DynaFlow object using the
            dyna_flow_id.
        7. Get the modified DynaFlow object.
        8. Verify that the last_change_code attribute
            of the modified DynaFlow object
            is different from the original value.

        Raises:
            AssertionError: If the last_change_code attribute
                            of the modified DynaFlow
                            object is the same as the original value.
        """
        dyna_flow = await \
            DynaFlowFactory.create_async(
                session=session)
        original_last_change_code = dyna_flow.last_change_code

        stmt = select(DynaFlow).where(
            DynaFlow._dyna_flow_id == (  # type: ignore # pylint: disable=protected-access  # noqa: ignore=E501
                dyna_flow.dyna_flow_id))
        result = await session.execute(stmt)
        obj_1 = result.scalars().first()

        obj_1.code = uuid.uuid4()
        await session.commit()

        stmt = select(DynaFlow).where(
            DynaFlow._dyna_flow_id == (  # type: ignore # pylint: disable=protected-access  # noqa: ignore=E501
                dyna_flow.dyna_flow_id))
        result = await session.execute(stmt)
        obj_2 = result.scalars().first()

        obj_2.code = uuid.uuid4()
        await session.commit()
        assert obj_2.last_change_code != original_last_change_code
    # completedUTCDateTime
    # dependencyDynaFlowID
    # description
    # DynaFlowTypeID

    @pytest.mark.asyncio
    async def test_invalid_dyna_flow_type_id(self, session):
        """
        Test case for handling an invalid dyna_flow_type ID.

        This test case creates a dyna_flow using the
        DynaFlowFactory and sets an invalid dyna_flow_type ID.
        It then asserts that committing the session
        raises an IntegrityError and rolls back the session.

        Args:
            session: The SQLAlchemy session object.

        Raises:
            IntegrityError: If committing the session
            fails due to an integrity constraint violation.
        """
        dyna_flow = await \
            DynaFlowFactory.create_async(
                session=session)
        dyna_flow.dyna_flow_type_id = 99999
        with pytest.raises(IntegrityError):
            await session.commit()
        await session.rollback()
    # isBuildTaskDebugRequired
    # isCanceled
    # isCancelRequested
    # isCompleted
    # isPaused
    # isResubmitted
    # isRunTaskDebugRequired
    # isStarted
    # isSuccessful
    # isTaskCreationStarted
    # isTasksCreated
    # minStartUTCDateTime
    # PacID

    @pytest.mark.asyncio
    async def test_invalid_pac_id(self, session):
        """
        Test case for handling an invalid pac ID.

        This test case creates a dyna_flow using the
        DynaFlowFactory and sets an invalid pac ID.
        It then asserts that committing the session
        raises an IntegrityError and rolls back the session.

        Args:
            session: The SQLAlchemy session object.

        Raises:
            IntegrityError: If committing the session
            fails due to an integrity constraint violation.
        """
        dyna_flow = await \
            DynaFlowFactory.create_async(
                session=session)
        dyna_flow.pac_id = 99999
        with pytest.raises(IntegrityError):
            await session.commit()
        await session.rollback()
    # param1
    # parentDynaFlowID
    # priorityLevel
    # requestedUTCDateTime
    # resultValue
    # rootDynaFlowID
    # startedUTCDateTime
    # subjectCode
    # taskCreationProcessorIdentifier
