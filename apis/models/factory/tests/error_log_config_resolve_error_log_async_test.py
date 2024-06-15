# apis/models/factory/tests/error_log_config_resolve_error_log_async_test.py
"""
    #TODO add comment
"""
import uuid
from datetime import date, datetime
from decimal import Decimal
import pytest
from ...error_log_config_resolve_error_log import ErrorLogConfigResolveErrorLogPostModelRequest
from ..error_log_config_resolve_error_log import ErrorLogConfigResolveErrorLogPostModelRequestFactory
class TestErrorLogConfigResolveErrorLogPostModelRequestFactoryAsync:
    """
    #TODO add comment
    """
    @pytest.mark.asyncio
    async def test_create_async(self, session):
        """
            #TODO add comment
        """
        model_instance = (
            await ErrorLogConfigResolveErrorLogPostModelRequestFactory.create_async(
                session=session)
        )
        assert isinstance(model_instance, ErrorLogConfigResolveErrorLogPostModelRequest)

