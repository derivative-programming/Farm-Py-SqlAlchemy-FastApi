# apis/models/tests/land_add_plant_test.py
# pylint: disable=unused-argument
"""
This module contains unit tests for the
LandAddPlantPostModelResponse class.
"""

import uuid
from datetime import date, datetime
from decimal import Decimal
from unittest.mock import AsyncMock, patch

import pytest

from business.land import LandBusObj
from flows.land_add_plant import FlowLandAddPlant, FlowLandAddPlantResult
from helpers.session_context import SessionContext
from helpers.type_conversion import TypeConversion
from models.factory.land import LandFactory

from ...models.land_add_plant import (LandAddPlantPostModelResponse)
from ..factory.land_add_plant import LandAddPlantPostModelRequestFactory


class TestLandAddPlantPostModelResponse:
    """
    This class contains unit tests for the
    LandAddPlantPostModelResponse class.
    """

    @pytest.mark.asyncio
    async def test_flow_process_request(self, session):
        """
        This method tests the flow process request
        for adding a plant to a land.
        It mocks the process method of FlowLandAddPlant
        and asserts that the response is successful.
        """

        async def mock_process(
            land_bus_obj: LandBusObj,
            request_flavor_code: uuid.UUID = uuid.UUID(int=0),
            request_other_flavor: str = "",
            request_some_int_val: int = 0,
            request_some_big_int_val: int = 0,
            request_some_bit_val: bool = False,
            request_is_edit_allowed: bool = False,
            request_is_delete_allowed: bool = False,
            request_some_float_val: float = 0,
            request_some_decimal_val: Decimal = Decimal(0),
            request_some_utc_date_time_val: datetime = (
                TypeConversion.get_default_date_time()),
            request_some_date_val: date = TypeConversion.get_default_date(),
            request_some_money_val: Decimal = Decimal(0),
            request_some_n_var_char_val: str = "",
            request_some_var_char_val: str = "",
            request_some_text_val: str = "",
            request_some_phone_number: str = "",
            request_some_email_address: str = "",
            request_sample_image_upload_file: str = "",
        ):
            return FlowLandAddPlantResult()
        with patch.object(
            FlowLandAddPlant,
            'process',
            new_callable=AsyncMock
        ) as mock_method:
            mock_method.side_effect = mock_process

            request_instance = await (
                LandAddPlantPostModelRequestFactory
                .create_async(
                    session=session
                )
            )
            response_instance = LandAddPlantPostModelResponse()
            session_context = SessionContext(dict(), session)

            land = await LandFactory.create_async(session)

            await response_instance.process_request(
                session_context=session_context,
                land_code=land.code,
                request=request_instance
            )
            assert response_instance.success is True
            mock_method.assert_awaited()
