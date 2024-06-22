# apis/models/tests/land_user_plant_multi_select_to_not_editable_test.py
# pylint: disable=unused-argument
"""
This module contains unit tests for the
LandUserPlantMultiSelectToNotEditablePostModelResponse class.
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
from ...models.land_user_plant_multi_select_to_not_editable import (
    LandUserPlantMultiSelectToNotEditablePostModelResponse,
    LandUserPlantMultiSelectToNotEditablePostModelRequest)
from ..factory.land_user_plant_multi_select_to_not_editable import LandUserPlantMultiSelectToNotEditablePostModelRequestFactory
class TestLandUserPlantMultiSelectToNotEditablePostModelRequest:
    def test_default_values(self):
        model = LandUserPlantMultiSelectToNotEditablePostModelRequest()
        assert model.force_error_message == ""
# endset
        assert model.plant_code_list_csv == ""
# endset
    def test_to_dict_snake(self):
        model = LandUserPlantMultiSelectToNotEditablePostModelRequest(
            force_error_message="Test Error",
# endset
            plant_code_list_csv="Plant Code List Csv",
# endset
        )
        snake_case_dict = model.to_dict_snake()
        assert snake_case_dict['force_error_message'] == "Test Error"
# endset
        assert snake_case_dict['plant_code_list_csv'] == "Plant Code List Csv"
# endset
    def test_to_dict_camel(self):
        model = LandUserPlantMultiSelectToNotEditablePostModelRequest(
            force_error_message="Test Error",
# endset
            plant_code_list_csv="Plant Code List Csv",
# endset
        )
        camel_case_dict = model.to_dict_camel()
        assert camel_case_dict['forceErrorMessage'] == "Test Error"
# endset
        assert camel_case_dict['plantCodeListCsv'] == "Plant Code List Csv"
# endset
class TestLandUserPlantMultiSelectToNotEditablePostModelResponse:
    """
    This class contains unit tests for the
    LandUserPlantMultiSelectToNotEditablePostModelResponse class.
    """
    @pytest.mark.asyncio
    async def test_flow_process_request(self, session):
        """
        This method tests the flow process request
        for adding a  to a land.
        It mocks the process method of FlowLandUserPlantMultiSelectToNotEditable
        and asserts that the response is successful.
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

