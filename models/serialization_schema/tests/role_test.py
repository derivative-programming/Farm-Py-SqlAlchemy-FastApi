import json
import pytest
import pytz
from models import Role
from datetime import date, datetime
from decimal import Decimal
from models.serialization_schema import RoleSchema
from models.factory import RoleFactory
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base
from services.logging_config import get_logger
logger = get_logger(__name__)
class TestRoleSchema:
    # Sample data for a Role instance
    sample_data = {
        "role_id": 1,
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
    def test_role_serialization(self, role:Role, session):
        schema = RoleSchema()
        result = schema.dump(role)
        assert result['code'] == role.code
        assert result['last_change_code'] == role.last_change_code
        assert result['insert_user_id'] == role.insert_user_id
        assert result['last_update_user_id'] == role.last_update_user_id

        assert result['description'] == role.description
        assert result['display_order'] == role.display_order
        assert result['is_active'] == role.is_active
        assert result['lookup_enum_name'] == role.lookup_enum_name
        assert result['name'] == role.name
        assert result['pac_id'] == role.pac_id

        assert result['insert_utc_date_time'] == role.insert_utc_date_time.isoformat()
        assert result['last_update_utc_date_time'] == role.last_update_utc_date_time.isoformat()

        assert result['pac_code_peek'] == role.pac_code_peek # PacID

    def test_role_deserialization(self, role:Role, session):
        schema = RoleSchema()
        serialized_data = schema.dump(role)
        deserialized_data = schema.load(serialized_data)
        assert deserialized_data['code'] == role.code
        assert deserialized_data['last_change_code'] == role.last_change_code
        assert deserialized_data['insert_user_id'] == role.insert_user_id
        assert deserialized_data['last_update_user_id'] == role.last_update_user_id

        assert deserialized_data['description'] == role.description
        assert deserialized_data['display_order'] == role.display_order
        assert deserialized_data['is_active'] == role.is_active
        assert deserialized_data['lookup_enum_name'] == role.lookup_enum_name
        assert deserialized_data['name'] == role.name
        assert deserialized_data['pac_id'] == role.pac_id

        assert deserialized_data['insert_utc_date_time'].isoformat() == role.insert_utc_date_time.isoformat()
        assert deserialized_data['last_update_utc_date_time'].isoformat() == role.last_update_utc_date_time.isoformat()

        assert deserialized_data['pac_code_peek'] == role.pac_code_peek # PacID

        new_role = Role(**deserialized_data)
        assert isinstance(new_role, Role)
        # Now compare the new_role attributes with the role attributes
        assert new_role.code == role.code
        assert new_role.last_change_code == role.last_change_code
        assert new_role.insert_user_id == role.insert_user_id
        assert new_role.last_update_user_id == role.last_update_user_id

        assert new_role.description == role.description
        assert new_role.display_order == role.display_order
        assert new_role.is_active == role.is_active
        assert new_role.lookup_enum_name == role.lookup_enum_name
        assert new_role.name == role.name
        assert new_role.pac_id == role.pac_id

        assert new_role.insert_utc_date_time.isoformat() == role.insert_utc_date_time.isoformat()
        assert new_role.last_update_utc_date_time.isoformat() == role.last_update_utc_date_time.isoformat()

        assert new_role.pac_code_peek == role.pac_code_peek #PacID

    def test_from_json(self, role:Role, session):
        role_schema = RoleSchema()
        # Convert sample data to JSON string
        json_str = json.dumps(self.sample_data)
        # Deserialize the JSON string to a dictionary
        json_data = json.loads(json_str)
        # Load the dictionary to an object
        deserialized_data = role_schema.load(json_data)
        assert str(deserialized_data['role_id']) == str(self.sample_data['role_id'])
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
        new_role = Role(**deserialized_data)
        assert isinstance(new_role, Role)
    def test_to_json(self, role:Role, session):
            # Convert the Role instance to JSON using the schema
            role_schema = RoleSchema()
            role_dict = role_schema.dump(role)
            # Convert the role_dict to JSON string
            role_json = json.dumps(role_dict)
            # Convert the JSON strings back to dictionaries
            role_dict_from_json = json.loads(role_json)
            # sample_dict_from_json = json.loads(self.sample_data)
            # Verify the keys in both dictionaries match
            assert set(role_dict_from_json.keys()) == set(self.sample_data.keys()), f"Expected keys: {set(self.sample_data.keys())}, Got: {set(role_dict_from_json.keys())}"
            assert role_dict_from_json['code'] == role.code
            assert role_dict_from_json['last_change_code'] == role.last_change_code
            assert role_dict_from_json['insert_user_id'] == role.insert_user_id
            assert role_dict_from_json['last_update_user_id'] == role.last_update_user_id

            assert role_dict_from_json['description'] == role.description
            assert role_dict_from_json['display_order'] == role.display_order
            assert role_dict_from_json['is_active'] == role.is_active
            assert role_dict_from_json['lookup_enum_name'] == role.lookup_enum_name
            assert role_dict_from_json['name'] == role.name
            assert role_dict_from_json['pac_id'] == role.pac_id

            assert role_dict_from_json['insert_utc_date_time'] == role.insert_utc_date_time.isoformat()
            assert role_dict_from_json['last_update_utc_date_time'] == role.last_update_utc_date_time.isoformat()

            assert role_dict_from_json['pac_code_peek'] == role.pac_code_peek # PacID

