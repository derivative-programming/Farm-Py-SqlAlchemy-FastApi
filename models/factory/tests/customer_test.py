# models/factory/tests/customer_test.py
"""
    #TODO add comment
"""
from decimal import Decimal
import time
import math
import uuid
import logging
from datetime import datetime, date, timedelta
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from models import Base, Customer
from models.factory import CustomerFactory
from services.logging_config import get_logger
logger = get_logger(__name__)
DATABASE_URL = "sqlite:///:memory:"
class TestCustomerFactory:
    """
    #TODO add comment
    """
    @pytest.fixture(scope="module")
    def engine(self):
        """
        #TODO add comment
        """
        engine = create_engine(DATABASE_URL, echo=False)
        #FKs are not activated by default in sqllite
        with engine.connect() as conn:
            conn.connection.execute("PRAGMA foreign_keys=ON")
        yield engine
        engine.dispose()
    @pytest.fixture
    def session(self, engine):
        """
        #TODO add comment
        """
        Base.metadata.create_all(engine)
        SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)
        session_instance = SessionLocal()
        yield session_instance
        session_instance.close()
    def test_customer_creation(self, session):
        """
        #TODO add comment
        """
        customer = CustomerFactory.create(session=session)
        assert customer.customer_id is not None
    def test_code_default(self, session):
        """
        #TODO add comment
        """
        logging.info("vrtest")
        customer = CustomerFactory.create(session=session)
        assert isinstance(customer.code, uuid.UUID)
    def test_last_change_code_default_on_build(self, session):
        """
        #TODO add comment
        """
        customer: Customer = CustomerFactory.build(session=session)
        assert customer.last_change_code == 0
    def test_last_change_code_default_on_creation(self, session):
        """
        #TODO add comment
        """
        customer: Customer = CustomerFactory.create(session=session)
        assert customer.last_change_code == 1
    def test_last_change_code_default_on_update(self, session):
        """
        #TODO add comment
        """
        customer = CustomerFactory.create(session=session)
        initial_code = customer.last_change_code
        customer.code = uuid.uuid4()
        session.commit()
        assert customer.last_change_code != initial_code
    def test_date_inserted_on_build(self, session):
        """
        #TODO add comment
        """
        customer = CustomerFactory.build(session=session)
        assert customer.insert_utc_date_time is not None
        assert isinstance(customer.insert_utc_date_time, datetime)
    def test_date_inserted_on_initial_save(self, session):
        """
        #TODO add comment
        """
        customer = CustomerFactory.build(session=session)
        assert customer.insert_utc_date_time is not None
        assert isinstance(customer.insert_utc_date_time, datetime)
        initial_time = datetime.utcnow() + timedelta(days=-1)
        customer.code = uuid.uuid4()
        session.add(customer)
        session.commit()
        assert customer.insert_utc_date_time > initial_time
    def test_date_inserted_on_second_save(self, session):
        """
        #TODO add comment
        """
        customer = CustomerFactory(session=session)
        assert customer.insert_utc_date_time is not None
        assert isinstance(customer.insert_utc_date_time, datetime)
        initial_time = customer.insert_utc_date_time
        customer.code = uuid.uuid4()
        time.sleep(1)
        session.commit()
        assert customer.insert_utc_date_time == initial_time
    def test_date_updated_on_build(self, session):
        """
        #TODO add comment
        """
        customer = CustomerFactory.build(session=session)
        assert customer.last_update_utc_date_time is not None
        assert isinstance(customer.last_update_utc_date_time, datetime)
    def test_date_updated_on_initial_save(self, session):
        """
        #TODO add comment
        """
        customer = CustomerFactory.build(session=session)
        assert customer.last_update_utc_date_time is not None
        assert isinstance(customer.last_update_utc_date_time, datetime)
        initial_time = datetime.utcnow() + timedelta(days=-1)
        customer.code = uuid.uuid4()
        session.add(customer)
        session.commit()
        assert customer.last_update_utc_date_time > initial_time
    def test_date_updated_on_second_save(self, session):
        """
        #TODO add comment
        """
        customer = CustomerFactory(session=session)
        assert customer.last_update_utc_date_time is not None
        assert isinstance(customer.last_update_utc_date_time, datetime)
        initial_time = customer.last_update_utc_date_time
        customer.code = uuid.uuid4()
        time.sleep(1)
        session.commit()
        assert customer.last_update_utc_date_time > initial_time
    def test_model_deletion(self, session):
        """
        #TODO add comment
        """
        customer = CustomerFactory.create(session=session)
        session.delete(customer)
        session.commit()
        deleted_customer = session.query(Customer).filter_by(
            customer_id=customer.customer_id).first()
        assert deleted_customer is None
    def test_data_types(self, session):
        """
        #TODO add comment
        """
        customer = CustomerFactory.create(session=session)
        assert isinstance(customer.customer_id, int)
        assert isinstance(customer.code, uuid.UUID)
        assert isinstance(customer.last_change_code, int)
        assert isinstance(customer.insert_user_id, uuid.UUID)
        assert isinstance(customer.last_update_user_id, uuid.UUID)
        assert isinstance(customer.active_organization_id, int)
        assert customer.email == "" or isinstance(
            customer.email, str)
        assert isinstance(customer.email_confirmed_utc_date_time, datetime)
        assert customer.first_name == "" or isinstance(customer.first_name, str)
        assert isinstance(customer.forgot_password_key_expiration_utc_date_time, datetime)
        assert customer.forgot_password_key_value == "" or isinstance(customer.forgot_password_key_value, str)
        # fSUserCodeValue
        assert isinstance(
            customer.fs_user_code_value, uuid.UUID)
        assert isinstance(customer.is_active, bool)
        assert isinstance(customer.is_email_allowed, bool)
        assert isinstance(customer.is_email_confirmed, bool)
        assert isinstance(customer.is_email_marketing_allowed, bool)
        assert isinstance(customer.is_locked, bool)
        assert isinstance(customer.is_multiple_organizations_allowed, bool)
        assert isinstance(customer.is_verbose_logging_forced, bool)
        assert isinstance(customer.last_login_utc_date_time, datetime)
        assert customer.last_name == "" or isinstance(customer.last_name, str)
        assert customer.password == "" or isinstance(customer.password, str)
        assert customer.phone == "" or isinstance(
            customer.phone, str)
        assert customer.province == "" or isinstance(customer.province, str)
        assert isinstance(customer.registration_utc_date_time, datetime)
        assert isinstance(customer.tac_id, int)
        assert isinstance(customer.utc_offset_in_minutes, int)
        assert customer.zip == "" or isinstance(customer.zip, str)
        # Check for the peek values,
        # assuming they are UUIDs based on your model
# endset
        # activeOrganizationID,
        # email,
        # emailConfirmedUTCDateTime
        # firstName,
        # forgotPasswordKeyExpirationUTCDateTime
        # forgotPasswordKeyValue,
        # fSUserCodeValue,
        # isActive,
        # isEmailAllowed,
        # isEmailConfirmed,
        # isEmailMarketingAllowed,
        # isLocked,
        # isMultipleOrganizationsAllowed,
        # isVerboseLoggingForced,
        # lastLoginUTCDateTime
        # lastName,
        # password,
        # phone,
        # province,
        # registrationUTCDateTime
        # tacID
        assert isinstance(
            customer.tac_code_peek, uuid.UUID)
        # uTCOffsetInMinutes,
        # zip,
# endset
        assert isinstance(customer.insert_utc_date_time, datetime)
        assert isinstance(customer.last_update_utc_date_time, datetime)
    def test_unique_code_constraint(self, session):
        """
        #TODO add comment
        """
        customer_1 = CustomerFactory.create(session=session)
        customer_2 = CustomerFactory.create(session=session)
        customer_2.code = customer_1.code
        session.add_all([customer_1, customer_2])
        with pytest.raises(Exception):
            session.commit()
        session.rollback()
    def test_fields_default(self):
        """
        #TODO add comment
        """
        customer = Customer()
        assert customer.code is not None
        assert customer.last_change_code is not None
        assert customer.insert_user_id == uuid.UUID(int=0)
        assert customer.last_update_user_id == uuid.UUID(int=0)
        assert customer.insert_utc_date_time is not None
        assert customer.last_update_utc_date_time is not None
# endset
        # activeOrganizationID,
        # email,
        # emailConfirmedUTCDateTime
        # firstName,
        # forgotPasswordKeyExpirationUTCDateTime
        # forgotPasswordKeyValue,
        # fSUserCodeValue,
        # isActive,
        # isEmailAllowed,
        # isEmailConfirmed,
        # isEmailMarketingAllowed,
        # isLocked,
        # isMultipleOrganizationsAllowed,
        # isVerboseLoggingForced,
        # lastLoginUTCDateTime
        # lastName,
        # password,
        # phone,
        # province,
        # registrationUTCDateTime
        # TacID
        assert isinstance(
            customer.tac_code_peek, uuid.UUID)
        # uTCOffsetInMinutes,
        # zip,
# endset
        assert customer is not None
        assert customer.active_organization_id == 0
        assert customer.email == ""
        assert customer.email_confirmed_utc_date_time == datetime(1753, 1, 1)
        assert customer.first_name == ""
        assert customer.forgot_password_key_expiration_utc_date_time == datetime(1753, 1, 1)
        assert customer.forgot_password_key_value == ""
        # fs_user_code_value
        assert isinstance(
            customer.fs_user_code_value,
            uuid.UUID
        )
        assert customer.is_active is False
        assert customer.is_email_allowed is False
        assert customer.is_email_confirmed is False
        assert customer.is_email_marketing_allowed is False
        assert customer.is_locked is False
        assert customer.is_multiple_organizations_allowed is False
        assert customer.is_verbose_logging_forced is False
        assert customer.last_login_utc_date_time == datetime(1753, 1, 1)
        assert customer.last_name == ""
        assert customer.password == ""
        assert customer.phone == ""
        assert customer.province == ""
        assert customer.registration_utc_date_time == datetime(1753, 1, 1)
        assert customer.tac_id == 0
        assert customer.utc_offset_in_minutes == 0
        assert customer.zip == ""
# endset
    def test_last_change_code_concurrency(self, session):
        """
        #TODO add comment
        """
        customer = CustomerFactory.create(session=session)
        original_last_change_code = customer.last_change_code
        customer_1 = session.query(Customer).filter_by(
            customer_id=customer.customer_id).first()
        customer_1.code = uuid.uuid4()
        session.commit()
        customer_2 = session.query(Customer).filter_by(
            customer_id=customer.customer_id).first()
        customer_2.code = uuid.uuid4()
        session.commit()
        assert customer_2.last_change_code != original_last_change_code
# endset
    # activeOrganizationID,
    # email,
    # emailConfirmedUTCDateTime
    # firstName,
    # forgotPasswordKeyExpirationUTCDateTime
    # forgotPasswordKeyValue,
    # fSUserCodeValue,
    # isActive,
    # isEmailAllowed,
    # isEmailConfirmed,
    # isEmailMarketingAllowed,
    # isLocked,
    # isMultipleOrganizationsAllowed,
    # isVerboseLoggingForced,
    # lastLoginUTCDateTime
    # lastName,
    # password,
    # phone,
    # province,
    # registrationUTCDateTime
    # TacID
    def test_invalid_tac_id(self, session):
        """
        #TODO add comment
        """
        customer = CustomerFactory.create(session=session)
        customer.tac_id = 99999
        with pytest.raises(IntegrityError):
            session.commit()
        session.rollback()
    # uTCOffsetInMinutes,
    # zip,
# endset
