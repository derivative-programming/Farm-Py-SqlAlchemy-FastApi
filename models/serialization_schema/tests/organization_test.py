import pytest
from models import Organization
from models.serialization_schema import OrganizationSchema
from models.factory import OrganizationFactory
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base
from services.logging_config import get_logger
logger = get_logger(__name__)
DATABASE_URL = "sqlite:///:memory:"
class TestOrganizationSchema:
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

