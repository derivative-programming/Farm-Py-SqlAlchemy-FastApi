import json
import pytest
import pytz
from models import Tac
from datetime import datetime
from decimal import Decimal
from models.serialization_schema import TacSchema
from models.factory import TacFactory
from services.logging_config import get_logger
logger = get_logger(__name__)
@pytest.fixture(scope="function")
def tac(session):
    # Use the TacFactory to create and return a tac instance
    return TacFactory.create(session=session)
class TestTacSchema:
    # Sample data for a Tac instance
    sample_data = {
        "tac_id": 1,
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
        "insert_utc_date_time": datetime(2024, 1, 1, 12, 0, 0, tzinfo=pytz.utc).isoformat(),

        "pac_code_peek": "a1b2c3d4-e5f6-7a8b-9c0d-123456789012",# PacID

        "last_update_utc_date_time": datetime(2025, 1, 1, 12, 0, 0, tzinfo=pytz.utc).isoformat()
    }
    def test_tac_serialization(self, tac:Tac, session):
        schema = TacSchema()
        result = schema.dump(tac)
        assert result['code'] == tac.code
        assert result['last_change_code'] == tac.last_change_code
        assert result['insert_user_id'] == tac.insert_user_id
        assert result['last_update_user_id'] == tac.last_update_user_id

        assert result['description'] == tac.description
        assert result['display_order'] == tac.display_order
        assert result['is_active'] == tac.is_active
        assert result['lookup_enum_name'] == tac.lookup_enum_name
        assert result['name'] == tac.name
        assert result['pac_id'] == tac.pac_id

        assert result['insert_utc_date_time'] == tac.insert_utc_date_time.isoformat()
        assert result['last_update_utc_date_time'] == tac.last_update_utc_date_time.isoformat()

        assert result['pac_code_peek'] == tac.pac_code_peek # PacID

    def test_tac_deserialization(self, tac:Tac, session):
        schema = TacSchema()
        serialized_data = schema.dump(tac)
        deserialized_data = schema.load(serialized_data)
        assert deserialized_data['code'] == tac.code
        assert deserialized_data['last_change_code'] == tac.last_change_code
        assert deserialized_data['insert_user_id'] == tac.insert_user_id
        assert deserialized_data['last_update_user_id'] == tac.last_update_user_id

        assert deserialized_data['description'] == tac.description
        assert deserialized_data['display_order'] == tac.display_order
        assert deserialized_data['is_active'] == tac.is_active
        assert deserialized_data['lookup_enum_name'] == tac.lookup_enum_name
        assert deserialized_data['name'] == tac.name
        assert deserialized_data['pac_id'] == tac.pac_id

        assert deserialized_data['insert_utc_date_time'].isoformat() == tac.insert_utc_date_time.isoformat()
        assert deserialized_data['last_update_utc_date_time'].isoformat() == tac.last_update_utc_date_time.isoformat()

        assert deserialized_data['pac_code_peek'] == tac.pac_code_peek # PacID

        new_tac = Tac(**deserialized_data)
        assert isinstance(new_tac, Tac)
        # Now compare the new_tac attributes with the tac attributes
        assert new_tac.code == tac.code
        assert new_tac.last_change_code == tac.last_change_code
        assert new_tac.insert_user_id == tac.insert_user_id
        assert new_tac.last_update_user_id == tac.last_update_user_id

        assert new_tac.description == tac.description
        assert new_tac.display_order == tac.display_order
        assert new_tac.is_active == tac.is_active
        assert new_tac.lookup_enum_name == tac.lookup_enum_name
        assert new_tac.name == tac.name
        assert new_tac.pac_id == tac.pac_id

        assert new_tac.insert_utc_date_time.isoformat() == tac.insert_utc_date_time.isoformat()
        assert new_tac.last_update_utc_date_time.isoformat() == tac.last_update_utc_date_time.isoformat()

        assert new_tac.pac_code_peek == tac.pac_code_peek #PacID

    def test_from_json(self, tac:Tac, session):
        tac_schema = TacSchema()
        # Convert sample data to JSON string
        json_str = json.dumps(self.sample_data)
        # Deserialize the JSON string to a dictionary
        json_data = json.loads(json_str)
        # Load the dictionary to an object
        deserialized_data = tac_schema.load(json_data)
        assert str(deserialized_data['tac_id']) == str(self.sample_data['tac_id'])
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

        assert deserialized_data['insert_utc_date_time'].isoformat() == self.sample_data['insert_utc_date_time']
        assert str(deserialized_data['pac_code_peek']) == str(self.sample_data['pac_code_peek']) #PacID

        assert deserialized_data['last_update_utc_date_time'].isoformat() == self.sample_data['last_update_utc_date_time']
        new_tac = Tac(**deserialized_data)
        assert isinstance(new_tac, Tac)
    def test_to_json(self, tac:Tac, session):
            # Convert the Tac instance to JSON using the schema
            tac_schema = TacSchema()
            tac_dict = tac_schema.dump(tac)
            # Convert the tac_dict to JSON string
            tac_json = json.dumps(tac_dict)
            # Convert the JSON strings back to dictionaries
            tac_dict_from_json = json.loads(tac_json)
            # sample_dict_from_json = json.loads(self.sample_data)
            # Verify the keys in both dictionaries match
            assert set(tac_dict_from_json.keys()) == set(self.sample_data.keys()), f"Expected keys: {set(self.sample_data.keys())}, Got: {set(tac_dict_from_json.keys())}"
            assert tac_dict_from_json['code'] == tac.code
            assert tac_dict_from_json['last_change_code'] == tac.last_change_code
            assert tac_dict_from_json['insert_user_id'] == tac.insert_user_id
            assert tac_dict_from_json['last_update_user_id'] == tac.last_update_user_id

            assert tac_dict_from_json['description'] == tac.description
            assert tac_dict_from_json['display_order'] == tac.display_order
            assert tac_dict_from_json['is_active'] == tac.is_active
            assert tac_dict_from_json['lookup_enum_name'] == tac.lookup_enum_name
            assert tac_dict_from_json['name'] == tac.name
            assert tac_dict_from_json['pac_id'] == tac.pac_id

            assert tac_dict_from_json['insert_utc_date_time'] == tac.insert_utc_date_time.isoformat()
            assert tac_dict_from_json['last_update_utc_date_time'] == tac.last_update_utc_date_time.isoformat()

            assert tac_dict_from_json['pac_code_peek'] == tac.pac_code_peek # PacID

