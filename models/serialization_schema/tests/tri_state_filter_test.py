import pytest
from models import TriStateFilter
from models.serialization_schema import TriStateFilterSchema
from models.factory import TriStateFilterFactory
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base
from services.logging_config import get_logger
logger = get_logger(__name__)
DATABASE_URL = "sqlite:///:memory:"
class TestTriStateFilterSchema:
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
    def tri_state_filter(self, session):
        # Use the TriStateFilterFactory to create and return a tri_state_filter instance
        return TriStateFilterFactory.create(session=session)
    # Tests
    def test_tri_state_filter_serialization(self, tri_state_filter:TriStateFilter, session):
        schema = TriStateFilterSchema()
        result = schema.dump(tri_state_filter)
        assert result['code'] == tri_state_filter.code
        assert result['last_change_code'] == tri_state_filter.last_change_code
        assert result['insert_user_id'] == tri_state_filter.insert_user_id
        assert result['last_update_user_id'] == tri_state_filter.last_update_user_id

        assert result['description'] == tri_state_filter.description
        assert result['display_order'] == tri_state_filter.display_order
        assert result['is_active'] == tri_state_filter.is_active
        assert result['lookup_enum_name'] == tri_state_filter.lookup_enum_name
        assert result['name'] == tri_state_filter.name
        assert result['pac_id'] == tri_state_filter.pac_id
        assert result['state_int_value'] == tri_state_filter.state_int_value

        assert result['insert_utc_date_time'] == tri_state_filter.insert_utc_date_time.isoformat()
        assert result['last_update_utc_date_time'] == tri_state_filter.last_update_utc_date_time.isoformat()

        assert result['pac_code_peek'] == tri_state_filter.pac_code_peek # PacID

    def test_tri_state_filter_deserialization(self, tri_state_filter:TriStateFilter, session):
        schema = TriStateFilterSchema()
        serialized_data = schema.dump(tri_state_filter)
        deserialized_data = schema.load(serialized_data)
        assert deserialized_data['code'] == tri_state_filter.code
        assert deserialized_data['last_change_code'] == tri_state_filter.last_change_code
        assert deserialized_data['insert_user_id'] == tri_state_filter.insert_user_id
        assert deserialized_data['last_update_user_id'] == tri_state_filter.last_update_user_id

        assert deserialized_data['description'] == tri_state_filter.description
        assert deserialized_data['display_order'] == tri_state_filter.display_order
        assert deserialized_data['is_active'] == tri_state_filter.is_active
        assert deserialized_data['lookup_enum_name'] == tri_state_filter.lookup_enum_name
        assert deserialized_data['name'] == tri_state_filter.name
        assert deserialized_data['pac_id'] == tri_state_filter.pac_id
        assert deserialized_data['state_int_value'] == tri_state_filter.state_int_value

        assert deserialized_data['insert_utc_date_time'].isoformat() == tri_state_filter.insert_utc_date_time.isoformat()
        assert deserialized_data['last_update_utc_date_time'].isoformat() == tri_state_filter.last_update_utc_date_time.isoformat()

        assert deserialized_data['pac_code_peek'] == tri_state_filter.pac_code_peek # PacID

        new_tri_state_filter = TriStateFilter(**deserialized_data)
        assert isinstance(new_tri_state_filter, TriStateFilter)
        # Now compare the new_tri_state_filter attributes with the tri_state_filter attributes
        assert new_tri_state_filter.code == tri_state_filter.code
        assert new_tri_state_filter.last_change_code == tri_state_filter.last_change_code
        assert new_tri_state_filter.insert_user_id == tri_state_filter.insert_user_id
        assert new_tri_state_filter.last_update_user_id == tri_state_filter.last_update_user_id

        assert new_tri_state_filter.description == tri_state_filter.description
        assert new_tri_state_filter.display_order == tri_state_filter.display_order
        assert new_tri_state_filter.is_active == tri_state_filter.is_active
        assert new_tri_state_filter.lookup_enum_name == tri_state_filter.lookup_enum_name
        assert new_tri_state_filter.name == tri_state_filter.name
        assert new_tri_state_filter.pac_id == tri_state_filter.pac_id
        assert new_tri_state_filter.state_int_value == tri_state_filter.state_int_value

        assert new_tri_state_filter.insert_utc_date_time.isoformat() == tri_state_filter.insert_utc_date_time.isoformat()
        assert new_tri_state_filter.last_update_utc_date_time.isoformat() == tri_state_filter.last_update_utc_date_time.isoformat()

        assert new_tri_state_filter.pac_code_peek == tri_state_filter.pac_code_peek #PacID

