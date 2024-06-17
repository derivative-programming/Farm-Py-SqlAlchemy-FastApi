# models/factory/tests/customer_role_test.py
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
from models import Base, CustomerRole
from models.factory import CustomerRoleFactory
from services.logging_config import get_logger
logger = get_logger(__name__)
DATABASE_URL = "sqlite:///:memory:"
class TestCustomerRoleFactory:
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
    def test_customer_role_creation(self, session):
        """
        #TODO add comment
        """
        customer_role = CustomerRoleFactory.create(session=session)
        assert customer_role.customer_role_id is not None
    def test_code_default(self, session):
        """
        #TODO add comment
        """
        logging.info("vrtest")
        customer_role = CustomerRoleFactory.create(session=session)
        assert isinstance(customer_role.code, uuid.UUID)
    def test_last_change_code_default_on_build(self, session):
        """
        #TODO add comment
        """
        customer_role: CustomerRole = CustomerRoleFactory.build(session=session)
        assert customer_role.last_change_code == 0
    def test_last_change_code_default_on_creation(self, session):
        """
        #TODO add comment
        """
        customer_role: CustomerRole = CustomerRoleFactory.create(session=session)
        assert customer_role.last_change_code == 1
    def test_last_change_code_default_on_update(self, session):
        """
        #TODO add comment
        """
        customer_role = CustomerRoleFactory.create(session=session)
        initial_code = customer_role.last_change_code
        customer_role.code = uuid.uuid4()
        session.commit()
        assert customer_role.last_change_code != initial_code
    def test_date_inserted_on_build(self, session):
        """
        #TODO add comment
        """
        customer_role = CustomerRoleFactory.build(session=session)
        assert customer_role.insert_utc_date_time is not None
        assert isinstance(customer_role.insert_utc_date_time, datetime)
    def test_date_inserted_on_initial_save(self, session):
        """
        #TODO add comment
        """
        customer_role = CustomerRoleFactory.build(session=session)
        assert customer_role.insert_utc_date_time is not None
        assert isinstance(customer_role.insert_utc_date_time, datetime)
        initial_time = datetime.utcnow() + timedelta(days=-1)
        customer_role.code = uuid.uuid4()
        session.add(customer_role)
        session.commit()
        assert customer_role.insert_utc_date_time > initial_time
    def test_date_inserted_on_second_save(self, session):
        """
        #TODO add comment
        """
        customer_role = CustomerRoleFactory(session=session)
        assert customer_role.insert_utc_date_time is not None
        assert isinstance(customer_role.insert_utc_date_time, datetime)
        initial_time = customer_role.insert_utc_date_time
        customer_role.code = uuid.uuid4()
        time.sleep(1)
        session.commit()
        assert customer_role.insert_utc_date_time == initial_time
    def test_date_updated_on_build(self, session):
        """
        #TODO add comment
        """
        customer_role = CustomerRoleFactory.build(session=session)
        assert customer_role.last_update_utc_date_time is not None
        assert isinstance(customer_role.last_update_utc_date_time, datetime)
    def test_date_updated_on_initial_save(self, session):
        """
        #TODO add comment
        """
        customer_role = CustomerRoleFactory.build(session=session)
        assert customer_role.last_update_utc_date_time is not None
        assert isinstance(customer_role.last_update_utc_date_time, datetime)
        initial_time = datetime.utcnow() + timedelta(days=-1)
        customer_role.code = uuid.uuid4()
        session.add(customer_role)
        session.commit()
        assert customer_role.last_update_utc_date_time > initial_time
    def test_date_updated_on_second_save(self, session):
        """
        #TODO add comment
        """
        customer_role = CustomerRoleFactory(session=session)
        assert customer_role.last_update_utc_date_time is not None
        assert isinstance(customer_role.last_update_utc_date_time, datetime)
        initial_time = customer_role.last_update_utc_date_time
        customer_role.code = uuid.uuid4()
        time.sleep(1)
        session.commit()
        assert customer_role.last_update_utc_date_time > initial_time
    def test_model_deletion(self, session):
        """
        #TODO add comment
        """
        customer_role = CustomerRoleFactory.create(session=session)
        session.delete(customer_role)
        session.commit()
        deleted_customer_role = session.query(CustomerRole).filter_by(
            customer_role_id=customer_role.customer_role_id).first()
        assert deleted_customer_role is None
    def test_data_types(self, session):
        """
        #TODO add comment
        """
        customer_role = CustomerRoleFactory.create(session=session)
        assert isinstance(customer_role.customer_role_id, int)
        assert isinstance(customer_role.code, uuid.UUID)
        assert isinstance(customer_role.last_change_code, int)
        assert isinstance(customer_role.insert_user_id, uuid.UUID)
        assert isinstance(customer_role.last_update_user_id, uuid.UUID)
        assert isinstance(customer_role.customer_id, int)
        assert isinstance(customer_role.is_placeholder, bool)
        assert isinstance(customer_role.placeholder, bool)
        assert isinstance(customer_role.role_id, int)
        # Check for the peek values,
        # assuming they are UUIDs based on your model
# endset
        # customerID
        assert isinstance(
            customer_role.customer_code_peek, uuid.UUID)
        # isPlaceholder,
        # placeholder,
        # roleID
        assert isinstance(
            customer_role.role_code_peek, uuid.UUID)
# endset
        assert isinstance(customer_role.insert_utc_date_time, datetime)
        assert isinstance(customer_role.last_update_utc_date_time, datetime)
    def test_unique_code_constraint(self, session):
        """
        #TODO add comment
        """
        customer_role_1 = CustomerRoleFactory.create(session=session)
        customer_role_2 = CustomerRoleFactory.create(session=session)
        customer_role_2.code = customer_role_1.code
        session.add_all([customer_role_1, customer_role_2])
        with pytest.raises(Exception):
            session.commit()
        session.rollback()
    def test_fields_default(self):
        """
        #TODO add comment
        """
        customer_role = CustomerRole()
        assert customer_role.code is not None
        assert customer_role.last_change_code is not None
        assert customer_role.insert_user_id == uuid.UUID(int=0)
        assert customer_role.last_update_user_id == uuid.UUID(int=0)
        assert customer_role.insert_utc_date_time is not None
        assert customer_role.last_update_utc_date_time is not None
# endset
        # CustomerID
        assert isinstance(
            customer_role.customer_code_peek, uuid.UUID)
        # isPlaceholder,
        # placeholder,
        # RoleID
        assert isinstance(
            customer_role.role_code_peek, uuid.UUID)
# endset
        assert customer_role is not None
        assert customer_role.customer_id == 0
        assert customer_role.is_placeholder is False
        assert customer_role.placeholder is False
        assert customer_role.role_id == 0
# endset
    def test_last_change_code_concurrency(self, session):
        """
        #TODO add comment
        """
        customer_role = CustomerRoleFactory.create(session=session)
        original_last_change_code = customer_role.last_change_code
        customer_role_1 = session.query(CustomerRole).filter_by(
            _customer_role_id=customer_role.customer_role_id).first()
        customer_role_1.code = uuid.uuid4()
        session.commit()
        customer_role_2 = session.query(CustomerRole).filter_by(
            _customer_role_id=customer_role.customer_role_id).first()
        customer_role_2.code = uuid.uuid4()
        session.commit()
        assert customer_role_2.last_change_code != original_last_change_code
# endset
    # CustomerID
    def test_invalid_customer_id(self, session):
        """
        #TODO add comment
        """
        customer_role = CustomerRoleFactory.create(session=session)
        customer_role.customer_id = 99999
        with pytest.raises(IntegrityError):
            session.commit()
        session.rollback()
    # isPlaceholder,
    # placeholder,
    # RoleID
    def test_invalid_role_id(self, session):
        """
        #TODO add comment
        """
        customer_role = CustomerRoleFactory.create(session=session)
        customer_role.role_id = 99999
        with pytest.raises(IntegrityError):
            session.commit()
        session.rollback()
# endset
