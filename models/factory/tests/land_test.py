# models/factory/tests/land_test.py
"""
This module contains unit tests for the LandFactory
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
from models import Base, Land
from models.factory import LandFactory
from services.logging_config import get_logger
logger = get_logger(__name__)

DATABASE_URL = "sqlite:///:memory:"


class TestLandFactory:
    """
    This class contains unit tests for the LandFactory class.
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

    def test_land_creation(self, session):
        """
        Test case for creating a land.
        """
        land = LandFactory.create(
            session=session)
        assert land.land_id is not None

    def test_code_default(self, session):
        """
        Test case for checking the default value of the code attribute.
        """
        logging.info("vrtest")
        land = LandFactory.create(
            session=session)
        assert isinstance(land.code, uuid.UUID)

    def test_last_change_code_default_on_build(self, session):
        """
        Test case for checking the default value of
        the last_change_code attribute on build.
        """
        land: Land = LandFactory.build(
            session=session)
        assert land.last_change_code == 0

    def test_last_change_code_default_on_creation(self, session):
        """
        Test case for checking the default value of the
        last_change_code attribute on creation.
        """
        land: Land = LandFactory.create(
            session=session)
        assert land.last_change_code == 1

    def test_last_change_code_default_on_update(self, session):
        """
        Test case for checking the default value of the
        last_change_code attribute on update.
        """
        land = LandFactory.create(
            session=session)
        initial_code = land.last_change_code
        land.code = uuid.uuid4()
        session.commit()
        assert land.last_change_code != \
            initial_code

    def test_date_inserted_on_build(self, session):
        """
        Test case for checking the value of the
        insert_utc_date_time attribute on build.
        """
        land = LandFactory.build(
            session=session)
        assert land.insert_utc_date_time is not None
        assert isinstance(
            land.insert_utc_date_time, datetime)

    def test_date_inserted_on_initial_save(self, session):
        """
        Test case for checking the value of the
        insert_utc_date_time attribute on initial save.
        """
        land = LandFactory.build(
            session=session)
        assert land.insert_utc_date_time is not None
        assert isinstance(
            land.insert_utc_date_time, datetime)
        initial_time = datetime.utcnow() + timedelta(days=-1)
        land.code = uuid.uuid4()
        session.add(land)
        session.commit()
        assert land.insert_utc_date_time > initial_time

    def test_date_inserted_on_second_save(self, session):
        """
        Test case for checking the value of the
        insert_utc_date_time attribute on second save.
        """
        land = LandFactory(
            session=session)
        assert land.insert_utc_date_time is not None
        assert isinstance(
            land.insert_utc_date_time, datetime)
        initial_time = land.insert_utc_date_time
        land.code = uuid.uuid4()
        time.sleep(1)
        session.commit()
        assert land.insert_utc_date_time == initial_time

    def test_date_updated_on_build(self, session):
        """
        Test case for checking the value of the
        last_update_utc_date_time attribute on build.
        """
        land = LandFactory.build(
            session=session)
        assert land.last_update_utc_date_time is not None
        assert isinstance(
            land.last_update_utc_date_time, datetime)

    def test_date_updated_on_initial_save(self, session):
        """
        Test case for checking the value of the
        last_update_utc_date_time attribute on initial save.
        """
        land = LandFactory.build(
            session=session)
        assert land.last_update_utc_date_time is not None
        assert isinstance(
            land.last_update_utc_date_time, datetime)
        initial_time = datetime.utcnow() + timedelta(days=-1)
        land.code = uuid.uuid4()
        session.add(land)
        session.commit()
        assert land.last_update_utc_date_time > initial_time

    def test_date_updated_on_second_save(self, session):
        """
        Test case for checking the value of the
        last_update_utc_date_time attribute on second save.
        """
        land = LandFactory(
            session=session)
        assert land.last_update_utc_date_time is not None
        assert isinstance(
            land.last_update_utc_date_time, datetime)
        initial_time = land.last_update_utc_date_time
        land.code = uuid.uuid4()
        time.sleep(1)
        session.commit()
        assert land.last_update_utc_date_time > initial_time

    def test_model_deletion(self, session):
        """
        Test case for deleting a
        land model.
        """
        land = LandFactory.create(
            session=session)
        session.delete(land)
        session.commit()
        deleted_land = session.query(Land).filter_by(
            _land_id=(
                land.land_id)
        ).first()
        assert deleted_land is None

    def test_data_types(self, session):
        """
        Test case for checking the data types of
        the land attributes.
        """
        land = LandFactory.create(
            session=session)
        assert isinstance(land.land_id, int)
        assert isinstance(land.code, uuid.UUID)
        assert isinstance(land.last_change_code, int)
        assert isinstance(land.insert_user_id, uuid.UUID)
        assert isinstance(land.last_update_user_id, uuid.UUID)
        assert land.description == "" or isinstance(land.description, str)
        assert isinstance(land.display_order, int)
        assert isinstance(land.is_active, bool)
        assert land.lookup_enum_name == "" or isinstance(land.lookup_enum_name, str)
        assert land.name == "" or isinstance(land.name, str)
        assert isinstance(land.pac_id, int)
        # Check for the peek values,
        # assuming they are UUIDs based on your model
        # description,
        # displayOrder,
        # isActive,
        # lookupEnumName,
        # name,
        # pacID

        assert isinstance(
            land.pac_code_peek, uuid.UUID)
        assert isinstance(land.insert_utc_date_time, datetime)
        assert isinstance(land.last_update_utc_date_time, datetime)

    def test_unique_code_constraint(self, session):
        """
        Test case for checking the unique code constraint.
        """
        land_1 = LandFactory.create(
            session=session)
        land_2 = LandFactory.create(
            session=session)
        land_2.code = land_1.code
        session.add_all([land_1,
                         land_2])
        with pytest.raises(Exception):
            session.commit()
        session.rollback()

    def test_fields_default(self):
        """
        Test case for checking the default values of
        the land fields.
        """
        land = Land()
        assert land.code is not None
        assert land.last_change_code is not None
        assert land.insert_user_id == uuid.UUID(int=0)
        assert land.last_update_user_id == uuid.UUID(int=0)
        assert land.insert_utc_date_time is not None
        assert land.last_update_utc_date_time is not None
        # description,
        # displayOrder,
        # isActive,
        # lookupEnumName,
        # name,
        # PacID

        assert isinstance(
            land.pac_code_peek, uuid.UUID)
        assert land is not None
        assert land.description == ""
        assert land.display_order == 0
        assert land.is_active is False
        assert land.lookup_enum_name == ""
        assert land.name == ""
        assert land.pac_id == 0

    def test_last_change_code_concurrency(self, session):
        """
        Test case to verify the concurrency of
        last_change_code in the Land
        model.

        This test case checks if the last_change_code
        of a Land object is
        updated correctly
        when multiple changes are made concurrently.
        It creates a Land object,
        retrieves it from the database, and updates its code
        attribute twice in separate transactions.
        Finally, it asserts that the last_change_code
        of the second retrieved Land object
        is different from the original last_change_code.

        Args:
            session (Session): The SQLAlchemy session object.

        Returns:
            None
        """

        land = LandFactory.create(
            session=session)
        original_last_change_code = land.last_change_code
        land_1 = session.query(Land).filter_by(
            _land_id=(
                land.land_id)
        ).first()
        land_1.code = uuid.uuid4()
        session.commit()
        land_2 = session.query(Land).filter_by(
            _land_id=(
                land.land_id)
        ).first()
        land_2.code = uuid.uuid4()
        session.commit()
        assert land_2.last_change_code != \
            original_last_change_code
    # description,
    # displayOrder,
    # isActive,
    # lookupEnumName,
    # name,
    # PacID

    def test_invalid_pac_id(self, session):
        """
        Test case to check if an invalid pac ID raises an IntegrityError.

        This test case creates a land object using
        the LandFactory and assigns an invalid pac ID to it.
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
        land = LandFactory.create(
            session=session)
        land.pac_id = 99999
        with pytest.raises(IntegrityError):
            session.commit()
        session.rollback()

