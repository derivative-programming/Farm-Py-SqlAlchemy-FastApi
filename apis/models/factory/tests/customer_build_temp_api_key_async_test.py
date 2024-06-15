# apis/models/factory/tests/customer_build_temp_api_key_async_test.py
"""
    #TODO add comment
"""
import uuid
from datetime import date, datetime
from decimal import Decimal
import pytest
from ...customer_build_temp_api_key import CustomerBuildTempApiKeyPostModelRequest
from ..customer_build_temp_api_key import CustomerBuildTempApiKeyPostModelRequestFactory
class TestCustomerBuildTempApiKeyPostModelRequestFactoryAsync:
    """
    #TODO add comment
    """
    @pytest.mark.asyncio
    async def test_create_async(self, session):
        """
            #TODO add comment
        """
        model_instance = (
            await CustomerBuildTempApiKeyPostModelRequestFactory.create_async(
                session=session)
        )
        assert isinstance(model_instance, CustomerBuildTempApiKeyPostModelRequest)

