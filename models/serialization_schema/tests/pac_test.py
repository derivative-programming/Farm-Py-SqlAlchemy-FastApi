import pytest
from models import Pac
from models.serialization_schema import PacSchema
from models.factory import PacFactory
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base
from services.logging_config import get_logger
logger = get_logger(__name__)
DATABASE_URL = "sqlite:///:memory:"
class TestPacSchema:
    @pytest.fixture(scope="module")
    def engine(self):
        engine = create_engine(DATABASE_URL, echo=True)
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
    @pytest.fixture
    def pac(self, session):
        # Use the PacFactory to create and return a pac instance
        return PacFactory.create(session=session)
    # Tests
    def test_pac_serialization(self, pac:Pac, session):
        schema = PacSchema()
        result = schema.dump(pac)
        assert result['code'] == pac.code
        assert result['last_change_code'] == pac.last_change_code
        assert result['insert_user_id'] == pac.insert_user_id
        assert result['last_update_user_id'] == pac.last_update_user_id

        assert result['description'] == pac.description
        assert result['display_order'] == pac.display_order
        assert result['is_active'] == pac.is_active
        assert result['lookup_enum_name'] == pac.lookup_enum_name
        assert result['name'] == pac.name

        assert result['insert_utc_date_time'] == pac.insert_utc_date_time.isoformat()
        assert result['last_update_utc_date_time'] == pac.last_update_utc_date_time.isoformat()

    def test_pac_deserialization(self, pac:Pac, session):
        schema = PacSchema()
        serialized_data = schema.dump(pac)
        deserialized_data = schema.load(serialized_data)
        assert deserialized_data['code'] == pac.code
        assert deserialized_data['last_change_code'] == pac.last_change_code
        assert deserialized_data['insert_user_id'] == pac.insert_user_id
        assert deserialized_data['last_update_user_id'] == pac.last_update_user_id

        assert deserialized_data['description'] == pac.description
        assert deserialized_data['display_order'] == pac.display_order
        assert deserialized_data['is_active'] == pac.is_active
        assert deserialized_data['lookup_enum_name'] == pac.lookup_enum_name
        assert deserialized_data['name'] == pac.name

        assert deserialized_data['insert_utc_date_time'].isoformat() == pac.insert_utc_date_time.isoformat()
        assert deserialized_data['last_update_utc_date_time'].isoformat() == pac.last_update_utc_date_time.isoformat()

        new_pac = Pac(**deserialized_data)
        assert isinstance(new_pac, Pac)
        # Now compare the new_pac attributes with the pac attributes
        assert new_pac.code == pac.code
        assert new_pac.last_change_code == pac.last_change_code
        assert new_pac.insert_user_id == pac.insert_user_id
        assert new_pac.last_update_user_id == pac.last_update_user_id

        assert new_pac.description == pac.description
        assert new_pac.display_order == pac.display_order
        assert new_pac.is_active == pac.is_active
        assert new_pac.lookup_enum_name == pac.lookup_enum_name
        assert new_pac.name == pac.name

        assert new_pac.insert_utc_date_time.isoformat() == pac.insert_utc_date_time.isoformat()
        assert new_pac.last_update_utc_date_time.isoformat() == pac.last_update_utc_date_time.isoformat()

