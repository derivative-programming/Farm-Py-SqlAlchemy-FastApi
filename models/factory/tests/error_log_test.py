# models/factory/tests/error_log_test.py
# pylint: disable=unused-import
"""
This module contains unit tests for the ErrorLogFactory
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
from models import Base, ErrorLog
from models.factory import ErrorLogFactory
from services.logging_config import get_logger
logger = get_logger(__name__)

DATABASE_URL = "sqlite:///:memory:"


class TestErrorLogFactory:
    """
    This class contains unit tests for the ErrorLogFactory class.
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

    def test_error_log_creation(self, session):
        """
        Test case for creating a error_log.
        """
        new_obj = ErrorLogFactory.create(
            session=session)
        assert new_obj.error_log_id is not None

    def test_code_default(self, session):
        """
        Test case for checking the default value of the code attribute.
        """
        new_obj = ErrorLogFactory.create(
            session=session)
        assert isinstance(new_obj.code, uuid.UUID)

    def test_last_change_code_default_on_build(self, session):
        """
        Test case for checking the default value of
        the last_change_code attribute on build.
        """
        new_obj: ErrorLog = ErrorLogFactory.build(
            session=session)
        assert new_obj.last_change_code == 0

    def test_last_change_code_default_on_creation(self, session):
        """
        Test case for checking the default value of the
        last_change_code attribute on creation.
        """
        new_obj: ErrorLog = ErrorLogFactory.create(
            session=session)
        assert new_obj.last_change_code == 1

    def test_last_change_code_default_on_update(self, session):
        """
        Test case for checking the default value of the
        last_change_code attribute on update.
        """
        new_obj = ErrorLogFactory.create(
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
        new_obj = ErrorLogFactory.build(
            session=session)
        assert new_obj.insert_utc_date_time is not None
        assert isinstance(
            new_obj.insert_utc_date_time, datetime)

    def test_date_inserted_on_initial_save(self, session):
        """
        Test case for checking the value of the
        insert_utc_date_time attribute on initial save.
        """
        new_obj = ErrorLogFactory.build(
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
        new_obj = ErrorLogFactory(
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
        new_obj = ErrorLogFactory.build(
            session=session)
        assert new_obj.last_update_utc_date_time is not None
        assert isinstance(
            new_obj.last_update_utc_date_time, datetime)

    def test_date_updated_on_initial_save(self, session):
        """
        Test case for checking the value of the
        last_update_utc_date_time attribute on initial save.
        """
        new_obj = ErrorLogFactory.build(
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
        new_obj = ErrorLogFactory(
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
        error_log model.
        """
        new_obj = ErrorLogFactory.create(
            session=session)
        session.delete(new_obj)
        session.commit()
        deleted_error_log = session.query(
            ErrorLog).filter_by(
            _error_log_id=(
                new_obj.error_log_id)
        ).first()
        assert deleted_error_log is None

    def test_data_types(self, session):
        """
        Test case for checking the data types of
        the error_log attributes.
        """
        obj = ErrorLogFactory.create(
            session=session)
        assert isinstance(obj.error_log_id, int)
        assert isinstance(obj.code, uuid.UUID)
        assert isinstance(obj.last_change_code, int)
        assert isinstance(obj.insert_user_id, uuid.UUID)
        assert isinstance(obj.last_update_user_id, uuid.UUID)
        # browserCode
        assert isinstance(
            obj.browser_code, uuid.UUID)
        # contextCode
        assert isinstance(
            obj.context_code, uuid.UUID)
        assert isinstance(obj.created_utc_date_time,
                          datetime)
        assert obj.description == "" or isinstance(
            obj.description, str)
        assert isinstance(obj.is_client_side_error, bool)
        assert isinstance(obj.is_resolved, bool)
        assert isinstance(obj.pac_id, int)
        assert obj.url == "" or isinstance(
            obj.url, str)
        # browserCode,
        # contextCode,
        # createdUTCDateTime
        # description,
        # isClientSideError,
        # isResolved,
        # pacID

        assert isinstance(
            obj.pac_code_peek, uuid.UUID)
        # url,
        assert isinstance(obj.insert_utc_date_time, datetime)
        assert isinstance(obj.last_update_utc_date_time, datetime)

    def test_unique_code_constraint(self, session):
        """
        Test case for checking the unique code constraint.
        """
        error_log_1 = ErrorLogFactory.create(
            session=session)
        error_log_2 = ErrorLogFactory.create(
            session=session)
        error_log_2.code = error_log_1.code
        session.add_all([error_log_1,
                         error_log_2])
        with pytest.raises(Exception):
            session.commit()
        session.rollback()

    def test_fields_default(self):
        """
        Test case for checking the default values of
        the error_log fields.
        """
        new_obj = ErrorLog()
        assert new_obj.code is not None
        assert new_obj.last_change_code is not None
        assert new_obj.insert_user_id == uuid.UUID(int=0)
        assert new_obj.last_update_user_id == uuid.UUID(int=0)
        assert new_obj.insert_utc_date_time is not None
        assert new_obj.last_update_utc_date_time is not None
        # browserCode,
        # contextCode,
        # createdUTCDateTime
        # description,
        # isClientSideError,
        # isResolved,
        # PacID

        assert isinstance(
            new_obj.pac_code_peek, uuid.UUID)
        # url,
        assert new_obj is not None
        # browser_code
        assert isinstance(
            new_obj.browser_code,
            uuid.UUID
        )
        # context_code
        assert isinstance(
            new_obj.context_code,
            uuid.UUID
        )
        assert new_obj.created_utc_date_time == datetime(1753, 1, 1, 0, 0, tzinfo=timezone.utc)
        assert new_obj.description == ""
        assert new_obj.is_client_side_error is False
        assert new_obj.is_resolved is False
        assert new_obj.pac_id == 0
        assert new_obj.url == ""

    def test_last_change_code_concurrency(self, session):
        """
        Test case to verify the concurrency of
        last_change_code in the ErrorLog
        model.

        This test case checks if the last_change_code
        of a ErrorLog object is
        updated correctly
        when multiple changes are made concurrently.
        It creates a ErrorLog object,
        retrieves it from the database, and updates its code
        attribute twice in separate transactions.
        Finally, it asserts that the last_change_code
        of the second retrieved ErrorLog object
        is different from the original last_change_code.

        Args:
            session (Session): The SQLAlchemy session object.

        Returns:
            None
        """

        new_obj = ErrorLogFactory.create(
            session=session)
        original_last_change_code = \
            new_obj.last_change_code
        error_log_1 = session.query(
            ErrorLog).filter_by(
            _error_log_id=(
                new_obj.error_log_id)
        ).first()
        error_log_1.code = uuid.uuid4()
        session.commit()
        error_log_2 = session.query(
            ErrorLog).filter_by(
            _error_log_id=(
                new_obj.error_log_id)
        ).first()
        error_log_2.code = uuid.uuid4()
        session.commit()
        assert error_log_2.last_change_code != \
            original_last_change_code
    # browserCode,
    # contextCode,
    # createdUTCDateTime
    # description,
    # isClientSideError,
    # isResolved,
    # PacID

    def test_invalid_pac_id(self, session):
        """
        Test case to check if an invalid pac ID raises an IntegrityError.

        This test case creates a error_log object using
        the ErrorLogFactory and assigns an invalid pac ID to it.
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
        new_obj = ErrorLogFactory.create(
            session=session)
        new_obj.pac_id = 99999
        with pytest.raises(IntegrityError):
            session.commit()
        session.rollback()
    # url,
