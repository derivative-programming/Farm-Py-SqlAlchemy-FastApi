# apis/models/tests/land_user_plant_multi_select_to_not_editable_test.py
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
from flows.land_user_plant_multi_select_to_not_editable import FlowLandUserPlantMultiSelectToNotEditable, FlowLandUserPlantMultiSelectToNotEditableResult
from helpers.session_context import SessionContext
from helpers.type_conversion import TypeConversion
from models.factory.land import LandFactory
from ...models.land_user_plant_multi_select_to_not_editable import (LandUserPlantMultiSelectToNotEditablePostModelResponse)
from ..factory.land_user_plant_multi_select_to_not_editable import LandUserPlantMultiSelectToNotEditablePostModelRequestFactory
class TestLandUserPlantMultiSelectToNotEditablePostModelResponse:
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
            return FlowLandUserPlantMultiSelectToNotEditableResult()
        with patch.object(
            FlowLandUserPlantMultiSelectToNotEditable,
            'process',
            new_callable=AsyncMock
        ) as mock_method:
            mock_method.side_effect = mock_process
            request_instance = await (
                LandUserPlantMultiSelectToNotEditablePostModelRequestFactory
                .create_async(
                    session=session
                )
            )
            response_instance = LandUserPlantMultiSelectToNotEditablePostModelResponse()
            session_context = SessionContext(dict(), session)
            land = await LandFactory.create_async(session)
            await response_instance.process_request(
                session_context=session_context,
                land_code=land.code,
                request=request_instance
            )
            assert response_instance.success is True
            mock_method.assert_awaited()

