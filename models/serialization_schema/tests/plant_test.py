# plant_test.py

"""
    #TODO add comment
"""

import json
import pytest
import pytz
import logging
from models import Plant
from datetime import datetime
from decimal import Decimal
from models.serialization_schema import PlantSchema
from models.factory import PlantFactory
from services.logging_config import get_logger
logger = get_logger(__name__)


@pytest.fixture(scope="function")
def plant(session):
    """
    #TODO add comment
    """
    # Use the PlantFactory to create and return a plant instance
    return PlantFactory.create(session=session)


class TestPlantSchema:
    """
    #TODO add comment
    """

    # Sample data for a Plant instance
    sample_data = {
        "plant_id": 1,
        "code": "a1b2c3d4-e5f6-7a8b-9c0d-123456789012",
        "last_change_code": 0,
        "insert_user_id": "a1b2c3d4-e5f6-7a8b-9c0d-123456789012",
        "last_update_user_id": "a1b2c3d4-e5f6-7a8b-9c0d-123456789012",
# endset  # noqa: E122
        "flvr_foreign_key_id": 1,
        "is_delete_allowed": False,
        "is_edit_allowed": True,
        "land_id": 2,
        "other_flavor": "Vanilla",
        "some_big_int_val": 1000000000,
        "some_bit_val": True,
        "some_date_val": "2022-01-01",
        "some_decimal_val": str(Decimal('1234.5678')),
        "some_email_address": "test@email.com",
        "some_float_val": 123.456,
        "some_int_val": 42,
        "some_money_val": str(Decimal('5678.9101')),
        "some_n_var_char_val": "Hello",
        "some_phone_number": "123-456-7890",
        "some_text_val": "Lorem ipsum",
        "some_uniqueidentifier_val": "a1b2c3d4-e5f6-7a8b-9c0d-123456789012",
        "some_utc_date_time_val": datetime(
            2023, 1, 1, 12, 0, 0, tzinfo=pytz.utc
        ).isoformat(),
        "some_var_char_val": "World",
        "insert_utc_date_time": datetime(
            2024, 1, 1, 12, 0, 0, tzinfo=pytz.utc
        ).isoformat(),
        "last_update_utc_date_time": datetime(
            2025, 1, 1, 12, 0, 0, tzinfo=pytz.utc
        ).isoformat(),
# endset  # noqa: E122
        "flvr_foreign_key_code_peek": "a1b2c3d4-e5f6-7a8b-9c0d-123456789012",  # FlvrForeignKeyID
        "land_code_peek": "a1b2c3d4-e5f6-7a8b-9c0d-123456789012",  # LandID
# endset  # noqa: E122
    }

    def test_plant_serialization(self, plant: Plant, session):
        schema = PlantSchema()
        result = schema.dump(plant)

        assert result['code'] == plant.code
        assert result['last_change_code'] == (
            plant.last_change_code)
        assert result['insert_user_id'] == (
            plant.insert_user_id)
        assert result['last_update_user_id'] == (
            plant.last_update_user_id)

# endset
        assert result['flvr_foreign_key_id'] == (
            plant.flvr_foreign_key_id)
        assert result['is_delete_allowed'] == (
            plant.is_delete_allowed)
        assert result['is_edit_allowed'] == (
            plant.is_edit_allowed)
        assert result['land_id'] == (
            plant.land_id)
        assert result['other_flavor'] == (
            plant.other_flavor)
        assert result['some_big_int_val'] == (
            plant.some_big_int_val)
        assert result['some_bit_val'] == (
            plant.some_bit_val)
        assert result['some_date_val'] == (
            plant.some_date_val.strftime('%Y-%m-%d'))
        assert result['some_decimal_val'] == (
            str(plant.some_decimal_val))
        assert result['some_email_address'] == (
            plant.some_email_address)
        assert result['some_float_val'] == (
            plant.some_float_val)
        assert result['some_int_val'] == (
            plant.some_int_val)
        assert result['some_money_val'] == (
            str(plant.some_money_val))
        assert result['some_n_var_char_val'] == (
            plant.some_n_var_char_val)
        assert result['some_phone_number'] == (
            plant.some_phone_number)
        assert result['some_text_val'] == (
            plant.some_text_val)
        assert result['some_uniqueidentifier_val'] == (
            plant.some_uniqueidentifier_val)
        assert result['some_utc_date_time_val'] == (
            plant.some_utc_date_time_val.isoformat())
        assert result['some_var_char_val'] == (
            plant.some_var_char_val)
# endset
        assert result['insert_utc_date_time'] == (
            plant.insert_utc_date_time.isoformat())
        assert result['last_update_utc_date_time'] == (
            plant.last_update_utc_date_time.isoformat())
# endset
        assert result['flvr_foreign_key_code_peek'] == (  # FlvrForeignKeyID
            plant.flvr_foreign_key_code_peek)
        assert result['land_code_peek'] == (  # LandID
            plant.land_code_peek)
# endset

    def test_plant_deserialization(self, plant: Plant, session):
        schema = PlantSchema()
        serialized_data = schema.dump(plant)
        deserialized_data = schema.load(serialized_data)

        assert deserialized_data['code'] == plant.code
        assert deserialized_data['last_change_code'] == (
            plant.last_change_code)
        assert deserialized_data['insert_user_id'] == (
            plant.insert_user_id)
        assert deserialized_data['last_update_user_id'] == (
            plant.last_update_user_id)
# endset

        assert deserialized_data['is_delete_allowed'] == (
            plant.is_delete_allowed)
        assert deserialized_data['is_edit_allowed'] == (
            plant.is_edit_allowed)
        assert deserialized_data['land_id'] == (
            plant.land_id)
        assert deserialized_data['other_flavor'] == (
            plant.other_flavor)
        assert deserialized_data['some_big_int_val'] == (
            plant.some_big_int_val)
        assert deserialized_data['some_bit_val'] == (
            plant.some_bit_val)
        assert deserialized_data['some_date_val'].strftime('%Y-%m-%d') == (
            plant.some_date_val.strftime('%Y-%m-%d'))
        assert deserialized_data['some_decimal_val'] == (
            plant.some_decimal_val)
        assert deserialized_data['some_email_address'] == (
            plant.some_email_address)
        assert deserialized_data['some_float_val'] == (
            plant.some_float_val)
        assert deserialized_data['some_int_val'] == (
            plant.some_int_val)
        assert deserialized_data['some_money_val'] == (
            plant.some_money_val)
        assert deserialized_data['some_n_var_char_val'] == (
            plant.some_n_var_char_val)
        assert deserialized_data['some_phone_number'] == (
            plant.some_phone_number)
        assert deserialized_data['some_text_val'] == (
            plant.some_text_val)
        assert deserialized_data['some_uniqueidentifier_val'] == (
            plant.some_uniqueidentifier_val)
        assert deserialized_data['some_utc_date_time_val'].isoformat() == (
            plant.some_utc_date_time_val.isoformat())
        assert deserialized_data['some_var_char_val'] == (
            plant.some_var_char_val)
        assert deserialized_data['flvr_foreign_key_id'] == (
            plant.flvr_foreign_key_id)
# endset
        assert deserialized_data['insert_utc_date_time'].isoformat() == (
            plant.insert_utc_date_time.isoformat())
        assert deserialized_data['last_update_utc_date_time'].isoformat() == (
            plant.last_update_utc_date_time.isoformat())
# endset
        assert deserialized_data['flvr_foreign_key_code_peek'] == (  # FlvrForeignKeyID
            plant.flvr_foreign_key_code_peek)
        assert deserialized_data['land_code_peek'] == (  # LandID
            plant.land_code_peek)
# endset

        new_plant = Plant(**deserialized_data)

        assert isinstance(new_plant, Plant)

        # Now compare the new_plant attributes with the plant attributes
        assert new_plant.code == plant.code
        assert new_plant.last_change_code == plant.last_change_code
        assert new_plant.insert_user_id == plant.insert_user_id
        assert new_plant.last_update_user_id == plant.last_update_user_id
# endset

        assert new_plant.is_delete_allowed == (
            plant.is_delete_allowed)
        assert new_plant.is_edit_allowed == (
            plant.is_edit_allowed)
        assert new_plant.land_id == (
            plant.land_id)
        assert new_plant.other_flavor == (
            plant.other_flavor)
        assert new_plant.some_big_int_val == (
            plant.some_big_int_val)
        assert new_plant.some_bit_val == (
            plant.some_bit_val)
        assert new_plant.some_date_val.strftime('%Y-%m-%d') == (
            plant.some_date_val.strftime('%Y-%m-%d'))
        assert new_plant.some_decimal_val == (
            plant.some_decimal_val)
        assert new_plant.some_email_address == (
            plant.some_email_address)
        assert new_plant.some_float_val == (
            plant.some_float_val)
        assert new_plant.some_int_val == (
            plant.some_int_val)
        assert new_plant.some_money_val == (
            plant.some_money_val)
        assert new_plant.some_n_var_char_val == (
            plant.some_n_var_char_val)
        assert new_plant.some_phone_number == (
            plant.some_phone_number)
        assert new_plant.some_text_val == (
            plant.some_text_val)
        assert new_plant.some_uniqueidentifier_val == (
            plant.some_uniqueidentifier_val)
        assert new_plant.some_utc_date_time_val.isoformat() == (
            plant.some_utc_date_time_val.isoformat())
        assert new_plant.some_var_char_val == (
            plant.some_var_char_val)
        assert new_plant.flvr_foreign_key_id == (
            plant.flvr_foreign_key_id)
# endset

        assert new_plant.insert_utc_date_time.isoformat() == (
            plant.insert_utc_date_time.isoformat())
        assert new_plant.last_update_utc_date_time.isoformat() == (
            plant.last_update_utc_date_time.isoformat())
# endset

        assert new_plant.flvr_foreign_key_code_peek == (  # FlvrForeignKeyID
            plant.flvr_foreign_key_code_peek)
        assert new_plant.land_code_peek == (  # LandID
            plant.land_code_peek)
# endset

    def test_from_json(self, plant: Plant, session):
        plant_schema = PlantSchema()

        # Convert sample data to JSON string
        json_str = json.dumps(self.sample_data)

        # Deserialize the JSON string to a dictionary
        json_data = json.loads(json_str)

        # Load the dictionary to an object
        deserialized_data = plant_schema.load(json_data)

        assert str(deserialized_data['plant_id']) == (
            str(self.sample_data['plant_id']))
        assert str(deserialized_data['code']) == (
            str(self.sample_data['code']))
        assert str(deserialized_data['last_change_code']) == (
            str(self.sample_data['last_change_code']))
        assert str(deserialized_data['insert_user_id']) == (
            str(self.sample_data['insert_user_id']))
        assert str(deserialized_data['last_update_user_id']) == (
            str(self.sample_data['last_update_user_id']))
# endset
        assert str(deserialized_data['flvr_foreign_key_id']) == (
            str(self.sample_data['flvr_foreign_key_id']))
        assert str(deserialized_data['is_delete_allowed']) == (
            str(self.sample_data['is_delete_allowed']))
        assert str(deserialized_data['is_edit_allowed']) == (
            str(self.sample_data['is_edit_allowed']))
        assert str(deserialized_data['land_id']) == (
            str(self.sample_data['land_id']))
        assert str(deserialized_data['other_flavor']) == (
            str(self.sample_data['other_flavor']))
        assert str(deserialized_data['some_big_int_val']) == (
            str(self.sample_data['some_big_int_val']))
        assert str(deserialized_data['some_bit_val']) == (
            str(self.sample_data['some_bit_val']))
        assert str(deserialized_data['some_date_val']) == (
            str(self.sample_data['some_date_val']))
        assert str(deserialized_data['some_decimal_val']) == (
            str(self.sample_data['some_decimal_val']))
        assert str(deserialized_data['some_email_address']) == (
            str(self.sample_data['some_email_address']))
        assert str(deserialized_data['some_float_val']) == (
            str(self.sample_data['some_float_val']))
        assert str(deserialized_data['some_int_val']) == (
            str(self.sample_data['some_int_val']))
        assert str(deserialized_data['some_money_val']) == (
            str(self.sample_data['some_money_val']))
        assert str(deserialized_data['some_n_var_char_val']) == (
            str(self.sample_data['some_n_var_char_val']))
        assert str(deserialized_data['some_phone_number']) == (
            str(self.sample_data['some_phone_number']))
        assert str(deserialized_data['some_text_val']) == (
            str(self.sample_data['some_text_val']))
        assert str(deserialized_data['some_uniqueidentifier_val']) == (
            str(self.sample_data['some_uniqueidentifier_val']))
        assert deserialized_data['some_utc_date_time_val'].isoformat() == (
            self.sample_data['some_utc_date_time_val'])
        assert str(deserialized_data['some_var_char_val']) == (
            str(self.sample_data['some_var_char_val']))
# endset
        assert deserialized_data['insert_utc_date_time'].isoformat() == (
            self.sample_data['insert_utc_date_time'])
        assert str(deserialized_data['flvr_foreign_key_code_peek']) == (  # FlvrForeignKeyID
            str(self.sample_data['flvr_foreign_key_code_peek']))
        assert str(deserialized_data['land_code_peek']) == (  # LandID
            str(self.sample_data['land_code_peek']))
# endset
        assert deserialized_data['last_update_utc_date_time'].isoformat() == (
            self.sample_data['last_update_utc_date_time'])

        new_plant = Plant(**deserialized_data)

        assert isinstance(new_plant, Plant)

    def test_to_json(self, plant: Plant, session):
        # Convert the Plant instance to JSON using the schema
        plant_schema = PlantSchema()
        plant_dict = plant_schema.dump(plant)

        # Convert the plant_dict to JSON string
        plant_json = json.dumps(plant_dict)

        # Convert the JSON strings back to dictionaries
        plant_dict_from_json = json.loads(plant_json)
        # sample_dict_from_json = json.loads(self.sample_data)

        logging.info("plant_dict_from_json.keys() %s", plant_dict_from_json.keys())

        logging.info("self.sample_data.keys() %s", self.sample_data.keys())

        # Verify the keys in both dictionaries match
        assert set(plant_dict_from_json.keys()) == (
            set(self.sample_data.keys())), (
            f"Expected keys: {set(self.sample_data.keys())}, Got: {set(plant_dict_from_json.keys())}"
        )

        assert plant_dict_from_json['code'] == plant.code, (
            "failed on code"
        )
        assert plant_dict_from_json['last_change_code'] == (
            plant.last_change_code), (
            "failed on last_change_code"
        )
        assert plant_dict_from_json['insert_user_id'] == (
            plant.insert_user_id), (
            "failed on insert_user_id"
        )
        assert plant_dict_from_json['last_update_user_id'] == (
            plant.last_update_user_id), (
            "failed on last_update_user_id"
        )
# endset

        assert plant_dict_from_json['is_delete_allowed'] == (
            plant.is_delete_allowed), (
            "failed on is_delete_allowed"
        )
        assert plant_dict_from_json['is_edit_allowed'] == (
            plant.is_edit_allowed), (
            "failed on is_edit_allowed"
        )
        assert plant_dict_from_json['land_id'] == (
            plant.land_id), (
            "failed on land_id"
        )
        assert plant_dict_from_json['other_flavor'] == (
            plant.other_flavor), (
            "failed on other_flavor"
        )
        assert plant_dict_from_json['some_big_int_val'] == (
            plant.some_big_int_val), (
            "failed on some_big_int_val"
        )
        assert plant_dict_from_json['some_bit_val'] == (
            plant.some_bit_val), (
            "failed on some_bit_val"
        )
        assert plant_dict_from_json['some_date_val'] == (
            plant.some_date_val.strftime('%Y-%m-%d')), (
            "failed on some_date_val"
        )
        assert plant_dict_from_json['some_decimal_val'] == str(
            plant.some_decimal_val), (
            "failed on some_decimal_val"
        )
        assert plant_dict_from_json['some_email_address'] == (
            plant.some_email_address), (
            "failed on some_email_address"
        )
        assert plant_dict_from_json['some_float_val'] == (
            plant.some_float_val), (
            "failed on some_float_val"
        )
        assert plant_dict_from_json['some_int_val'] == (
            plant.some_int_val), (
            "failed on some_int_val"
        )
        assert plant_dict_from_json['some_money_val'] == str(
            plant.some_money_val), (
            "failed on some_money_val"
        )
        assert plant_dict_from_json['some_n_var_char_val'] == (
            plant.some_n_var_char_val), (
            "failed on some_n_var_char_val"
        )
        assert plant_dict_from_json['some_phone_number'] == (
            plant.some_phone_number), (
            "failed on some_phone_number"
        )
        assert plant_dict_from_json['some_text_val'] == (
            plant.some_text_val), (
            "failed on some_text_val"
        )
        assert plant_dict_from_json['some_uniqueidentifier_val'] == (
            plant.some_uniqueidentifier_val), (
            "failed on some_uniqueidentifier_val"
        )
        assert plant_dict_from_json['some_utc_date_time_val'] == (
            plant.some_utc_date_time_val.isoformat()), (
            "failed on some_utc_date_time_val"
        )
        assert plant_dict_from_json['some_var_char_val'] == (
            plant.some_var_char_val), (
            "failed on some_var_char_val"
        )
        assert plant_dict_from_json['flvr_foreign_key_id'] == (
            plant.flvr_foreign_key_id), (
            "failed on flvr_foreign_key_id"
        )
# endset
        assert plant_dict_from_json['insert_utc_date_time'] == (
            plant.insert_utc_date_time.isoformat()), (
            "failed on insert_utc_date_time"
        )
        assert plant_dict_from_json['last_update_utc_date_time'] == (
            plant.last_update_utc_date_time.isoformat()), (
            "failed on last_update_utc_date_time"
        )
# endset
        assert plant_dict_from_json['flvr_foreign_key_code_peek'] == (  # FlvrForeignKeyID
            plant.flvr_foreign_key_code_peek), (
            "failed on flvr_foreign_key_code_peek"
        )
        assert plant_dict_from_json['land_code_peek'] == (  # LandID
            plant.land_code_peek), (
            "failed on land_code_peek"
        )
# endset
