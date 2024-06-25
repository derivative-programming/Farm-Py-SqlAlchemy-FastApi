# models/factory/tests/tri_state_filter_test.py
"""
This module contains unit tests for the TriStateFilterFactory
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
from models import Base, TriStateFilter
from models.factory import TriStateFilterFactory
from services.logging_config import get_logger
logger = get_logger(__name__)

DATABASE_URL = "sqlite:///:memory:"


class TestTriStateFilterFactory:
    """
    This class contains unit tests for the TriStateFilterFactory class.
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

    def test_tri_state_filter_creation(self, session):
        """
        Test case for creating a tri_state_filter.
        """
        tri_state_filter = TriStateFilterFactory.create(
            session=session)
        assert tri_state_filter.tri_state_filter_id is not None

    def test_code_default(self, session):
        """
        Test case for checking the default value of the code attribute.
        """
        logging.info("vrtest")
        tri_state_filter = TriStateFilterFactory.create(
            session=session)
        assert isinstance(tri_state_filter.code, uuid.UUID)

    def test_last_change_code_default_on_build(self, session):
        """
        Test case for checking the default value of
        the last_change_code attribute on build.
        """
        tri_state_filter: TriStateFilter = TriStateFilterFactory.build(
            session=session)
        assert tri_state_filter.last_change_code == 0

    def test_last_change_code_default_on_creation(self, session):
        """
        Test case for checking the default value of the
        last_change_code attribute on creation.
        """
        tri_state_filter: TriStateFilter = TriStateFilterFactory.create(
            session=session)
        assert tri_state_filter.last_change_code == 1

    def test_last_change_code_default_on_update(self, session):
        """
        Test case for checking the default value of the
        last_change_code attribute on update.
        """
        tri_state_filter = TriStateFilterFactory.create(
            session=session)
        initial_code = tri_state_filter.last_change_code
        tri_state_filter.code = uuid.uuid4()
        session.commit()
        assert tri_state_filter.last_change_code != initial_code

    def test_date_inserted_on_build(self, session):
        """
        Test case for checking the value of the
        insert_utc_date_time attribute on build.
        """
        tri_state_filter = TriStateFilterFactory.build(
            session=session)
        assert tri_state_filter.insert_utc_date_time is not None
        assert isinstance(
            tri_state_filter.insert_utc_date_time, datetime)

    def test_date_inserted_on_initial_save(self, session):
        """
        Test case for checking the value of the
        insert_utc_date_time attribute on initial save.
        """
        tri_state_filter = TriStateFilterFactory.build(
            session=session)
        assert tri_state_filter.insert_utc_date_time is not None
        assert isinstance(
            tri_state_filter.insert_utc_date_time, datetime)
        initial_time = datetime.utcnow() + timedelta(days=-1)
        tri_state_filter.code = uuid.uuid4()
        session.add(tri_state_filter)
        session.commit()
        assert tri_state_filter.insert_utc_date_time > initial_time

    def test_date_inserted_on_second_save(self, session):
        """
        Test case for checking the value of the
        insert_utc_date_time attribute on second save.
        """
        tri_state_filter = TriStateFilterFactory(
            session=session)
        assert tri_state_filter.insert_utc_date_time is not None
        assert isinstance(
            tri_state_filter.insert_utc_date_time, datetime)
        initial_time = tri_state_filter.insert_utc_date_time
        tri_state_filter.code = uuid.uuid4()
        time.sleep(1)
        session.commit()
        assert tri_state_filter.insert_utc_date_time == initial_time

    def test_date_updated_on_build(self, session):
        """
        Test case for checking the value of the
        last_update_utc_date_time attribute on build.
        """
        tri_state_filter = TriStateFilterFactory.build(
            session=session)
        assert tri_state_filter.last_update_utc_date_time is not None
        assert isinstance(
            tri_state_filter.last_update_utc_date_time, datetime)

    def test_date_updated_on_initial_save(self, session):
        """
        Test case for checking the value of the
        last_update_utc_date_time attribute on initial save.
        """
        tri_state_filter = TriStateFilterFactory.build(
            session=session)
        assert tri_state_filter.last_update_utc_date_time is not None
        assert isinstance(
            tri_state_filter.last_update_utc_date_time, datetime)
        initial_time = datetime.utcnow() + timedelta(days=-1)
        tri_state_filter.code = uuid.uuid4()
        session.add(tri_state_filter)
        session.commit()
        assert tri_state_filter.last_update_utc_date_time > initial_time

    def test_date_updated_on_second_save(self, session):
        """
        Test case for checking the value of the
        last_update_utc_date_time attribute on second save.
        """
        tri_state_filter = TriStateFilterFactory(
            session=session)
        assert tri_state_filter.last_update_utc_date_time is not None
        assert isinstance(
            tri_state_filter.last_update_utc_date_time, datetime)
        initial_time = tri_state_filter.last_update_utc_date_time
        tri_state_filter.code = uuid.uuid4()
        time.sleep(1)
        session.commit()
        assert tri_state_filter.last_update_utc_date_time > initial_time

    def test_model_deletion(self, session):
        """
        Test case for deleting a
        tri_state_filter model.
        """
        tri_state_filter = TriStateFilterFactory.create(
            session=session)
        session.delete(tri_state_filter)
        session.commit()
        deleted_tri_state_filter = session.query(TriStateFilter).filter_by(
            tri_state_filter_id=tri_state_filter.tri_state_filter_id).first()
        assert deleted_tri_state_filter is None

    def test_data_types(self, session):
        """
        Test case for checking the data types of
        the tri_state_filter attributes.
        """
        tri_state_filter = TriStateFilterFactory.create(
            session=session)
        assert isinstance(tri_state_filter.tri_state_filter_id, int)
        assert isinstance(tri_state_filter.code, uuid.UUID)
        assert isinstance(tri_state_filter.last_change_code, int)
        assert isinstance(tri_state_filter.insert_user_id, uuid.UUID)
        assert isinstance(tri_state_filter.last_update_user_id, uuid.UUID)
        assert tri_state_filter.description == "" or isinstance(tri_state_filter.description, str)
        assert isinstance(tri_state_filter.display_order, int)
        assert isinstance(tri_state_filter.is_active, bool)
        assert tri_state_filter.lookup_enum_name == "" or isinstance(tri_state_filter.lookup_enum_name, str)
        assert tri_state_filter.name == "" or isinstance(tri_state_filter.name, str)
        assert isinstance(tri_state_filter.pac_id, int)
        assert isinstance(tri_state_filter.state_int_value, int)
        # Check for the peek values,
        # assuming they are UUIDs based on your model
        # description,
        # displayOrder,
        # isActive,
        # lookupEnumName,
        # name,
        # pacID

        assert isinstance(
            tri_state_filter.pac_code_peek, uuid.UUID)
        # stateIntValue,
        assert isinstance(tri_state_filter.insert_utc_date_time, datetime)
        assert isinstance(tri_state_filter.last_update_utc_date_time, datetime)

    def test_unique_code_constraint(self, session):
        """
        Test case for checking the unique code constraint.
        """
        tri_state_filter_1 = TriStateFilterFactory.create(session=session)
        tri_state_filter_2 = TriStateFilterFactory.create(session=session)
        tri_state_filter_2.code = tri_state_filter_1.code
        session.add_all([tri_state_filter_1, tri_state_filter_2])
        with pytest.raises(Exception):
            session.commit()
        session.rollback()

    def test_fields_default(self):
        """
        Test case for checking the default values of
        the tri_state_filter fields.
        """
        tri_state_filter = TriStateFilter()
        assert tri_state_filter.code is not None
        assert tri_state_filter.last_change_code is not None
        assert tri_state_filter.insert_user_id == uuid.UUID(int=0)
        assert tri_state_filter.last_update_user_id == uuid.UUID(int=0)
        assert tri_state_filter.insert_utc_date_time is not None
        assert tri_state_filter.last_update_utc_date_time is not None
        # description,
        # displayOrder,
        # isActive,
        # lookupEnumName,
        # name,
        # PacID

        assert isinstance(
            tri_state_filter.pac_code_peek, uuid.UUID)
        # stateIntValue,
        assert tri_state_filter is not None
        assert tri_state_filter.description == ""
        assert tri_state_filter.display_order == 0
        assert tri_state_filter.is_active is False
        assert tri_state_filter.lookup_enum_name == ""
        assert tri_state_filter.name == ""
        assert tri_state_filter.pac_id == 0
        assert tri_state_filter.state_int_value == 0

    def test_last_change_code_concurrency(self, session):
        """
        Test case to verify the concurrency of
        last_change_code in the TriStateFilter
        model.

        This test case checks if the last_change_code
        of a TriStateFilter object is
        updated correctly
        when multiple changes are made concurrently.
        It creates a TriStateFilter object,
        retrieves it from the database, and updates its code
        attribute twice in separate transactions.
        Finally, it asserts that the last_change_code
        of the second retrieved TriStateFilter object
        is different from the original last_change_code.

        Args:
            session (Session): The SQLAlchemy session object.

        Returns:
            None
        """

        tri_state_filter = TriStateFilterFactory.create(
            session=session)
        original_last_change_code = tri_state_filter.last_change_code
        tri_state_filter_1 = session.query(TriStateFilter).filter_by(
            _tri_state_filter_id=tri_state_filter.tri_state_filter_id).first()
        tri_state_filter_1.code = uuid.uuid4()
        session.commit()
        tri_state_filter_2 = session.query(TriStateFilter).filter_by(
            _tri_state_filter_id=tri_state_filter.tri_state_filter_id).first()
        tri_state_filter_2.code = uuid.uuid4()
        session.commit()
        assert tri_state_filter_2.last_change_code != original_last_change_code
    # description,
    # displayOrder,
    # isActive,
    # lookupEnumName,
    # name,
    # PacID

    def test_invalid_pac_id(self, session):
        """
        Test case to check if an invalid pac ID raises an IntegrityError.

        This test case creates a tri_state_filter object using
        the TriStateFilterFactory and assigns an invalid pac ID to it.
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
        tri_state_filter = TriStateFilterFactory.create(
            session=session)
        tri_state_filter.pac_id = 99999
        with pytest.raises(IntegrityError):
            session.commit()
        session.rollback()
    # stateIntValue,

