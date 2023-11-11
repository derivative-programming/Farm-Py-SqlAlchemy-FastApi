from decimal import Decimal
import pytest
import time
from decimal import Decimal
from datetime import datetime, date
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, DateGreaterThanFilter
from models.factory import DateGreaterThanFilterFactory
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
class TestDateGreaterThanFilterFactory:
    @pytest.fixture(scope="module")
    def engine(self):
        engine = create_engine(DATABASE_URL, echo=False)
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
    def test_date_greater_than_filter_creation(self, session):
        date_greater_than_filter = DateGreaterThanFilterFactory.create(session=session)
        assert date_greater_than_filter.date_greater_than_filter_id is not None
    def test_code_default(self, session):
        date_greater_than_filter = DateGreaterThanFilterFactory.create(session=session)
        if db_dialect == 'postgresql':
            assert isinstance(date_greater_than_filter.code, UUID)
        elif db_dialect == 'mssql':
            assert isinstance(date_greater_than_filter.code, UNIQUEIDENTIFIER)
        else:  # This will cover SQLite, MySQL, and other databases
            assert isinstance(date_greater_than_filter.code, str)
    def test_last_change_code_default_on_build(self, session):
        date_greater_than_filter:DateGreaterThanFilter = DateGreaterThanFilterFactory.build(session=session)
        assert date_greater_than_filter.last_change_code == 0
    def test_last_change_code_default_on_creation(self, session):
        date_greater_than_filter:DateGreaterThanFilter = DateGreaterThanFilterFactory.create(session=session)
        assert date_greater_than_filter.last_change_code == 1
    def test_last_change_code_default_on_update(self, session):
        date_greater_than_filter = DateGreaterThanFilterFactory.create(session=session)
        initial_code = date_greater_than_filter.last_change_code
        date_greater_than_filter.code = generate_uuid()
        session.commit()
        assert date_greater_than_filter.last_change_code != initial_code
    def test_date_inserted_on_build(self, session):
        date_greater_than_filter = DateGreaterThanFilterFactory.build(session=session)
        assert date_greater_than_filter.insert_utc_date_time is not None
        assert isinstance(date_greater_than_filter.insert_utc_date_time, datetime)
    def test_date_inserted_on_initial_save(self, session):
        date_greater_than_filter = DateGreaterThanFilterFactory.build(session=session)
        assert date_greater_than_filter.insert_utc_date_time is not None
        assert isinstance(date_greater_than_filter.insert_utc_date_time, datetime)
        initial_time = date_greater_than_filter.insert_utc_date_time
        date_greater_than_filter.code = generate_uuid()
        time.sleep(1)
        session.commit()
        assert date_greater_than_filter.insert_utc_date_time > initial_time
    def test_date_inserted_on_second_save(self, session):
        date_greater_than_filter = DateGreaterThanFilterFactory(session=session)
        assert date_greater_than_filter.insert_utc_date_time is not None
        assert isinstance(date_greater_than_filter.insert_utc_date_time, datetime)
        initial_time = date_greater_than_filter.insert_utc_date_time
        date_greater_than_filter.code = generate_uuid()
        time.sleep(1)
        session.commit()
        assert date_greater_than_filter.insert_utc_date_time == initial_time
    def test_date_updated_on_build(self, session):
        date_greater_than_filter = DateGreaterThanFilterFactory.build(session=session)
        assert date_greater_than_filter.last_update_utc_date_time is not None
        assert isinstance(date_greater_than_filter.last_update_utc_date_time, datetime)
    def test_date_updated_on_initial_save(self, session):
        date_greater_than_filter = DateGreaterThanFilterFactory.build(session=session)
        assert date_greater_than_filter.last_update_utc_date_time is not None
        assert isinstance(date_greater_than_filter.last_update_utc_date_time, datetime)
        initial_time = date_greater_than_filter.last_update_utc_date_time
        date_greater_than_filter.code = generate_uuid()
        time.sleep(1)
        session.commit()
        assert date_greater_than_filter.last_update_utc_date_time > initial_time
    def test_date_updated_on_second_save(self, session):
        date_greater_than_filter = DateGreaterThanFilterFactory(session=session)
        assert date_greater_than_filter.last_update_utc_date_time is not None
        assert isinstance(date_greater_than_filter.last_update_utc_date_time, datetime)
        initial_time = date_greater_than_filter.last_update_utc_date_time
        date_greater_than_filter.code = generate_uuid()
        time.sleep(1)
        session.commit()
        assert date_greater_than_filter.last_update_utc_date_time > initial_time
    def test_model_deletion(self, session):
        date_greater_than_filter = DateGreaterThanFilterFactory.create(session=session)
        session.delete(date_greater_than_filter)
        session.commit()
        deleted_date_greater_than_filter = session.query(DateGreaterThanFilter).filter_by(date_greater_than_filter_id=date_greater_than_filter.date_greater_than_filter_id).first()
        assert deleted_date_greater_than_filter is None
    def test_data_types(self, session):
        date_greater_than_filter = DateGreaterThanFilterFactory.create(session=session)
        assert isinstance(date_greater_than_filter.date_greater_than_filter_id, int)
        if db_dialect == 'postgresql':
            assert isinstance(date_greater_than_filter.code, UUID)
        elif db_dialect == 'mssql':
            assert isinstance(date_greater_than_filter.code, UNIQUEIDENTIFIER)
        else:  # This will cover SQLite, MySQL, and other databases
            assert isinstance(date_greater_than_filter.code, str)
        assert isinstance(date_greater_than_filter.last_change_code, int)
        if db_dialect == 'postgresql':
            assert isinstance(date_greater_than_filter.insert_user_id, UUID)
        elif db_dialect == 'mssql':
            assert isinstance(date_greater_than_filter.insert_user_id, UNIQUEIDENTIFIER)
        else:  # This will cover SQLite, MySQL, and other databases
            assert isinstance(date_greater_than_filter.insert_user_id, str)
        if db_dialect == 'postgresql':
            assert isinstance(date_greater_than_filter.last_update_user_id, UUID)
        elif db_dialect == 'mssql':
            assert isinstance(date_greater_than_filter.last_update_user_id, UNIQUEIDENTIFIER)
        else:  # This will cover SQLite, MySQL, and other databases
            assert isinstance(date_greater_than_filter.last_update_user_id, str)
        assert isinstance(date_greater_than_filter.day_count, int)
        assert date_greater_than_filter.description == "" or isinstance(date_greater_than_filter.description, str)
        assert isinstance(date_greater_than_filter.display_order, int)
        assert isinstance(date_greater_than_filter.is_active, bool)
        assert date_greater_than_filter.lookup_enum_name == "" or isinstance(date_greater_than_filter.lookup_enum_name, str)
        assert date_greater_than_filter.name == "" or isinstance(date_greater_than_filter.name, str)
        assert isinstance(date_greater_than_filter.pac_id, int)
        # Check for the peek values, assuming they are UUIDs based on your model

        #dayCount,
        #description,
        #displayOrder,
        #isActive,
        #lookupEnumName,
        #name,
        #pacID
        if db_dialect == 'postgresql':
            assert isinstance(date_greater_than_filter.pac_code_peek, UUID)
        elif db_dialect == 'mssql':
            assert isinstance(date_greater_than_filter.pac_code_peek, UNIQUEIDENTIFIER)
        else:  # This will cover SQLite, MySQL, and other databases
            assert isinstance(date_greater_than_filter.pac_code_peek, str)

        assert isinstance(date_greater_than_filter.insert_utc_date_time, datetime)
        assert isinstance(date_greater_than_filter.last_update_utc_date_time, datetime)
    def test_unique_code_constraint(self, session):
        date_greater_than_filter_1 = DateGreaterThanFilterFactory.create(session=session)
        date_greater_than_filter_2 = DateGreaterThanFilterFactory.create(session=session)
        date_greater_than_filter_2.code = date_greater_than_filter_1.code
        session.add_all([date_greater_than_filter_1, date_greater_than_filter_2])
        with pytest.raises(Exception):  # adjust for the specific DB exception you'd expect
            session.commit()
        session.rollback()
    def test_fields_default(self, session):
        date_greater_than_filter = DateGreaterThanFilter()
        assert date_greater_than_filter.code is not None
        assert date_greater_than_filter.last_change_code is not None
        assert date_greater_than_filter.insert_user_id is None
        assert date_greater_than_filter.last_update_user_id is None
        assert date_greater_than_filter.insert_utc_date_time is not None
        assert date_greater_than_filter.last_update_utc_date_time is not None

        #dayCount,
        #description,
        #displayOrder,
        #isActive,
        #lookupEnumName,
        #name,
        #PacID
        if db_dialect == 'postgresql':
            assert isinstance(date_greater_than_filter.pac_code_peek, UUID)
        elif db_dialect == 'mssql':
            assert isinstance(date_greater_than_filter.pac_code_peek, UNIQUEIDENTIFIER)
        else:  # This will cover SQLite, MySQL, and other databases
            assert isinstance(date_greater_than_filter.pac_code_peek, str)

        assert date_greater_than_filter.day_count == 0
        assert date_greater_than_filter.description == ""
        assert date_greater_than_filter.display_order == 0
        assert date_greater_than_filter.is_active == False
        assert date_greater_than_filter.lookup_enum_name == ""
        assert date_greater_than_filter.name == ""
        assert date_greater_than_filter.pac_id == 0

    def test_last_change_code_concurrency(self, session):
        date_greater_than_filter = DateGreaterThanFilterFactory.create(session=session)
        original_last_change_code = date_greater_than_filter.last_change_code
        date_greater_than_filter_1 = session.query(DateGreaterThanFilter).filter_by(date_greater_than_filter_id=date_greater_than_filter.date_greater_than_filter_id).first()
        date_greater_than_filter_1.code = generate_uuid()
        session.commit()
        date_greater_than_filter_2 = session.query(DateGreaterThanFilter).filter_by(date_greater_than_filter_id=date_greater_than_filter.date_greater_than_filter_id).first()
        date_greater_than_filter_2.code = generate_uuid()
        session.commit()
        assert date_greater_than_filter_2.last_change_code != original_last_change_code

    #dayCount,
    #description,
    #displayOrder,
    #isActive,
    #lookupEnumName,
    #name,
    #PacID
    def test_invalid_pac_id(self, session):
        date_greater_than_filter = DateGreaterThanFilterFactory.create(session=session)
        date_greater_than_filter.pac_id = 99999
        with pytest.raises(IntegrityError):  # adjust for the specific DB exception you'd expect
            session.commit()
        session.rollback()

