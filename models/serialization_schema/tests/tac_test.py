import pytest
from models import Tac
from models.serialization_schema import TacSchema
from models.factory import TacFactory
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base
from services.logging_config import get_logger
logger = get_logger(__name__)
DATABASE_URL = "sqlite:///:memory:"
class TestTacSchema:
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
    def tac(self, session):
        # Use the TacFactory to create and return a tac instance
        return TacFactory.create(session=session)
    # Tests
    def test_tac_serialization(self, tac:Tac, session):
        schema = TacSchema()
        result = schema.dump(tac)
        assert result['code'] == tac.code
        assert result['last_change_code'] == tac.last_change_code
        assert result['insert_user_id'] == tac.insert_user_id
        assert result['last_update_user_id'] == tac.last_update_user_id

        assert result['description'] == tac.description
        assert result['display_order'] == tac.display_order
        assert result['is_active'] == tac.is_active
        assert result['lookup_enum_name'] == tac.lookup_enum_name
        assert result['name'] == tac.name
        assert result['pac_id'] == tac.pac_id

        assert result['insert_utc_date_time'] == tac.insert_utc_date_time.isoformat()
        assert result['last_update_utc_date_time'] == tac.last_update_utc_date_time.isoformat()

        assert result['pac_code_peek'] == tac.pac_code_peek # PacID

    def test_tac_deserialization(self, tac:Tac, session):
        schema = TacSchema()
        serialized_data = schema.dump(tac)
        deserialized_data = schema.load(serialized_data)
        assert deserialized_data['code'] == tac.code
        assert deserialized_data['last_change_code'] == tac.last_change_code
        assert deserialized_data['insert_user_id'] == tac.insert_user_id
        assert deserialized_data['last_update_user_id'] == tac.last_update_user_id

        assert deserialized_data['description'] == tac.description
        assert deserialized_data['display_order'] == tac.display_order
        assert deserialized_data['is_active'] == tac.is_active
        assert deserialized_data['lookup_enum_name'] == tac.lookup_enum_name
        assert deserialized_data['name'] == tac.name
        assert deserialized_data['pac_id'] == tac.pac_id

        assert deserialized_data['insert_utc_date_time'].isoformat() == tac.insert_utc_date_time.isoformat()
        assert deserialized_data['last_update_utc_date_time'].isoformat() == tac.last_update_utc_date_time.isoformat()

        assert deserialized_data['pac_code_peek'] == tac.pac_code_peek # PacID

        new_tac = Tac(**deserialized_data)
        assert isinstance(new_tac, Tac)
        # Now compare the new_tac attributes with the tac attributes
        assert new_tac.code == tac.code
        assert new_tac.last_change_code == tac.last_change_code
        assert new_tac.insert_user_id == tac.insert_user_id
        assert new_tac.last_update_user_id == tac.last_update_user_id

        assert new_tac.description == tac.description
        assert new_tac.display_order == tac.display_order
        assert new_tac.is_active == tac.is_active
        assert new_tac.lookup_enum_name == tac.lookup_enum_name
        assert new_tac.name == tac.name
        assert new_tac.pac_id == tac.pac_id

        assert new_tac.insert_utc_date_time.isoformat() == tac.insert_utc_date_time.isoformat()
        assert new_tac.last_update_utc_date_time.isoformat() == tac.last_update_utc_date_time.isoformat()

        assert new_tac.pac_code_peek == tac.pac_code_peek #PacID

