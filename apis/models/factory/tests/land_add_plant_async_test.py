# apis/models/factory/tests/land_add_plant_async_test.py
# pylint: disable=unused-import

"""
This module contains test cases for the
LandAddPlantPostModelRequestFactoryAsync
class.
"""

import uuid  # noqa: F401
from datetime import date, datetime  # noqa: F401
from decimal import Decimal  # noqa: F401

import pytest

from ...land_add_plant import (
    LandAddPlantPostModelRequest)
from ..land_add_plant import (
    LandAddPlantPostModelRequestFactory)


class TestLandAddPlantPostModelRequestFactoryAsync:
    """
    This class contains test cases for the
    LandAddPlantPostModelRequestFactoryAsync
    class.
    """

    @pytest.mark.asyncio
    async def test_create_async(self, session):
        """
        Test the create_async method of
        LandAddPlantPostModelRequestFactoryAsync
        class.
        """

        model_instance = await \
            LandAddPlantPostModelRequestFactory \
            .create_async(
                session=session)

        assert isinstance(
            model_instance,
            LandAddPlantPostModelRequest)
        assert isinstance(model_instance.request_flavor_code,
                          uuid.UUID)
        assert isinstance(model_instance.request_other_flavor,
                          str)
        assert isinstance(model_instance.request_some_int_val,
                          int)
        assert isinstance(model_instance.request_some_big_int_val,
                          int)
        assert isinstance(model_instance.request_some_bit_val,
                          bool)
        assert isinstance(model_instance.request_is_edit_allowed,
                          bool)
        assert isinstance(model_instance.request_is_delete_allowed,
                          bool)
        assert isinstance(model_instance.request_some_float_val,
                          float)
        assert isinstance(model_instance.request_some_decimal_val,
                          Decimal)
        assert isinstance(model_instance.request_some_utc_date_time_val,
                          datetime)
        assert isinstance(model_instance.request_some_date_val,
                          date)
        assert isinstance(model_instance.request_some_money_val,
                          Decimal)
        assert isinstance(model_instance.request_some_n_var_char_val,
                          str)
        assert isinstance(model_instance.request_some_var_char_val,
                          str)
        assert isinstance(model_instance.request_some_text_val,
                          str)
        assert isinstance(model_instance.request_some_phone_number,
                          str)
        assert isinstance(model_instance.request_some_email_address,
                          str)
        assert isinstance(model_instance.request_sample_image_upload_file,
                          str)
