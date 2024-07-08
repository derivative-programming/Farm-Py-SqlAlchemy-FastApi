# models/serialization_schema/tests/org_api_key_test.py  # pylint: disable=duplicate-code
# pylint: disable=redefined-outer-name, too-many-public-methods
# pylint: disable=unused-import

"""
This module contains tests for the
OrgApiKey serialization schema.

The OrgApiKey serialization schema
is responsible for serializing and deserializing
OrgApiKey instances. It ensures that the
data is properly formatted and can be
stored or retrieved from a database or
transmitted over a network.

The tests in this module cover the serialization
and deserialization of OrgApiKey
instances using the OrgApiKeySchema
class. They verify
that the serialized data
matches the expected format and that the
deserialized data can be used to
reconstruct a OrgApiKey instance.

The OrgApiKeySchema class
is used to define
the serialization and deserialization
rules for OrgApiKey instances. It
specifies how each attribute of a
OrgApiKey instance
should be converted to a serialized
format and how the serialized data should
be converted back to a OrgApiKey
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
from models import OrgApiKey
from models.factory import OrgApiKeyFactory
from models.serialization_schema import OrgApiKeySchema
from services.logging_config import get_logger

logger = get_logger(__name__)


@pytest.fixture(scope="function")
def new_obj(
    session
) -> OrgApiKey:
    """
    Fixture to create and return a OrgApiKey
    instance using the
    OrgApiKeyFactory.

    Args:
        session: The database session.

    Returns:
        OrgApiKey: A newly created
            OrgApiKey instance.
    """

    return OrgApiKeyFactory.create(session=session)


class TestOrgApiKeySchema:
    """
    Tests for the OrgApiKey
    serialization schema.
    """

    # Sample data for a OrgApiKey
    # instance
    sample_data = {
        "org_api_key_id": 1,
        "code":
            "a1b2c3d4-e5f6-7a8b-9c0d-123456789012",
        "last_change_code": 0,
        "insert_user_id":
            "a1b2c3d4-e5f6-7a8b-9c0d-123456789012",
        "last_update_user_id":
            "a1b2c3d4-e5f6-7a8b-9c0d-123456789012",
# endset  # noqa: E122
        "api_key_value": "Vanilla",
        "created_by": "Vanilla",
        "created_utc_date_time": datetime(
            2023, 1, 1, 12, 0, 0, tzinfo=pytz.utc
        ).isoformat(),
        "expiration_utc_date_time": datetime(
            2023, 1, 1, 12, 0, 0, tzinfo=pytz.utc
        ).isoformat(),
        "is_active": False,
        "is_temp_user_key": False,
        "name": "Vanilla",
        "organization_id": 2,
        "org_customer_id": 1,
        "insert_utc_date_time": datetime(
            2024, 1, 1, 12, 0, 0, tzinfo=pytz.utc
        ).isoformat(),
        "last_update_utc_date_time": datetime(
            2025, 1, 1, 12, 0, 0, tzinfo=pytz.utc
        ).isoformat(),
# endset  # noqa: E122
        "organization_code_peek":  # OrganizationID
            "a1b2c3d4-e5f6-7a8b-9c0d-123456789012",
        "org_customer_code_peek":  # OrgCustomerID
            "a1b2c3d4-e5f6-7a8b-9c0d-123456789012",
# endset  # noqa: E122
    }

    def test_org_api_key_serialization(
        self,
        new_obj: OrgApiKey
    ):
        """
        Test the serialization of a
        OrgApiKey instance using
        OrgApiKeySchema.

        Args:
            org_api_key (OrgApiKey):
                A OrgApiKey instance to serialize.
        """

        schema = OrgApiKeySchema()
        org_api_key_data = schema.dump(new_obj)

        assert isinstance(org_api_key_data, dict)

        result = org_api_key_data

        assert result['code'] == str(new_obj.code)
        assert result['last_change_code'] == (
            new_obj.last_change_code)
        assert result['insert_user_id'] == (
            str(new_obj.insert_user_id))
        assert result['last_update_user_id'] == (
            str(new_obj.last_update_user_id))

        assert result['api_key_value'] == (
            new_obj.api_key_value)
        assert result['created_by'] == (
            new_obj.created_by)
        assert result['created_utc_date_time'] == (
            new_obj.created_utc_date_time.isoformat())
        assert result['expiration_utc_date_time'] == (
            new_obj.expiration_utc_date_time.isoformat())
        assert result['is_active'] == (
            new_obj.is_active)
        assert result['is_temp_user_key'] == (
            new_obj.is_temp_user_key)
        assert result['name'] == (
            new_obj.name)
        assert result['organization_id'] == (
            new_obj.organization_id)
        assert result['org_customer_id'] == (
            new_obj.org_customer_id)
        assert result['insert_utc_date_time'] == (
            new_obj.insert_utc_date_time.isoformat())
        assert result['last_update_utc_date_time'] == (
            new_obj.last_update_utc_date_time.isoformat())
        assert result['organization_code_peek'] == (  # OrganizationID
            str(new_obj.organization_code_peek))
        assert result['org_customer_code_peek'] == (  # OrgCustomerID
            str(new_obj.org_customer_code_peek))

    def test_org_api_key_deserialization(
        self,
        new_obj: OrgApiKey
    ):
        """
        Test the deserialization of a
        OrgApiKey object using the
        OrgApiKeySchema.

        Args:
            org_api_key (OrgApiKey): The
                OrgApiKey object to be deserialized.

        Raises:
            AssertionError: If any of the assertions fail.

        Returns:
            None
        """

        schema = OrgApiKeySchema()
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
        assert deserialized_data['api_key_value'] == (
            new_obj.api_key_value)
        assert deserialized_data['created_by'] == (
            new_obj.created_by)
        assert deserialized_data['created_utc_date_time'].isoformat() == (
            new_obj.created_utc_date_time.isoformat())
        assert deserialized_data['expiration_utc_date_time'].isoformat() == (
            new_obj.expiration_utc_date_time.isoformat())
        assert deserialized_data['is_active'] == (
            new_obj.is_active)
        assert deserialized_data['is_temp_user_key'] == (
            new_obj.is_temp_user_key)
        assert deserialized_data['name'] == (
            new_obj.name)
        assert deserialized_data['organization_id'] == (
            new_obj.organization_id)
        assert deserialized_data['org_customer_id'] == (
            new_obj.org_customer_id)
        assert deserialized_data['insert_utc_date_time'].isoformat() == (
            new_obj.insert_utc_date_time.isoformat())
        assert deserialized_data['last_update_utc_date_time'].isoformat() == (
            new_obj.last_update_utc_date_time.isoformat())
        assert deserialized_data[(  # OrganizationID
            'organization_code_peek')] == (
            new_obj.organization_code_peek)
        assert deserialized_data[(  # OrgCustomerID
            'org_customer_code_peek')] == (
            new_obj.org_customer_code_peek)

        obj_from_dict = OrgApiKey(
            **deserialized_data)

        assert isinstance(new_obj,
                          OrgApiKey)

        # Now compare the new_obj attributes with
        # the org_api_key attributes
        assert obj_from_dict.code == \
            new_obj.code
        assert obj_from_dict.last_change_code == \
            new_obj.last_change_code
        assert obj_from_dict.insert_user_id == \
            new_obj.insert_user_id
        assert obj_from_dict.last_update_user_id == \
            new_obj.last_update_user_id
        assert obj_from_dict.api_key_value == (
            new_obj.api_key_value)
        assert obj_from_dict.created_by == (
            new_obj.created_by)
        assert obj_from_dict.created_utc_date_time.isoformat() == (
            new_obj.created_utc_date_time.isoformat())
        assert obj_from_dict.expiration_utc_date_time.isoformat() == (
            new_obj.expiration_utc_date_time.isoformat())
        assert obj_from_dict.is_active == (
            new_obj.is_active)
        assert obj_from_dict.is_temp_user_key == (
            new_obj.is_temp_user_key)
        assert obj_from_dict.name == (
            new_obj.name)
        assert obj_from_dict.organization_id == (
            new_obj.organization_id)
        assert obj_from_dict.org_customer_id == (
            new_obj.org_customer_id)

        assert obj_from_dict.insert_utc_date_time.isoformat() == (
            new_obj.insert_utc_date_time.isoformat())
        assert obj_from_dict.last_update_utc_date_time.isoformat() == (
            new_obj.last_update_utc_date_time.isoformat())
        assert obj_from_dict.organization_code_peek == (  # OrganizationID
            new_obj.organization_code_peek)
        assert obj_from_dict.org_customer_code_peek == (  # OrgCustomerID
            new_obj.org_customer_code_peek)

    def test_from_json(self):
        """
        Test the `from_json` method of the OrgApiKeySchema class.

        This method tests the deserialization of
        a JSON string to a
        OrgApiKey object.
        It converts the sample data to a JSON string,
        deserializes it to a dictionary,
        and then loads the dictionary to a OrgApiKey
        object. Finally, it asserts the
        equality of the deserialized
        OrgApiKey object
        with the sample data.

        Returns:
            None
        """

        org_api_key_schema = OrgApiKeySchema()

        # Convert sample data to JSON string
        json_str = json.dumps(self.sample_data)

        # Deserialize the JSON string to a dictionary
        json_data = json.loads(json_str)

        # Load the dictionary to an object
        deserialized_data = org_api_key_schema.load(json_data)

        assert str(deserialized_data['org_api_key_id']) == (
            str(self.sample_data['org_api_key_id']))
        assert str(deserialized_data['code']) == (
            str(self.sample_data['code']))
        assert str(deserialized_data['last_change_code']) == (
            str(self.sample_data['last_change_code']))
        assert str(deserialized_data['insert_user_id']) == (
            str(self.sample_data['insert_user_id']))
        assert str(deserialized_data['last_update_user_id']) == (
            str(self.sample_data['last_update_user_id']))
        assert str(deserialized_data['api_key_value']) == (
            str(self.sample_data['api_key_value']))
        assert str(deserialized_data['created_by']) == (
            str(self.sample_data['created_by']))
        assert deserialized_data['created_utc_date_time'].isoformat() == (
            self.sample_data['created_utc_date_time'])
        assert deserialized_data['expiration_utc_date_time'].isoformat() == (
            self.sample_data['expiration_utc_date_time'])
        assert str(deserialized_data['is_active']) == (
            str(self.sample_data['is_active']))
        assert str(deserialized_data['is_temp_user_key']) == (
            str(self.sample_data['is_temp_user_key']))
        assert str(deserialized_data['name']) == (
            str(self.sample_data['name']))
        assert str(deserialized_data['organization_id']) == (
            str(self.sample_data['organization_id']))
        assert str(deserialized_data['org_customer_id']) == (
            str(self.sample_data['org_customer_id']))
        assert deserialized_data['insert_utc_date_time'].isoformat() == (
            self.sample_data['insert_utc_date_time'])
        assert str(deserialized_data[(  # OrganizationID
            'organization_code_peek')]) == (
            str(self.sample_data['organization_code_peek']))
        assert str(deserialized_data[(  # OrgCustomerID
            'org_customer_code_peek')]) == (
            str(self.sample_data['org_customer_code_peek']))
        assert deserialized_data['last_update_utc_date_time'].isoformat() == (
            self.sample_data['last_update_utc_date_time'])

        new_org_api_key = OrgApiKey(
            **deserialized_data)

        assert isinstance(new_org_api_key,
                          OrgApiKey)

    def test_to_json(
        self,
        new_obj: OrgApiKey
    ):
        """
        Test the conversion of a
        OrgApiKey instance to JSON.

        Args:
            org_api_key (OrgApiKey): The
            OrgApiKey instance to convert.

        Raises:
            AssertionError: If the conversion fails or the
            converted JSON does not match the expected values.
        """

        # Convert the OrgApiKey instance
        # to JSON using the schema
        org_api_key_schema = OrgApiKeySchema()
        org_api_key_dict = org_api_key_schema.dump(
            new_obj)

        # Convert the org_api_key_dict to JSON string
        org_api_key_json = json.dumps(
            org_api_key_dict)

        # Convert the JSON strings back to dictionaries
        dict_from_json = json.loads(
            org_api_key_json)

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
        assert dict_from_json['api_key_value'] == (
            new_obj.api_key_value), (
            "failed on api_key_value"
        )
        assert dict_from_json['created_by'] == (
            new_obj.created_by), (
            "failed on created_by"
        )
        assert dict_from_json['created_utc_date_time'] == (
            new_obj.created_utc_date_time.isoformat()), (
            "failed on created_utc_date_time"
        )
        assert dict_from_json['expiration_utc_date_time'] == (
            new_obj.expiration_utc_date_time.isoformat()), (
            "failed on expiration_utc_date_time"
        )
        assert dict_from_json['is_active'] == (
            new_obj.is_active), (
            "failed on is_active"
        )
        assert dict_from_json['is_temp_user_key'] == (
            new_obj.is_temp_user_key), (
            "failed on is_temp_user_key"
        )
        assert dict_from_json['name'] == (
            new_obj.name), (
            "failed on name"
        )
        assert dict_from_json['organization_id'] == (
            new_obj.organization_id), (
            "failed on organization_id"
        )
        assert dict_from_json['org_customer_id'] == (
            new_obj.org_customer_id), (
            "failed on org_customer_id"
        )
        assert dict_from_json['insert_utc_date_time'] == (
            new_obj.insert_utc_date_time.isoformat()), (
            "failed on insert_utc_date_time"
        )
        assert dict_from_json['last_update_utc_date_time'] == (
            new_obj.last_update_utc_date_time.isoformat()), (
            "failed on last_update_utc_date_time"
        )
        assert dict_from_json[(  # OrganizationID
            'organization_code_peek')] == (
            str(new_obj.organization_code_peek)), (
            "failed on organization_code_peek"
        )
        assert dict_from_json[(  # OrgCustomerID
            'org_customer_code_peek')] == (
            str(new_obj.org_customer_code_peek)), (
            "failed on org_customer_code_peek"
        )
