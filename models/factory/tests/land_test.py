# models/factory/tests/land_test.py
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
from models import Base, Land
from models.factory import LandFactory
from services.logging_config import get_logger
logger = get_logger(__name__)
DATABASE_URL = "sqlite:///:memory:"
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
        logging.info("vrtest")
        land = LandFactory.create(session=session)
        assert isinstance(land.code, uuid.UUID)
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
        land.code = uuid.uuid4()
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
        land.code = uuid.uuid4()
        session.add(land)
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
        land.code = uuid.uuid4()
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
        land.code = uuid.uuid4()
        session.add(land)
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
        land.code = uuid.uuid4()
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
        assert isinstance(land.code, uuid.UUID)
        assert isinstance(land.last_change_code, int)
        assert isinstance(land.insert_user_id, uuid.UUID)
        assert isinstance(land.last_update_user_id, uuid.UUID)
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
        assert isinstance(
            land.pac_code_peek, uuid.UUID)
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
    def test_fields_default(self):
        """
        #TODO add comment
        """
        land = Land()
        assert land.code is not None
        assert land.last_change_code is not None
        assert land.insert_user_id == uuid.UUID(int=0)
        assert land.last_update_user_id == uuid.UUID(int=0)
        assert land.insert_utc_date_time is not None
        assert land.last_update_utc_date_time is not None
# endset
        # description,
        # displayOrder,
        # isActive,
        # lookupEnumName,
        # name,
        # PacID
        assert isinstance(
            land.pac_code_peek, uuid.UUID)
# endset
        assert land is not None
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
            _land_id=land.land_id).first()
        land_1.code = uuid.uuid4()
        session.commit()
        land_2 = session.query(Land).filter_by(
            _land_id=land.land_id).first()
        land_2.code = uuid.uuid4()
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
