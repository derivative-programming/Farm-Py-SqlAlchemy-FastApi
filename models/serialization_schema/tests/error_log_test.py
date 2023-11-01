import pytest
from models import ErrorLog
from models.serialization_schema import ErrorLogSchema
from models.factory import ErrorLogFactory
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base
from services.logging_config import get_logger
logger = get_logger(__name__)
DATABASE_URL = "sqlite:///:memory:"
class TestErrorLogSchema:
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

