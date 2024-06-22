# apis/models/tests/error_log_config_resolve_error_log_test.py
# pylint: disable=unused-argument
"""
This module contains unit tests for the
ErrorLogConfigResolveErrorLogPostModelResponse class.
"""
import uuid
from datetime import date, datetime
from decimal import Decimal
from unittest.mock import AsyncMock, patch
import pytest
from business.error_log import ErrorLogBusObj
from flows.error_log_config_resolve_error_log import FlowErrorLogConfigResolveErrorLog, FlowErrorLogConfigResolveErrorLogResult
from helpers.session_context import SessionContext
from helpers.type_conversion import TypeConversion
from models.factory.error_log import ErrorLogFactory
from ...models.error_log_config_resolve_error_log import (
    ErrorLogConfigResolveErrorLogPostModelResponse,
    ErrorLogConfigResolveErrorLogPostModelRequest)
from ..factory.error_log_config_resolve_error_log import ErrorLogConfigResolveErrorLogPostModelRequestFactory
class TestErrorLogConfigResolveErrorLogPostModelRequest:
    def test_default_values(self):
        model = ErrorLogConfigResolveErrorLogPostModelRequest()
        assert model.force_error_message == ""
# endset

# endset
    def test_to_dict_snake(self):
        model = ErrorLogConfigResolveErrorLogPostModelRequest(
            force_error_message="Test Error",
# endset

# endset
        )
        snake_case_dict = model.to_dict_snake()
        assert snake_case_dict['force_error_message'] == "Test Error"
# endset

# endset
    def test_to_dict_camel(self):
        model = ErrorLogConfigResolveErrorLogPostModelRequest(
            force_error_message="Test Error",
# endset

# endset
        )
        camel_case_dict = model.to_dict_camel()
        assert camel_case_dict['forceErrorMessage'] == "Test Error"
# endset

# endset
class TestErrorLogConfigResolveErrorLogPostModelResponse:
    """
    This class contains unit tests for the
    ErrorLogConfigResolveErrorLogPostModelResponse class.
    """
    @pytest.mark.asyncio
    async def test_flow_process_request(self, session):
        """
        This method tests the flow process request
        for adding a  to a error_log.
        It mocks the process method of FlowErrorLogConfigResolveErrorLog
        and asserts that the response is successful.
        """
        async def mock_process(
            error_log_bus_obj: ErrorLogBusObj,

        ):
            return FlowErrorLogConfigResolveErrorLogResult()
        with patch.object(
            FlowErrorLogConfigResolveErrorLog,
            'process',
            new_callable=AsyncMock
        ) as mock_method:
            mock_method.side_effect = mock_process
            request_instance = await (
                ErrorLogConfigResolveErrorLogPostModelRequestFactory
                .create_async(
                    session=session
                )
            )
            response_instance = ErrorLogConfigResolveErrorLogPostModelResponse()
            session_context = SessionContext(dict(), session)
            error_log = await ErrorLogFactory.create_async(session)
            await response_instance.process_request(
                session_context=session_context,
                error_log_code=error_log.code,
                request=request_instance
            )
            assert response_instance.success is True
            mock_method.assert_awaited()

