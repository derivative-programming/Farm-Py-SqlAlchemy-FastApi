# tri_state_filter_test.py
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
from models import TriStateFilter
from models.factory import TriStateFilterFactory
from models.serialization_schema import TriStateFilterSchema
from services.logging_config import get_logger
logger = get_logger(__name__)
@pytest.fixture(scope="function")
def tri_state_filter(session):
    """
    Fixture to create and return a TriStateFilter instance using the TriStateFilterFactory.
    Args:
        session: The database session.
    Returns:
        TriStateFilter: A newly created TriStateFilter instance.
    """
    return TriStateFilterFactory.create(session=session)
class TestTriStateFilterSchema:
    """
    Tests for the TriStateFilter serialization schema.
    """
    # Sample data for a TriStateFilter instance
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
    def test_tri_state_filter_serialization(self, tri_state_filter: TriStateFilter):
        """
        Test the serialization of a TriStateFilter instance using TriStateFilterSchema.
        Args:
            tri_state_filter (TriStateFilter): A TriStateFilter instance to serialize.
        """
        schema = TriStateFilterSchema()
        result: Dict[str, Any] = schema.dump(tri_state_filter)
        assert result['code'] == str(tri_state_filter.code)
        assert result['last_change_code'] == (
            tri_state_filter.last_change_code)
        assert result['insert_user_id'] == (
            str(tri_state_filter.insert_user_id))
        assert result['last_update_user_id'] == (
            str(tri_state_filter.last_update_user_id))
# endset
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
# endset
        assert result['insert_utc_date_time'] == (
            tri_state_filter.insert_utc_date_time.isoformat())
        assert result['last_update_utc_date_time'] == (
            tri_state_filter.last_update_utc_date_time.isoformat())
# endset
        assert result['pac_code_peek'] == (  # PacID
            str(tri_state_filter.pac_code_peek))
# endset
    def test_tri_state_filter_deserialization(self, tri_state_filter: TriStateFilter):
        """
            #TODO add comment
        """
        schema = TriStateFilterSchema()
        serialized_data = schema.dump(tri_state_filter)
        deserialized_data = schema.load(serialized_data)
        assert deserialized_data['code'] == tri_state_filter.code
        assert deserialized_data['last_change_code'] == (
            tri_state_filter.last_change_code)
        assert deserialized_data['insert_user_id'] == (
            tri_state_filter.insert_user_id)
        assert deserialized_data['last_update_user_id'] == (
            tri_state_filter.last_update_user_id)
# endset
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
# endset
        assert deserialized_data['insert_utc_date_time'].isoformat() == (
            tri_state_filter.insert_utc_date_time.isoformat())
        assert deserialized_data['last_update_utc_date_time'].isoformat() == (
            tri_state_filter.last_update_utc_date_time.isoformat())
# endset
        assert deserialized_data['pac_code_peek'] == (  # PacID
            tri_state_filter.pac_code_peek)
# endset
        new_tri_state_filter = TriStateFilter(**deserialized_data)
        assert isinstance(new_tri_state_filter, TriStateFilter)
        # Now compare the new_tri_state_filter attributes with the tri_state_filter attributes
        assert new_tri_state_filter.code == tri_state_filter.code
        assert new_tri_state_filter.last_change_code == tri_state_filter.last_change_code
        assert new_tri_state_filter.insert_user_id == tri_state_filter.insert_user_id
        assert new_tri_state_filter.last_update_user_id == tri_state_filter.last_update_user_id
# endset
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
# endset
        assert new_tri_state_filter.insert_utc_date_time.isoformat() == (
            tri_state_filter.insert_utc_date_time.isoformat())
        assert new_tri_state_filter.last_update_utc_date_time.isoformat() == (
            tri_state_filter.last_update_utc_date_time.isoformat())
# endset
        assert new_tri_state_filter.pac_code_peek == (  # PacID
            tri_state_filter.pac_code_peek)
# endset
    def test_from_json(self):
        """
            #TODO add comment
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
# endset
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
# endset
        assert deserialized_data['insert_utc_date_time'].isoformat() == (
            self.sample_data['insert_utc_date_time'])
        assert str(deserialized_data['pac_code_peek']) == (  # PacID
            str(self.sample_data['pac_code_peek']))
# endset
        assert deserialized_data['last_update_utc_date_time'].isoformat() == (
            self.sample_data['last_update_utc_date_time'])
        new_tri_state_filter = TriStateFilter(**deserialized_data)
        assert isinstance(new_tri_state_filter, TriStateFilter)
    def test_to_json(self, tri_state_filter: TriStateFilter):
        """
            #TODO add comment
        """
        # Convert the TriStateFilter instance to JSON using the schema
        tri_state_filter_schema = TriStateFilterSchema()
        tri_state_filter_dict = tri_state_filter_schema.dump(tri_state_filter)
        # Convert the tri_state_filter_dict to JSON string
        tri_state_filter_json = json.dumps(tri_state_filter_dict)
        # Convert the JSON strings back to dictionaries
        tri_state_filter_dict_from_json = json.loads(tri_state_filter_json)
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
        assert tri_state_filter_dict_from_json['code'] == str(tri_state_filter.code), (
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
# endset
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
# endset
        assert tri_state_filter_dict_from_json['insert_utc_date_time'] == (
            tri_state_filter.insert_utc_date_time.isoformat()), (
            "failed on insert_utc_date_time"
        )
        assert tri_state_filter_dict_from_json['last_update_utc_date_time'] == (
            tri_state_filter.last_update_utc_date_time.isoformat()), (
            "failed on last_update_utc_date_time"
        )
# endset
        assert tri_state_filter_dict_from_json['pac_code_peek'] == (  # PacID
            str(tri_state_filter.pac_code_peek)), (
            "failed on pac_code_peek"
        )
# endset
