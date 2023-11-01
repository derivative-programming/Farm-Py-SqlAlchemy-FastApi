import pytest
from models import Land
from models.serialization_schema import LandSchema
from models.factory import LandFactory
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base
from services.logging_config import get_logger
logger = get_logger(__name__)
DATABASE_URL = "sqlite:///:memory:"
class TestLandSchema:
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
    def land(self, session):
        # Use the LandFactory to create and return a land instance
        return LandFactory.create(session=session)
    # Tests
    def test_land_serialization(self, land:Land, session):
        schema = LandSchema()
        result = schema.dump(land)
        assert result['code'] == land.code
        assert result['last_change_code'] == land.last_change_code
        assert result['insert_user_id'] == land.insert_user_id
        assert result['last_update_user_id'] == land.last_update_user_id

        assert result['description'] == land.description
        assert result['display_order'] == land.display_order
        assert result['is_active'] == land.is_active
        assert result['lookup_enum_name'] == land.lookup_enum_name
        assert result['name'] == land.name
        assert result['pac_id'] == land.pac_id

        assert result['insert_utc_date_time'] == land.insert_utc_date_time.isoformat()
        assert result['last_update_utc_date_time'] == land.last_update_utc_date_time.isoformat()

        assert result['pac_code_peek'] == land.pac_code_peek # PacID

    def test_land_deserialization(self, land:Land, session):
        schema = LandSchema()
        serialized_data = schema.dump(land)
        deserialized_data = schema.load(serialized_data)
        assert deserialized_data['code'] == land.code
        assert deserialized_data['last_change_code'] == land.last_change_code
        assert deserialized_data['insert_user_id'] == land.insert_user_id
        assert deserialized_data['last_update_user_id'] == land.last_update_user_id

        assert deserialized_data['description'] == land.description
        assert deserialized_data['display_order'] == land.display_order
        assert deserialized_data['is_active'] == land.is_active
        assert deserialized_data['lookup_enum_name'] == land.lookup_enum_name
        assert deserialized_data['name'] == land.name
        assert deserialized_data['pac_id'] == land.pac_id

        assert deserialized_data['insert_utc_date_time'].isoformat() == land.insert_utc_date_time.isoformat()
        assert deserialized_data['last_update_utc_date_time'].isoformat() == land.last_update_utc_date_time.isoformat()

        assert deserialized_data['pac_code_peek'] == land.pac_code_peek # PacID

        new_land = Land(**deserialized_data)
        assert isinstance(new_land, Land)
        # Now compare the new_land attributes with the land attributes
        assert new_land.code == land.code
        assert new_land.last_change_code == land.last_change_code
        assert new_land.insert_user_id == land.insert_user_id
        assert new_land.last_update_user_id == land.last_update_user_id

        assert new_land.description == land.description
        assert new_land.display_order == land.display_order
        assert new_land.is_active == land.is_active
        assert new_land.lookup_enum_name == land.lookup_enum_name
        assert new_land.name == land.name
        assert new_land.pac_id == land.pac_id

        assert new_land.insert_utc_date_time.isoformat() == land.insert_utc_date_time.isoformat()
        assert new_land.last_update_utc_date_time.isoformat() == land.last_update_utc_date_time.isoformat()

        assert new_land.pac_code_peek == land.pac_code_peek #PacID

