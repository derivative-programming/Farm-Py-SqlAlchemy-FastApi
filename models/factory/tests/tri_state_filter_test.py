# models/factory/tests/tri_state_filter_test.py
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
from models import Base, TriStateFilter
from models.factory import TriStateFilterFactory
from services.logging_config import get_logger
logger = get_logger(__name__)
DATABASE_URL = "sqlite:///:memory:"
class TestTriStateFilterFactory:
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
    def test_tri_state_filter_creation(self, session):
        """
        #TODO add comment
        """
        tri_state_filter = TriStateFilterFactory.create(session=session)
        assert tri_state_filter.tri_state_filter_id is not None
    def test_code_default(self, session):
        """
        #TODO add comment
        """
        logging.info("vrtest")
        tri_state_filter = TriStateFilterFactory.create(session=session)
        assert isinstance(tri_state_filter.code, uuid.UUID)
    def test_last_change_code_default_on_build(self, session):
        """
        #TODO add comment
        """
        tri_state_filter: TriStateFilter = TriStateFilterFactory.build(session=session)
        assert tri_state_filter.last_change_code == 0
    def test_last_change_code_default_on_creation(self, session):
        """
        #TODO add comment
        """
        tri_state_filter: TriStateFilter = TriStateFilterFactory.create(session=session)
        assert tri_state_filter.last_change_code == 1
    def test_last_change_code_default_on_update(self, session):
        """
        #TODO add comment
        """
        tri_state_filter = TriStateFilterFactory.create(session=session)
        initial_code = tri_state_filter.last_change_code
        tri_state_filter.code = uuid.uuid4()
        session.commit()
        assert tri_state_filter.last_change_code != initial_code
    def test_date_inserted_on_build(self, session):
        """
        #TODO add comment
        """
        tri_state_filter = TriStateFilterFactory.build(session=session)
        assert tri_state_filter.insert_utc_date_time is not None
        assert isinstance(tri_state_filter.insert_utc_date_time, datetime)
    def test_date_inserted_on_initial_save(self, session):
        """
        #TODO add comment
        """
        tri_state_filter = TriStateFilterFactory.build(session=session)
        assert tri_state_filter.insert_utc_date_time is not None
        assert isinstance(tri_state_filter.insert_utc_date_time, datetime)
        initial_time = datetime.utcnow() + timedelta(days=-1)
        tri_state_filter.code = uuid.uuid4()
        session.commit()
        assert tri_state_filter.insert_utc_date_time > initial_time
    def test_date_inserted_on_second_save(self, session):
        """
        #TODO add comment
        """
        tri_state_filter = TriStateFilterFactory(session=session)
        assert tri_state_filter.insert_utc_date_time is not None
        assert isinstance(tri_state_filter.insert_utc_date_time, datetime)
        initial_time = tri_state_filter.insert_utc_date_time
        tri_state_filter.code = uuid.uuid4()
        time.sleep(1)
        session.commit()
        assert tri_state_filter.insert_utc_date_time == initial_time
    def test_date_updated_on_build(self, session):
        """
        #TODO add comment
        """
        tri_state_filter = TriStateFilterFactory.build(session=session)
        assert tri_state_filter.last_update_utc_date_time is not None
        assert isinstance(tri_state_filter.last_update_utc_date_time, datetime)
    def test_date_updated_on_initial_save(self, session):
        """
        #TODO add comment
        """
        tri_state_filter = TriStateFilterFactory.build(session=session)
        assert tri_state_filter.last_update_utc_date_time is not None
        assert isinstance(tri_state_filter.last_update_utc_date_time, datetime)
        initial_time = datetime.utcnow() + timedelta(days=-1)
        tri_state_filter.code = uuid.uuid4()
        session.commit()
        assert tri_state_filter.last_update_utc_date_time > initial_time
    def test_date_updated_on_second_save(self, session):
        """
        #TODO add comment
        """
        tri_state_filter = TriStateFilterFactory(session=session)
        assert tri_state_filter.last_update_utc_date_time is not None
        assert isinstance(tri_state_filter.last_update_utc_date_time, datetime)
        initial_time = tri_state_filter.last_update_utc_date_time
        tri_state_filter.code = uuid.uuid4()
        time.sleep(1)
        session.commit()
        assert tri_state_filter.last_update_utc_date_time > initial_time
    def test_model_deletion(self, session):
        """
        #TODO add comment
        """
        tri_state_filter = TriStateFilterFactory.create(session=session)
        session.delete(tri_state_filter)
        session.commit()
        deleted_tri_state_filter = session.query(TriStateFilter).filter_by(
            tri_state_filter_id=tri_state_filter.tri_state_filter_id).first()
        assert deleted_tri_state_filter is None
    def test_data_types(self, session):
        """
        #TODO add comment
        """
        tri_state_filter = TriStateFilterFactory.create(session=session)
        assert isinstance(tri_state_filter.tri_state_filter_id, int)
        assert isinstance(tri_state_filter.code, uuid.UUID)
        assert isinstance(tri_state_filter.last_change_code, int)
        assert isinstance(tri_state_filter.insert_user_id, uuid.UUID)
        assert isinstance(tri_state_filter.last_update_user_id, uuid.UUID)
        assert tri_state_filter.description == "" or isinstance(tri_state_filter.description, str)
        assert isinstance(tri_state_filter.display_order, int)
        assert isinstance(tri_state_filter.is_active, bool)
        assert tri_state_filter.lookup_enum_name == "" or isinstance(tri_state_filter.lookup_enum_name, str)
        assert tri_state_filter.name == "" or isinstance(tri_state_filter.name, str)
        assert isinstance(tri_state_filter.pac_id, int)
        assert isinstance(tri_state_filter.state_int_value, int)
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
            tri_state_filter.pac_code_peek, uuid.UUID)
        # stateIntValue,
# endset
        assert isinstance(tri_state_filter.insert_utc_date_time, datetime)
        assert isinstance(tri_state_filter.last_update_utc_date_time, datetime)
    def test_unique_code_constraint(self, session):
        """
        #TODO add comment
        """
        tri_state_filter_1 = TriStateFilterFactory.create(session=session)
        tri_state_filter_2 = TriStateFilterFactory.create(session=session)
        tri_state_filter_2.code = tri_state_filter_1.code
        session.add_all([tri_state_filter_1, tri_state_filter_2])
        with pytest.raises(Exception):
            session.commit()
        session.rollback()
    def test_fields_default(self, session):
        """
        #TODO add comment
        """
        tri_state_filter = TriStateFilter()
        assert tri_state_filter.code is not None
        assert tri_state_filter.last_change_code is not None
        assert tri_state_filter.insert_user_id == uuid.UUID(int=0)
        assert tri_state_filter.last_update_user_id == uuid.UUID(int=0)
        assert tri_state_filter.insert_utc_date_time is not None
        assert tri_state_filter.last_update_utc_date_time is not None
# endset
        # description,
        # displayOrder,
        # isActive,
        # lookupEnumName,
        # name,
        # PacID
        assert isinstance(
            tri_state_filter.pac_code_peek, uuid.UUID)
        # stateIntValue,
# endset
        assert tri_state_filter.description == ""
        assert tri_state_filter.display_order == 0
        assert tri_state_filter.is_active is False
        assert tri_state_filter.lookup_enum_name == ""
        assert tri_state_filter.name == ""
        assert tri_state_filter.pac_id == 0
        assert tri_state_filter.state_int_value == 0
# endset
    def test_last_change_code_concurrency(self, session):
        """
        #TODO add comment
        """
        tri_state_filter = TriStateFilterFactory.create(session=session)
        original_last_change_code = tri_state_filter.last_change_code
        tri_state_filter_1 = session.query(TriStateFilter).filter_by(
            tri_state_filter_id=tri_state_filter.tri_state_filter_id).first()
        tri_state_filter_1.code = uuid.uuid4()
        session.commit()
        tri_state_filter_2 = session.query(TriStateFilter).filter_by(
            tri_state_filter_id=tri_state_filter.tri_state_filter_id).first()
        tri_state_filter_2.code = uuid.uuid4()
        session.commit()
        assert tri_state_filter_2.last_change_code != original_last_change_code
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
        tri_state_filter = TriStateFilterFactory.create(session=session)
        tri_state_filter.pac_id = 99999
        with pytest.raises(IntegrityError):
            session.commit()
        session.rollback()
    # stateIntValue,
# endset
