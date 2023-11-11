from decimal import Decimal
import pytest
import time
from decimal import Decimal
from datetime import datetime, date
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Customer
from models.factory import CustomerFactory
from services.db_config import db_dialect
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
from services.db_config import db_dialect,generate_uuid
from sqlalchemy import String
from sqlalchemy.exc import IntegrityError
DATABASE_URL = "sqlite:///:memory:"
db_dialect = "sqlite"
# Conditionally set the UUID column type
if db_dialect == 'postgresql':
    UUIDType = UUID(as_uuid=True)
elif db_dialect == 'mssql':
    UUIDType = UNIQUEIDENTIFIER
else:  # This will cover SQLite, MySQL, and other databases
    UUIDType = String(36)
class TestCustomerFactory:
    @pytest.fixture(scope="module")
    def engine(self):
        engine = create_engine(DATABASE_URL, echo=False)
        #FKs are not activated by default in sqllite
        with engine.connect() as conn:
            conn.connection.execute("PRAGMA foreign_keys=ON")
        yield engine
        engine.dispose()
    @pytest.fixture
    def session(self, engine):
        Base.metadata.create_all(engine)
        SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)
        session_instance = SessionLocal()
        yield session_instance
        session_instance.close()
    def test_customer_creation(self, session):
        customer = CustomerFactory.create(session=session)
        assert customer.customer_id is not None
    def test_code_default(self, session):
        customer = CustomerFactory.create(session=session)
        if db_dialect == 'postgresql':
            assert isinstance(customer.code, UUID)
        elif db_dialect == 'mssql':
            assert isinstance(customer.code, UNIQUEIDENTIFIER)
        else:  # This will cover SQLite, MySQL, and other databases
            assert isinstance(customer.code, str)
    def test_last_change_code_default_on_build(self, session):
        customer:Customer = CustomerFactory.build(session=session)
        assert customer.last_change_code == 0
    def test_last_change_code_default_on_creation(self, session):
        customer:Customer = CustomerFactory.create(session=session)
        assert customer.last_change_code == 1
    def test_last_change_code_default_on_update(self, session):
        customer = CustomerFactory.create(session=session)
        initial_code = customer.last_change_code
        customer.code = generate_uuid()
        session.commit()
        assert customer.last_change_code != initial_code
    def test_date_inserted_on_build(self, session):
        customer = CustomerFactory.build(session=session)
        assert customer.insert_utc_date_time is not None
        assert isinstance(customer.insert_utc_date_time, datetime)
    def test_date_inserted_on_initial_save(self, session):
        customer = CustomerFactory.build(session=session)
        assert customer.insert_utc_date_time is not None
        assert isinstance(customer.insert_utc_date_time, datetime)
        initial_time = customer.insert_utc_date_time
        customer.code = generate_uuid()
        time.sleep(1)
        session.commit()
        assert customer.insert_utc_date_time > initial_time
    def test_date_inserted_on_second_save(self, session):
        customer = CustomerFactory(session=session)
        assert customer.insert_utc_date_time is not None
        assert isinstance(customer.insert_utc_date_time, datetime)
        initial_time = customer.insert_utc_date_time
        customer.code = generate_uuid()
        time.sleep(1)
        session.commit()
        assert customer.insert_utc_date_time == initial_time
    def test_date_updated_on_build(self, session):
        customer = CustomerFactory.build(session=session)
        assert customer.last_update_utc_date_time is not None
        assert isinstance(customer.last_update_utc_date_time, datetime)
    def test_date_updated_on_initial_save(self, session):
        customer = CustomerFactory.build(session=session)
        assert customer.last_update_utc_date_time is not None
        assert isinstance(customer.last_update_utc_date_time, datetime)
        initial_time = customer.last_update_utc_date_time
        customer.code = generate_uuid()
        time.sleep(1)
        session.commit()
        assert customer.last_update_utc_date_time > initial_time
    def test_date_updated_on_second_save(self, session):
        customer = CustomerFactory(session=session)
        assert customer.last_update_utc_date_time is not None
        assert isinstance(customer.last_update_utc_date_time, datetime)
        initial_time = customer.last_update_utc_date_time
        customer.code = generate_uuid()
        time.sleep(1)
        session.commit()
        assert customer.last_update_utc_date_time > initial_time
    def test_model_deletion(self, session):
        customer = CustomerFactory.create(session=session)
        session.delete(customer)
        session.commit()
        deleted_customer = session.query(Customer).filter_by(customer_id=customer.customer_id).first()
        assert deleted_customer is None
    def test_data_types(self, session):
        customer = CustomerFactory.create(session=session)
        assert isinstance(customer.customer_id, int)
        if db_dialect == 'postgresql':
            assert isinstance(customer.code, UUID)
        elif db_dialect == 'mssql':
            assert isinstance(customer.code, UNIQUEIDENTIFIER)
        else:  # This will cover SQLite, MySQL, and other databases
            assert isinstance(customer.code, str)
        assert isinstance(customer.last_change_code, int)
        if db_dialect == 'postgresql':
            assert isinstance(customer.insert_user_id, UUID)
        elif db_dialect == 'mssql':
            assert isinstance(customer.insert_user_id, UNIQUEIDENTIFIER)
        else:  # This will cover SQLite, MySQL, and other databases
            assert isinstance(customer.insert_user_id, str)
        if db_dialect == 'postgresql':
            assert isinstance(customer.last_update_user_id, UUID)
        elif db_dialect == 'mssql':
            assert isinstance(customer.last_update_user_id, UNIQUEIDENTIFIER)
        else:  # This will cover SQLite, MySQL, and other databases
            assert isinstance(customer.last_update_user_id, str)
        assert isinstance(customer.active_organization_id, int)
        assert customer.email == "" or isinstance(customer.email, str)
        assert isinstance(customer.email_confirmed_utc_date_time, datetime)
        assert customer.first_name == "" or isinstance(customer.first_name, str)
        assert isinstance(customer.forgot_password_key_expiration_utc_date_time, datetime)
        assert customer.forgot_password_key_value == "" or isinstance(customer.forgot_password_key_value, str)
        #FSUserCodeValue
        if db_dialect == 'postgresql':
            assert isinstance(customer.fs_user_code_value, UUID)
        elif db_dialect == 'mssql':
            assert isinstance(customer.fs_user_code_value, UNIQUEIDENTIFIER)
        else:  # This will cover SQLite, MySQL, and other databases
            assert isinstance(customer.fs_user_code_value, str)
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
        assert customer.phone == "" or isinstance(customer.phone, str)
        assert customer.province == "" or isinstance(customer.province, str)
        assert isinstance(customer.registration_utc_date_time, datetime)
        assert isinstance(customer.tac_id, int)
        assert isinstance(customer.utc_offset_in_minutes, int)
        assert customer.zip == "" or isinstance(customer.zip, str)
        # Check for the peek values, assuming they are UUIDs based on your model

        #activeOrganizationID,
        #email,
        #emailConfirmedUTCDateTime
        #firstName,
        #forgotPasswordKeyExpirationUTCDateTime
        #forgotPasswordKeyValue,
        #fSUserCodeValue,
        #isActive,
        #isEmailAllowed,
        #isEmailConfirmed,
        #isEmailMarketingAllowed,
        #isLocked,
        #isMultipleOrganizationsAllowed,
        #isVerboseLoggingForced,
        #lastLoginUTCDateTime
        #lastName,
        #password,
        #phone,
        #province,
        #registrationUTCDateTime
        #tacID
        if db_dialect == 'postgresql':
            assert isinstance(customer.tac_code_peek, UUID)
        elif db_dialect == 'mssql':
            assert isinstance(customer.tac_code_peek, UNIQUEIDENTIFIER)
        else:  # This will cover SQLite, MySQL, and other databases
            assert isinstance(customer.tac_code_peek, str)
        #uTCOffsetInMinutes,
        #zip,

        assert isinstance(customer.insert_utc_date_time, datetime)
        assert isinstance(customer.last_update_utc_date_time, datetime)
    def test_unique_code_constraint(self, session):
        customer_1 = CustomerFactory.create(session=session)
        customer_2 = CustomerFactory.create(session=session)
        customer_2.code = customer_1.code
        session.add_all([customer_1, customer_2])
        with pytest.raises(Exception):  # adjust for the specific DB exception you'd expect
            session.commit()
        session.rollback()
    def test_fields_default(self, session):
        customer = Customer()
        assert customer.code is not None
        assert customer.last_change_code is not None
        assert customer.insert_user_id is None
        assert customer.last_update_user_id is None
        assert customer.insert_utc_date_time is not None
        assert customer.last_update_utc_date_time is not None

        #activeOrganizationID,
        #email,
        #emailConfirmedUTCDateTime
        #firstName,
        #forgotPasswordKeyExpirationUTCDateTime
        #forgotPasswordKeyValue,
        #fSUserCodeValue,
        #isActive,
        #isEmailAllowed,
        #isEmailConfirmed,
        #isEmailMarketingAllowed,
        #isLocked,
        #isMultipleOrganizationsAllowed,
        #isVerboseLoggingForced,
        #lastLoginUTCDateTime
        #lastName,
        #password,
        #phone,
        #province,
        #registrationUTCDateTime
        #TacID
        if db_dialect == 'postgresql':
            assert isinstance(customer.tac_code_peek, UUID)
        elif db_dialect == 'mssql':
            assert isinstance(customer.tac_code_peek, UNIQUEIDENTIFIER)
        else:  # This will cover SQLite, MySQL, and other databases
            assert isinstance(customer.tac_code_peek, str)
        #uTCOffsetInMinutes,
        #zip,

        assert customer.active_organization_id == 0
        assert customer.email == ""
        assert customer.email_confirmed_utc_date_time == datetime(1753, 1, 1)
        assert customer.first_name == ""
        assert customer.forgot_password_key_expiration_utc_date_time == datetime(1753, 1, 1)
        assert customer.forgot_password_key_value == ""
        #SomeUniqueIdentifierVal
        if db_dialect == 'postgresql':
            assert isinstance(customer.fs_user_code_value, UUID)
        elif db_dialect == 'mssql':
            assert isinstance(customer.fs_user_code_value, UNIQUEIDENTIFIER)
        else:  # This will cover SQLite, MySQL, and other databases
            assert isinstance(customer.fs_user_code_value, str)
        assert customer.is_active == False
        assert customer.is_email_allowed == False
        assert customer.is_email_confirmed == False
        assert customer.is_email_marketing_allowed == False
        assert customer.is_locked == False
        assert customer.is_multiple_organizations_allowed == False
        assert customer.is_verbose_logging_forced == False
        assert customer.last_login_utc_date_time == datetime(1753, 1, 1)
        assert customer.last_name == ""
        assert customer.password == ""
        assert customer.phone == ""
        assert customer.province == ""
        assert customer.registration_utc_date_time == datetime(1753, 1, 1)
        assert customer.tac_id == 0
        assert customer.utc_offset_in_minutes == 0
        assert customer.zip == ""

    def test_last_change_code_concurrency(self, session):
        customer = CustomerFactory.create(session=session)
        original_last_change_code = customer.last_change_code
        customer_1 = session.query(Customer).filter_by(customer_id=customer.customer_id).first()
        customer_1.code = generate_uuid()
        session.commit()
        customer_2 = session.query(Customer).filter_by(customer_id=customer.customer_id).first()
        customer_2.code = generate_uuid()
        session.commit()
        assert customer_2.last_change_code != original_last_change_code

    #activeOrganizationID,
    #email,
    #emailConfirmedUTCDateTime
    #firstName,
    #forgotPasswordKeyExpirationUTCDateTime
    #forgotPasswordKeyValue,
    #fSUserCodeValue,
    #isActive,
    #isEmailAllowed,
    #isEmailConfirmed,
    #isEmailMarketingAllowed,
    #isLocked,
    #isMultipleOrganizationsAllowed,
    #isVerboseLoggingForced,
    #lastLoginUTCDateTime
    #lastName,
    #password,
    #phone,
    #province,
    #registrationUTCDateTime
    #TacID
    def test_invalid_tac_id(self, session):
        customer = CustomerFactory.create(session=session)
        customer.tac_id = 99999
        with pytest.raises(IntegrityError):  # adjust for the specific DB exception you'd expect
            session.commit()
        session.rollback()
    #uTCOffsetInMinutes,
    #zip,

