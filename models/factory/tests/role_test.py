# models/factory/tests/role_test.py
"""
This module contains unit tests for the RoleFactory
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
from models import Base, Role
from models.factory import RoleFactory
from services.logging_config import get_logger
logger = get_logger(__name__)

DATABASE_URL = "sqlite:///:memory:"


class TestRoleFactory:
    """
    This class contains unit tests for the RoleFactory class.
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

    def test_role_creation(self, session):
        """
        Test case for creating a role.
        """
        role = RoleFactory.create(
            session=session)
        assert role.role_id is not None

    def test_code_default(self, session):
        """
        Test case for checking the default value of the code attribute.
        """
        logging.info("vrtest")
        role = RoleFactory.create(
            session=session)
        assert isinstance(role.code, uuid.UUID)

    def test_last_change_code_default_on_build(self, session):
        """
        Test case for checking the default value of
        the last_change_code attribute on build.
        """
        role: Role = RoleFactory.build(
            session=session)
        assert role.last_change_code == 0

    def test_last_change_code_default_on_creation(self, session):
        """
        Test case for checking the default value of the
        last_change_code attribute on creation.
        """
        role: Role = RoleFactory.create(
            session=session)
        assert role.last_change_code == 1

    def test_last_change_code_default_on_update(self, session):
        """
        Test case for checking the default value of the
        last_change_code attribute on update.
        """
        role = RoleFactory.create(
            session=session)
        initial_code = role.last_change_code
        role.code = uuid.uuid4()
        session.commit()
        assert role.last_change_code != \
            initial_code

    def test_date_inserted_on_build(self, session):
        """
        Test case for checking the value of the
        insert_utc_date_time attribute on build.
        """
        role = RoleFactory.build(
            session=session)
        assert role.insert_utc_date_time is not None
        assert isinstance(
            role.insert_utc_date_time, datetime)

    def test_date_inserted_on_initial_save(self, session):
        """
        Test case for checking the value of the
        insert_utc_date_time attribute on initial save.
        """
        role = RoleFactory.build(
            session=session)
        assert role.insert_utc_date_time is not None
        assert isinstance(
            role.insert_utc_date_time, datetime)
        initial_time = datetime.utcnow() + timedelta(days=-1)
        role.code = uuid.uuid4()
        session.add(role)
        session.commit()
        assert role.insert_utc_date_time > initial_time

    def test_date_inserted_on_second_save(self, session):
        """
        Test case for checking the value of the
        insert_utc_date_time attribute on second save.
        """
        role = RoleFactory(
            session=session)
        assert role.insert_utc_date_time is not None
        assert isinstance(
            role.insert_utc_date_time, datetime)
        initial_time = role.insert_utc_date_time
        role.code = uuid.uuid4()
        time.sleep(1)
        session.commit()
        assert role.insert_utc_date_time == initial_time

    def test_date_updated_on_build(self, session):
        """
        Test case for checking the value of the
        last_update_utc_date_time attribute on build.
        """
        role = RoleFactory.build(
            session=session)
        assert role.last_update_utc_date_time is not None
        assert isinstance(
            role.last_update_utc_date_time, datetime)

    def test_date_updated_on_initial_save(self, session):
        """
        Test case for checking the value of the
        last_update_utc_date_time attribute on initial save.
        """
        role = RoleFactory.build(
            session=session)
        assert role.last_update_utc_date_time is not None
        assert isinstance(
            role.last_update_utc_date_time, datetime)
        initial_time = datetime.utcnow() + timedelta(days=-1)
        role.code = uuid.uuid4()
        session.add(role)
        session.commit()
        assert role.last_update_utc_date_time > initial_time

    def test_date_updated_on_second_save(self, session):
        """
        Test case for checking the value of the
        last_update_utc_date_time attribute on second save.
        """
        role = RoleFactory(
            session=session)
        assert role.last_update_utc_date_time is not None
        assert isinstance(
            role.last_update_utc_date_time, datetime)
        initial_time = role.last_update_utc_date_time
        role.code = uuid.uuid4()
        time.sleep(1)
        session.commit()
        assert role.last_update_utc_date_time > initial_time

    def test_model_deletion(self, session):
        """
        Test case for deleting a
        role model.
        """
        role = RoleFactory.create(
            session=session)
        session.delete(role)
        session.commit()
        deleted_role = session.query(Role).filter_by(
            _role_id=(
                role.role_id)
        ).first()
        assert deleted_role is None

    def test_data_types(self, session):
        """
        Test case for checking the data types of
        the role attributes.
        """
        role = RoleFactory.create(
            session=session)
        assert isinstance(role.role_id, int)
        assert isinstance(role.code, uuid.UUID)
        assert isinstance(role.last_change_code, int)
        assert isinstance(role.insert_user_id, uuid.UUID)
        assert isinstance(role.last_update_user_id, uuid.UUID)
        assert role.description == "" or isinstance(role.description, str)
        assert isinstance(role.display_order, int)
        assert isinstance(role.is_active, bool)
        assert role.lookup_enum_name == "" or isinstance(role.lookup_enum_name, str)
        assert role.name == "" or isinstance(role.name, str)
        assert isinstance(role.pac_id, int)
        # Check for the peek values,
        # assuming they are UUIDs based on your model
        # description,
        # displayOrder,
        # isActive,
        # lookupEnumName,
        # name,
        # pacID

        assert isinstance(
            role.pac_code_peek, uuid.UUID)
        assert isinstance(role.insert_utc_date_time, datetime)
        assert isinstance(role.last_update_utc_date_time, datetime)

    def test_unique_code_constraint(self, session):
        """
        Test case for checking the unique code constraint.
        """
        role_1 = RoleFactory.create(
            session=session)
        role_2 = RoleFactory.create(
            session=session)
        role_2.code = role_1.code
        session.add_all([role_1,
                         role_2])
        with pytest.raises(Exception):
            session.commit()
        session.rollback()

    def test_fields_default(self):
        """
        Test case for checking the default values of
        the role fields.
        """
        role = Role()
        assert role.code is not None
        assert role.last_change_code is not None
        assert role.insert_user_id == uuid.UUID(int=0)
        assert role.last_update_user_id == uuid.UUID(int=0)
        assert role.insert_utc_date_time is not None
        assert role.last_update_utc_date_time is not None
        # description,
        # displayOrder,
        # isActive,
        # lookupEnumName,
        # name,
        # PacID

        assert isinstance(
            role.pac_code_peek, uuid.UUID)
        assert role is not None
        assert role.description == ""
        assert role.display_order == 0
        assert role.is_active is False
        assert role.lookup_enum_name == ""
        assert role.name == ""
        assert role.pac_id == 0

    def test_last_change_code_concurrency(self, session):
        """
        Test case to verify the concurrency of
        last_change_code in the Role
        model.

        This test case checks if the last_change_code
        of a Role object is
        updated correctly
        when multiple changes are made concurrently.
        It creates a Role object,
        retrieves it from the database, and updates its code
        attribute twice in separate transactions.
        Finally, it asserts that the last_change_code
        of the second retrieved Role object
        is different from the original last_change_code.

        Args:
            session (Session): The SQLAlchemy session object.

        Returns:
            None
        """

        role = RoleFactory.create(
            session=session)
        original_last_change_code = role.last_change_code
        role_1 = session.query(Role).filter_by(
            _role_id=(
                role.role_id)
        ).first()
        role_1.code = uuid.uuid4()
        session.commit()
        role_2 = session.query(Role).filter_by(
            _role_id=(
                role.role_id)
        ).first()
        role_2.code = uuid.uuid4()
        session.commit()
        assert role_2.last_change_code != \
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

        This test case creates a role object using
        the RoleFactory and assigns an invalid pac ID to it.
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
        role = RoleFactory.create(
            session=session)
        role.pac_id = 99999
        with pytest.raises(IntegrityError):
            session.commit()
        session.rollback()

