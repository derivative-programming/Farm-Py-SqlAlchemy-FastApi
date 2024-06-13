# apis/models/tests/customer_user_log_out_test.py
"""
    #TODO add comment
"""
import asyncio
from decimal import Decimal
import uuid
import pytest
import pytest_asyncio
import time
from typing import AsyncGenerator
from datetime import datetime, date
from sqlalchemy import event
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from business.customer import CustomerBusObj
from flows.base.flow_validation_error import FlowValidationError
from flows.customer_user_log_out import FlowCustomerUserLogOut, FlowCustomerUserLogOutResult
from helpers.session_context import SessionContext
from helpers.type_conversion import TypeConversion
from models.factory.customer import CustomerFactory
from ...models.customer_user_log_out import CustomerUserLogOutPostModelRequest, CustomerUserLogOutPostModelResponse
from models import Base
from ..factory.customer_user_log_out import CustomerUserLogOutPostModelRequestFactory
from sqlalchemy import String
from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select
from pydantic import Field, UUID4
import flows.constants.error_log_config_resolve_error_log as FlowConstants
from unittest.mock import patch, AsyncMock
class TestCustomerUserLogOutPostModelResponse:
    """
    #TODO add comment
    """
    @pytest.mark.asyncio
    async def test_flow_process_request(self, session):
        async def mock_process(
            customer_bus_obj: CustomerBusObj,

        ):
            return FlowCustomerUserLogOutResult()
        with patch.object(FlowCustomerUserLogOut, 'process', new_callable=AsyncMock) as mock_method:
            mock_method.side_effect = mock_process
            request_instance = await CustomerUserLogOutPostModelRequestFactory.create_async(session=session)
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

