import pytest
from models import OrgApiKey
from models.serialization_schema import OrgApiKeySchema
from models.factory import OrgApiKeyFactory
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base
from services.logging_config import get_logger
logger = get_logger(__name__)
DATABASE_URL = "sqlite:///:memory:"
class TestOrgApiKeySchema:
    @pytest.fixture(scope="module")
    def engine(self):
        engine = create_engine(DATABASE_URL, echo=True)
        with engine.connect() as conn:
            conn.connection.execute("PRAGMA foreign_keys=ON")
        yield engine
        engine.dispose()
    @pytest.fixture
    def session(self, engine):
        Base.metadata.create_all(engine)
        SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)
        session_instance = SessionLocal()
        yield session_instance
        session_instance.close()
    @pytest.fixture
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

