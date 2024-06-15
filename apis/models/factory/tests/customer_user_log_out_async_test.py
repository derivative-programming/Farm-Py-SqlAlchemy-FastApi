# apis/models/factory/tests/customer_user_log_out_async_test.py
"""
    #TODO add comment
"""
import uuid
from datetime import date, datetime
from decimal import Decimal
import pytest
from ...customer_user_log_out import CustomerUserLogOutPostModelRequest
from ..customer_user_log_out import CustomerUserLogOutPostModelRequestFactory
class TestCustomerUserLogOutPostModelRequestFactoryAsync:
    """
    #TODO add comment
    """
    @pytest.mark.asyncio
    async def test_create_async(self, session):
        """
            #TODO add comment
        """
        model_instance = (
            await CustomerUserLogOutPostModelRequestFactory.create_async(
                session=session)
        )
        assert isinstance(model_instance, CustomerUserLogOutPostModelRequest)

