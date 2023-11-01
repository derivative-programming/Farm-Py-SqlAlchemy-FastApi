import pytest
from models import Flavor
from models.serialization_schema import FlavorSchema
from models.factory import FlavorFactory
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base
from services.logging_config import get_logger
logger = get_logger(__name__)
DATABASE_URL = "sqlite:///:memory:"
class TestFlavorSchema:
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
    def flavor(self, session):
        # Use the FlavorFactory to create and return a flavor instance
        return FlavorFactory.create(session=session)
    # Tests
    def test_flavor_serialization(self, flavor:Flavor, session):
        schema = FlavorSchema()
        result = schema.dump(flavor)
        assert result['code'] == flavor.code
        assert result['last_change_code'] == flavor.last_change_code
        assert result['insert_user_id'] == flavor.insert_user_id
        assert result['last_update_user_id'] == flavor.last_update_user_id

        assert result['description'] == flavor.description
        assert result['display_order'] == flavor.display_order
        assert result['is_active'] == flavor.is_active
        assert result['lookup_enum_name'] == flavor.lookup_enum_name
        assert result['name'] == flavor.name
        assert result['pac_id'] == flavor.pac_id

        assert result['insert_utc_date_time'] == flavor.insert_utc_date_time.isoformat()
        assert result['last_update_utc_date_time'] == flavor.last_update_utc_date_time.isoformat()

        assert result['pac_code_peek'] == flavor.pac_code_peek # PacID

    def test_flavor_deserialization(self, flavor:Flavor, session):
        schema = FlavorSchema()
        serialized_data = schema.dump(flavor)
        deserialized_data = schema.load(serialized_data)
        assert deserialized_data['code'] == flavor.code
        assert deserialized_data['last_change_code'] == flavor.last_change_code
        assert deserialized_data['insert_user_id'] == flavor.insert_user_id
        assert deserialized_data['last_update_user_id'] == flavor.last_update_user_id

        assert deserialized_data['description'] == flavor.description
        assert deserialized_data['display_order'] == flavor.display_order
        assert deserialized_data['is_active'] == flavor.is_active
        assert deserialized_data['lookup_enum_name'] == flavor.lookup_enum_name
        assert deserialized_data['name'] == flavor.name
        assert deserialized_data['pac_id'] == flavor.pac_id

        assert deserialized_data['insert_utc_date_time'].isoformat() == flavor.insert_utc_date_time.isoformat()
        assert deserialized_data['last_update_utc_date_time'].isoformat() == flavor.last_update_utc_date_time.isoformat()

        assert deserialized_data['pac_code_peek'] == flavor.pac_code_peek # PacID

        new_flavor = Flavor(**deserialized_data)
        assert isinstance(new_flavor, Flavor)
        # Now compare the new_flavor attributes with the flavor attributes
        assert new_flavor.code == flavor.code
        assert new_flavor.last_change_code == flavor.last_change_code
        assert new_flavor.insert_user_id == flavor.insert_user_id
        assert new_flavor.last_update_user_id == flavor.last_update_user_id

        assert new_flavor.description == flavor.description
        assert new_flavor.display_order == flavor.display_order
        assert new_flavor.is_active == flavor.is_active
        assert new_flavor.lookup_enum_name == flavor.lookup_enum_name
        assert new_flavor.name == flavor.name
        assert new_flavor.pac_id == flavor.pac_id

        assert new_flavor.insert_utc_date_time.isoformat() == flavor.insert_utc_date_time.isoformat()
        assert new_flavor.last_update_utc_date_time.isoformat() == flavor.last_update_utc_date_time.isoformat()

        assert new_flavor.pac_code_peek == flavor.pac_code_peek #PacID

