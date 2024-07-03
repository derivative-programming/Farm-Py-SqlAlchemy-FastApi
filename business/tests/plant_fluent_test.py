# business/tests/plant_fluent_test.py
# pylint: disable=unused-import
"""
Unit tests for the
PlantFluentBusObj class.
"""
import math  # noqa: F401
from datetime import date, datetime, timezone  # noqa: F401
from decimal import Decimal  # noqa: F401
from uuid import uuid4  # noqa: F401

import pytest

from business.plant_fluent import (
    PlantFluentBusObj)
from helpers.session_context import SessionContext


class MockPlantBaseBusObj:
    """
    A mock base class for the
    PlantFluentBusObj class.
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
    Unit tests for the
    PlantFluentBusObj class.
    """
    @pytest.fixture
    def new_fluent_bus_obj(self, session):
        """
        Return a PlantFluentBusObj
        object.
        """
        session_context = SessionContext(dict(), session=session)
        return PlantFluentBusObj(
            session_context)
    # FlvrForeignKeyID
    # isDeleteAllowed

    def test_set_prop_is_delete_allowed(self, new_fluent_bus_obj):
        """
        Test setting the is_delete_allowed property.
        """
        result = new_fluent_bus_obj.set_prop_is_delete_allowed(True)
        assert new_fluent_bus_obj.is_delete_allowed is True
        assert result is new_fluent_bus_obj
    # isEditAllowed

    def test_set_prop_is_edit_allowed(self, new_fluent_bus_obj):
        """
        Test setting the is_edit_allowed property.
        """
        result = new_fluent_bus_obj.set_prop_is_edit_allowed(True)
        assert new_fluent_bus_obj.is_edit_allowed is True
        assert result is new_fluent_bus_obj
    # otherFlavor

    def test_set_prop_other_flavor(self, new_fluent_bus_obj):
        """
        Test setting the other_flavor property.
        """
        result = new_fluent_bus_obj.set_prop_other_flavor(
            "Vanilla")
        assert new_fluent_bus_obj.other_flavor == \
            "Vanilla"
        assert result is new_fluent_bus_obj
    # someBigIntVal

    def test_set_prop_some_big_int_val(self, new_fluent_bus_obj):
        """
        Test setting the some_big_int_val property.
        """
        result = new_fluent_bus_obj.set_prop_some_big_int_val(
            123456789)
        assert new_fluent_bus_obj.some_big_int_val == \
            123456789
        assert result is new_fluent_bus_obj
    # someBitVal

    def test_set_prop_some_bit_val(self, new_fluent_bus_obj):
        """
        Test setting the some_bit_val property.
        """
        result = new_fluent_bus_obj.set_prop_some_bit_val(True)
        assert new_fluent_bus_obj.some_bit_val is True
        assert result is new_fluent_bus_obj
    # someDateVal

    def test_set_prop_some_date_val(self, new_fluent_bus_obj):
        """
        Test setting the some_date_val property.
        """
        test_date = date(2023, 1, 1)
        result = new_fluent_bus_obj.set_prop_some_date_val(test_date)
        assert new_fluent_bus_obj.some_date_val == \
            test_date
        assert result is new_fluent_bus_obj
    # someDecimalVal

    def test_set_prop_some_decimal_val(self, new_fluent_bus_obj):
        """
        Test setting the some_decimal_val property.
        """
        result = new_fluent_bus_obj.set_prop_some_decimal_val(
            Decimal('99.99'))
        assert new_fluent_bus_obj.some_decimal_val == \
            Decimal('99.99')
        assert result is new_fluent_bus_obj
    # someEmailAddress

    def test_set_prop_some_email_address(self, new_fluent_bus_obj):
        """
        Test setting the some_email_address property.
        """
        result = new_fluent_bus_obj.set_prop_some_email_address(
            "test@example.com")
        assert new_fluent_bus_obj.some_email_address == \
            "test@example.com"
        assert result is new_fluent_bus_obj
    # someFloatVal

    def test_set_prop_some_float_val(self, new_fluent_bus_obj):
        """
        Test setting the some_float_val property.
        """
        result = new_fluent_bus_obj.set_prop_some_float_val(3.14)
        assert math.isclose(new_fluent_bus_obj.some_float_val, 3.14)
        assert result is new_fluent_bus_obj
    # someIntVal

    def test_set_prop_some_int_val(self, new_fluent_bus_obj):
        """
        Test setting the some_int_val property.
        """
        result = new_fluent_bus_obj.set_prop_some_int_val(42)
        assert new_fluent_bus_obj.some_int_val == 42
        assert result is new_fluent_bus_obj
    # someMoneyVal

    def test_set_prop_some_money_val(self, new_fluent_bus_obj):
        """
        Test setting the some_money_val property.
        """
        result = new_fluent_bus_obj.set_prop_some_money_val(
            Decimal('100.00'))
        assert new_fluent_bus_obj.some_money_val == \
            Decimal('100.00')
        assert result is new_fluent_bus_obj
    # someNVarCharVal

    def test_set_prop_some_n_var_char_val(self, new_fluent_bus_obj):
        """
        Test setting the some_n_var_char_val property.
        """
        result = new_fluent_bus_obj.set_prop_some_n_var_char_val(
            "nvarchar")
        assert new_fluent_bus_obj.some_n_var_char_val == \
            "nvarchar"
        assert result is new_fluent_bus_obj
    # somePhoneNumber

    def test_set_prop_some_phone_number(self, new_fluent_bus_obj):
        """
        Test setting the some_phone_number property.
        """
        result = new_fluent_bus_obj.set_prop_some_phone_number(
            "123-456-7890")
        assert new_fluent_bus_obj.some_phone_number == \
            "123-456-7890"
        assert result is new_fluent_bus_obj
    # someTextVal

    def test_set_prop_some_text_val(self, new_fluent_bus_obj):
        """
        Test setting the some_text_val property.
        """
        result = new_fluent_bus_obj.set_prop_some_text_val(
            "Some text")
        assert new_fluent_bus_obj.some_text_val == \
            "Some text"
        assert result is new_fluent_bus_obj
    # someUniqueidentifierVal

    def test_set_prop_some_uniqueidentifier_val(self, new_fluent_bus_obj):
        """
        Test setting the some_uniqueidentifier_val property.
        """
        test_uuid = uuid4()
        result = new_fluent_bus_obj.set_prop_some_uniqueidentifier_val(
            test_uuid)
        assert new_fluent_bus_obj.some_uniqueidentifier_val == \
            test_uuid
        assert result is new_fluent_bus_obj
    # someUTCDateTimeVal

    def test_set_prop_some_utc_date_time_val(self, new_fluent_bus_obj):
        """
        Test setting the some_utc_date_time_val property.
        """
        test_datetime = datetime(2023, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
        result = new_fluent_bus_obj.set_prop_some_utc_date_time_val(
            test_datetime)
        assert new_fluent_bus_obj.some_utc_date_time_val == \
            test_datetime
        assert result is new_fluent_bus_obj
    # someVarCharVal

    def test_set_prop_some_var_char_val(self, new_fluent_bus_obj):
        """
        Test setting the some_var_char_val property.
        """
        result = new_fluent_bus_obj.set_prop_some_var_char_val(
            "varchar")
        assert new_fluent_bus_obj.some_var_char_val == \
            "varchar"
        assert result is new_fluent_bus_obj
    # LandID
# endset
    # isDeleteAllowed,
    # isEditAllowed,
    # otherFlavor,
    # someBigIntVal,
    # someBitVal,
    # someDecimalVal,
    # someEmailAddress,
    # someFloatVal,
    # someIntVal,
    # someMoneyVal,
    # someNVarCharVal,
    # someDateVal
    # someUTCDateTimeVal
    # FlvrForeignKeyID

    def test_set_prop_flvr_foreign_key_id(self, new_fluent_bus_obj):
        """
        Test setting the flvr_foreign_key_id property.
        """
        result = new_fluent_bus_obj.set_prop_flvr_foreign_key_id(1)
        assert new_fluent_bus_obj.flvr_foreign_key_id == 1
        assert result is new_fluent_bus_obj
    # LandID

    def test_set_prop_land_id(self, new_fluent_bus_obj):
        """
        Test setting the land_id property.
        """
        result = new_fluent_bus_obj.set_prop_land_id(1)
        assert new_fluent_bus_obj.land_id == 1
        assert result is new_fluent_bus_obj
    # somePhoneNumber,
    # someTextVal,
    # someUniqueidentifierVal,
    # someVarCharVal,
# endset
