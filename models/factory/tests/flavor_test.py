# models/factory/tests/flavor_test.py
"""
This module contains unit tests for the FlavorFactory
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
from models import Base, Flavor
from models.factory import FlavorFactory
from services.logging_config import get_logger
logger = get_logger(__name__)

DATABASE_URL = "sqlite:///:memory:"


class TestFlavorFactory:
    """
    This class contains unit tests for the FlavorFactory class.
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

    def test_flavor_creation(self, session):
        """
        Test case for creating a flavor.
        """
        flavor = FlavorFactory.create(
            session=session)
        assert flavor.flavor_id is not None

    def test_code_default(self, session):
        """
        Test case for checking the default value of the code attribute.
        """
        logging.info("vrtest")
        flavor = FlavorFactory.create(
            session=session)
        assert isinstance(flavor.code, uuid.UUID)

    def test_last_change_code_default_on_build(self, session):
        """
        Test case for checking the default value of
        the last_change_code attribute on build.
        """
        flavor: Flavor = FlavorFactory.build(
            session=session)
        assert flavor.last_change_code == 0

    def test_last_change_code_default_on_creation(self, session):
        """
        Test case for checking the default value of the
        last_change_code attribute on creation.
        """
        flavor: Flavor = FlavorFactory.create(
            session=session)
        assert flavor.last_change_code == 1

    def test_last_change_code_default_on_update(self, session):
        """
        Test case for checking the default value of the
        last_change_code attribute on update.
        """
        flavor = FlavorFactory.create(
            session=session)
        initial_code = flavor.last_change_code
        flavor.code = uuid.uuid4()
        session.commit()
        assert flavor.last_change_code != initial_code

    def test_date_inserted_on_build(self, session):
        """
        Test case for checking the value of the
        insert_utc_date_time attribute on build.
        """
        flavor = FlavorFactory.build(
            session=session)
        assert flavor.insert_utc_date_time is not None
        assert isinstance(
            flavor.insert_utc_date_time, datetime)

    def test_date_inserted_on_initial_save(self, session):
        """
        Test case for checking the value of the
        insert_utc_date_time attribute on initial save.
        """
        flavor = FlavorFactory.build(
            session=session)
        assert flavor.insert_utc_date_time is not None
        assert isinstance(
            flavor.insert_utc_date_time, datetime)
        initial_time = datetime.utcnow() + timedelta(days=-1)
        flavor.code = uuid.uuid4()
        session.add(flavor)
        session.commit()
        assert flavor.insert_utc_date_time > initial_time

    def test_date_inserted_on_second_save(self, session):
        """
        Test case for checking the value of the
        insert_utc_date_time attribute on second save.
        """
        flavor = FlavorFactory(
            session=session)
        assert flavor.insert_utc_date_time is not None
        assert isinstance(
            flavor.insert_utc_date_time, datetime)
        initial_time = flavor.insert_utc_date_time
        flavor.code = uuid.uuid4()
        time.sleep(1)
        session.commit()
        assert flavor.insert_utc_date_time == initial_time

    def test_date_updated_on_build(self, session):
        """
        Test case for checking the value of the
        last_update_utc_date_time attribute on build.
        """
        flavor = FlavorFactory.build(
            session=session)
        assert flavor.last_update_utc_date_time is not None
        assert isinstance(
            flavor.last_update_utc_date_time, datetime)

    def test_date_updated_on_initial_save(self, session):
        """
        Test case for checking the value of the
        last_update_utc_date_time attribute on initial save.
        """
        flavor = FlavorFactory.build(
            session=session)
        assert flavor.last_update_utc_date_time is not None
        assert isinstance(
            flavor.last_update_utc_date_time, datetime)
        initial_time = datetime.utcnow() + timedelta(days=-1)
        flavor.code = uuid.uuid4()
        session.add(flavor)
        session.commit()
        assert flavor.last_update_utc_date_time > initial_time

    def test_date_updated_on_second_save(self, session):
        """
        Test case for checking the value of the
        last_update_utc_date_time attribute on second save.
        """
        flavor = FlavorFactory(
            session=session)
        assert flavor.last_update_utc_date_time is not None
        assert isinstance(
            flavor.last_update_utc_date_time, datetime)
        initial_time = flavor.last_update_utc_date_time
        flavor.code = uuid.uuid4()
        time.sleep(1)
        session.commit()
        assert flavor.last_update_utc_date_time > initial_time

    def test_model_deletion(self, session):
        """
        Test case for deleting a
        flavor model.
        """
        flavor = FlavorFactory.create(
            session=session)
        session.delete(flavor)
        session.commit()
        deleted_flavor = session.query(Flavor).filter_by(
            flavor_id=flavor.flavor_id).first()
        assert deleted_flavor is None

    def test_data_types(self, session):
        """
        Test case for checking the data types of
        the flavor attributes.
        """
        flavor = FlavorFactory.create(
            session=session)
        assert isinstance(flavor.flavor_id, int)
        assert isinstance(flavor.code, uuid.UUID)
        assert isinstance(flavor.last_change_code, int)
        assert isinstance(flavor.insert_user_id, uuid.UUID)
        assert isinstance(flavor.last_update_user_id, uuid.UUID)
        assert flavor.description == "" or isinstance(flavor.description, str)
        assert isinstance(flavor.display_order, int)
        assert isinstance(flavor.is_active, bool)
        assert flavor.lookup_enum_name == "" or isinstance(flavor.lookup_enum_name, str)
        assert flavor.name == "" or isinstance(flavor.name, str)
        assert isinstance(flavor.pac_id, int)
        # Check for the peek values,
        # assuming they are UUIDs based on your model
        # description,
        # displayOrder,
        # isActive,
        # lookupEnumName,
        # name,
        # pacID

        assert isinstance(
            flavor.pac_code_peek, uuid.UUID)
        assert isinstance(flavor.insert_utc_date_time, datetime)
        assert isinstance(flavor.last_update_utc_date_time, datetime)

    def test_unique_code_constraint(self, session):
        """
        Test case for checking the unique code constraint.
        """
        flavor_1 = FlavorFactory.create(session=session)
        flavor_2 = FlavorFactory.create(session=session)
        flavor_2.code = flavor_1.code
        session.add_all([flavor_1, flavor_2])
        with pytest.raises(Exception):
            session.commit()
        session.rollback()

    def test_fields_default(self):
        """
        Test case for checking the default values of
        the flavor fields.
        """
        flavor = Flavor()
        assert flavor.code is not None
        assert flavor.last_change_code is not None
        assert flavor.insert_user_id == uuid.UUID(int=0)
        assert flavor.last_update_user_id == uuid.UUID(int=0)
        assert flavor.insert_utc_date_time is not None
        assert flavor.last_update_utc_date_time is not None
        # description,
        # displayOrder,
        # isActive,
        # lookupEnumName,
        # name,
        # PacID

        assert isinstance(
            flavor.pac_code_peek, uuid.UUID)
        assert flavor is not None
        assert flavor.description == ""
        assert flavor.display_order == 0
        assert flavor.is_active is False
        assert flavor.lookup_enum_name == ""
        assert flavor.name == ""
        assert flavor.pac_id == 0

    def test_last_change_code_concurrency(self, session):
        """
        Test case to verify the concurrency of
        last_change_code in the Flavor
        model.

        This test case checks if the last_change_code
        of a Flavor object is
        updated correctly
        when multiple changes are made concurrently.
        It creates a Flavor object,
        retrieves it from the database, and updates its code
        attribute twice in separate transactions.
        Finally, it asserts that the last_change_code
        of the second retrieved Flavor object
        is different from the original last_change_code.

        Args:
            session (Session): The SQLAlchemy session object.

        Returns:
            None
        """

        flavor = FlavorFactory.create(
            session=session)
        original_last_change_code = flavor.last_change_code
        flavor_1 = session.query(Flavor).filter_by(
            _flavor_id=flavor.flavor_id).first()
        flavor_1.code = uuid.uuid4()
        session.commit()
        flavor_2 = session.query(Flavor).filter_by(
            _flavor_id=flavor.flavor_id).first()
        flavor_2.code = uuid.uuid4()
        session.commit()
        assert flavor_2.last_change_code != original_last_change_code
    # description,
    # displayOrder,
    # isActive,
    # lookupEnumName,
    # name,
    # PacID

    def test_invalid_pac_id(self, session):
        """
        Test case to check if an invalid pac ID raises an IntegrityError.

        This test case creates a flavor object using
        the FlavorFactory and assigns an invalid pac ID to it.
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
        flavor = FlavorFactory.create(
            session=session)
        flavor.pac_id = 99999
        with pytest.raises(IntegrityError):
            session.commit()
        session.rollback()

