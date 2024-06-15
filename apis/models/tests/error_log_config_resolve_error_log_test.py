# apis/models/tests/error_log_config_resolve_error_log_test.py
"""
    #TODO add comment
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
from ...models.error_log_config_resolve_error_log import (ErrorLogConfigResolveErrorLogPostModelResponse)
from ..factory.error_log_config_resolve_error_log import ErrorLogConfigResolveErrorLogPostModelRequestFactory
class TestErrorLogConfigResolveErrorLogPostModelResponse:
    """
    #TODO add comment
    """
    @pytest.mark.asyncio
    async def test_flow_process_request(self, session):
        """
            #TODO add comment
        """
        async def mock_process(
            error_log_bus_obj: ErrorLogBusObj,  # pylint: disable=unused-argument

        ):
            return FlowErrorLogConfigResolveErrorLogResult()
        with patch.object(FlowErrorLogConfigResolveErrorLog, 'process', new_callable=AsyncMock) as mock_method:
            mock_method.side_effect = mock_process
            request_instance = await ErrorLogConfigResolveErrorLogPostModelRequestFactory.create_async(session=session)
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

