import json
import pytest
import pytz
from models import Pac
from datetime import date, datetime
from decimal import Decimal
from models.serialization_schema import PacSchema
from models.factory import PacFactory
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base
from services.logging_config import get_logger
logger = get_logger(__name__)
DATABASE_URL = "sqlite:///:memory:"
class TestPacSchema:
    # Sample data for a Pac instance
    sample_data = {
        "pac_id": 1,
        "code": "a1b2c3d4-e5f6-7a8b-9c0d-123456789012",
        "last_change_code": 0,
        "insert_user_id": "a1b2c3d4-e5f6-7a8b-9c0d-123456789012",
        "last_update_user_id": "a1b2c3d4-e5f6-7a8b-9c0d-123456789012",

        "description": "Vanilla",
        "display_order": 42,
        "is_active": False,
        "lookup_enum_name": "Vanilla",
        "name": "Vanilla",
        "insert_utc_date_time": datetime(2024, 1, 1, 12, 0, 0, tzinfo=pytz.utc).isoformat(),

        "last_update_utc_date_time": datetime(2025, 1, 1, 12, 0, 0, tzinfo=pytz.utc).isoformat()
    }
    @pytest.fixture(scope="module")
    def engine(self):
        engine = create_engine(DATABASE_URL, echo=False)
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

    def test_from_json(self, pac:Pac, session):
        pac_schema = PacSchema()
        # Convert sample data to JSON string
        json_str = json.dumps(self.sample_data)
        # Deserialize the JSON string to a dictionary
        json_data = json.loads(json_str)
        # Load the dictionary to an object
        deserialized_data = pac_schema.load(json_data)
        assert str(deserialized_data['pac_id']) == str(self.sample_data['pac_id'])
        assert str(deserialized_data['code']) == str(self.sample_data['code'])
        assert str(deserialized_data['last_change_code']) == str(self.sample_data['last_change_code'])
        assert str(deserialized_data['insert_user_id']) == str(self.sample_data['insert_user_id'])
        assert str(deserialized_data['last_update_user_id']) == str(self.sample_data['last_update_user_id'])

        assert str(deserialized_data['description']) == str(self.sample_data['description'])
        assert str(deserialized_data['display_order']) == str(self.sample_data['display_order'])
        assert str(deserialized_data['is_active']) == str(self.sample_data['is_active'])
        assert str(deserialized_data['lookup_enum_name']) == str(self.sample_data['lookup_enum_name'])
        assert str(deserialized_data['name']) == str(self.sample_data['name'])

        assert deserialized_data['insert_utc_date_time'].isoformat() == self.sample_data['insert_utc_date_time']

        assert deserialized_data['last_update_utc_date_time'].isoformat() == self.sample_data['last_update_utc_date_time']
