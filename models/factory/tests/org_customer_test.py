# models/factory/tests/org_customer_test.py
"""
This module contains unit tests for the OrgCustomerFactory
class in the models.factory package.
"""
from decimal import Decimal
import time
import math
import uuid
import logging
from datetime import datetime, date, timedelta
import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from models import Base, OrgCustomer
from models.factory import OrgCustomerFactory
from services.logging_config import get_logger
logger = get_logger(__name__)
DATABASE_URL = "sqlite:///:memory:"
class TestOrgCustomerFactory:
    """
    This class contains unit tests for the OrgCustomerFactory class.
    """
    @pytest.fixture(scope="module")
    def engine(self):
        """
        Fixture for creating a database engine.
        """
        engine = create_engine(DATABASE_URL, echo=False)
        # FKs are not activated by default in sqllite
        with engine.connect() as conn:
            conn.execute(text("PRAGMA foreign_keys=ON"))
        yield engine
        engine.dispose()
    @pytest.fixture
    def session(self, engine):
        """
        Fixture for creating a database session.
        """
        Base.metadata.create_all(engine)
        SessionLocal = sessionmaker(  # pylint: disable=invalid-name
            bind=engine, expire_on_commit=False)
        session_instance = SessionLocal()
        yield session_instance
        session_instance.close()
    def test_org_customer_creation(self, session):
        """
        Test case for creating a org_customer.
        """
        org_customer = OrgCustomerFactory.create(
            session=session)
        assert org_customer.org_customer_id is not None
    def test_code_default(self, session):
        """
        Test case for checking the default value of the code attribute.
        """
        logging.info("vrtest")
        org_customer = OrgCustomerFactory.create(
            session=session)
        assert isinstance(org_customer.code, uuid.UUID)
    def test_last_change_code_default_on_build(self, session):
        """
        Test case for checking the default value of
        the last_change_code attribute on build.
        """
        org_customer: OrgCustomer = OrgCustomerFactory.build(
            session=session)
        assert org_customer.last_change_code == 0
    def test_last_change_code_default_on_creation(self, session):
        """
        Test case for checking the default value of the
        last_change_code attribute on creation.
        """
        org_customer: OrgCustomer = OrgCustomerFactory.create(
            session=session)
        assert org_customer.last_change_code == 1
    def test_last_change_code_default_on_update(self, session):
        """
        Test case for checking the default value of the
        last_change_code attribute on update.
        """
        org_customer = OrgCustomerFactory.create(
            session=session)
        initial_code = org_customer.last_change_code
        org_customer.code = uuid.uuid4()
        session.commit()
        assert org_customer.last_change_code != initial_code
    def test_date_inserted_on_build(self, session):
        """
        Test case for checking the value of the
        insert_utc_date_time attribute on build.
        """
        org_customer = OrgCustomerFactory.build(
            session=session)
        assert org_customer.insert_utc_date_time is not None
        assert isinstance(
            org_customer.insert_utc_date_time, datetime)
    def test_date_inserted_on_initial_save(self, session):
        """
        Test case for checking the value of the
        insert_utc_date_time attribute on initial save.
        """
        org_customer = OrgCustomerFactory.build(
            session=session)
        assert org_customer.insert_utc_date_time is not None
        assert isinstance(
            org_customer.insert_utc_date_time, datetime)
        initial_time = datetime.utcnow() + timedelta(days=-1)
        org_customer.code = uuid.uuid4()
        session.add(org_customer)
        session.commit()
        assert org_customer.insert_utc_date_time > initial_time
    def test_date_inserted_on_second_save(self, session):
        """
        Test case for checking the value of the
        insert_utc_date_time attribute on second save.
        """
        org_customer = OrgCustomerFactory(
            session=session)
        assert org_customer.insert_utc_date_time is not None
        assert isinstance(
            org_customer.insert_utc_date_time, datetime)
        initial_time = org_customer.insert_utc_date_time
        org_customer.code = uuid.uuid4()
        time.sleep(1)
        session.commit()
        assert org_customer.insert_utc_date_time == initial_time
    def test_date_updated_on_build(self, session):
        """
        Test case for checking the value of the
        last_update_utc_date_time attribute on build.
        """
        org_customer = OrgCustomerFactory.build(
            session=session)
        assert org_customer.last_update_utc_date_time is not None
        assert isinstance(
            org_customer.last_update_utc_date_time, datetime)
    def test_date_updated_on_initial_save(self, session):
        """
        Test case for checking the value of the
        last_update_utc_date_time attribute on initial save.
        """
        org_customer = OrgCustomerFactory.build(
            session=session)
        assert org_customer.last_update_utc_date_time is not None
        assert isinstance(
            org_customer.last_update_utc_date_time, datetime)
        initial_time = datetime.utcnow() + timedelta(days=-1)
        org_customer.code = uuid.uuid4()
        session.add(org_customer)
        session.commit()
        assert org_customer.last_update_utc_date_time > initial_time
    def test_date_updated_on_second_save(self, session):
        """
        Test case for checking the value of the
        last_update_utc_date_time attribute on second save.
        """
        org_customer = OrgCustomerFactory(
            session=session)
        assert org_customer.last_update_utc_date_time is not None
        assert isinstance(
            org_customer.last_update_utc_date_time, datetime)
        initial_time = org_customer.last_update_utc_date_time
        org_customer.code = uuid.uuid4()
        time.sleep(1)
        session.commit()
        assert org_customer.last_update_utc_date_time > initial_time
    def test_model_deletion(self, session):
        """
        Test case for deleting a
        org_customer model.
        """
        org_customer = OrgCustomerFactory.create(
            session=session)
        session.delete(org_customer)
        session.commit()
        deleted_org_customer = session.query(OrgCustomer).filter_by(
            org_customer_id=org_customer.org_customer_id).first()
        assert deleted_org_customer is None
    def test_data_types(self, session):
        """
        Test case for checking the data types of
        the org_customer attributes.
        """
        org_customer = OrgCustomerFactory.create(
            session=session)
        assert isinstance(org_customer.org_customer_id, int)
        assert isinstance(org_customer.code, uuid.UUID)
        assert isinstance(org_customer.last_change_code, int)
        assert isinstance(org_customer.insert_user_id, uuid.UUID)
        assert isinstance(org_customer.last_update_user_id, uuid.UUID)
        assert isinstance(org_customer.customer_id, int)
        assert org_customer.email == "" or isinstance(
            org_customer.email, str)
        assert isinstance(org_customer.organization_id, int)
        # Check for the peek values,
        # assuming they are UUIDs based on your model
# endset
        # customerID
        assert isinstance(
            org_customer.customer_code_peek, uuid.UUID)
        # email,
        # organizationID
        assert isinstance(
            org_customer.organization_code_peek, uuid.UUID)
# endset
        assert isinstance(org_customer.insert_utc_date_time, datetime)
        assert isinstance(org_customer.last_update_utc_date_time, datetime)
    def test_unique_code_constraint(self, session):
        """
        Test case for checking the unique code constraint.
        """
        org_customer_1 = OrgCustomerFactory.create(session=session)
        org_customer_2 = OrgCustomerFactory.create(session=session)
        org_customer_2.code = org_customer_1.code
        session.add_all([org_customer_1, org_customer_2])
        with pytest.raises(Exception):
            session.commit()
        session.rollback()
    def test_fields_default(self):
        """
        Test case for checking the default values of
        the org_customer fields.
        """
        org_customer = OrgCustomer()
        assert org_customer.code is not None
        assert org_customer.last_change_code is not None
        assert org_customer.insert_user_id == uuid.UUID(int=0)
        assert org_customer.last_update_user_id == uuid.UUID(int=0)
        assert org_customer.insert_utc_date_time is not None
        assert org_customer.last_update_utc_date_time is not None
# endset
        # CustomerID
        assert isinstance(
            org_customer.customer_code_peek, uuid.UUID)
        # email,
        # OrganizationID
        assert isinstance(
            org_customer.organization_code_peek, uuid.UUID)
# endset
        assert org_customer is not None
        assert org_customer.customer_id == 0
        assert org_customer.email == ""
        assert org_customer.organization_id == 0
# endset
    def test_last_change_code_concurrency(self, session):
        """
        Test case to verify the concurrency of
        last_change_code in the OrgCustomer
        model.
        This test case checks if the last_change_code
        of a OrgCustomer object is
        updated correctly
        when multiple changes are made concurrently.
        It creates a OrgCustomer object,
        retrieves it from the database, and updates its code
        attribute twice in separate transactions.
        Finally, it asserts that the last_change_code
        of the second retrieved OrgCustomer object
        is different from the original last_change_code.
        Args:
            session (Session): The SQLAlchemy session object.
        Returns:
            None
        """
        org_customer = OrgCustomerFactory.create(
            session=session)
        original_last_change_code = org_customer.last_change_code
        org_customer_1 = session.query(OrgCustomer).filter_by(
            _org_customer_id=org_customer.org_customer_id).first()
        org_customer_1.code = uuid.uuid4()
        session.commit()
        org_customer_2 = session.query(OrgCustomer).filter_by(
            _org_customer_id=org_customer.org_customer_id).first()
        org_customer_2.code = uuid.uuid4()
        session.commit()
        assert org_customer_2.last_change_code != original_last_change_code
# endset
    # CustomerID
    def test_invalid_customer_id(self, session):
        """
        Test case to check if an invalid customer ID raises an IntegrityError.
        This test case creates a org_customer object using
        the OrgCustomerFactory and assigns an invalid customer ID to it.
        It then tries to commit the changes to the
        session and expects an IntegrityError to be raised.
        Finally, it rolls back the session to ensure
        no changes are persisted.
        Args:
            session (Session): The SQLAlchemy session object.
        Raises:
            IntegrityError: If the changes to the
                session violate any integrity constraints.
        """
        org_customer = OrgCustomerFactory.create(
            session=session)
        org_customer.customer_id = 99999
        with pytest.raises(IntegrityError):
            session.commit()
        session.rollback()
    # email,
    # OrganizationID
    def test_invalid_organization_id(self, session):
        """
        Test case to check if an invalid organization ID raises an IntegrityError.
        This test case creates a org_customer object using
        the OrgCustomerFactory and assigns an invalid organization ID to it.
        It then tries to commit the changes to the
        session and expects an IntegrityError to be raised.
        Finally, it rolls back the session to ensure
        no changes are persisted.
        Args:
            session (Session): The SQLAlchemy session object.
        Raises:
            IntegrityError: If the changes to the
                session violate any integrity constraints.
        """
        org_customer = OrgCustomerFactory.create(
            session=session)
        org_customer.organization_id = 99999
        with pytest.raises(IntegrityError):
            session.commit()
        session.rollback()
# endset
