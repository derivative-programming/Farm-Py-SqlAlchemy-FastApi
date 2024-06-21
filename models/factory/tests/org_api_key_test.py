# models/factory/tests/org_api_key_test.py
"""
This module contains unit tests for the OrgApiKeyFactory
class in the models.factory package.
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
from models import Base, OrgApiKey
from models.factory import OrgApiKeyFactory
from services.logging_config import get_logger
logger = get_logger(__name__)
DATABASE_URL = "sqlite:///:memory:"
class TestOrgApiKeyFactory:
    """
    This class contains unit tests for the OrgApiKeyFactory class.
    """
    @pytest.fixture(scope="module")
    def engine(self):
        """
        Fixture for creating a database engine.
        """
        engine = create_engine(DATABASE_URL, echo=False)
        # FKs are not activated by default in sqllite
        with engine.connect() as conn:
            conn.connection.execute("PRAGMA foreign_keys=ON")
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
    def test_org_api_key_creation(self, session):
        """
        Test case for creating a org_api_key.
        """
        org_api_key = OrgApiKeyFactory.create(
            session=session)
        assert org_api_key.org_api_key_id is not None
    def test_code_default(self, session):
        """
        Test case for checking the default value of the code attribute.
        """
        logging.info("vrtest")
        org_api_key = OrgApiKeyFactory.create(
            session=session)
        assert isinstance(org_api_key.code, uuid.UUID)
    def test_last_change_code_default_on_build(self, session):
        """
        Test case for checking the default value of
        the last_change_code attribute on build.
        """
        org_api_key: OrgApiKey = OrgApiKeyFactory.build(
            session=session)
        assert org_api_key.last_change_code == 0
    def test_last_change_code_default_on_creation(self, session):
        """
        Test case for checking the default value of the
        last_change_code attribute on creation.
        """
        org_api_key: OrgApiKey = OrgApiKeyFactory.create(
            session=session)
        assert org_api_key.last_change_code == 1
    def test_last_change_code_default_on_update(self, session):
        """
        Test case for checking the default value of the
        last_change_code attribute on update.
        """
        org_api_key = OrgApiKeyFactory.create(
            session=session)
        initial_code = org_api_key.last_change_code
        org_api_key.code = uuid.uuid4()
        session.commit()
        assert org_api_key.last_change_code != initial_code
    def test_date_inserted_on_build(self, session):
        """
        Test case for checking the value of the
        insert_utc_date_time attribute on build.
        """
        org_api_key = OrgApiKeyFactory.build(
            session=session)
        assert org_api_key.insert_utc_date_time is not None
        assert isinstance(
            org_api_key.insert_utc_date_time, datetime)
    def test_date_inserted_on_initial_save(self, session):
        """
        Test case for checking the value of the
        insert_utc_date_time attribute on initial save.
        """
        org_api_key = OrgApiKeyFactory.build(
            session=session)
        assert org_api_key.insert_utc_date_time is not None
        assert isinstance(
            org_api_key.insert_utc_date_time, datetime)
        initial_time = datetime.utcnow() + timedelta(days=-1)
        org_api_key.code = uuid.uuid4()
        session.add(org_api_key)
        session.commit()
        assert org_api_key.insert_utc_date_time > initial_time
    def test_date_inserted_on_second_save(self, session):
        """
        Test case for checking the value of the
        insert_utc_date_time attribute on second save.
        """
        org_api_key = OrgApiKeyFactory(
            session=session)
        assert org_api_key.insert_utc_date_time is not None
        assert isinstance(
            org_api_key.insert_utc_date_time, datetime)
        initial_time = org_api_key.insert_utc_date_time
        org_api_key.code = uuid.uuid4()
        time.sleep(1)
        session.commit()
        assert org_api_key.insert_utc_date_time == initial_time
    def test_date_updated_on_build(self, session):
        """
        Test case for checking the value of the
        last_update_utc_date_time attribute on build.
        """
        org_api_key = OrgApiKeyFactory.build(
            session=session)
        assert org_api_key.last_update_utc_date_time is not None
        assert isinstance(
            org_api_key.last_update_utc_date_time, datetime)
    def test_date_updated_on_initial_save(self, session):
        """
        Test case for checking the value of the
        last_update_utc_date_time attribute on initial save.
        """
        org_api_key = OrgApiKeyFactory.build(
            session=session)
        assert org_api_key.last_update_utc_date_time is not None
        assert isinstance(
            org_api_key.last_update_utc_date_time, datetime)
        initial_time = datetime.utcnow() + timedelta(days=-1)
        org_api_key.code = uuid.uuid4()
        session.add(org_api_key)
        session.commit()
        assert org_api_key.last_update_utc_date_time > initial_time
    def test_date_updated_on_second_save(self, session):
        """
        Test case for checking the value of the
        last_update_utc_date_time attribute on second save.
        """
        org_api_key = OrgApiKeyFactory(
            session=session)
        assert org_api_key.last_update_utc_date_time is not None
        assert isinstance(
            org_api_key.last_update_utc_date_time, datetime)
        initial_time = org_api_key.last_update_utc_date_time
        org_api_key.code = uuid.uuid4()
        time.sleep(1)
        session.commit()
        assert org_api_key.last_update_utc_date_time > initial_time
    def test_model_deletion(self, session):
        """
        Test case for deleting a
        org_api_key model.
        """
        org_api_key = OrgApiKeyFactory.create(
            session=session)
        session.delete(org_api_key)
        session.commit()
        deleted_org_api_key = session.query(OrgApiKey).filter_by(
            org_api_key_id=org_api_key.org_api_key_id).first()
        assert deleted_org_api_key is None
    def test_data_types(self, session):
        """
        Test case for checking the data types of
        the org_api_key attributes.
        """
        org_api_key = OrgApiKeyFactory.create(
            session=session)
        assert isinstance(org_api_key.org_api_key_id, int)
        assert isinstance(org_api_key.code, uuid.UUID)
        assert isinstance(org_api_key.last_change_code, int)
        assert isinstance(org_api_key.insert_user_id, uuid.UUID)
        assert isinstance(org_api_key.last_update_user_id, uuid.UUID)
        assert org_api_key.api_key_value == "" or isinstance(org_api_key.api_key_value, str)
        assert org_api_key.created_by == "" or isinstance(org_api_key.created_by, str)
        assert isinstance(org_api_key.created_utc_date_time, datetime)
        assert isinstance(org_api_key.expiration_utc_date_time, datetime)
        assert isinstance(org_api_key.is_active, bool)
        assert isinstance(org_api_key.is_temp_user_key, bool)
        assert org_api_key.name == "" or isinstance(org_api_key.name, str)
        assert isinstance(org_api_key.organization_id, int)
        assert isinstance(org_api_key.org_customer_id, int)
        # Check for the peek values,
        # assuming they are UUIDs based on your model
# endset
        # apiKeyValue,
        # createdBy,
        # createdUTCDateTime
        # expirationUTCDateTime
        # isActive,
        # isTempUserKey,
        # name,
        # organizationID
        assert isinstance(
            org_api_key.organization_code_peek, uuid.UUID)
        # orgCustomerID
        assert isinstance(
            org_api_key.org_customer_code_peek, uuid.UUID)
# endset
        assert isinstance(org_api_key.insert_utc_date_time, datetime)
        assert isinstance(org_api_key.last_update_utc_date_time, datetime)
    def test_unique_code_constraint(self, session):
        """
        Test case for checking the unique code constraint.
        """
        org_api_key_1 = OrgApiKeyFactory.create(session=session)
        org_api_key_2 = OrgApiKeyFactory.create(session=session)
        org_api_key_2.code = org_api_key_1.code
        session.add_all([org_api_key_1, org_api_key_2])
        with pytest.raises(Exception):
            session.commit()
        session.rollback()
    def test_fields_default(self):
        """
        Test case for checking the default values of
        the org_api_key fields.
        """
        org_api_key = OrgApiKey()
        assert org_api_key.code is not None
        assert org_api_key.last_change_code is not None
        assert org_api_key.insert_user_id == uuid.UUID(int=0)
        assert org_api_key.last_update_user_id == uuid.UUID(int=0)
        assert org_api_key.insert_utc_date_time is not None
        assert org_api_key.last_update_utc_date_time is not None
# endset
        # apiKeyValue,
        # createdBy,
        # createdUTCDateTime
        # expirationUTCDateTime
        # isActive,
        # isTempUserKey,
        # name,
        # OrganizationID
        assert isinstance(
            org_api_key.organization_code_peek, uuid.UUID)
        # OrgCustomerID
        assert isinstance(
            org_api_key.org_customer_code_peek, uuid.UUID)
# endset
        assert org_api_key is not None
        assert org_api_key.api_key_value == ""
        assert org_api_key.created_by == ""
        assert org_api_key.created_utc_date_time == datetime(1753, 1, 1)
        assert org_api_key.expiration_utc_date_time == datetime(1753, 1, 1)
        assert org_api_key.is_active is False
        assert org_api_key.is_temp_user_key is False
        assert org_api_key.name == ""
        assert org_api_key.organization_id == 0
        assert org_api_key.org_customer_id == 0
# endset
    def test_last_change_code_concurrency(self, session):
        """
        Test case to verify the concurrency of
        last_change_code in the OrgApiKey
        model.
        This test case checks if the last_change_code
        of a OrgApiKey object is
        updated correctly
        when multiple changes are made concurrently.
        It creates a OrgApiKey object,
        retrieves it from the database, and updates its code
        attribute twice in separate transactions.
        Finally, it asserts that the last_change_code
        of the second retrieved OrgApiKey object
        is different from the original last_change_code.
        Args:
            session (Session): The SQLAlchemy session object.
        Returns:
            None
        """
        org_api_key = OrgApiKeyFactory.create(
            session=session)
        original_last_change_code = org_api_key.last_change_code
        org_api_key_1 = session.query(OrgApiKey).filter_by(
            _org_api_key_id=org_api_key.org_api_key_id).first()
        org_api_key_1.code = uuid.uuid4()
        session.commit()
        org_api_key_2 = session.query(OrgApiKey).filter_by(
            _org_api_key_id=org_api_key.org_api_key_id).first()
        org_api_key_2.code = uuid.uuid4()
        session.commit()
        assert org_api_key_2.last_change_code != original_last_change_code
# endset
    # apiKeyValue,
    # createdBy,
    # createdUTCDateTime
    # expirationUTCDateTime
    # isActive,
    # isTempUserKey,
    # name,
    # OrganizationID
    def test_invalid_organization_id(self, session):
        """
        Test case to check if an invalid organization ID raises an IntegrityError.
        This test case creates a org_api_key object using
        the OrgApiKeyFactory and assigns an invalid organization ID to it.
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
        org_api_key = OrgApiKeyFactory.create(
            session=session)
        org_api_key.organization_id = 99999
        with pytest.raises(IntegrityError):
            session.commit()
        session.rollback()
    # OrgCustomerID
    def test_invalid_org_customer_id(self, session):
        """
        Test case to check if an invalid org_customer ID raises an IntegrityError.
        This test case creates a org_api_key object using
        the OrgApiKeyFactory and assigns an invalid org_customer ID to it.
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
        org_api_key = OrgApiKeyFactory.create(
            session=session)
        org_api_key.org_customer_id = 99999
        with pytest.raises(IntegrityError):
            session.commit()
        session.rollback()
# endset
