# apis/models/tests/customer_user_log_out_test.py
"""
    #TODO add comment
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
from ...models.customer_user_log_out import (CustomerUserLogOutPostModelResponse)
from ..factory.customer_user_log_out import CustomerUserLogOutPostModelRequestFactory
class TestCustomerUserLogOutPostModelResponse:
    """
    #TODO add comment
    """
    @pytest.mark.asyncio
    async def test_flow_process_request(self, session):
        """
            #TODO add comment
        """
        async def mock_process(
            customer_bus_obj: CustomerBusObj,  # pylint: disable=unused-argument

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

