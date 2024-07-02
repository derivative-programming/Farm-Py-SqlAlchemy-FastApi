# models/factory/tests/dyna_flow_test.py
# pylint: disable=unused-import
"""
This module contains unit tests for the DynaFlowFactory
class in the models.factory package.
"""

from decimal import Decimal  # noqa: F401
import time
import math  # noqa: F401
import uuid  # noqa: F401
import logging
from datetime import datetime, date, timedelta  # noqa: F401
import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from models import Base, DynaFlow
from models.factory import DynaFlowFactory
from services.logging_config import get_logger
logger = get_logger(__name__)

DATABASE_URL = "sqlite:///:memory:"


class TestDynaFlowFactory:
    """
    This class contains unit tests for the DynaFlowFactory class.
    """

    @pytest.fixture(scope="module")
    def engine(self):
        """
        Fixture for creating a database engine.
        """
        engine = create_engine(DATABASE_URL, echo=False)
        # FKs are not activated by default in sqllite
        with engine.connect() as conn:
            conn.execute(text("PRAGMA foreign_keys=ON"))
        yield engine
        engine.dispose()

    @pytest.fixture
    def session(self, engine):
        """
        Fixture for creating a database session.
        """
        Base.metadata.create_all(engine)
        SessionLocal = sessionmaker(  # pylint: disable=invalid-name
            bind=engine, expire_on_commit=False)
        session_instance = SessionLocal()
        yield session_instance
        session_instance.close()

    def test_dyna_flow_creation(self, session):
        """
        Test case for creating a dyna_flow.
        """
        new_obj = DynaFlowFactory.create(
            session=session)
        assert new_obj.dyna_flow_id is not None

    def test_code_default(self, session):
        """
        Test case for checking the default value of the code attribute.
        """
        new_obj = DynaFlowFactory.create(
            session=session)
        assert isinstance(new_obj.code, uuid.UUID)

    def test_last_change_code_default_on_build(self, session):
        """
        Test case for checking the default value of
        the last_change_code attribute on build.
        """
        new_obj: DynaFlow = DynaFlowFactory.build(
            session=session)
        assert new_obj.last_change_code == 0

    def test_last_change_code_default_on_creation(self, session):
        """
        Test case for checking the default value of the
        last_change_code attribute on creation.
        """
        new_obj: DynaFlow = DynaFlowFactory.create(
            session=session)
        assert new_obj.last_change_code == 1

    def test_last_change_code_default_on_update(self, session):
        """
        Test case for checking the default value of the
        last_change_code attribute on update.
        """
        new_obj = DynaFlowFactory.create(
            session=session)
        initial_code = new_obj.last_change_code
        new_obj.code = uuid.uuid4()
        session.commit()
        assert new_obj.last_change_code != \
            initial_code

    def test_date_inserted_on_build(self, session):
        """
        Test case for checking the value of the
        insert_utc_date_time attribute on build.
        """
        new_obj = DynaFlowFactory.build(
            session=session)
        assert new_obj.insert_utc_date_time is not None
        assert isinstance(
            new_obj.insert_utc_date_time, datetime)

    def test_date_inserted_on_initial_save(self, session):
        """
        Test case for checking the value of the
        insert_utc_date_time attribute on initial save.
        """
        new_obj = DynaFlowFactory.build(
            session=session)
        assert new_obj.insert_utc_date_time is not None
        assert isinstance(
            new_obj.insert_utc_date_time, datetime)
        initial_time = datetime.utcnow() + timedelta(days=-1)
        new_obj.code = uuid.uuid4()
        session.add(new_obj)
        session.commit()
        assert new_obj.insert_utc_date_time > \
            initial_time

    def test_date_inserted_on_second_save(self, session):
        """
        Test case for checking the value of the
        insert_utc_date_time attribute on second save.
        """
        new_obj = DynaFlowFactory(
            session=session)
        assert new_obj.insert_utc_date_time is not None
        assert isinstance(
            new_obj.insert_utc_date_time, datetime)
        initial_time = new_obj.insert_utc_date_time
        new_obj.code = uuid.uuid4()
        time.sleep(1)
        session.commit()
        assert new_obj.insert_utc_date_time == initial_time

    def test_date_updated_on_build(self, session):
        """
        Test case for checking the value of the
        last_update_utc_date_time attribute on build.
        """
        new_obj = DynaFlowFactory.build(
            session=session)
        assert new_obj.last_update_utc_date_time is not None
        assert isinstance(
            new_obj.last_update_utc_date_time, datetime)

    def test_date_updated_on_initial_save(self, session):
        """
        Test case for checking the value of the
        last_update_utc_date_time attribute on initial save.
        """
        new_obj = DynaFlowFactory.build(
            session=session)
        assert new_obj.last_update_utc_date_time is not None
        assert isinstance(
            new_obj.last_update_utc_date_time, datetime)
        initial_time = datetime.utcnow() + timedelta(days=-1)
        new_obj.code = uuid.uuid4()
        session.add(new_obj)
        session.commit()
        assert new_obj.last_update_utc_date_time > \
            initial_time

    def test_date_updated_on_second_save(self, session):
        """
        Test case for checking the value of the
        last_update_utc_date_time attribute on second save.
        """
        new_obj = DynaFlowFactory(
            session=session)
        assert new_obj.last_update_utc_date_time is not None
        assert isinstance(
            new_obj.last_update_utc_date_time, datetime)
        initial_time = new_obj.last_update_utc_date_time
        new_obj.code = uuid.uuid4()
        time.sleep(1)
        session.commit()
        assert new_obj.last_update_utc_date_time > \
            initial_time

    def test_model_deletion(self, session):
        """
        Test case for deleting a
        dyna_flow model.
        """
        new_obj = DynaFlowFactory.create(
            session=session)
        session.delete(new_obj)
        session.commit()
        deleted_dyna_flow = session.query(
            DynaFlow).filter_by(
            _dyna_flow_id=(
                new_obj.dyna_flow_id)
        ).first()
        assert deleted_dyna_flow is None

    def test_data_types(self, session):
        """
        Test case for checking the data types of
        the dyna_flow attributes.
        """
        obj = DynaFlowFactory.create(
            session=session)
        assert isinstance(obj.dyna_flow_id, int)
        assert isinstance(obj.code, uuid.UUID)
        assert isinstance(obj.last_change_code, int)
        assert isinstance(obj.insert_user_id, uuid.UUID)
        assert isinstance(obj.last_update_user_id, uuid.UUID)
        assert isinstance(obj.completed_utc_date_time,
                          datetime)
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
        assert isinstance(obj.min_start_utc_date_time,
                          datetime)
        assert isinstance(obj.pac_id, int)
        assert obj.param_1 == "" or isinstance(
            obj.param_1, str)
        assert isinstance(obj.parent_dyna_flow_id, int)
        assert isinstance(obj.priority_level, int)
        assert isinstance(obj.requested_utc_date_time,
                          datetime)
        assert obj.result_value == "" or isinstance(
            obj.result_value, str)
        assert isinstance(obj.root_dyna_flow_id, int)
        assert isinstance(obj.started_utc_date_time,
                          datetime)
        # subjectCode
        assert isinstance(
            obj.subject_code, uuid.UUID)
        assert obj.task_creation_processor_identifier == "" or isinstance(
            obj.task_creation_processor_identifier, str)
        # completedUTCDateTime
        # dependencyDynaFlowID,
        # description,
        # dynaFlowTypeID

        assert isinstance(
            obj.dyna_flow_type_code_peek, uuid.UUID)
        # isBuildTaskDebugRequired,
        # isCanceled,
        # isCancelRequested,
        # isCompleted,
        # isPaused,
        # isResubmitted,
        # isRunTaskDebugRequired,
        # isStarted,
        # isSuccessful,
        # isTaskCreationStarted,
        # isTasksCreated,
        # minStartUTCDateTime
        # pacID

        assert isinstance(
            obj.pac_code_peek, uuid.UUID)
        # param1,
        # parentDynaFlowID,
        # priorityLevel,
        # requestedUTCDateTime
        # resultValue,
        # rootDynaFlowID,
        # startedUTCDateTime
        # subjectCode,
        # taskCreationProcessorIdentifier,
        assert isinstance(obj.insert_utc_date_time, datetime)
        assert isinstance(obj.last_update_utc_date_time, datetime)

    def test_unique_code_constraint(self, session):
        """
        Test case for checking the unique code constraint.
        """
        dyna_flow_1 = DynaFlowFactory.create(
            session=session)
        dyna_flow_2 = DynaFlowFactory.create(
            session=session)
        dyna_flow_2.code = dyna_flow_1.code
        session.add_all([dyna_flow_1,
                         dyna_flow_2])
        with pytest.raises(Exception):
            session.commit()
        session.rollback()

    def test_fields_default(self):
        """
        Test case for checking the default values of
        the dyna_flow fields.
        """
        new_obj = DynaFlow()
        assert new_obj.code is not None
        assert new_obj.last_change_code is not None
        assert new_obj.insert_user_id == uuid.UUID(int=0)
        assert new_obj.last_update_user_id == uuid.UUID(int=0)
        assert new_obj.insert_utc_date_time is not None
        assert new_obj.last_update_utc_date_time is not None
        # completedUTCDateTime
        # dependencyDynaFlowID,
        # description,
        # DynaFlowTypeID

        assert isinstance(
            new_obj.dyna_flow_type_code_peek, uuid.UUID)
        # isBuildTaskDebugRequired,
        # isCanceled,
        # isCancelRequested,
        # isCompleted,
        # isPaused,
        # isResubmitted,
        # isRunTaskDebugRequired,
        # isStarted,
        # isSuccessful,
        # isTaskCreationStarted,
        # isTasksCreated,
        # minStartUTCDateTime
        # PacID

        assert isinstance(
            new_obj.pac_code_peek, uuid.UUID)
        # param1,
        # parentDynaFlowID,
        # priorityLevel,
        # requestedUTCDateTime
        # resultValue,
        # rootDynaFlowID,
        # startedUTCDateTime
        # subjectCode,
        # taskCreationProcessorIdentifier,
        assert new_obj is not None
        assert new_obj.completed_utc_date_time == datetime(1753, 1, 1)
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
        assert new_obj.min_start_utc_date_time == datetime(1753, 1, 1)
        assert new_obj.pac_id == 0
        assert new_obj.param_1 == ""
        assert new_obj.parent_dyna_flow_id == 0
        assert new_obj.priority_level == 0
        assert new_obj.requested_utc_date_time == datetime(1753, 1, 1)
        assert new_obj.result_value == ""
        assert new_obj.root_dyna_flow_id == 0
        assert new_obj.started_utc_date_time == datetime(1753, 1, 1)
        # subject_code
        assert isinstance(
            new_obj.subject_code,
            uuid.UUID
        )
        assert new_obj.task_creation_processor_identifier == ""

    def test_last_change_code_concurrency(self, session):
        """
        Test case to verify the concurrency of
        last_change_code in the DynaFlow
        model.

        This test case checks if the last_change_code
        of a DynaFlow object is
        updated correctly
        when multiple changes are made concurrently.
        It creates a DynaFlow object,
        retrieves it from the database, and updates its code
        attribute twice in separate transactions.
        Finally, it asserts that the last_change_code
        of the second retrieved DynaFlow object
        is different from the original last_change_code.

        Args:
            session (Session): The SQLAlchemy session object.

        Returns:
            None
        """

        new_obj = DynaFlowFactory.create(
            session=session)
        original_last_change_code = \
            new_obj.last_change_code
        dyna_flow_1 = session.query(
            DynaFlow).filter_by(
            _dyna_flow_id=(
                new_obj.dyna_flow_id)
        ).first()
        dyna_flow_1.code = uuid.uuid4()
        session.commit()
        dyna_flow_2 = session.query(
            DynaFlow).filter_by(
            _dyna_flow_id=(
                new_obj.dyna_flow_id)
        ).first()
        dyna_flow_2.code = uuid.uuid4()
        session.commit()
        assert dyna_flow_2.last_change_code != \
            original_last_change_code
    # completedUTCDateTime
    # dependencyDynaFlowID,
    # description,
    # DynaFlowTypeID

    def test_invalid_dyna_flow_type_id(self, session):
        """
        Test case to check if an invalid dyna_flow_type ID raises an IntegrityError.

        This test case creates a dyna_flow object using
        the DynaFlowFactory and assigns an invalid dyna_flow_type ID to it.
        It then tries to commit the changes to the
        session and expects an IntegrityError to be raised.
        Finally, it rolls back the session to ensure
        no changes are persisted.

        Args:
            session (Session): The SQLAlchemy session object.

        Raises:
            IntegrityError: If the changes to the
                session violate any integrity constraints.

        """
        new_obj = DynaFlowFactory.create(
            session=session)
        new_obj.dyna_flow_type_id = 99999
        with pytest.raises(IntegrityError):
            session.commit()
        session.rollback()
    # isBuildTaskDebugRequired,
    # isCanceled,
    # isCancelRequested,
    # isCompleted,
    # isPaused,
    # isResubmitted,
    # isRunTaskDebugRequired,
    # isStarted,
    # isSuccessful,
    # isTaskCreationStarted,
    # isTasksCreated,
    # minStartUTCDateTime
    # PacID

    def test_invalid_pac_id(self, session):
        """
        Test case to check if an invalid pac ID raises an IntegrityError.

        This test case creates a dyna_flow object using
        the DynaFlowFactory and assigns an invalid pac ID to it.
        It then tries to commit the changes to the
        session and expects an IntegrityError to be raised.
        Finally, it rolls back the session to ensure
        no changes are persisted.

        Args:
            session (Session): The SQLAlchemy session object.

        Raises:
            IntegrityError: If the changes to the
                session violate any integrity constraints.

        """
        new_obj = DynaFlowFactory.create(
            session=session)
        new_obj.pac_id = 99999
        with pytest.raises(IntegrityError):
            session.commit()
        session.rollback()
    # param1,
    # parentDynaFlowID,
    # priorityLevel,
    # requestedUTCDateTime
    # resultValue,
    # rootDynaFlowID,
    # startedUTCDateTime
    # subjectCode,
    # taskCreationProcessorIdentifier,
