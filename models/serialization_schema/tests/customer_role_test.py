import pytest
from models import CustomerRole
from models.serialization_schema import CustomerRoleSchema
from models.factory import CustomerRoleFactory
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base
from services.logging_config import get_logger
logger = get_logger(__name__)
DATABASE_URL = "sqlite:///:memory:"
class TestCustomerRoleSchema:
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
    def customer_role(self, session):
        # Use the CustomerRoleFactory to create and return a customer_role instance
        return CustomerRoleFactory.create(session=session)
    # Tests
    def test_customer_role_serialization(self, customer_role:CustomerRole, session):
        schema = CustomerRoleSchema()
        result = schema.dump(customer_role)
        assert result['code'] == customer_role.code
        assert result['last_change_code'] == customer_role.last_change_code
        assert result['insert_user_id'] == customer_role.insert_user_id
        assert result['last_update_user_id'] == customer_role.last_update_user_id

        assert result['customer_id'] == customer_role.customer_id
        assert result['is_placeholder'] == customer_role.is_placeholder
        assert result['placeholder'] == customer_role.placeholder
        assert result['role_id'] == customer_role.role_id

        assert result['insert_utc_date_time'] == customer_role.insert_utc_date_time.isoformat()
        assert result['last_update_utc_date_time'] == customer_role.last_update_utc_date_time.isoformat()

        assert result['customer_code_peek'] == customer_role.customer_code_peek # CustomerID
        assert result['role_code_peek'] == customer_role.role_code_peek # RoleID

    def test_customer_role_deserialization(self, customer_role:CustomerRole, session):
        schema = CustomerRoleSchema()
        serialized_data = schema.dump(customer_role)
        deserialized_data = schema.load(serialized_data)
        assert deserialized_data['code'] == customer_role.code
        assert deserialized_data['last_change_code'] == customer_role.last_change_code
        assert deserialized_data['insert_user_id'] == customer_role.insert_user_id
        assert deserialized_data['last_update_user_id'] == customer_role.last_update_user_id

        assert deserialized_data['customer_id'] == customer_role.customer_id
        assert deserialized_data['is_placeholder'] == customer_role.is_placeholder
        assert deserialized_data['placeholder'] == customer_role.placeholder
        assert deserialized_data['role_id'] == customer_role.role_id

        assert deserialized_data['insert_utc_date_time'].isoformat() == customer_role.insert_utc_date_time.isoformat()
        assert deserialized_data['last_update_utc_date_time'].isoformat() == customer_role.last_update_utc_date_time.isoformat()

        assert deserialized_data['customer_code_peek'] == customer_role.customer_code_peek # CustomerID
        assert deserialized_data['role_code_peek'] == customer_role.role_code_peek # RoleID

        new_customer_role = CustomerRole(**deserialized_data)
        assert isinstance(new_customer_role, CustomerRole)
        # Now compare the new_customer_role attributes with the customer_role attributes
        assert new_customer_role.code == customer_role.code
        assert new_customer_role.last_change_code == customer_role.last_change_code
        assert new_customer_role.insert_user_id == customer_role.insert_user_id
        assert new_customer_role.last_update_user_id == customer_role.last_update_user_id

        assert new_customer_role.customer_id == customer_role.customer_id
        assert new_customer_role.is_placeholder == customer_role.is_placeholder
        assert new_customer_role.placeholder == customer_role.placeholder
        assert new_customer_role.role_id == customer_role.role_id

        assert new_customer_role.insert_utc_date_time.isoformat() == customer_role.insert_utc_date_time.isoformat()
        assert new_customer_role.last_update_utc_date_time.isoformat() == customer_role.last_update_utc_date_time.isoformat()

        assert new_customer_role.customer_code_peek == customer_role.customer_code_peek #CustomerID
        assert new_customer_role.role_code_peek == customer_role.role_code_peek  #RoleID

