# apis/models/tests/customer_build_temp_api_key_test.py
"""
    #TODO add comment
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
from ...models.customer_build_temp_api_key import (CustomerBuildTempApiKeyPostModelResponse)
from ..factory.customer_build_temp_api_key import CustomerBuildTempApiKeyPostModelRequestFactory
class TestCustomerBuildTempApiKeyPostModelResponse:
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

