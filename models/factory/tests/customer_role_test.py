# models/factory/tests/customer_role_test.py
# pylint: disable=unused-import
"""
This module contains unit tests for the CustomerRoleFactory
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
from models import Base, CustomerRole
from models.factory import CustomerRoleFactory
from services.logging_config import get_logger
logger = get_logger(__name__)

DATABASE_URL = "sqlite:///:memory:"


class TestCustomerRoleFactory:
    """
    This class contains unit tests for the CustomerRoleFactory class.
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

    def test_customer_role_creation(self, session):
        """
        Test case for creating a customer_role.
        """
        new_obj = CustomerRoleFactory.create(
            session=session)
        assert new_obj.customer_role_id is not None

    def test_code_default(self, session):
        """
        Test case for checking the default value of the code attribute.
        """
        logging.info("vrtest")
        new_obj = CustomerRoleFactory.create(
            session=session)
        assert isinstance(new_obj.code, uuid.UUID)

    def test_last_change_code_default_on_build(self, session):
        """
        Test case for checking the default value of
        the last_change_code attribute on build.
        """
        new_obj: CustomerRole = CustomerRoleFactory.build(
            session=session)
        assert new_obj.last_change_code == 0

    def test_last_change_code_default_on_creation(self, session):
        """
        Test case for checking the default value of the
        last_change_code attribute on creation.
        """
        new_obj: CustomerRole = CustomerRoleFactory.create(
            session=session)
        assert new_obj.last_change_code == 1

    def test_last_change_code_default_on_update(self, session):
        """
        Test case for checking the default value of the
        last_change_code attribute on update.
        """
        new_obj = CustomerRoleFactory.create(
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
        new_obj = CustomerRoleFactory.build(
            session=session)
        assert new_obj.insert_utc_date_time is not None
        assert isinstance(
            new_obj.insert_utc_date_time, datetime)

    def test_date_inserted_on_initial_save(self, session):
        """
        Test case for checking the value of the
        insert_utc_date_time attribute on initial save.
        """
        new_obj = CustomerRoleFactory.build(
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
        new_obj = CustomerRoleFactory(
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
        new_obj = CustomerRoleFactory.build(
            session=session)
        assert new_obj.last_update_utc_date_time is not None
        assert isinstance(
            new_obj.last_update_utc_date_time, datetime)

    def test_date_updated_on_initial_save(self, session):
        """
        Test case for checking the value of the
        last_update_utc_date_time attribute on initial save.
        """
        new_obj = CustomerRoleFactory.build(
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
        new_obj = CustomerRoleFactory(
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
        customer_role model.
        """
        new_obj = CustomerRoleFactory.create(
            session=session)
        session.delete(new_obj)
        session.commit()
        deleted_customer_role = session.query(
            CustomerRole).filter_by(
            _customer_role_id=(
                new_obj.customer_role_id)
        ).first()
        assert deleted_customer_role is None

    def test_data_types(self, session):
        """
        Test case for checking the data types of
        the customer_role attributes.
        """
        obj = CustomerRoleFactory.create(
            session=session)
        assert isinstance(obj.customer_role_id, int)
        assert isinstance(obj.code, uuid.UUID)
        assert isinstance(obj.last_change_code, int)
        assert isinstance(obj.insert_user_id, uuid.UUID)
        assert isinstance(obj.last_update_user_id, uuid.UUID)
        assert isinstance(obj.customer_id, int)
        assert isinstance(obj.is_placeholder, bool)
        assert isinstance(obj.placeholder, bool)
        assert isinstance(obj.role_id, int)
        # customerID

        assert isinstance(
            obj.customer_code_peek, uuid.UUID)
        # isPlaceholder,
        # placeholder,
        # roleID

        assert isinstance(
            obj.role_code_peek, uuid.UUID)
        assert isinstance(obj.insert_utc_date_time, datetime)
        assert isinstance(obj.last_update_utc_date_time, datetime)

    def test_unique_code_constraint(self, session):
        """
        Test case for checking the unique code constraint.
        """
        customer_role_1 = CustomerRoleFactory.create(
            session=session)
        customer_role_2 = CustomerRoleFactory.create(
            session=session)
        customer_role_2.code = customer_role_1.code
        session.add_all([customer_role_1,
                         customer_role_2])
        with pytest.raises(Exception):
            session.commit()
        session.rollback()

    def test_fields_default(self):
        """
        Test case for checking the default values of
        the customer_role fields.
        """
        new_obj = CustomerRole()
        assert new_obj.code is not None
        assert new_obj.last_change_code is not None
        assert new_obj.insert_user_id == uuid.UUID(int=0)
        assert new_obj.last_update_user_id == uuid.UUID(int=0)
        assert new_obj.insert_utc_date_time is not None
        assert new_obj.last_update_utc_date_time is not None
        # CustomerID

        assert isinstance(
            new_obj.customer_code_peek, uuid.UUID)
        # isPlaceholder,
        # placeholder,
        # RoleID

        assert isinstance(
            new_obj.role_code_peek, uuid.UUID)
        assert new_obj is not None
        assert new_obj.customer_id == 0
        assert new_obj.is_placeholder is False
        assert new_obj.placeholder is False
        assert new_obj.role_id == 0

    def test_last_change_code_concurrency(self, session):
        """
        Test case to verify the concurrency of
        last_change_code in the CustomerRole
        model.

        This test case checks if the last_change_code
        of a CustomerRole object is
        updated correctly
        when multiple changes are made concurrently.
        It creates a CustomerRole object,
        retrieves it from the database, and updates its code
        attribute twice in separate transactions.
        Finally, it asserts that the last_change_code
        of the second retrieved CustomerRole object
        is different from the original last_change_code.

        Args:
            session (Session): The SQLAlchemy session object.

        Returns:
            None
        """

        new_obj = CustomerRoleFactory.create(
            session=session)
        original_last_change_code = \
            new_obj.last_change_code
        customer_role_1 = session.query(
            CustomerRole).filter_by(
            _customer_role_id=(
                new_obj.customer_role_id)
        ).first()
        customer_role_1.code = uuid.uuid4()
        session.commit()
        customer_role_2 = session.query(
            CustomerRole).filter_by(
            _customer_role_id=(
                new_obj.customer_role_id)
        ).first()
        customer_role_2.code = uuid.uuid4()
        session.commit()
        assert customer_role_2.last_change_code != \
            original_last_change_code
    # CustomerID

    def test_invalid_customer_id(self, session):
        """
        Test case to check if an invalid customer ID raises an IntegrityError.

        This test case creates a customer_role object using
        the CustomerRoleFactory and assigns an invalid customer ID to it.
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
        new_obj = CustomerRoleFactory.create(
            session=session)
        new_obj.customer_id = 99999
        with pytest.raises(IntegrityError):
            session.commit()
        session.rollback()
    # isPlaceholder,
    # placeholder,
    # RoleID

    def test_invalid_role_id(self, session):
        """
        Test case to check if an invalid role ID raises an IntegrityError.

        This test case creates a customer_role object using
        the CustomerRoleFactory and assigns an invalid role ID to it.
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
        new_obj = CustomerRoleFactory.create(
            session=session)
        new_obj.role_id = 99999
        with pytest.raises(IntegrityError):
            session.commit()
        session.rollback()
