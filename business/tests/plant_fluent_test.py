# business/tests/plant_fluent_test.py
"""
Unit tests for the PlantFluentBusObj class.
"""
import math
from datetime import date, datetime
from decimal import Decimal
from uuid import uuid4

import pytest

from business.plant_fluent import PlantFluentBusObj
from helpers.session_context import SessionContext


class MockPlantBaseBusObj:
    """
    A mock base class for the PlantFluentBusObj class.
    """
    def __init__(self):
        self.is_delete_allowed = None
        self.is_edit_allowed = None
        self.other_flavor = None
        self.some_big_int_val = None
        self.some_bit_val = None
        self.some_date_val = None
        self.some_decimal_val = None
        self.some_email_address = None
        self.some_float_val = None
        self.some_int_val = None
        self.some_money_val = None
        self.some_n_var_char_val = None
        self.some_phone_number = None
        self.some_text_val = None
        self.some_uniqueidentifier_val = None
        self.some_utc_date_time_val = None
        self.some_var_char_val = None
        self.flvr_foreign_key_id = None
        self.land_id = None


class TestPlantFluentBusObj:
    """
    Unit tests for the PlantFluentBusObj class.
    """
    @pytest.fixture
    def plant(self, session):
        """
        Return a PlantFluentBusObj object.
        """
        session_context = SessionContext(dict(), session=session)
        return PlantFluentBusObj(session_context)

    def test_set_prop_is_delete_allowed(self, plant):
        """
        Test setting the is_delete_allowed property.
        """
        result = plant.set_prop_is_delete_allowed(True)
        assert plant.is_delete_allowed is True
        assert result is plant

    def test_set_prop_is_edit_allowed(self, plant):
        """
        Test setting the is_edit_allowed property.
        """
        result = plant.set_prop_is_edit_allowed(True)
        assert plant.is_edit_allowed is True
        assert result is plant

    def test_set_prop_other_flavor(self, plant):
        """
        Test setting the other_flavor property.
        """
        result = plant.set_prop_other_flavor("Vanilla")
        assert plant.other_flavor == "Vanilla"
        assert result is plant

    def test_set_prop_some_big_int_val(self, plant):
        """
        Test setting the some_big_int_val property.
        """
        result = plant.set_prop_some_big_int_val(123456789)
        assert plant.some_big_int_val == 123456789
        assert result is plant

    def test_set_prop_some_bit_val(self, plant):
        """
        Test setting the some_bit_val property.
        """
        result = plant.set_prop_some_bit_val(True)
        assert plant.some_bit_val is True
        assert result is plant

    def test_set_prop_some_date_val(self, plant):
        """
        Test setting the some_date_val property.
        """
        test_date = date(2023, 1, 1)
        result = plant.set_prop_some_date_val(test_date)
        assert plant.some_date_val == test_date
        assert result is plant

    def test_set_prop_some_decimal_val(self, plant):
        """
        Test setting the some_decimal_val property.
        """
        result = plant.set_prop_some_decimal_val(Decimal('99.99'))
        assert plant.some_decimal_val == Decimal('99.99')
        assert result is plant

    def test_set_prop_some_email_address(self, plant):
        """
        Test setting the some_email_address property.
        """
        result = plant.set_prop_some_email_address("test@example.com")
        assert plant.some_email_address == "test@example.com"
        assert result is plant

    def test_set_prop_some_float_val(self, plant):
        """
        Test setting the some_float_val property.
        """
        result = plant.set_prop_some_float_val(3.14)
        assert math.isclose(plant.some_float_val, 3.14)
        assert result is plant

    def test_set_prop_some_int_val(self, plant):
        """
        Test setting the some_int_val property.
        """
        result = plant.set_prop_some_int_val(42)
        assert plant.some_int_val == 42
        assert result is plant

    def test_set_prop_some_money_val(self, plant):
        """
        Test setting the some_money_val property.
        """
        result = plant.set_prop_some_money_val(Decimal('100.00'))
        assert plant.some_money_val == Decimal('100.00')
        assert result is plant

    def test_set_prop_some_n_var_char_val(self, plant):
        """
        Test setting the some_n_var_char_val property.
        """
        result = plant.set_prop_some_n_var_char_val("nvarchar")
        assert plant.some_n_var_char_val == "nvarchar"
        assert result is plant

    def test_set_prop_some_phone_number(self, plant):
        """
        Test setting the some_phone_number property.
        """
        result = plant.set_prop_some_phone_number("123-456-7890")
        assert plant.some_phone_number == "123-456-7890"
        assert result is plant

    def test_set_prop_some_text_val(self, plant):
        """
        Test setting the some_text_val property.
        """
        result = plant.set_prop_some_text_val("Some text")
        assert plant.some_text_val == "Some text"
        assert result is plant

    def test_set_prop_some_uniqueidentifier_val(self, plant):
        """
        Test setting the some_uniqueidentifier_val property.
        """
        test_uuid = uuid4()
        result = plant.set_prop_some_uniqueidentifier_val(test_uuid)
        assert plant.some_uniqueidentifier_val == test_uuid
        assert result is plant

    def test_set_prop_some_utc_date_time_val(self, plant):
        """
        Test setting the some_utc_date_time_val property.
        """
        test_datetime = datetime(2023, 1, 1, 12, 0, 0)
        result = plant.set_prop_some_utc_date_time_val(test_datetime)
        assert plant.some_utc_date_time_val == test_datetime
        assert result is plant

    def test_set_prop_some_var_char_val(self, plant):
        """
        Test setting the some_var_char_val property.
        """
        result = plant.set_prop_some_var_char_val("varchar")
        assert plant.some_var_char_val == "varchar"
        assert result is plant

    def test_set_prop_flvr_foreign_key_id(self, plant):
        """
        Test setting the flvr_foreign_key_id property.
        """
        result = plant.set_prop_flvr_foreign_key_id(1)
        assert plant.flvr_foreign_key_id == 1
        assert result is plant

    def test_set_prop_land_id(self, plant):
        """
        Test setting the land_id property.
        """
        result = plant.set_prop_land_id(1)
        assert plant.land_id == 1
        assert result is plant
