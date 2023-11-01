import pytest
from models import Role
from models.serialization_schema import RoleSchema
from models.factory import RoleFactory
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base
from services.logging_config import get_logger
logger = get_logger(__name__)
DATABASE_URL = "sqlite:///:memory:"
class TestRoleSchema:
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
    def role(self, session):
        # Use the RoleFactory to create and return a role instance
        return RoleFactory.create(session=session)
    # Tests
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

