# apis/models/tests/land_user_plant_multi_select_to_editable_test.py  # pylint: disable=duplicate-code # noqa: E501
# pylint: disable=unused-argument, too-many-public-methods
# pylint: disable=unused-import
# pylint: disable=too-few-public-methods
"""
This module contains unit tests for the
LandUserPlantMultiSelectToEditablePostModelResponse class.
"""

import uuid  # noqa: F401
import math  # noqa: F401
from datetime import date, datetime, timezone  # noqa: F401
from decimal import Decimal  # noqa: F401
from unittest.mock import AsyncMock, patch

import pytest

from business.land import LandBusObj
from flows.land_user_plant_multi_select_to_editable import (
    FlowLandUserPlantMultiSelectToEditable,
    FlowLandUserPlantMultiSelectToEditableResult)
from helpers.session_context import SessionContext
from helpers.type_conversion import TypeConversion  # noqa: F401
from models.factory.land import LandFactory

from ...models.land_user_plant_multi_select_to_editable import (
    LandUserPlantMultiSelectToEditablePostModelResponse,
    LandUserPlantMultiSelectToEditablePostModelRequest)
from ..factory.land_user_plant_multi_select_to_editable import (
    LandUserPlantMultiSelectToEditablePostModelRequestFactory)

TEST_ERROR_TEXT = "Test Error"

TEST_EMAIL = "test@example.com"

TEST_PHONE = "123-456-7890"


class TestLandUserPlantMultiSelectToEditablePostModelRequest:
    """
    This class contains unit tests for the
    LandUserPlantMultiSelectToEditablePostModelRequest class.
    """

    def test_default_values(self):
        """
        This method tests the default values of the
        LandUserPlantMultiSelectToEditablePostModelRequest class.
        """
        model = LandUserPlantMultiSelectToEditablePostModelRequest()
        assert model.force_error_message == ""
        assert model.plant_code_list_csv == ""

    def test_to_dict_snake(self):
        """
        This method tests the to_dict_snake method of the
        LandUserPlantMultiSelectToEditablePostModelRequest class.
        """
        model = LandUserPlantMultiSelectToEditablePostModelRequest(
            force_error_message=TEST_ERROR_TEXT,
# endset  # noqa: E122
            plant_code_list_csv="Plant Code List Csv",
# endset  # noqa: E122
        )

        snake_case_dict = model.to_dict_snake()
        assert snake_case_dict['force_error_message'] == TEST_ERROR_TEXT
        assert snake_case_dict['plant_code_list_csv'] == \
            model.plant_code_list_csv

    def test_to_dict_camel(self):
        """
        This method tests the to_dict_camel method of the
        LandUserPlantMultiSelectToEditablePostModelRequest class.
        """
        model = LandUserPlantMultiSelectToEditablePostModelRequest(
            force_error_message=TEST_ERROR_TEXT,
# endset  # noqa: E122
            plant_code_list_csv="Plant Code List Csv",
# endset  # noqa: E122
        )

        camel_case_dict = model.to_dict_camel()
        assert camel_case_dict['forceErrorMessage'] == TEST_ERROR_TEXT
        assert camel_case_dict['plantCodeListCsv'] == \
            model.plant_code_list_csv

    def test_to_dict_snake_serialized(self):
        """
        This method tests the to_dict_snake_serialized method of the
        LandUserPlantMultiSelectToEditablePostModelRequest class.
        """
        # Create an instance of the
        # LandUserPlantMultiSelectToEditablePostModelRequest class
        request = LandUserPlantMultiSelectToEditablePostModelRequest(
            force_error_message="Test Error Message",
# endset  # noqa: E122
            plant_code_list_csv="Test Text",
# endset  # noqa: E122
        )

        # Convert the model to a dictionary with snake_case
        # keys and serialized values
        data = request.to_dict_snake_serialized()

        # Define the expected dictionary
        expected_data = {
            "force_error_message": "Test Error Message",
# endset  # noqa: E122
            "plant_code_list_csv": "Test Text",
# endset  # noqa: E122
        }

        # Compare the actual and expected dictionaries
        assert data == expected_data

    def test_to_dict_camel_serialized(self):
        """
        This method tests the to_dict_camel_serialized method of the
        LandUserPlantMultiSelectToEditablePostModelRequest class.
        """
        request = LandUserPlantMultiSelectToEditablePostModelRequest(
            force_error_message="Test Error Message",
            plant_code_list_csv="Test Text",
        )

        expected_data = {
            "forceErrorMessage": "Test Error Message",
            "plantCodeListCsv": "Test Text",
        }

        data = request.to_dict_camel_serialized()

        assert data == expected_data


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
        It mocks the process method of
        FlowLandUserPlantMultiSelectToEditable
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
            response_instance = \
                LandUserPlantMultiSelectToEditablePostModelResponse()
            session_context = SessionContext({}, session)

            land = await LandFactory.create_async(session)

            await response_instance.process_request(
                session_context=session_context,
                land_code=land.code,
                request=request_instance
            )
            assert response_instance.success is True
            mock_method.assert_awaited()
