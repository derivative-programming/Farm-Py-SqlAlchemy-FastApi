# apis/models/tests/land_add_plant_test.py

"""
    #TODO add comment
"""

import asyncio
import time
import uuid
from datetime import date, datetime
from decimal import Decimal
from typing import AsyncGenerator
from unittest.mock import AsyncMock, patch

import pytest
import pytest_asyncio
from pydantic import UUID4, Field
from sqlalchemy import String, event
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.future import select
from sqlalchemy.orm import sessionmaker

import flows.constants.error_log_config_resolve_error_log as FlowConstants
from business.land import LandBusObj
from flows.base.flow_validation_error import FlowValidationError
from flows.land_add_plant import FlowLandAddPlant, FlowLandAddPlantResult
from helpers.session_context import SessionContext
from helpers.type_conversion import TypeConversion
from models import Base
from models.factory.land import LandFactory

from ...models.land_add_plant import (LandAddPlantPostModelRequest,
                                      LandAddPlantPostModelResponse)
from ..factory.land_add_plant import LandAddPlantPostModelRequestFactory


class TestLandAddPlantPostModelResponse:
    """
    #TODO add comment
    """

    @pytest.mark.asyncio
    async def test_flow_process_request(self, session):
        async def mock_process(
            land_bus_obj: LandBusObj,  # pylint: disable=unused-argument
            request_flavor_code: uuid.UUID = uuid.UUID(int=0),  # pylint: disable=unused-argument
            request_other_flavor: str = "",  # pylint: disable=unused-argument
            request_some_int_val: int = 0,  # pylint: disable=unused-argument
            request_some_big_int_val: int = 0,  # pylint: disable=unused-argument
            request_some_bit_val: bool = False,  # pylint: disable=unused-argument
            request_is_edit_allowed: bool = False,  # pylint: disable=unused-argument
            request_is_delete_allowed: bool = False,  # pylint: disable=unused-argument
            request_some_float_val: float = 0,  # pylint: disable=unused-argument
            request_some_decimal_val: Decimal = 0,  # pylint: disable=unused-argument
            request_some_utc_date_time_val: datetime = TypeConversion.get_default_date_time(),  # pylint: disable=unused-argument
            request_some_date_val: date = TypeConversion.get_default_date(),  # pylint: disable=unused-argument
            request_some_money_val: Decimal = 0,  # pylint: disable=unused-argument
            request_some_n_var_char_val: str = "",  # pylint: disable=unused-argument
            request_some_var_char_val: str = "",  # pylint: disable=unused-argument
            request_some_text_val: str = "",  # pylint: disable=unused-argument
            request_some_phone_number: str = "",  # pylint: disable=unused-argument
            request_some_email_address: str = "",  # pylint: disable=unused-argument
            request_sample_image_upload_file: str = "",  # pylint: disable=unused-argument
        ):
            return FlowLandAddPlantResult()
        with patch.object(FlowLandAddPlant, 'process', new_callable=AsyncMock) as mock_method:
            mock_method.side_effect = mock_process

            request_instance = await LandAddPlantPostModelRequestFactory.create_async(session=session)
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
