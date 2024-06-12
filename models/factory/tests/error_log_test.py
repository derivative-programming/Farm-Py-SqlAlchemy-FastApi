# models/factory/tests/error_log_test.py
"""
    #TODO add comment
"""
from decimal import Decimal
import time
import math
from datetime import datetime, date, timedelta
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import String
from sqlalchemy.exc import IntegrityError
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
from models import Base, ErrorLog
from models.factory import ErrorLogFactory
from services.db_config import DB_DIALECT, generate_uuid
DATABASE_URL = "sqlite:///:memory:"
DB_DIALECT = "sqlite"  # noqa: F811
# Conditionally set the UUID column type
if DB_DIALECT == 'postgresql':
    UUIDType = UUID(as_uuid=True)
elif DB_DIALECT == 'mssql':
    UUIDType = UNIQUEIDENTIFIER
else:  # This will cover SQLite, MySQL, and other databases
    UUIDType = String(36)
class TestErrorLogFactory:
    """
    #TODO add comment
    """
    @pytest.fixture(scope="module")
    def engine(self):
        """
        #TODO add comment
        """
        engine = create_engine(DATABASE_URL, echo=False)
        #FKs are not activated by default in sqllite
        with engine.connect() as conn:
            conn.connection.execute("PRAGMA foreign_keys=ON")
        yield engine
        engine.dispose()
    @pytest.fixture
    def session(self, engine):
        """
        #TODO add comment
        """
        Base.metadata.create_all(engine)
        SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)
        session_instance = SessionLocal()
        yield session_instance
        session_instance.close()
    def test_error_log_creation(self, session):
        """
        #TODO add comment
        """
        error_log = ErrorLogFactory.create(session=session)
        assert error_log.error_log_id is not None
    def test_code_default(self, session):
        """
        #TODO add comment
        """
        error_log = ErrorLogFactory.create(session=session)
        if DB_DIALECT == 'postgresql':
            assert isinstance(error_log.code, UUID)
        elif DB_DIALECT == 'mssql':
            assert isinstance(error_log.code, UNIQUEIDENTIFIER)
        else:  # This will cover SQLite, MySQL, and other databases
            assert isinstance(error_log.code, str)
    def test_last_change_code_default_on_build(self, session):
        """
        #TODO add comment
        """
        error_log: ErrorLog = ErrorLogFactory.build(session=session)
        assert error_log.last_change_code == 0
    def test_last_change_code_default_on_creation(self, session):
        """
        #TODO add comment
        """
        error_log: ErrorLog = ErrorLogFactory.create(session=session)
        assert error_log.last_change_code == 1
    def test_last_change_code_default_on_update(self, session):
        """
        #TODO add comment
        """
        error_log = ErrorLogFactory.create(session=session)
        initial_code = error_log.last_change_code
        error_log.code = generate_uuid()
        session.commit()
        assert error_log.last_change_code != initial_code
    def test_date_inserted_on_build(self, session):
        """
        #TODO add comment
        """
        error_log = ErrorLogFactory.build(session=session)
        assert error_log.insert_utc_date_time is not None
        assert isinstance(error_log.insert_utc_date_time, datetime)
    def test_date_inserted_on_initial_save(self, session):
        """
        #TODO add comment
        """
        error_log = ErrorLogFactory.build(session=session)
        assert error_log.insert_utc_date_time is not None
        assert isinstance(error_log.insert_utc_date_time, datetime)
        initial_time = datetime.utcnow() + timedelta(days=-1)
        error_log.code = generate_uuid()
        session.commit()
        assert error_log.insert_utc_date_time > initial_time
    def test_date_inserted_on_second_save(self, session):
        """
        #TODO add comment
        """
        error_log = ErrorLogFactory(session=session)
        assert error_log.insert_utc_date_time is not None
        assert isinstance(error_log.insert_utc_date_time, datetime)
        initial_time = error_log.insert_utc_date_time
        error_log.code = generate_uuid()
        time.sleep(1)
        session.commit()
        assert error_log.insert_utc_date_time == initial_time
    def test_date_updated_on_build(self, session):
        """
        #TODO add comment
        """
        error_log = ErrorLogFactory.build(session=session)
        assert error_log.last_update_utc_date_time is not None
        assert isinstance(error_log.last_update_utc_date_time, datetime)
    def test_date_updated_on_initial_save(self, session):
        """
        #TODO add comment
        """
        error_log = ErrorLogFactory.build(session=session)
        assert error_log.last_update_utc_date_time is not None
        assert isinstance(error_log.last_update_utc_date_time, datetime)
        initial_time = datetime.utcnow() + timedelta(days=-1)
        error_log.code = generate_uuid()
        session.commit()
        assert error_log.last_update_utc_date_time > initial_time
    def test_date_updated_on_second_save(self, session):
        """
        #TODO add comment
        """
        error_log = ErrorLogFactory(session=session)
        assert error_log.last_update_utc_date_time is not None
        assert isinstance(error_log.last_update_utc_date_time, datetime)
        initial_time = error_log.last_update_utc_date_time
        error_log.code = generate_uuid()
        time.sleep(1)
        session.commit()
        assert error_log.last_update_utc_date_time > initial_time
    def test_model_deletion(self, session):
        """
        #TODO add comment
        """
        error_log = ErrorLogFactory.create(session=session)
        session.delete(error_log)
        session.commit()
        deleted_error_log = session.query(ErrorLog).filter_by(
            error_log_id=error_log.error_log_id).first()
        assert deleted_error_log is None
    def test_data_types(self, session):
        """
        #TODO add comment
        """
        error_log = ErrorLogFactory.create(session=session)
        assert isinstance(error_log.error_log_id, int)
        if DB_DIALECT == 'postgresql':
            assert isinstance(error_log.code, UUID)
        elif DB_DIALECT == 'mssql':
            assert isinstance(error_log.code, UNIQUEIDENTIFIER)
        else:  # This will cover SQLite, MySQL, and other databases
            assert isinstance(error_log.code, str)
        assert isinstance(error_log.last_change_code, int)
        if DB_DIALECT == 'postgresql':
            assert isinstance(error_log.insert_user_id, UUID)
        elif DB_DIALECT == 'mssql':
            assert isinstance(error_log.insert_user_id, UNIQUEIDENTIFIER)
        else:  # This will cover SQLite, MySQL, and other databases
            assert isinstance(error_log.insert_user_id, str)
        if DB_DIALECT == 'postgresql':
            assert isinstance(error_log.last_update_user_id, UUID)
        elif DB_DIALECT == 'mssql':
            assert isinstance(error_log.last_update_user_id, UNIQUEIDENTIFIER)
        else:  # This will cover SQLite, MySQL, and other databases
            assert isinstance(error_log.last_update_user_id, str)
        # browserCode
        if DB_DIALECT == 'postgresql':
            assert isinstance(
                error_log.browser_code, UUID)
        elif DB_DIALECT == 'mssql':
            assert isinstance(
                error_log.browser_code, UNIQUEIDENTIFIER)
        else:  # This will cover SQLite, MySQL, and other databases
            assert isinstance(error_log.browser_code, str)
        # contextCode
        if DB_DIALECT == 'postgresql':
            assert isinstance(
                error_log.context_code, UUID)
        elif DB_DIALECT == 'mssql':
            assert isinstance(
                error_log.context_code, UNIQUEIDENTIFIER)
        else:  # This will cover SQLite, MySQL, and other databases
            assert isinstance(error_log.context_code, str)
        assert isinstance(error_log.created_utc_date_time, datetime)
        assert error_log.description == "" or isinstance(error_log.description, str)
        assert isinstance(error_log.is_client_side_error, bool)
        assert isinstance(error_log.is_resolved, bool)
        assert isinstance(error_log.pac_id, int)
        assert error_log.url == "" or isinstance(error_log.url, str)
        # Check for the peek values,
        # assuming they are UUIDs based on your model
# endset
        # browserCode,
        # contextCode,
        # createdUTCDateTime
        # description,
        # isClientSideError,
        # isResolved,
        # pacID
        if DB_DIALECT == 'postgresql':
            assert isinstance(
                error_log.pac_code_peek, UUID)
        elif DB_DIALECT == 'mssql':
            assert isinstance(
                error_log.pac_code_peek, UNIQUEIDENTIFIER)
        else:  # This will cover SQLite, MySQL, and other databases
            assert isinstance(
                error_log.pac_code_peek, str)
        # url,
# endset
        assert isinstance(error_log.insert_utc_date_time, datetime)
        assert isinstance(error_log.last_update_utc_date_time, datetime)
    def test_unique_code_constraint(self, session):
        """
        #TODO add comment
        """
        error_log_1 = ErrorLogFactory.create(session=session)
        error_log_2 = ErrorLogFactory.create(session=session)
        error_log_2.code = error_log_1.code
        session.add_all([error_log_1, error_log_2])
        with pytest.raises(Exception):
            session.commit()
        session.rollback()
    def test_fields_default(self, session):
        """
        #TODO add comment
        """
        error_log = ErrorLog()
        assert error_log.code is not None
        assert error_log.last_change_code is not None
        assert error_log.insert_user_id is None
        assert error_log.last_update_user_id is None
        assert error_log.insert_utc_date_time is not None
        assert error_log.last_update_utc_date_time is not None
# endset
        # browserCode,
        # contextCode,
        # createdUTCDateTime
        # description,
        # isClientSideError,
        # isResolved,
        # PacID
        if DB_DIALECT == 'postgresql':
            assert isinstance(
                error_log.pac_code_peek, UUID)
        elif DB_DIALECT == 'mssql':
            assert isinstance(
                error_log.pac_code_peek,
                UNIQUEIDENTIFIER)
        else:  # This will cover SQLite, MySQL, and other databases
            assert isinstance(
                error_log.pac_code_peek, str)
        # url,
# endset
        # browser_code
        if DB_DIALECT == 'postgresql':
            assert isinstance(
                error_log.browser_code,
                UUID)
        elif DB_DIALECT == 'mssql':
            assert isinstance(
                error_log.browser_code,
                UNIQUEIDENTIFIER)
        else:  # This will cover SQLite, MySQL, and other databases
            assert isinstance(error_log.browser_code, str)
        # context_code
        if DB_DIALECT == 'postgresql':
            assert isinstance(
                error_log.context_code,
                UUID)
        elif DB_DIALECT == 'mssql':
            assert isinstance(
                error_log.context_code,
                UNIQUEIDENTIFIER)
        else:  # This will cover SQLite, MySQL, and other databases
            assert isinstance(error_log.context_code, str)
        assert error_log.created_utc_date_time == datetime(1753, 1, 1)
        assert error_log.description == ""
        assert error_log.is_client_side_error is False
        assert error_log.is_resolved is False
        assert error_log.pac_id == 0
        assert error_log.url == ""
# endset
    def test_last_change_code_concurrency(self, session):
        """
        #TODO add comment
        """
        error_log = ErrorLogFactory.create(session=session)
        original_last_change_code = error_log.last_change_code
        error_log_1 = session.query(ErrorLog).filter_by(
            error_log_id=error_log.error_log_id).first()
        error_log_1.code = generate_uuid()
        session.commit()
        error_log_2 = session.query(ErrorLog).filter_by(
            error_log_id=error_log.error_log_id).first()
        error_log_2.code = generate_uuid()
        session.commit()
        assert error_log_2.last_change_code != original_last_change_code
# endset
    # browserCode,
    # contextCode,
    # createdUTCDateTime
    # description,
    # isClientSideError,
    # isResolved,
    # PacID
    def test_invalid_pac_id(self, session):
        """
        #TODO add comment
        """
        error_log = ErrorLogFactory.create(session=session)
        error_log.pac_id = 99999
        with pytest.raises(IntegrityError):
            session.commit()
        session.rollback()
    # url,
# endset
