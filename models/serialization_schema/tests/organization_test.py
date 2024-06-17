# organization_test.py
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
from models import Organization
from models.factory import OrganizationFactory
from models.serialization_schema import OrganizationSchema
from services.logging_config import get_logger
logger = get_logger(__name__)
@pytest.fixture(scope="function")
def organization(session):
    """
    Fixture to create and return a Organization instance using the OrganizationFactory.
    Args:
        session: The database session.
    Returns:
        Organization: A newly created Organization instance.
    """
    return OrganizationFactory.create(session=session)
class TestOrganizationSchema:
    """
    Tests for the Organization serialization schema.
    """
    # Sample data for a Organization instance
    sample_data = {
        "organization_id": 1,
        "code":
            "a1b2c3d4-e5f6-7a8b-9c0d-123456789012",
        "last_change_code": 0,
        "insert_user_id":
            "a1b2c3d4-e5f6-7a8b-9c0d-123456789012",
        "last_update_user_id":
            "a1b2c3d4-e5f6-7a8b-9c0d-123456789012",
# endset  # noqa: E122
        "name": "Vanilla",
        "tac_id": 2,
        "insert_utc_date_time": datetime(
            2024, 1, 1, 12, 0, 0, tzinfo=pytz.utc
        ).isoformat(),
        "last_update_utc_date_time": datetime(
            2025, 1, 1, 12, 0, 0, tzinfo=pytz.utc
        ).isoformat(),
# endset  # noqa: E122
        "tac_code_peek":  # TacID
            "a1b2c3d4-e5f6-7a8b-9c0d-123456789012",
# endset  # noqa: E122
    }
    def test_organization_serialization(self, organization: Organization):
        """
        Test the serialization of a Organization instance using OrganizationSchema.
        Args:
            organization (Organization): A Organization instance to serialize.
        """
        schema = OrganizationSchema()
        result: Dict[str, Any] = schema.dump(organization)
        assert result['code'] == str(organization.code)
        assert result['last_change_code'] == (
            organization.last_change_code)
        assert result['insert_user_id'] == (
            str(organization.insert_user_id))
        assert result['last_update_user_id'] == (
            str(organization.last_update_user_id))
# endset
        assert result['name'] == (
            organization.name)
        assert result['tac_id'] == (
            organization.tac_id)
# endset
        assert result['insert_utc_date_time'] == (
            organization.insert_utc_date_time.isoformat())
        assert result['last_update_utc_date_time'] == (
            organization.last_update_utc_date_time.isoformat())
# endset
        assert result['tac_code_peek'] == (  # TacID
            str(organization.tac_code_peek))
# endset
    def test_organization_deserialization(self, organization: Organization):
        """
            #TODO add comment
        """
        schema = OrganizationSchema()
        serialized_data = schema.dump(organization)
        deserialized_data = schema.load(serialized_data)
        assert deserialized_data['code'] == organization.code
        assert deserialized_data['last_change_code'] == (
            organization.last_change_code)
        assert deserialized_data['insert_user_id'] == (
            organization.insert_user_id)
        assert deserialized_data['last_update_user_id'] == (
            organization.last_update_user_id)
# endset
        assert deserialized_data['name'] == (
            organization.name)
        assert deserialized_data['tac_id'] == (
            organization.tac_id)
# endset
        assert deserialized_data['insert_utc_date_time'].isoformat() == (
            organization.insert_utc_date_time.isoformat())
        assert deserialized_data['last_update_utc_date_time'].isoformat() == (
            organization.last_update_utc_date_time.isoformat())
# endset
        assert deserialized_data['tac_code_peek'] == (  # TacID
            organization.tac_code_peek)
# endset
        new_organization = Organization(**deserialized_data)
        assert isinstance(new_organization, Organization)
        # Now compare the new_organization attributes with the organization attributes
        assert new_organization.code == organization.code
        assert new_organization.last_change_code == organization.last_change_code
        assert new_organization.insert_user_id == organization.insert_user_id
        assert new_organization.last_update_user_id == organization.last_update_user_id
# endset
        assert new_organization.name == (
            organization.name)
        assert new_organization.tac_id == (
            organization.tac_id)
# endset
        assert new_organization.insert_utc_date_time.isoformat() == (
            organization.insert_utc_date_time.isoformat())
        assert new_organization.last_update_utc_date_time.isoformat() == (
            organization.last_update_utc_date_time.isoformat())
# endset
        assert new_organization.tac_code_peek == (  # TacID
            organization.tac_code_peek)
# endset
    def test_from_json(self):
        """
            #TODO add comment
        """
        organization_schema = OrganizationSchema()
        # Convert sample data to JSON string
        json_str = json.dumps(self.sample_data)
        # Deserialize the JSON string to a dictionary
        json_data = json.loads(json_str)
        # Load the dictionary to an object
        deserialized_data = organization_schema.load(json_data)
        assert str(deserialized_data['organization_id']) == (
            str(self.sample_data['organization_id']))
        assert str(deserialized_data['code']) == (
            str(self.sample_data['code']))
        assert str(deserialized_data['last_change_code']) == (
            str(self.sample_data['last_change_code']))
        assert str(deserialized_data['insert_user_id']) == (
            str(self.sample_data['insert_user_id']))
        assert str(deserialized_data['last_update_user_id']) == (
            str(self.sample_data['last_update_user_id']))
# endset
        assert str(deserialized_data['name']) == (
            str(self.sample_data['name']))
        assert str(deserialized_data['tac_id']) == (
            str(self.sample_data['tac_id']))
# endset
        assert deserialized_data['insert_utc_date_time'].isoformat() == (
            self.sample_data['insert_utc_date_time'])
        assert str(deserialized_data['tac_code_peek']) == (  # TacID
            str(self.sample_data['tac_code_peek']))
# endset
        assert deserialized_data['last_update_utc_date_time'].isoformat() == (
            self.sample_data['last_update_utc_date_time'])
        new_organization = Organization(**deserialized_data)
        assert isinstance(new_organization, Organization)
    def test_to_json(self, organization: Organization):
        """
            #TODO add comment
        """
        # Convert the Organization instance to JSON using the schema
        organization_schema = OrganizationSchema()
        organization_dict = organization_schema.dump(organization)
        # Convert the organization_dict to JSON string
        organization_json = json.dumps(organization_dict)
        # Convert the JSON strings back to dictionaries
        organization_dict_from_json = json.loads(organization_json)
        # sample_dict_from_json = json.loads(self.sample_data)
        logging.info(
            "organization_dict_from_json.keys() %s",
            organization_dict_from_json.keys())
        logging.info("self.sample_data.keys() %s", self.sample_data.keys())
        # Verify the keys in both dictionaries match
        assert set(organization_dict_from_json.keys()) == (
            set(self.sample_data.keys())), (
            f"Expected keys: {set(self.sample_data.keys())}, "
            f"Got: {set(organization_dict_from_json.keys())}"
        )
        assert organization_dict_from_json['code'] == str(organization.code), (
            "failed on code"
        )
        assert organization_dict_from_json['last_change_code'] == (
            organization.last_change_code), (
            "failed on last_change_code"
        )
        assert organization_dict_from_json['insert_user_id'] == (
            str(organization.insert_user_id)), (
            "failed on insert_user_id"
        )
        assert organization_dict_from_json['last_update_user_id'] == (
            str(organization.last_update_user_id)), (
            "failed on last_update_user_id"
        )
# endset
        assert organization_dict_from_json['name'] == (
            organization.name), (
            "failed on name"
        )
        assert organization_dict_from_json['tac_id'] == (
            organization.tac_id), (
            "failed on tac_id"
        )
# endset
        assert organization_dict_from_json['insert_utc_date_time'] == (
            organization.insert_utc_date_time.isoformat()), (
            "failed on insert_utc_date_time"
        )
        assert organization_dict_from_json['last_update_utc_date_time'] == (
            organization.last_update_utc_date_time.isoformat()), (
            "failed on last_update_utc_date_time"
        )
# endset
        assert organization_dict_from_json['tac_code_peek'] == (  # TacID
            str(organization.tac_code_peek)), (
            "failed on tac_code_peek"
        )
# endset
