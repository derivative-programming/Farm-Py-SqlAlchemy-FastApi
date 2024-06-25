# apis/models/factory/tests/customer_user_log_out_async_test.py

"""
This module contains test cases for the
CustomerUserLogOutPostModelRequestFactoryAsync class.
"""

import uuid
from datetime import date, datetime
from decimal import Decimal

import pytest

from ...customer_user_log_out import (
    CustomerUserLogOutPostModelRequest)
from ..customer_user_log_out import (
    CustomerUserLogOutPostModelRequestFactory)


class TestCustomerUserLogOutPostModelRequestFactoryAsync:
    """
    This class contains test cases for the
    CustomerUserLogOutPostModelRequestFactoryAsync class.
    """

    @pytest.mark.asyncio
    async def test_create_async(self, session):
        """
        Test the create_async method of
        CustomerUserLogOutPostModelRequestFactoryAsync class.
        """

        model_instance = (
            await CustomerUserLogOutPostModelRequestFactory.create_async(
                session=session)
        )
        assert isinstance(model_instance,
                          CustomerUserLogOutPostModelRequest)

