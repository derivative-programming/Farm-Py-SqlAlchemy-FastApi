# models/factory/tests/customer_test.py  # pylint: disable=duplicate-code
# pylint: disable=unused-import, too-many-public-methods
"""
This module contains unit tests for the CustomerFactory
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
from models import Base, Customer
from models.factory import CustomerFactory
from services.logging_config import get_logger

logger = get_logger(__name__)

TEST_DATABASE_URL = "sqlite:///:memory:"


class TestCustomerFactory:
    """
    This class contains unit tests for the CustomerFactory class.
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

    def test_customer_creation(self, session):
        """
        Test case for creating a customer.
        """
        new_obj = CustomerFactory.create(
            session=session)
        assert new_obj.customer_id is not None

    def test_code_default(self, session):
        """
        Test case for checking the default value of the code attribute.
        """
        new_obj = CustomerFactory.create(
            session=session)
        assert isinstance(new_obj.code, uuid.UUID)

    def test_last_change_code_default_on_build(self, session):
        """
        Test case for checking the default value of
        the last_change_code attribute on build.
        """
        new_obj: Customer = CustomerFactory.build(
            session=session)
        assert new_obj.last_change_code == 0

    def test_last_change_code_default_on_creation(self, session):
        """
        Test case for checking the default value of the
        last_change_code attribute on creation.
        """
        new_obj: Customer = CustomerFactory.create(
            session=session)
        assert new_obj.last_change_code == 1

    def test_last_change_code_default_on_update(self, session):
        """
        Test case for checking the default value of the
        last_change_code attribute on update.
        """
        new_obj = CustomerFactory.create(
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
        new_obj = CustomerFactory.build(
            session=session)
        assert new_obj.insert_utc_date_time is not None
        assert isinstance(
            new_obj.insert_utc_date_time, datetime)

    def test_date_inserted_on_initial_save(self, session):
        """
        Test case for checking the value of the
        insert_utc_date_time attribute on initial save.
        """
        new_obj = CustomerFactory.build(
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
        new_obj = CustomerFactory(
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
        new_obj = CustomerFactory.build(
            session=session)
        assert new_obj.last_update_utc_date_time is not None
        assert isinstance(
            new_obj.last_update_utc_date_time, datetime)

    def test_date_updated_on_initial_save(self, session):
        """
        Test case for checking the value of the
        last_update_utc_date_time attribute on initial save.
        """
        new_obj = CustomerFactory.build(
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
        new_obj = CustomerFactory(
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
        customer model.
        """
        new_obj = CustomerFactory.create(
            session=session)
        session.delete(new_obj)
        session.commit()
        deleted_customer = session.query(
            Customer).filter_by(
            _customer_id=(
                new_obj.customer_id)
        ).first()
        assert deleted_customer is None

    def test_data_types(self, session):
        """
        Test case for checking the data types of
        the customer attributes.
        """
        obj = CustomerFactory.create(
            session=session)
        assert isinstance(obj.customer_id, int)
        assert isinstance(obj.code, uuid.UUID)
        assert isinstance(obj.last_change_code, int)
        assert isinstance(obj.insert_user_id, uuid.UUID)
        assert isinstance(obj.last_update_user_id, uuid.UUID)
        assert isinstance(obj.active_organization_id, int)
        assert obj.email == "" or isinstance(
            obj.email, str)
        assert isinstance(obj.email_confirmed_utc_date_time,
                          datetime)
        assert obj.first_name == "" or isinstance(
            obj.first_name, str)
        assert isinstance(obj.forgot_password_key_expiration_utc_date_time,
                          datetime)
        assert obj.forgot_password_key_value == "" or isinstance(
            obj.forgot_password_key_value, str)
        # fSUserCodeValue
        assert isinstance(
            obj.fs_user_code_value, uuid.UUID)
        assert isinstance(obj.is_active, bool)
        assert isinstance(obj.is_email_allowed, bool)
        assert isinstance(obj.is_email_confirmed, bool)
        assert isinstance(obj.is_email_marketing_allowed, bool)
        assert isinstance(obj.is_locked, bool)
        assert isinstance(obj.is_multiple_organizations_allowed, bool)
        assert isinstance(obj.is_verbose_logging_forced, bool)
        assert isinstance(obj.last_login_utc_date_time,
                          datetime)
        assert obj.last_name == "" or isinstance(
            obj.last_name, str)
        assert obj.password == "" or isinstance(
            obj.password, str)
        assert obj.phone == "" or isinstance(
            obj.phone, str)
        assert obj.province == "" or isinstance(
            obj.province, str)
        assert isinstance(obj.registration_utc_date_time,
                          datetime)
        assert isinstance(obj.tac_id, int)
        assert isinstance(obj.utc_offset_in_minutes, int)
        assert obj.zip == "" or isinstance(
            obj.zip, str)
        # activeOrganizationID
        # email
        # emailConfirmedUTCDateTime
        # firstName
        # forgotPasswordKeyExpirationUTCDateTime
        # forgotPasswordKeyValue
        # fSUserCodeValue
        # isActive
        # isEmailAllowed
        # isEmailConfirmed
        # isEmailMarketingAllowed
        # isLocked
        # isMultipleOrganizationsAllowed
        # isVerboseLoggingForced
        # lastLoginUTCDateTime
        # lastName
        # password
        # phone
        # province
        # registrationUTCDateTime
        # tacID

        assert isinstance(
            obj.tac_code_peek, uuid.UUID)
        # uTCOffsetInMinutes
        # zip
        assert isinstance(obj.insert_utc_date_time, datetime)
        assert isinstance(obj.last_update_utc_date_time, datetime)

    def test_unique_code_constraint(self, session):
        """
        Test case for checking the unique code constraint.
        """
        customer_1 = CustomerFactory.create(
            session=session)
        customer_2 = CustomerFactory.create(
            session=session)
        customer_2.code = customer_1.code
        session.add_all([customer_1,
                         customer_2])
        with pytest.raises(Exception):
            session.commit()
        session.rollback()

    def test_fields_default(self):
        """
        Test case for checking the default values of
        the customer fields.
        """
        new_obj = Customer()
        assert new_obj.code is not None
        assert new_obj.last_change_code is not None
        assert new_obj.insert_user_id == uuid.UUID(int=0)
        assert new_obj.last_update_user_id == uuid.UUID(int=0)
        assert new_obj.insert_utc_date_time is not None
        assert new_obj.last_update_utc_date_time is not None
        # activeOrganizationID
        # email
        # emailConfirmedUTCDateTime
        # firstName
        # forgotPasswordKeyExpirationUTCDateTime
        # forgotPasswordKeyValue
        # fSUserCodeValue
        # isActive
        # isEmailAllowed
        # isEmailConfirmed
        # isEmailMarketingAllowed
        # isLocked
        # isMultipleOrganizationsAllowed
        # isVerboseLoggingForced
        # lastLoginUTCDateTime
        # lastName
        # password
        # phone
        # province
        # registrationUTCDateTime
        # TacID

        assert isinstance(
            new_obj.tac_code_peek, uuid.UUID)
        # uTCOffsetInMinutes
        # zip
        assert new_obj is not None
        assert new_obj.active_organization_id == 0
        assert new_obj.email == ""
        assert new_obj.email_confirmed_utc_date_time == datetime(1753, 1, 1, 0, 0, tzinfo=timezone.utc)
        assert new_obj.first_name == ""
        assert new_obj.forgot_password_key_expiration_utc_date_time == datetime(1753, 1, 1, 0, 0, tzinfo=timezone.utc)
        assert new_obj.forgot_password_key_value == ""
        # fs_user_code_value
        assert isinstance(
            new_obj.fs_user_code_value,
            uuid.UUID
        )
        assert new_obj.is_active is False
        assert new_obj.is_email_allowed is False
        assert new_obj.is_email_confirmed is False
        assert new_obj.is_email_marketing_allowed is False
        assert new_obj.is_locked is False
        assert new_obj.is_multiple_organizations_allowed is False
        assert new_obj.is_verbose_logging_forced is False
        assert new_obj.last_login_utc_date_time == datetime(1753, 1, 1, 0, 0, tzinfo=timezone.utc)
        assert new_obj.last_name == ""
        assert new_obj.password == ""
        assert new_obj.phone == ""
        assert new_obj.province == ""
        assert new_obj.registration_utc_date_time == datetime(1753, 1, 1, 0, 0, tzinfo=timezone.utc)
        assert new_obj.tac_id == 0
        assert new_obj.utc_offset_in_minutes == 0
        assert new_obj.zip == ""

    def test_last_change_code_concurrency(self, session):
        """
        Test case to verify the concurrency of
        last_change_code in the Customer
        model.

        This test case checks if the last_change_code
        of a Customer object is
        updated correctly
        when multiple changes are made concurrently.
        It creates a Customer object,
        retrieves it from the database, and updates its code
        attribute twice in separate transactions.
        Finally, it asserts that the last_change_code
        of the second retrieved Customer object
        is different from the original last_change_code.

        Args:
            session (Session): The SQLAlchemy session object.

        Returns:
            None
        """

        new_obj = CustomerFactory.create(
            session=session)
        original_last_change_code = \
            new_obj.last_change_code
        customer_1 = session.query(
            Customer).filter_by(
            _customer_id=(
                new_obj.customer_id)
        ).first()
        customer_1.code = uuid.uuid4()
        session.commit()
        customer_2 = session.query(
            Customer).filter_by(
            _customer_id=(
                new_obj.customer_id)
        ).first()
        customer_2.code = uuid.uuid4()
        session.commit()
        assert customer_2.last_change_code != \
            original_last_change_code
    # activeOrganizationID
    # email
    # emailConfirmedUTCDateTime
    # firstName
    # forgotPasswordKeyExpirationUTCDateTime
    # forgotPasswordKeyValue
    # fSUserCodeValue
    # isActive
    # isEmailAllowed
    # isEmailConfirmed
    # isEmailMarketingAllowed
    # isLocked
    # isMultipleOrganizationsAllowed
    # isVerboseLoggingForced
    # lastLoginUTCDateTime
    # lastName
    # password
    # phone
    # province
    # registrationUTCDateTime
    # TacID

    def test_invalid_tac_id(self, session):
        """
        Test case to check if an invalid tac ID raises an IntegrityError.

        This test case creates a customer object using
        the CustomerFactory and assigns an invalid tac ID to it.
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
        new_obj = CustomerFactory.create(
            session=session)
        new_obj.tac_id = 99999
        with pytest.raises(IntegrityError):
            session.commit()
        session.rollback()
    # uTCOffsetInMinutes
    # zip
