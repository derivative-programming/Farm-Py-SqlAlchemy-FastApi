from decimal import Decimal
import pytest
import uuid
import time
from decimal import Decimal
from datetime import datetime, date
from sqlalchemy import Numeric, create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, ErrorLog
from models.factory import ErrorLogFactory
from services.db_config import db_dialect
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
from services.db_config import db_dialect,generate_uuid
from sqlalchemy import String
from sqlalchemy.exc import IntegrityError
DATABASE_URL = "sqlite:///:memory:"
db_dialect = "sqlite"
# Conditionally set the UUID column type
if db_dialect == 'postgresql':
    UUIDType = UUID(as_uuid=True)
elif db_dialect == 'mssql':
    UUIDType = UNIQUEIDENTIFIER
else:  # This will cover SQLite, MySQL, and other databases
    UUIDType = String(36)
class TestErrorLogFactory:
    @pytest.fixture(scope="module")
    def engine(self):
        engine = create_engine(DATABASE_URL, echo=True)
        #FKs are not activated by default in sqllite
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
    def test_error_log_creation(self, session):
        error_log = ErrorLogFactory.create(session=session)
        assert error_log.error_log_id is not None
    def test_code_default(self, session):
        error_log = ErrorLogFactory.create(session=session)
        if db_dialect == 'postgresql':
            assert isinstance(error_log.code, UUID)
        elif db_dialect == 'mssql':
            assert isinstance(error_log.code, UNIQUEIDENTIFIER)
        else:  # This will cover SQLite, MySQL, and other databases
            assert isinstance(error_log.code, str)
    def test_last_change_code_default_on_build(self, session):
        error_log:ErrorLog = ErrorLogFactory.build(session=session)
        assert error_log.last_change_code == 0
    def test_last_change_code_default_on_creation(self, session):
        error_log:ErrorLog = ErrorLogFactory.create(session=session)
        assert error_log.last_change_code == 1
    def test_last_change_code_default_on_update(self, session):
        error_log = ErrorLogFactory.create(session=session)
        initial_code = error_log.last_change_code
        error_log.code = generate_uuid()
        session.commit()
        assert error_log.last_change_code != initial_code
    def test_date_inserted_on_build(self, session):
        error_log = ErrorLogFactory.build(session=session)
        assert error_log.insert_utc_date_time is not None
        assert isinstance(error_log.insert_utc_date_time, datetime)
    def test_date_inserted_on_initial_save(self, session):
        error_log = ErrorLogFactory.build(session=session)
        assert error_log.insert_utc_date_time is not None
        assert isinstance(error_log.insert_utc_date_time, datetime)
        initial_time = error_log.insert_utc_date_time
        error_log.code = generate_uuid()
        time.sleep(2)
        session.commit()
        assert error_log.insert_utc_date_time > initial_time
    def test_date_inserted_on_second_save(self, session):
        error_log = ErrorLogFactory(session=session)
        assert error_log.insert_utc_date_time is not None
        assert isinstance(error_log.insert_utc_date_time, datetime)
        initial_time = error_log.insert_utc_date_time
        error_log.code = generate_uuid()
        time.sleep(2)
        session.commit()
        assert error_log.insert_utc_date_time == initial_time
    def test_date_updated_on_build(self, session):
        error_log = ErrorLogFactory.build(session=session)
        assert error_log.last_update_utc_date_time is not None
        assert isinstance(error_log.last_update_utc_date_time, datetime)
    def test_date_updated_on_initial_save(self, session):
        error_log = ErrorLogFactory.build(session=session)
        assert error_log.last_update_utc_date_time is not None
        assert isinstance(error_log.last_update_utc_date_time, datetime)
        initial_time = error_log.last_update_utc_date_time
        error_log.code = generate_uuid()
        time.sleep(2)
        session.commit()
        assert error_log.last_update_utc_date_time > initial_time
    def test_date_updated_on_second_save(self, session):
        error_log = ErrorLogFactory(session=session)
        assert error_log.last_update_utc_date_time is not None
        assert isinstance(error_log.last_update_utc_date_time, datetime)
        initial_time = error_log.last_update_utc_date_time
        error_log.code = generate_uuid()
        time.sleep(2)
        session.commit()
        assert error_log.last_update_utc_date_time > initial_time
    def test_model_deletion(self, session):
        error_log = ErrorLogFactory.create(session=session)
        session.delete(error_log)
        session.commit()
        deleted_error_log = session.query(ErrorLog).filter_by(error_log_id=error_log.error_log_id).first()
        assert deleted_error_log is None
    def test_data_types(self, session):
        error_log = ErrorLogFactory.create(session=session)
        assert isinstance(error_log.error_log_id, int)
        if db_dialect == 'postgresql':
            assert isinstance(error_log.code, UUID)
        elif db_dialect == 'mssql':
            assert isinstance(error_log.code, UNIQUEIDENTIFIER)
        else:  # This will cover SQLite, MySQL, and other databases
            assert isinstance(error_log.code, str)
        assert isinstance(error_log.last_change_code, int)
        if db_dialect == 'postgresql':
            assert isinstance(error_log.insert_user_id, UUID)
        elif db_dialect == 'mssql':
            assert isinstance(error_log.insert_user_id, UNIQUEIDENTIFIER)
        else:  # This will cover SQLite, MySQL, and other databases
            assert isinstance(error_log.insert_user_id, str)
        if db_dialect == 'postgresql':
            assert isinstance(error_log.last_update_user_id, UUID)
        elif db_dialect == 'mssql':
            assert isinstance(error_log.last_update_user_id, UNIQUEIDENTIFIER)
        else:  # This will cover SQLite, MySQL, and other databases
            assert isinstance(error_log.last_update_user_id, str)
        #BrowserCode
        if db_dialect == 'postgresql':
            assert isinstance(error_log.browser_code, UUID)
        elif db_dialect == 'mssql':
            assert isinstance(error_log.browser_code, UNIQUEIDENTIFIER)
        else:  # This will cover SQLite, MySQL, and other databases
            assert isinstance(error_log.browser_code, str)
        #ContextCode
        if db_dialect == 'postgresql':
            assert isinstance(error_log.context_code, UUID)
        elif db_dialect == 'mssql':
            assert isinstance(error_log.context_code, UNIQUEIDENTIFIER)
        else:  # This will cover SQLite, MySQL, and other databases
            assert isinstance(error_log.context_code, str)
        assert isinstance(error_log.created_utc_date_time, datetime)
        assert error_log.description == "" or isinstance(error_log.description, str)
        assert isinstance(error_log.is_client_side_error, bool)
        assert isinstance(error_log.is_resolved, bool)
        assert isinstance(error_log.pac_id, int)
        assert error_log.url == "" or isinstance(error_log.url, str)
        # Check for the peek values, assuming they are UUIDs based on your model

        #browserCode,
        #contextCode,
        #createdUTCDateTime
        #description,
        #isClientSideError,
        #isResolved,
        #pacID
        if db_dialect == 'postgresql':
            assert isinstance(error_log.pac_code_peek, UUID)
        elif db_dialect == 'mssql':
            assert isinstance(error_log.pac_code_peek, UNIQUEIDENTIFIER)
        else:  # This will cover SQLite, MySQL, and other databases
            assert isinstance(error_log.pac_code_peek, str)
        #url,

        assert isinstance(error_log.insert_utc_date_time, datetime)
        assert isinstance(error_log.last_update_utc_date_time, datetime)
    def test_unique_code_constraint(self, session):
        error_log_1 = ErrorLogFactory.create(session=session)
        error_log_2 = ErrorLogFactory.create(session=session)
        error_log_2.code = error_log_1.code
        session.add_all([error_log_1, error_log_2])
        with pytest.raises(Exception):  # adjust for the specific DB exception you'd expect
            session.commit()
        session.rollback()
    def test_fields_default(self, session):
        error_log = ErrorLog()
        assert error_log.code is not None
        assert error_log.last_change_code is not None
        assert error_log.insert_user_id is None
        assert error_log.last_update_user_id is None
        assert error_log.insert_utc_date_time is not None
        assert error_log.last_update_utc_date_time is not None

        #browserCode,
        #contextCode,
        #createdUTCDateTime
        #description,
        #isClientSideError,
        #isResolved,
        #PacID
        if db_dialect == 'postgresql':
            assert isinstance(error_log.pac_code_peek, UUID)
        elif db_dialect == 'mssql':
            assert isinstance(error_log.pac_code_peek, UNIQUEIDENTIFIER)
        else:  # This will cover SQLite, MySQL, and other databases
            assert isinstance(error_log.pac_code_peek, str)
        #url,

        #SomeUniqueIdentifierVal
        if db_dialect == 'postgresql':
            assert isinstance(error_log.browser_code, UUID)
        elif db_dialect == 'mssql':
            assert isinstance(error_log.browser_code, UNIQUEIDENTIFIER)
        else:  # This will cover SQLite, MySQL, and other databases
            assert isinstance(error_log.browser_code, str)
        #SomeUniqueIdentifierVal
        if db_dialect == 'postgresql':
            assert isinstance(error_log.context_code, UUID)
        elif db_dialect == 'mssql':
            assert isinstance(error_log.context_code, UNIQUEIDENTIFIER)
        else:  # This will cover SQLite, MySQL, and other databases
            assert isinstance(error_log.context_code, str)
        assert error_log.created_utc_date_time == datetime(1753, 1, 1)
        assert error_log.description == ""
        assert error_log.is_client_side_error == False
        assert error_log.is_resolved == False
        assert error_log.pac_id == 0
        assert error_log.url == ""

    def test_last_change_code_concurrency(self, session):
        error_log = ErrorLogFactory.create(session=session)
        original_last_change_code = error_log.last_change_code
        error_log_1 = session.query(ErrorLog).filter_by(error_log_id=error_log.error_log_id).first()
        error_log_1.code = generate_uuid()
        session.commit()
        error_log_2 = session.query(ErrorLog).filter_by(error_log_id=error_log.error_log_id).first()
        error_log_2.code = generate_uuid()
        session.commit()
        assert error_log_2.last_change_code != original_last_change_code

    #browserCode,
    #contextCode,
    #createdUTCDateTime
    #description,
    #isClientSideError,
    #isResolved,
    #PacID
    def test_invalid_pac_id(self, session):
        error_log = ErrorLogFactory.create(session=session)
        error_log.pac_id = 99999
        with pytest.raises(IntegrityError):  # adjust for the specific DB exception you'd expect
            session.commit()
        session.rollback()
    #url,

