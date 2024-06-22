# apis/models/tests/land_user_plant_multi_select_to_editable_test.py
# pylint: disable=unused-argument
"""
This module contains unit tests for the
LandUserPlantMultiSelectToEditablePostModelResponse class.
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
from ...models.land_user_plant_multi_select_to_editable import (
    LandUserPlantMultiSelectToEditablePostModelResponse,
    LandUserPlantMultiSelectToEditablePostModelRequest)
from ..factory.land_user_plant_multi_select_to_editable import LandUserPlantMultiSelectToEditablePostModelRequestFactory
class TestLandUserPlantMultiSelectToEditablePostModelRequest:
    def test_default_values(self):
        model = LandUserPlantMultiSelectToEditablePostModelRequest()
        assert model.force_error_message == ""
# endset
        assert model.plant_code_list_csv == ""
# endset
    def test_to_dict_snake(self):
        model = LandUserPlantMultiSelectToEditablePostModelRequest(
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
        model = LandUserPlantMultiSelectToEditablePostModelRequest(
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
class TestLandUserPlantMultiSelectToEditablePostModelResponse:
    """
    This class contains unit tests for the
    LandUserPlantMultiSelectToEditablePostModelResponse class.
    """
    @pytest.mark.asyncio
    async def test_flow_process_request(self, session):
        """
        This method tests the flow process request
        for adding a  to a land.
        It mocks the process method of FlowLandUserPlantMultiSelectToEditable
        and asserts that the response is successful.
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

