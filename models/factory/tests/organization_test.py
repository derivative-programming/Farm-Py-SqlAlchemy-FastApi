from decimal import Decimal
import pytest
import uuid
import time
from decimal import Decimal
from datetime import datetime, date
from sqlalchemy import Numeric, create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Organization
from models.factory import OrganizationFactory
from services.db_config import db_dialect
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
from services.db_config import db_dialect,generate_uuid
from sqlalchemy import String
from sqlalchemy.exc import IntegrityError
DATABASE_URL = "sqlite:///:memory:"
db_dialect = "sqlite"
# Conditionally set the UUID column type
if db_dialect == 'postgresql':
    UUIDType = UUID(as_uuid=True)
elif db_dialect == 'mssql':
    UUIDType = UNIQUEIDENTIFIER
else:  # This will cover SQLite, MySQL, and other databases
    UUIDType = String(36)
class TestOrganizationFactory:
    @pytest.fixture(scope="module")
    def engine(self):
        engine = create_engine(DATABASE_URL, echo=True)
        #FKs are not activated by default in sqllite
        with engine.connect() as conn:
            conn.connection.execute("PRAGMA foreign_keys=ON")
        yield engine
        engine.dispose()
    @pytest.fixture
    def session(self, engine):
        Base.metadata.create_all(engine)
        SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)
        session_instance = SessionLocal()
        yield session_instance
        session_instance.close()
    def test_organization_creation(self, session):
        organization = OrganizationFactory.create(session=session)
        assert organization.organization_id is not None
    def test_code_default(self, session):
        organization = OrganizationFactory.create(session=session)
        if db_dialect == 'postgresql':
            assert isinstance(organization.code, UUID)
        elif db_dialect == 'mssql':
            assert isinstance(organization.code, UNIQUEIDENTIFIER)
        else:  # This will cover SQLite, MySQL, and other databases
            assert isinstance(organization.code, str)
    def test_last_change_code_default_on_build(self, session):
        organization:Organization = OrganizationFactory.build(session=session)
        assert organization.last_change_code == 0
    def test_last_change_code_default_on_creation(self, session):
        organization:Organization = OrganizationFactory.create(session=session)
        assert organization.last_change_code == 1
    def test_last_change_code_default_on_update(self, session):
        organization = OrganizationFactory.create(session=session)
        initial_code = organization.last_change_code
        organization.code = generate_uuid()
        session.commit()
        assert organization.last_change_code != initial_code
    def test_date_inserted_on_build(self, session):
        organization = OrganizationFactory.build(session=session)
        assert organization.insert_utc_date_time is not None
        assert isinstance(organization.insert_utc_date_time, datetime)
    def test_date_inserted_on_initial_save(self, session):
        organization = OrganizationFactory.build(session=session)
        assert organization.insert_utc_date_time is not None
        assert isinstance(organization.insert_utc_date_time, datetime)
        initial_time = organization.insert_utc_date_time
        organization.code = generate_uuid()
        time.sleep(2)
        session.commit()
        assert organization.insert_utc_date_time > initial_time
    def test_date_inserted_on_second_save(self, session):
        organization = OrganizationFactory(session=session)
        assert organization.insert_utc_date_time is not None
        assert isinstance(organization.insert_utc_date_time, datetime)
        initial_time = organization.insert_utc_date_time
        organization.code = generate_uuid()
        time.sleep(2)
        session.commit()
        assert organization.insert_utc_date_time == initial_time
    def test_date_updated_on_build(self, session):
        organization = OrganizationFactory.build(session=session)
        assert organization.last_update_utc_date_time is not None
        assert isinstance(organization.last_update_utc_date_time, datetime)
    def test_date_updated_on_initial_save(self, session):
        organization = OrganizationFactory.build(session=session)
        assert organization.last_update_utc_date_time is not None
        assert isinstance(organization.last_update_utc_date_time, datetime)
        initial_time = organization.last_update_utc_date_time
        organization.code = generate_uuid()
        time.sleep(2)
        session.commit()
        assert organization.last_update_utc_date_time > initial_time
    def test_date_updated_on_second_save(self, session):
        organization = OrganizationFactory(session=session)
        assert organization.last_update_utc_date_time is not None
        assert isinstance(organization.last_update_utc_date_time, datetime)
        initial_time = organization.last_update_utc_date_time
        organization.code = generate_uuid()
        time.sleep(2)
        session.commit()
        assert organization.last_update_utc_date_time > initial_time
    def test_model_deletion(self, session):
        organization = OrganizationFactory.create(session=session)
        session.delete(organization)
        session.commit()
        deleted_organization = session.query(Organization).filter_by(organization_id=organization.organization_id).first()
        assert deleted_organization is None
    def test_data_types(self, session):
        organization = OrganizationFactory.create(session=session)
        assert isinstance(organization.organization_id, int)
        if db_dialect == 'postgresql':
            assert isinstance(organization.code, UUID)
        elif db_dialect == 'mssql':
            assert isinstance(organization.code, UNIQUEIDENTIFIER)
        else:  # This will cover SQLite, MySQL, and other databases
            assert isinstance(organization.code, str)
        assert isinstance(organization.last_change_code, int)
        if db_dialect == 'postgresql':
            assert isinstance(organization.insert_user_id, UUID)
        elif db_dialect == 'mssql':
            assert isinstance(organization.insert_user_id, UNIQUEIDENTIFIER)
        else:  # This will cover SQLite, MySQL, and other databases
            assert isinstance(organization.insert_user_id, str)
        if db_dialect == 'postgresql':
            assert isinstance(organization.last_update_user_id, UUID)
        elif db_dialect == 'mssql':
            assert isinstance(organization.last_update_user_id, UNIQUEIDENTIFIER)
        else:  # This will cover SQLite, MySQL, and other databases
            assert isinstance(organization.last_update_user_id, str)
        assert organization.name == "" or isinstance(organization.name, str)
        assert isinstance(organization.tac_id, int)
        # Check for the peek values, assuming they are UUIDs based on your model

        #name,
        #tacID
        if db_dialect == 'postgresql':
            assert isinstance(organization.tac_code_peek, UUID)
        elif db_dialect == 'mssql':
            assert isinstance(organization.tac_code_peek, UNIQUEIDENTIFIER)
        else:  # This will cover SQLite, MySQL, and other databases
            assert isinstance(organization.tac_code_peek, str)

        assert isinstance(organization.insert_utc_date_time, datetime)
        assert isinstance(organization.last_update_utc_date_time, datetime)
    def test_unique_code_constraint(self, session):
        organization_1 = OrganizationFactory.create(session=session)
        organization_2 = OrganizationFactory.create(session=session)
        organization_2.code = organization_1.code
        session.add_all([organization_1, organization_2])
        with pytest.raises(Exception):  # adjust for the specific DB exception you'd expect
            session.commit()
        session.rollback()
    def test_fields_default(self, session):
        organization = Organization()
        assert organization.code is not None
        assert organization.last_change_code is not None
        assert organization.insert_user_id is None
        assert organization.last_update_user_id is None
        assert organization.insert_utc_date_time is not None
        assert organization.last_update_utc_date_time is not None

        #name,
        #TacID
        if db_dialect == 'postgresql':
            assert isinstance(organization.tac_code_peek, UUID)
        elif db_dialect == 'mssql':
            assert isinstance(organization.tac_code_peek, UNIQUEIDENTIFIER)
        else:  # This will cover SQLite, MySQL, and other databases
            assert isinstance(organization.tac_code_peek, str)

        assert organization.name == ""
        assert organization.tac_id == 0

    def test_last_change_code_concurrency(self, session):
        organization = OrganizationFactory.create(session=session)
        original_last_change_code = organization.last_change_code
        organization_1 = session.query(Organization).filter_by(organization_id=organization.organization_id).first()
        organization_1.code = generate_uuid()
        session.commit()
        organization_2 = session.query(Organization).filter_by(organization_id=organization.organization_id).first()
        organization_2.code = generate_uuid()
        session.commit()
        assert organization_2.last_change_code != original_last_change_code

    #name,
    #TacID
    def test_invalid_tac_id(self, session):
        organization = OrganizationFactory.create(session=session)
        organization.tac_id = 99999
        with pytest.raises(IntegrityError):  # adjust for the specific DB exception you'd expect
            session.commit()
        session.rollback()

