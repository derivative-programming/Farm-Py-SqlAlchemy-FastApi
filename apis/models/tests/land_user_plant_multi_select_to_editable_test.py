# apis/models/tests/land_user_plant_multi_select_to_editable_test.py
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
from flows.land_user_plant_multi_select_to_editable import FlowLandUserPlantMultiSelectToEditable, FlowLandUserPlantMultiSelectToEditableResult
from helpers.session_context import SessionContext
from helpers.type_conversion import TypeConversion
from models import Base
from models.factory.land import LandFactory
from ...models.land_user_plant_multi_select_to_editable import (LandUserPlantMultiSelectToEditablePostModelRequest,
                                      LandUserPlantMultiSelectToEditablePostModelResponse)
from ..factory.land_user_plant_multi_select_to_editable import LandUserPlantMultiSelectToEditablePostModelRequestFactory
class TestLandUserPlantMultiSelectToEditablePostModelResponse:
    """
    #TODO add comment
    """
    @pytest.mark.asyncio
    async def test_flow_process_request(self, session):
        async def mock_process(
            land_bus_obj: LandBusObj,  # pylint: disable=unused-argument
            plant_code_list_csv: str = "",  # pylint: disable=unused-argument
        ):
            return FlowLandUserPlantMultiSelectToEditableResult()
        with patch.object(FlowLandUserPlantMultiSelectToEditable, 'process', new_callable=AsyncMock) as mock_method:
            mock_method.side_effect = mock_process
            request_instance = await LandUserPlantMultiSelectToEditablePostModelRequestFactory.create_async(session=session)
            response_instance = LandUserPlantMultiSelectToEditablePostModelResponse()
            session_context = SessionContext(dict(), session)
            land = await LandFactory.create_async(session)
            await response_instance.process_request(
                session_context=session_context,
                land_code=land.code,
                request=request_instance
            )
            assert response_instance.success is True
            mock_method.assert_awaited()

