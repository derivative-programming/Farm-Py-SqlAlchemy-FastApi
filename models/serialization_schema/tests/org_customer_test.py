import json
import pytest
import pytz
from models import OrgCustomer
from datetime import datetime
from decimal import Decimal
from models.serialization_schema import OrgCustomerSchema
from models.factory import OrgCustomerFactory
from services.logging_config import get_logger
logger = get_logger(__name__)
@pytest.fixture(scope="function")
def org_customer(session):
    # Use the OrgCustomerFactory to create and return a org_customer instance
    return OrgCustomerFactory.create(session=session)
class TestOrgCustomerSchema:
    # Sample data for a OrgCustomer instance
    sample_data = {
        "org_customer_id": 1,
        "code": "a1b2c3d4-e5f6-7a8b-9c0d-123456789012",
        "last_change_code": 0,
        "insert_user_id": "a1b2c3d4-e5f6-7a8b-9c0d-123456789012",
        "last_update_user_id": "a1b2c3d4-e5f6-7a8b-9c0d-123456789012",

        "customer_id": 1,
        "email": "test@email.com",
        "organization_id": 2,
        "insert_utc_date_time": datetime(2024, 1, 1, 12, 0, 0, tzinfo=pytz.utc).isoformat(),

        "customer_code_peek": "a1b2c3d4-e5f6-7a8b-9c0d-123456789012",# CustomerID
        "organization_code_peek": "a1b2c3d4-e5f6-7a8b-9c0d-123456789012",# OrganizationID

        "last_update_utc_date_time": datetime(2025, 1, 1, 12, 0, 0, tzinfo=pytz.utc).isoformat()
    }
    def test_org_customer_serialization(self, org_customer:OrgCustomer, session):
        schema = OrgCustomerSchema()
        result = schema.dump(org_customer)
        assert result['code'] == org_customer.code
        assert result['last_change_code'] == org_customer.last_change_code
        assert result['insert_user_id'] == org_customer.insert_user_id
        assert result['last_update_user_id'] == org_customer.last_update_user_id

        assert result['customer_id'] == org_customer.customer_id
        assert result['email'] == org_customer.email
        assert result['organization_id'] == org_customer.organization_id

        assert result['insert_utc_date_time'] == org_customer.insert_utc_date_time.isoformat()
        assert result['last_update_utc_date_time'] == org_customer.last_update_utc_date_time.isoformat()

        assert result['customer_code_peek'] == org_customer.customer_code_peek # CustomerID
        assert result['organization_code_peek'] == org_customer.organization_code_peek # OrganizationID

    def test_org_customer_deserialization(self, org_customer:OrgCustomer, session):
        schema = OrgCustomerSchema()
        serialized_data = schema.dump(org_customer)
        deserialized_data = schema.load(serialized_data)
        assert deserialized_data['code'] == org_customer.code
        assert deserialized_data['last_change_code'] == org_customer.last_change_code
        assert deserialized_data['insert_user_id'] == org_customer.insert_user_id
        assert deserialized_data['last_update_user_id'] == org_customer.last_update_user_id

        assert deserialized_data['customer_id'] == org_customer.customer_id
        assert deserialized_data['email'] == org_customer.email
        assert deserialized_data['organization_id'] == org_customer.organization_id

        assert deserialized_data['insert_utc_date_time'].isoformat() == org_customer.insert_utc_date_time.isoformat()
        assert deserialized_data['last_update_utc_date_time'].isoformat() == org_customer.last_update_utc_date_time.isoformat()

        assert deserialized_data['customer_code_peek'] == org_customer.customer_code_peek # CustomerID
        assert deserialized_data['organization_code_peek'] == org_customer.organization_code_peek # OrganizationID

        new_org_customer = OrgCustomer(**deserialized_data)
        assert isinstance(new_org_customer, OrgCustomer)
        # Now compare the new_org_customer attributes with the org_customer attributes
        assert new_org_customer.code == org_customer.code
        assert new_org_customer.last_change_code == org_customer.last_change_code
        assert new_org_customer.insert_user_id == org_customer.insert_user_id
        assert new_org_customer.last_update_user_id == org_customer.last_update_user_id

        assert new_org_customer.customer_id == org_customer.customer_id
        assert new_org_customer.email == org_customer.email
        assert new_org_customer.organization_id == org_customer.organization_id

        assert new_org_customer.insert_utc_date_time.isoformat() == org_customer.insert_utc_date_time.isoformat()
        assert new_org_customer.last_update_utc_date_time.isoformat() == org_customer.last_update_utc_date_time.isoformat()

        assert new_org_customer.customer_code_peek == org_customer.customer_code_peek  #CustomerID
        assert new_org_customer.organization_code_peek == org_customer.organization_code_peek #OrganizationID

    def test_from_json(self, org_customer:OrgCustomer, session):
        org_customer_schema = OrgCustomerSchema()
        # Convert sample data to JSON string
        json_str = json.dumps(self.sample_data)
        # Deserialize the JSON string to a dictionary
        json_data = json.loads(json_str)
        # Load the dictionary to an object
        deserialized_data = org_customer_schema.load(json_data)
        assert str(deserialized_data['org_customer_id']) == str(self.sample_data['org_customer_id'])
        assert str(deserialized_data['code']) == str(self.sample_data['code'])
        assert str(deserialized_data['last_change_code']) == str(self.sample_data['last_change_code'])
        assert str(deserialized_data['insert_user_id']) == str(self.sample_data['insert_user_id'])
        assert str(deserialized_data['last_update_user_id']) == str(self.sample_data['last_update_user_id'])

        assert str(deserialized_data['customer_id']) == str(self.sample_data['customer_id'])
        assert str(deserialized_data['email']) == str(self.sample_data['email'])
        assert str(deserialized_data['organization_id']) == str(self.sample_data['organization_id'])

        assert deserialized_data['insert_utc_date_time'].isoformat() == self.sample_data['insert_utc_date_time']
        assert str(deserialized_data['customer_code_peek']) == str(self.sample_data['customer_code_peek'])   #CustomerID
        assert str(deserialized_data['organization_code_peek']) == str(self.sample_data['organization_code_peek']) #OrganizationID

        assert deserialized_data['last_update_utc_date_time'].isoformat() == self.sample_data['last_update_utc_date_time']
        new_org_customer = OrgCustomer(**deserialized_data)
        assert isinstance(new_org_customer, OrgCustomer)
    def test_to_json(self, org_customer:OrgCustomer, session):
            # Convert the OrgCustomer instance to JSON using the schema
            org_customer_schema = OrgCustomerSchema()
            org_customer_dict = org_customer_schema.dump(org_customer)
            # Convert the org_customer_dict to JSON string
            org_customer_json = json.dumps(org_customer_dict)
            # Convert the JSON strings back to dictionaries
            org_customer_dict_from_json = json.loads(org_customer_json)
            # sample_dict_from_json = json.loads(self.sample_data)
            # Verify the keys in both dictionaries match
            assert set(org_customer_dict_from_json.keys()) == set(self.sample_data.keys()), f"Expected keys: {set(self.sample_data.keys())}, Got: {set(org_customer_dict_from_json.keys())}"
            assert org_customer_dict_from_json['code'] == org_customer.code
            assert org_customer_dict_from_json['last_change_code'] == org_customer.last_change_code
            assert org_customer_dict_from_json['insert_user_id'] == org_customer.insert_user_id
            assert org_customer_dict_from_json['last_update_user_id'] == org_customer.last_update_user_id

            assert org_customer_dict_from_json['customer_id'] == org_customer.customer_id
            assert org_customer_dict_from_json['email'] == org_customer.email
            assert org_customer_dict_from_json['organization_id'] == org_customer.organization_id

            assert org_customer_dict_from_json['insert_utc_date_time'] == org_customer.insert_utc_date_time.isoformat()
            assert org_customer_dict_from_json['last_update_utc_date_time'] == org_customer.last_update_utc_date_time.isoformat()

            assert org_customer_dict_from_json['customer_code_peek'] == org_customer.customer_code_peek # CustomerID
            assert org_customer_dict_from_json['organization_code_peek'] == org_customer.organization_code_peek # OrganizationID

