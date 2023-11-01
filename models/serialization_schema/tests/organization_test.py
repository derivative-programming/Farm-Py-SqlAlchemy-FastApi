import json
import pytest
import pytz
from models import Organization
from datetime import date, datetime
from decimal import Decimal
from models.serialization_schema import OrganizationSchema
from models.factory import OrganizationFactory
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base
from services.logging_config import get_logger
logger = get_logger(__name__)
DATABASE_URL = "sqlite:///:memory:"
class TestOrganizationSchema:
    # Sample data for a Organization instance
    sample_data = {
        "organization_id": 1,
        "code": "a1b2c3d4-e5f6-7a8b-9c0d-123456789012",
        "last_change_code": 0,
        "insert_user_id": "a1b2c3d4-e5f6-7a8b-9c0d-123456789012",
        "last_update_user_id": "a1b2c3d4-e5f6-7a8b-9c0d-123456789012",

        "name": "Vanilla",
        "tac_id": 2,
        "insert_utc_date_time": datetime(2024, 1, 1, 12, 0, 0, tzinfo=pytz.utc).isoformat(),

        "tac_code_peek": "a1b2c3d4-e5f6-7a8b-9c0d-123456789012",# TacID

        "last_update_utc_date_time": datetime(2025, 1, 1, 12, 0, 0, tzinfo=pytz.utc).isoformat()
    }
    @pytest.fixture(scope="module")
    def engine(self):
        engine = create_engine(DATABASE_URL, echo=False)
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
    def organization(self, session):
        # Use the OrganizationFactory to create and return a organization instance
        return OrganizationFactory.create(session=session)
    # Tests
    def test_organization_serialization(self, organization:Organization, session):
        schema = OrganizationSchema()
        result = schema.dump(organization)
        assert result['code'] == organization.code
        assert result['last_change_code'] == organization.last_change_code
        assert result['insert_user_id'] == organization.insert_user_id
        assert result['last_update_user_id'] == organization.last_update_user_id

        assert result['name'] == organization.name
        assert result['tac_id'] == organization.tac_id

        assert result['insert_utc_date_time'] == organization.insert_utc_date_time.isoformat()
        assert result['last_update_utc_date_time'] == organization.last_update_utc_date_time.isoformat()

        assert result['tac_code_peek'] == organization.tac_code_peek # TacID

    def test_organization_deserialization(self, organization:Organization, session):
        schema = OrganizationSchema()
        serialized_data = schema.dump(organization)
        deserialized_data = schema.load(serialized_data)
        assert deserialized_data['code'] == organization.code
        assert deserialized_data['last_change_code'] == organization.last_change_code
        assert deserialized_data['insert_user_id'] == organization.insert_user_id
        assert deserialized_data['last_update_user_id'] == organization.last_update_user_id

        assert deserialized_data['name'] == organization.name
        assert deserialized_data['tac_id'] == organization.tac_id

        assert deserialized_data['insert_utc_date_time'].isoformat() == organization.insert_utc_date_time.isoformat()
        assert deserialized_data['last_update_utc_date_time'].isoformat() == organization.last_update_utc_date_time.isoformat()

        assert deserialized_data['tac_code_peek'] == organization.tac_code_peek # TacID

        new_organization = Organization(**deserialized_data)
        assert isinstance(new_organization, Organization)
        # Now compare the new_organization attributes with the organization attributes
        assert new_organization.code == organization.code
        assert new_organization.last_change_code == organization.last_change_code
        assert new_organization.insert_user_id == organization.insert_user_id
        assert new_organization.last_update_user_id == organization.last_update_user_id

        assert new_organization.name == organization.name
        assert new_organization.tac_id == organization.tac_id

        assert new_organization.insert_utc_date_time.isoformat() == organization.insert_utc_date_time.isoformat()
        assert new_organization.last_update_utc_date_time.isoformat() == organization.last_update_utc_date_time.isoformat()

        assert new_organization.tac_code_peek == organization.tac_code_peek #TacID

    def test_from_json(self, organization:Organization, session):
        organization_schema = OrganizationSchema()
        # Convert sample data to JSON string
        json_str = json.dumps(self.sample_data)
        # Deserialize the JSON string to a dictionary
        json_data = json.loads(json_str)
        # Load the dictionary to an object
        deserialized_data = organization_schema.load(json_data)
        assert str(deserialized_data['organization_id']) == str(self.sample_data['organization_id'])
        assert str(deserialized_data['code']) == str(self.sample_data['code'])
        assert str(deserialized_data['last_change_code']) == str(self.sample_data['last_change_code'])
        assert str(deserialized_data['insert_user_id']) == str(self.sample_data['insert_user_id'])
        assert str(deserialized_data['last_update_user_id']) == str(self.sample_data['last_update_user_id'])

        assert str(deserialized_data['name']) == str(self.sample_data['name'])
        assert str(deserialized_data['tac_id']) == str(self.sample_data['tac_id'])

        assert deserialized_data['insert_utc_date_time'].isoformat() == self.sample_data['insert_utc_date_time']
        assert str(deserialized_data['tac_code_peek']) == str(self.sample_data['tac_code_peek']) #TacID

        assert deserialized_data['last_update_utc_date_time'].isoformat() == self.sample_data['last_update_utc_date_time']
