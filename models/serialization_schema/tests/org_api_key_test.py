# org_api_key_test.py
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
from models import OrgApiKey
from models.factory import OrgApiKeyFactory
from models.serialization_schema import OrgApiKeySchema
from services.logging_config import get_logger
logger = get_logger(__name__)
@pytest.fixture(scope="function")
def org_api_key(session):
    """
    Fixture to create and return a OrgApiKey instance using the OrgApiKeyFactory.
    Args:
        session: The database session.
    Returns:
        OrgApiKey: A newly created OrgApiKey instance.
    """
    return OrgApiKeyFactory.create(session=session)
class TestOrgApiKeySchema:
    """
    Tests for the OrgApiKey serialization schema.
    """
    # Sample data for a OrgApiKey instance
    sample_data = {
        "org_api_key_id": 1,
        "code":
            "a1b2c3d4-e5f6-7a8b-9c0d-123456789012",
        "last_change_code": 0,
        "insert_user_id":
            "a1b2c3d4-e5f6-7a8b-9c0d-123456789012",
        "last_update_user_id":
            "a1b2c3d4-e5f6-7a8b-9c0d-123456789012",
# endset  # noqa: E122
        "api_key_value": "Vanilla",
        "created_by": "Vanilla",
        "created_utc_date_time": datetime(
            2023, 1, 1, 12, 0, 0, tzinfo=pytz.utc
        ).isoformat(),
        "expiration_utc_date_time": datetime(
            2023, 1, 1, 12, 0, 0, tzinfo=pytz.utc
        ).isoformat(),
        "is_active": False,
        "is_temp_user_key": False,
        "name": "Vanilla",
        "organization_id": 2,
        "org_customer_id": 1,
        "insert_utc_date_time": datetime(
            2024, 1, 1, 12, 0, 0, tzinfo=pytz.utc
        ).isoformat(),
        "last_update_utc_date_time": datetime(
            2025, 1, 1, 12, 0, 0, tzinfo=pytz.utc
        ).isoformat(),
# endset  # noqa: E122
        "organization_code_peek":  # OrganizationID
            "a1b2c3d4-e5f6-7a8b-9c0d-123456789012",
        "org_customer_code_peek":  # OrgCustomerID
            "a1b2c3d4-e5f6-7a8b-9c0d-123456789012",
# endset  # noqa: E122
    }
    def test_org_api_key_serialization(self, org_api_key: OrgApiKey):
        """
        Test the serialization of a OrgApiKey instance using OrgApiKeySchema.
        Args:
            org_api_key (OrgApiKey): A OrgApiKey instance to serialize.
        """
        schema = OrgApiKeySchema()
        result: Dict[str, Any] = schema.dump(org_api_key)
        assert result['code'] == str(org_api_key.code)
        assert result['last_change_code'] == (
            org_api_key.last_change_code)
        assert result['insert_user_id'] == (
            str(org_api_key.insert_user_id))
        assert result['last_update_user_id'] == (
            str(org_api_key.last_update_user_id))
# endset
        assert result['api_key_value'] == (
            org_api_key.api_key_value)
        assert result['created_by'] == (
            org_api_key.created_by)
        assert result['created_utc_date_time'] == (
            org_api_key.created_utc_date_time.isoformat())
        assert result['expiration_utc_date_time'] == (
            org_api_key.expiration_utc_date_time.isoformat())
        assert result['is_active'] == (
            org_api_key.is_active)
        assert result['is_temp_user_key'] == (
            org_api_key.is_temp_user_key)
        assert result['name'] == (
            org_api_key.name)
        assert result['organization_id'] == (
            org_api_key.organization_id)
        assert result['org_customer_id'] == (
            org_api_key.org_customer_id)
# endset
        assert result['insert_utc_date_time'] == (
            org_api_key.insert_utc_date_time.isoformat())
        assert result['last_update_utc_date_time'] == (
            org_api_key.last_update_utc_date_time.isoformat())
# endset
        assert result['organization_code_peek'] == (  # OrganizationID
            str(org_api_key.organization_code_peek))
        assert result['org_customer_code_peek'] == (  # OrgCustomerID
            str(org_api_key.org_customer_code_peek))
# endset
    def test_org_api_key_deserialization(self, org_api_key: OrgApiKey):
        """
            #TODO add comment
        """
        schema = OrgApiKeySchema()
        serialized_data = schema.dump(org_api_key)
        deserialized_data = schema.load(serialized_data)
        assert deserialized_data['code'] == org_api_key.code
        assert deserialized_data['last_change_code'] == (
            org_api_key.last_change_code)
        assert deserialized_data['insert_user_id'] == (
            org_api_key.insert_user_id)
        assert deserialized_data['last_update_user_id'] == (
            org_api_key.last_update_user_id)
# endset
        assert deserialized_data['api_key_value'] == (
            org_api_key.api_key_value)
        assert deserialized_data['created_by'] == (
            org_api_key.created_by)
        assert deserialized_data['created_utc_date_time'].isoformat() == (
            org_api_key.created_utc_date_time.isoformat())
        assert deserialized_data['expiration_utc_date_time'].isoformat() == (
            org_api_key.expiration_utc_date_time.isoformat())
        assert deserialized_data['is_active'] == (
            org_api_key.is_active)
        assert deserialized_data['is_temp_user_key'] == (
            org_api_key.is_temp_user_key)
        assert deserialized_data['name'] == (
            org_api_key.name)
        assert deserialized_data['organization_id'] == (
            org_api_key.organization_id)
        assert deserialized_data['org_customer_id'] == (
            org_api_key.org_customer_id)
# endset
        assert deserialized_data['insert_utc_date_time'].isoformat() == (
            org_api_key.insert_utc_date_time.isoformat())
        assert deserialized_data['last_update_utc_date_time'].isoformat() == (
            org_api_key.last_update_utc_date_time.isoformat())
# endset
        assert deserialized_data['organization_code_peek'] == (  # OrganizationID
            org_api_key.organization_code_peek)
        assert deserialized_data['org_customer_code_peek'] == (  # OrgCustomerID
            org_api_key.org_customer_code_peek)
# endset
        new_org_api_key = OrgApiKey(**deserialized_data)
        assert isinstance(new_org_api_key, OrgApiKey)
        # Now compare the new_org_api_key attributes with the org_api_key attributes
        assert new_org_api_key.code == org_api_key.code
        assert new_org_api_key.last_change_code == org_api_key.last_change_code
        assert new_org_api_key.insert_user_id == org_api_key.insert_user_id
        assert new_org_api_key.last_update_user_id == org_api_key.last_update_user_id
# endset
        assert new_org_api_key.api_key_value == (
            org_api_key.api_key_value)
        assert new_org_api_key.created_by == (
            org_api_key.created_by)
        assert new_org_api_key.created_utc_date_time.isoformat() == (
            org_api_key.created_utc_date_time.isoformat())
        assert new_org_api_key.expiration_utc_date_time.isoformat() == (
            org_api_key.expiration_utc_date_time.isoformat())
        assert new_org_api_key.is_active == (
            org_api_key.is_active)
        assert new_org_api_key.is_temp_user_key == (
            org_api_key.is_temp_user_key)
        assert new_org_api_key.name == (
            org_api_key.name)
        assert new_org_api_key.organization_id == (
            org_api_key.organization_id)
        assert new_org_api_key.org_customer_id == (
            org_api_key.org_customer_id)
# endset
        assert new_org_api_key.insert_utc_date_time.isoformat() == (
            org_api_key.insert_utc_date_time.isoformat())
        assert new_org_api_key.last_update_utc_date_time.isoformat() == (
            org_api_key.last_update_utc_date_time.isoformat())
# endset
        assert new_org_api_key.organization_code_peek == (  # OrganizationID
            org_api_key.organization_code_peek)
        assert new_org_api_key.org_customer_code_peek == (  # OrgCustomerID
            org_api_key.org_customer_code_peek)
# endset
    def test_from_json(self):
        """
            #TODO add comment
        """
        org_api_key_schema = OrgApiKeySchema()
        # Convert sample data to JSON string
        json_str = json.dumps(self.sample_data)
        # Deserialize the JSON string to a dictionary
        json_data = json.loads(json_str)
        # Load the dictionary to an object
        deserialized_data = org_api_key_schema.load(json_data)
        assert str(deserialized_data['org_api_key_id']) == (
            str(self.sample_data['org_api_key_id']))
        assert str(deserialized_data['code']) == (
            str(self.sample_data['code']))
        assert str(deserialized_data['last_change_code']) == (
            str(self.sample_data['last_change_code']))
        assert str(deserialized_data['insert_user_id']) == (
            str(self.sample_data['insert_user_id']))
        assert str(deserialized_data['last_update_user_id']) == (
            str(self.sample_data['last_update_user_id']))
# endset
        assert str(deserialized_data['api_key_value']) == (
            str(self.sample_data['api_key_value']))
        assert str(deserialized_data['created_by']) == (
            str(self.sample_data['created_by']))
        assert deserialized_data['created_utc_date_time'].isoformat() == (
            self.sample_data['created_utc_date_time'])
        assert deserialized_data['expiration_utc_date_time'].isoformat() == (
            self.sample_data['expiration_utc_date_time'])
        assert str(deserialized_data['is_active']) == (
            str(self.sample_data['is_active']))
        assert str(deserialized_data['is_temp_user_key']) == (
            str(self.sample_data['is_temp_user_key']))
        assert str(deserialized_data['name']) == (
            str(self.sample_data['name']))
        assert str(deserialized_data['organization_id']) == (
            str(self.sample_data['organization_id']))
        assert str(deserialized_data['org_customer_id']) == (
            str(self.sample_data['org_customer_id']))
# endset
        assert deserialized_data['insert_utc_date_time'].isoformat() == (
            self.sample_data['insert_utc_date_time'])
        assert str(deserialized_data['organization_code_peek']) == (  # OrganizationID
            str(self.sample_data['organization_code_peek']))
        assert str(deserialized_data['org_customer_code_peek']) == (  # OrgCustomerID
            str(self.sample_data['org_customer_code_peek']))
# endset
        assert deserialized_data['last_update_utc_date_time'].isoformat() == (
            self.sample_data['last_update_utc_date_time'])
        new_org_api_key = OrgApiKey(**deserialized_data)
        assert isinstance(new_org_api_key, OrgApiKey)
    def test_to_json(self, org_api_key: OrgApiKey):
        """
            #TODO add comment
        """
        # Convert the OrgApiKey instance to JSON using the schema
        org_api_key_schema = OrgApiKeySchema()
        org_api_key_dict = org_api_key_schema.dump(org_api_key)
        # Convert the org_api_key_dict to JSON string
        org_api_key_json = json.dumps(org_api_key_dict)
        # Convert the JSON strings back to dictionaries
        org_api_key_dict_from_json = json.loads(org_api_key_json)
        # sample_dict_from_json = json.loads(self.sample_data)
        logging.info(
            "org_api_key_dict_from_json.keys() %s",
            org_api_key_dict_from_json.keys())
        logging.info("self.sample_data.keys() %s", self.sample_data.keys())
        # Verify the keys in both dictionaries match
        assert set(org_api_key_dict_from_json.keys()) == (
            set(self.sample_data.keys())), (
            f"Expected keys: {set(self.sample_data.keys())}, "
            f"Got: {set(org_api_key_dict_from_json.keys())}"
        )
        assert org_api_key_dict_from_json['code'] == str(org_api_key.code), (
            "failed on code"
        )
        assert org_api_key_dict_from_json['last_change_code'] == (
            org_api_key.last_change_code), (
            "failed on last_change_code"
        )
        assert org_api_key_dict_from_json['insert_user_id'] == (
            str(org_api_key.insert_user_id)), (
            "failed on insert_user_id"
        )
        assert org_api_key_dict_from_json['last_update_user_id'] == (
            str(org_api_key.last_update_user_id)), (
            "failed on last_update_user_id"
        )
# endset
        assert org_api_key_dict_from_json['api_key_value'] == (
            org_api_key.api_key_value), (
            "failed on api_key_value"
        )
        assert org_api_key_dict_from_json['created_by'] == (
            org_api_key.created_by), (
            "failed on created_by"
        )
        assert org_api_key_dict_from_json['created_utc_date_time'] == (
            org_api_key.created_utc_date_time.isoformat()), (
            "failed on created_utc_date_time"
        )
        assert org_api_key_dict_from_json['expiration_utc_date_time'] == (
            org_api_key.expiration_utc_date_time.isoformat()), (
            "failed on expiration_utc_date_time"
        )
        assert org_api_key_dict_from_json['is_active'] == (
            org_api_key.is_active), (
            "failed on is_active"
        )
        assert org_api_key_dict_from_json['is_temp_user_key'] == (
            org_api_key.is_temp_user_key), (
            "failed on is_temp_user_key"
        )
        assert org_api_key_dict_from_json['name'] == (
            org_api_key.name), (
            "failed on name"
        )
        assert org_api_key_dict_from_json['organization_id'] == (
            org_api_key.organization_id), (
            "failed on organization_id"
        )
        assert org_api_key_dict_from_json['org_customer_id'] == (
            org_api_key.org_customer_id), (
            "failed on org_customer_id"
        )
# endset
        assert org_api_key_dict_from_json['insert_utc_date_time'] == (
            org_api_key.insert_utc_date_time.isoformat()), (
            "failed on insert_utc_date_time"
        )
        assert org_api_key_dict_from_json['last_update_utc_date_time'] == (
            org_api_key.last_update_utc_date_time.isoformat()), (
            "failed on last_update_utc_date_time"
        )
# endset
        assert org_api_key_dict_from_json['organization_code_peek'] == (  # OrganizationID
            str(org_api_key.organization_code_peek)), (
            "failed on organization_code_peek"
        )
        assert org_api_key_dict_from_json['org_customer_code_peek'] == (  # OrgCustomerID
            str(org_api_key.org_customer_code_peek)), (
            "failed on org_customer_code_peek"
        )
# endset
