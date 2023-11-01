import pytest
from models import OrgCustomer
from models.serialization_schema import OrgCustomerSchema
from models.factory import OrgCustomerFactory
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base
from services.logging_config import get_logger
logger = get_logger(__name__)
DATABASE_URL = "sqlite:///:memory:"
class TestOrgCustomerSchema:
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
    def org_customer(self, session):
        # Use the OrgCustomerFactory to create and return a org_customer instance
        return OrgCustomerFactory.create(session=session)
    # Tests
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

