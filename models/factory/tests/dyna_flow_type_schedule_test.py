# models/factory/tests/dyna_flow_type_schedule_test.py  # pylint: disable=duplicate-code
# pylint: disable=unused-import, too-many-public-methods
"""
This module contains unit tests for the DynaFlowTypeScheduleFactory
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
from models import Base, DynaFlowTypeSchedule
from models.factory import DynaFlowTypeScheduleFactory
from services.logging_config import get_logger

logger = get_logger(__name__)

TEST_DATABASE_URL = "sqlite:///:memory:"


class TestDynaFlowTypeScheduleFactory:
    """
    This class contains unit tests for the DynaFlowTypeScheduleFactory class.
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

    def test_dyna_flow_type_schedule_creation(self, session):
        """
        Test case for creating a dyna_flow_type_schedule.
        """
        new_obj = DynaFlowTypeScheduleFactory.create(
            session=session)
        assert new_obj.dyna_flow_type_schedule_id is not None

    def test_code_default(self, session):
        """
        Test case for checking the default value of the code attribute.
        """
        new_obj = DynaFlowTypeScheduleFactory.create(
            session=session)
        assert isinstance(new_obj.code, uuid.UUID)

    def test_last_change_code_default_on_build(self, session):
        """
        Test case for checking the default value of
        the last_change_code attribute on build.
        """
        new_obj: DynaFlowTypeSchedule = DynaFlowTypeScheduleFactory.build(
            session=session)
        assert new_obj.last_change_code == 0

    def test_last_change_code_default_on_creation(self, session):
        """
        Test case for checking the default value of the
        last_change_code attribute on creation.
        """
        new_obj: DynaFlowTypeSchedule = DynaFlowTypeScheduleFactory.create(
            session=session)
        assert new_obj.last_change_code == 1

    def test_last_change_code_default_on_update(self, session):
        """
        Test case for checking the default value of the
        last_change_code attribute on update.
        """
        new_obj = DynaFlowTypeScheduleFactory.create(
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
        new_obj = DynaFlowTypeScheduleFactory.build(
            session=session)
        assert new_obj.insert_utc_date_time is not None
        assert isinstance(
            new_obj.insert_utc_date_time, datetime)

    def test_date_inserted_on_initial_save(self, session):
        """
        Test case for checking the value of the
        insert_utc_date_time attribute on initial save.
        """
        new_obj = DynaFlowTypeScheduleFactory.build(
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
        new_obj = DynaFlowTypeScheduleFactory(
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
        new_obj = DynaFlowTypeScheduleFactory.build(
            session=session)
        assert new_obj.last_update_utc_date_time is not None
        assert isinstance(
            new_obj.last_update_utc_date_time, datetime)

    def test_date_updated_on_initial_save(self, session):
        """
        Test case for checking the value of the
        last_update_utc_date_time attribute on initial save.
        """
        new_obj = DynaFlowTypeScheduleFactory.build(
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
        new_obj = DynaFlowTypeScheduleFactory(
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
        dyna_flow_type_schedule model.
        """
        new_obj = DynaFlowTypeScheduleFactory.create(
            session=session)
        session.delete(new_obj)
        session.commit()
        deleted_dyna_flow_type_schedule = session.query(
            DynaFlowTypeSchedule).filter_by(
            _dyna_flow_type_schedule_id=(
                new_obj.dyna_flow_type_schedule_id)
        ).first()
        assert deleted_dyna_flow_type_schedule is None

    def test_data_types(self, session):
        """
        Test case for checking the data types of
        the dyna_flow_type_schedule attributes.
        """
        obj = DynaFlowTypeScheduleFactory.create(
            session=session)
        assert isinstance(obj.dyna_flow_type_schedule_id, int)
        assert isinstance(obj.code, uuid.UUID)
        assert isinstance(obj.last_change_code, int)
        assert isinstance(obj.insert_user_id, uuid.UUID)
        assert isinstance(obj.last_update_user_id, uuid.UUID)
        assert isinstance(obj.dyna_flow_type_id, int)
        assert isinstance(obj.frequency_in_hours, int)
        assert isinstance(obj.is_active, bool)
        assert isinstance(obj.last_utc_date_time,
                          datetime)
        assert isinstance(obj.next_utc_date_time,
                          datetime)
        assert isinstance(obj.pac_id, int)
        # dynaFlowTypeID

        assert isinstance(
            obj.dyna_flow_type_code_peek, uuid.UUID)
        # frequencyInHours
        # isActive
        # lastUTCDateTime
        # nextUTCDateTime
        # pacID

        assert isinstance(
            obj.pac_code_peek, uuid.UUID)
        assert isinstance(obj.insert_utc_date_time, datetime)
        assert isinstance(obj.last_update_utc_date_time, datetime)

    def test_unique_code_constraint(self, session):
        """
        Test case for checking the unique code constraint.
        """
        dyna_flow_type_schedule_1 = DynaFlowTypeScheduleFactory.create(
            session=session)
        dyna_flow_type_schedule_2 = DynaFlowTypeScheduleFactory.create(
            session=session)
        dyna_flow_type_schedule_2.code = dyna_flow_type_schedule_1.code
        session.add_all([dyna_flow_type_schedule_1,
                         dyna_flow_type_schedule_2])
        with pytest.raises(Exception):
            session.commit()
        session.rollback()

    def test_fields_default(self):
        """
        Test case for checking the default values of
        the dyna_flow_type_schedule fields.
        """
        new_obj = DynaFlowTypeSchedule()
        assert new_obj.code is not None
        assert new_obj.last_change_code is not None
        assert new_obj.insert_user_id == uuid.UUID(int=0)
        assert new_obj.last_update_user_id == uuid.UUID(int=0)
        assert new_obj.insert_utc_date_time is not None
        assert new_obj.last_update_utc_date_time is not None
        # DynaFlowTypeID

        assert isinstance(
            new_obj.dyna_flow_type_code_peek, uuid.UUID)
        # frequencyInHours
        # isActive
        # lastUTCDateTime
        # nextUTCDateTime
        # PacID

        assert isinstance(
            new_obj.pac_code_peek, uuid.UUID)
        assert new_obj is not None
        assert new_obj.dyna_flow_type_id == 0
        assert new_obj.frequency_in_hours == 0
        assert new_obj.is_active is False
        assert new_obj.last_utc_date_time == datetime(1753, 1, 1, 0, 0, tzinfo=timezone.utc)
        assert new_obj.next_utc_date_time == datetime(1753, 1, 1, 0, 0, tzinfo=timezone.utc)
        assert new_obj.pac_id == 0

    def test_last_change_code_concurrency(self, session):
        """
        Test case to verify the concurrency of
        last_change_code in the DynaFlowTypeSchedule
        model.

        This test case checks if the last_change_code
        of a DynaFlowTypeSchedule object is
        updated correctly
        when multiple changes are made concurrently.
        It creates a DynaFlowTypeSchedule object,
        retrieves it from the database, and updates its code
        attribute twice in separate transactions.
        Finally, it asserts that the last_change_code
        of the second retrieved DynaFlowTypeSchedule object
        is different from the original last_change_code.

        Args:
            session (Session): The SQLAlchemy session object.

        Returns:
            None
        """

        new_obj = DynaFlowTypeScheduleFactory.create(
            session=session)
        original_last_change_code = \
            new_obj.last_change_code
        dyna_flow_type_schedule_1 = session.query(
            DynaFlowTypeSchedule).filter_by(
            _dyna_flow_type_schedule_id=(
                new_obj.dyna_flow_type_schedule_id)
        ).first()
        dyna_flow_type_schedule_1.code = uuid.uuid4()
        session.commit()
        dyna_flow_type_schedule_2 = session.query(
            DynaFlowTypeSchedule).filter_by(
            _dyna_flow_type_schedule_id=(
                new_obj.dyna_flow_type_schedule_id)
        ).first()
        dyna_flow_type_schedule_2.code = uuid.uuid4()
        session.commit()
        assert dyna_flow_type_schedule_2.last_change_code != \
            original_last_change_code
    # DynaFlowTypeID

    def test_invalid_dyna_flow_type_id(self, session):
        """
        Test case to check if an invalid dyna_flow_type ID raises an IntegrityError.

        This test case creates a dyna_flow_type_schedule object using
        the DynaFlowTypeScheduleFactory and assigns an invalid dyna_flow_type ID to it.
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
        new_obj = DynaFlowTypeScheduleFactory.create(
            session=session)
        new_obj.dyna_flow_type_id = 99999
        with pytest.raises(IntegrityError):
            session.commit()
        session.rollback()
    # frequencyInHours
    # isActive
    # lastUTCDateTime
    # nextUTCDateTime
    # PacID

    def test_invalid_pac_id(self, session):
        """
        Test case to check if an invalid pac ID raises an IntegrityError.

        This test case creates a dyna_flow_type_schedule object using
        the DynaFlowTypeScheduleFactory and assigns an invalid pac ID to it.
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
        new_obj = DynaFlowTypeScheduleFactory.create(
            session=session)
        new_obj.pac_id = 99999
        with pytest.raises(IntegrityError):
            session.commit()
        session.rollback()
