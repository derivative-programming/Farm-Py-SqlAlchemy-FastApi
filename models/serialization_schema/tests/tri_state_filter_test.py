import json
import pytest
import pytz
from models import TriStateFilter
from datetime import datetime
from decimal import Decimal
from models.serialization_schema import TriStateFilterSchema
from models.factory import TriStateFilterFactory
from services.logging_config import get_logger
logger = get_logger(__name__)
@pytest.fixture(scope="function")
def tri_state_filter(session):
    # Use the TriStateFilterFactory to create and return a tri_state_filter instance
    return TriStateFilterFactory.create(session=session)
class TestTriStateFilterSchema:
    # Sample data for a TriStateFilter instance
    sample_data = {
        "tri_state_filter_id": 1,
        "code": "a1b2c3d4-e5f6-7a8b-9c0d-123456789012",
        "last_change_code": 0,
        "insert_user_id": "a1b2c3d4-e5f6-7a8b-9c0d-123456789012",
        "last_update_user_id": "a1b2c3d4-e5f6-7a8b-9c0d-123456789012",

        "description": "Vanilla",
        "display_order": 42,
        "is_active": False,
        "lookup_enum_name": "Vanilla",
        "name": "Vanilla",
        "pac_id": 2,
        "state_int_value": 42,
        "insert_utc_date_time": datetime(2024, 1, 1, 12, 0, 0, tzinfo=pytz.utc).isoformat(),

        "pac_code_peek": "a1b2c3d4-e5f6-7a8b-9c0d-123456789012",  # PacID

        "last_update_utc_date_time": datetime(2025, 1, 1, 12, 0, 0, tzinfo=pytz.utc).isoformat()
    }
    def test_tri_state_filter_serialization(self, tri_state_filter:TriStateFilter, session):
        schema = TriStateFilterSchema()
        result = schema.dump(tri_state_filter)
        assert result['code'] == tri_state_filter.code
        assert result['last_change_code'] == tri_state_filter.last_change_code
        assert result['insert_user_id'] == tri_state_filter.insert_user_id
        assert result['last_update_user_id'] == tri_state_filter.last_update_user_id

        assert result['description'] == tri_state_filter.description
        assert result['display_order'] == tri_state_filter.display_order
        assert result['is_active'] == tri_state_filter.is_active
        assert result['lookup_enum_name'] == tri_state_filter.lookup_enum_name
        assert result['name'] == tri_state_filter.name
        assert result['pac_id'] == tri_state_filter.pac_id
        assert result['state_int_value'] == tri_state_filter.state_int_value

        assert result['insert_utc_date_time'] == tri_state_filter.insert_utc_date_time.isoformat()
        assert result['last_update_utc_date_time'] == tri_state_filter.last_update_utc_date_time.isoformat()

        assert result['pac_code_peek'] == tri_state_filter.pac_code_peek  # PacID

    def test_tri_state_filter_deserialization(self, tri_state_filter:TriStateFilter, session):
        schema = TriStateFilterSchema()
        serialized_data = schema.dump(tri_state_filter)
        deserialized_data = schema.load(serialized_data)
        assert deserialized_data['code'] == tri_state_filter.code
        assert deserialized_data['last_change_code'] == tri_state_filter.last_change_code
        assert deserialized_data['insert_user_id'] == tri_state_filter.insert_user_id
        assert deserialized_data['last_update_user_id'] == tri_state_filter.last_update_user_id

        assert deserialized_data['description'] == tri_state_filter.description
        assert deserialized_data['display_order'] == tri_state_filter.display_order
        assert deserialized_data['is_active'] == tri_state_filter.is_active
        assert deserialized_data['lookup_enum_name'] == tri_state_filter.lookup_enum_name
        assert deserialized_data['name'] == tri_state_filter.name
        assert deserialized_data['pac_id'] == tri_state_filter.pac_id
        assert deserialized_data['state_int_value'] == tri_state_filter.state_int_value

        assert deserialized_data['insert_utc_date_time'].isoformat() == tri_state_filter.insert_utc_date_time.isoformat()
        assert deserialized_data['last_update_utc_date_time'].isoformat() == tri_state_filter.last_update_utc_date_time.isoformat()

        assert deserialized_data['pac_code_peek'] == tri_state_filter.pac_code_peek  # PacID

        new_tri_state_filter = TriStateFilter(**deserialized_data)
        assert isinstance(new_tri_state_filter, TriStateFilter)
        # Now compare the new_tri_state_filter attributes with the tri_state_filter attributes
        assert new_tri_state_filter.code == tri_state_filter.code
        assert new_tri_state_filter.last_change_code == tri_state_filter.last_change_code
        assert new_tri_state_filter.insert_user_id == tri_state_filter.insert_user_id
        assert new_tri_state_filter.last_update_user_id == tri_state_filter.last_update_user_id

        assert new_tri_state_filter.description == tri_state_filter.description
        assert new_tri_state_filter.display_order == tri_state_filter.display_order
        assert new_tri_state_filter.is_active == tri_state_filter.is_active
        assert new_tri_state_filter.lookup_enum_name == tri_state_filter.lookup_enum_name
        assert new_tri_state_filter.name == tri_state_filter.name
        assert new_tri_state_filter.pac_id == tri_state_filter.pac_id
        assert new_tri_state_filter.state_int_value == tri_state_filter.state_int_value

        assert new_tri_state_filter.insert_utc_date_time.isoformat() == tri_state_filter.insert_utc_date_time.isoformat()
        assert new_tri_state_filter.last_update_utc_date_time.isoformat() == tri_state_filter.last_update_utc_date_time.isoformat()

        assert new_tri_state_filter.pac_code_peek == tri_state_filter.pac_code_peek  # PacID

    def test_from_json(self, tri_state_filter:TriStateFilter, session):
        tri_state_filter_schema = TriStateFilterSchema()
        # Convert sample data to JSON string
        json_str = json.dumps(self.sample_data)
        # Deserialize the JSON string to a dictionary
        json_data = json.loads(json_str)
        # Load the dictionary to an object
        deserialized_data = tri_state_filter_schema.load(json_data)
        assert str(deserialized_data['tri_state_filter_id']) == str(self.sample_data['tri_state_filter_id'])
        assert str(deserialized_data['code']) == str(self.sample_data['code'])
        assert str(deserialized_data['last_change_code']) == str(self.sample_data['last_change_code'])
        assert str(deserialized_data['insert_user_id']) == str(self.sample_data['insert_user_id'])
        assert str(deserialized_data['last_update_user_id']) == str(self.sample_data['last_update_user_id'])

        assert str(deserialized_data['description']) == str(self.sample_data['description'])
        assert str(deserialized_data['display_order']) == str(self.sample_data['display_order'])
        assert str(deserialized_data['is_active']) == str(self.sample_data['is_active'])
        assert str(deserialized_data['lookup_enum_name']) == str(self.sample_data['lookup_enum_name'])
        assert str(deserialized_data['name']) == str(self.sample_data['name'])
        assert str(deserialized_data['pac_id']) == str(self.sample_data['pac_id'])
        assert str(deserialized_data['state_int_value']) == str(self.sample_data['state_int_value'])

        assert deserialized_data['insert_utc_date_time'].isoformat() == self.sample_data['insert_utc_date_time']
        assert str(deserialized_data['pac_code_peek']) == str(self.sample_data['pac_code_peek'])  # PacID

        assert deserialized_data['last_update_utc_date_time'].isoformat() == self.sample_data['last_update_utc_date_time']
        new_tri_state_filter = TriStateFilter(**deserialized_data)
        assert isinstance(new_tri_state_filter, TriStateFilter)
    def test_to_json(self, tri_state_filter:TriStateFilter, session):
            # Convert the TriStateFilter instance to JSON using the schema
            tri_state_filter_schema = TriStateFilterSchema()
            tri_state_filter_dict = tri_state_filter_schema.dump(tri_state_filter)
            # Convert the tri_state_filter_dict to JSON string
            tri_state_filter_json = json.dumps(tri_state_filter_dict)
            # Convert the JSON strings back to dictionaries
            tri_state_filter_dict_from_json = json.loads(tri_state_filter_json)
            # sample_dict_from_json = json.loads(self.sample_data)
            # Verify the keys in both dictionaries match
            assert set(tri_state_filter_dict_from_json.keys()) == set(self.sample_data.keys()), f"Expected keys: {set(self.sample_data.keys())}, Got: {set(tri_state_filter_dict_from_json.keys())}"
            assert tri_state_filter_dict_from_json['code'] == tri_state_filter.code
            assert tri_state_filter_dict_from_json['last_change_code'] == tri_state_filter.last_change_code
            assert tri_state_filter_dict_from_json['insert_user_id'] == tri_state_filter.insert_user_id
            assert tri_state_filter_dict_from_json['last_update_user_id'] == tri_state_filter.last_update_user_id

            assert tri_state_filter_dict_from_json['description'] == tri_state_filter.description
            assert tri_state_filter_dict_from_json['display_order'] == tri_state_filter.display_order
            assert tri_state_filter_dict_from_json['is_active'] == tri_state_filter.is_active
            assert tri_state_filter_dict_from_json['lookup_enum_name'] == tri_state_filter.lookup_enum_name
            assert tri_state_filter_dict_from_json['name'] == tri_state_filter.name
            assert tri_state_filter_dict_from_json['pac_id'] == tri_state_filter.pac_id
            assert tri_state_filter_dict_from_json['state_int_value'] == tri_state_filter.state_int_value

            assert tri_state_filter_dict_from_json['insert_utc_date_time'] == tri_state_filter.insert_utc_date_time.isoformat()
            assert tri_state_filter_dict_from_json['last_update_utc_date_time'] == tri_state_filter.last_update_utc_date_time.isoformat()

            assert tri_state_filter_dict_from_json['pac_code_peek'] == tri_state_filter.pac_code_peek  # PacID

