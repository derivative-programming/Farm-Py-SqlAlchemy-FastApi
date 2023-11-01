from decimal import Decimal
import pytest
import uuid
import time
from decimal import Decimal
from datetime import datetime, date
from sqlalchemy import Numeric, create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Role
from models.factory import RoleFactory
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
class TestRoleFactory:
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
    def test_role_creation(self, session):
        role = RoleFactory.create(session=session)
        assert role.role_id is not None
    def test_code_default(self, session):
        role = RoleFactory.create(session=session)
        if db_dialect == 'postgresql':
            assert isinstance(role.code, UUID)
        elif db_dialect == 'mssql':
            assert isinstance(role.code, UNIQUEIDENTIFIER)
        else:  # This will cover SQLite, MySQL, and other databases
            assert isinstance(role.code, str)
    def test_last_change_code_default_on_build(self, session):
        role:Role = RoleFactory.build(session=session)
        assert role.last_change_code == 0
    def test_last_change_code_default_on_creation(self, session):
        role:Role = RoleFactory.create(session=session)
        assert role.last_change_code == 1
    def test_last_change_code_default_on_update(self, session):
        role = RoleFactory.create(session=session)
        initial_code = role.last_change_code
        role.code = generate_uuid()
        session.commit()
        assert role.last_change_code != initial_code
    def test_date_inserted_on_build(self, session):
        role = RoleFactory.build(session=session)
        assert role.insert_utc_date_time is not None
        assert isinstance(role.insert_utc_date_time, datetime)
    def test_date_inserted_on_initial_save(self, session):
        role = RoleFactory.build(session=session)
        assert role.insert_utc_date_time is not None
        assert isinstance(role.insert_utc_date_time, datetime)
        initial_time = role.insert_utc_date_time
        role.code = generate_uuid()
        time.sleep(2)
        session.commit()
        assert role.insert_utc_date_time > initial_time
    def test_date_inserted_on_second_save(self, session):
        role = RoleFactory(session=session)
        assert role.insert_utc_date_time is not None
        assert isinstance(role.insert_utc_date_time, datetime)
        initial_time = role.insert_utc_date_time
        role.code = generate_uuid()
        time.sleep(2)
        session.commit()
        assert role.insert_utc_date_time == initial_time
    def test_date_updated_on_build(self, session):
        role = RoleFactory.build(session=session)
        assert role.last_update_utc_date_time is not None
        assert isinstance(role.last_update_utc_date_time, datetime)
    def test_date_updated_on_initial_save(self, session):
        role = RoleFactory.build(session=session)
        assert role.last_update_utc_date_time is not None
        assert isinstance(role.last_update_utc_date_time, datetime)
        initial_time = role.last_update_utc_date_time
        role.code = generate_uuid()
        time.sleep(2)
        session.commit()
        assert role.last_update_utc_date_time > initial_time
    def test_date_updated_on_second_save(self, session):
        role = RoleFactory(session=session)
        assert role.last_update_utc_date_time is not None
        assert isinstance(role.last_update_utc_date_time, datetime)
        initial_time = role.last_update_utc_date_time
        role.code = generate_uuid()
        time.sleep(2)
        session.commit()
        assert role.last_update_utc_date_time > initial_time
    def test_model_deletion(self, session):
        role = RoleFactory.create(session=session)
        session.delete(role)
        session.commit()
        deleted_role = session.query(Role).filter_by(role_id=role.role_id).first()
        assert deleted_role is None
    def test_data_types(self, session):
        role = RoleFactory.create(session=session)
        assert isinstance(role.role_id, int)
        if db_dialect == 'postgresql':
            assert isinstance(role.code, UUID)
        elif db_dialect == 'mssql':
            assert isinstance(role.code, UNIQUEIDENTIFIER)
        else:  # This will cover SQLite, MySQL, and other databases
            assert isinstance(role.code, str)
        assert isinstance(role.last_change_code, int)
        if db_dialect == 'postgresql':
            assert isinstance(role.insert_user_id, UUID)
        elif db_dialect == 'mssql':
            assert isinstance(role.insert_user_id, UNIQUEIDENTIFIER)
        else:  # This will cover SQLite, MySQL, and other databases
            assert isinstance(role.insert_user_id, str)
        if db_dialect == 'postgresql':
            assert isinstance(role.last_update_user_id, UUID)
        elif db_dialect == 'mssql':
            assert isinstance(role.last_update_user_id, UNIQUEIDENTIFIER)
        else:  # This will cover SQLite, MySQL, and other databases
            assert isinstance(role.last_update_user_id, str)
        assert role.description == "" or isinstance(role.description, str)
        assert isinstance(role.display_order, int)
        assert isinstance(role.is_active, bool)
        assert role.lookup_enum_name == "" or isinstance(role.lookup_enum_name, str)
        assert role.name == "" or isinstance(role.name, str)
        assert isinstance(role.pac_id, int)
        # Check for the peek values, assuming they are UUIDs based on your model

        #description,
        #displayOrder,
        #isActive,
        #lookupEnumName,
        #name,
        #pacID
        if db_dialect == 'postgresql':
            assert isinstance(role.pac_code_peek, UUID)
        elif db_dialect == 'mssql':
            assert isinstance(role.pac_code_peek, UNIQUEIDENTIFIER)
        else:  # This will cover SQLite, MySQL, and other databases
            assert isinstance(role.pac_code_peek, str)

        assert isinstance(role.insert_utc_date_time, datetime)
        assert isinstance(role.last_update_utc_date_time, datetime)
    def test_unique_code_constraint(self, session):
        role_1 = RoleFactory.create(session=session)
        role_2 = RoleFactory.create(session=session)
        role_2.code = role_1.code
        session.add_all([role_1, role_2])
        with pytest.raises(Exception):  # adjust for the specific DB exception you'd expect
            session.commit()
        session.rollback()
    def test_fields_default(self, session):
        role = Role()
        assert role.code is not None
        assert role.last_change_code is not None
        assert role.insert_user_id is None
        assert role.last_update_user_id is None
        assert role.insert_utc_date_time is not None
        assert role.last_update_utc_date_time is not None

        #description,
        #displayOrder,
        #isActive,
        #lookupEnumName,
        #name,
        #PacID
        if db_dialect == 'postgresql':
            assert isinstance(role.pac_code_peek, UUID)
        elif db_dialect == 'mssql':
            assert isinstance(role.pac_code_peek, UNIQUEIDENTIFIER)
        else:  # This will cover SQLite, MySQL, and other databases
            assert isinstance(role.pac_code_peek, str)

        assert role.description == ""
        assert role.display_order == 0
        assert role.is_active == False
        assert role.lookup_enum_name == ""
        assert role.name == ""
        assert role.pac_id == 0

    def test_last_change_code_concurrency(self, session):
        role = RoleFactory.create(session=session)
        original_last_change_code = role.last_change_code
        role_1 = session.query(Role).filter_by(role_id=role.role_id).first()
        role_1.code = generate_uuid()
        session.commit()
        role_2 = session.query(Role).filter_by(role_id=role.role_id).first()
        role_2.code = generate_uuid()
        session.commit()
        assert role_2.last_change_code != original_last_change_code

    #description,
    #displayOrder,
    #isActive,
    #lookupEnumName,
    #name,
    #PacID
    def test_invalid_pac_id(self, session):
        role = RoleFactory.create(session=session)
        role.pac_id = 99999
        with pytest.raises(IntegrityError):  # adjust for the specific DB exception you'd expect
            session.commit()
        session.rollback()

