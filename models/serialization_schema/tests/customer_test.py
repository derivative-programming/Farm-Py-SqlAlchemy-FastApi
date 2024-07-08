# models/serialization_schema/tests/customer_test.py  # pylint: disable=duplicate-code
# pylint: disable=redefined-outer-name, too-many-public-methods
# pylint: disable=unused-import

"""
This module contains tests for the
Customer serialization schema.

The Customer serialization schema
is responsible for serializing and deserializing
Customer instances. It ensures that the
data is properly formatted and can be
stored or retrieved from a database or
transmitted over a network.

The tests in this module cover the serialization
and deserialization of Customer
instances using the CustomerSchema
class. They verify
that the serialized data
matches the expected format and that the
deserialized data can be used to
reconstruct a Customer instance.

The CustomerSchema class
is used to define
the serialization and deserialization
rules for Customer instances. It
specifies how each attribute of a
Customer instance
should be converted to a serialized
format and how the serialized data should
be converted back to a Customer
instance.

The tests in this module use the pytest
framework to define test cases and
assertions. They ensure that the serialization
and deserialization process
works correctly and produces the expected results.

"""

import json
import logging
from datetime import datetime  # noqa: F401
from decimal import Decimal  # noqa: F401

import pytz

import pytest
from models import Customer
from models.factory import CustomerFactory
from models.serialization_schema import CustomerSchema
from services.logging_config import get_logger

logger = get_logger(__name__)


@pytest.fixture(scope="function")
def new_obj(
    session
) -> Customer:
    """
    Fixture to create and return a Customer
    instance using the
    CustomerFactory.

    Args:
        session: The database session.

    Returns:
        Customer: A newly created
            Customer instance.
    """

    return CustomerFactory.create(session=session)


class TestCustomerSchema:
    """
    Tests for the Customer
    serialization schema.
    """

    # Sample data for a Customer
    # instance
    sample_data = {
        "customer_id": 1,
        "code":
            "a1b2c3d4-e5f6-7a8b-9c0d-123456789012",
        "last_change_code": 0,
        "insert_user_id":
            "a1b2c3d4-e5f6-7a8b-9c0d-123456789012",
        "last_update_user_id":
            "a1b2c3d4-e5f6-7a8b-9c0d-123456789012",
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
        "fs_user_code_value":
            "a1b2c3d4-e5f6-7a8b-9c0d-123456789012",
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
        "tac_code_peek":  # TacID
            "a1b2c3d4-e5f6-7a8b-9c0d-123456789012",
# endset  # noqa: E122
    }

    def test_customer_serialization(
        self,
        new_obj: Customer
    ):
        """
        Test the serialization of a
        Customer instance using
        CustomerSchema.

        Args:
            customer (Customer):
                A Customer instance to serialize.
        """

        schema = CustomerSchema()
        customer_data = schema.dump(new_obj)

        assert isinstance(customer_data, dict)

        result = customer_data

        assert result['code'] == str(new_obj.code)
        assert result['last_change_code'] == (
            new_obj.last_change_code)
        assert result['insert_user_id'] == (
            str(new_obj.insert_user_id))
        assert result['last_update_user_id'] == (
            str(new_obj.last_update_user_id))

        assert result['active_organization_id'] == (
            new_obj.active_organization_id)
        assert result['email'] == (
            new_obj.email)
        assert result['email_confirmed_utc_date_time'] == (
            new_obj.email_confirmed_utc_date_time.isoformat())
        assert result['first_name'] == (
            new_obj.first_name)
        assert result['forgot_password_key_expiration_utc_date_time'] == (
            new_obj.forgot_password_key_expiration_utc_date_time.isoformat())
        assert result['forgot_password_key_value'] == (
            new_obj.forgot_password_key_value)
        assert result['fs_user_code_value'] == (
            str(new_obj.fs_user_code_value))
        assert result['is_active'] == (
            new_obj.is_active)
        assert result['is_email_allowed'] == (
            new_obj.is_email_allowed)
        assert result['is_email_confirmed'] == (
            new_obj.is_email_confirmed)
        assert result['is_email_marketing_allowed'] == (
            new_obj.is_email_marketing_allowed)
        assert result['is_locked'] == (
            new_obj.is_locked)
        assert result['is_multiple_organizations_allowed'] == (
            new_obj.is_multiple_organizations_allowed)
        assert result['is_verbose_logging_forced'] == (
            new_obj.is_verbose_logging_forced)
        assert result['last_login_utc_date_time'] == (
            new_obj.last_login_utc_date_time.isoformat())
        assert result['last_name'] == (
            new_obj.last_name)
        assert result['password'] == (
            new_obj.password)
        assert result['phone'] == (
            new_obj.phone)
        assert result['province'] == (
            new_obj.province)
        assert result['registration_utc_date_time'] == (
            new_obj.registration_utc_date_time.isoformat())
        assert result['tac_id'] == (
            new_obj.tac_id)
        assert result['utc_offset_in_minutes'] == (
            new_obj.utc_offset_in_minutes)
        assert result['zip'] == (
            new_obj.zip)
        assert result['insert_utc_date_time'] == (
            new_obj.insert_utc_date_time.isoformat())
        assert result['last_update_utc_date_time'] == (
            new_obj.last_update_utc_date_time.isoformat())
        assert result['tac_code_peek'] == (  # TacID
            str(new_obj.tac_code_peek))

    def test_customer_deserialization(
        self,
        new_obj: Customer
    ):
        """
        Test the deserialization of a
        Customer object using the
        CustomerSchema.

        Args:
            customer (Customer): The
                Customer object to be deserialized.

        Raises:
            AssertionError: If any of the assertions fail.

        Returns:
            None
        """

        schema = CustomerSchema()
        serialized_data = schema.dump(new_obj)
        deserialized_data = schema.load(serialized_data)

        assert deserialized_data['code'] == \
            new_obj.code
        assert deserialized_data['last_change_code'] == (
            new_obj.last_change_code)
        assert deserialized_data['insert_user_id'] == (
            new_obj.insert_user_id)
        assert deserialized_data['last_update_user_id'] == (
            new_obj.last_update_user_id)
        assert deserialized_data['active_organization_id'] == (
            new_obj.active_organization_id)
        assert deserialized_data['email'] == (
            new_obj.email)
        assert deserialized_data['email_confirmed_utc_date_time'].isoformat() == (
            new_obj.email_confirmed_utc_date_time.isoformat())
        assert deserialized_data['first_name'] == (
            new_obj.first_name)
        assert deserialized_data['forgot_password_key_expiration_utc_date_time'].isoformat() == (
            new_obj.forgot_password_key_expiration_utc_date_time.isoformat())
        assert deserialized_data['forgot_password_key_value'] == (
            new_obj.forgot_password_key_value)
        assert deserialized_data['fs_user_code_value'] == (
            new_obj.fs_user_code_value)
        assert deserialized_data['is_active'] == (
            new_obj.is_active)
        assert deserialized_data['is_email_allowed'] == (
            new_obj.is_email_allowed)
        assert deserialized_data['is_email_confirmed'] == (
            new_obj.is_email_confirmed)
        assert deserialized_data['is_email_marketing_allowed'] == (
            new_obj.is_email_marketing_allowed)
        assert deserialized_data['is_locked'] == (
            new_obj.is_locked)
        assert deserialized_data['is_multiple_organizations_allowed'] == (
            new_obj.is_multiple_organizations_allowed)
        assert deserialized_data['is_verbose_logging_forced'] == (
            new_obj.is_verbose_logging_forced)
        assert deserialized_data['last_login_utc_date_time'].isoformat() == (
            new_obj.last_login_utc_date_time.isoformat())
        assert deserialized_data['last_name'] == (
            new_obj.last_name)
        assert deserialized_data['password'] == (
            new_obj.password)
        assert deserialized_data['phone'] == (
            new_obj.phone)
        assert deserialized_data['province'] == (
            new_obj.province)
        assert deserialized_data['registration_utc_date_time'].isoformat() == (
            new_obj.registration_utc_date_time.isoformat())
        assert deserialized_data['tac_id'] == (
            new_obj.tac_id)
        assert deserialized_data['utc_offset_in_minutes'] == (
            new_obj.utc_offset_in_minutes)
        assert deserialized_data['zip'] == (
            new_obj.zip)
        assert deserialized_data['insert_utc_date_time'].isoformat() == (
            new_obj.insert_utc_date_time.isoformat())
        assert deserialized_data['last_update_utc_date_time'].isoformat() == (
            new_obj.last_update_utc_date_time.isoformat())
        assert deserialized_data[(  # TacID
            'tac_code_peek')] == (
            new_obj.tac_code_peek)

        obj_from_dict = Customer(
            **deserialized_data)

        assert isinstance(new_obj,
                          Customer)

        # Now compare the new_obj attributes with
        # the customer attributes
        assert obj_from_dict.code == \
            new_obj.code
        assert obj_from_dict.last_change_code == \
            new_obj.last_change_code
        assert obj_from_dict.insert_user_id == \
            new_obj.insert_user_id
        assert obj_from_dict.last_update_user_id == \
            new_obj.last_update_user_id
        assert obj_from_dict.active_organization_id == (
            new_obj.active_organization_id)
        assert obj_from_dict.email == (
            new_obj.email)
        assert obj_from_dict.email_confirmed_utc_date_time.isoformat() == (
            new_obj.email_confirmed_utc_date_time.isoformat())
        assert obj_from_dict.first_name == (
            new_obj.first_name)
        assert obj_from_dict.forgot_password_key_expiration_utc_date_time.isoformat() == (
            new_obj.forgot_password_key_expiration_utc_date_time.isoformat())
        assert obj_from_dict.forgot_password_key_value == (
            new_obj.forgot_password_key_value)
        assert obj_from_dict.fs_user_code_value == (
            new_obj.fs_user_code_value)
        assert obj_from_dict.is_active == (
            new_obj.is_active)
        assert obj_from_dict.is_email_allowed == (
            new_obj.is_email_allowed)
        assert obj_from_dict.is_email_confirmed == (
            new_obj.is_email_confirmed)
        assert obj_from_dict.is_email_marketing_allowed == (
            new_obj.is_email_marketing_allowed)
        assert obj_from_dict.is_locked == (
            new_obj.is_locked)
        assert obj_from_dict.is_multiple_organizations_allowed == (
            new_obj.is_multiple_organizations_allowed)
        assert obj_from_dict.is_verbose_logging_forced == (
            new_obj.is_verbose_logging_forced)
        assert obj_from_dict.last_login_utc_date_time.isoformat() == (
            new_obj.last_login_utc_date_time.isoformat())
        assert obj_from_dict.last_name == (
            new_obj.last_name)
        assert obj_from_dict.password == (
            new_obj.password)
        assert obj_from_dict.phone == (
            new_obj.phone)
        assert obj_from_dict.province == (
            new_obj.province)
        assert obj_from_dict.registration_utc_date_time.isoformat() == (
            new_obj.registration_utc_date_time.isoformat())
        assert obj_from_dict.tac_id == (
            new_obj.tac_id)
        assert obj_from_dict.utc_offset_in_minutes == (
            new_obj.utc_offset_in_minutes)
        assert obj_from_dict.zip == (
            new_obj.zip)

        assert obj_from_dict.insert_utc_date_time.isoformat() == (
            new_obj.insert_utc_date_time.isoformat())
        assert obj_from_dict.last_update_utc_date_time.isoformat() == (
            new_obj.last_update_utc_date_time.isoformat())
        assert obj_from_dict.tac_code_peek == (  # TacID
            new_obj.tac_code_peek)

    def test_from_json(self):
        """
        Test the `from_json` method of the CustomerSchema class.

        This method tests the deserialization of
        a JSON string to a
        Customer object.
        It converts the sample data to a JSON string,
        deserializes it to a dictionary,
        and then loads the dictionary to a Customer
        object. Finally, it asserts the
        equality of the deserialized
        Customer object
        with the sample data.

        Returns:
            None
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
        assert deserialized_data['insert_utc_date_time'].isoformat() == (
            self.sample_data['insert_utc_date_time'])
        assert str(deserialized_data[(  # TacID
            'tac_code_peek')]) == (
            str(self.sample_data['tac_code_peek']))
        assert deserialized_data['last_update_utc_date_time'].isoformat() == (
            self.sample_data['last_update_utc_date_time'])

        new_customer = Customer(
            **deserialized_data)

        assert isinstance(new_customer,
                          Customer)

    def test_to_json(
        self,
        new_obj: Customer
    ):
        """
        Test the conversion of a
        Customer instance to JSON.

        Args:
            customer (Customer): The
            Customer instance to convert.

        Raises:
            AssertionError: If the conversion fails or the
            converted JSON does not match the expected values.
        """

        # Convert the Customer instance
        # to JSON using the schema
        customer_schema = CustomerSchema()
        customer_dict = customer_schema.dump(
            new_obj)

        # Convert the customer_dict to JSON string
        customer_json = json.dumps(
            customer_dict)

        # Convert the JSON strings back to dictionaries
        dict_from_json = json.loads(
            customer_json)

        logging.info(
            "dict_from_json.keys() %s",
            dict_from_json.keys())

        logging.info("self.sample_data.keys() %s", self.sample_data.keys())

        # Verify the keys in both dictionaries match
        assert set(dict_from_json.keys()) == (
            set(self.sample_data.keys())), (
            f"Expected keys: {set(self.sample_data.keys())}, "
            f"Got: {set(dict_from_json.keys())}"
        )

        assert dict_from_json['code'] == \
            str(new_obj.code), (
            "failed on code"
        )
        assert dict_from_json['last_change_code'] == (
            new_obj.last_change_code), (
            "failed on last_change_code"
        )
        assert dict_from_json['insert_user_id'] == (
            str(new_obj.insert_user_id)), (
            "failed on insert_user_id"
        )
        assert dict_from_json['last_update_user_id'] == (
            str(new_obj.last_update_user_id)), (
            "failed on last_update_user_id"
        )
        assert dict_from_json['active_organization_id'] == (
            new_obj.active_organization_id), (
            "failed on active_organization_id"
        )
        assert dict_from_json['email'] == (
            new_obj.email), (
            "failed on email"
        )
        assert dict_from_json['email_confirmed_utc_date_time'] == (
            new_obj.email_confirmed_utc_date_time.isoformat()), (
            "failed on email_confirmed_utc_date_time"
        )
        assert dict_from_json['first_name'] == (
            new_obj.first_name), (
            "failed on first_name"
        )
        assert dict_from_json['forgot_password_key_expiration_utc_date_time'] == (
            new_obj.forgot_password_key_expiration_utc_date_time.isoformat()), (
            "failed on forgot_password_key_expiration_utc_date_time"
        )
        assert dict_from_json['forgot_password_key_value'] == (
            new_obj.forgot_password_key_value), (
            "failed on forgot_password_key_value"
        )
        assert dict_from_json['fs_user_code_value'] == (
            str(new_obj.fs_user_code_value)), (
            "failed on fs_user_code_value"
        )
        assert dict_from_json['is_active'] == (
            new_obj.is_active), (
            "failed on is_active"
        )
        assert dict_from_json['is_email_allowed'] == (
            new_obj.is_email_allowed), (
            "failed on is_email_allowed"
        )
        assert dict_from_json['is_email_confirmed'] == (
            new_obj.is_email_confirmed), (
            "failed on is_email_confirmed"
        )
        assert dict_from_json['is_email_marketing_allowed'] == (
            new_obj.is_email_marketing_allowed), (
            "failed on is_email_marketing_allowed"
        )
        assert dict_from_json['is_locked'] == (
            new_obj.is_locked), (
            "failed on is_locked"
        )
        assert dict_from_json['is_multiple_organizations_allowed'] == (
            new_obj.is_multiple_organizations_allowed), (
            "failed on is_multiple_organizations_allowed"
        )
        assert dict_from_json['is_verbose_logging_forced'] == (
            new_obj.is_verbose_logging_forced), (
            "failed on is_verbose_logging_forced"
        )
        assert dict_from_json['last_login_utc_date_time'] == (
            new_obj.last_login_utc_date_time.isoformat()), (
            "failed on last_login_utc_date_time"
        )
        assert dict_from_json['last_name'] == (
            new_obj.last_name), (
            "failed on last_name"
        )
        assert dict_from_json['password'] == (
            new_obj.password), (
            "failed on password"
        )
        assert dict_from_json['phone'] == (
            new_obj.phone), (
            "failed on phone"
        )
        assert dict_from_json['province'] == (
            new_obj.province), (
            "failed on province"
        )
        assert dict_from_json['registration_utc_date_time'] == (
            new_obj.registration_utc_date_time.isoformat()), (
            "failed on registration_utc_date_time"
        )
        assert dict_from_json['tac_id'] == (
            new_obj.tac_id), (
            "failed on tac_id"
        )
        assert dict_from_json['utc_offset_in_minutes'] == (
            new_obj.utc_offset_in_minutes), (
            "failed on utc_offset_in_minutes"
        )
        assert dict_from_json['zip'] == (
            new_obj.zip), (
            "failed on zip"
        )
        assert dict_from_json['insert_utc_date_time'] == (
            new_obj.insert_utc_date_time.isoformat()), (
            "failed on insert_utc_date_time"
        )
        assert dict_from_json['last_update_utc_date_time'] == (
            new_obj.last_update_utc_date_time.isoformat()), (
            "failed on last_update_utc_date_time"
        )
        assert dict_from_json[(  # TacID
            'tac_code_peek')] == (
            str(new_obj.tac_code_peek)), (
            "failed on tac_code_peek"
        )
