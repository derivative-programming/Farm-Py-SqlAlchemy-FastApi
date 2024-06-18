# date_greater_than_filter_test.py
# pylint: disable=redefined-outer-name
"""
    #TODO add comment
"""
import json
import logging
from datetime import datetime
from decimal import Decimal
from typing import Any, Dict
import pytest
import pytz
from models import DateGreaterThanFilter
from models.factory import DateGreaterThanFilterFactory
from models.serialization_schema import DateGreaterThanFilterSchema
from services.logging_config import get_logger
logger = get_logger(__name__)
@pytest.fixture(scope="function")
def date_greater_than_filter(session) -> DateGreaterThanFilter:
    """
    Fixture to create and return a DateGreaterThanFilter instance using the DateGreaterThanFilterFactory.
    Args:
        session: The database session.
    Returns:
        DateGreaterThanFilter: A newly created DateGreaterThanFilter instance.
    """
    return DateGreaterThanFilterFactory.create(session=session)
class TestDateGreaterThanFilterSchema:
    """
    Tests for the DateGreaterThanFilter serialization schema.
    """
    # Sample data for a DateGreaterThanFilter instance
    sample_data = {
        "date_greater_than_filter_id": 1,
        "code":
            "a1b2c3d4-e5f6-7a8b-9c0d-123456789012",
        "last_change_code": 0,
        "insert_user_id":
            "a1b2c3d4-e5f6-7a8b-9c0d-123456789012",
        "last_update_user_id":
            "a1b2c3d4-e5f6-7a8b-9c0d-123456789012",
# endset  # noqa: E122
        "day_count": 42,
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
    def test_date_greater_than_filter_serialization(self, date_greater_than_filter: DateGreaterThanFilter):
        """
        Test the serialization of a DateGreaterThanFilter instance using
        DateGreaterThanFilterSchema.
        Args:
            date_greater_than_filter (DateGreaterThanFilter):
                A DateGreaterThanFilter instance to serialize.
        """
        schema = DateGreaterThanFilterSchema()
        result: Dict[str, Any] = schema.dump(date_greater_than_filter)
        assert result['code'] == str(date_greater_than_filter.code)
        assert result['last_change_code'] == (
            date_greater_than_filter.last_change_code)
        assert result['insert_user_id'] == (
            str(date_greater_than_filter.insert_user_id))
        assert result['last_update_user_id'] == (
            str(date_greater_than_filter.last_update_user_id))
# endset
        assert result['day_count'] == (
            date_greater_than_filter.day_count)
        assert result['description'] == (
            date_greater_than_filter.description)
        assert result['display_order'] == (
            date_greater_than_filter.display_order)
        assert result['is_active'] == (
            date_greater_than_filter.is_active)
        assert result['lookup_enum_name'] == (
            date_greater_than_filter.lookup_enum_name)
        assert result['name'] == (
            date_greater_than_filter.name)
        assert result['pac_id'] == (
            date_greater_than_filter.pac_id)
# endset
        assert result['insert_utc_date_time'] == (
            date_greater_than_filter.insert_utc_date_time.isoformat())
        assert result['last_update_utc_date_time'] == (
            date_greater_than_filter.last_update_utc_date_time.isoformat())
# endset
        assert result['pac_code_peek'] == (  # PacID
            str(date_greater_than_filter.pac_code_peek))
# endset
    def test_date_greater_than_filter_deserialization(self, date_greater_than_filter):
        """
            #TODO add comment
        """
        schema = DateGreaterThanFilterSchema()
        serialized_data = schema.dump(date_greater_than_filter)
        deserialized_data = schema.load(serialized_data)
        assert deserialized_data['code'] == date_greater_than_filter.code
        assert deserialized_data['last_change_code'] == (
            date_greater_than_filter.last_change_code)
        assert deserialized_data['insert_user_id'] == (
            date_greater_than_filter.insert_user_id)
        assert deserialized_data['last_update_user_id'] == (
            date_greater_than_filter.last_update_user_id)
# endset
        assert deserialized_data['day_count'] == (
            date_greater_than_filter.day_count)
        assert deserialized_data['description'] == (
            date_greater_than_filter.description)
        assert deserialized_data['display_order'] == (
            date_greater_than_filter.display_order)
        assert deserialized_data['is_active'] == (
            date_greater_than_filter.is_active)
        assert deserialized_data['lookup_enum_name'] == (
            date_greater_than_filter.lookup_enum_name)
        assert deserialized_data['name'] == (
            date_greater_than_filter.name)
        assert deserialized_data['pac_id'] == (
            date_greater_than_filter.pac_id)
# endset
        assert deserialized_data['insert_utc_date_time'].isoformat() == (
            date_greater_than_filter.insert_utc_date_time.isoformat())
        assert deserialized_data['last_update_utc_date_time'].isoformat() == (
            date_greater_than_filter.last_update_utc_date_time.isoformat())
# endset
        assert deserialized_data['pac_code_peek'] == (  # PacID
            date_greater_than_filter.pac_code_peek)
# endset
        new_date_greater_than_filter = DateGreaterThanFilter(**deserialized_data)
        assert isinstance(new_date_greater_than_filter, DateGreaterThanFilter)
        # Now compare the new_date_greater_than_filter attributes with the date_greater_than_filter attributes
        assert new_date_greater_than_filter.code == date_greater_than_filter.code
        assert new_date_greater_than_filter.last_change_code == date_greater_than_filter.last_change_code
        assert new_date_greater_than_filter.insert_user_id == date_greater_than_filter.insert_user_id
        assert new_date_greater_than_filter.last_update_user_id == date_greater_than_filter.last_update_user_id
# endset
        assert new_date_greater_than_filter.day_count == (
            date_greater_than_filter.day_count)
        assert new_date_greater_than_filter.description == (
            date_greater_than_filter.description)
        assert new_date_greater_than_filter.display_order == (
            date_greater_than_filter.display_order)
        assert new_date_greater_than_filter.is_active == (
            date_greater_than_filter.is_active)
        assert new_date_greater_than_filter.lookup_enum_name == (
            date_greater_than_filter.lookup_enum_name)
        assert new_date_greater_than_filter.name == (
            date_greater_than_filter.name)
        assert new_date_greater_than_filter.pac_id == (
            date_greater_than_filter.pac_id)
# endset
        assert new_date_greater_than_filter.insert_utc_date_time.isoformat() == (
            date_greater_than_filter.insert_utc_date_time.isoformat())
        assert new_date_greater_than_filter.last_update_utc_date_time.isoformat() == (
            date_greater_than_filter.last_update_utc_date_time.isoformat())
# endset
        assert new_date_greater_than_filter.pac_code_peek == (  # PacID
            date_greater_than_filter.pac_code_peek)
# endset
    def test_from_json(self):
        """
            #TODO add comment
        """
        date_greater_than_filter_schema = DateGreaterThanFilterSchema()
        # Convert sample data to JSON string
        json_str = json.dumps(self.sample_data)
        # Deserialize the JSON string to a dictionary
        json_data = json.loads(json_str)
        # Load the dictionary to an object
        deserialized_data = date_greater_than_filter_schema.load(json_data)
        assert str(deserialized_data['date_greater_than_filter_id']) == (
            str(self.sample_data['date_greater_than_filter_id']))
        assert str(deserialized_data['code']) == (
            str(self.sample_data['code']))
        assert str(deserialized_data['last_change_code']) == (
            str(self.sample_data['last_change_code']))
        assert str(deserialized_data['insert_user_id']) == (
            str(self.sample_data['insert_user_id']))
        assert str(deserialized_data['last_update_user_id']) == (
            str(self.sample_data['last_update_user_id']))
# endset
        assert str(deserialized_data['day_count']) == (
            str(self.sample_data['day_count']))
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
# endset
        assert deserialized_data['insert_utc_date_time'].isoformat() == (
            self.sample_data['insert_utc_date_time'])
        assert str(deserialized_data['pac_code_peek']) == (  # PacID
            str(self.sample_data['pac_code_peek']))
# endset
        assert deserialized_data['last_update_utc_date_time'].isoformat() == (
            self.sample_data['last_update_utc_date_time'])
        new_date_greater_than_filter = DateGreaterThanFilter(**deserialized_data)
        assert isinstance(new_date_greater_than_filter, DateGreaterThanFilter)
    def test_to_json(self, date_greater_than_filter: DateGreaterThanFilter):
        """
            #TODO add comment
        """
        # Convert the DateGreaterThanFilter instance to JSON using the schema
        date_greater_than_filter_schema = DateGreaterThanFilterSchema()
        date_greater_than_filter_dict = date_greater_than_filter_schema.dump(date_greater_than_filter)
        # Convert the date_greater_than_filter_dict to JSON string
        date_greater_than_filter_json = json.dumps(date_greater_than_filter_dict)
        # Convert the JSON strings back to dictionaries
        date_greater_than_filter_dict_from_json = json.loads(date_greater_than_filter_json)
        # sample_dict_from_json = json.loads(self.sample_data)
        logging.info(
            "date_greater_than_filter_dict_from_json.keys() %s",
            date_greater_than_filter_dict_from_json.keys())
        logging.info("self.sample_data.keys() %s", self.sample_data.keys())
        # Verify the keys in both dictionaries match
        assert set(date_greater_than_filter_dict_from_json.keys()) == (
            set(self.sample_data.keys())), (
            f"Expected keys: {set(self.sample_data.keys())}, "
            f"Got: {set(date_greater_than_filter_dict_from_json.keys())}"
        )
        assert date_greater_than_filter_dict_from_json['code'] == str(date_greater_than_filter.code), (
            "failed on code"
        )
        assert date_greater_than_filter_dict_from_json['last_change_code'] == (
            date_greater_than_filter.last_change_code), (
            "failed on last_change_code"
        )
        assert date_greater_than_filter_dict_from_json['insert_user_id'] == (
            str(date_greater_than_filter.insert_user_id)), (
            "failed on insert_user_id"
        )
        assert date_greater_than_filter_dict_from_json['last_update_user_id'] == (
            str(date_greater_than_filter.last_update_user_id)), (
            "failed on last_update_user_id"
        )
# endset
        assert date_greater_than_filter_dict_from_json['day_count'] == (
            date_greater_than_filter.day_count), (
            "failed on day_count"
        )
        assert date_greater_than_filter_dict_from_json['description'] == (
            date_greater_than_filter.description), (
            "failed on description"
        )
        assert date_greater_than_filter_dict_from_json['display_order'] == (
            date_greater_than_filter.display_order), (
            "failed on display_order"
        )
        assert date_greater_than_filter_dict_from_json['is_active'] == (
            date_greater_than_filter.is_active), (
            "failed on is_active"
        )
        assert date_greater_than_filter_dict_from_json['lookup_enum_name'] == (
            date_greater_than_filter.lookup_enum_name), (
            "failed on lookup_enum_name"
        )
        assert date_greater_than_filter_dict_from_json['name'] == (
            date_greater_than_filter.name), (
            "failed on name"
        )
        assert date_greater_than_filter_dict_from_json['pac_id'] == (
            date_greater_than_filter.pac_id), (
            "failed on pac_id"
        )
# endset
        assert date_greater_than_filter_dict_from_json['insert_utc_date_time'] == (
            date_greater_than_filter.insert_utc_date_time.isoformat()), (
            "failed on insert_utc_date_time"
        )
        assert date_greater_than_filter_dict_from_json['last_update_utc_date_time'] == (
            date_greater_than_filter.last_update_utc_date_time.isoformat()), (
            "failed on last_update_utc_date_time"
        )
# endset
        assert date_greater_than_filter_dict_from_json['pac_code_peek'] == (  # PacID
            str(date_greater_than_filter.pac_code_peek)), (
            "failed on pac_code_peek"
        )
# endset
