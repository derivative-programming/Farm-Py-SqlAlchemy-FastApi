from decimal import Decimal
import pytest
import uuid
import time
from decimal import Decimal
from datetime import datetime, date
from sqlalchemy import Numeric, create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Flavor
from models.factory import FlavorFactory
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
class TestFlavorFactory:
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
    def test_flavor_creation(self, session):
        flavor = FlavorFactory.create(session=session)
        assert flavor.flavor_id is not None
    def test_code_default(self, session):
        flavor = FlavorFactory.create(session=session)
        if db_dialect == 'postgresql':
            assert isinstance(flavor.code, UUID)
        elif db_dialect == 'mssql':
            assert isinstance(flavor.code, UNIQUEIDENTIFIER)
        else:  # This will cover SQLite, MySQL, and other databases
            assert isinstance(flavor.code, str)
    def test_last_change_code_default_on_build(self, session):
        flavor:Flavor = FlavorFactory.build(session=session)
        assert flavor.last_change_code == 0
    def test_last_change_code_default_on_creation(self, session):
        flavor:Flavor = FlavorFactory.create(session=session)
        assert flavor.last_change_code == 1
    def test_last_change_code_default_on_update(self, session):
        flavor = FlavorFactory.create(session=session)
        initial_code = flavor.last_change_code
        flavor.code = generate_uuid()
        session.commit()
        assert flavor.last_change_code != initial_code
    def test_date_inserted_on_build(self, session):
        flavor = FlavorFactory.build(session=session)
        assert flavor.insert_utc_date_time is not None
        assert isinstance(flavor.insert_utc_date_time, datetime)
    def test_date_inserted_on_initial_save(self, session):
        flavor = FlavorFactory.build(session=session)
        assert flavor.insert_utc_date_time is not None
        assert isinstance(flavor.insert_utc_date_time, datetime)
        initial_time = flavor.insert_utc_date_time
        flavor.code = generate_uuid()
        time.sleep(2)
        session.commit()
        assert flavor.insert_utc_date_time > initial_time
    def test_date_inserted_on_second_save(self, session):
        flavor = FlavorFactory(session=session)
        assert flavor.insert_utc_date_time is not None
        assert isinstance(flavor.insert_utc_date_time, datetime)
        initial_time = flavor.insert_utc_date_time
        flavor.code = generate_uuid()
        time.sleep(2)
        session.commit()
        assert flavor.insert_utc_date_time == initial_time
    def test_date_updated_on_build(self, session):
        flavor = FlavorFactory.build(session=session)
        assert flavor.last_update_utc_date_time is not None
        assert isinstance(flavor.last_update_utc_date_time, datetime)
    def test_date_updated_on_initial_save(self, session):
        flavor = FlavorFactory.build(session=session)
        assert flavor.last_update_utc_date_time is not None
        assert isinstance(flavor.last_update_utc_date_time, datetime)
        initial_time = flavor.last_update_utc_date_time
        flavor.code = generate_uuid()
        time.sleep(2)
        session.commit()
        assert flavor.last_update_utc_date_time > initial_time
    def test_date_updated_on_second_save(self, session):
        flavor = FlavorFactory(session=session)
        assert flavor.last_update_utc_date_time is not None
        assert isinstance(flavor.last_update_utc_date_time, datetime)
        initial_time = flavor.last_update_utc_date_time
        flavor.code = generate_uuid()
        time.sleep(2)
        session.commit()
        assert flavor.last_update_utc_date_time > initial_time
    def test_model_deletion(self, session):
        flavor = FlavorFactory.create(session=session)
        session.delete(flavor)
        session.commit()
        deleted_flavor = session.query(Flavor).filter_by(flavor_id=flavor.flavor_id).first()
        assert deleted_flavor is None
    def test_data_types(self, session):
        flavor = FlavorFactory.create(session=session)
        assert isinstance(flavor.flavor_id, int)
        if db_dialect == 'postgresql':
            assert isinstance(flavor.code, UUID)
        elif db_dialect == 'mssql':
            assert isinstance(flavor.code, UNIQUEIDENTIFIER)
        else:  # This will cover SQLite, MySQL, and other databases
            assert isinstance(flavor.code, str)
        assert isinstance(flavor.last_change_code, int)
        if db_dialect == 'postgresql':
            assert isinstance(flavor.insert_user_id, UUID)
        elif db_dialect == 'mssql':
            assert isinstance(flavor.insert_user_id, UNIQUEIDENTIFIER)
        else:  # This will cover SQLite, MySQL, and other databases
            assert isinstance(flavor.insert_user_id, str)
        if db_dialect == 'postgresql':
            assert isinstance(flavor.last_update_user_id, UUID)
        elif db_dialect == 'mssql':
            assert isinstance(flavor.last_update_user_id, UNIQUEIDENTIFIER)
        else:  # This will cover SQLite, MySQL, and other databases
            assert isinstance(flavor.last_update_user_id, str)
        assert flavor.description == "" or isinstance(flavor.description, str)
        assert isinstance(flavor.display_order, int)
        assert isinstance(flavor.is_active, bool)
        assert flavor.lookup_enum_name == "" or isinstance(flavor.lookup_enum_name, str)
        assert flavor.name == "" or isinstance(flavor.name, str)
        assert isinstance(flavor.pac_id, int)
        # Check for the peek values, assuming they are UUIDs based on your model

        #description,
        #displayOrder,
        #isActive,
        #lookupEnumName,
        #name,
        #pacID
        if db_dialect == 'postgresql':
            assert isinstance(flavor.pac_code_peek, UUID)
        elif db_dialect == 'mssql':
            assert isinstance(flavor.pac_code_peek, UNIQUEIDENTIFIER)
        else:  # This will cover SQLite, MySQL, and other databases
            assert isinstance(flavor.pac_code_peek, str)

        assert isinstance(flavor.insert_utc_date_time, datetime)
        assert isinstance(flavor.last_update_utc_date_time, datetime)
    def test_unique_code_constraint(self, session):
        flavor_1 = FlavorFactory.create(session=session)
        flavor_2 = FlavorFactory.create(session=session)
        flavor_2.code = flavor_1.code
        session.add_all([flavor_1, flavor_2])
        with pytest.raises(Exception):  # adjust for the specific DB exception you'd expect
            session.commit()
    def test_fields_default(self, session):
        flavor = Flavor()
        assert flavor.code is not None
        assert flavor.last_change_code is not None
        assert flavor.insert_user_id is None
        assert flavor.last_update_user_id is None
        assert flavor.insert_utc_date_time is not None
        assert flavor.last_update_utc_date_time is not None

        #description,
        #displayOrder,
        #isActive,
        #lookupEnumName,
        #name,
        #PacID
        if db_dialect == 'postgresql':
            assert isinstance(flavor.pac_code_peek, UUID)
        elif db_dialect == 'mssql':
            assert isinstance(flavor.pac_code_peek, UNIQUEIDENTIFIER)
        else:  # This will cover SQLite, MySQL, and other databases
            assert isinstance(flavor.pac_code_peek, str)

        assert flavor.description == ""
        assert flavor.display_order == 0
        assert flavor.is_active == False
        assert flavor.lookup_enum_name == ""
        assert flavor.name == ""
        assert flavor.pac_id == 0

    def test_last_change_code_concurrency(self, session):
        flavor = FlavorFactory.create(session=session)
        original_last_change_code = flavor.last_change_code
        flavor_1 = session.query(Flavor).filter_by(flavor_id=flavor.flavor_id).first()
        flavor_1.code = generate_uuid()
        session.commit()
        flavor_2 = session.query(Flavor).filter_by(flavor_id=flavor.flavor_id).first()
        flavor_2.code = generate_uuid()
        session.commit()
        assert flavor_2.last_change_code != original_last_change_code

    #description,
    #displayOrder,
    #isActive,
    #lookupEnumName,
    #name,
    #PacID
    def test_invalid_pac_id(self, session):
        flavor = FlavorFactory.create(session=session)
        flavor.pac_id = 99999
        with pytest.raises(IntegrityError):  # adjust for the specific DB exception you'd expect
            session.commit()

