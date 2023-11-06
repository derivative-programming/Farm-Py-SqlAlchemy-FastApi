import json
import pytest
import pytz
from models import OrgApiKey
from datetime import date, datetime
from decimal import Decimal
from models.serialization_schema import OrgApiKeySchema
from models.factory import OrgApiKeyFactory
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base
from services.logging_config import get_logger
logger = get_logger(__name__)
DATABASE_URL = "sqlite:///:memory:"
class TestOrgApiKeySchema:
    # Sample data for a OrgApiKey instance
    sample_data = {
        "org_api_key_id": 1,
        "code": "a1b2c3d4-e5f6-7a8b-9c0d-123456789012",
        "last_change_code": 0,
        "insert_user_id": "a1b2c3d4-e5f6-7a8b-9c0d-123456789012",
        "last_update_user_id": "a1b2c3d4-e5f6-7a8b-9c0d-123456789012",

        "api_key_value": "Vanilla",
        "created_by": "Vanilla",
        "created_utc_date_time": datetime(2023, 1, 1, 12, 0, 0, tzinfo=pytz.utc).isoformat(),
        "expiration_utc_date_time": datetime(2023, 1, 1, 12, 0, 0, tzinfo=pytz.utc).isoformat(),
        "is_active": False,
        "is_temp_user_key": False,
        "name": "Vanilla",
        "organization_id": 2,
        "org_customer_id": 1,
        "insert_utc_date_time": datetime(2024, 1, 1, 12, 0, 0, tzinfo=pytz.utc).isoformat(),

        "organization_code_peek": "a1b2c3d4-e5f6-7a8b-9c0d-123456789012",# OrganizationID
        "org_customer_code_peek": "a1b2c3d4-e5f6-7a8b-9c0d-123456789012",# OrgCustomerID

        "last_update_utc_date_time": datetime(2025, 1, 1, 12, 0, 0, tzinfo=pytz.utc).isoformat()
    }
    @pytest.fixture(scope="module")
    def engine(self):
        engine = create_engine(DATABASE_URL, echo=False)
        with engine.connect() as conn:
            conn.connection.execute("PRAGMA foreign_keys=ON")
        yield engine
        engine.dispose()
    @pytest.fixture(scope="function")
    def session(self, engine):
        Base.metadata.create_all(engine)
        SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)
        session_instance = SessionLocal()
        yield session_instance
        session_instance.close()
    @pytest.fixture(scope="function")
    def org_api_key(self, session):
        # Use the OrgApiKeyFactory to create and return a org_api_key instance
        return OrgApiKeyFactory.create(session=session)
    # Tests
    def test_org_api_key_serialization(self, org_api_key:OrgApiKey, session):
        schema = OrgApiKeySchema()
        result = schema.dump(org_api_key)
        assert result['code'] == org_api_key.code
        assert result['last_change_code'] == org_api_key.last_change_code
        assert result['insert_user_id'] == org_api_key.insert_user_id
        assert result['last_update_user_id'] == org_api_key.last_update_user_id

        assert result['api_key_value'] == org_api_key.api_key_value
        assert result['created_by'] == org_api_key.created_by
        assert result['created_utc_date_time'] == org_api_key.created_utc_date_time.isoformat()
        assert result['expiration_utc_date_time'] == org_api_key.expiration_utc_date_time.isoformat()
        assert result['is_active'] == org_api_key.is_active
        assert result['is_temp_user_key'] == org_api_key.is_temp_user_key
        assert result['name'] == org_api_key.name
        assert result['organization_id'] == org_api_key.organization_id
        assert result['org_customer_id'] == org_api_key.org_customer_id

        assert result['insert_utc_date_time'] == org_api_key.insert_utc_date_time.isoformat()
        assert result['last_update_utc_date_time'] == org_api_key.last_update_utc_date_time.isoformat()

        assert result['organization_code_peek'] == org_api_key.organization_code_peek # OrganizationID
        assert result['org_customer_code_peek'] == org_api_key.org_customer_code_peek # OrgCustomerID

    def test_org_api_key_deserialization(self, org_api_key:OrgApiKey, session):
        schema = OrgApiKeySchema()
        serialized_data = schema.dump(org_api_key)
        deserialized_data = schema.load(serialized_data)
        assert deserialized_data['code'] == org_api_key.code
        assert deserialized_data['last_change_code'] == org_api_key.last_change_code
        assert deserialized_data['insert_user_id'] == org_api_key.insert_user_id
        assert deserialized_data['last_update_user_id'] == org_api_key.last_update_user_id

        assert deserialized_data['api_key_value'] == org_api_key.api_key_value
        assert deserialized_data['created_by'] == org_api_key.created_by
        assert deserialized_data['created_utc_date_time'].isoformat() == org_api_key.created_utc_date_time.isoformat()
        assert deserialized_data['expiration_utc_date_time'].isoformat() == org_api_key.expiration_utc_date_time.isoformat()
        assert deserialized_data['is_active'] == org_api_key.is_active
        assert deserialized_data['is_temp_user_key'] == org_api_key.is_temp_user_key
        assert deserialized_data['name'] == org_api_key.name
        assert deserialized_data['organization_id'] == org_api_key.organization_id
        assert deserialized_data['org_customer_id'] == org_api_key.org_customer_id

        assert deserialized_data['insert_utc_date_time'].isoformat() == org_api_key.insert_utc_date_time.isoformat()
        assert deserialized_data['last_update_utc_date_time'].isoformat() == org_api_key.last_update_utc_date_time.isoformat()

        assert deserialized_data['organization_code_peek'] == org_api_key.organization_code_peek # OrganizationID
        assert deserialized_data['org_customer_code_peek'] == org_api_key.org_customer_code_peek # OrgCustomerID

        new_org_api_key = OrgApiKey(**deserialized_data)
        assert isinstance(new_org_api_key, OrgApiKey)
        # Now compare the new_org_api_key attributes with the org_api_key attributes
        assert new_org_api_key.code == org_api_key.code
        assert new_org_api_key.last_change_code == org_api_key.last_change_code
        assert new_org_api_key.insert_user_id == org_api_key.insert_user_id
        assert new_org_api_key.last_update_user_id == org_api_key.last_update_user_id

        assert new_org_api_key.api_key_value == org_api_key.api_key_value
        assert new_org_api_key.created_by == org_api_key.created_by
        assert new_org_api_key.created_utc_date_time.isoformat() == org_api_key.created_utc_date_time.isoformat()
        assert new_org_api_key.expiration_utc_date_time.isoformat() == org_api_key.expiration_utc_date_time.isoformat()
        assert new_org_api_key.is_active == org_api_key.is_active
        assert new_org_api_key.is_temp_user_key == org_api_key.is_temp_user_key
        assert new_org_api_key.name == org_api_key.name
        assert new_org_api_key.organization_id == org_api_key.organization_id
        assert new_org_api_key.org_customer_id == org_api_key.org_customer_id

        assert new_org_api_key.insert_utc_date_time.isoformat() == org_api_key.insert_utc_date_time.isoformat()
        assert new_org_api_key.last_update_utc_date_time.isoformat() == org_api_key.last_update_utc_date_time.isoformat()

        assert new_org_api_key.organization_code_peek == org_api_key.organization_code_peek #OrganizationID
        assert new_org_api_key.org_customer_code_peek == org_api_key.org_customer_code_peek  #OrgCustomerID

    def test_from_json(self, org_api_key:OrgApiKey, session):
        org_api_key_schema = OrgApiKeySchema()
        # Convert sample data to JSON string
        json_str = json.dumps(self.sample_data)
        # Deserialize the JSON string to a dictionary
        json_data = json.loads(json_str)
        # Load the dictionary to an object
        deserialized_data = org_api_key_schema.load(json_data)
        assert str(deserialized_data['org_api_key_id']) == str(self.sample_data['org_api_key_id'])
        assert str(deserialized_data['code']) == str(self.sample_data['code'])
        assert str(deserialized_data['last_change_code']) == str(self.sample_data['last_change_code'])
        assert str(deserialized_data['insert_user_id']) == str(self.sample_data['insert_user_id'])
        assert str(deserialized_data['last_update_user_id']) == str(self.sample_data['last_update_user_id'])

        assert str(deserialized_data['api_key_value']) == str(self.sample_data['api_key_value'])
        assert str(deserialized_data['created_by']) == str(self.sample_data['created_by'])
        assert deserialized_data['created_utc_date_time'].isoformat() == self.sample_data['created_utc_date_time']
        assert deserialized_data['expiration_utc_date_time'].isoformat() == self.sample_data['expiration_utc_date_time']
        assert str(deserialized_data['is_active']) == str(self.sample_data['is_active'])
        assert str(deserialized_data['is_temp_user_key']) == str(self.sample_data['is_temp_user_key'])
        assert str(deserialized_data['name']) == str(self.sample_data['name'])
        assert str(deserialized_data['organization_id']) == str(self.sample_data['organization_id'])
        assert str(deserialized_data['org_customer_id']) == str(self.sample_data['org_customer_id'])

        assert deserialized_data['insert_utc_date_time'].isoformat() == self.sample_data['insert_utc_date_time']
        assert str(deserialized_data['organization_code_peek']) == str(self.sample_data['organization_code_peek']) #OrganizationID
        assert str(deserialized_data['org_customer_code_peek']) == str(self.sample_data['org_customer_code_peek'])   #OrgCustomerID

        assert deserialized_data['last_update_utc_date_time'].isoformat() == self.sample_data['last_update_utc_date_time']
        new_org_api_key = OrgApiKey(**deserialized_data)
        assert isinstance(new_org_api_key, OrgApiKey)
    def test_to_json(self, org_api_key:OrgApiKey, session):
            # Convert the OrgApiKey instance to JSON using the schema
            org_api_key_schema = OrgApiKeySchema()
            org_api_key_dict = org_api_key_schema.dump(org_api_key)
            # Convert the org_api_key_dict to JSON string
            org_api_key_json = json.dumps(org_api_key_dict)
            # Convert the JSON strings back to dictionaries
            org_api_key_dict_from_json = json.loads(org_api_key_json)
            # sample_dict_from_json = json.loads(self.sample_data)
            # Verify the keys in both dictionaries match
            assert set(org_api_key_dict_from_json.keys()) == set(self.sample_data.keys()), f"Expected keys: {set(self.sample_data.keys())}, Got: {set(org_api_key_dict_from_json.keys())}"
            assert org_api_key_dict_from_json['code'] == org_api_key.code
            assert org_api_key_dict_from_json['last_change_code'] == org_api_key.last_change_code
            assert org_api_key_dict_from_json['insert_user_id'] == org_api_key.insert_user_id
            assert org_api_key_dict_from_json['last_update_user_id'] == org_api_key.last_update_user_id

            assert org_api_key_dict_from_json['api_key_value'] == org_api_key.api_key_value
            assert org_api_key_dict_from_json['created_by'] == org_api_key.created_by
            assert org_api_key_dict_from_json['created_utc_date_time'] == org_api_key.created_utc_date_time.isoformat()
            assert org_api_key_dict_from_json['expiration_utc_date_time'] == org_api_key.expiration_utc_date_time.isoformat()
            assert org_api_key_dict_from_json['is_active'] == org_api_key.is_active
            assert org_api_key_dict_from_json['is_temp_user_key'] == org_api_key.is_temp_user_key
            assert org_api_key_dict_from_json['name'] == org_api_key.name
            assert org_api_key_dict_from_json['organization_id'] == org_api_key.organization_id
            assert org_api_key_dict_from_json['org_customer_id'] == org_api_key.org_customer_id

            assert org_api_key_dict_from_json['insert_utc_date_time'] == org_api_key.insert_utc_date_time.isoformat()
            assert org_api_key_dict_from_json['last_update_utc_date_time'] == org_api_key.last_update_utc_date_time.isoformat()

            assert org_api_key_dict_from_json['organization_code_peek'] == org_api_key.organization_code_peek # OrganizationID
            assert org_api_key_dict_from_json['org_customer_code_peek'] == org_api_key.org_customer_code_peek # OrgCustomerID

