# models/serialization_schema/tests/pac_test.py  # pylint: disable=duplicate-code
# pylint: disable=redefined-outer-name, too-many-public-methods
# pylint: disable=unused-import

"""
This module contains tests for the
Pac serialization schema.

The Pac serialization schema
is responsible for serializing and deserializing
Pac instances. It ensures that the
data is properly formatted and can be
stored or retrieved from a database or
transmitted over a network.

The tests in this module cover the serialization
and deserialization of Pac
instances using the PacSchema
class. They verify
that the serialized data
matches the expected format and that the
deserialized data can be used to
reconstruct a Pac instance.

The PacSchema class
is used to define
the serialization and deserialization
rules for Pac instances. It
specifies how each attribute of a
Pac instance
should be converted to a serialized
format and how the serialized data should
be converted back to a Pac
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
from models import Pac
from models.factory import PacFactory
from models.serialization_schema import PacSchema
from services.logging_config import get_logger

logger = get_logger(__name__)


@pytest.fixture(scope="function")
def new_obj(
    session
) -> Pac:
    """
    Fixture to create and return a Pac
    instance using the
    PacFactory.

    Args:
        session: The database session.

    Returns:
        Pac: A newly created
            Pac instance.
    """

    return PacFactory.create(session=session)


class TestPacSchema:
    """
    Tests for the Pac
    serialization schema.
    """

    # Sample data for a Pac
    # instance
    sample_data = {
        "pac_id": 1,
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
        "insert_utc_date_time": datetime(
            2024, 1, 1, 12, 0, 0, tzinfo=pytz.utc
        ).isoformat(),
        "last_update_utc_date_time": datetime(
            2025, 1, 1, 12, 0, 0, tzinfo=pytz.utc
        ).isoformat(),
# endset  # noqa: E122

# endset  # noqa: E122
    }

    def test_pac_serialization(
        self,
        new_obj: Pac
    ):
        """
        Test the serialization of a
        Pac instance using
        PacSchema.

        Args:
            pac (Pac):
                A Pac instance to serialize.
        """

        schema = PacSchema()
        pac_data = schema.dump(new_obj)

        assert isinstance(pac_data, dict)

        result = pac_data

        assert result['code'] == str(new_obj.code)
        assert result['last_change_code'] == (
            new_obj.last_change_code)
        assert result['insert_user_id'] == (
            str(new_obj.insert_user_id))
        assert result['last_update_user_id'] == (
            str(new_obj.last_update_user_id))

        assert result['description'] == (
            new_obj.description)
        assert result['display_order'] == (
            new_obj.display_order)
        assert result['is_active'] == (
            new_obj.is_active)
        assert result['lookup_enum_name'] == (
            new_obj.lookup_enum_name)
        assert result['name'] == (
            new_obj.name)
        assert result['insert_utc_date_time'] == (
            new_obj.insert_utc_date_time.isoformat())
        assert result['last_update_utc_date_time'] == (
            new_obj.last_update_utc_date_time.isoformat())


    def test_pac_deserialization(
        self,
        new_obj: Pac
    ):
        """
        Test the deserialization of a
        Pac object using the
        PacSchema.

        Args:
            pac (Pac): The
                Pac object to be deserialized.

        Raises:
            AssertionError: If any of the assertions fail.

        Returns:
            None
        """

        schema = PacSchema()
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
        assert deserialized_data['description'] == (
            new_obj.description)
        assert deserialized_data['display_order'] == (
            new_obj.display_order)
        assert deserialized_data['is_active'] == (
            new_obj.is_active)
        assert deserialized_data['lookup_enum_name'] == (
            new_obj.lookup_enum_name)
        assert deserialized_data['name'] == (
            new_obj.name)
        assert deserialized_data['insert_utc_date_time'].isoformat() == (
            new_obj.insert_utc_date_time.isoformat())
        assert deserialized_data['last_update_utc_date_time'].isoformat() == (
            new_obj.last_update_utc_date_time.isoformat())


        obj_from_dict = Pac(
            **deserialized_data)

        assert isinstance(new_obj,
                          Pac)

        # Now compare the new_obj attributes with
        # the pac attributes
        assert obj_from_dict.code == \
            new_obj.code
        assert obj_from_dict.last_change_code == \
            new_obj.last_change_code
        assert obj_from_dict.insert_user_id == \
            new_obj.insert_user_id
        assert obj_from_dict.last_update_user_id == \
            new_obj.last_update_user_id
        assert obj_from_dict.description == (
            new_obj.description)
        assert obj_from_dict.display_order == (
            new_obj.display_order)
        assert obj_from_dict.is_active == (
            new_obj.is_active)
        assert obj_from_dict.lookup_enum_name == (
            new_obj.lookup_enum_name)
        assert obj_from_dict.name == (
            new_obj.name)

        assert obj_from_dict.insert_utc_date_time.isoformat() == (
            new_obj.insert_utc_date_time.isoformat())
        assert obj_from_dict.last_update_utc_date_time.isoformat() == (
            new_obj.last_update_utc_date_time.isoformat())


    def test_from_json(self):
        """
        Test the `from_json` method of the PacSchema class.

        This method tests the deserialization of
        a JSON string to a
        Pac object.
        It converts the sample data to a JSON string,
        deserializes it to a dictionary,
        and then loads the dictionary to a Pac
        object. Finally, it asserts the
        equality of the deserialized
        Pac object
        with the sample data.

        Returns:
            None
        """

        pac_schema = PacSchema()

        # Convert sample data to JSON string
        json_str = json.dumps(self.sample_data)

        # Deserialize the JSON string to a dictionary
        json_data = json.loads(json_str)

        # Load the dictionary to an object
        deserialized_data = pac_schema.load(json_data)

        assert str(deserialized_data['pac_id']) == (
            str(self.sample_data['pac_id']))
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
        assert deserialized_data['insert_utc_date_time'].isoformat() == (
            self.sample_data['insert_utc_date_time'])

        assert deserialized_data['last_update_utc_date_time'].isoformat() == (
            self.sample_data['last_update_utc_date_time'])

        new_pac = Pac(
            **deserialized_data)

        assert isinstance(new_pac,
                          Pac)

    def test_to_json(
        self,
        new_obj: Pac
    ):
        """
        Test the conversion of a
        Pac instance to JSON.

        Args:
            pac (Pac): The
            Pac instance to convert.

        Raises:
            AssertionError: If the conversion fails or the
            converted JSON does not match the expected values.
        """

        # Convert the Pac instance
        # to JSON using the schema
        pac_schema = PacSchema()
        pac_dict = pac_schema.dump(
            new_obj)

        # Convert the pac_dict to JSON string
        pac_json = json.dumps(
            pac_dict)

        # Convert the JSON strings back to dictionaries
        dict_from_json = json.loads(
            pac_json)

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
        assert dict_from_json['description'] == (
            new_obj.description), (
            "failed on description"
        )
        assert dict_from_json['display_order'] == (
            new_obj.display_order), (
            "failed on display_order"
        )
        assert dict_from_json['is_active'] == (
            new_obj.is_active), (
            "failed on is_active"
        )
        assert dict_from_json['lookup_enum_name'] == (
            new_obj.lookup_enum_name), (
            "failed on lookup_enum_name"
        )
        assert dict_from_json['name'] == (
            new_obj.name), (
            "failed on name"
        )
        assert dict_from_json['insert_utc_date_time'] == (
            new_obj.insert_utc_date_time.isoformat()), (
            "failed on insert_utc_date_time"
        )
        assert dict_from_json['last_update_utc_date_time'] == (
            new_obj.last_update_utc_date_time.isoformat()), (
            "failed on last_update_utc_date_time"
        )
