# models/factory/tests/organization_test.py
"""
This module contains unit tests for the OrganizationFactory
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
from models import Base, Organization
from models.factory import OrganizationFactory
from services.logging_config import get_logger
logger = get_logger(__name__)
DATABASE_URL = "sqlite:///:memory:"
class TestOrganizationFactory:
    """
    This class contains unit tests for the OrganizationFactory class.
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
    def test_organization_creation(self, session):
        """
        Test case for creating a organization.
        """
        organization = OrganizationFactory.create(session=session)
        assert organization.organization_id is not None
    def test_code_default(self, session):
        """
        Test case for checking the default value of the code attribute.
        """
        logging.info("vrtest")
        organization = OrganizationFactory.create(session=session)
        assert isinstance(organization.code, uuid.UUID)
    def test_last_change_code_default_on_build(self, session):
        """
        Test case for checking the default value of
        the last_change_code attribute on build.
        """
        organization: Organization = OrganizationFactory.build(session=session)
        assert organization.last_change_code == 0
    def test_last_change_code_default_on_creation(self, session):
        """
        Test case for checking the default value of the
        last_change_code attribute on creation.
        """
        organization: Organization = OrganizationFactory.create(session=session)
        assert organization.last_change_code == 1
    def test_last_change_code_default_on_update(self, session):
        """
        Test case for checking the default value of the
        last_change_code attribute on update.
        """
        organization = OrganizationFactory.create(session=session)
        initial_code = organization.last_change_code
        organization.code = uuid.uuid4()
        session.commit()
        assert organization.last_change_code != initial_code
    def test_date_inserted_on_build(self, session):
        """
        Test case for checking the value of the
        insert_utc_date_time attribute on build.
        """
        organization = OrganizationFactory.build(session=session)
        assert organization.insert_utc_date_time is not None
        assert isinstance(organization.insert_utc_date_time, datetime)
    def test_date_inserted_on_initial_save(self, session):
        """
        Test case for checking the value of the
        insert_utc_date_time attribute on initial save.
        """
        organization = OrganizationFactory.build(session=session)
        assert organization.insert_utc_date_time is not None
        assert isinstance(organization.insert_utc_date_time, datetime)
        initial_time = datetime.utcnow() + timedelta(days=-1)
        organization.code = uuid.uuid4()
        session.add(organization)
        session.commit()
        assert organization.insert_utc_date_time > initial_time
    def test_date_inserted_on_second_save(self, session):
        """
        Test case for checking the value of the
        insert_utc_date_time attribute on second save.
        """
        organization = OrganizationFactory(session=session)
        assert organization.insert_utc_date_time is not None
        assert isinstance(organization.insert_utc_date_time, datetime)
        initial_time = organization.insert_utc_date_time
        organization.code = uuid.uuid4()
        time.sleep(1)
        session.commit()
        assert organization.insert_utc_date_time == initial_time
    def test_date_updated_on_build(self, session):
        """
        Test case for checking the value of the
        last_update_utc_date_time attribute on build.
        """
        organization = OrganizationFactory.build(session=session)
        assert organization.last_update_utc_date_time is not None
        assert isinstance(organization.last_update_utc_date_time, datetime)
    def test_date_updated_on_initial_save(self, session):
        """
        Test case for checking the value of the
        last_update_utc_date_time attribute on initial save.
        """
        organization = OrganizationFactory.build(session=session)
        assert organization.last_update_utc_date_time is not None
        assert isinstance(organization.last_update_utc_date_time, datetime)
        initial_time = datetime.utcnow() + timedelta(days=-1)
        organization.code = uuid.uuid4()
        session.add(organization)
        session.commit()
        assert organization.last_update_utc_date_time > initial_time
    def test_date_updated_on_second_save(self, session):
        """
        Test case for checking the value of the
        last_update_utc_date_time attribute on second save.
        """
        organization = OrganizationFactory(session=session)
        assert organization.last_update_utc_date_time is not None
        assert isinstance(organization.last_update_utc_date_time, datetime)
        initial_time = organization.last_update_utc_date_time
        organization.code = uuid.uuid4()
        time.sleep(1)
        session.commit()
        assert organization.last_update_utc_date_time > initial_time
    def test_model_deletion(self, session):
        """
        Test case for deleting a organization model.
        """
        organization = OrganizationFactory.create(session=session)
        session.delete(organization)
        session.commit()
        deleted_organization = session.query(Organization).filter_by(
            organization_id=organization.organization_id).first()
        assert deleted_organization is None
    def test_data_types(self, session):
        """
        Test case for checking the data types of the organization attributes.
        """
        organization = OrganizationFactory.create(session=session)
        assert isinstance(organization.organization_id, int)
        assert isinstance(organization.code, uuid.UUID)
        assert isinstance(organization.last_change_code, int)
        assert isinstance(organization.insert_user_id, uuid.UUID)
        assert isinstance(organization.last_update_user_id, uuid.UUID)
        assert organization.name == "" or isinstance(organization.name, str)
        assert isinstance(organization.tac_id, int)
        # Check for the peek values,
        # assuming they are UUIDs based on your model
# endset
        # name,
        # tacID
        assert isinstance(
            organization.tac_code_peek, uuid.UUID)
# endset
        assert isinstance(organization.insert_utc_date_time, datetime)
        assert isinstance(organization.last_update_utc_date_time, datetime)
    def test_unique_code_constraint(self, session):
        """
        Test case for checking the unique code constraint.
        """
        organization_1 = OrganizationFactory.create(session=session)
        organization_2 = OrganizationFactory.create(session=session)
        organization_2.code = organization_1.code
        session.add_all([organization_1, organization_2])
        with pytest.raises(Exception):
            session.commit()
        session.rollback()
    def test_fields_default(self):
        """
        Test case for checking the default values of the organization fields.
        """
        organization = Organization()
        assert organization.code is not None
        assert organization.last_change_code is not None
        assert organization.insert_user_id == uuid.UUID(int=0)
        assert organization.last_update_user_id == uuid.UUID(int=0)
        assert organization.insert_utc_date_time is not None
        assert organization.last_update_utc_date_time is not None
# endset
        # name,
        # TacID
        assert isinstance(
            organization.tac_code_peek, uuid.UUID)
# endset
        assert organization is not None
        assert organization.name == ""
        assert organization.tac_id == 0
# endset
    def test_last_change_code_concurrency(self, session):
        """
        Test case to verify the concurrency of
        last_change_code in the Organization model.
        This test case checks if the last_change_code
        of a Organization object is updated correctly
        when multiple changes are made concurrently.
        It creates a Organization object, retrieves it
        from the database, and updates its code
        attribute twice in separate transactions.
        Finally, it asserts that the last_change_code
        of the second retrieved Organization object
        is different from the original last_change_code.
        Args:
            session (Session): The SQLAlchemy session object.
        Returns:
            None
        """
        organization = OrganizationFactory.create(session=session)
        original_last_change_code = organization.last_change_code
        organization_1 = session.query(Organization).filter_by(
            _organization_id=organization.organization_id).first()
        organization_1.code = uuid.uuid4()
        session.commit()
        organization_2 = session.query(Organization).filter_by(
            _organization_id=organization.organization_id).first()
        organization_2.code = uuid.uuid4()
        session.commit()
        assert organization_2.last_change_code != original_last_change_code
# endset
    # name,
    # TacID
    def test_invalid_tac_id(self, session):
        """
        Test case to check if an invalid tac ID raises an IntegrityError.
        This test case creates a organization object using
        the OrganizationFactory and assigns an invalid tac ID to it.
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
        organization = OrganizationFactory.create(session=session)
        organization.tac_id = 99999
        with pytest.raises(IntegrityError):
            session.commit()
        session.rollback()
# endset
