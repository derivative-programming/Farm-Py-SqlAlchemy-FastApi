# models/factory/tests/flavor_test.py
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
from models import Base, Flavor
from models.factory import FlavorFactory
from services.logging_config import get_logger
logger = get_logger(__name__)
DATABASE_URL = "sqlite:///:memory:"
class TestFlavorFactory:
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
    def test_flavor_creation(self, session):
        """
        #TODO add comment
        """
        flavor = FlavorFactory.create(session=session)
        assert flavor.flavor_id is not None
    def test_code_default(self, session):
        """
        #TODO add comment
        """
        logging.info("vrtest")
        flavor = FlavorFactory.create(session=session)
        assert isinstance(flavor.code, uuid.UUID)
    def test_last_change_code_default_on_build(self, session):
        """
        #TODO add comment
        """
        flavor: Flavor = FlavorFactory.build(session=session)
        assert flavor.last_change_code == 0
    def test_last_change_code_default_on_creation(self, session):
        """
        #TODO add comment
        """
        flavor: Flavor = FlavorFactory.create(session=session)
        assert flavor.last_change_code == 1
    def test_last_change_code_default_on_update(self, session):
        """
        #TODO add comment
        """
        flavor = FlavorFactory.create(session=session)
        initial_code = flavor.last_change_code
        flavor.code = uuid.uuid4()
        session.commit()
        assert flavor.last_change_code != initial_code
    def test_date_inserted_on_build(self, session):
        """
        #TODO add comment
        """
        flavor = FlavorFactory.build(session=session)
        assert flavor.insert_utc_date_time is not None
        assert isinstance(flavor.insert_utc_date_time, datetime)
    def test_date_inserted_on_initial_save(self, session):
        """
        #TODO add comment
        """
        flavor = FlavorFactory.build(session=session)
        assert flavor.insert_utc_date_time is not None
        assert isinstance(flavor.insert_utc_date_time, datetime)
        initial_time = datetime.utcnow() + timedelta(days=-1)
        flavor.code = uuid.uuid4()
        session.add(flavor)
        session.commit()
        assert flavor.insert_utc_date_time > initial_time
    def test_date_inserted_on_second_save(self, session):
        """
        #TODO add comment
        """
        flavor = FlavorFactory(session=session)
        assert flavor.insert_utc_date_time is not None
        assert isinstance(flavor.insert_utc_date_time, datetime)
        initial_time = flavor.insert_utc_date_time
        flavor.code = uuid.uuid4()
        time.sleep(1)
        session.commit()
        assert flavor.insert_utc_date_time == initial_time
    def test_date_updated_on_build(self, session):
        """
        #TODO add comment
        """
        flavor = FlavorFactory.build(session=session)
        assert flavor.last_update_utc_date_time is not None
        assert isinstance(flavor.last_update_utc_date_time, datetime)
    def test_date_updated_on_initial_save(self, session):
        """
        #TODO add comment
        """
        flavor = FlavorFactory.build(session=session)
        assert flavor.last_update_utc_date_time is not None
        assert isinstance(flavor.last_update_utc_date_time, datetime)
        initial_time = datetime.utcnow() + timedelta(days=-1)
        flavor.code = uuid.uuid4()
        session.add(flavor)
        session.commit()
        assert flavor.last_update_utc_date_time > initial_time
    def test_date_updated_on_second_save(self, session):
        """
        #TODO add comment
        """
        flavor = FlavorFactory(session=session)
        assert flavor.last_update_utc_date_time is not None
        assert isinstance(flavor.last_update_utc_date_time, datetime)
        initial_time = flavor.last_update_utc_date_time
        flavor.code = uuid.uuid4()
        time.sleep(1)
        session.commit()
        assert flavor.last_update_utc_date_time > initial_time
    def test_model_deletion(self, session):
        """
        #TODO add comment
        """
        flavor = FlavorFactory.create(session=session)
        session.delete(flavor)
        session.commit()
        deleted_flavor = session.query(Flavor).filter_by(
            flavor_id=flavor.flavor_id).first()
        assert deleted_flavor is None
    def test_data_types(self, session):
        """
        #TODO add comment
        """
        flavor = FlavorFactory.create(session=session)
        assert isinstance(flavor.flavor_id, int)
        assert isinstance(flavor.code, uuid.UUID)
        assert isinstance(flavor.last_change_code, int)
        assert isinstance(flavor.insert_user_id, uuid.UUID)
        assert isinstance(flavor.last_update_user_id, uuid.UUID)
        assert flavor.description == "" or isinstance(flavor.description, str)
        assert isinstance(flavor.display_order, int)
        assert isinstance(flavor.is_active, bool)
        assert flavor.lookup_enum_name == "" or isinstance(flavor.lookup_enum_name, str)
        assert flavor.name == "" or isinstance(flavor.name, str)
        assert isinstance(flavor.pac_id, int)
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
            flavor.pac_code_peek, uuid.UUID)
# endset
        assert isinstance(flavor.insert_utc_date_time, datetime)
        assert isinstance(flavor.last_update_utc_date_time, datetime)
    def test_unique_code_constraint(self, session):
        """
        #TODO add comment
        """
        flavor_1 = FlavorFactory.create(session=session)
        flavor_2 = FlavorFactory.create(session=session)
        flavor_2.code = flavor_1.code
        session.add_all([flavor_1, flavor_2])
        with pytest.raises(Exception):
            session.commit()
        session.rollback()
    def test_fields_default(self):
        """
        #TODO add comment
        """
        flavor = Flavor()
        assert flavor.code is not None
        assert flavor.last_change_code is not None
        assert flavor.insert_user_id == uuid.UUID(int=0)
        assert flavor.last_update_user_id == uuid.UUID(int=0)
        assert flavor.insert_utc_date_time is not None
        assert flavor.last_update_utc_date_time is not None
# endset
        # description,
        # displayOrder,
        # isActive,
        # lookupEnumName,
        # name,
        # PacID
        assert isinstance(
            flavor.pac_code_peek, uuid.UUID)
# endset
        assert flavor is not None
        assert flavor.description == ""
        assert flavor.display_order == 0
        assert flavor.is_active is False
        assert flavor.lookup_enum_name == ""
        assert flavor.name == ""
        assert flavor.pac_id == 0
# endset
    def test_last_change_code_concurrency(self, session):
        """
        #TODO add comment
        """
        flavor = FlavorFactory.create(session=session)
        original_last_change_code = flavor.last_change_code
        flavor_1 = session.query(Flavor).filter_by(
            _flavor_id=flavor.flavor_id).first()
        flavor_1.code = uuid.uuid4()
        session.commit()
        flavor_2 = session.query(Flavor).filter_by(
            _flavor_id=flavor.flavor_id).first()
        flavor_2.code = uuid.uuid4()
        session.commit()
        assert flavor_2.last_change_code != original_last_change_code
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
        flavor = FlavorFactory.create(session=session)
        flavor.pac_id = 99999
        with pytest.raises(IntegrityError):
            session.commit()
        session.rollback()
# endset
