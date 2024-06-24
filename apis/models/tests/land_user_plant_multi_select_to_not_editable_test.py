# apis/models/tests/land_user_plant_multi_select_to_not_editable_test.py
# pylint: disable=unused-argument
"""
This module contains unit tests for the
LandUserPlantMultiSelectToNotEditablePostModelResponse class.
"""
import uuid
import math
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
TEST_ERROR_TEXT = "Test Error"
TEST_EMAIL = "test@example.com"
TEST_PHONE = "123-456-7890"
class TestLandUserPlantMultiSelectToNotEditablePostModelRequest:
    """
    This class contains unit tests for the
    LandUserPlantMultiSelectToNotEditablePostModelRequest class.
    """
    def test_default_values(self):
        """
        This method tests the default values of the
        LandUserPlantMultiSelectToNotEditablePostModelRequest class.
        """
        model = LandUserPlantMultiSelectToNotEditablePostModelRequest()
        assert model.force_error_message == ""
# endset
        assert model.plant_code_list_csv == ""
# endset
    def test_to_dict_snake(self):
        """
        This method tests the to_dict_snake method of the
        LandUserPlantMultiSelectToNotEditablePostModelRequest class.
        """
        model = LandUserPlantMultiSelectToNotEditablePostModelRequest(
            force_error_message=TEST_ERROR_TEXT,
# endset  # noqa: E122
            plant_code_list_csv="Plant Code List Csv",
# endset  # noqa: E122
        )
        snake_case_dict = model.to_dict_snake()
        assert snake_case_dict['force_error_message'] == TEST_ERROR_TEXT
# endset
        assert snake_case_dict['plant_code_list_csv'] == \
            model.plant_code_list_csv
# endset
    def test_to_dict_camel(self):
        """
        This method tests the to_dict_camel method of the
        LandUserPlantMultiSelectToNotEditablePostModelRequest class.
        """
        model = LandUserPlantMultiSelectToNotEditablePostModelRequest(
            force_error_message=TEST_ERROR_TEXT,
# endset  # noqa: E122
            plant_code_list_csv="Plant Code List Csv",
# endset  # noqa: E122
        )
        camel_case_dict = model.to_dict_camel()
        assert camel_case_dict['forceErrorMessage'] == TEST_ERROR_TEXT
# endset
        assert camel_case_dict['plantCodeListCsv'] == \
            model.plant_code_list_csv
# endset
    def test_to_dict_snake_serialized(self):
        """
        This method tests the to_dict_snake_serialized method of the
        LandUserPlantMultiSelectToNotEditablePostModelRequest class.
        """
        # Create an instance of the LandUserPlantMultiSelectToNotEditablePostModelRequest class
        request = LandUserPlantMultiSelectToNotEditablePostModelRequest(
            force_error_message="Test Error Message",
# endset  # noqa: E122
            plant_code_list_csv="Test Flavor",
# endset  # noqa: E122
        )
        # Convert the model to a dictionary with snake_case keys and serialized values
        data = request.to_dict_snake_serialized()
        # Define the expected dictionary
        expected_data = {
            "force_error_message": "Test Error Message",
# endset  # noqa: E122
            "plant_code_list_csv": "Test Flavor",
# endset  # noqa: E122
        }
        # Compare the actual and expected dictionaries
        assert data == expected_data
    def test_to_dict_camel_serialized(self):
        """
        This method tests the to_dict_camel_serialized method of the
        LandUserPlantMultiSelectToNotEditablePostModelRequest class.
        """
        request = LandUserPlantMultiSelectToNotEditablePostModelRequest(
            force_error_message="Test Error Message",
            plant_code_list_csv="Test Flavor",
        )
        expected_data = {
            "forceErrorMessage": "Test Error Message",
            "plantCodeListCsv": "Test Flavor",
        }
        data = request.to_dict_camel_serialized()
        assert data == expected_data
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

