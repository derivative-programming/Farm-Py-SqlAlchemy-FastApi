# customer_role_test.py
# pylint: disable=redefined-outer-name

"""
This module contains tests for the
CustomerRole serialization schema.

The CustomerRole serialization schema
is responsible for serializing and deserializing
CustomerRole instances. It ensures that the
data is properly formatted and can be
stored or retrieved from a database or
transmitted over a network.

The tests in this module cover the serialization
and deserialization of CustomerRole
instances using the CustomerRoleSchema class. They verify
that the serialized data
matches the expected format and that the
deserialized data can be used to
reconstruct a CustomerRole instance.

The CustomerRoleSchema class is used to define
the serialization and deserialization
rules for CustomerRole instances. It
specifies how each attribute of a
CustomerRole instance
should be converted to a serialized
format and how the serialized data should
be converted back to a CustomerRole
instance.

The tests in this module use the pytest
framework to define test cases and
assertions. They ensure that the serialization
and deserialization process
works correctly and produces the expected results.

"""

import json
import logging
from datetime import datetime
from decimal import Decimal

import pytest
import pytz

from models import CustomerRole
from models.factory import CustomerRoleFactory
from models.serialization_schema import CustomerRoleSchema
from services.logging_config import get_logger

logger = get_logger(__name__)


@pytest.fixture(scope="function")
def customer_role(
    session
) -> CustomerRole:
    """
    Fixture to create and return a CustomerRole
    instance using the
    CustomerRoleFactory.

    Args:
        session: The database session.

    Returns:
        CustomerRole: A newly created
            CustomerRole instance.
    """

    return CustomerRoleFactory.create(session=session)


class TestCustomerRoleSchema:
    """
    Tests for the CustomerRole
    serialization schema.
    """

    # Sample data for a CustomerRole
    # instance
    sample_data = {
        "customer_role_id": 1,
        "code":
            "a1b2c3d4-e5f6-7a8b-9c0d-123456789012",
        "last_change_code": 0,
        "insert_user_id":
            "a1b2c3d4-e5f6-7a8b-9c0d-123456789012",
        "last_update_user_id":
            "a1b2c3d4-e5f6-7a8b-9c0d-123456789012",
# endset  # noqa: E122
        "customer_id": 2,
        "is_placeholder": False,
        "placeholder": False,
        "role_id": 1,
        "insert_utc_date_time": datetime(
            2024, 1, 1, 12, 0, 0, tzinfo=pytz.utc
        ).isoformat(),
        "last_update_utc_date_time": datetime(
            2025, 1, 1, 12, 0, 0, tzinfo=pytz.utc
        ).isoformat(),
# endset  # noqa: E122
        "customer_code_peek":  # CustomerID
            "a1b2c3d4-e5f6-7a8b-9c0d-123456789012",
        "role_code_peek":  # RoleID
            "a1b2c3d4-e5f6-7a8b-9c0d-123456789012",
# endset  # noqa: E122
    }

    def test_customer_role_serialization(
        self,
        customer_role: CustomerRole
    ):
        """
        Test the serialization of a
        CustomerRole instance using
        CustomerRoleSchema.

        Args:
            customer_role (CustomerRole):
                A CustomerRole instance to serialize.
        """

        schema = CustomerRoleSchema()
        customer_role_data = schema.dump(customer_role)

        assert isinstance(customer_role_data, dict)

        result = customer_role_data

        assert result['code'] == str(customer_role.code)
        assert result['last_change_code'] == (
            customer_role.last_change_code)
        assert result['insert_user_id'] == (
            str(customer_role.insert_user_id))
        assert result['last_update_user_id'] == (
            str(customer_role.last_update_user_id))

        assert result['customer_id'] == (
            customer_role.customer_id)
        assert result['is_placeholder'] == (
            customer_role.is_placeholder)
        assert result['placeholder'] == (
            customer_role.placeholder)
        assert result['role_id'] == (
            customer_role.role_id)
        assert result['insert_utc_date_time'] == (
            customer_role.insert_utc_date_time.isoformat())
        assert result['last_update_utc_date_time'] == (
            customer_role.last_update_utc_date_time.isoformat())
        assert result['customer_code_peek'] == (  # CustomerID
            str(customer_role.customer_code_peek))
        assert result['role_code_peek'] == (  # RoleID
            str(customer_role.role_code_peek))

    def test_customer_role_deserialization(self, customer_role):
        """
        Test the deserialization of a
        CustomerRole object using the
        CustomerRoleSchema.

        Args:
            customer_role (CustomerRole): The
                CustomerRole object to be deserialized.

        Raises:
            AssertionError: If any of the assertions fail.

        Returns:
            None
        """

        schema = CustomerRoleSchema()
        serialized_data = schema.dump(customer_role)
        deserialized_data = schema.load(serialized_data)

        assert deserialized_data['code'] == \
            customer_role.code
        assert deserialized_data['last_change_code'] == (
            customer_role.last_change_code)
        assert deserialized_data['insert_user_id'] == (
            customer_role.insert_user_id)
        assert deserialized_data['last_update_user_id'] == (
            customer_role.last_update_user_id)
        assert deserialized_data['customer_id'] == (
            customer_role.customer_id)
        assert deserialized_data['is_placeholder'] == (
            customer_role.is_placeholder)
        assert deserialized_data['placeholder'] == (
            customer_role.placeholder)
        assert deserialized_data['role_id'] == (
            customer_role.role_id)
        assert deserialized_data['insert_utc_date_time'].isoformat() == (
            customer_role.insert_utc_date_time.isoformat())
        assert deserialized_data['last_update_utc_date_time'].isoformat() == (
            customer_role.last_update_utc_date_time.isoformat())
        assert deserialized_data[(  # CustomerID
            'customer_code_peek')] == (
            customer_role.customer_code_peek)
        assert deserialized_data[(  # RoleID
            'role_code_peek')] == (
            customer_role.role_code_peek)

        new_customer_role = CustomerRole(**deserialized_data)

        assert isinstance(new_customer_role, CustomerRole)

        # Now compare the new_customer_role attributes with
        # the customer_role attributes
        assert new_customer_role.code == \
            customer_role.code
        assert new_customer_role.last_change_code == \
            customer_role.last_change_code
        assert new_customer_role.insert_user_id == \
            customer_role.insert_user_id
        assert new_customer_role.last_update_user_id == \
            customer_role.last_update_user_id
        assert new_customer_role.customer_id == (
            customer_role.customer_id)
        assert new_customer_role.is_placeholder == (
            customer_role.is_placeholder)
        assert new_customer_role.placeholder == (
            customer_role.placeholder)
        assert new_customer_role.role_id == (
            customer_role.role_id)

        assert new_customer_role.insert_utc_date_time.isoformat() == (
            customer_role.insert_utc_date_time.isoformat())
        assert new_customer_role.last_update_utc_date_time.isoformat() == (
            customer_role.last_update_utc_date_time.isoformat())
        assert new_customer_role.customer_code_peek == (  # CustomerID
            customer_role.customer_code_peek)
        assert new_customer_role.role_code_peek == (  # RoleID
            customer_role.role_code_peek)

    def test_from_json(self):
        """
        Test the `from_json` method of the CustomerRoleSchema class.

        This method tests the deserialization of
        a JSON string to a
        CustomerRole object.
        It converts the sample data to a JSON string,
        deserializes it to a dictionary,
        and then loads the dictionary to a CustomerRole
        object. Finally, it asserts the
        equality of the deserialized
        CustomerRole object
        with the sample data.

        Returns:
            None
        """

        customer_role_schema = CustomerRoleSchema()

        # Convert sample data to JSON string
        json_str = json.dumps(self.sample_data)

        # Deserialize the JSON string to a dictionary
        json_data = json.loads(json_str)

        # Load the dictionary to an object
        deserialized_data = customer_role_schema.load(json_data)

        assert str(deserialized_data['customer_role_id']) == (
            str(self.sample_data['customer_role_id']))
        assert str(deserialized_data['code']) == (
            str(self.sample_data['code']))
        assert str(deserialized_data['last_change_code']) == (
            str(self.sample_data['last_change_code']))
        assert str(deserialized_data['insert_user_id']) == (
            str(self.sample_data['insert_user_id']))
        assert str(deserialized_data['last_update_user_id']) == (
            str(self.sample_data['last_update_user_id']))
        assert str(deserialized_data['customer_id']) == (
            str(self.sample_data['customer_id']))
        assert str(deserialized_data['is_placeholder']) == (
            str(self.sample_data['is_placeholder']))
        assert str(deserialized_data['placeholder']) == (
            str(self.sample_data['placeholder']))
        assert str(deserialized_data['role_id']) == (
            str(self.sample_data['role_id']))
        assert deserialized_data['insert_utc_date_time'].isoformat() == (
            self.sample_data['insert_utc_date_time'])
        assert str(deserialized_data[(  # CustomerID
            'customer_code_peek')]) == (
            str(self.sample_data['customer_code_peek']))
        assert str(deserialized_data[(  # RoleID
            'role_code_peek')]) == (
            str(self.sample_data['role_code_peek']))
        assert deserialized_data['last_update_utc_date_time'].isoformat() == (
            self.sample_data['last_update_utc_date_time'])

        new_customer_role = CustomerRole(**deserialized_data)

        assert isinstance(new_customer_role, CustomerRole)

    def test_to_json(
        self,
        customer_role: CustomerRole
    ):
        """
        Test the conversion of a
        CustomerRole instance to JSON.

        Args:
            customer_role (CustomerRole): The
            CustomerRole instance to convert.

        Raises:
            AssertionError: If the conversion fails or the
            converted JSON does not match the expected values.
        """

        # Convert the CustomerRole instance
        # to JSON using the schema
        customer_role_schema = CustomerRoleSchema()
        customer_role_dict = customer_role_schema.dump(
            customer_role)

        # Convert the customer_role_dict to JSON string
        customer_role_json = json.dumps(
            customer_role_dict)

        # Convert the JSON strings back to dictionaries
        customer_role_dict_from_json = json.loads(
            customer_role_json)
        # sample_dict_from_json = json.loads(self.sample_data)

        logging.info(
            "customer_role_dict_from_json.keys() %s",
            customer_role_dict_from_json.keys())

        logging.info("self.sample_data.keys() %s", self.sample_data.keys())

        # Verify the keys in both dictionaries match
        assert set(customer_role_dict_from_json.keys()) == (
            set(self.sample_data.keys())), (
            f"Expected keys: {set(self.sample_data.keys())}, "
            f"Got: {set(customer_role_dict_from_json.keys())}"
        )

        assert customer_role_dict_from_json['code'] == \
            str(customer_role.code), (
            "failed on code"
        )
        assert customer_role_dict_from_json['last_change_code'] == (
            customer_role.last_change_code), (
            "failed on last_change_code"
        )
        assert customer_role_dict_from_json['insert_user_id'] == (
            str(customer_role.insert_user_id)), (
            "failed on insert_user_id"
        )
        assert customer_role_dict_from_json['last_update_user_id'] == (
            str(customer_role.last_update_user_id)), (
            "failed on last_update_user_id"
        )
        assert customer_role_dict_from_json['customer_id'] == (
            customer_role.customer_id), (
            "failed on customer_id"
        )
        assert customer_role_dict_from_json['is_placeholder'] == (
            customer_role.is_placeholder), (
            "failed on is_placeholder"
        )
        assert customer_role_dict_from_json['placeholder'] == (
            customer_role.placeholder), (
            "failed on placeholder"
        )
        assert customer_role_dict_from_json['role_id'] == (
            customer_role.role_id), (
            "failed on role_id"
        )
        assert customer_role_dict_from_json['insert_utc_date_time'] == (
            customer_role.insert_utc_date_time.isoformat()), (
            "failed on insert_utc_date_time"
        )
        assert customer_role_dict_from_json['last_update_utc_date_time'] == (
            customer_role.last_update_utc_date_time.isoformat()), (
            "failed on last_update_utc_date_time"
        )
        assert customer_role_dict_from_json[(  # CustomerID
            'customer_code_peek')] == (
            str(customer_role.customer_code_peek)), (
            "failed on customer_code_peek"
        )
        assert customer_role_dict_from_json[(  # RoleID
            'role_code_peek')] == (
            str(customer_role.role_code_peek)), (
            "failed on role_code_peek"
        )

