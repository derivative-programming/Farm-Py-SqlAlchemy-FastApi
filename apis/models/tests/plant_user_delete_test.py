# apis/models/tests/plant_user_delete_test.py
# pylint: disable=unused-argument
"""
This module contains unit tests for the
PlantUserDeletePostModelResponse class.
"""
import uuid
from datetime import date, datetime
from decimal import Decimal
from unittest.mock import AsyncMock, patch
import pytest
from business.plant import PlantBusObj
from flows.plant_user_delete import FlowPlantUserDelete, FlowPlantUserDeleteResult
from helpers.session_context import SessionContext
from helpers.type_conversion import TypeConversion
from models.factory.plant import PlantFactory
from ...models.plant_user_delete import (
    PlantUserDeletePostModelResponse,
    PlantUserDeletePostModelRequest)
from ..factory.plant_user_delete import PlantUserDeletePostModelRequestFactory
class TestPlantUserDeletePostModelRequest:
    def test_default_values(self):
        model = PlantUserDeletePostModelRequest()
        assert model.force_error_message == ""
# endset

# endset
    def test_to_dict_snake(self):
        model = PlantUserDeletePostModelRequest(
            force_error_message="Test Error",
# endset

# endset
        )
        snake_case_dict = model.to_dict_snake()
        assert snake_case_dict['force_error_message'] == "Test Error"
# endset

# endset
    def test_to_dict_camel(self):
        model = PlantUserDeletePostModelRequest(
            force_error_message="Test Error",
# endset

# endset
        )
        camel_case_dict = model.to_dict_camel()
        assert camel_case_dict['forceErrorMessage'] == "Test Error"
# endset

# endset
class TestPlantUserDeletePostModelResponse:
    """
    This class contains unit tests for the
    PlantUserDeletePostModelResponse class.
    """
    @pytest.mark.asyncio
    async def test_flow_process_request(self, session):
        """
        This method tests the flow process request
        for adding a  to a plant.
        It mocks the process method of FlowPlantUserDelete
        and asserts that the response is successful.
        """
        async def mock_process(
            plant_bus_obj: PlantBusObj,

        ):
            return FlowPlantUserDeleteResult()
        with patch.object(
            FlowPlantUserDelete,
            'process',
            new_callable=AsyncMock
        ) as mock_method:
            mock_method.side_effect = mock_process
            request_instance = await (
                PlantUserDeletePostModelRequestFactory
                .create_async(
                    session=session
                )
            )
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

