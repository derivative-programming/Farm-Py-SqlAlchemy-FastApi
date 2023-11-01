import json
import pytest
import pytz
from models import ErrorLog
from datetime import date, datetime
from decimal import Decimal
from models.serialization_schema import ErrorLogSchema
from models.factory import ErrorLogFactory
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base
from services.logging_config import get_logger
logger = get_logger(__name__)
DATABASE_URL = "sqlite:///:memory:"
class TestErrorLogSchema:
    # Sample data for a ErrorLog instance
    sample_data = {
        "error_log_id": 1,
        "code": "a1b2c3d4-e5f6-7a8b-9c0d-123456789012",
        "last_change_code": 0,
        "insert_user_id": "a1b2c3d4-e5f6-7a8b-9c0d-123456789012",
        "last_update_user_id": "a1b2c3d4-e5f6-7a8b-9c0d-123456789012",

        "browser_code": "a1b2c3d4-e5f6-7a8b-9c0d-123456789012",
        "context_code": "a1b2c3d4-e5f6-7a8b-9c0d-123456789012",
        "created_utc_date_time": datetime(2023, 1, 1, 12, 0, 0, tzinfo=pytz.utc).isoformat(),
        "description": "Vanilla",
        "is_client_side_error": False,
        "is_resolved": False,
        "pac_id": 2,
        "url": "Vanilla",
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
    def error_log(self, session):
        # Use the ErrorLogFactory to create and return a error_log instance
        return ErrorLogFactory.create(session=session)
    # Tests
    def test_error_log_serialization(self, error_log:ErrorLog, session):
        schema = ErrorLogSchema()
        result = schema.dump(error_log)
        assert result['code'] == error_log.code
        assert result['last_change_code'] == error_log.last_change_code
        assert result['insert_user_id'] == error_log.insert_user_id
        assert result['last_update_user_id'] == error_log.last_update_user_id

        assert result['browser_code'] == error_log.browser_code
        assert result['context_code'] == error_log.context_code
        assert result['created_utc_date_time'] == error_log.created_utc_date_time.isoformat()
        assert result['description'] == error_log.description
        assert result['is_client_side_error'] == error_log.is_client_side_error
        assert result['is_resolved'] == error_log.is_resolved
        assert result['pac_id'] == error_log.pac_id
        assert result['url'] == error_log.url

        assert result['insert_utc_date_time'] == error_log.insert_utc_date_time.isoformat()
        assert result['last_update_utc_date_time'] == error_log.last_update_utc_date_time.isoformat()

        assert result['pac_code_peek'] == error_log.pac_code_peek # PacID

    def test_error_log_deserialization(self, error_log:ErrorLog, session):
        schema = ErrorLogSchema()
        serialized_data = schema.dump(error_log)
        deserialized_data = schema.load(serialized_data)
        assert deserialized_data['code'] == error_log.code
        assert deserialized_data['last_change_code'] == error_log.last_change_code
        assert deserialized_data['insert_user_id'] == error_log.insert_user_id
        assert deserialized_data['last_update_user_id'] == error_log.last_update_user_id

        assert deserialized_data['browser_code'] == error_log.browser_code
        assert deserialized_data['context_code'] == error_log.context_code
        assert deserialized_data['created_utc_date_time'].isoformat() == error_log.created_utc_date_time.isoformat()
        assert deserialized_data['description'] == error_log.description
        assert deserialized_data['is_client_side_error'] == error_log.is_client_side_error
        assert deserialized_data['is_resolved'] == error_log.is_resolved
        assert deserialized_data['pac_id'] == error_log.pac_id
        assert deserialized_data['url'] == error_log.url

        assert deserialized_data['insert_utc_date_time'].isoformat() == error_log.insert_utc_date_time.isoformat()
        assert deserialized_data['last_update_utc_date_time'].isoformat() == error_log.last_update_utc_date_time.isoformat()

        assert deserialized_data['pac_code_peek'] == error_log.pac_code_peek # PacID

        new_error_log = ErrorLog(**deserialized_data)
        assert isinstance(new_error_log, ErrorLog)
        # Now compare the new_error_log attributes with the error_log attributes
        assert new_error_log.code == error_log.code
        assert new_error_log.last_change_code == error_log.last_change_code
        assert new_error_log.insert_user_id == error_log.insert_user_id
        assert new_error_log.last_update_user_id == error_log.last_update_user_id

        assert new_error_log.browser_code == error_log.browser_code
        assert new_error_log.context_code == error_log.context_code
        assert new_error_log.created_utc_date_time.isoformat() == error_log.created_utc_date_time.isoformat()
        assert new_error_log.description == error_log.description
        assert new_error_log.is_client_side_error == error_log.is_client_side_error
        assert new_error_log.is_resolved == error_log.is_resolved
        assert new_error_log.pac_id == error_log.pac_id
        assert new_error_log.url == error_log.url

        assert new_error_log.insert_utc_date_time.isoformat() == error_log.insert_utc_date_time.isoformat()
        assert new_error_log.last_update_utc_date_time.isoformat() == error_log.last_update_utc_date_time.isoformat()

        assert new_error_log.pac_code_peek == error_log.pac_code_peek #PacID

    def test_from_json(self, error_log:ErrorLog, session):
        error_log_schema = ErrorLogSchema()
        # Convert sample data to JSON string
        json_str = json.dumps(self.sample_data)
        # Deserialize the JSON string to a dictionary
        json_data = json.loads(json_str)
        # Load the dictionary to an object
        deserialized_data = error_log_schema.load(json_data)
        assert str(deserialized_data['error_log_id']) == str(self.sample_data['error_log_id'])
        assert str(deserialized_data['code']) == str(self.sample_data['code'])
        assert str(deserialized_data['last_change_code']) == str(self.sample_data['last_change_code'])
        assert str(deserialized_data['insert_user_id']) == str(self.sample_data['insert_user_id'])
        assert str(deserialized_data['last_update_user_id']) == str(self.sample_data['last_update_user_id'])

        assert str(deserialized_data['browser_code']) == str(self.sample_data['browser_code'])
        assert str(deserialized_data['context_code']) == str(self.sample_data['context_code'])
        assert deserialized_data['created_utc_date_time'].isoformat() == self.sample_data['created_utc_date_time']
        assert str(deserialized_data['description']) == str(self.sample_data['description'])
        assert str(deserialized_data['is_client_side_error']) == str(self.sample_data['is_client_side_error'])
        assert str(deserialized_data['is_resolved']) == str(self.sample_data['is_resolved'])
        assert str(deserialized_data['pac_id']) == str(self.sample_data['pac_id'])
        assert str(deserialized_data['url']) == str(self.sample_data['url'])

        assert deserialized_data['insert_utc_date_time'].isoformat() == self.sample_data['insert_utc_date_time']
        assert str(deserialized_data['pac_code_peek']) == str(self.sample_data['pac_code_peek']) #PacID

        assert deserialized_data['last_update_utc_date_time'].isoformat() == self.sample_data['last_update_utc_date_time']
        new_error_log = ErrorLog(**deserialized_data)
        assert isinstance(new_error_log, ErrorLog)
    def test_to_json(self, error_log:ErrorLog, session):
            # Convert the ErrorLog instance to JSON using the schema
            error_log_schema = ErrorLogSchema()
            error_log_dict = error_log_schema.dump(error_log)
            # Convert the error_log_dict to JSON string
            error_log_json = json.dumps(error_log_dict)
            # Convert the JSON strings back to dictionaries
            error_log_dict_from_json = json.loads(error_log_json)
            # sample_dict_from_json = json.loads(self.sample_data)
            # Verify the keys in both dictionaries match
            assert set(error_log_dict_from_json.keys()) == set(self.sample_data.keys()), f"Expected keys: {set(self.sample_data.keys())}, Got: {set(error_log_dict_from_json.keys())}"
            assert error_log_dict_from_json['code'] == error_log.code
            assert error_log_dict_from_json['last_change_code'] == error_log.last_change_code
            assert error_log_dict_from_json['insert_user_id'] == error_log.insert_user_id
            assert error_log_dict_from_json['last_update_user_id'] == error_log.last_update_user_id

            assert error_log_dict_from_json['browser_code'] == error_log.browser_code
            assert error_log_dict_from_json['context_code'] == error_log.context_code
            assert error_log_dict_from_json['created_utc_date_time'] == error_log.created_utc_date_time.isoformat()
            assert error_log_dict_from_json['description'] == error_log.description
            assert error_log_dict_from_json['is_client_side_error'] == error_log.is_client_side_error
            assert error_log_dict_from_json['is_resolved'] == error_log.is_resolved
            assert error_log_dict_from_json['pac_id'] == error_log.pac_id
            assert error_log_dict_from_json['url'] == error_log.url

            assert error_log_dict_from_json['insert_utc_date_time'] == error_log.insert_utc_date_time.isoformat()
            assert error_log_dict_from_json['last_update_utc_date_time'] == error_log.last_update_utc_date_time.isoformat()

            assert error_log_dict_from_json['pac_code_peek'] == error_log.pac_code_peek # PacID

