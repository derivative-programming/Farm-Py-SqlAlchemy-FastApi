# models/serialization_schema/tests/customer_role_test.py  # pylint: disable=duplicate-code # noqa: E501
# pylint: disable=redefined-outer-name, too-many-public-methods
# pylint: disable=unused-import

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
instances using the CustomerRoleSchema
class. They verify
that the serialized data
matches the expected format and that the
deserialized data can be used to
reconstruct a CustomerRole instance.

The CustomerRoleSchema class
is used to define
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
from datetime import datetime  # noqa: F401
from decimal import Decimal  # noqa: F401

import pytz

import pytest
from models import CustomerRole
from models.factory import CustomerRoleFactory
from models.serialization_schema import CustomerRoleSchema
from services.logging_config import get_logger

logger = get_logger(__name__)


@pytest.fixture(scope="function")
def new_obj(
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
        new_obj: CustomerRole
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
        customer_role_data = schema.dump(new_obj)

        assert isinstance(customer_role_data, dict)

        result = customer_role_data

        assert result['code'] == str(new_obj.code)
        assert result['last_change_code'] == (
            new_obj.last_change_code)
        assert result['insert_user_id'] == (
            str(new_obj.insert_user_id))
        assert result['last_update_user_id'] == (
            str(new_obj.last_update_user_id))

        assert result['customer_id'] == (
            new_obj.customer_id)
        assert result['is_placeholder'] == (
            new_obj.is_placeholder)
        assert result['placeholder'] == (
            new_obj.placeholder)
        assert result['role_id'] == (
            new_obj.role_id)
        assert result['insert_utc_date_time'] == (
            new_obj.insert_utc_date_time.isoformat())
        assert result['last_update_utc_date_time'] == (
            new_obj.last_update_utc_date_time.isoformat())
        assert result['customer_code_peek'] == (  # CustomerID
            str(new_obj.customer_code_peek))
        assert result['role_code_peek'] == (  # RoleID
            str(new_obj.role_code_peek))

    def test_customer_role_deserialization(
        self,
        new_obj: CustomerRole
    ):
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
        assert deserialized_data['customer_id'] == (
            new_obj.customer_id)
        assert deserialized_data['is_placeholder'] == (
            new_obj.is_placeholder)
        assert deserialized_data['placeholder'] == (
            new_obj.placeholder)
        assert deserialized_data['role_id'] == (
            new_obj.role_id)
        assert deserialized_data['insert_utc_date_time'].isoformat() == (
            new_obj.insert_utc_date_time.isoformat())
        assert deserialized_data['last_update_utc_date_time'].isoformat() == (
            new_obj.last_update_utc_date_time.isoformat())
        assert deserialized_data[(  # CustomerID
            'customer_code_peek')] == (
            new_obj.customer_code_peek)
        assert deserialized_data[(  # RoleID
            'role_code_peek')] == (
            new_obj.role_code_peek)

        obj_from_dict = CustomerRole(
            **deserialized_data)

        assert isinstance(new_obj,
                          CustomerRole)

        # Now compare the new_obj attributes with
        # the customer_role attributes
        assert obj_from_dict.code == \
            new_obj.code
        assert obj_from_dict.last_change_code == \
            new_obj.last_change_code
        assert obj_from_dict.insert_user_id == \
            new_obj.insert_user_id
        assert obj_from_dict.last_update_user_id == \
            new_obj.last_update_user_id
        assert obj_from_dict.customer_id == (
            new_obj.customer_id)
        assert obj_from_dict.is_placeholder == (
            new_obj.is_placeholder)
        assert obj_from_dict.placeholder == (
            new_obj.placeholder)
        assert obj_from_dict.role_id == (
            new_obj.role_id)

        assert obj_from_dict.insert_utc_date_time.isoformat() == (
            new_obj.insert_utc_date_time.isoformat())
        assert obj_from_dict.last_update_utc_date_time.isoformat() == (
            new_obj.last_update_utc_date_time.isoformat())
        assert obj_from_dict.customer_code_peek == (  # CustomerID
            new_obj.customer_code_peek)
        assert obj_from_dict.role_code_peek == (  # RoleID
            new_obj.role_code_peek)

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

        new_customer_role = CustomerRole(
            **deserialized_data)

        assert isinstance(new_customer_role,
                          CustomerRole)

    def test_to_json(
        self,
        new_obj: CustomerRole
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
            new_obj)

        # Convert the customer_role_dict to JSON string
        customer_role_json = json.dumps(
            customer_role_dict)

        # Convert the JSON strings back to dictionaries
        dict_from_json = json.loads(
            customer_role_json)

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
        assert dict_from_json['customer_id'] == (
            new_obj.customer_id), (
            "failed on customer_id"
        )
        assert dict_from_json['is_placeholder'] == (
            new_obj.is_placeholder), (
            "failed on is_placeholder"
        )
        assert dict_from_json['placeholder'] == (
            new_obj.placeholder), (
            "failed on placeholder"
        )
        assert dict_from_json['role_id'] == (
            new_obj.role_id), (
            "failed on role_id"
        )
        assert dict_from_json['insert_utc_date_time'] == (
            new_obj.insert_utc_date_time.isoformat()), (
            "failed on insert_utc_date_time"
        )
        assert dict_from_json['last_update_utc_date_time'] == (
            new_obj.last_update_utc_date_time.isoformat()), (
            "failed on last_update_utc_date_time"
        )
        assert dict_from_json[(  # CustomerID
            'customer_code_peek')] == (
            str(new_obj.customer_code_peek)), (
            "failed on customer_code_peek"
        )
        assert dict_from_json[(  # RoleID
            'role_code_peek')] == (
            str(new_obj.role_code_peek)), (
            "failed on role_code_peek"
        )
