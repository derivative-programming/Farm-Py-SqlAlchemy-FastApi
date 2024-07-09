# models/serialization_schema/tests/organization_test.py  # pylint: disable=duplicate-code # noqa: E501
# pylint: disable=redefined-outer-name, too-many-public-methods
# pylint: disable=unused-import

"""
This module contains tests for the
Organization serialization schema.

The Organization serialization schema
is responsible for serializing and deserializing
Organization instances. It ensures that the
data is properly formatted and can be
stored or retrieved from a database or
transmitted over a network.

The tests in this module cover the serialization
and deserialization of Organization
instances using the OrganizationSchema
class. They verify
that the serialized data
matches the expected format and that the
deserialized data can be used to
reconstruct a Organization instance.

The OrganizationSchema class
is used to define
the serialization and deserialization
rules for Organization instances. It
specifies how each attribute of a
Organization instance
should be converted to a serialized
format and how the serialized data should
be converted back to a Organization
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
from models import Organization
from models.factory import OrganizationFactory
from models.serialization_schema import OrganizationSchema
from services.logging_config import get_logger

logger = get_logger(__name__)


@pytest.fixture(scope="function")
def new_obj(
    session
) -> Organization:
    """
    Fixture to create and return a Organization
    instance using the
    OrganizationFactory.

    Args:
        session: The database session.

    Returns:
        Organization: A newly created
            Organization instance.
    """

    return OrganizationFactory.create(session=session)


class TestOrganizationSchema:
    """
    Tests for the Organization
    serialization schema.
    """

    # Sample data for a Organization
    # instance
    sample_data = {
        "organization_id": 1,
        "code":
            "a1b2c3d4-e5f6-7a8b-9c0d-123456789012",
        "last_change_code": 0,
        "insert_user_id":
            "a1b2c3d4-e5f6-7a8b-9c0d-123456789012",
        "last_update_user_id":
            "a1b2c3d4-e5f6-7a8b-9c0d-123456789012",
# endset  # noqa: E122
        "name": "Vanilla",
        "tac_id": 2,
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

    def test_organization_serialization(
        self,
        new_obj: Organization
    ):
        """
        Test the serialization of a
        Organization instance using
        OrganizationSchema.

        Args:
            organization (Organization):
                A Organization instance to serialize.
        """

        schema = OrganizationSchema()
        organization_data = schema.dump(new_obj)

        assert isinstance(organization_data, dict)

        result = organization_data

        assert result['code'] == str(new_obj.code)
        assert result['last_change_code'] == (
            new_obj.last_change_code)
        assert result['insert_user_id'] == (
            str(new_obj.insert_user_id))
        assert result['last_update_user_id'] == (
            str(new_obj.last_update_user_id))

        assert result['name'] == (
            new_obj.name)
        assert result['tac_id'] == (
            new_obj.tac_id)
        assert result['insert_utc_date_time'] == (
            new_obj.insert_utc_date_time.isoformat())
        assert result['last_update_utc_date_time'] == (
            new_obj.last_update_utc_date_time.isoformat())
        assert result['tac_code_peek'] == (  # TacID
            str(new_obj.tac_code_peek))

    def test_organization_deserialization(
        self,
        new_obj: Organization
    ):
        """
        Test the deserialization of a
        Organization object using the
        OrganizationSchema.

        Args:
            organization (Organization): The
                Organization object to be deserialized.

        Raises:
            AssertionError: If any of the assertions fail.

        Returns:
            None
        """

        schema = OrganizationSchema()
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
        assert deserialized_data['name'] == (
            new_obj.name)
        assert deserialized_data['tac_id'] == (
            new_obj.tac_id)
        assert deserialized_data['insert_utc_date_time'].isoformat() == (
            new_obj.insert_utc_date_time.isoformat())
        assert deserialized_data['last_update_utc_date_time'].isoformat() == (
            new_obj.last_update_utc_date_time.isoformat())
        assert deserialized_data[(  # TacID
            'tac_code_peek')] == (
            new_obj.tac_code_peek)

        obj_from_dict = Organization(
            **deserialized_data)

        assert isinstance(new_obj,
                          Organization)

        # Now compare the new_obj attributes with
        # the organization attributes
        assert obj_from_dict.code == \
            new_obj.code
        assert obj_from_dict.last_change_code == \
            new_obj.last_change_code
        assert obj_from_dict.insert_user_id == \
            new_obj.insert_user_id
        assert obj_from_dict.last_update_user_id == \
            new_obj.last_update_user_id
        assert obj_from_dict.name == (
            new_obj.name)
        assert obj_from_dict.tac_id == (
            new_obj.tac_id)

        assert obj_from_dict.insert_utc_date_time.isoformat() == (
            new_obj.insert_utc_date_time.isoformat())
        assert obj_from_dict.last_update_utc_date_time.isoformat() == (
            new_obj.last_update_utc_date_time.isoformat())
        assert obj_from_dict.tac_code_peek == (  # TacID
            new_obj.tac_code_peek)

    def test_from_json(self):
        """
        Test the `from_json` method of the OrganizationSchema class.

        This method tests the deserialization of
        a JSON string to a
        Organization object.
        It converts the sample data to a JSON string,
        deserializes it to a dictionary,
        and then loads the dictionary to a Organization
        object. Finally, it asserts the
        equality of the deserialized
        Organization object
        with the sample data.

        Returns:
            None
        """

        organization_schema = OrganizationSchema()

        # Convert sample data to JSON string
        json_str = json.dumps(self.sample_data)

        # Deserialize the JSON string to a dictionary
        json_data = json.loads(json_str)

        # Load the dictionary to an object
        deserialized_data = organization_schema.load(json_data)

        assert str(deserialized_data['organization_id']) == (
            str(self.sample_data['organization_id']))
        assert str(deserialized_data['code']) == (
            str(self.sample_data['code']))
        assert str(deserialized_data['last_change_code']) == (
            str(self.sample_data['last_change_code']))
        assert str(deserialized_data['insert_user_id']) == (
            str(self.sample_data['insert_user_id']))
        assert str(deserialized_data['last_update_user_id']) == (
            str(self.sample_data['last_update_user_id']))
        assert str(deserialized_data['name']) == (
            str(self.sample_data['name']))
        assert str(deserialized_data['tac_id']) == (
            str(self.sample_data['tac_id']))
        assert deserialized_data['insert_utc_date_time'].isoformat() == (
            self.sample_data['insert_utc_date_time'])
        assert str(deserialized_data[(  # TacID
            'tac_code_peek')]) == (
            str(self.sample_data['tac_code_peek']))
        assert deserialized_data['last_update_utc_date_time'].isoformat() == (
            self.sample_data['last_update_utc_date_time'])

        new_organization = Organization(
            **deserialized_data)

        assert isinstance(new_organization,
                          Organization)

    def test_to_json(
        self,
        new_obj: Organization
    ):
        """
        Test the conversion of a
        Organization instance to JSON.

        Args:
            organization (Organization): The
            Organization instance to convert.

        Raises:
            AssertionError: If the conversion fails or the
            converted JSON does not match the expected values.
        """

        # Convert the Organization instance
        # to JSON using the schema
        organization_schema = OrganizationSchema()
        organization_dict = organization_schema.dump(
            new_obj)

        # Convert the organization_dict to JSON string
        organization_json = json.dumps(
            organization_dict)

        # Convert the JSON strings back to dictionaries
        dict_from_json = json.loads(
            organization_json)

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
        assert dict_from_json['name'] == (
            new_obj.name), (
            "failed on name"
        )
        assert dict_from_json['tac_id'] == (
            new_obj.tac_id), (
            "failed on tac_id"
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
