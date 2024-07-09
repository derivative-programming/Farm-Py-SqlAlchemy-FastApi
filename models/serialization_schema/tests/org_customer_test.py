# models/serialization_schema/tests/org_customer_test.py  # pylint: disable=duplicate-code # noqa: E501
# pylint: disable=redefined-outer-name, too-many-public-methods
# pylint: disable=unused-import

"""
This module contains tests for the
OrgCustomer serialization schema.

The OrgCustomer serialization schema
is responsible for serializing and deserializing
OrgCustomer instances. It ensures that the
data is properly formatted and can be
stored or retrieved from a database or
transmitted over a network.

The tests in this module cover the serialization
and deserialization of OrgCustomer
instances using the OrgCustomerSchema
class. They verify
that the serialized data
matches the expected format and that the
deserialized data can be used to
reconstruct a OrgCustomer instance.

The OrgCustomerSchema class
is used to define
the serialization and deserialization
rules for OrgCustomer instances. It
specifies how each attribute of a
OrgCustomer instance
should be converted to a serialized
format and how the serialized data should
be converted back to a OrgCustomer
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
from models import OrgCustomer
from models.factory import OrgCustomerFactory
from models.serialization_schema import OrgCustomerSchema
from services.logging_config import get_logger

logger = get_logger(__name__)


@pytest.fixture(scope="function")
def new_obj(
    session
) -> OrgCustomer:
    """
    Fixture to create and return a OrgCustomer
    instance using the
    OrgCustomerFactory.

    Args:
        session: The database session.

    Returns:
        OrgCustomer: A newly created
            OrgCustomer instance.
    """

    return OrgCustomerFactory.create(session=session)


class TestOrgCustomerSchema:
    """
    Tests for the OrgCustomer
    serialization schema.
    """

    # Sample data for a OrgCustomer
    # instance
    sample_data = {
        "org_customer_id": 1,
        "code":
            "a1b2c3d4-e5f6-7a8b-9c0d-123456789012",
        "last_change_code": 0,
        "insert_user_id":
            "a1b2c3d4-e5f6-7a8b-9c0d-123456789012",
        "last_update_user_id":
            "a1b2c3d4-e5f6-7a8b-9c0d-123456789012",
# endset  # noqa: E122
        "customer_id": 1,
        "email": "test@email.com",
        "organization_id": 2,
        "insert_utc_date_time": datetime(
            2024, 1, 1, 12, 0, 0, tzinfo=pytz.utc
        ).isoformat(),
        "last_update_utc_date_time": datetime(
            2025, 1, 1, 12, 0, 0, tzinfo=pytz.utc
        ).isoformat(),
# endset  # noqa: E122
        "customer_code_peek":  # CustomerID
            "a1b2c3d4-e5f6-7a8b-9c0d-123456789012",
        "organization_code_peek":  # OrganizationID
            "a1b2c3d4-e5f6-7a8b-9c0d-123456789012",
# endset  # noqa: E122
    }

    def test_org_customer_serialization(
        self,
        new_obj: OrgCustomer
    ):
        """
        Test the serialization of a
        OrgCustomer instance using
        OrgCustomerSchema.

        Args:
            org_customer (OrgCustomer):
                A OrgCustomer instance to serialize.
        """

        schema = OrgCustomerSchema()
        org_customer_data = schema.dump(new_obj)

        assert isinstance(org_customer_data, dict)

        result = org_customer_data

        assert result['code'] == str(new_obj.code)
        assert result['last_change_code'] == (
            new_obj.last_change_code)
        assert result['insert_user_id'] == (
            str(new_obj.insert_user_id))
        assert result['last_update_user_id'] == (
            str(new_obj.last_update_user_id))

        assert result['customer_id'] == (
            new_obj.customer_id)
        assert result['email'] == (
            new_obj.email)
        assert result['organization_id'] == (
            new_obj.organization_id)
        assert result['insert_utc_date_time'] == (
            new_obj.insert_utc_date_time.isoformat())
        assert result['last_update_utc_date_time'] == (
            new_obj.last_update_utc_date_time.isoformat())
        assert result['customer_code_peek'] == (  # CustomerID
            str(new_obj.customer_code_peek))
        assert result['organization_code_peek'] == (  # OrganizationID
            str(new_obj.organization_code_peek))

    def test_org_customer_deserialization(
        self,
        new_obj: OrgCustomer
    ):
        """
        Test the deserialization of a
        OrgCustomer object using the
        OrgCustomerSchema.

        Args:
            org_customer (OrgCustomer): The
                OrgCustomer object to be deserialized.

        Raises:
            AssertionError: If any of the assertions fail.

        Returns:
            None
        """

        schema = OrgCustomerSchema()
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
        assert deserialized_data['email'] == (
            new_obj.email)
        assert deserialized_data['organization_id'] == (
            new_obj.organization_id)
        assert deserialized_data['insert_utc_date_time'].isoformat() == (
            new_obj.insert_utc_date_time.isoformat())
        assert deserialized_data['last_update_utc_date_time'].isoformat() == (
            new_obj.last_update_utc_date_time.isoformat())
        assert deserialized_data[(  # CustomerID
            'customer_code_peek')] == (
            new_obj.customer_code_peek)
        assert deserialized_data[(  # OrganizationID
            'organization_code_peek')] == (
            new_obj.organization_code_peek)

        obj_from_dict = OrgCustomer(
            **deserialized_data)

        assert isinstance(new_obj,
                          OrgCustomer)

        # Now compare the new_obj attributes with
        # the org_customer attributes
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
        assert obj_from_dict.email == (
            new_obj.email)
        assert obj_from_dict.organization_id == (
            new_obj.organization_id)

        assert obj_from_dict.insert_utc_date_time.isoformat() == (
            new_obj.insert_utc_date_time.isoformat())
        assert obj_from_dict.last_update_utc_date_time.isoformat() == (
            new_obj.last_update_utc_date_time.isoformat())
        assert obj_from_dict.customer_code_peek == (  # CustomerID
            new_obj.customer_code_peek)
        assert obj_from_dict.organization_code_peek == (  # OrganizationID
            new_obj.organization_code_peek)

    def test_from_json(self):
        """
        Test the `from_json` method of the OrgCustomerSchema class.

        This method tests the deserialization of
        a JSON string to a
        OrgCustomer object.
        It converts the sample data to a JSON string,
        deserializes it to a dictionary,
        and then loads the dictionary to a OrgCustomer
        object. Finally, it asserts the
        equality of the deserialized
        OrgCustomer object
        with the sample data.

        Returns:
            None
        """

        org_customer_schema = OrgCustomerSchema()

        # Convert sample data to JSON string
        json_str = json.dumps(self.sample_data)

        # Deserialize the JSON string to a dictionary
        json_data = json.loads(json_str)

        # Load the dictionary to an object
        deserialized_data = org_customer_schema.load(json_data)

        assert str(deserialized_data['org_customer_id']) == (
            str(self.sample_data['org_customer_id']))
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
        assert str(deserialized_data['email']) == (
            str(self.sample_data['email']))
        assert str(deserialized_data['organization_id']) == (
            str(self.sample_data['organization_id']))
        assert deserialized_data['insert_utc_date_time'].isoformat() == (
            self.sample_data['insert_utc_date_time'])
        assert str(deserialized_data[(  # CustomerID
            'customer_code_peek')]) == (
            str(self.sample_data['customer_code_peek']))
        assert str(deserialized_data[(  # OrganizationID
            'organization_code_peek')]) == (
            str(self.sample_data['organization_code_peek']))
        assert deserialized_data['last_update_utc_date_time'].isoformat() == (
            self.sample_data['last_update_utc_date_time'])

        new_org_customer = OrgCustomer(
            **deserialized_data)

        assert isinstance(new_org_customer,
                          OrgCustomer)

    def test_to_json(
        self,
        new_obj: OrgCustomer
    ):
        """
        Test the conversion of a
        OrgCustomer instance to JSON.

        Args:
            org_customer (OrgCustomer): The
            OrgCustomer instance to convert.

        Raises:
            AssertionError: If the conversion fails or the
            converted JSON does not match the expected values.
        """

        # Convert the OrgCustomer instance
        # to JSON using the schema
        org_customer_schema = OrgCustomerSchema()
        org_customer_dict = org_customer_schema.dump(
            new_obj)

        # Convert the org_customer_dict to JSON string
        org_customer_json = json.dumps(
            org_customer_dict)

        # Convert the JSON strings back to dictionaries
        dict_from_json = json.loads(
            org_customer_json)

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
        assert dict_from_json['email'] == (
            new_obj.email), (
            "failed on email"
        )
        assert dict_from_json['organization_id'] == (
            new_obj.organization_id), (
            "failed on organization_id"
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
        assert dict_from_json[(  # OrganizationID
            'organization_code_peek')] == (
            str(new_obj.organization_code_peek)), (
            "failed on organization_code_peek"
        )
