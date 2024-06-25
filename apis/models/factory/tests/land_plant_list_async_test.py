# apis/models/factory/tests/land_plant_list_async_test.py
# pylint: disable=unused-import

"""
This module contains test cases for the
LandPlantListGetModelRequestFactoryAsync
class.
"""

import uuid  # noqa: F401
from datetime import date, datetime  # noqa: F401
from decimal import Decimal  # noqa: F401

import pytest

from ...land_plant_list import (
    LandPlantListGetModelRequest)
from ..land_plant_list import (
    LandPlantListGetModelRequestFactory)


class TestLandPlantListGetModelRequestFactoryAsync:
    """
    This class contains test cases for the
    LandPlantListGetModelRequestFactoryAsync
    class.
    """

    @pytest.mark.asyncio
    async def test_create_async(self, session):
        """
        Test the create_async method of
        LandPlantListGetModelRequestFactoryAsync
        class.
        """

        model_instance = await (
            LandPlantListGetModelRequestFactory
            .create_async(
                session=session
            )
        )
        assert isinstance(model_instance,
                          LandPlantListGetModelRequest)
        assert isinstance(model_instance.flavor_code,
                          uuid.UUID)
        assert isinstance(model_instance.some_int_val,
                          int)
        assert isinstance(model_instance.some_big_int_val,
                          int)
        assert isinstance(model_instance.some_float_val,
                          float)
        assert isinstance(model_instance.some_bit_val,
                          bool)
        assert isinstance(model_instance.is_edit_allowed,
                          bool)
        assert isinstance(model_instance.is_delete_allowed,
                          bool)
        assert isinstance(model_instance.some_decimal_val,
                          Decimal)
        assert isinstance(model_instance.some_min_utc_date_time_val,
                          datetime)
        assert isinstance(model_instance.some_min_date_val,
                          date)
        assert isinstance(model_instance.some_money_val,
                          Decimal)
        assert isinstance(model_instance.some_n_var_char_val,
                          str)
        assert isinstance(model_instance.some_var_char_val,
                          str)
        assert isinstance(model_instance.some_text_val,
                          str)
        assert isinstance(model_instance.some_phone_number,
                          str)
        assert isinstance(model_instance.some_email_address,
                          str)
        assert isinstance(model_instance.page_number,
                          int)
        assert isinstance(model_instance.item_count_per_page,
                          int)
