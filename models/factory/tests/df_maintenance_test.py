# models/factory/tests/df_maintenance_test.py  # pylint: disable=duplicate-code
# pylint: disable=unused-import, too-many-public-methods
"""
This module contains unit tests for the DFMaintenanceFactory
class in the models.factory package.
"""

import logging
import math  # noqa: F401
import time
import uuid  # noqa: F401
from datetime import date, datetime, timedelta, timezone  # noqa: F401
from decimal import Decimal  # noqa: F401

from sqlalchemy import create_engine, text
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker

import pytest
from models import Base, DFMaintenance
from models.factory import DFMaintenanceFactory
from services.logging_config import get_logger

logger = get_logger(__name__)

TEST_DATABASE_URL = "sqlite:///:memory:"


class TestDFMaintenanceFactory:
    """
    This class contains unit tests for the DFMaintenanceFactory class.
    """

    @pytest.fixture(scope="module")
    def engine(self):
        """
        Fixture for creating a database engine.
        """
        engine = create_engine(TEST_DATABASE_URL, echo=False)
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
        session_local = sessionmaker(  # pylint: disable=invalid-name
            bind=engine, expire_on_commit=False)
        session_instance = session_local()
        yield session_instance
        session_instance.close()

    def test_df_maintenance_creation(self, session):
        """
        Test case for creating a df_maintenance.
        """
        new_obj = DFMaintenanceFactory.create(
            session=session)
        assert new_obj.df_maintenance_id is not None

    def test_code_default(self, session):
        """
        Test case for checking the default value of the code attribute.
        """
        new_obj = DFMaintenanceFactory.create(
            session=session)
        assert isinstance(new_obj.code, uuid.UUID)

    def test_last_change_code_default_on_build(self, session):
        """
        Test case for checking the default value of
        the last_change_code attribute on build.
        """
        new_obj: DFMaintenance = DFMaintenanceFactory.build(
            session=session)
        assert new_obj.last_change_code == 0

    def test_last_change_code_default_on_creation(self, session):
        """
        Test case for checking the default value of the
        last_change_code attribute on creation.
        """
        new_obj: DFMaintenance = DFMaintenanceFactory.create(
            session=session)
        assert new_obj.last_change_code == 1

    def test_last_change_code_default_on_update(self, session):
        """
        Test case for checking the default value of the
        last_change_code attribute on update.
        """
        new_obj = DFMaintenanceFactory.create(
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
        new_obj = DFMaintenanceFactory.build(
            session=session)
        assert new_obj.insert_utc_date_time is not None
        assert isinstance(
            new_obj.insert_utc_date_time, datetime)

    def test_date_inserted_on_initial_save(self, session):
        """
        Test case for checking the value of the
        insert_utc_date_time attribute on initial save.
        """
        new_obj = DFMaintenanceFactory.build(
            session=session)
        assert new_obj.insert_utc_date_time is not None
        assert isinstance(
            new_obj.insert_utc_date_time, datetime)
        initial_time = datetime.now(timezone.utc) + timedelta(days=-1)
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
        new_obj = DFMaintenanceFactory(
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
        new_obj = DFMaintenanceFactory.build(
            session=session)
        assert new_obj.last_update_utc_date_time is not None
        assert isinstance(
            new_obj.last_update_utc_date_time, datetime)

    def test_date_updated_on_initial_save(self, session):
        """
        Test case for checking the value of the
        last_update_utc_date_time attribute on initial save.
        """
        new_obj = DFMaintenanceFactory.build(
            session=session)
        assert new_obj.last_update_utc_date_time is not None
        assert isinstance(
            new_obj.last_update_utc_date_time, datetime)
        initial_time = datetime.now(timezone.utc) + timedelta(days=-1)
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
        new_obj = DFMaintenanceFactory(
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
        df_maintenance model.
        """
        new_obj = DFMaintenanceFactory.create(
            session=session)
        session.delete(new_obj)
        session.commit()
        deleted_df_maintenance = session.query(
            DFMaintenance).filter_by(
            _df_maintenance_id=(
                new_obj.df_maintenance_id)
        ).first()
        assert deleted_df_maintenance is None

    def test_data_types(self, session):
        """
        Test case for checking the data types of
        the df_maintenance attributes.
        """
        obj = DFMaintenanceFactory.create(
            session=session)
        assert isinstance(obj.df_maintenance_id, int)
        assert isinstance(obj.code, uuid.UUID)
        assert isinstance(obj.last_change_code, int)
        assert isinstance(obj.insert_user_id, uuid.UUID)
        assert isinstance(obj.last_update_user_id, uuid.UUID)
        assert isinstance(obj.is_paused, bool)
        assert isinstance(obj.is_scheduled_df_process_request_completed, bool)
        assert isinstance(obj.is_scheduled_df_process_request_started, bool)
        assert isinstance(obj.last_scheduled_df_process_request_utc_date_time,
                          datetime)
        assert isinstance(obj.next_scheduled_df_process_request_utc_date_time,
                          datetime)
        assert isinstance(obj.pac_id, int)
        assert obj.paused_by_username == "" or isinstance(
            obj.paused_by_username, str)
        assert isinstance(obj.paused_utc_date_time,
                          datetime)
        assert obj.scheduled_df_process_request_processor_identifier == "" or isinstance(
            obj.scheduled_df_process_request_processor_identifier, str)
        # isPaused
        # isScheduledDFProcessRequestCompleted
        # isScheduledDFProcessRequestStarted
        # lastScheduledDFProcessRequestUTCDateTime
        # nextScheduledDFProcessRequestUTCDateTime
        # pacID

        assert isinstance(
            obj.pac_code_peek, uuid.UUID)
        # pausedByUsername
        # pausedUTCDateTime
        # scheduledDFProcessRequestProcessorIdentifier
        assert isinstance(obj.insert_utc_date_time, datetime)
        assert isinstance(obj.last_update_utc_date_time, datetime)

    def test_unique_code_constraint(self, session):
        """
        Test case for checking the unique code constraint.
        """
        df_maintenance_1 = DFMaintenanceFactory.create(
            session=session)
        df_maintenance_2 = DFMaintenanceFactory.create(
            session=session)
        df_maintenance_2.code = df_maintenance_1.code
        session.add_all([df_maintenance_1,
                         df_maintenance_2])
        with pytest.raises(Exception):
            session.commit()
        session.rollback()

    def test_fields_default(self):
        """
        Test case for checking the default values of
        the df_maintenance fields.
        """
        new_obj = DFMaintenance()
        assert new_obj.code is not None
        assert new_obj.last_change_code is not None
        assert new_obj.insert_user_id == uuid.UUID(int=0)
        assert new_obj.last_update_user_id == uuid.UUID(int=0)
        assert new_obj.insert_utc_date_time is not None
        assert new_obj.last_update_utc_date_time is not None
        # isPaused
        # isScheduledDFProcessRequestCompleted
        # isScheduledDFProcessRequestStarted
        # lastScheduledDFProcessRequestUTCDateTime
        # nextScheduledDFProcessRequestUTCDateTime
        # PacID

        assert isinstance(
            new_obj.pac_code_peek, uuid.UUID)
        # pausedByUsername
        # pausedUTCDateTime
        # scheduledDFProcessRequestProcessorIdentifier
        assert new_obj is not None
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

    def test_last_change_code_concurrency(self, session):
        """
        Test case to verify the concurrency of
        last_change_code in the DFMaintenance
        model.

        This test case checks if the last_change_code
        of a DFMaintenance object is
        updated correctly
        when multiple changes are made concurrently.
        It creates a DFMaintenance object,
        retrieves it from the database, and updates its code
        attribute twice in separate transactions.
        Finally, it asserts that the last_change_code
        of the second retrieved DFMaintenance object
        is different from the original last_change_code.

        Args:
            session (Session): The SQLAlchemy session object.

        Returns:
            None
        """

        new_obj = DFMaintenanceFactory.create(
            session=session)
        original_last_change_code = \
            new_obj.last_change_code
        df_maintenance_1 = session.query(
            DFMaintenance).filter_by(
            _df_maintenance_id=(
                new_obj.df_maintenance_id)
        ).first()
        df_maintenance_1.code = uuid.uuid4()
        session.commit()
        df_maintenance_2 = session.query(
            DFMaintenance).filter_by(
            _df_maintenance_id=(
                new_obj.df_maintenance_id)
        ).first()
        df_maintenance_2.code = uuid.uuid4()
        session.commit()
        assert df_maintenance_2.last_change_code != \
            original_last_change_code
    # isPaused
    # isScheduledDFProcessRequestCompleted
    # isScheduledDFProcessRequestStarted
    # lastScheduledDFProcessRequestUTCDateTime
    # nextScheduledDFProcessRequestUTCDateTime
    # PacID

    def test_invalid_pac_id(self, session):
        """
        Test case to check if an invalid pac ID raises an IntegrityError.

        This test case creates a df_maintenance object using
        the DFMaintenanceFactory and assigns an invalid pac ID to it.
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
        new_obj = DFMaintenanceFactory.create(
            session=session)
        new_obj.pac_id = 99999
        with pytest.raises(IntegrityError):
            session.commit()
        session.rollback()
    # pausedByUsername
    # pausedUTCDateTime
    # scheduledDFProcessRequestProcessorIdentifier
