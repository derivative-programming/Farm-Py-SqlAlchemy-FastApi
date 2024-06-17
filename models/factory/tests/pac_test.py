# models/factory/tests/pac_test.py
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
from models import Base, Pac
from models.factory import PacFactory
from services.logging_config import get_logger
logger = get_logger(__name__)
DATABASE_URL = "sqlite:///:memory:"
class TestPacFactory:
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
        SessionLocal = sessionmaker(  # pylint: disable=invalid-name
            bind=engine, expire_on_commit=False)
        session_instance = SessionLocal()
        yield session_instance
        session_instance.close()
    def test_pac_creation(self, session):
        """
        #TODO add comment
        """
        pac = PacFactory.create(session=session)
        assert pac.pac_id is not None
    def test_code_default(self, session):
        """
        #TODO add comment
        """
        logging.info("vrtest")
        pac = PacFactory.create(session=session)
        assert isinstance(pac.code, uuid.UUID)
    def test_last_change_code_default_on_build(self, session):
        """
        #TODO add comment
        """
        pac: Pac = PacFactory.build(session=session)
        assert pac.last_change_code == 0
    def test_last_change_code_default_on_creation(self, session):
        """
        #TODO add comment
        """
        pac: Pac = PacFactory.create(session=session)
        assert pac.last_change_code == 1
    def test_last_change_code_default_on_update(self, session):
        """
        #TODO add comment
        """
        pac = PacFactory.create(session=session)
        initial_code = pac.last_change_code
        pac.code = uuid.uuid4()
        session.commit()
        assert pac.last_change_code != initial_code
    def test_date_inserted_on_build(self, session):
        """
        #TODO add comment
        """
        pac = PacFactory.build(session=session)
        assert pac.insert_utc_date_time is not None
        assert isinstance(pac.insert_utc_date_time, datetime)
    def test_date_inserted_on_initial_save(self, session):
        """
        #TODO add comment
        """
        pac = PacFactory.build(session=session)
        assert pac.insert_utc_date_time is not None
        assert isinstance(pac.insert_utc_date_time, datetime)
        initial_time = datetime.utcnow() + timedelta(days=-1)
        pac.code = uuid.uuid4()
        session.add(pac)
        session.commit()
        assert pac.insert_utc_date_time > initial_time
    def test_date_inserted_on_second_save(self, session):
        """
        #TODO add comment
        """
        pac = PacFactory(session=session)
        assert pac.insert_utc_date_time is not None
        assert isinstance(pac.insert_utc_date_time, datetime)
        initial_time = pac.insert_utc_date_time
        pac.code = uuid.uuid4()
        time.sleep(1)
        session.commit()
        assert pac.insert_utc_date_time == initial_time
    def test_date_updated_on_build(self, session):
        """
        #TODO add comment
        """
        pac = PacFactory.build(session=session)
        assert pac.last_update_utc_date_time is not None
        assert isinstance(pac.last_update_utc_date_time, datetime)
    def test_date_updated_on_initial_save(self, session):
        """
        #TODO add comment
        """
        pac = PacFactory.build(session=session)
        assert pac.last_update_utc_date_time is not None
        assert isinstance(pac.last_update_utc_date_time, datetime)
        initial_time = datetime.utcnow() + timedelta(days=-1)
        pac.code = uuid.uuid4()
        session.add(pac)
        session.commit()
        assert pac.last_update_utc_date_time > initial_time
    def test_date_updated_on_second_save(self, session):
        """
        #TODO add comment
        """
        pac = PacFactory(session=session)
        assert pac.last_update_utc_date_time is not None
        assert isinstance(pac.last_update_utc_date_time, datetime)
        initial_time = pac.last_update_utc_date_time
        pac.code = uuid.uuid4()
        time.sleep(1)
        session.commit()
        assert pac.last_update_utc_date_time > initial_time
    def test_model_deletion(self, session):
        """
        #TODO add comment
        """
        pac = PacFactory.create(session=session)
        session.delete(pac)
        session.commit()
        deleted_pac = session.query(Pac).filter_by(
            pac_id=pac.pac_id).first()
        assert deleted_pac is None
    def test_data_types(self, session):
        """
        #TODO add comment
        """
        pac = PacFactory.create(session=session)
        assert isinstance(pac.pac_id, int)
        assert isinstance(pac.code, uuid.UUID)
        assert isinstance(pac.last_change_code, int)
        assert isinstance(pac.insert_user_id, uuid.UUID)
        assert isinstance(pac.last_update_user_id, uuid.UUID)
        assert pac.description == "" or isinstance(pac.description, str)
        assert isinstance(pac.display_order, int)
        assert isinstance(pac.is_active, bool)
        assert pac.lookup_enum_name == "" or isinstance(pac.lookup_enum_name, str)
        assert pac.name == "" or isinstance(pac.name, str)
        # Check for the peek values,
        # assuming they are UUIDs based on your model
# endset
        # description,
        # displayOrder,
        # isActive,
        # lookupEnumName,
        # name,
# endset
        assert isinstance(pac.insert_utc_date_time, datetime)
        assert isinstance(pac.last_update_utc_date_time, datetime)
    def test_unique_code_constraint(self, session):
        """
        #TODO add comment
        """
        pac_1 = PacFactory.create(session=session)
        pac_2 = PacFactory.create(session=session)
        pac_2.code = pac_1.code
        session.add_all([pac_1, pac_2])
        with pytest.raises(Exception):
            session.commit()
        session.rollback()
    def test_fields_default(self):
        """
        #TODO add comment
        """
        pac = Pac()
        assert pac.code is not None
        assert pac.last_change_code is not None
        assert pac.insert_user_id == uuid.UUID(int=0)
        assert pac.last_update_user_id == uuid.UUID(int=0)
        assert pac.insert_utc_date_time is not None
        assert pac.last_update_utc_date_time is not None
# endset
        # description,
        # displayOrder,
        # isActive,
        # lookupEnumName,
        # name,
# endset
        assert pac is not None
        assert pac.description == ""
        assert pac.display_order == 0
        assert pac.is_active is False
        assert pac.lookup_enum_name == ""
        assert pac.name == ""
# endset
    def test_last_change_code_concurrency(self, session):
        """
        #TODO add comment
        """
        pac = PacFactory.create(session=session)
        original_last_change_code = pac.last_change_code
        pac_1 = session.query(Pac).filter_by(
            _pac_id=pac.pac_id).first()
        pac_1.code = uuid.uuid4()
        session.commit()
        pac_2 = session.query(Pac).filter_by(
            _pac_id=pac.pac_id).first()
        pac_2.code = uuid.uuid4()
        session.commit()
        assert pac_2.last_change_code != original_last_change_code
# endset
    # description,
    # displayOrder,
    # isActive,
    # lookupEnumName,
    # name,
# endset
