# models/factory/tests/tac_test.py
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
from models import Base, Tac
from models.factory import TacFactory
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
class TestTacFactory:
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
    def test_tac_creation(self, session):
        """
        #TODO add comment
        """
        tac = TacFactory.create(session=session)
        assert tac.tac_id is not None
    def test_code_default(self, session):
        """
        #TODO add comment
        """
        tac = TacFactory.create(session=session)
        if DB_DIALECT == 'postgresql':
            assert isinstance(tac.code, UUID)
        elif DB_DIALECT == 'mssql':
            assert isinstance(tac.code, UNIQUEIDENTIFIER)
        else:  # This will cover SQLite, MySQL, and other databases
            assert isinstance(tac.code, str)
    def test_last_change_code_default_on_build(self, session):
        """
        #TODO add comment
        """
        tac: Tac = TacFactory.build(session=session)
        assert tac.last_change_code == 0
    def test_last_change_code_default_on_creation(self, session):
        """
        #TODO add comment
        """
        tac: Tac = TacFactory.create(session=session)
        assert tac.last_change_code == 1
    def test_last_change_code_default_on_update(self, session):
        """
        #TODO add comment
        """
        tac = TacFactory.create(session=session)
        initial_code = tac.last_change_code
        tac.code = generate_uuid()
        session.commit()
        assert tac.last_change_code != initial_code
    def test_date_inserted_on_build(self, session):
        """
        #TODO add comment
        """
        tac = TacFactory.build(session=session)
        assert tac.insert_utc_date_time is not None
        assert isinstance(tac.insert_utc_date_time, datetime)
    def test_date_inserted_on_initial_save(self, session):
        """
        #TODO add comment
        """
        tac = TacFactory.build(session=session)
        assert tac.insert_utc_date_time is not None
        assert isinstance(tac.insert_utc_date_time, datetime)
        initial_time = datetime.utcnow() + timedelta(days=-1)
        tac.code = generate_uuid()
        session.commit()
        assert tac.insert_utc_date_time > initial_time
    def test_date_inserted_on_second_save(self, session):
        """
        #TODO add comment
        """
        tac = TacFactory(session=session)
        assert tac.insert_utc_date_time is not None
        assert isinstance(tac.insert_utc_date_time, datetime)
        initial_time = tac.insert_utc_date_time
        tac.code = generate_uuid()
        time.sleep(1)
        session.commit()
        assert tac.insert_utc_date_time == initial_time
    def test_date_updated_on_build(self, session):
        """
        #TODO add comment
        """
        tac = TacFactory.build(session=session)
        assert tac.last_update_utc_date_time is not None
        assert isinstance(tac.last_update_utc_date_time, datetime)
    def test_date_updated_on_initial_save(self, session):
        """
        #TODO add comment
        """
        tac = TacFactory.build(session=session)
        assert tac.last_update_utc_date_time is not None
        assert isinstance(tac.last_update_utc_date_time, datetime)
        initial_time = datetime.utcnow() + timedelta(days=-1)
        tac.code = generate_uuid()
        session.commit()
        assert tac.last_update_utc_date_time > initial_time
    def test_date_updated_on_second_save(self, session):
        """
        #TODO add comment
        """
        tac = TacFactory(session=session)
        assert tac.last_update_utc_date_time is not None
        assert isinstance(tac.last_update_utc_date_time, datetime)
        initial_time = tac.last_update_utc_date_time
        tac.code = generate_uuid()
        time.sleep(1)
        session.commit()
        assert tac.last_update_utc_date_time > initial_time
    def test_model_deletion(self, session):
        """
        #TODO add comment
        """
        tac = TacFactory.create(session=session)
        session.delete(tac)
        session.commit()
        deleted_tac = session.query(Tac).filter_by(
            tac_id=tac.tac_id).first()
        assert deleted_tac is None
    def test_data_types(self, session):
        """
        #TODO add comment
        """
        tac = TacFactory.create(session=session)
        assert isinstance(tac.tac_id, int)
        if DB_DIALECT == 'postgresql':
            assert isinstance(tac.code, UUID)
        elif DB_DIALECT == 'mssql':
            assert isinstance(tac.code, UNIQUEIDENTIFIER)
        else:  # This will cover SQLite, MySQL, and other databases
            assert isinstance(tac.code, str)
        assert isinstance(tac.last_change_code, int)
        if DB_DIALECT == 'postgresql':
            assert isinstance(tac.insert_user_id, UUID)
        elif DB_DIALECT == 'mssql':
            assert isinstance(tac.insert_user_id, UNIQUEIDENTIFIER)
        else:  # This will cover SQLite, MySQL, and other databases
            assert isinstance(tac.insert_user_id, str)
        if DB_DIALECT == 'postgresql':
            assert isinstance(tac.last_update_user_id, UUID)
        elif DB_DIALECT == 'mssql':
            assert isinstance(tac.last_update_user_id, UNIQUEIDENTIFIER)
        else:  # This will cover SQLite, MySQL, and other databases
            assert isinstance(tac.last_update_user_id, str)
        assert tac.description == "" or isinstance(tac.description, str)
        assert isinstance(tac.display_order, int)
        assert isinstance(tac.is_active, bool)
        assert tac.lookup_enum_name == "" or isinstance(tac.lookup_enum_name, str)
        assert tac.name == "" or isinstance(tac.name, str)
        assert isinstance(tac.pac_id, int)
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
                tac.pac_code_peek, UUID)
        elif DB_DIALECT == 'mssql':
            assert isinstance(
                tac.pac_code_peek, UNIQUEIDENTIFIER)
        else:  # This will cover SQLite, MySQL, and other databases
            assert isinstance(
                tac.pac_code_peek, str)
# endset
        assert isinstance(tac.insert_utc_date_time, datetime)
        assert isinstance(tac.last_update_utc_date_time, datetime)
    def test_unique_code_constraint(self, session):
        """
        #TODO add comment
        """
        tac_1 = TacFactory.create(session=session)
        tac_2 = TacFactory.create(session=session)
        tac_2.code = tac_1.code
        session.add_all([tac_1, tac_2])
        with pytest.raises(Exception):
            session.commit()
        session.rollback()
    def test_fields_default(self, session):
        """
        #TODO add comment
        """
        tac = Tac()
        assert tac.code is not None
        assert tac.last_change_code is not None
        assert tac.insert_user_id is None
        assert tac.last_update_user_id is None
        assert tac.insert_utc_date_time is not None
        assert tac.last_update_utc_date_time is not None
# endset
        # description,
        # displayOrder,
        # isActive,
        # lookupEnumName,
        # name,
        # PacID
        if DB_DIALECT == 'postgresql':
            assert isinstance(
                tac.pac_code_peek, UUID)
        elif DB_DIALECT == 'mssql':
            assert isinstance(
                tac.pac_code_peek,
                UNIQUEIDENTIFIER)
        else:  # This will cover SQLite, MySQL, and other databases
            assert isinstance(
                tac.pac_code_peek, str)
# endset
        assert tac.description == ""
        assert tac.display_order == 0
        assert tac.is_active is False
        assert tac.lookup_enum_name == ""
        assert tac.name == ""
        assert tac.pac_id == 0
# endset
    def test_last_change_code_concurrency(self, session):
        """
        #TODO add comment
        """
        tac = TacFactory.create(session=session)
        original_last_change_code = tac.last_change_code
        tac_1 = session.query(Tac).filter_by(
            tac_id=tac.tac_id).first()
        tac_1.code = generate_uuid()
        session.commit()
        tac_2 = session.query(Tac).filter_by(
            tac_id=tac.tac_id).first()
        tac_2.code = generate_uuid()
        session.commit()
        assert tac_2.last_change_code != original_last_change_code
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
        tac = TacFactory.create(session=session)
        tac.pac_id = 99999
        with pytest.raises(IntegrityError):
            session.commit()
        session.rollback()
# endset
