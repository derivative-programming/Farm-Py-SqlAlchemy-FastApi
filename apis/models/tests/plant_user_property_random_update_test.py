# apis/models/tests/plant_user_property_random_update_test.py
# pylint: disable=unused-argument
"""
This module contains unit tests for the
PlantUserPropertyRandomUpdatePostModelResponse class.
"""
import uuid
from datetime import date, datetime
from decimal import Decimal
from unittest.mock import AsyncMock, patch
import pytest
from business.plant import PlantBusObj
from flows.plant_user_property_random_update import FlowPlantUserPropertyRandomUpdate, FlowPlantUserPropertyRandomUpdateResult
from helpers.session_context import SessionContext
from helpers.type_conversion import TypeConversion
from models.factory.plant import PlantFactory
from ...models.plant_user_property_random_update import (
    PlantUserPropertyRandomUpdatePostModelResponse,
    PlantUserPropertyRandomUpdatePostModelRequest)
from ..factory.plant_user_property_random_update import PlantUserPropertyRandomUpdatePostModelRequestFactory
class TestPlantUserPropertyRandomUpdatePostModelRequest:
    """
    This class contains unit tests for the
    PlantUserPropertyRandomUpdatePostModelRequest class.
    """
    def test_default_values(self):
        """
        This method tests the default values of the
        PlantUserPropertyRandomUpdatePostModelRequest class.
        """
        model = PlantUserPropertyRandomUpdatePostModelRequest()
        assert model.force_error_message == ""
# endset

# endset
    def test_to_dict_snake(self):
        """
        This method tests the to_dict_snake method of the
        PlantUserPropertyRandomUpdatePostModelRequest class.
        """
        model = PlantUserPropertyRandomUpdatePostModelRequest(
            force_error_message="Test Error",
# endset  # noqa: E122

# endset  # noqa: E122
        )
        snake_case_dict = model.to_dict_snake()
        assert snake_case_dict['force_error_message'] == "Test Error"
# endset

# endset
    def test_to_dict_camel(self):
        """
        This method tests the to_dict_camel method of the
        PlantUserPropertyRandomUpdatePostModelRequest class.
        """
        model = PlantUserPropertyRandomUpdatePostModelRequest(
            force_error_message="Test Error",
# endset  # noqa: E122

# endset  # noqa: E122
        )
        camel_case_dict = model.to_dict_camel()
        assert camel_case_dict['forceErrorMessage'] == "Test Error"
# endset

# endset
    def test_to_dict_snake_serialized(self):
        """
        This method tests the to_dict_snake_serialized method of the
        PlantUserPropertyRandomUpdatePostModelRequest class.
        """
        # Create an instance of the PlantUserPropertyRandomUpdatePostModelRequest class
        request = PlantUserPropertyRandomUpdatePostModelRequest(
            force_error_message="Test Error Message",
# endset  # noqa: E122

# endset  # noqa: E122
        )
        # Convert the model to a dictionary with snake_case keys and serialized values
        data = request.to_dict_snake_serialized()
        # Define the expected dictionary
        expected_data = {
            "force_error_message": "Test Error Message",
# endset  # noqa: E122

# endset  # noqa: E122
        }
        # Compare the actual and expected dictionaries
        assert data == expected_data
    def test_to_dict_camel_serialized(self):
        """
        This method tests the to_dict_camel_serialized method of the
        PlantUserPropertyRandomUpdatePostModelRequest class.
        """
        request = PlantUserPropertyRandomUpdatePostModelRequest(
            force_error_message="Test Error Message",

        )
        expected_data = {
            "forceErrorMessage": "Test Error Message",

        }
        data = request.to_dict_camel_serialized()
        assert data == expected_data
class TestPlantUserPropertyRandomUpdatePostModelResponse:
    """
    This class contains unit tests for the
    PlantUserPropertyRandomUpdatePostModelResponse class.
    """
    @pytest.mark.asyncio
    async def test_flow_process_request(self, session):
        """
        This method tests the flow process request
        for adding a  to a plant.
        It mocks the process method of FlowPlantUserPropertyRandomUpdate
        and asserts that the response is successful.
        """
        async def mock_process(
            plant_bus_obj: PlantBusObj,

        ):
            return FlowPlantUserPropertyRandomUpdateResult()
        with patch.object(
            FlowPlantUserPropertyRandomUpdate,
            'process',
            new_callable=AsyncMock
        ) as mock_method:
            mock_method.side_effect = mock_process
            request_instance = await (
                PlantUserPropertyRandomUpdatePostModelRequestFactory
                .create_async(
                    session=session
                )
            )
            response_instance = PlantUserPropertyRandomUpdatePostModelResponse()
            session_context = SessionContext(dict(), session)
            plant = await PlantFactory.create_async(session)
            await response_instance.process_request(
                session_context=session_context,
                plant_code=plant.code,
                request=request_instance
            )
            assert response_instance.success is True
            mock_method.assert_awaited()

