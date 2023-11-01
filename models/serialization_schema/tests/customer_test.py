import pytest
from models import Customer
from models.serialization_schema import CustomerSchema
from models.factory import CustomerFactory
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base
from services.logging_config import get_logger
logger = get_logger(__name__)
DATABASE_URL = "sqlite:///:memory:"
class TestCustomerSchema:
    @pytest.fixture(scope="module")
    def engine(self):
        engine = create_engine(DATABASE_URL, echo=True)
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
    @pytest.fixture
    def customer(self, session):
        # Use the CustomerFactory to create and return a customer instance
        return CustomerFactory.create(session=session)
    # Tests
    def test_customer_serialization(self, customer:Customer, session):
        schema = CustomerSchema()
        result = schema.dump(customer)
        assert result['code'] == customer.code
        assert result['last_change_code'] == customer.last_change_code
        assert result['insert_user_id'] == customer.insert_user_id
        assert result['last_update_user_id'] == customer.last_update_user_id

        assert result['active_organization_id'] == customer.active_organization_id
        assert result['email'] == customer.email
        assert result['email_confirmed_utc_date_time'] == customer.email_confirmed_utc_date_time.isoformat()
        assert result['first_name'] == customer.first_name
        assert result['forgot_password_key_expiration_utc_date_time'] == customer.forgot_password_key_expiration_utc_date_time.isoformat()
        assert result['forgot_password_key_value'] == customer.forgot_password_key_value
        assert result['fs_user_code_value'] == customer.fs_user_code_value
        assert result['is_active'] == customer.is_active
        assert result['is_email_allowed'] == customer.is_email_allowed
        assert result['is_email_confirmed'] == customer.is_email_confirmed
        assert result['is_email_marketing_allowed'] == customer.is_email_marketing_allowed
        assert result['is_locked'] == customer.is_locked
        assert result['is_multiple_organizations_allowed'] == customer.is_multiple_organizations_allowed
        assert result['is_verbose_logging_forced'] == customer.is_verbose_logging_forced
        assert result['last_login_utc_date_time'] == customer.last_login_utc_date_time.isoformat()
        assert result['last_name'] == customer.last_name
        assert result['password'] == customer.password
        assert result['phone'] == customer.phone
        assert result['province'] == customer.province
        assert result['registration_utc_date_time'] == customer.registration_utc_date_time.isoformat()
        assert result['tac_id'] == customer.tac_id
        assert result['utc_offset_in_minutes'] == customer.utc_offset_in_minutes
        assert result['zip'] == customer.zip

        assert result['insert_utc_date_time'] == customer.insert_utc_date_time.isoformat()
        assert result['last_update_utc_date_time'] == customer.last_update_utc_date_time.isoformat()

        assert result['tac_code_peek'] == customer.tac_code_peek # TacID

    def test_customer_deserialization(self, customer:Customer, session):
        schema = CustomerSchema()
        serialized_data = schema.dump(customer)
        deserialized_data = schema.load(serialized_data)
        assert deserialized_data['code'] == customer.code
        assert deserialized_data['last_change_code'] == customer.last_change_code
        assert deserialized_data['insert_user_id'] == customer.insert_user_id
        assert deserialized_data['last_update_user_id'] == customer.last_update_user_id

        assert deserialized_data['active_organization_id'] == customer.active_organization_id
        assert deserialized_data['email'] == customer.email
        assert deserialized_data['email_confirmed_utc_date_time'].isoformat() == customer.email_confirmed_utc_date_time.isoformat()
        assert deserialized_data['first_name'] == customer.first_name
        assert deserialized_data['forgot_password_key_expiration_utc_date_time'].isoformat() == customer.forgot_password_key_expiration_utc_date_time.isoformat()
        assert deserialized_data['forgot_password_key_value'] == customer.forgot_password_key_value
        assert deserialized_data['fs_user_code_value'] == customer.fs_user_code_value
        assert deserialized_data['is_active'] == customer.is_active
        assert deserialized_data['is_email_allowed'] == customer.is_email_allowed
        assert deserialized_data['is_email_confirmed'] == customer.is_email_confirmed
        assert deserialized_data['is_email_marketing_allowed'] == customer.is_email_marketing_allowed
        assert deserialized_data['is_locked'] == customer.is_locked
        assert deserialized_data['is_multiple_organizations_allowed'] == customer.is_multiple_organizations_allowed
        assert deserialized_data['is_verbose_logging_forced'] == customer.is_verbose_logging_forced
        assert deserialized_data['last_login_utc_date_time'].isoformat() == customer.last_login_utc_date_time.isoformat()
        assert deserialized_data['last_name'] == customer.last_name
        assert deserialized_data['password'] == customer.password
        assert deserialized_data['phone'] == customer.phone
        assert deserialized_data['province'] == customer.province
        assert deserialized_data['registration_utc_date_time'].isoformat() == customer.registration_utc_date_time.isoformat()
        assert deserialized_data['tac_id'] == customer.tac_id
        assert deserialized_data['utc_offset_in_minutes'] == customer.utc_offset_in_minutes
        assert deserialized_data['zip'] == customer.zip

        assert deserialized_data['insert_utc_date_time'].isoformat() == customer.insert_utc_date_time.isoformat()
        assert deserialized_data['last_update_utc_date_time'].isoformat() == customer.last_update_utc_date_time.isoformat()

        assert deserialized_data['tac_code_peek'] == customer.tac_code_peek # TacID

        new_customer = Customer(**deserialized_data)
        assert isinstance(new_customer, Customer)
        # Now compare the new_customer attributes with the customer attributes
        assert new_customer.code == customer.code
        assert new_customer.last_change_code == customer.last_change_code
        assert new_customer.insert_user_id == customer.insert_user_id
        assert new_customer.last_update_user_id == customer.last_update_user_id

        assert new_customer.active_organization_id == customer.active_organization_id
        assert new_customer.email == customer.email
        assert new_customer.email_confirmed_utc_date_time.isoformat() == customer.email_confirmed_utc_date_time.isoformat()
        assert new_customer.first_name == customer.first_name
        assert new_customer.forgot_password_key_expiration_utc_date_time.isoformat() == customer.forgot_password_key_expiration_utc_date_time.isoformat()
        assert new_customer.forgot_password_key_value == customer.forgot_password_key_value
        assert new_customer.fs_user_code_value == customer.fs_user_code_value
        assert new_customer.is_active == customer.is_active
        assert new_customer.is_email_allowed == customer.is_email_allowed
        assert new_customer.is_email_confirmed == customer.is_email_confirmed
        assert new_customer.is_email_marketing_allowed == customer.is_email_marketing_allowed
        assert new_customer.is_locked == customer.is_locked
        assert new_customer.is_multiple_organizations_allowed == customer.is_multiple_organizations_allowed
        assert new_customer.is_verbose_logging_forced == customer.is_verbose_logging_forced
        assert new_customer.last_login_utc_date_time.isoformat() == customer.last_login_utc_date_time.isoformat()
        assert new_customer.last_name == customer.last_name
        assert new_customer.password == customer.password
        assert new_customer.phone == customer.phone
        assert new_customer.province == customer.province
        assert new_customer.registration_utc_date_time.isoformat() == customer.registration_utc_date_time.isoformat()
        assert new_customer.tac_id == customer.tac_id
        assert new_customer.utc_offset_in_minutes == customer.utc_offset_in_minutes
        assert new_customer.zip == customer.zip

        assert new_customer.insert_utc_date_time.isoformat() == customer.insert_utc_date_time.isoformat()
        assert new_customer.last_update_utc_date_time.isoformat() == customer.last_update_utc_date_time.isoformat()

        assert new_customer.tac_code_peek == customer.tac_code_peek #TacID

