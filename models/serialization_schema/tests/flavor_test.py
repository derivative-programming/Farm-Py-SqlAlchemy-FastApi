# flavor_test.py
# pylint: disable=redefined-outer-name

"""
This module contains tests for the
Flavor serialization schema.

The Flavor serialization schema
is responsible for serializing and deserializing
Flavor instances. It ensures that the
data is properly formatted and can be
stored or retrieved from a database or
transmitted over a network.

The tests in this module cover the serialization
and deserialization of Flavor
instances using the FlavorSchema class. They verify
that the serialized data
matches the expected format and that the
deserialized data can be used to
reconstruct a Flavor instance.

The FlavorSchema class is used to define
the serialization and deserialization
rules for Flavor instances. It
specifies how each attribute of a
Flavor instance
should be converted to a serialized
format and how the serialized data should
be converted back to a Flavor
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

from models import Flavor
from models.factory import FlavorFactory
from models.serialization_schema import FlavorSchema
from services.logging_config import get_logger

logger = get_logger(__name__)


@pytest.fixture(scope="function")
def flavor(
    session
) -> Flavor:
    """
    Fixture to create and return a Flavor
    instance using the
    FlavorFactory.

    Args:
        session: The database session.

    Returns:
        Flavor: A newly created
            Flavor instance.
    """

    return FlavorFactory.create(session=session)


class TestFlavorSchema:
    """
    Tests for the Flavor
    serialization schema.
    """

    # Sample data for a Flavor
    # instance
    sample_data = {
        "flavor_id": 1,
        "code":
            "a1b2c3d4-e5f6-7a8b-9c0d-123456789012",
        "last_change_code": 0,
        "insert_user_id":
            "a1b2c3d4-e5f6-7a8b-9c0d-123456789012",
        "last_update_user_id":
            "a1b2c3d4-e5f6-7a8b-9c0d-123456789012",
# endset  # noqa: E122
        "description": "Vanilla",
        "display_order": 42,
        "is_active": False,
        "lookup_enum_name": "Vanilla",
        "name": "Vanilla",
        "pac_id": 2,
        "insert_utc_date_time": datetime(
            2024, 1, 1, 12, 0, 0, tzinfo=pytz.utc
        ).isoformat(),
        "last_update_utc_date_time": datetime(
            2025, 1, 1, 12, 0, 0, tzinfo=pytz.utc
        ).isoformat(),
# endset  # noqa: E122
        "pac_code_peek":  # PacID
            "a1b2c3d4-e5f6-7a8b-9c0d-123456789012",
# endset  # noqa: E122
    }

    def test_flavor_serialization(
        self,
        flavor: Flavor
    ):
        """
        Test the serialization of a
        Flavor instance using
        FlavorSchema.

        Args:
            flavor (Flavor):
                A Flavor instance to serialize.
        """

        schema = FlavorSchema()
        flavor_data = schema.dump(flavor)

        assert isinstance(flavor_data, dict)

        result = flavor_data

        assert result['code'] == str(flavor.code)
        assert result['last_change_code'] == (
            flavor.last_change_code)
        assert result['insert_user_id'] == (
            str(flavor.insert_user_id))
        assert result['last_update_user_id'] == (
            str(flavor.last_update_user_id))

        assert result['description'] == (
            flavor.description)
        assert result['display_order'] == (
            flavor.display_order)
        assert result['is_active'] == (
            flavor.is_active)
        assert result['lookup_enum_name'] == (
            flavor.lookup_enum_name)
        assert result['name'] == (
            flavor.name)
        assert result['pac_id'] == (
            flavor.pac_id)
        assert result['insert_utc_date_time'] == (
            flavor.insert_utc_date_time.isoformat())
        assert result['last_update_utc_date_time'] == (
            flavor.last_update_utc_date_time.isoformat())
        assert result['pac_code_peek'] == (  # PacID
            str(flavor.pac_code_peek))

    def test_flavor_deserialization(
        self,
        flavor
    ):
        """
        Test the deserialization of a
        Flavor object using the
        FlavorSchema.

        Args:
            flavor (Flavor): The
                Flavor object to be deserialized.

        Raises:
            AssertionError: If any of the assertions fail.

        Returns:
            None
        """

        schema = FlavorSchema()
        serialized_data = schema.dump(flavor)
        deserialized_data = schema.load(serialized_data)

        assert deserialized_data['code'] == \
            flavor.code
        assert deserialized_data['last_change_code'] == (
            flavor.last_change_code)
        assert deserialized_data['insert_user_id'] == (
            flavor.insert_user_id)
        assert deserialized_data['last_update_user_id'] == (
            flavor.last_update_user_id)
        assert deserialized_data['description'] == (
            flavor.description)
        assert deserialized_data['display_order'] == (
            flavor.display_order)
        assert deserialized_data['is_active'] == (
            flavor.is_active)
        assert deserialized_data['lookup_enum_name'] == (
            flavor.lookup_enum_name)
        assert deserialized_data['name'] == (
            flavor.name)
        assert deserialized_data['pac_id'] == (
            flavor.pac_id)
        assert deserialized_data['insert_utc_date_time'].isoformat() == (
            flavor.insert_utc_date_time.isoformat())
        assert deserialized_data['last_update_utc_date_time'].isoformat() == (
            flavor.last_update_utc_date_time.isoformat())
        assert deserialized_data[(  # PacID
            'pac_code_peek')] == (
            flavor.pac_code_peek)

        new_flavor = Flavor(
            **deserialized_data)

        assert isinstance(new_flavor, Flavor)

        # Now compare the new_flavor attributes with
        # the flavor attributes
        assert new_flavor.code == \
            flavor.code
        assert new_flavor.last_change_code == \
            flavor.last_change_code
        assert new_flavor.insert_user_id == \
            flavor.insert_user_id
        assert new_flavor.last_update_user_id == \
            flavor.last_update_user_id
        assert new_flavor.description == (
            flavor.description)
        assert new_flavor.display_order == (
            flavor.display_order)
        assert new_flavor.is_active == (
            flavor.is_active)
        assert new_flavor.lookup_enum_name == (
            flavor.lookup_enum_name)
        assert new_flavor.name == (
            flavor.name)
        assert new_flavor.pac_id == (
            flavor.pac_id)

        assert new_flavor.insert_utc_date_time.isoformat() == (
            flavor.insert_utc_date_time.isoformat())
        assert new_flavor.last_update_utc_date_time.isoformat() == (
            flavor.last_update_utc_date_time.isoformat())
        assert new_flavor.pac_code_peek == (  # PacID
            flavor.pac_code_peek)

    def test_from_json(self):
        """
        Test the `from_json` method of the FlavorSchema class.

        This method tests the deserialization of
        a JSON string to a
        Flavor object.
        It converts the sample data to a JSON string,
        deserializes it to a dictionary,
        and then loads the dictionary to a Flavor
        object. Finally, it asserts the
        equality of the deserialized
        Flavor object
        with the sample data.

        Returns:
            None
        """

        flavor_schema = FlavorSchema()

        # Convert sample data to JSON string
        json_str = json.dumps(self.sample_data)

        # Deserialize the JSON string to a dictionary
        json_data = json.loads(json_str)

        # Load the dictionary to an object
        deserialized_data = flavor_schema.load(json_data)

        assert str(deserialized_data['flavor_id']) == (
            str(self.sample_data['flavor_id']))
        assert str(deserialized_data['code']) == (
            str(self.sample_data['code']))
        assert str(deserialized_data['last_change_code']) == (
            str(self.sample_data['last_change_code']))
        assert str(deserialized_data['insert_user_id']) == (
            str(self.sample_data['insert_user_id']))
        assert str(deserialized_data['last_update_user_id']) == (
            str(self.sample_data['last_update_user_id']))
        assert str(deserialized_data['description']) == (
            str(self.sample_data['description']))
        assert str(deserialized_data['display_order']) == (
            str(self.sample_data['display_order']))
        assert str(deserialized_data['is_active']) == (
            str(self.sample_data['is_active']))
        assert str(deserialized_data['lookup_enum_name']) == (
            str(self.sample_data['lookup_enum_name']))
        assert str(deserialized_data['name']) == (
            str(self.sample_data['name']))
        assert str(deserialized_data['pac_id']) == (
            str(self.sample_data['pac_id']))
        assert deserialized_data['insert_utc_date_time'].isoformat() == (
            self.sample_data['insert_utc_date_time'])
        assert str(deserialized_data[(  # PacID
            'pac_code_peek')]) == (
            str(self.sample_data['pac_code_peek']))
        assert deserialized_data['last_update_utc_date_time'].isoformat() == (
            self.sample_data['last_update_utc_date_time'])

        new_flavor = Flavor(
            **deserialized_data)

        assert isinstance(new_flavor, Flavor)

    def test_to_json(
        self,
        flavor: Flavor
    ):
        """
        Test the conversion of a
        Flavor instance to JSON.

        Args:
            flavor (Flavor): The
            Flavor instance to convert.

        Raises:
            AssertionError: If the conversion fails or the
            converted JSON does not match the expected values.
        """

        # Convert the Flavor instance
        # to JSON using the schema
        flavor_schema = FlavorSchema()
        flavor_dict = flavor_schema.dump(
            flavor)

        # Convert the flavor_dict to JSON string
        flavor_json = json.dumps(
            flavor_dict)

        # Convert the JSON strings back to dictionaries
        flavor_dict_from_json = json.loads(
            flavor_json)
        # sample_dict_from_json = json.loads(self.sample_data)

        logging.info(
            "flavor_dict_from_json.keys() %s",
            flavor_dict_from_json.keys())

        logging.info("self.sample_data.keys() %s", self.sample_data.keys())

        # Verify the keys in both dictionaries match
        assert set(flavor_dict_from_json.keys()) == (
            set(self.sample_data.keys())), (
            f"Expected keys: {set(self.sample_data.keys())}, "
            f"Got: {set(flavor_dict_from_json.keys())}"
        )

        assert flavor_dict_from_json['code'] == \
            str(flavor.code), (
            "failed on code"
        )
        assert flavor_dict_from_json['last_change_code'] == (
            flavor.last_change_code), (
            "failed on last_change_code"
        )
        assert flavor_dict_from_json['insert_user_id'] == (
            str(flavor.insert_user_id)), (
            "failed on insert_user_id"
        )
        assert flavor_dict_from_json['last_update_user_id'] == (
            str(flavor.last_update_user_id)), (
            "failed on last_update_user_id"
        )
        assert flavor_dict_from_json['description'] == (
            flavor.description), (
            "failed on description"
        )
        assert flavor_dict_from_json['display_order'] == (
            flavor.display_order), (
            "failed on display_order"
        )
        assert flavor_dict_from_json['is_active'] == (
            flavor.is_active), (
            "failed on is_active"
        )
        assert flavor_dict_from_json['lookup_enum_name'] == (
            flavor.lookup_enum_name), (
            "failed on lookup_enum_name"
        )
        assert flavor_dict_from_json['name'] == (
            flavor.name), (
            "failed on name"
        )
        assert flavor_dict_from_json['pac_id'] == (
            flavor.pac_id), (
            "failed on pac_id"
        )
        assert flavor_dict_from_json['insert_utc_date_time'] == (
            flavor.insert_utc_date_time.isoformat()), (
            "failed on insert_utc_date_time"
        )
        assert flavor_dict_from_json['last_update_utc_date_time'] == (
            flavor.last_update_utc_date_time.isoformat()), (
            "failed on last_update_utc_date_time"
        )
        assert flavor_dict_from_json[(  # PacID
            'pac_code_peek')] == (
            str(flavor.pac_code_peek)), (
            "failed on pac_code_peek"
        )

