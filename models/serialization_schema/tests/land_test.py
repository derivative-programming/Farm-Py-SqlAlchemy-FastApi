# land_test.py
"""
    #TODO add comment
"""
import json
import pytest
import pytz
from models import Land
from datetime import datetime
from decimal import Decimal
from models.serialization_schema import LandSchema
from models.factory import LandFactory
from services.logging_config import get_logger
logger = get_logger(__name__)
@pytest.fixture(scope="function")
def land(session):
    """
    #TODO add comment
    """
    # Use the LandFactory to create and return a land instance
    return LandFactory.create(session=session)
class TestLandSchema:
    """
    #TODO add comment
    """
    # Sample data for a Land instance
    sample_data = {
        "land_id": 1,
        "code": "a1b2c3d4-e5f6-7a8b-9c0d-123456789012",
        "last_change_code": 0,
        "insert_user_id": "a1b2c3d4-e5f6-7a8b-9c0d-123456789012",
        "last_update_user_id": "a1b2c3d4-e5f6-7a8b-9c0d-123456789012",
# endset
        "description": "Vanilla",
        "display_order": 42,
        "is_active": False,
        "lookup_enum_name": "Vanilla",
        "name": "Vanilla",
        "pac_id": 2,
        "insert_utc_date_time": datetime(
                        2024, 1, 1, 12, 0, 0, tzinfo=pytz.utc
                ).isoformat(),
# endset
        "pac_code_peek": "a1b2c3d4-e5f6-7a8b-9c0d-123456789012",  # PacID
# endset
        "last_update_utc_date_time": datetime(
             2025, 1, 1, 12, 0, 0, tzinfo=pytz.utc
             ).isoformat()
    }
    def test_land_serialization(self, land: Land, session):
        schema = LandSchema()
        result = schema.dump(land)
        assert result['code'] == land.code
        assert result['last_change_code'] == (
            land.last_change_code)
        assert result['insert_user_id'] == (
            land.insert_user_id)
        assert result['last_update_user_id'] == (
            land.last_update_user_id)
# endset
        assert result['description'] == (
            land.description)
        assert result['display_order'] == (
            land.display_order)
        assert result['is_active'] == (
            land.is_active)
        assert result['lookup_enum_name'] == (
            land.lookup_enum_name)
        assert result['name'] == (
            land.name)
        assert result['pac_id'] == (
            land.pac_id)
# endset
        assert result['insert_utc_date_time'] == (
            land.insert_utc_date_time.isoformat())
        assert result['last_update_utc_date_time'] == (
            land.last_update_utc_date_time.isoformat())
# endset
        assert result['pac_code_peek'] == (  # PacID
            land.pac_code_peek)
# endset
    def test_land_deserialization(self, land: Land, session):
        schema = LandSchema()
        serialized_data = schema.dump(land)
        deserialized_data = schema.load(serialized_data)
        assert deserialized_data['code'] == land.code
        assert deserialized_data['last_change_code'] == (
            land.last_change_code)
        assert deserialized_data['insert_user_id'] == (
            land.insert_user_id)
        assert deserialized_data['last_update_user_id'] == (
            land.last_update_user_id)
# endset
        assert deserialized_data['description'] == (
            land.description)
        assert deserialized_data['display_order'] == (
            land.display_order)
        assert deserialized_data['is_active'] == (
            land.is_active)
        assert deserialized_data['lookup_enum_name'] == (
            land.lookup_enum_name)
        assert deserialized_data['name'] == (
            land.name)
        assert deserialized_data['pac_id'] == (
            land.pac_id)
# endset
        assert deserialized_data['insert_utc_date_time'].isoformat() == (
            land.insert_utc_date_time.isoformat())
        assert deserialized_data['last_update_utc_date_time'].isoformat() == (
            land.last_update_utc_date_time.isoformat())
# endset
        assert deserialized_data['pac_code_peek'] == (  # PacID
            land.pac_code_peek)
# endset
        new_land = Land(**deserialized_data)
        assert isinstance(new_land, Land)
        # Now compare the new_land attributes with the land attributes
        assert new_land.code == land.code
        assert new_land.last_change_code == land.last_change_code
        assert new_land.insert_user_id == land.insert_user_id
        assert new_land.last_update_user_id == land.last_update_user_id
# endset
        assert new_land.description == (
            land.description)
        assert new_land.display_order == (
            land.display_order)
        assert new_land.is_active == (
            land.is_active)
        assert new_land.lookup_enum_name == (
            land.lookup_enum_name)
        assert new_land.name == (
            land.name)
        assert new_land.pac_id == (
            land.pac_id)
# endset
        assert new_land.insert_utc_date_time.isoformat() == (
            land.insert_utc_date_time.isoformat())
        assert new_land.last_update_utc_date_time.isoformat() == (
            land.last_update_utc_date_time.isoformat())
# endset
        assert new_land.pac_code_peek == (  # PacID
            land.pac_code_peek)
# endset
    def test_from_json(self, land: Land, session):
        land_schema = LandSchema()
        # Convert sample data to JSON string
        json_str = json.dumps(self.sample_data)
        # Deserialize the JSON string to a dictionary
        json_data = json.loads(json_str)
        # Load the dictionary to an object
        deserialized_data = land_schema.load(json_data)
        assert str(deserialized_data['land_id']) == (
            str(self.sample_data['land_id']))
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
# endset
        assert deserialized_data['insert_utc_date_time'].isoformat() == (
            self.sample_data['insert_utc_date_time'])
        assert str(deserialized_data['pac_code_peek']) == (  # PacID
            str(self.sample_data['pac_code_peek']))
# endset
        assert deserialized_data['last_update_utc_date_time'].isoformat() == (
            self.sample_data['last_update_utc_date_time'])
        new_land = Land(**deserialized_data)
        assert isinstance(new_land, Land)
    def test_to_json(self, land: Land, session):
            # Convert the Land instance to JSON using the schema
            land_schema = LandSchema()
            land_dict = land_schema.dump(land)
            # Convert the land_dict to JSON string
            land_json = json.dumps(land_dict)
            # Convert the JSON strings back to dictionaries
            land_dict_from_json = json.loads(land_json)
            # sample_dict_from_json = json.loads(self.sample_data)
            # Verify the keys in both dictionaries match
            assert set(land_dict_from_json.keys()) == (
                 set(self.sample_data.keys()), f"Expected keys: {set(self.sample_data.keys())}, Got: {set(land_dict_from_json.keys())}"
            )
            assert land_dict_from_json['code'] == land.code
            assert land_dict_from_json['last_change_code'] == (
                 land.last_change_code)
            assert land_dict_from_json['insert_user_id'] == (
                 land.insert_user_id)
            assert land_dict_from_json['last_update_user_id'] == (
                 land.last_update_user_id)
    # endset
            assert land_dict_from_json['description'] == (
                 land.description)
            assert land_dict_from_json['display_order'] == (
                 land.display_order)
            assert land_dict_from_json['is_active'] == (
                 land.is_active)
            assert land_dict_from_json['lookup_enum_name'] == (
                 land.lookup_enum_name)
            assert land_dict_from_json['name'] == (
                 land.name)
            assert land_dict_from_json['pac_id'] == (
                 land.pac_id)
    # endset
            assert land_dict_from_json['insert_utc_date_time'] == (
                 land.insert_utc_date_time.isoformat())
            assert land_dict_from_json['last_update_utc_date_time'] == (
                 land.last_update_utc_date_time.isoformat())
    # endset
            assert land_dict_from_json['pac_code_peek'] == (  # PacID
                 land.pac_code_peek)
    # endset
