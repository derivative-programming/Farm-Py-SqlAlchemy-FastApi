# models/factory/tests/date_greater_than_filter_test.py
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
from models import Base, DateGreaterThanFilter
from models.factory import DateGreaterThanFilterFactory
from services.logging_config import get_logger
logger = get_logger(__name__)
DATABASE_URL = "sqlite:///:memory:"
class TestDateGreaterThanFilterFactory:
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
    def test_date_greater_than_filter_creation(self, session):
        """
        #TODO add comment
        """
        date_greater_than_filter = DateGreaterThanFilterFactory.create(session=session)
        assert date_greater_than_filter.date_greater_than_filter_id is not None
    def test_code_default(self, session):
        """
        #TODO add comment
        """
        logging.info("vrtest")
        date_greater_than_filter = DateGreaterThanFilterFactory.create(session=session)
        assert isinstance(date_greater_than_filter.code, uuid.UUID)
    def test_last_change_code_default_on_build(self, session):
        """
        #TODO add comment
        """
        date_greater_than_filter: DateGreaterThanFilter = DateGreaterThanFilterFactory.build(session=session)
        assert date_greater_than_filter.last_change_code == 0
    def test_last_change_code_default_on_creation(self, session):
        """
        #TODO add comment
        """
        date_greater_than_filter: DateGreaterThanFilter = DateGreaterThanFilterFactory.create(session=session)
        assert date_greater_than_filter.last_change_code == 1
    def test_last_change_code_default_on_update(self, session):
        """
        #TODO add comment
        """
        date_greater_than_filter = DateGreaterThanFilterFactory.create(session=session)
        initial_code = date_greater_than_filter.last_change_code
        date_greater_than_filter.code = uuid.uuid4()
        session.commit()
        assert date_greater_than_filter.last_change_code != initial_code
    def test_date_inserted_on_build(self, session):
        """
        #TODO add comment
        """
        date_greater_than_filter = DateGreaterThanFilterFactory.build(session=session)
        assert date_greater_than_filter.insert_utc_date_time is not None
        assert isinstance(date_greater_than_filter.insert_utc_date_time, datetime)
    def test_date_inserted_on_initial_save(self, session):
        """
        #TODO add comment
        """
        date_greater_than_filter = DateGreaterThanFilterFactory.build(session=session)
        assert date_greater_than_filter.insert_utc_date_time is not None
        assert isinstance(date_greater_than_filter.insert_utc_date_time, datetime)
        initial_time = datetime.utcnow() + timedelta(days=-1)
        date_greater_than_filter.code = uuid.uuid4()
        session.commit()
        assert date_greater_than_filter.insert_utc_date_time > initial_time
    def test_date_inserted_on_second_save(self, session):
        """
        #TODO add comment
        """
        date_greater_than_filter = DateGreaterThanFilterFactory(session=session)
        assert date_greater_than_filter.insert_utc_date_time is not None
        assert isinstance(date_greater_than_filter.insert_utc_date_time, datetime)
        initial_time = date_greater_than_filter.insert_utc_date_time
        date_greater_than_filter.code = uuid.uuid4()
        time.sleep(1)
        session.commit()
        assert date_greater_than_filter.insert_utc_date_time == initial_time
    def test_date_updated_on_build(self, session):
        """
        #TODO add comment
        """
        date_greater_than_filter = DateGreaterThanFilterFactory.build(session=session)
        assert date_greater_than_filter.last_update_utc_date_time is not None
        assert isinstance(date_greater_than_filter.last_update_utc_date_time, datetime)
    def test_date_updated_on_initial_save(self, session):
        """
        #TODO add comment
        """
        date_greater_than_filter = DateGreaterThanFilterFactory.build(session=session)
        assert date_greater_than_filter.last_update_utc_date_time is not None
        assert isinstance(date_greater_than_filter.last_update_utc_date_time, datetime)
        initial_time = datetime.utcnow() + timedelta(days=-1)
        date_greater_than_filter.code = uuid.uuid4()
        session.commit()
        assert date_greater_than_filter.last_update_utc_date_time > initial_time
    def test_date_updated_on_second_save(self, session):
        """
        #TODO add comment
        """
        date_greater_than_filter = DateGreaterThanFilterFactory(session=session)
        assert date_greater_than_filter.last_update_utc_date_time is not None
        assert isinstance(date_greater_than_filter.last_update_utc_date_time, datetime)
        initial_time = date_greater_than_filter.last_update_utc_date_time
        date_greater_than_filter.code = uuid.uuid4()
        time.sleep(1)
        session.commit()
        assert date_greater_than_filter.last_update_utc_date_time > initial_time
    def test_model_deletion(self, session):
        """
        #TODO add comment
        """
        date_greater_than_filter = DateGreaterThanFilterFactory.create(session=session)
        session.delete(date_greater_than_filter)
        session.commit()
        deleted_date_greater_than_filter = session.query(DateGreaterThanFilter).filter_by(
            date_greater_than_filter_id=date_greater_than_filter.date_greater_than_filter_id).first()
        assert deleted_date_greater_than_filter is None
    def test_data_types(self, session):
        """
        #TODO add comment
        """
        date_greater_than_filter = DateGreaterThanFilterFactory.create(session=session)
        assert isinstance(date_greater_than_filter.date_greater_than_filter_id, int)
        assert isinstance(date_greater_than_filter.code, uuid.UUID)
        assert isinstance(date_greater_than_filter.last_change_code, int)
        assert isinstance(date_greater_than_filter.insert_user_id, uuid.UUID)
        assert isinstance(date_greater_than_filter.last_update_user_id, uuid.UUID)
        assert isinstance(date_greater_than_filter.day_count, int)
        assert date_greater_than_filter.description == "" or isinstance(date_greater_than_filter.description, str)
        assert isinstance(date_greater_than_filter.display_order, int)
        assert isinstance(date_greater_than_filter.is_active, bool)
        assert date_greater_than_filter.lookup_enum_name == "" or isinstance(date_greater_than_filter.lookup_enum_name, str)
        assert date_greater_than_filter.name == "" or isinstance(date_greater_than_filter.name, str)
        assert isinstance(date_greater_than_filter.pac_id, int)
        # Check for the peek values,
        # assuming they are UUIDs based on your model
# endset
        # dayCount,
        # description,
        # displayOrder,
        # isActive,
        # lookupEnumName,
        # name,
        # pacID
        assert isinstance(
            date_greater_than_filter.pac_code_peek, uuid.UUID)
# endset
        assert isinstance(date_greater_than_filter.insert_utc_date_time, datetime)
        assert isinstance(date_greater_than_filter.last_update_utc_date_time, datetime)
    def test_unique_code_constraint(self, session):
        """
        #TODO add comment
        """
        date_greater_than_filter_1 = DateGreaterThanFilterFactory.create(session=session)
        date_greater_than_filter_2 = DateGreaterThanFilterFactory.create(session=session)
        date_greater_than_filter_2.code = date_greater_than_filter_1.code
        session.add_all([date_greater_than_filter_1, date_greater_than_filter_2])
        with pytest.raises(Exception):
            session.commit()
        session.rollback()
    def test_fields_default(self, session):
        """
        #TODO add comment
        """
        date_greater_than_filter = DateGreaterThanFilter()
        assert date_greater_than_filter.code is not None
        assert date_greater_than_filter.last_change_code is not None
        assert date_greater_than_filter.insert_user_id == uuid.UUID(int=0)
        assert date_greater_than_filter.last_update_user_id == uuid.UUID(int=0)
        assert date_greater_than_filter.insert_utc_date_time is not None
        assert date_greater_than_filter.last_update_utc_date_time is not None
# endset
        # dayCount,
        # description,
        # displayOrder,
        # isActive,
        # lookupEnumName,
        # name,
        # PacID
        assert isinstance(
            date_greater_than_filter.pac_code_peek, uuid.UUID)
# endset
        assert date_greater_than_filter is not None
        assert date_greater_than_filter.day_count == 0
        assert date_greater_than_filter.description == ""
        assert date_greater_than_filter.display_order == 0
        assert date_greater_than_filter.is_active is False
        assert date_greater_than_filter.lookup_enum_name == ""
        assert date_greater_than_filter.name == ""
        assert date_greater_than_filter.pac_id == 0
# endset
    def test_last_change_code_concurrency(self, session):
        """
        #TODO add comment
        """
        date_greater_than_filter = DateGreaterThanFilterFactory.create(session=session)
        original_last_change_code = date_greater_than_filter.last_change_code
        date_greater_than_filter_1 = session.query(DateGreaterThanFilter).filter_by(
            date_greater_than_filter_id=date_greater_than_filter.date_greater_than_filter_id).first()
        date_greater_than_filter_1.code = uuid.uuid4()
        session.commit()
        date_greater_than_filter_2 = session.query(DateGreaterThanFilter).filter_by(
            date_greater_than_filter_id=date_greater_than_filter.date_greater_than_filter_id).first()
        date_greater_than_filter_2.code = uuid.uuid4()
        session.commit()
        assert date_greater_than_filter_2.last_change_code != original_last_change_code
# endset
    # dayCount,
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
        date_greater_than_filter = DateGreaterThanFilterFactory.create(session=session)
        date_greater_than_filter.pac_id = 99999
        with pytest.raises(IntegrityError):
            session.commit()
        session.rollback()
# endset
