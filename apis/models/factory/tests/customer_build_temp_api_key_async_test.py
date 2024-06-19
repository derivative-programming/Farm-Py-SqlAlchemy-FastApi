# apis/models/factory/tests/customer_build_temp_api_key_async_test.py
"""
This module contains test cases for the
CustomerBuildTempApiKeyPostModelRequestFactoryAsync class.
"""
import uuid
from datetime import date, datetime
from decimal import Decimal
import pytest
from ...customer_build_temp_api_key import CustomerBuildTempApiKeyPostModelRequest
from ..customer_build_temp_api_key import CustomerBuildTempApiKeyPostModelRequestFactory
class TestCustomerBuildTempApiKeyPostModelRequestFactoryAsync:
    """
    This class contains test cases for the
    CustomerBuildTempApiKeyPostModelRequestFactoryAsync class.
    """
    @pytest.mark.asyncio
    async def test_create_async(self, session):
        """
        Test the create_async method of
        CustomerBuildTempApiKeyPostModelRequestFactoryAsync class.
        """
        model_instance = (
            await CustomerBuildTempApiKeyPostModelRequestFactory.create_async(
                session=session)
        )
        assert isinstance(model_instance, CustomerBuildTempApiKeyPostModelRequest)

