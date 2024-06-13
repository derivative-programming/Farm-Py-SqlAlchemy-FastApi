# apis/models/tests/plant_user_delete_test.py
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
from business.plant import PlantBusObj
from flows.base.flow_validation_error import FlowValidationError
from flows.plant_user_delete import FlowPlantUserDelete, FlowPlantUserDeleteResult
from helpers.session_context import SessionContext
from helpers.type_conversion import TypeConversion
from models import Base
from models.factory.plant import PlantFactory
from ...models.plant_user_delete import (PlantUserDeletePostModelRequest,
                                      PlantUserDeletePostModelResponse)
from ..factory.plant_user_delete import PlantUserDeletePostModelRequestFactory
class TestPlantUserDeletePostModelResponse:
    """
    #TODO add comment
    """
    @pytest.mark.asyncio
    async def test_flow_process_request(self, session):
        async def mock_process(
            plant_bus_obj: PlantBusObj,  # pylint: disable=unused-argument

        ):
            return FlowPlantUserDeleteResult()
        with patch.object(FlowPlantUserDelete, 'process', new_callable=AsyncMock) as mock_method:
            mock_method.side_effect = mock_process
            request_instance = await PlantUserDeletePostModelRequestFactory.create_async(session=session)
            response_instance = PlantUserDeletePostModelResponse()
            session_context = SessionContext(dict(), session)
            plant = await PlantFactory.create_async(session)
            await response_instance.process_request(
                session_context=session_context,
                plant_code=plant.code,
                request=request_instance
            )
            assert response_instance.success is True
            mock_method.assert_awaited()

