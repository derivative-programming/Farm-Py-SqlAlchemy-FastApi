from decimal import Decimal
import pytest
import uuid
import time
from decimal import Decimal
from datetime import datetime, date
from sqlalchemy import Numeric, create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Land
from models.factory import LandFactory
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
class TestLandFactory:
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
    def test_land_creation(self, session):
        land = LandFactory.create(session=session)
        assert land.land_id is not None
    def test_code_default(self, session):
        land = LandFactory.create(session=session)
        if db_dialect == 'postgresql':
            assert isinstance(land.code, UUID)
        elif db_dialect == 'mssql':
            assert isinstance(land.code, UNIQUEIDENTIFIER)
        else:  # This will cover SQLite, MySQL, and other databases
            assert isinstance(land.code, str)
    def test_last_change_code_default_on_build(self, session):
        land:Land = LandFactory.build(session=session)
        assert land.last_change_code == 0
    def test_last_change_code_default_on_creation(self, session):
        land:Land = LandFactory.create(session=session)
        assert land.last_change_code == 1
    def test_last_change_code_default_on_update(self, session):
        land = LandFactory.create(session=session)
        initial_code = land.last_change_code
        land.code = generate_uuid()
        session.commit()
        assert land.last_change_code != initial_code
    def test_date_inserted_on_build(self, session):
        land = LandFactory.build(session=session)
        assert land.insert_utc_date_time is not None
        assert isinstance(land.insert_utc_date_time, datetime)
    def test_date_inserted_on_initial_save(self, session):
        land = LandFactory.build(session=session)
        assert land.insert_utc_date_time is not None
        assert isinstance(land.insert_utc_date_time, datetime)
        initial_time = land.insert_utc_date_time
        land.code = generate_uuid()
        time.sleep(2)
        session.commit()
        assert land.insert_utc_date_time > initial_time
    def test_date_inserted_on_second_save(self, session):
        land = LandFactory(session=session)
        assert land.insert_utc_date_time is not None
        assert isinstance(land.insert_utc_date_time, datetime)
        initial_time = land.insert_utc_date_time
        land.code = generate_uuid()
        time.sleep(2)
        session.commit()
        assert land.insert_utc_date_time == initial_time
    def test_date_updated_on_build(self, session):
        land = LandFactory.build(session=session)
        assert land.last_update_utc_date_time is not None
        assert isinstance(land.last_update_utc_date_time, datetime)
    def test_date_updated_on_initial_save(self, session):
        land = LandFactory.build(session=session)
        assert land.last_update_utc_date_time is not None
        assert isinstance(land.last_update_utc_date_time, datetime)
        initial_time = land.last_update_utc_date_time
        land.code = generate_uuid()
        time.sleep(2)
        session.commit()
        assert land.last_update_utc_date_time > initial_time
    def test_date_updated_on_second_save(self, session):
        land = LandFactory(session=session)
        assert land.last_update_utc_date_time is not None
        assert isinstance(land.last_update_utc_date_time, datetime)
        initial_time = land.last_update_utc_date_time
        land.code = generate_uuid()
        time.sleep(2)
        session.commit()
        assert land.last_update_utc_date_time > initial_time
    def test_model_deletion(self, session):
        land = LandFactory.create(session=session)
        session.delete(land)
        session.commit()
        deleted_land = session.query(Land).filter_by(land_id=land.land_id).first()
        assert deleted_land is None
    def test_data_types(self, session):
        land = LandFactory.create(session=session)
        assert isinstance(land.land_id, int)
        if db_dialect == 'postgresql':
            assert isinstance(land.code, UUID)
        elif db_dialect == 'mssql':
            assert isinstance(land.code, UNIQUEIDENTIFIER)
        else:  # This will cover SQLite, MySQL, and other databases
            assert isinstance(land.code, str)
        assert isinstance(land.last_change_code, int)
        if db_dialect == 'postgresql':
            assert isinstance(land.insert_user_id, UUID)
        elif db_dialect == 'mssql':
            assert isinstance(land.insert_user_id, UNIQUEIDENTIFIER)
        else:  # This will cover SQLite, MySQL, and other databases
            assert isinstance(land.insert_user_id, str)
        if db_dialect == 'postgresql':
            assert isinstance(land.last_update_user_id, UUID)
        elif db_dialect == 'mssql':
            assert isinstance(land.last_update_user_id, UNIQUEIDENTIFIER)
        else:  # This will cover SQLite, MySQL, and other databases
            assert isinstance(land.last_update_user_id, str)
        assert land.description == "" or isinstance(land.description, str)
        assert isinstance(land.display_order, int)
        assert isinstance(land.is_active, bool)
        assert land.lookup_enum_name == "" or isinstance(land.lookup_enum_name, str)
        assert land.name == "" or isinstance(land.name, str)
        assert isinstance(land.pac_id, int)
        # Check for the peek values, assuming they are UUIDs based on your model

        #description,
        #displayOrder,
        #isActive,
        #lookupEnumName,
        #name,
        #pacID
        if db_dialect == 'postgresql':
            assert isinstance(land.pac_code_peek, UUID)
        elif db_dialect == 'mssql':
            assert isinstance(land.pac_code_peek, UNIQUEIDENTIFIER)
        else:  # This will cover SQLite, MySQL, and other databases
            assert isinstance(land.pac_code_peek, str)

        assert isinstance(land.insert_utc_date_time, datetime)
        assert isinstance(land.last_update_utc_date_time, datetime)
    def test_unique_code_constraint(self, session):
        land_1 = LandFactory.create(session=session)
        land_2 = LandFactory.create(session=session)
        land_2.code = land_1.code
        session.add_all([land_1, land_2])
        with pytest.raises(Exception):  # adjust for the specific DB exception you'd expect
            session.commit()
    def test_fields_default(self, session):
        land = Land()
        assert land.code is not None
        assert land.last_change_code is not None
        assert land.insert_user_id is None
        assert land.last_update_user_id is None
        assert land.insert_utc_date_time is not None
        assert land.last_update_utc_date_time is not None

        #description,
        #displayOrder,
        #isActive,
        #lookupEnumName,
        #name,
        #PacID
        if db_dialect == 'postgresql':
            assert isinstance(land.pac_code_peek, UUID)
        elif db_dialect == 'mssql':
            assert isinstance(land.pac_code_peek, UNIQUEIDENTIFIER)
        else:  # This will cover SQLite, MySQL, and other databases
            assert isinstance(land.pac_code_peek, str)

        assert land.description == ""
        assert land.display_order == 0
        assert land.is_active == False
        assert land.lookup_enum_name == ""
        assert land.name == ""
        assert land.pac_id == 0

    def test_last_change_code_concurrency(self, session):
        land = LandFactory.create(session=session)
        original_last_change_code = land.last_change_code
        land_1 = session.query(Land).filter_by(land_id=land.land_id).first()
        land_1.code = generate_uuid()
        session.commit()
        land_2 = session.query(Land).filter_by(land_id=land.land_id).first()
        land_2.code = generate_uuid()
        session.commit()
        assert land_2.last_change_code != original_last_change_code

    #description,
    #displayOrder,
    #isActive,
    #lookupEnumName,
    #name,
    #PacID
    def test_invalid_pac_id(self, session):
        land = LandFactory.create(session=session)
        land.pac_id = 99999
        with pytest.raises(IntegrityError):  # adjust for the specific DB exception you'd expect
            session.commit()

