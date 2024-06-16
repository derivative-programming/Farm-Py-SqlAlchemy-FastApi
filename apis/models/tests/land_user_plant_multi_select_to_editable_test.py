# apis/models/tests/land_user_plant_multi_select_to_editable_test.py
# pylint: disable=unused-argument
"""
    #TODO add comment
"""
import uuid
from datetime import date, datetime
from decimal import Decimal
from unittest.mock import AsyncMock, patch
import pytest
from business.land import LandBusObj
from flows.land_user_plant_multi_select_to_editable import FlowLandUserPlantMultiSelectToEditable, FlowLandUserPlantMultiSelectToEditableResult
from helpers.session_context import SessionContext
from helpers.type_conversion import TypeConversion
from models.factory.land import LandFactory
from ...models.land_user_plant_multi_select_to_editable import (LandUserPlantMultiSelectToEditablePostModelResponse)
from ..factory.land_user_plant_multi_select_to_editable import LandUserPlantMultiSelectToEditablePostModelRequestFactory
class TestLandUserPlantMultiSelectToEditablePostModelResponse:
    """
    #TODO add comment
    """
    @pytest.mark.asyncio
    async def test_flow_process_request(self, session):
        """
            #TODO add comment
        """
        async def mock_process(
            land_bus_obj: LandBusObj,
            plant_code_list_csv: str = "",
        ):
            return FlowLandUserPlantMultiSelectToEditableResult()
        with patch.object(
            FlowLandUserPlantMultiSelectToEditable,
            'process',
            new_callable=AsyncMock
        ) as mock_method:
            mock_method.side_effect = mock_process
            request_instance = await (
                LandUserPlantMultiSelectToEditablePostModelRequestFactory
                .create_async(
                    session=session
                )
            )
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

