import json
import pytest
import pytz
from models import DateGreaterThanFilter
from datetime import date, datetime
from decimal import Decimal
from models.serialization_schema import DateGreaterThanFilterSchema
from models.factory import DateGreaterThanFilterFactory
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base
from services.logging_config import get_logger
logger = get_logger(__name__)
DATABASE_URL = "sqlite:///:memory:"
class TestDateGreaterThanFilterSchema:
    # Sample data for a DateGreaterThanFilter instance
    sample_data = {
        "date_greater_than_filter_id": 1,
        "code": "a1b2c3d4-e5f6-7a8b-9c0d-123456789012",
        "last_change_code": 0,
        "insert_user_id": "a1b2c3d4-e5f6-7a8b-9c0d-123456789012",
        "last_update_user_id": "a1b2c3d4-e5f6-7a8b-9c0d-123456789012",

        "day_count": 42,
        "description": "Vanilla",
        "display_order": 42,
        "is_active": False,
        "lookup_enum_name": "Vanilla",
        "name": "Vanilla",
        "pac_id": 2,
        "insert_utc_date_time": datetime(2024, 1, 1, 12, 0, 0, tzinfo=pytz.utc).isoformat(),

        "pac_code_peek": "a1b2c3d4-e5f6-7a8b-9c0d-123456789012",# PacID

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

    def test_from_json(self, date_greater_than_filter:DateGreaterThanFilter, session):
        date_greater_than_filter_schema = DateGreaterThanFilterSchema()
        # Convert sample data to JSON string
        json_str = json.dumps(self.sample_data)
        # Deserialize the JSON string to a dictionary
        json_data = json.loads(json_str)
        # Load the dictionary to an object
        deserialized_data = date_greater_than_filter_schema.load(json_data)
        assert str(deserialized_data['date_greater_than_filter_id']) == str(self.sample_data['date_greater_than_filter_id'])
        assert str(deserialized_data['code']) == str(self.sample_data['code'])
        assert str(deserialized_data['last_change_code']) == str(self.sample_data['last_change_code'])
        assert str(deserialized_data['insert_user_id']) == str(self.sample_data['insert_user_id'])
        assert str(deserialized_data['last_update_user_id']) == str(self.sample_data['last_update_user_id'])

        assert str(deserialized_data['day_count']) == str(self.sample_data['day_count'])
        assert str(deserialized_data['description']) == str(self.sample_data['description'])
        assert str(deserialized_data['display_order']) == str(self.sample_data['display_order'])
        assert str(deserialized_data['is_active']) == str(self.sample_data['is_active'])
        assert str(deserialized_data['lookup_enum_name']) == str(self.sample_data['lookup_enum_name'])
        assert str(deserialized_data['name']) == str(self.sample_data['name'])
        assert str(deserialized_data['pac_id']) == str(self.sample_data['pac_id'])

        assert deserialized_data['insert_utc_date_time'].isoformat() == self.sample_data['insert_utc_date_time']
        assert str(deserialized_data['pac_code_peek']) == str(self.sample_data['pac_code_peek']) #PacID

        assert deserialized_data['last_update_utc_date_time'].isoformat() == self.sample_data['last_update_utc_date_time']
        new_date_greater_than_filter = DateGreaterThanFilter(**deserialized_data)
        assert isinstance(new_date_greater_than_filter, DateGreaterThanFilter)
    def test_to_json(self, date_greater_than_filter:DateGreaterThanFilter, session):
            # Convert the DateGreaterThanFilter instance to JSON using the schema
            date_greater_than_filter_schema = DateGreaterThanFilterSchema()
            date_greater_than_filter_dict = date_greater_than_filter_schema.dump(date_greater_than_filter)
            # Convert the date_greater_than_filter_dict to JSON string
            date_greater_than_filter_json = json.dumps(date_greater_than_filter_dict)
            # Convert the JSON strings back to dictionaries
            date_greater_than_filter_dict_from_json = json.loads(date_greater_than_filter_json)
            # sample_dict_from_json = json.loads(self.sample_data)
            # Verify the keys in both dictionaries match
            assert set(date_greater_than_filter_dict_from_json.keys()) == set(self.sample_data.keys()), f"Expected keys: {set(self.sample_data.keys())}, Got: {set(date_greater_than_filter_dict_from_json.keys())}"
            assert date_greater_than_filter_dict_from_json['code'] == date_greater_than_filter.code
            assert date_greater_than_filter_dict_from_json['last_change_code'] == date_greater_than_filter.last_change_code
            assert date_greater_than_filter_dict_from_json['insert_user_id'] == date_greater_than_filter.insert_user_id
            assert date_greater_than_filter_dict_from_json['last_update_user_id'] == date_greater_than_filter.last_update_user_id

            assert date_greater_than_filter_dict_from_json['day_count'] == date_greater_than_filter.day_count
            assert date_greater_than_filter_dict_from_json['description'] == date_greater_than_filter.description
            assert date_greater_than_filter_dict_from_json['display_order'] == date_greater_than_filter.display_order
            assert date_greater_than_filter_dict_from_json['is_active'] == date_greater_than_filter.is_active
            assert date_greater_than_filter_dict_from_json['lookup_enum_name'] == date_greater_than_filter.lookup_enum_name
            assert date_greater_than_filter_dict_from_json['name'] == date_greater_than_filter.name
            assert date_greater_than_filter_dict_from_json['pac_id'] == date_greater_than_filter.pac_id

            assert date_greater_than_filter_dict_from_json['insert_utc_date_time'] == date_greater_than_filter.insert_utc_date_time.isoformat()
            assert date_greater_than_filter_dict_from_json['last_update_utc_date_time'] == date_greater_than_filter.last_update_utc_date_time.isoformat()

            assert date_greater_than_filter_dict_from_json['pac_code_peek'] == date_greater_than_filter.pac_code_peek # PacID

