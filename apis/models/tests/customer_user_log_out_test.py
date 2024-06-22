# apis/models/tests/customer_user_log_out_test.py
# pylint: disable=unused-argument
"""
This module contains unit tests for the
CustomerUserLogOutPostModelResponse class.
"""
import uuid
from datetime import date, datetime
from decimal import Decimal
from unittest.mock import AsyncMock, patch
import pytest
from business.customer import CustomerBusObj
from flows.customer_user_log_out import FlowCustomerUserLogOut, FlowCustomerUserLogOutResult
from helpers.session_context import SessionContext
from helpers.type_conversion import TypeConversion
from models.factory.customer import CustomerFactory
from ...models.customer_user_log_out import (
    CustomerUserLogOutPostModelResponse,
    CustomerUserLogOutPostModelRequest)
from ..factory.customer_user_log_out import CustomerUserLogOutPostModelRequestFactory
class TestCustomerUserLogOutPostModelRequest:
    def test_default_values(self):
        model = CustomerUserLogOutPostModelRequest()
        assert model.force_error_message == ""
# endset

# endset
    def test_to_dict_snake(self):
        model = CustomerUserLogOutPostModelRequest(
            force_error_message="Test Error",
# endset

# endset
        )
        snake_case_dict = model.to_dict_snake()
        assert snake_case_dict['force_error_message'] == "Test Error"
# endset

# endset
    def test_to_dict_camel(self):
        model = CustomerUserLogOutPostModelRequest(
            force_error_message="Test Error",
# endset

# endset
        )
        camel_case_dict = model.to_dict_camel()
        assert camel_case_dict['forceErrorMessage'] == "Test Error"
# endset

# endset
class TestCustomerUserLogOutPostModelResponse:
    """
    This class contains unit tests for the
    CustomerUserLogOutPostModelResponse class.
    """
    @pytest.mark.asyncio
    async def test_flow_process_request(self, session):
        """
        This method tests the flow process request
        for adding a  to a customer.
        It mocks the process method of FlowCustomerUserLogOut
        and asserts that the response is successful.
        """
        async def mock_process(
            customer_bus_obj: CustomerBusObj,

        ):
            return FlowCustomerUserLogOutResult()
        with patch.object(
            FlowCustomerUserLogOut,
            'process',
            new_callable=AsyncMock
        ) as mock_method:
            mock_method.side_effect = mock_process
            request_instance = await (
                CustomerUserLogOutPostModelRequestFactory
                .create_async(
                    session=session
                )
            )
            response_instance = CustomerUserLogOutPostModelResponse()
            session_context = SessionContext(dict(), session)
            customer = await CustomerFactory.create_async(session)
            await response_instance.process_request(
                session_context=session_context,
                customer_code=customer.code,
                request=request_instance
            )
            assert response_instance.success is True
            mock_method.assert_awaited()

