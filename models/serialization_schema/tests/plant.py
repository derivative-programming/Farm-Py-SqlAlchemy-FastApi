import pytest
from models import Plant, PlantSchema
from models.factory import PlantFactory
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

DATABASE_URL = "sqlite:///:memory:"

class TestPlantSchema:

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
    def plant(self, session):
        # Use the PlantFactory to create and return a plant instance
        return PlantFactory.create(session=session)
    # Tests

    def test_plant_serialization(self, plant, session):
        schema = PlantSchema()
        result = schema.dump(plant)

        assert result['code'] == plant.code
        assert result['last_change_code'] == plant.last_change_code
        assert result['insert_user_id'] == plant.insert_user_id
        assert result['last_update_user_id'] == plant.last_update_user_id
        assert result['flvr_foreign_key_id'] == plant.flvr_foreign_key_id
        assert result['is_delete_allowed'] == plant.is_delete_allowed
        assert result['is_edit_allowed'] == plant.is_edit_allowed
        assert result['land_id'] == plant.land_id
        assert result['other_flavor'] == plant.other_flavor
        assert result['some_big_int_val'] == plant.some_big_int_val
        assert result['some_bit_val'] == plant.some_bit_val
        assert result['some_date_val'] == plant.some_date_val.isoformat()
        assert result['some_decimal_val'] == plant.some_decimal_val
        assert result['some_email_address'] == plant.some_email_address
        assert result['some_float_val'] == plant.some_float_val
        assert result['some_int_val'] == plant.some_int_val
        assert result['some_money_val'] == plant.some_money_val
        assert result['some_n_var_char_val'] == plant.some_n_var_char_val
        assert result['some_phone_number'] == plant.some_phone_number
        assert result['some_text_val'] == plant.some_text_val
        assert result['some_uniqueidentifier_val'] == plant.some_uniqueidentifier_val
        assert result['some_utc_date_time_val'] == plant.some_utc_date_time_val.isoformat()
        assert result['some_var_char_val'] == plant.some_var_char_val
        assert result['insert_utc_date_time'] == plant.insert_utc_date_time.isoformat()
        assert result['last_update_utc_date_time'] == plant.last_update_utc_date_time.isoformat()
        assert result['flvr_foreign_key_code_peek'] == plant.flvr_foreign_key_code_peek
        assert result['land_code_peek'] == plant.land_code_peek

    def test_plant_deserialization(self, plant, session):
        schema = PlantSchema()
        serialized_data = schema.dump(plant)
        deserialized_data = schema.load(serialized_data)

        assert isinstance(deserialized_data, Plant)
        assert deserialized_data.code == plant.code
        assert deserialized_data.last_change_code == plant.last_change_code
        assert deserialized_data.insert_user_id == plant.insert_user_id
        assert deserialized_data.last_update_user_id == plant.last_update_user_id
        assert deserialized_data.flvr_foreign_key_id == plant.flvr_foreign_key_id
        assert deserialized_data.is_delete_allowed == plant.is_delete_allowed
        assert deserialized_data.is_edit_allowed == plant.is_edit_allowed
        assert deserialized_data.land_id == plant.land_id
        assert deserialized_data.other_flavor == plant.other_flavor
        assert deserialized_data.some_big_int_val == plant.some_big_int_val
        assert deserialized_data.some_bit_val == plant.some_bit_val
        assert deserialized_data.some_date_val == plant.some_date_val
        assert deserialized_data.some_decimal_val == plant.some_decimal_val
        assert deserialized_data.some_email_address == plant.some_email_address
        assert deserialized_data.some_float_val == plant.some_float_val
        assert deserialized_data.some_int_val == plant.some_int_val
        assert deserialized_data.some_money_val == plant.some_money_val
        assert deserialized_data.some_n_var_char_val == plant.some_n_var_char_val
        assert deserialized_data.some_phone_number == plant.some_phone_number
        assert deserialized_data.some_text_val == plant.some_text_val
        assert deserialized_data.some_uniqueidentifier_val == plant.some_uniqueidentifier_val
        assert deserialized_data.some_utc_date_time_val == plant.some_utc_date_time_val
        assert deserialized_data.some_var_char_val == plant.some_var_char_val
        assert deserialized_data.insert_utc_date_time == plant.insert_utc_date_time
        assert deserialized_data.last_update_utc_date_time == plant.last_update_utc_date_time
        assert deserialized_data.flvr_foreign_key_code_peek == plant.flvr_foreign_key_code_peek
        assert deserialized_data.land_code_peek == plant.land_code_peek
