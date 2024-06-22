# apis/models/tests/customer_build_temp_api_key_test.py
# pylint: disable=unused-argument
"""
This module contains unit tests for the
CustomerBuildTempApiKeyPostModelResponse class.
"""
import uuid
from datetime import date, datetime
from decimal import Decimal
from unittest.mock import AsyncMock, patch
import pytest
from business.customer import CustomerBusObj
from flows.customer_build_temp_api_key import FlowCustomerBuildTempApiKey, FlowCustomerBuildTempApiKeyResult
from helpers.session_context import SessionContext
from helpers.type_conversion import TypeConversion
from models.factory.customer import CustomerFactory
from ...models.customer_build_temp_api_key import (
    CustomerBuildTempApiKeyPostModelResponse,
    CustomerBuildTempApiKeyPostModelRequest)
from ..factory.customer_build_temp_api_key import CustomerBuildTempApiKeyPostModelRequestFactory
class TestCustomerBuildTempApiKeyPostModelRequest:
    def test_default_values(self):
        model = CustomerBuildTempApiKeyPostModelRequest()
        assert model.force_error_message == ""
# endset

# endset
    def test_to_dict_snake(self):
        model = CustomerBuildTempApiKeyPostModelRequest(
            force_error_message="Test Error",
# endset

# endset
        )
        snake_case_dict = model.to_dict_snake()
        assert snake_case_dict['force_error_message'] == "Test Error"
# endset

# endset
    def test_to_dict_camel(self):
        model = CustomerBuildTempApiKeyPostModelRequest(
            force_error_message="Test Error",
# endset

# endset
        )
        camel_case_dict = model.to_dict_camel()
        assert camel_case_dict['forceErrorMessage'] == "Test Error"
# endset

# endset
class TestCustomerBuildTempApiKeyPostModelResponse:
    """
    This class contains unit tests for the
    CustomerBuildTempApiKeyPostModelResponse class.
    """
    @pytest.mark.asyncio
    async def test_flow_process_request(self, session):
        """
        This method tests the flow process request
        for adding a  to a customer.
        It mocks the process method of FlowCustomerBuildTempApiKey
        and asserts that the response is successful.
        """
        async def mock_process(
            customer_bus_obj: CustomerBusObj,

        ):
            return FlowCustomerBuildTempApiKeyResult()
        with patch.object(
            FlowCustomerBuildTempApiKey,
            'process',
            new_callable=AsyncMock
        ) as mock_method:
            mock_method.side_effect = mock_process
            request_instance = await (
                CustomerBuildTempApiKeyPostModelRequestFactory
                .create_async(
                    session=session
                )
            )
            response_instance = CustomerBuildTempApiKeyPostModelResponse()
            session_context = SessionContext(dict(), session)
            customer = await CustomerFactory.create_async(session)
            await response_instance.process_request(
                session_context=session_context,
                customer_code=customer.code,
                request=request_instance
            )
            assert response_instance.success is True
            mock_method.assert_awaited()

