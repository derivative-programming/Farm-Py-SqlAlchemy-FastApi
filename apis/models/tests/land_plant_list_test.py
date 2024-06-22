# apis/models/tests/land_plant_list_test.py

"""
This module contains unit tests for the
LandPlantListGetModelRequestFactoryAsync class.
"""

import uuid
from datetime import date, datetime
from decimal import Decimal

import pytest

from helpers.type_conversion import TypeConversion

from ..factory.land_plant_list import LandPlantListGetModelRequestFactory
from ..land_plant_list import LandPlantListGetModelRequest



class TestLandPlantListGetModelRequest():

    def test_default_values(self):
        model = LandPlantListGetModelRequest()
        assert model.page_number == 0
        assert model.item_count_per_page == 0
        assert model.order_by_column_name == ""
        assert model.order_by_descending is False
        assert model.force_error_message == ""
# endset
        assert model.flavor_code == uuid.UUID('00000000-0000-0000-0000-000000000000')
        assert model.some_int_val == 0
        assert model.some_big_int_val == 0
        assert model.some_float_val == 0.0
        assert model.some_bit_val is False
        assert model.is_edit_allowed is False
        assert model.is_delete_allowed is False
        assert model.some_decimal_val == Decimal(0)
        assert model.some_min_utc_date_time_val == TypeConversion.get_default_date_time()
        assert model.some_min_date_val == TypeConversion.get_default_date()
        assert model.some_money_val == Decimal(0)
        assert model.some_n_var_char_val == ""
        assert model.some_var_char_val == ""
        assert model.some_text_val == ""
        assert model.some_phone_number == ""
        assert model.some_email_address == ""
# endset

    def test_to_dict_snake(self):
        model = LandPlantListGetModelRequest(
            page_number=1,
            item_count_per_page=10,
            order_by_column_name="name",
            order_by_descending=True,
            force_error_message="Test Error",
# endset
            flavor_code=uuid.uuid4(),  # Use a valid version 4 UUID
            some_int_val=42,
            some_big_int_val=123456789,
            some_float_val=3.14,
            some_bit_val=True,
            is_edit_allowed=True,
            is_delete_allowed=True,
            some_decimal_val=Decimal('99.99'),
            some_min_utc_date_time_val=datetime(2023, 1, 1, 12, 0, 0),
            some_min_date_val=date(2023, 1, 1),
            some_money_val=Decimal('100.00'),
            some_n_var_char_val="nvarchar",
            some_var_char_val="varchar",
            some_text_val="text",
            some_phone_number="123-456-7890",
            some_email_address="test@example.com"
# endset
        )

        snake_case_dict = model.to_dict_snake()
        assert snake_case_dict['page_number'] == 1
        assert snake_case_dict['item_count_per_page'] == 10
        assert snake_case_dict['order_by_column_name'] == "name"
        assert snake_case_dict['order_by_descending'] is True
        assert snake_case_dict['force_error_message'] == "Test Error"
# endset
        assert snake_case_dict['flavor_code'] == model.flavor_code
        assert snake_case_dict['some_int_val'] == 42
        assert snake_case_dict['some_big_int_val'] == 123456789
        assert snake_case_dict['some_float_val'] == 3.14
        assert snake_case_dict['some_bit_val'] is True
        assert snake_case_dict['is_edit_allowed'] is True
        assert snake_case_dict['is_delete_allowed'] is True
        assert snake_case_dict['some_decimal_val'] == Decimal('99.99')
        assert snake_case_dict['some_min_utc_date_time_val'] == datetime(2023, 1, 1, 12, 0, 0)
        assert snake_case_dict['some_min_date_val'] == date(2023, 1, 1)
        assert snake_case_dict['some_money_val'] == Decimal('100.00')
        assert snake_case_dict['some_n_var_char_val'] == "nvarchar"
        assert snake_case_dict['some_var_char_val'] == "varchar"
        assert snake_case_dict['some_text_val'] == "text"
        assert snake_case_dict['some_phone_number'] == "123-456-7890"
        assert snake_case_dict['some_email_address'] == "test@example.com"
# endset

    def test_to_dict_camel(self):
        model = LandPlantListGetModelRequest(
            page_number=1,
            item_count_per_page=10,
            order_by_column_name="name",
            order_by_descending=True,
            force_error_message="Test Error",
# endset
            flavor_code=uuid.uuid4(),  # Use a valid version 4 UUID
            some_int_val=42,
            some_big_int_val=123456789,
            some_float_val=3.14,
            some_bit_val=True,
            is_edit_allowed=True,
            is_delete_allowed=True,
            some_decimal_val=Decimal('99.99'),
            some_min_utc_date_time_val=datetime(2023, 1, 1, 12, 0, 0),
            some_min_date_val=date(2023, 1, 1),
            some_money_val=Decimal('100.00'),
            some_n_var_char_val="nvarchar",
            some_var_char_val="varchar",
            some_text_val="text",
            some_phone_number="123-456-7890",
            some_email_address="test@example.com"
# endset
        )

        camel_case_dict = model.to_dict_camel()
        assert camel_case_dict['pageNumber'] == 1
        assert camel_case_dict['itemCountPerPage'] == 10
        assert camel_case_dict['orderByColumnName'] == "name"
        assert camel_case_dict['orderByDescending'] is True
        assert camel_case_dict['forceErrorMessage'] == "Test Error"
# endset
        assert camel_case_dict['flavorCode'] == model.flavor_code  # Convert to string for comparison
        assert camel_case_dict['someIntVal'] == 42
        assert camel_case_dict['someBigIntVal'] == 123456789
        assert camel_case_dict['someFloatVal'] == 3.14
        assert camel_case_dict['someBitVal'] is True
        assert camel_case_dict['isEditAllowed'] is True
        assert camel_case_dict['isDeleteAllowed'] is True
        assert camel_case_dict['someDecimalVal'] == Decimal('99.99')
        # assert camel_case_dict['someMinUtcDateTimeVal'] == datetime(2023, 1, 1, 12, 0, 0).isoformat()  # Convert to ISO format
        # assert camel_case_dict['someMinDateVal'] == date(2023, 1, 1).isoformat()  # Convert to ISO format
        assert camel_case_dict['someMoneyVal'] == Decimal('100.00')
        assert camel_case_dict['someNVarCharVal'] == "nvarchar"
        assert camel_case_dict['someVarCharVal'] == "varchar"
        assert camel_case_dict['someTextVal'] == "text"
        assert camel_case_dict['somePhoneNumber'] == "123-456-7890"
        assert camel_case_dict['someEmailAddress'] == "test@example.com"
# endset


class LandPlantListGetModelRequestFactoryAsync:
    """
    This class contains asynchronous unit tests for the
    LandPlantListGetModelRequestFactory class.
    """

    @pytest.mark.asyncio
    async def test_report_generation(self, session):
        """
        Test the generation of a report using the
        LandPlantListGetModelRequestFactory class.

        Args:
            session: The database session.

        Returns:
            None

        Raises:
            AssertionError: If any of the assertions fail.
        """

        model_instance = await (
            LandPlantListGetModelRequestFactory
            .create_async(session=session)
        )
        assert isinstance(model_instance, LandPlantListGetModelRequest)
        assert isinstance(model_instance.flavor_code, uuid.UUID)
        assert isinstance(model_instance.some_int_val, int)
        assert isinstance(model_instance.some_big_int_val, int)
        assert isinstance(model_instance.some_float_val, float)
        assert isinstance(model_instance.some_bit_val, bool)
        assert isinstance(model_instance.is_edit_allowed, bool)
        assert isinstance(model_instance.is_delete_allowed, bool)
        assert isinstance(model_instance.some_decimal_val, Decimal)
        assert isinstance(model_instance.some_min_utc_date_time_val, datetime)
        assert isinstance(model_instance.some_min_date_val, date)
        assert isinstance(model_instance.some_money_val, Decimal)
        assert isinstance(model_instance.some_n_var_char_val, str)
        assert isinstance(model_instance.some_var_char_val, str)
        assert isinstance(model_instance.some_text_val, str)
        assert isinstance(model_instance.some_phone_number, str)
        assert isinstance(model_instance.some_email_address, str)
        assert isinstance(model_instance.page_number, int)
        assert isinstance(model_instance.item_count_per_page, int)
