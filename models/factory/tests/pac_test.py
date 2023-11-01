from decimal import Decimal
import pytest
import uuid
import time
from decimal import Decimal
from datetime import datetime, date
from sqlalchemy import Numeric, create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Pac
from models.factory import PacFactory
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
class TestPacFactory:
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
    def test_pac_creation(self, session):
        pac = PacFactory.create(session=session)
        assert pac.pac_id is not None
    def test_code_default(self, session):
        pac = PacFactory.create(session=session)
        if db_dialect == 'postgresql':
            assert isinstance(pac.code, UUID)
        elif db_dialect == 'mssql':
            assert isinstance(pac.code, UNIQUEIDENTIFIER)
        else:  # This will cover SQLite, MySQL, and other databases
            assert isinstance(pac.code, str)
    def test_last_change_code_default_on_build(self, session):
        pac:Pac = PacFactory.build(session=session)
        assert pac.last_change_code == 0
    def test_last_change_code_default_on_creation(self, session):
        pac:Pac = PacFactory.create(session=session)
        assert pac.last_change_code == 1
    def test_last_change_code_default_on_update(self, session):
        pac = PacFactory.create(session=session)
        initial_code = pac.last_change_code
        pac.code = generate_uuid()
        session.commit()
        assert pac.last_change_code != initial_code
    def test_date_inserted_on_build(self, session):
        pac = PacFactory.build(session=session)
        assert pac.insert_utc_date_time is not None
        assert isinstance(pac.insert_utc_date_time, datetime)
    def test_date_inserted_on_initial_save(self, session):
        pac = PacFactory.build(session=session)
        assert pac.insert_utc_date_time is not None
        assert isinstance(pac.insert_utc_date_time, datetime)
        initial_time = pac.insert_utc_date_time
        pac.code = generate_uuid()
        time.sleep(2)
        session.commit()
        assert pac.insert_utc_date_time > initial_time
    def test_date_inserted_on_second_save(self, session):
        pac = PacFactory(session=session)
        assert pac.insert_utc_date_time is not None
        assert isinstance(pac.insert_utc_date_time, datetime)
        initial_time = pac.insert_utc_date_time
        pac.code = generate_uuid()
        time.sleep(2)
        session.commit()
        assert pac.insert_utc_date_time == initial_time
    def test_date_updated_on_build(self, session):
        pac = PacFactory.build(session=session)
        assert pac.last_update_utc_date_time is not None
        assert isinstance(pac.last_update_utc_date_time, datetime)
    def test_date_updated_on_initial_save(self, session):
        pac = PacFactory.build(session=session)
        assert pac.last_update_utc_date_time is not None
        assert isinstance(pac.last_update_utc_date_time, datetime)
        initial_time = pac.last_update_utc_date_time
        pac.code = generate_uuid()
        time.sleep(2)
        session.commit()
        assert pac.last_update_utc_date_time > initial_time
    def test_date_updated_on_second_save(self, session):
        pac = PacFactory(session=session)
        assert pac.last_update_utc_date_time is not None
        assert isinstance(pac.last_update_utc_date_time, datetime)
        initial_time = pac.last_update_utc_date_time
        pac.code = generate_uuid()
        time.sleep(2)
        session.commit()
        assert pac.last_update_utc_date_time > initial_time
    def test_model_deletion(self, session):
        pac = PacFactory.create(session=session)
        session.delete(pac)
        session.commit()
        deleted_pac = session.query(Pac).filter_by(pac_id=pac.pac_id).first()
        assert deleted_pac is None
    def test_data_types(self, session):
        pac = PacFactory.create(session=session)
        assert isinstance(pac.pac_id, int)
        if db_dialect == 'postgresql':
            assert isinstance(pac.code, UUID)
        elif db_dialect == 'mssql':
            assert isinstance(pac.code, UNIQUEIDENTIFIER)
        else:  # This will cover SQLite, MySQL, and other databases
            assert isinstance(pac.code, str)
        assert isinstance(pac.last_change_code, int)
        if db_dialect == 'postgresql':
            assert isinstance(pac.insert_user_id, UUID)
        elif db_dialect == 'mssql':
            assert isinstance(pac.insert_user_id, UNIQUEIDENTIFIER)
        else:  # This will cover SQLite, MySQL, and other databases
            assert isinstance(pac.insert_user_id, str)
        if db_dialect == 'postgresql':
            assert isinstance(pac.last_update_user_id, UUID)
        elif db_dialect == 'mssql':
            assert isinstance(pac.last_update_user_id, UNIQUEIDENTIFIER)
        else:  # This will cover SQLite, MySQL, and other databases
            assert isinstance(pac.last_update_user_id, str)
        assert pac.description == "" or isinstance(pac.description, str)
        assert isinstance(pac.display_order, int)
        assert isinstance(pac.is_active, bool)
        assert pac.lookup_enum_name == "" or isinstance(pac.lookup_enum_name, str)
        assert pac.name == "" or isinstance(pac.name, str)
        # Check for the peek values, assuming they are UUIDs based on your model

        #description,
        #displayOrder,
        #isActive,
        #lookupEnumName,
        #name,

        assert isinstance(pac.insert_utc_date_time, datetime)
        assert isinstance(pac.last_update_utc_date_time, datetime)
    def test_unique_code_constraint(self, session):
        pac_1 = PacFactory.create(session=session)
        pac_2 = PacFactory.create(session=session)
        pac_2.code = pac_1.code
        session.add_all([pac_1, pac_2])
        with pytest.raises(Exception):  # adjust for the specific DB exception you'd expect
            session.commit()
    def test_fields_default(self, session):
        pac = Pac()
        assert pac.code is not None
        assert pac.last_change_code is not None
        assert pac.insert_user_id is None
        assert pac.last_update_user_id is None
        assert pac.insert_utc_date_time is not None
        assert pac.last_update_utc_date_time is not None

        #description,
        #displayOrder,
        #isActive,
        #lookupEnumName,
        #name,

        assert pac.description == ""
        assert pac.display_order == 0
        assert pac.is_active == False
        assert pac.lookup_enum_name == ""
        assert pac.name == ""

    def test_last_change_code_concurrency(self, session):
        pac = PacFactory.create(session=session)
        original_last_change_code = pac.last_change_code
        pac_1 = session.query(Pac).filter_by(pac_id=pac.pac_id).first()
        pac_1.code = generate_uuid()
        session.commit()
        pac_2 = session.query(Pac).filter_by(pac_id=pac.pac_id).first()
        pac_2.code = generate_uuid()
        session.commit()
        assert pac_2.last_change_code != original_last_change_code

    #description,
    #displayOrder,
    #isActive,
    #lookupEnumName,
    #name,

