# customer_test.py
"""
    #TODO add comment
"""
import json
import logging
from datetime import datetime
from decimal import Decimal
import pytest
import pytz
from models import Customer
from models.factory import CustomerFactory
from models.serialization_schema import CustomerSchema
from services.logging_config import get_logger
logger = get_logger(__name__)
@pytest.fixture(scope="function")
def customer(session):
    """
    #TODO add comment
    """
    # Use the CustomerFactory to create and return a customer instance
    return CustomerFactory.create(session=session)
class TestCustomerSchema:
    """
    #TODO add comment
    """
    # Sample data for a Customer instance
    sample_data = {
        "customer_id": 1,
        "code": "a1b2c3d4-e5f6-7a8b-9c0d-123456789012",
        "last_change_code": 0,
        "insert_user_id": "a1b2c3d4-e5f6-7a8b-9c0d-123456789012",
        "last_update_user_id": "a1b2c3d4-e5f6-7a8b-9c0d-123456789012",
# endset  # noqa: E122
        "active_organization_id": 42,
        "email": "test@email.com",
        "email_confirmed_utc_date_time": datetime(
            2023, 1, 1, 12, 0, 0, tzinfo=pytz.utc
        ).isoformat(),
        "first_name": "Vanilla",
        "forgot_password_key_expiration_utc_date_time": datetime(
            2023, 1, 1, 12, 0, 0, tzinfo=pytz.utc
        ).isoformat(),
        "forgot_password_key_value": "Vanilla",
        "fs_user_code_value": "a1b2c3d4-e5f6-7a8b-9c0d-123456789012",
        "is_active": False,
        "is_email_allowed": False,
        "is_email_confirmed": False,
        "is_email_marketing_allowed": False,
        "is_locked": False,
        "is_multiple_organizations_allowed": False,
        "is_verbose_logging_forced": False,
        "last_login_utc_date_time": datetime(
            2023, 1, 1, 12, 0, 0, tzinfo=pytz.utc
        ).isoformat(),
        "last_name": "Vanilla",
        "password": "Vanilla",
        "phone": "123-456-7890",
        "province": "Vanilla",
        "registration_utc_date_time": datetime(
            2023, 1, 1, 12, 0, 0, tzinfo=pytz.utc
        ).isoformat(),
        "tac_id": 2,
        "utc_offset_in_minutes": 42,
        "zip": "Vanilla",
        "insert_utc_date_time": datetime(
            2024, 1, 1, 12, 0, 0, tzinfo=pytz.utc
        ).isoformat(),
        "last_update_utc_date_time": datetime(
            2025, 1, 1, 12, 0, 0, tzinfo=pytz.utc
        ).isoformat(),
# endset  # noqa: E122
        "tac_code_peek": "a1b2c3d4-e5f6-7a8b-9c0d-123456789012",  # TacID
# endset  # noqa: E122
    }
    def test_customer_serialization(self, customer: Customer):
        """
            #TODO add comment
        """
        schema = CustomerSchema()
        result = schema.dump(customer)
        assert result['code'] == str(customer.code)
        assert result['last_change_code'] == (
            customer.last_change_code)
        assert result['insert_user_id'] == (
            str(customer.insert_user_id))
        assert result['last_update_user_id'] == (
            str(customer.last_update_user_id))
# endset
        assert result['active_organization_id'] == (
            customer.active_organization_id)
        assert result['email'] == (
            customer.email)
        assert result['email_confirmed_utc_date_time'] == (
            customer.email_confirmed_utc_date_time.isoformat())
        assert result['first_name'] == (
            customer.first_name)
        assert result['forgot_password_key_expiration_utc_date_time'] == (
            customer.forgot_password_key_expiration_utc_date_time.isoformat())
        assert result['forgot_password_key_value'] == (
            customer.forgot_password_key_value)
        assert result['fs_user_code_value'] == (
            str(customer.fs_user_code_value))
        assert result['is_active'] == (
            customer.is_active)
        assert result['is_email_allowed'] == (
            customer.is_email_allowed)
        assert result['is_email_confirmed'] == (
            customer.is_email_confirmed)
        assert result['is_email_marketing_allowed'] == (
            customer.is_email_marketing_allowed)
        assert result['is_locked'] == (
            customer.is_locked)
        assert result['is_multiple_organizations_allowed'] == (
            customer.is_multiple_organizations_allowed)
        assert result['is_verbose_logging_forced'] == (
            customer.is_verbose_logging_forced)
        assert result['last_login_utc_date_time'] == (
            customer.last_login_utc_date_time.isoformat())
        assert result['last_name'] == (
            customer.last_name)
        assert result['password'] == (
            customer.password)
        assert result['phone'] == (
            customer.phone)
        assert result['province'] == (
            customer.province)
        assert result['registration_utc_date_time'] == (
            customer.registration_utc_date_time.isoformat())
        assert result['tac_id'] == (
            customer.tac_id)
        assert result['utc_offset_in_minutes'] == (
            customer.utc_offset_in_minutes)
        assert result['zip'] == (
            customer.zip)
# endset
        assert result['insert_utc_date_time'] == (
            customer.insert_utc_date_time.isoformat())
        assert result['last_update_utc_date_time'] == (
            customer.last_update_utc_date_time.isoformat())
# endset
        assert result['tac_code_peek'] == (  # TacID
            str(customer.tac_code_peek))
# endset
    def test_customer_deserialization(self, customer: Customer):
        """
            #TODO add comment
        """
        schema = CustomerSchema()
        serialized_data = schema.dump(customer)
        deserialized_data = schema.load(serialized_data)
        assert deserialized_data['code'] == customer.code
        assert deserialized_data['last_change_code'] == (
            customer.last_change_code)
        assert deserialized_data['insert_user_id'] == (
            customer.insert_user_id)
        assert deserialized_data['last_update_user_id'] == (
            customer.last_update_user_id)
# endset
        assert deserialized_data['active_organization_id'] == (
            customer.active_organization_id)
        assert deserialized_data['email'] == (
            customer.email)
        assert deserialized_data['email_confirmed_utc_date_time'].isoformat() == (
            customer.email_confirmed_utc_date_time.isoformat())
        assert deserialized_data['first_name'] == (
            customer.first_name)
        assert deserialized_data['forgot_password_key_expiration_utc_date_time'].isoformat() == (
            customer.forgot_password_key_expiration_utc_date_time.isoformat())
        assert deserialized_data['forgot_password_key_value'] == (
            customer.forgot_password_key_value)
        assert deserialized_data['fs_user_code_value'] == (
            customer.fs_user_code_value)
        assert deserialized_data['is_active'] == (
            customer.is_active)
        assert deserialized_data['is_email_allowed'] == (
            customer.is_email_allowed)
        assert deserialized_data['is_email_confirmed'] == (
            customer.is_email_confirmed)
        assert deserialized_data['is_email_marketing_allowed'] == (
            customer.is_email_marketing_allowed)
        assert deserialized_data['is_locked'] == (
            customer.is_locked)
        assert deserialized_data['is_multiple_organizations_allowed'] == (
            customer.is_multiple_organizations_allowed)
        assert deserialized_data['is_verbose_logging_forced'] == (
            customer.is_verbose_logging_forced)
        assert deserialized_data['last_login_utc_date_time'].isoformat() == (
            customer.last_login_utc_date_time.isoformat())
        assert deserialized_data['last_name'] == (
            customer.last_name)
        assert deserialized_data['password'] == (
            customer.password)
        assert deserialized_data['phone'] == (
            customer.phone)
        assert deserialized_data['province'] == (
            customer.province)
        assert deserialized_data['registration_utc_date_time'].isoformat() == (
            customer.registration_utc_date_time.isoformat())
        assert deserialized_data['tac_id'] == (
            customer.tac_id)
        assert deserialized_data['utc_offset_in_minutes'] == (
            customer.utc_offset_in_minutes)
        assert deserialized_data['zip'] == (
            customer.zip)
# endset
        assert deserialized_data['insert_utc_date_time'].isoformat() == (
            customer.insert_utc_date_time.isoformat())
        assert deserialized_data['last_update_utc_date_time'].isoformat() == (
            customer.last_update_utc_date_time.isoformat())
# endset
        assert deserialized_data['tac_code_peek'] == (  # TacID
            customer.tac_code_peek)
# endset
        new_customer = Customer(**deserialized_data)
        assert isinstance(new_customer, Customer)
        # Now compare the new_customer attributes with the customer attributes
        assert new_customer.code == customer.code
        assert new_customer.last_change_code == customer.last_change_code
        assert new_customer.insert_user_id == customer.insert_user_id
        assert new_customer.last_update_user_id == customer.last_update_user_id
# endset
        assert new_customer.active_organization_id == (
            customer.active_organization_id)
        assert new_customer.email == (
            customer.email)
        assert new_customer.email_confirmed_utc_date_time.isoformat() == (
            customer.email_confirmed_utc_date_time.isoformat())
        assert new_customer.first_name == (
            customer.first_name)
        assert new_customer.forgot_password_key_expiration_utc_date_time.isoformat() == (
            customer.forgot_password_key_expiration_utc_date_time.isoformat())
        assert new_customer.forgot_password_key_value == (
            customer.forgot_password_key_value)
        assert new_customer.fs_user_code_value == (
            customer.fs_user_code_value)
        assert new_customer.is_active == (
            customer.is_active)
        assert new_customer.is_email_allowed == (
            customer.is_email_allowed)
        assert new_customer.is_email_confirmed == (
            customer.is_email_confirmed)
        assert new_customer.is_email_marketing_allowed == (
            customer.is_email_marketing_allowed)
        assert new_customer.is_locked == (
            customer.is_locked)
        assert new_customer.is_multiple_organizations_allowed == (
            customer.is_multiple_organizations_allowed)
        assert new_customer.is_verbose_logging_forced == (
            customer.is_verbose_logging_forced)
        assert new_customer.last_login_utc_date_time.isoformat() == (
            customer.last_login_utc_date_time.isoformat())
        assert new_customer.last_name == (
            customer.last_name)
        assert new_customer.password == (
            customer.password)
        assert new_customer.phone == (
            customer.phone)
        assert new_customer.province == (
            customer.province)
        assert new_customer.registration_utc_date_time.isoformat() == (
            customer.registration_utc_date_time.isoformat())
        assert new_customer.tac_id == (
            customer.tac_id)
        assert new_customer.utc_offset_in_minutes == (
            customer.utc_offset_in_minutes)
        assert new_customer.zip == (
            customer.zip)
# endset
        assert new_customer.insert_utc_date_time.isoformat() == (
            customer.insert_utc_date_time.isoformat())
        assert new_customer.last_update_utc_date_time.isoformat() == (
            customer.last_update_utc_date_time.isoformat())
# endset
        assert new_customer.tac_code_peek == (  # TacID
            customer.tac_code_peek)
# endset
    def test_from_json(self):
        """
            #TODO add comment
        """
        customer_schema = CustomerSchema()
        # Convert sample data to JSON string
        json_str = json.dumps(self.sample_data)
        # Deserialize the JSON string to a dictionary
        json_data = json.loads(json_str)
        # Load the dictionary to an object
        deserialized_data = customer_schema.load(json_data)
        assert str(deserialized_data['customer_id']) == (
            str(self.sample_data['customer_id']))
        assert str(deserialized_data['code']) == (
            str(self.sample_data['code']))
        assert str(deserialized_data['last_change_code']) == (
            str(self.sample_data['last_change_code']))
        assert str(deserialized_data['insert_user_id']) == (
            str(self.sample_data['insert_user_id']))
        assert str(deserialized_data['last_update_user_id']) == (
            str(self.sample_data['last_update_user_id']))
# endset
        assert str(deserialized_data['active_organization_id']) == (
            str(self.sample_data['active_organization_id']))
        assert str(deserialized_data['email']) == (
            str(self.sample_data['email']))
        assert deserialized_data['email_confirmed_utc_date_time'].isoformat() == (
            self.sample_data['email_confirmed_utc_date_time'])
        assert str(deserialized_data['first_name']) == (
            str(self.sample_data['first_name']))
        assert deserialized_data['forgot_password_key_expiration_utc_date_time'].isoformat() == (
            self.sample_data['forgot_password_key_expiration_utc_date_time'])
        assert str(deserialized_data['forgot_password_key_value']) == (
            str(self.sample_data['forgot_password_key_value']))
        assert str(deserialized_data['fs_user_code_value']) == (
            str(self.sample_data['fs_user_code_value']))
        assert str(deserialized_data['is_active']) == (
            str(self.sample_data['is_active']))
        assert str(deserialized_data['is_email_allowed']) == (
            str(self.sample_data['is_email_allowed']))
        assert str(deserialized_data['is_email_confirmed']) == (
            str(self.sample_data['is_email_confirmed']))
        assert str(deserialized_data['is_email_marketing_allowed']) == (
            str(self.sample_data['is_email_marketing_allowed']))
        assert str(deserialized_data['is_locked']) == (
            str(self.sample_data['is_locked']))
        assert str(deserialized_data['is_multiple_organizations_allowed']) == (
            str(self.sample_data['is_multiple_organizations_allowed']))
        assert str(deserialized_data['is_verbose_logging_forced']) == (
            str(self.sample_data['is_verbose_logging_forced']))
        assert deserialized_data['last_login_utc_date_time'].isoformat() == (
            self.sample_data['last_login_utc_date_time'])
        assert str(deserialized_data['last_name']) == (
            str(self.sample_data['last_name']))
        assert str(deserialized_data['password']) == (
            str(self.sample_data['password']))
        assert str(deserialized_data['phone']) == (
            str(self.sample_data['phone']))
        assert str(deserialized_data['province']) == (
            str(self.sample_data['province']))
        assert deserialized_data['registration_utc_date_time'].isoformat() == (
            self.sample_data['registration_utc_date_time'])
        assert str(deserialized_data['tac_id']) == (
            str(self.sample_data['tac_id']))
        assert str(deserialized_data['utc_offset_in_minutes']) == (
            str(self.sample_data['utc_offset_in_minutes']))
        assert str(deserialized_data['zip']) == (
            str(self.sample_data['zip']))
# endset
        assert deserialized_data['insert_utc_date_time'].isoformat() == (
            self.sample_data['insert_utc_date_time'])
        assert str(deserialized_data['tac_code_peek']) == (  # TacID
            str(self.sample_data['tac_code_peek']))
# endset
        assert deserialized_data['last_update_utc_date_time'].isoformat() == (
            self.sample_data['last_update_utc_date_time'])
        new_customer = Customer(**deserialized_data)
        assert isinstance(new_customer, Customer)
    def test_to_json(self, customer: Customer):
        """
            #TODO add comment
        """
        # Convert the Customer instance to JSON using the schema
        customer_schema = CustomerSchema()
        customer_dict = customer_schema.dump(customer)
        # Convert the customer_dict to JSON string
        customer_json = json.dumps(customer_dict)
        # Convert the JSON strings back to dictionaries
        customer_dict_from_json = json.loads(customer_json)
        # sample_dict_from_json = json.loads(self.sample_data)
        logging.info("customer_dict_from_json.keys() %s", customer_dict_from_json.keys())
        logging.info("self.sample_data.keys() %s", self.sample_data.keys())
        # Verify the keys in both dictionaries match
        assert set(customer_dict_from_json.keys()) == (
            set(self.sample_data.keys())), (
            f"Expected keys: {set(self.sample_data.keys())}, Got: {set(customer_dict_from_json.keys())}"
        )
        assert customer_dict_from_json['code'] == str(customer.code), (
            "failed on code"
        )
        assert customer_dict_from_json['last_change_code'] == (
            customer.last_change_code), (
            "failed on last_change_code"
        )
        assert customer_dict_from_json['insert_user_id'] == (
            str(customer.insert_user_id)), (
            "failed on insert_user_id"
        )
        assert customer_dict_from_json['last_update_user_id'] == (
            str(customer.last_update_user_id)), (
            "failed on last_update_user_id"
        )
# endset
        assert customer_dict_from_json['active_organization_id'] == (
            customer.active_organization_id), (
            "failed on active_organization_id"
        )
        assert customer_dict_from_json['email'] == (
            customer.email), (
            "failed on email"
        )
        assert customer_dict_from_json['email_confirmed_utc_date_time'] == (
            customer.email_confirmed_utc_date_time.isoformat()), (
            "failed on email_confirmed_utc_date_time"
        )
        assert customer_dict_from_json['first_name'] == (
            customer.first_name), (
            "failed on first_name"
        )
        assert customer_dict_from_json['forgot_password_key_expiration_utc_date_time'] == (
            customer.forgot_password_key_expiration_utc_date_time.isoformat()), (
            "failed on forgot_password_key_expiration_utc_date_time"
        )
        assert customer_dict_from_json['forgot_password_key_value'] == (
            customer.forgot_password_key_value), (
            "failed on forgot_password_key_value"
        )
        assert customer_dict_from_json['fs_user_code_value'] == (
            str(customer.fs_user_code_value)), (
            "failed on fs_user_code_value"
        )
        assert customer_dict_from_json['is_active'] == (
            customer.is_active), (
            "failed on is_active"
        )
        assert customer_dict_from_json['is_email_allowed'] == (
            customer.is_email_allowed), (
            "failed on is_email_allowed"
        )
        assert customer_dict_from_json['is_email_confirmed'] == (
            customer.is_email_confirmed), (
            "failed on is_email_confirmed"
        )
        assert customer_dict_from_json['is_email_marketing_allowed'] == (
            customer.is_email_marketing_allowed), (
            "failed on is_email_marketing_allowed"
        )
        assert customer_dict_from_json['is_locked'] == (
            customer.is_locked), (
            "failed on is_locked"
        )
        assert customer_dict_from_json['is_multiple_organizations_allowed'] == (
            customer.is_multiple_organizations_allowed), (
            "failed on is_multiple_organizations_allowed"
        )
        assert customer_dict_from_json['is_verbose_logging_forced'] == (
            customer.is_verbose_logging_forced), (
            "failed on is_verbose_logging_forced"
        )
        assert customer_dict_from_json['last_login_utc_date_time'] == (
            customer.last_login_utc_date_time.isoformat()), (
            "failed on last_login_utc_date_time"
        )
        assert customer_dict_from_json['last_name'] == (
            customer.last_name), (
            "failed on last_name"
        )
        assert customer_dict_from_json['password'] == (
            customer.password), (
            "failed on password"
        )
        assert customer_dict_from_json['phone'] == (
            customer.phone), (
            "failed on phone"
        )
        assert customer_dict_from_json['province'] == (
            customer.province), (
            "failed on province"
        )
        assert customer_dict_from_json['registration_utc_date_time'] == (
            customer.registration_utc_date_time.isoformat()), (
            "failed on registration_utc_date_time"
        )
        assert customer_dict_from_json['tac_id'] == (
            customer.tac_id), (
            "failed on tac_id"
        )
        assert customer_dict_from_json['utc_offset_in_minutes'] == (
            customer.utc_offset_in_minutes), (
            "failed on utc_offset_in_minutes"
        )
        assert customer_dict_from_json['zip'] == (
            customer.zip), (
            "failed on zip"
        )
# endset
        assert customer_dict_from_json['insert_utc_date_time'] == (
            customer.insert_utc_date_time.isoformat()), (
            "failed on insert_utc_date_time"
        )
        assert customer_dict_from_json['last_update_utc_date_time'] == (
            customer.last_update_utc_date_time.isoformat()), (
            "failed on last_update_utc_date_time"
        )
# endset
        assert customer_dict_from_json['tac_code_peek'] == (  # TacID
            str(customer.tac_code_peek)), (
            "failed on tac_code_peek"
        )
# endset
