# models/factory/tests/dyna_flow_task_type_test.py
# pylint: disable=unused-import
"""
This module contains unit tests for the DynaFlowTaskTypeFactory
class in the models.factory package.
"""

from decimal import Decimal  # noqa: F401
import time
import math  # noqa: F401
import uuid  # noqa: F401
import logging
from datetime import datetime, date, timedelta, timezone  # noqa: F401
import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from models import Base, DynaFlowTaskType
from models.factory import DynaFlowTaskTypeFactory
from services.logging_config import get_logger
logger = get_logger(__name__)

DATABASE_URL = "sqlite:///:memory:"


class TestDynaFlowTaskTypeFactory:
    """
    This class contains unit tests for the DynaFlowTaskTypeFactory class.
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

    def test_dyna_flow_task_type_creation(self, session):
        """
        Test case for creating a dyna_flow_task_type.
        """
        new_obj = DynaFlowTaskTypeFactory.create(
            session=session)
        assert new_obj.dyna_flow_task_type_id is not None

    def test_code_default(self, session):
        """
        Test case for checking the default value of the code attribute.
        """
        new_obj = DynaFlowTaskTypeFactory.create(
            session=session)
        assert isinstance(new_obj.code, uuid.UUID)

    def test_last_change_code_default_on_build(self, session):
        """
        Test case for checking the default value of
        the last_change_code attribute on build.
        """
        new_obj: DynaFlowTaskType = DynaFlowTaskTypeFactory.build(
            session=session)
        assert new_obj.last_change_code == 0

    def test_last_change_code_default_on_creation(self, session):
        """
        Test case for checking the default value of the
        last_change_code attribute on creation.
        """
        new_obj: DynaFlowTaskType = DynaFlowTaskTypeFactory.create(
            session=session)
        assert new_obj.last_change_code == 1

    def test_last_change_code_default_on_update(self, session):
        """
        Test case for checking the default value of the
        last_change_code attribute on update.
        """
        new_obj = DynaFlowTaskTypeFactory.create(
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
        new_obj = DynaFlowTaskTypeFactory.build(
            session=session)
        assert new_obj.insert_utc_date_time is not None
        assert isinstance(
            new_obj.insert_utc_date_time, datetime)

    def test_date_inserted_on_initial_save(self, session):
        """
        Test case for checking the value of the
        insert_utc_date_time attribute on initial save.
        """
        new_obj = DynaFlowTaskTypeFactory.build(
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
        new_obj = DynaFlowTaskTypeFactory(
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
        new_obj = DynaFlowTaskTypeFactory.build(
            session=session)
        assert new_obj.last_update_utc_date_time is not None
        assert isinstance(
            new_obj.last_update_utc_date_time, datetime)

    def test_date_updated_on_initial_save(self, session):
        """
        Test case for checking the value of the
        last_update_utc_date_time attribute on initial save.
        """
        new_obj = DynaFlowTaskTypeFactory.build(
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
        new_obj = DynaFlowTaskTypeFactory(
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
        dyna_flow_task_type model.
        """
        new_obj = DynaFlowTaskTypeFactory.create(
            session=session)
        session.delete(new_obj)
        session.commit()
        deleted_dyna_flow_task_type = session.query(
            DynaFlowTaskType).filter_by(
            _dyna_flow_task_type_id=(
                new_obj.dyna_flow_task_type_id)
        ).first()
        assert deleted_dyna_flow_task_type is None

    def test_data_types(self, session):
        """
        Test case for checking the data types of
        the dyna_flow_task_type attributes.
        """
        obj = DynaFlowTaskTypeFactory.create(
            session=session)
        assert isinstance(obj.dyna_flow_task_type_id, int)
        assert isinstance(obj.code, uuid.UUID)
        assert isinstance(obj.last_change_code, int)
        assert isinstance(obj.insert_user_id, uuid.UUID)
        assert isinstance(obj.last_update_user_id, uuid.UUID)
        assert obj.description == "" or isinstance(
            obj.description, str)
        assert isinstance(obj.display_order, int)
        assert isinstance(obj.is_active, bool)
        assert obj.lookup_enum_name == "" or isinstance(
            obj.lookup_enum_name, str)
        assert isinstance(obj.max_retry_count, int)
        assert obj.name == "" or isinstance(
            obj.name, str)
        assert isinstance(obj.pac_id, int)
        # description,
        # displayOrder,
        # isActive,
        # lookupEnumName,
        # maxRetryCount,
        # name,
        # pacID

        assert isinstance(
            obj.pac_code_peek, uuid.UUID)
        assert isinstance(obj.insert_utc_date_time, datetime)
        assert isinstance(obj.last_update_utc_date_time, datetime)

    def test_unique_code_constraint(self, session):
        """
        Test case for checking the unique code constraint.
        """
        dyna_flow_task_type_1 = DynaFlowTaskTypeFactory.create(
            session=session)
        dyna_flow_task_type_2 = DynaFlowTaskTypeFactory.create(
            session=session)
        dyna_flow_task_type_2.code = dyna_flow_task_type_1.code
        session.add_all([dyna_flow_task_type_1,
                         dyna_flow_task_type_2])
        with pytest.raises(Exception):
            session.commit()
        session.rollback()

    def test_fields_default(self):
        """
        Test case for checking the default values of
        the dyna_flow_task_type fields.
        """
        new_obj = DynaFlowTaskType()
        assert new_obj.code is not None
        assert new_obj.last_change_code is not None
        assert new_obj.insert_user_id == uuid.UUID(int=0)
        assert new_obj.last_update_user_id == uuid.UUID(int=0)
        assert new_obj.insert_utc_date_time is not None
        assert new_obj.last_update_utc_date_time is not None
        # description,
        # displayOrder,
        # isActive,
        # lookupEnumName,
        # maxRetryCount,
        # name,
        # PacID

        assert isinstance(
            new_obj.pac_code_peek, uuid.UUID)
        assert new_obj is not None
        assert new_obj.description == ""
        assert new_obj.display_order == 0
        assert new_obj.is_active is False
        assert new_obj.lookup_enum_name == ""
        assert new_obj.max_retry_count == 0
        assert new_obj.name == ""
        assert new_obj.pac_id == 0

    def test_last_change_code_concurrency(self, session):
        """
        Test case to verify the concurrency of
        last_change_code in the DynaFlowTaskType
        model.

        This test case checks if the last_change_code
        of a DynaFlowTaskType object is
        updated correctly
        when multiple changes are made concurrently.
        It creates a DynaFlowTaskType object,
        retrieves it from the database, and updates its code
        attribute twice in separate transactions.
        Finally, it asserts that the last_change_code
        of the second retrieved DynaFlowTaskType object
        is different from the original last_change_code.

        Args:
            session (Session): The SQLAlchemy session object.

        Returns:
            None
        """

        new_obj = DynaFlowTaskTypeFactory.create(
            session=session)
        original_last_change_code = \
            new_obj.last_change_code
        dyna_flow_task_type_1 = session.query(
            DynaFlowTaskType).filter_by(
            _dyna_flow_task_type_id=(
                new_obj.dyna_flow_task_type_id)
        ).first()
        dyna_flow_task_type_1.code = uuid.uuid4()
        session.commit()
        dyna_flow_task_type_2 = session.query(
            DynaFlowTaskType).filter_by(
            _dyna_flow_task_type_id=(
                new_obj.dyna_flow_task_type_id)
        ).first()
        dyna_flow_task_type_2.code = uuid.uuid4()
        session.commit()
        assert dyna_flow_task_type_2.last_change_code != \
            original_last_change_code
    # description,
    # displayOrder,
    # isActive,
    # lookupEnumName,
    # maxRetryCount,
    # name,
    # PacID

    def test_invalid_pac_id(self, session):
        """
        Test case to check if an invalid pac ID raises an IntegrityError.

        This test case creates a dyna_flow_task_type object using
        the DynaFlowTaskTypeFactory and assigns an invalid pac ID to it.
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
        new_obj = DynaFlowTaskTypeFactory.create(
            session=session)
        new_obj.pac_id = 99999
        with pytest.raises(IntegrityError):
            session.commit()
        session.rollback()
