import json
import pytest
import pytz
from models import Flavor
from datetime import date, datetime
from decimal import Decimal
from models.serialization_schema import FlavorSchema
from models.factory import FlavorFactory
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base
from services.logging_config import get_logger
logger = get_logger(__name__)
DATABASE_URL = "sqlite:///:memory:"
class TestFlavorSchema:
    # Sample data for a Flavor instance
    sample_data = {
        "flavor_id": 1,
        "code": "a1b2c3d4-e5f6-7a8b-9c0d-123456789012",
        "last_change_code": 0,
        "insert_user_id": "a1b2c3d4-e5f6-7a8b-9c0d-123456789012",
        "last_update_user_id": "a1b2c3d4-e5f6-7a8b-9c0d-123456789012",

        "description": "Vanilla",
        "display_order": 42,
        "is_active": False,
        "lookup_enum_name": "Vanilla",
        "name": "Vanilla",
        "pac_id": 2,
        "insert_utc_date_time": datetime(2024, 1, 1, 12, 0, 0, tzinfo=pytz.utc).isoformat(),

        "pac_code_peek": "a1b2c3d4-e5f6-7a8b-9c0d-123456789012",# PacID

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
    def flavor(self, session):
        # Use the FlavorFactory to create and return a flavor instance
        return FlavorFactory.create(session=session)
    # Tests
    def test_flavor_serialization(self, flavor:Flavor, session):
        schema = FlavorSchema()
        result = schema.dump(flavor)
        assert result['code'] == flavor.code
        assert result['last_change_code'] == flavor.last_change_code
        assert result['insert_user_id'] == flavor.insert_user_id
        assert result['last_update_user_id'] == flavor.last_update_user_id

        assert result['description'] == flavor.description
        assert result['display_order'] == flavor.display_order
        assert result['is_active'] == flavor.is_active
        assert result['lookup_enum_name'] == flavor.lookup_enum_name
        assert result['name'] == flavor.name
        assert result['pac_id'] == flavor.pac_id

        assert result['insert_utc_date_time'] == flavor.insert_utc_date_time.isoformat()
        assert result['last_update_utc_date_time'] == flavor.last_update_utc_date_time.isoformat()

        assert result['pac_code_peek'] == flavor.pac_code_peek # PacID

    def test_flavor_deserialization(self, flavor:Flavor, session):
        schema = FlavorSchema()
        serialized_data = schema.dump(flavor)
        deserialized_data = schema.load(serialized_data)
        assert deserialized_data['code'] == flavor.code
        assert deserialized_data['last_change_code'] == flavor.last_change_code
        assert deserialized_data['insert_user_id'] == flavor.insert_user_id
        assert deserialized_data['last_update_user_id'] == flavor.last_update_user_id

        assert deserialized_data['description'] == flavor.description
        assert deserialized_data['display_order'] == flavor.display_order
        assert deserialized_data['is_active'] == flavor.is_active
        assert deserialized_data['lookup_enum_name'] == flavor.lookup_enum_name
        assert deserialized_data['name'] == flavor.name
        assert deserialized_data['pac_id'] == flavor.pac_id

        assert deserialized_data['insert_utc_date_time'].isoformat() == flavor.insert_utc_date_time.isoformat()
        assert deserialized_data['last_update_utc_date_time'].isoformat() == flavor.last_update_utc_date_time.isoformat()

        assert deserialized_data['pac_code_peek'] == flavor.pac_code_peek # PacID

        new_flavor = Flavor(**deserialized_data)
        assert isinstance(new_flavor, Flavor)
        # Now compare the new_flavor attributes with the flavor attributes
        assert new_flavor.code == flavor.code
        assert new_flavor.last_change_code == flavor.last_change_code
        assert new_flavor.insert_user_id == flavor.insert_user_id
        assert new_flavor.last_update_user_id == flavor.last_update_user_id

        assert new_flavor.description == flavor.description
        assert new_flavor.display_order == flavor.display_order
        assert new_flavor.is_active == flavor.is_active
        assert new_flavor.lookup_enum_name == flavor.lookup_enum_name
        assert new_flavor.name == flavor.name
        assert new_flavor.pac_id == flavor.pac_id

        assert new_flavor.insert_utc_date_time.isoformat() == flavor.insert_utc_date_time.isoformat()
        assert new_flavor.last_update_utc_date_time.isoformat() == flavor.last_update_utc_date_time.isoformat()

        assert new_flavor.pac_code_peek == flavor.pac_code_peek #PacID

    def test_from_json(self, flavor:Flavor, session):
        flavor_schema = FlavorSchema()
        # Convert sample data to JSON string
        json_str = json.dumps(self.sample_data)
        # Deserialize the JSON string to a dictionary
        json_data = json.loads(json_str)
        # Load the dictionary to an object
        deserialized_data = flavor_schema.load(json_data)
        assert str(deserialized_data['flavor_id']) == str(self.sample_data['flavor_id'])
        assert str(deserialized_data['code']) == str(self.sample_data['code'])
        assert str(deserialized_data['last_change_code']) == str(self.sample_data['last_change_code'])
        assert str(deserialized_data['insert_user_id']) == str(self.sample_data['insert_user_id'])
        assert str(deserialized_data['last_update_user_id']) == str(self.sample_data['last_update_user_id'])

        assert str(deserialized_data['description']) == str(self.sample_data['description'])
        assert str(deserialized_data['display_order']) == str(self.sample_data['display_order'])
        assert str(deserialized_data['is_active']) == str(self.sample_data['is_active'])
        assert str(deserialized_data['lookup_enum_name']) == str(self.sample_data['lookup_enum_name'])
        assert str(deserialized_data['name']) == str(self.sample_data['name'])
        assert str(deserialized_data['pac_id']) == str(self.sample_data['pac_id'])

        assert deserialized_data['insert_utc_date_time'].isoformat() == self.sample_data['insert_utc_date_time']
        assert str(deserialized_data['pac_code_peek']) == str(self.sample_data['pac_code_peek']) #PacID

        assert deserialized_data['last_update_utc_date_time'].isoformat() == self.sample_data['last_update_utc_date_time']
        new_flavor = Flavor(**deserialized_data)
        assert isinstance(new_flavor, Flavor)
    def test_to_json(self, flavor:Flavor, session):
            # Convert the Flavor instance to JSON using the schema
            flavor_schema = FlavorSchema()
            flavor_dict = flavor_schema.dump(flavor)
            # Convert the flavor_dict to JSON string
            flavor_json = json.dumps(flavor_dict)
            # Convert the JSON strings back to dictionaries
            flavor_dict_from_json = json.loads(flavor_json)
            # sample_dict_from_json = json.loads(self.sample_data)
            # Verify the keys in both dictionaries match
            assert set(flavor_dict_from_json.keys()) == set(self.sample_data.keys()), f"Expected keys: {set(self.sample_data.keys())}, Got: {set(flavor_dict_from_json.keys())}"
            assert flavor_dict_from_json['code'] == flavor.code
            assert flavor_dict_from_json['last_change_code'] == flavor.last_change_code
            assert flavor_dict_from_json['insert_user_id'] == flavor.insert_user_id
            assert flavor_dict_from_json['last_update_user_id'] == flavor.last_update_user_id

            assert flavor_dict_from_json['description'] == flavor.description
            assert flavor_dict_from_json['display_order'] == flavor.display_order
            assert flavor_dict_from_json['is_active'] == flavor.is_active
            assert flavor_dict_from_json['lookup_enum_name'] == flavor.lookup_enum_name
            assert flavor_dict_from_json['name'] == flavor.name
            assert flavor_dict_from_json['pac_id'] == flavor.pac_id

            assert flavor_dict_from_json['insert_utc_date_time'] == flavor.insert_utc_date_time.isoformat()
            assert flavor_dict_from_json['last_update_utc_date_time'] == flavor.last_update_utc_date_time.isoformat()

            assert flavor_dict_from_json['pac_code_peek'] == flavor.pac_code_peek # PacID

