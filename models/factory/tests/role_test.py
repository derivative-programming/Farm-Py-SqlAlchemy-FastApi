# models/factory/tests/role_test.py
"""
    #TODO add comment
"""
from decimal import Decimal
import time
import math
import uuid
import logging
from datetime import datetime, date, timedelta
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from models import Base, Role
from models.factory import RoleFactory
from services.logging_config import get_logger
logger = get_logger(__name__)
DATABASE_URL = "sqlite:///:memory:"
class TestRoleFactory:
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
    def test_role_creation(self, session):
        """
        #TODO add comment
        """
        role = RoleFactory.create(session=session)
        assert role.role_id is not None
    def test_code_default(self, session):
        """
        #TODO add comment
        """
        logging.info("vrtest")
        role = RoleFactory.create(session=session)
        assert isinstance(role.code, uuid.UUID)
    def test_last_change_code_default_on_build(self, session):
        """
        #TODO add comment
        """
        role: Role = RoleFactory.build(session=session)
        assert role.last_change_code == 0
    def test_last_change_code_default_on_creation(self, session):
        """
        #TODO add comment
        """
        role: Role = RoleFactory.create(session=session)
        assert role.last_change_code == 1
    def test_last_change_code_default_on_update(self, session):
        """
        #TODO add comment
        """
        role = RoleFactory.create(session=session)
        initial_code = role.last_change_code
        role.code = uuid.uuid4()
        session.commit()
        assert role.last_change_code != initial_code
    def test_date_inserted_on_build(self, session):
        """
        #TODO add comment
        """
        role = RoleFactory.build(session=session)
        assert role.insert_utc_date_time is not None
        assert isinstance(role.insert_utc_date_time, datetime)
    def test_date_inserted_on_initial_save(self, session):
        """
        #TODO add comment
        """
        role = RoleFactory.build(session=session)
        assert role.insert_utc_date_time is not None
        assert isinstance(role.insert_utc_date_time, datetime)
        initial_time = datetime.utcnow() + timedelta(days=-1)
        role.code = uuid.uuid4()
        session.commit()
        assert role.insert_utc_date_time > initial_time
    def test_date_inserted_on_second_save(self, session):
        """
        #TODO add comment
        """
        role = RoleFactory(session=session)
        assert role.insert_utc_date_time is not None
        assert isinstance(role.insert_utc_date_time, datetime)
        initial_time = role.insert_utc_date_time
        role.code = uuid.uuid4()
        time.sleep(1)
        session.commit()
        assert role.insert_utc_date_time == initial_time
    def test_date_updated_on_build(self, session):
        """
        #TODO add comment
        """
        role = RoleFactory.build(session=session)
        assert role.last_update_utc_date_time is not None
        assert isinstance(role.last_update_utc_date_time, datetime)
    def test_date_updated_on_initial_save(self, session):
        """
        #TODO add comment
        """
        role = RoleFactory.build(session=session)
        assert role.last_update_utc_date_time is not None
        assert isinstance(role.last_update_utc_date_time, datetime)
        initial_time = datetime.utcnow() + timedelta(days=-1)
        role.code = uuid.uuid4()
        session.commit()
        assert role.last_update_utc_date_time > initial_time
    def test_date_updated_on_second_save(self, session):
        """
        #TODO add comment
        """
        role = RoleFactory(session=session)
        assert role.last_update_utc_date_time is not None
        assert isinstance(role.last_update_utc_date_time, datetime)
        initial_time = role.last_update_utc_date_time
        role.code = uuid.uuid4()
        time.sleep(1)
        session.commit()
        assert role.last_update_utc_date_time > initial_time
    def test_model_deletion(self, session):
        """
        #TODO add comment
        """
        role = RoleFactory.create(session=session)
        session.delete(role)
        session.commit()
        deleted_role = session.query(Role).filter_by(
            role_id=role.role_id).first()
        assert deleted_role is None
    def test_data_types(self, session):
        """
        #TODO add comment
        """
        role = RoleFactory.create(session=session)
        assert isinstance(role.role_id, int)
        assert isinstance(role.code, uuid.UUID)
        assert isinstance(role.last_change_code, int)
        assert isinstance(role.insert_user_id, uuid.UUID)
        assert isinstance(role.last_update_user_id, uuid.UUID)
        assert role.description == "" or isinstance(role.description, str)
        assert isinstance(role.display_order, int)
        assert isinstance(role.is_active, bool)
        assert role.lookup_enum_name == "" or isinstance(role.lookup_enum_name, str)
        assert role.name == "" or isinstance(role.name, str)
        assert isinstance(role.pac_id, int)
        # Check for the peek values,
        # assuming they are UUIDs based on your model
# endset
        # description,
        # displayOrder,
        # isActive,
        # lookupEnumName,
        # name,
        # pacID
        assert isinstance(
            role.pac_code_peek, uuid.UUID)
# endset
        assert isinstance(role.insert_utc_date_time, datetime)
        assert isinstance(role.last_update_utc_date_time, datetime)
    def test_unique_code_constraint(self, session):
        """
        #TODO add comment
        """
        role_1 = RoleFactory.create(session=session)
        role_2 = RoleFactory.create(session=session)
        role_2.code = role_1.code
        session.add_all([role_1, role_2])
        with pytest.raises(Exception):
            session.commit()
        session.rollback()
    def test_fields_default(self, session):
        """
        #TODO add comment
        """
        role = Role()
        assert role.code is not None
        assert role.last_change_code is not None
        assert role.insert_user_id == uuid.UUID(int=0)
        assert role.last_update_user_id == uuid.UUID(int=0)
        assert role.insert_utc_date_time is not None
        assert role.last_update_utc_date_time is not None
# endset
        # description,
        # displayOrder,
        # isActive,
        # lookupEnumName,
        # name,
        # PacID
        assert isinstance(
            role.pac_code_peek, uuid.UUID)
# endset
        assert role.description == ""
        assert role.display_order == 0
        assert role.is_active is False
        assert role.lookup_enum_name == ""
        assert role.name == ""
        assert role.pac_id == 0
# endset
    def test_last_change_code_concurrency(self, session):
        """
        #TODO add comment
        """
        role = RoleFactory.create(session=session)
        original_last_change_code = role.last_change_code
        role_1 = session.query(Role).filter_by(
            role_id=role.role_id).first()
        role_1.code = uuid.uuid4()
        session.commit()
        role_2 = session.query(Role).filter_by(
            role_id=role.role_id).first()
        role_2.code = uuid.uuid4()
        session.commit()
        assert role_2.last_change_code != original_last_change_code
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
        role = RoleFactory.create(session=session)
        role.pac_id = 99999
        with pytest.raises(IntegrityError):
            session.commit()
        session.rollback()
# endset
