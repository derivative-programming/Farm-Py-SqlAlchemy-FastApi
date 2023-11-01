import pytest
from models import DateGreaterThanFilter
from models.serialization_schema import DateGreaterThanFilterSchema
from models.factory import DateGreaterThanFilterFactory
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base
from services.logging_config import get_logger
logger = get_logger(__name__)
DATABASE_URL = "sqlite:///:memory:"
class TestDateGreaterThanFilterSchema:
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
    def date_greater_than_filter(self, session):
        # Use the DateGreaterThanFilterFactory to create and return a date_greater_than_filter instance
        return DateGreaterThanFilterFactory.create(session=session)
    # Tests
    def test_date_greater_than_filter_serialization(self, date_greater_than_filter:DateGreaterThanFilter, session):
        schema = DateGreaterThanFilterSchema()
        result = schema.dump(date_greater_than_filter)
        assert result['code'] == date_greater_than_filter.code
        assert result['last_change_code'] == date_greater_than_filter.last_change_code
        assert result['insert_user_id'] == date_greater_than_filter.insert_user_id
        assert result['last_update_user_id'] == date_greater_than_filter.last_update_user_id

        assert result['day_count'] == date_greater_than_filter.day_count
        assert result['description'] == date_greater_than_filter.description
        assert result['display_order'] == date_greater_than_filter.display_order
        assert result['is_active'] == date_greater_than_filter.is_active
        assert result['lookup_enum_name'] == date_greater_than_filter.lookup_enum_name
        assert result['name'] == date_greater_than_filter.name
        assert result['pac_id'] == date_greater_than_filter.pac_id

        assert result['insert_utc_date_time'] == date_greater_than_filter.insert_utc_date_time.isoformat()
        assert result['last_update_utc_date_time'] == date_greater_than_filter.last_update_utc_date_time.isoformat()

        assert result['pac_code_peek'] == date_greater_than_filter.pac_code_peek # PacID

    def test_date_greater_than_filter_deserialization(self, date_greater_than_filter:DateGreaterThanFilter, session):
        schema = DateGreaterThanFilterSchema()
        serialized_data = schema.dump(date_greater_than_filter)
        deserialized_data = schema.load(serialized_data)
        assert deserialized_data['code'] == date_greater_than_filter.code
        assert deserialized_data['last_change_code'] == date_greater_than_filter.last_change_code
        assert deserialized_data['insert_user_id'] == date_greater_than_filter.insert_user_id
        assert deserialized_data['last_update_user_id'] == date_greater_than_filter.last_update_user_id

        assert deserialized_data['day_count'] == date_greater_than_filter.day_count
        assert deserialized_data['description'] == date_greater_than_filter.description
        assert deserialized_data['display_order'] == date_greater_than_filter.display_order
        assert deserialized_data['is_active'] == date_greater_than_filter.is_active
        assert deserialized_data['lookup_enum_name'] == date_greater_than_filter.lookup_enum_name
        assert deserialized_data['name'] == date_greater_than_filter.name
        assert deserialized_data['pac_id'] == date_greater_than_filter.pac_id

        assert deserialized_data['insert_utc_date_time'].isoformat() == date_greater_than_filter.insert_utc_date_time.isoformat()
        assert deserialized_data['last_update_utc_date_time'].isoformat() == date_greater_than_filter.last_update_utc_date_time.isoformat()

        assert deserialized_data['pac_code_peek'] == date_greater_than_filter.pac_code_peek # PacID

        new_date_greater_than_filter = DateGreaterThanFilter(**deserialized_data)
        assert isinstance(new_date_greater_than_filter, DateGreaterThanFilter)
        # Now compare the new_date_greater_than_filter attributes with the date_greater_than_filter attributes
        assert new_date_greater_than_filter.code == date_greater_than_filter.code
        assert new_date_greater_than_filter.last_change_code == date_greater_than_filter.last_change_code
        assert new_date_greater_than_filter.insert_user_id == date_greater_than_filter.insert_user_id
        assert new_date_greater_than_filter.last_update_user_id == date_greater_than_filter.last_update_user_id

        assert new_date_greater_than_filter.day_count == date_greater_than_filter.day_count
        assert new_date_greater_than_filter.description == date_greater_than_filter.description
        assert new_date_greater_than_filter.display_order == date_greater_than_filter.display_order
        assert new_date_greater_than_filter.is_active == date_greater_than_filter.is_active
        assert new_date_greater_than_filter.lookup_enum_name == date_greater_than_filter.lookup_enum_name
        assert new_date_greater_than_filter.name == date_greater_than_filter.name
        assert new_date_greater_than_filter.pac_id == date_greater_than_filter.pac_id

        assert new_date_greater_than_filter.insert_utc_date_time.isoformat() == date_greater_than_filter.insert_utc_date_time.isoformat()
        assert new_date_greater_than_filter.last_update_utc_date_time.isoformat() == date_greater_than_filter.last_update_utc_date_time.isoformat()

        assert new_date_greater_than_filter.pac_code_peek == date_greater_than_filter.pac_code_peek #PacID

