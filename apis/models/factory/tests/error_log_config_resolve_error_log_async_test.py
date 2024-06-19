# apis/models/factory/tests/error_log_config_resolve_error_log_async_test.py
"""
This module contains test cases for the
ErrorLogConfigResolveErrorLogPostModelRequestFactoryAsync class.
"""
import uuid
from datetime import date, datetime
from decimal import Decimal
import pytest
from ...error_log_config_resolve_error_log import ErrorLogConfigResolveErrorLogPostModelRequest
from ..error_log_config_resolve_error_log import ErrorLogConfigResolveErrorLogPostModelRequestFactory
class TestErrorLogConfigResolveErrorLogPostModelRequestFactoryAsync:
    """
    This class contains test cases for the
    ErrorLogConfigResolveErrorLogPostModelRequestFactoryAsync class.
    """
    @pytest.mark.asyncio
    async def test_create_async(self, session):
        """
        Test the create_async method of
        ErrorLogConfigResolveErrorLogPostModelRequestFactoryAsync class.
        """
        model_instance = (
            await ErrorLogConfigResolveErrorLogPostModelRequestFactory.create_async(
                session=session)
        )
        assert isinstance(model_instance, ErrorLogConfigResolveErrorLogPostModelRequest)

