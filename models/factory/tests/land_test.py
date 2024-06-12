# models/factory/tests/land_test.py
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
from models import Base, Land
from models.factory import LandFactory
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
class TestLandFactory:
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
    def test_land_creation(self, session):
        """
        #TODO add comment
        """
        land = LandFactory.create(session=session)
        assert land.land_id is not None
    def test_code_default(self, session):
        """
        #TODO add comment
        """
        land = LandFactory.create(session=session)
        if DB_DIALECT == 'postgresql':
            assert isinstance(land.code, UUID)
        elif DB_DIALECT == 'mssql':
            assert isinstance(land.code, UNIQUEIDENTIFIER)
        else:  # This will cover SQLite, MySQL, and other databases
            assert isinstance(land.code, str)
    def test_last_change_code_default_on_build(self, session):
        """
        #TODO add comment
        """
        land: Land = LandFactory.build(session=session)
        assert land.last_change_code == 0
    def test_last_change_code_default_on_creation(self, session):
        """
        #TODO add comment
        """
        land: Land = LandFactory.create(session=session)
        assert land.last_change_code == 1
    def test_last_change_code_default_on_update(self, session):
        """
        #TODO add comment
        """
        land = LandFactory.create(session=session)
        initial_code = land.last_change_code
        land.code = generate_uuid()
        session.commit()
        assert land.last_change_code != initial_code
    def test_date_inserted_on_build(self, session):
        """
        #TODO add comment
        """
        land = LandFactory.build(session=session)
        assert land.insert_utc_date_time is not None
        assert isinstance(land.insert_utc_date_time, datetime)
    def test_date_inserted_on_initial_save(self, session):
        """
        #TODO add comment
        """
        land = LandFactory.build(session=session)
        assert land.insert_utc_date_time is not None
        assert isinstance(land.insert_utc_date_time, datetime)
        initial_time = datetime.utcnow() + timedelta(days=-1)
        land.code = generate_uuid()
        session.commit()
        assert land.insert_utc_date_time > initial_time
    def test_date_inserted_on_second_save(self, session):
        """
        #TODO add comment
        """
        land = LandFactory(session=session)
        assert land.insert_utc_date_time is not None
        assert isinstance(land.insert_utc_date_time, datetime)
        initial_time = land.insert_utc_date_time
        land.code = generate_uuid()
        time.sleep(1)
        session.commit()
        assert land.insert_utc_date_time == initial_time
    def test_date_updated_on_build(self, session):
        """
        #TODO add comment
        """
        land = LandFactory.build(session=session)
        assert land.last_update_utc_date_time is not None
        assert isinstance(land.last_update_utc_date_time, datetime)
    def test_date_updated_on_initial_save(self, session):
        """
        #TODO add comment
        """
        land = LandFactory.build(session=session)
        assert land.last_update_utc_date_time is not None
        assert isinstance(land.last_update_utc_date_time, datetime)
        initial_time = datetime.utcnow() + timedelta(days=-1)
        land.code = generate_uuid()
        session.commit()
        assert land.last_update_utc_date_time > initial_time
    def test_date_updated_on_second_save(self, session):
        """
        #TODO add comment
        """
        land = LandFactory(session=session)
        assert land.last_update_utc_date_time is not None
        assert isinstance(land.last_update_utc_date_time, datetime)
        initial_time = land.last_update_utc_date_time
        land.code = generate_uuid()
        time.sleep(1)
        session.commit()
        assert land.last_update_utc_date_time > initial_time
    def test_model_deletion(self, session):
        """
        #TODO add comment
        """
        land = LandFactory.create(session=session)
        session.delete(land)
        session.commit()
        deleted_land = session.query(Land).filter_by(
            land_id=land.land_id).first()
        assert deleted_land is None
    def test_data_types(self, session):
        """
        #TODO add comment
        """
        land = LandFactory.create(session=session)
        assert isinstance(land.land_id, int)
        if DB_DIALECT == 'postgresql':
            assert isinstance(land.code, UUID)
        elif DB_DIALECT == 'mssql':
            assert isinstance(land.code, UNIQUEIDENTIFIER)
        else:  # This will cover SQLite, MySQL, and other databases
            assert isinstance(land.code, str)
        assert isinstance(land.last_change_code, int)
        if DB_DIALECT == 'postgresql':
            assert isinstance(land.insert_user_id, UUID)
        elif DB_DIALECT == 'mssql':
            assert isinstance(land.insert_user_id, UNIQUEIDENTIFIER)
        else:  # This will cover SQLite, MySQL, and other databases
            assert isinstance(land.insert_user_id, str)
        if DB_DIALECT == 'postgresql':
            assert isinstance(land.last_update_user_id, UUID)
        elif DB_DIALECT == 'mssql':
            assert isinstance(land.last_update_user_id, UNIQUEIDENTIFIER)
        else:  # This will cover SQLite, MySQL, and other databases
            assert isinstance(land.last_update_user_id, str)
        assert land.description == "" or isinstance(land.description, str)
        assert isinstance(land.display_order, int)
        assert isinstance(land.is_active, bool)
        assert land.lookup_enum_name == "" or isinstance(land.lookup_enum_name, str)
        assert land.name == "" or isinstance(land.name, str)
        assert isinstance(land.pac_id, int)
        # Check for the peek values,
        # assuming they are UUIDs based on your model
# endset
        # description,
        # displayOrder,
        # isActive,
        # lookupEnumName,
        # name,
        # pacID
        if DB_DIALECT == 'postgresql':
            assert isinstance(
                land.pac_code_peek, UUID)
        elif DB_DIALECT == 'mssql':
            assert isinstance(
                land.pac_code_peek, UNIQUEIDENTIFIER)
        else:  # This will cover SQLite, MySQL, and other databases
            assert isinstance(
                land.pac_code_peek, str)
# endset
        assert isinstance(land.insert_utc_date_time, datetime)
        assert isinstance(land.last_update_utc_date_time, datetime)
    def test_unique_code_constraint(self, session):
        """
        #TODO add comment
        """
        land_1 = LandFactory.create(session=session)
        land_2 = LandFactory.create(session=session)
        land_2.code = land_1.code
        session.add_all([land_1, land_2])
        with pytest.raises(Exception):
            session.commit()
        session.rollback()
    def test_fields_default(self, session):
        """
        #TODO add comment
        """
        land = Land()
        assert land.code is not None
        assert land.last_change_code is not None
        assert land.insert_user_id is None
        assert land.last_update_user_id is None
        assert land.insert_utc_date_time is not None
        assert land.last_update_utc_date_time is not None
# endset
        # description,
        # displayOrder,
        # isActive,
        # lookupEnumName,
        # name,
        # PacID
        if DB_DIALECT == 'postgresql':
            assert isinstance(
                land.pac_code_peek, UUID)
        elif DB_DIALECT == 'mssql':
            assert isinstance(
                land.pac_code_peek,
                UNIQUEIDENTIFIER)
        else:  # This will cover SQLite, MySQL, and other databases
            assert isinstance(
                land.pac_code_peek, str)
# endset
        assert land.description == ""
        assert land.display_order == 0
        assert land.is_active is False
        assert land.lookup_enum_name == ""
        assert land.name == ""
        assert land.pac_id == 0
# endset
    def test_last_change_code_concurrency(self, session):
        """
        #TODO add comment
        """
        land = LandFactory.create(session=session)
        original_last_change_code = land.last_change_code
        land_1 = session.query(Land).filter_by(
            land_id=land.land_id).first()
        land_1.code = generate_uuid()
        session.commit()
        land_2 = session.query(Land).filter_by(
            land_id=land.land_id).first()
        land_2.code = generate_uuid()
        session.commit()
        assert land_2.last_change_code != original_last_change_code
# endset
    # description,
    # displayOrder,
    # isActive,
    # lookupEnumName,
    # name,
    # PacID
    def test_invalid_pac_id(self, session):
        """
        #TODO add comment
        """
        land = LandFactory.create(session=session)
        land.pac_id = 99999
        with pytest.raises(IntegrityError):
            session.commit()
        session.rollback()
# endset
