# tri_state_filter_test.py
# pylint: disable=redefined-outer-name

"""
This module contains tests for the
TriStateFilter serialization schema.

The TriStateFilter serialization schema
is responsible for serializing and deserializing
TriStateFilter instances. It ensures that the
data is properly formatted and can be
stored or retrieved from a database or
transmitted over a network.

The tests in this module cover the serialization
and deserialization of TriStateFilter
instances using the TriStateFilterSchema class. They verify
that the serialized data
matches the expected format and that the
deserialized data can be used to
reconstruct a TriStateFilter instance.

The TriStateFilterSchema class is used to define
the serialization and deserialization
rules for TriStateFilter instances. It
specifies how each attribute of a
TriStateFilter instance
should be converted to a serialized
format and how the serialized data should
be converted back to a TriStateFilter
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

from models import TriStateFilter
from models.factory import TriStateFilterFactory
from models.serialization_schema import TriStateFilterSchema
from services.logging_config import get_logger

logger = get_logger(__name__)


@pytest.fixture(scope="function")
def tri_state_filter(
    session
) -> TriStateFilter:
    """
    Fixture to create and return a TriStateFilter
    instance using the
    TriStateFilterFactory.

    Args:
        session: The database session.

    Returns:
        TriStateFilter: A newly created
            TriStateFilter instance.
    """

    return TriStateFilterFactory.create(session=session)


class TestTriStateFilterSchema:
    """
    Tests for the TriStateFilter
    serialization schema.
    """

    # Sample data for a TriStateFilter
    # instance
    sample_data = {
        "tri_state_filter_id": 1,
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
        "state_int_value": 42,
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

    def test_tri_state_filter_serialization(
        self,
        tri_state_filter: TriStateFilter
    ):
        """
        Test the serialization of a
        TriStateFilter instance using
        TriStateFilterSchema.

        Args:
            tri_state_filter (TriStateFilter):
                A TriStateFilter instance to serialize.
        """

        schema = TriStateFilterSchema()
        tri_state_filter_data = schema.dump(tri_state_filter)

        assert isinstance(tri_state_filter_data, dict)

        result = tri_state_filter_data

        assert result['code'] == str(tri_state_filter.code)
        assert result['last_change_code'] == (
            tri_state_filter.last_change_code)
        assert result['insert_user_id'] == (
            str(tri_state_filter.insert_user_id))
        assert result['last_update_user_id'] == (
            str(tri_state_filter.last_update_user_id))

        assert result['description'] == (
            tri_state_filter.description)
        assert result['display_order'] == (
            tri_state_filter.display_order)
        assert result['is_active'] == (
            tri_state_filter.is_active)
        assert result['lookup_enum_name'] == (
            tri_state_filter.lookup_enum_name)
        assert result['name'] == (
            tri_state_filter.name)
        assert result['pac_id'] == (
            tri_state_filter.pac_id)
        assert result['state_int_value'] == (
            tri_state_filter.state_int_value)
        assert result['insert_utc_date_time'] == (
            tri_state_filter.insert_utc_date_time.isoformat())
        assert result['last_update_utc_date_time'] == (
            tri_state_filter.last_update_utc_date_time.isoformat())
        assert result['pac_code_peek'] == (  # PacID
            str(tri_state_filter.pac_code_peek))

    def test_tri_state_filter_deserialization(
        self,
        tri_state_filter
    ):
        """
        Test the deserialization of a
        TriStateFilter object using the
        TriStateFilterSchema.

        Args:
            tri_state_filter (TriStateFilter): The
                TriStateFilter object to be deserialized.

        Raises:
            AssertionError: If any of the assertions fail.

        Returns:
            None
        """

        schema = TriStateFilterSchema()
        serialized_data = schema.dump(tri_state_filter)
        deserialized_data = schema.load(serialized_data)

        assert deserialized_data['code'] == \
            tri_state_filter.code
        assert deserialized_data['last_change_code'] == (
            tri_state_filter.last_change_code)
        assert deserialized_data['insert_user_id'] == (
            tri_state_filter.insert_user_id)
        assert deserialized_data['last_update_user_id'] == (
            tri_state_filter.last_update_user_id)
        assert deserialized_data['description'] == (
            tri_state_filter.description)
        assert deserialized_data['display_order'] == (
            tri_state_filter.display_order)
        assert deserialized_data['is_active'] == (
            tri_state_filter.is_active)
        assert deserialized_data['lookup_enum_name'] == (
            tri_state_filter.lookup_enum_name)
        assert deserialized_data['name'] == (
            tri_state_filter.name)
        assert deserialized_data['pac_id'] == (
            tri_state_filter.pac_id)
        assert deserialized_data['state_int_value'] == (
            tri_state_filter.state_int_value)
        assert deserialized_data['insert_utc_date_time'].isoformat() == (
            tri_state_filter.insert_utc_date_time.isoformat())
        assert deserialized_data['last_update_utc_date_time'].isoformat() == (
            tri_state_filter.last_update_utc_date_time.isoformat())
        assert deserialized_data[(  # PacID
            'pac_code_peek')] == (
            tri_state_filter.pac_code_peek)

        new_tri_state_filter = TriStateFilter(
            **deserialized_data)

        assert isinstance(new_tri_state_filter, TriStateFilter)

        # Now compare the new_tri_state_filter attributes with
        # the tri_state_filter attributes
        assert new_tri_state_filter.code == \
            tri_state_filter.code
        assert new_tri_state_filter.last_change_code == \
            tri_state_filter.last_change_code
        assert new_tri_state_filter.insert_user_id == \
            tri_state_filter.insert_user_id
        assert new_tri_state_filter.last_update_user_id == \
            tri_state_filter.last_update_user_id
        assert new_tri_state_filter.description == (
            tri_state_filter.description)
        assert new_tri_state_filter.display_order == (
            tri_state_filter.display_order)
        assert new_tri_state_filter.is_active == (
            tri_state_filter.is_active)
        assert new_tri_state_filter.lookup_enum_name == (
            tri_state_filter.lookup_enum_name)
        assert new_tri_state_filter.name == (
            tri_state_filter.name)
        assert new_tri_state_filter.pac_id == (
            tri_state_filter.pac_id)
        assert new_tri_state_filter.state_int_value == (
            tri_state_filter.state_int_value)

        assert new_tri_state_filter.insert_utc_date_time.isoformat() == (
            tri_state_filter.insert_utc_date_time.isoformat())
        assert new_tri_state_filter.last_update_utc_date_time.isoformat() == (
            tri_state_filter.last_update_utc_date_time.isoformat())
        assert new_tri_state_filter.pac_code_peek == (  # PacID
            tri_state_filter.pac_code_peek)

    def test_from_json(self):
        """
        Test the `from_json` method of the TriStateFilterSchema class.

        This method tests the deserialization of
        a JSON string to a
        TriStateFilter object.
        It converts the sample data to a JSON string,
        deserializes it to a dictionary,
        and then loads the dictionary to a TriStateFilter
        object. Finally, it asserts the
        equality of the deserialized
        TriStateFilter object
        with the sample data.

        Returns:
            None
        """

        tri_state_filter_schema = TriStateFilterSchema()

        # Convert sample data to JSON string
        json_str = json.dumps(self.sample_data)

        # Deserialize the JSON string to a dictionary
        json_data = json.loads(json_str)

        # Load the dictionary to an object
        deserialized_data = tri_state_filter_schema.load(json_data)

        assert str(deserialized_data['tri_state_filter_id']) == (
            str(self.sample_data['tri_state_filter_id']))
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
        assert str(deserialized_data['state_int_value']) == (
            str(self.sample_data['state_int_value']))
        assert deserialized_data['insert_utc_date_time'].isoformat() == (
            self.sample_data['insert_utc_date_time'])
        assert str(deserialized_data[(  # PacID
            'pac_code_peek')]) == (
            str(self.sample_data['pac_code_peek']))
        assert deserialized_data['last_update_utc_date_time'].isoformat() == (
            self.sample_data['last_update_utc_date_time'])

        new_tri_state_filter = TriStateFilter(
            **deserialized_data)

        assert isinstance(new_tri_state_filter, TriStateFilter)

    def test_to_json(
        self,
        tri_state_filter: TriStateFilter
    ):
        """
        Test the conversion of a
        TriStateFilter instance to JSON.

        Args:
            tri_state_filter (TriStateFilter): The
            TriStateFilter instance to convert.

        Raises:
            AssertionError: If the conversion fails or the
            converted JSON does not match the expected values.
        """

        # Convert the TriStateFilter instance
        # to JSON using the schema
        tri_state_filter_schema = TriStateFilterSchema()
        tri_state_filter_dict = tri_state_filter_schema.dump(
            tri_state_filter)

        # Convert the tri_state_filter_dict to JSON string
        tri_state_filter_json = json.dumps(
            tri_state_filter_dict)

        # Convert the JSON strings back to dictionaries
        tri_state_filter_dict_from_json = json.loads(
            tri_state_filter_json)
        # sample_dict_from_json = json.loads(self.sample_data)

        logging.info(
            "tri_state_filter_dict_from_json.keys() %s",
            tri_state_filter_dict_from_json.keys())

        logging.info("self.sample_data.keys() %s", self.sample_data.keys())

        # Verify the keys in both dictionaries match
        assert set(tri_state_filter_dict_from_json.keys()) == (
            set(self.sample_data.keys())), (
            f"Expected keys: {set(self.sample_data.keys())}, "
            f"Got: {set(tri_state_filter_dict_from_json.keys())}"
        )

        assert tri_state_filter_dict_from_json['code'] == \
            str(tri_state_filter.code), (
            "failed on code"
        )
        assert tri_state_filter_dict_from_json['last_change_code'] == (
            tri_state_filter.last_change_code), (
            "failed on last_change_code"
        )
        assert tri_state_filter_dict_from_json['insert_user_id'] == (
            str(tri_state_filter.insert_user_id)), (
            "failed on insert_user_id"
        )
        assert tri_state_filter_dict_from_json['last_update_user_id'] == (
            str(tri_state_filter.last_update_user_id)), (
            "failed on last_update_user_id"
        )
        assert tri_state_filter_dict_from_json['description'] == (
            tri_state_filter.description), (
            "failed on description"
        )
        assert tri_state_filter_dict_from_json['display_order'] == (
            tri_state_filter.display_order), (
            "failed on display_order"
        )
        assert tri_state_filter_dict_from_json['is_active'] == (
            tri_state_filter.is_active), (
            "failed on is_active"
        )
        assert tri_state_filter_dict_from_json['lookup_enum_name'] == (
            tri_state_filter.lookup_enum_name), (
            "failed on lookup_enum_name"
        )
        assert tri_state_filter_dict_from_json['name'] == (
            tri_state_filter.name), (
            "failed on name"
        )
        assert tri_state_filter_dict_from_json['pac_id'] == (
            tri_state_filter.pac_id), (
            "failed on pac_id"
        )
        assert tri_state_filter_dict_from_json['state_int_value'] == (
            tri_state_filter.state_int_value), (
            "failed on state_int_value"
        )
        assert tri_state_filter_dict_from_json['insert_utc_date_time'] == (
            tri_state_filter.insert_utc_date_time.isoformat()), (
            "failed on insert_utc_date_time"
        )
        assert tri_state_filter_dict_from_json['last_update_utc_date_time'] == (
            tri_state_filter.last_update_utc_date_time.isoformat()), (
            "failed on last_update_utc_date_time"
        )
        assert tri_state_filter_dict_from_json[(  # PacID
            'pac_code_peek')] == (
            str(tri_state_filter.pac_code_peek)), (
            "failed on pac_code_peek"
        )

