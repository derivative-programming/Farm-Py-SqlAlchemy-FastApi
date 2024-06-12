# models/factory/tests/org_customer_test.py
"""
    #TODO add comment
"""
from decimal import Decimal
import pytest
import time
import math
from decimal import Decimal
from datetime import datetime, date, timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, OrgCustomer
from models.factory import OrgCustomerFactory
from services.db_config import DB_DIALECT
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
from services.db_config import DB_DIALECT,generate_uuid
from sqlalchemy import String
from sqlalchemy.exc import IntegrityError
DATABASE_URL = "sqlite:///:memory:"
DB_DIALECT = "sqlite"
# Conditionally set the UUID column type
if DB_DIALECT == 'postgresql':
    UUIDType = UUID(as_uuid=True)
elif DB_DIALECT == 'mssql':
    UUIDType = UNIQUEIDENTIFIER
else:  # This will cover SQLite, MySQL, and other databases
    UUIDType = String(36)
class TestOrgCustomerFactory:
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
    def test_org_customer_creation(self, session):
        """
        #TODO add comment
        """
        org_customer = OrgCustomerFactory.create(session=session)
        assert org_customer.org_customer_id is not None
    def test_code_default(self, session):
        """
        #TODO add comment
        """
        org_customer = OrgCustomerFactory.create(session=session)
        if DB_DIALECT == 'postgresql':
            assert isinstance(org_customer.code, UUID)
        elif DB_DIALECT == 'mssql':
            assert isinstance(org_customer.code, UNIQUEIDENTIFIER)
        else:  # This will cover SQLite, MySQL, and other databases
            assert isinstance(org_customer.code, str)
    def test_last_change_code_default_on_build(self, session):
        """
        #TODO add comment
        """
        org_customer: OrgCustomer = OrgCustomerFactory.build(session=session)
        assert org_customer.last_change_code == 0
    def test_last_change_code_default_on_creation(self, session):
        """
        #TODO add comment
        """
        org_customer: OrgCustomer = OrgCustomerFactory.create(session=session)
        assert org_customer.last_change_code == 1
    def test_last_change_code_default_on_update(self, session):
        """
        #TODO add comment
        """
        org_customer = OrgCustomerFactory.create(session=session)
        initial_code = org_customer.last_change_code
        org_customer.code = generate_uuid()
        session.commit()
        assert org_customer.last_change_code != initial_code
    def test_date_inserted_on_build(self, session):
        """
        #TODO add comment
        """
        org_customer = OrgCustomerFactory.build(session=session)
        assert org_customer.insert_utc_date_time is not None
        assert isinstance(org_customer.insert_utc_date_time, datetime)
    def test_date_inserted_on_initial_save(self, session):
        """
        #TODO add comment
        """
        org_customer = OrgCustomerFactory.build(session=session)
        assert org_customer.insert_utc_date_time is not None
        assert isinstance(org_customer.insert_utc_date_time, datetime)
        initial_time = datetime.utcnow() + timedelta(days=-1)
        org_customer.code = generate_uuid()
        session.commit()
        assert org_customer.insert_utc_date_time > initial_time
    def test_date_inserted_on_second_save(self, session):
        """
        #TODO add comment
        """
        org_customer = OrgCustomerFactory(session=session)
        assert org_customer.insert_utc_date_time is not None
        assert isinstance(org_customer.insert_utc_date_time, datetime)
        initial_time = org_customer.insert_utc_date_time
        org_customer.code = generate_uuid()
        time.sleep(1)
        session.commit()
        assert org_customer.insert_utc_date_time == initial_time
    def test_date_updated_on_build(self, session):
        """
        #TODO add comment
        """
        org_customer = OrgCustomerFactory.build(session=session)
        assert org_customer.last_update_utc_date_time is not None
        assert isinstance(org_customer.last_update_utc_date_time, datetime)
    def test_date_updated_on_initial_save(self, session):
        """
        #TODO add comment
        """
        org_customer = OrgCustomerFactory.build(session=session)
        assert org_customer.last_update_utc_date_time is not None
        assert isinstance(org_customer.last_update_utc_date_time, datetime)
        initial_time = datetime.utcnow() + timedelta(days=-1)
        org_customer.code = generate_uuid()
        session.commit()
        assert org_customer.last_update_utc_date_time > initial_time
    def test_date_updated_on_second_save(self, session):
        """
        #TODO add comment
        """
        org_customer = OrgCustomerFactory(session=session)
        assert org_customer.last_update_utc_date_time is not None
        assert isinstance(org_customer.last_update_utc_date_time, datetime)
        initial_time = org_customer.last_update_utc_date_time
        org_customer.code = generate_uuid()
        time.sleep(1)
        session.commit()
        assert org_customer.last_update_utc_date_time > initial_time
    def test_model_deletion(self, session):
        """
        #TODO add comment
        """
        org_customer = OrgCustomerFactory.create(session=session)
        session.delete(org_customer)
        session.commit()
        deleted_org_customer = session.query(OrgCustomer).filter_by(
            org_customer_id=org_customer.org_customer_id).first()
        assert deleted_org_customer is None
    def test_data_types(self, session):
        """
        #TODO add comment
        """
        org_customer = OrgCustomerFactory.create(session=session)
        assert isinstance(org_customer.org_customer_id, int)
        if DB_DIALECT == 'postgresql':
            assert isinstance(org_customer.code, UUID)
        elif DB_DIALECT == 'mssql':
            assert isinstance(org_customer.code, UNIQUEIDENTIFIER)
        else:  # This will cover SQLite, MySQL, and other databases
            assert isinstance(org_customer.code, str)
        assert isinstance(org_customer.last_change_code, int)
        if DB_DIALECT == 'postgresql':
            assert isinstance(org_customer.insert_user_id, UUID)
        elif DB_DIALECT == 'mssql':
            assert isinstance(org_customer.insert_user_id, UNIQUEIDENTIFIER)
        else:  # This will cover SQLite, MySQL, and other databases
            assert isinstance(org_customer.insert_user_id, str)
        if DB_DIALECT == 'postgresql':
            assert isinstance(org_customer.last_update_user_id, UUID)
        elif DB_DIALECT == 'mssql':
            assert isinstance(org_customer.last_update_user_id, UNIQUEIDENTIFIER)
        else:  # This will cover SQLite, MySQL, and other databases
            assert isinstance(org_customer.last_update_user_id, str)
        assert isinstance(org_customer.customer_id, int)
        assert org_customer.email == "" or isinstance(
            org_customer.email, str)
        assert isinstance(org_customer.organization_id, int)
        # Check for the peek values,
        # assuming they are UUIDs based on your model
# endset
        # customerID
        if DB_DIALECT == 'postgresql':
            assert isinstance(
                org_customer.customer_code_peek, UUID)
        elif DB_DIALECT == 'mssql':
            assert isinstance(
                org_customer.customer_code_peek, UNIQUEIDENTIFIER)
        else:  # This will cover SQLite, MySQL, and other databases
            assert isinstance(
                org_customer.customer_code_peek, str)
        # email,
        # organizationID
        if DB_DIALECT == 'postgresql':
            assert isinstance(
                org_customer.organization_code_peek, UUID)
        elif DB_DIALECT == 'mssql':
            assert isinstance(
                org_customer.organization_code_peek, UNIQUEIDENTIFIER)
        else:  # This will cover SQLite, MySQL, and other databases
            assert isinstance(
                org_customer.organization_code_peek, str)
# endset
        assert isinstance(org_customer.insert_utc_date_time, datetime)
        assert isinstance(org_customer.last_update_utc_date_time, datetime)
    def test_unique_code_constraint(self, session):
        """
        #TODO add comment
        """
        org_customer_1 = OrgCustomerFactory.create(session=session)
        org_customer_2 = OrgCustomerFactory.create(session=session)
        org_customer_2.code = org_customer_1.code
        session.add_all([org_customer_1, org_customer_2])
        with pytest.raises(Exception):
            session.commit()
        session.rollback()
    def test_fields_default(self, session):
        """
        #TODO add comment
        """
        org_customer = OrgCustomer()
        assert org_customer.code is not None
        assert org_customer.last_change_code is not None
        assert org_customer.insert_user_id is None
        assert org_customer.last_update_user_id is None
        assert org_customer.insert_utc_date_time is not None
        assert org_customer.last_update_utc_date_time is not None
# endset
        # CustomerID
        if DB_DIALECT == 'postgresql':
            assert isinstance(
                org_customer.customer_code_peek, UUID)
        elif DB_DIALECT == 'mssql':
            assert isinstance(
                org_customer.customer_code_peek,
                UNIQUEIDENTIFIER)
        else:  # This will cover SQLite, MySQL, and other databases
            assert isinstance(
                org_customer.customer_code_peek, str)
        # email,
        # OrganizationID
        if DB_DIALECT == 'postgresql':
            assert isinstance(
                org_customer.organization_code_peek, UUID)
        elif DB_DIALECT == 'mssql':
            assert isinstance(
                org_customer.organization_code_peek,
                UNIQUEIDENTIFIER)
        else:  # This will cover SQLite, MySQL, and other databases
            assert isinstance(
                org_customer.organization_code_peek, str)
# endset
        assert org_customer.customer_id == 0
        assert org_customer.email == ""
        assert org_customer.organization_id == 0
# endset
    def test_last_change_code_concurrency(self, session):
        """
        #TODO add comment
        """
        org_customer = OrgCustomerFactory.create(session=session)
        original_last_change_code = org_customer.last_change_code
        org_customer_1 = session.query(OrgCustomer).filter_by(
            org_customer_id=org_customer.org_customer_id).first()
        org_customer_1.code = generate_uuid()
        session.commit()
        org_customer_2 = session.query(OrgCustomer).filter_by(
            org_customer_id=org_customer.org_customer_id).first()
        org_customer_2.code = generate_uuid()
        session.commit()
        assert org_customer_2.last_change_code != original_last_change_code
# endset
    # CustomerID
    def test_invalid_customer_id(self, session):
        """
        #TODO add comment
        """
        org_customer = OrgCustomerFactory.create(session=session)
        org_customer.customer_id = 99999
        with pytest.raises(IntegrityError):
            session.commit()
        session.rollback()
    # email,
    # OrganizationID
    def test_invalid_organization_id(self, session):
        """
        #TODO add comment
        """
        org_customer = OrgCustomerFactory.create(session=session)
        org_customer.organization_id = 99999
        with pytest.raises(IntegrityError):
            session.commit()
        session.rollback()
# endset
