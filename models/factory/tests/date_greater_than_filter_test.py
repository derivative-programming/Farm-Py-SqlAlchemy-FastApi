# models/factory/tests/date_greater_than_filter_test.py
"""
This module contains unit tests for the DateGreaterThanFilterFactory
class in the models.factory package.
"""

from decimal import Decimal
import time
import math
import uuid
import logging
from datetime import datetime, date, timedelta
import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from models import Base, DateGreaterThanFilter
from models.factory import DateGreaterThanFilterFactory
from services.logging_config import get_logger
logger = get_logger(__name__)

DATABASE_URL = "sqlite:///:memory:"


class TestDateGreaterThanFilterFactory:
    """
    This class contains unit tests for the DateGreaterThanFilterFactory class.
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

    def test_date_greater_than_filter_creation(self, session):
        """
        Test case for creating a date_greater_than_filter.
        """
        date_greater_than_filter = DateGreaterThanFilterFactory.create(
            session=session)
        assert date_greater_than_filter.date_greater_than_filter_id is not None

    def test_code_default(self, session):
        """
        Test case for checking the default value of the code attribute.
        """
        logging.info("vrtest")
        date_greater_than_filter = DateGreaterThanFilterFactory.create(
            session=session)
        assert isinstance(date_greater_than_filter.code, uuid.UUID)

    def test_last_change_code_default_on_build(self, session):
        """
        Test case for checking the default value of
        the last_change_code attribute on build.
        """
        date_greater_than_filter: DateGreaterThanFilter = DateGreaterThanFilterFactory.build(
            session=session)
        assert date_greater_than_filter.last_change_code == 0

    def test_last_change_code_default_on_creation(self, session):
        """
        Test case for checking the default value of the
        last_change_code attribute on creation.
        """
        date_greater_than_filter: DateGreaterThanFilter = DateGreaterThanFilterFactory.create(
            session=session)
        assert date_greater_than_filter.last_change_code == 1

    def test_last_change_code_default_on_update(self, session):
        """
        Test case for checking the default value of the
        last_change_code attribute on update.
        """
        date_greater_than_filter = DateGreaterThanFilterFactory.create(
            session=session)
        initial_code = date_greater_than_filter.last_change_code
        date_greater_than_filter.code = uuid.uuid4()
        session.commit()
        assert date_greater_than_filter.last_change_code != \
            initial_code

    def test_date_inserted_on_build(self, session):
        """
        Test case for checking the value of the
        insert_utc_date_time attribute on build.
        """
        date_greater_than_filter = DateGreaterThanFilterFactory.build(
            session=session)
        assert date_greater_than_filter.insert_utc_date_time is not None
        assert isinstance(
            date_greater_than_filter.insert_utc_date_time, datetime)

    def test_date_inserted_on_initial_save(self, session):
        """
        Test case for checking the value of the
        insert_utc_date_time attribute on initial save.
        """
        date_greater_than_filter = DateGreaterThanFilterFactory.build(
            session=session)
        assert date_greater_than_filter.insert_utc_date_time is not None
        assert isinstance(
            date_greater_than_filter.insert_utc_date_time, datetime)
        initial_time = datetime.utcnow() + timedelta(days=-1)
        date_greater_than_filter.code = uuid.uuid4()
        session.add(date_greater_than_filter)
        session.commit()
        assert date_greater_than_filter.insert_utc_date_time > initial_time

    def test_date_inserted_on_second_save(self, session):
        """
        Test case for checking the value of the
        insert_utc_date_time attribute on second save.
        """
        date_greater_than_filter = DateGreaterThanFilterFactory(
            session=session)
        assert date_greater_than_filter.insert_utc_date_time is not None
        assert isinstance(
            date_greater_than_filter.insert_utc_date_time, datetime)
        initial_time = date_greater_than_filter.insert_utc_date_time
        date_greater_than_filter.code = uuid.uuid4()
        time.sleep(1)
        session.commit()
        assert date_greater_than_filter.insert_utc_date_time == initial_time

    def test_date_updated_on_build(self, session):
        """
        Test case for checking the value of the
        last_update_utc_date_time attribute on build.
        """
        date_greater_than_filter = DateGreaterThanFilterFactory.build(
            session=session)
        assert date_greater_than_filter.last_update_utc_date_time is not None
        assert isinstance(
            date_greater_than_filter.last_update_utc_date_time, datetime)

    def test_date_updated_on_initial_save(self, session):
        """
        Test case for checking the value of the
        last_update_utc_date_time attribute on initial save.
        """
        date_greater_than_filter = DateGreaterThanFilterFactory.build(
            session=session)
        assert date_greater_than_filter.last_update_utc_date_time is not None
        assert isinstance(
            date_greater_than_filter.last_update_utc_date_time, datetime)
        initial_time = datetime.utcnow() + timedelta(days=-1)
        date_greater_than_filter.code = uuid.uuid4()
        session.add(date_greater_than_filter)
        session.commit()
        assert date_greater_than_filter.last_update_utc_date_time > initial_time

    def test_date_updated_on_second_save(self, session):
        """
        Test case for checking the value of the
        last_update_utc_date_time attribute on second save.
        """
        date_greater_than_filter = DateGreaterThanFilterFactory(
            session=session)
        assert date_greater_than_filter.last_update_utc_date_time is not None
        assert isinstance(
            date_greater_than_filter.last_update_utc_date_time, datetime)
        initial_time = date_greater_than_filter.last_update_utc_date_time
        date_greater_than_filter.code = uuid.uuid4()
        time.sleep(1)
        session.commit()
        assert date_greater_than_filter.last_update_utc_date_time > initial_time

    def test_model_deletion(self, session):
        """
        Test case for deleting a
        date_greater_than_filter model.
        """
        date_greater_than_filter = DateGreaterThanFilterFactory.create(
            session=session)
        session.delete(date_greater_than_filter)
        session.commit()
        deleted_date_greater_than_filter = session.query(DateGreaterThanFilter).filter_by(
            _date_greater_than_filter_id=(
                date_greater_than_filter.date_greater_than_filter_id)
        ).first()
        assert deleted_date_greater_than_filter is None

    def test_data_types(self, session):
        """
        Test case for checking the data types of
        the date_greater_than_filter attributes.
        """
        date_greater_than_filter = DateGreaterThanFilterFactory.create(
            session=session)
        assert isinstance(date_greater_than_filter.date_greater_than_filter_id, int)
        assert isinstance(date_greater_than_filter.code, uuid.UUID)
        assert isinstance(date_greater_than_filter.last_change_code, int)
        assert isinstance(date_greater_than_filter.insert_user_id, uuid.UUID)
        assert isinstance(date_greater_than_filter.last_update_user_id, uuid.UUID)
        assert isinstance(date_greater_than_filter.day_count, int)
        assert date_greater_than_filter.description == "" or isinstance(date_greater_than_filter.description, str)
        assert isinstance(date_greater_than_filter.display_order, int)
        assert isinstance(date_greater_than_filter.is_active, bool)
        assert date_greater_than_filter.lookup_enum_name == "" or isinstance(date_greater_than_filter.lookup_enum_name, str)
        assert date_greater_than_filter.name == "" or isinstance(date_greater_than_filter.name, str)
        assert isinstance(date_greater_than_filter.pac_id, int)
        # Check for the peek values,
        # assuming they are UUIDs based on your model
        # dayCount,
        # description,
        # displayOrder,
        # isActive,
        # lookupEnumName,
        # name,
        # pacID

        assert isinstance(
            date_greater_than_filter.pac_code_peek, uuid.UUID)
        assert isinstance(date_greater_than_filter.insert_utc_date_time, datetime)
        assert isinstance(date_greater_than_filter.last_update_utc_date_time, datetime)

    def test_unique_code_constraint(self, session):
        """
        Test case for checking the unique code constraint.
        """
        date_greater_than_filter_1 = DateGreaterThanFilterFactory.create(
            session=session)
        date_greater_than_filter_2 = DateGreaterThanFilterFactory.create(
            session=session)
        date_greater_than_filter_2.code = date_greater_than_filter_1.code
        session.add_all([date_greater_than_filter_1,
                         date_greater_than_filter_2])
        with pytest.raises(Exception):
            session.commit()
        session.rollback()

    def test_fields_default(self):
        """
        Test case for checking the default values of
        the date_greater_than_filter fields.
        """
        date_greater_than_filter = DateGreaterThanFilter()
        assert date_greater_than_filter.code is not None
        assert date_greater_than_filter.last_change_code is not None
        assert date_greater_than_filter.insert_user_id == uuid.UUID(int=0)
        assert date_greater_than_filter.last_update_user_id == uuid.UUID(int=0)
        assert date_greater_than_filter.insert_utc_date_time is not None
        assert date_greater_than_filter.last_update_utc_date_time is not None
        # dayCount,
        # description,
        # displayOrder,
        # isActive,
        # lookupEnumName,
        # name,
        # PacID

        assert isinstance(
            date_greater_than_filter.pac_code_peek, uuid.UUID)
        assert date_greater_than_filter is not None
        assert date_greater_than_filter.day_count == 0
        assert date_greater_than_filter.description == ""
        assert date_greater_than_filter.display_order == 0
        assert date_greater_than_filter.is_active is False
        assert date_greater_than_filter.lookup_enum_name == ""
        assert date_greater_than_filter.name == ""
        assert date_greater_than_filter.pac_id == 0

    def test_last_change_code_concurrency(self, session):
        """
        Test case to verify the concurrency of
        last_change_code in the DateGreaterThanFilter
        model.

        This test case checks if the last_change_code
        of a DateGreaterThanFilter object is
        updated correctly
        when multiple changes are made concurrently.
        It creates a DateGreaterThanFilter object,
        retrieves it from the database, and updates its code
        attribute twice in separate transactions.
        Finally, it asserts that the last_change_code
        of the second retrieved DateGreaterThanFilter object
        is different from the original last_change_code.

        Args:
            session (Session): The SQLAlchemy session object.

        Returns:
            None
        """

        date_greater_than_filter = DateGreaterThanFilterFactory.create(
            session=session)
        original_last_change_code = date_greater_than_filter.last_change_code
        date_greater_than_filter_1 = session.query(DateGreaterThanFilter).filter_by(
            _date_greater_than_filter_id=(
                date_greater_than_filter.date_greater_than_filter_id)
        ).first()
        date_greater_than_filter_1.code = uuid.uuid4()
        session.commit()
        date_greater_than_filter_2 = session.query(DateGreaterThanFilter).filter_by(
            _date_greater_than_filter_id=(
                date_greater_than_filter.date_greater_than_filter_id)
        ).first()
        date_greater_than_filter_2.code = uuid.uuid4()
        session.commit()
        assert date_greater_than_filter_2.last_change_code != \
            original_last_change_code
    # dayCount,
    # description,
    # displayOrder,
    # isActive,
    # lookupEnumName,
    # name,
    # PacID

    def test_invalid_pac_id(self, session):
        """
        Test case to check if an invalid pac ID raises an IntegrityError.

        This test case creates a date_greater_than_filter object using
        the DateGreaterThanFilterFactory and assigns an invalid pac ID to it.
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
        date_greater_than_filter = DateGreaterThanFilterFactory.create(
            session=session)
        date_greater_than_filter.pac_id = 99999
        with pytest.raises(IntegrityError):
            session.commit()
        session.rollback()

