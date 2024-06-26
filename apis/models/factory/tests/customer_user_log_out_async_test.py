# apis/models/factory/tests/customer_user_log_out_async_test.py
# pylint: disable=unused-import

"""
This module contains test cases for the
CustomerUserLogOutPostModelRequestFactoryAsync
class.
"""

import uuid  # noqa: F401
from datetime import date, datetime  # noqa: F401
from decimal import Decimal  # noqa: F401

import pytest

from ...customer_user_log_out import (
    CustomerUserLogOutPostModelRequest)
from ..customer_user_log_out import (
    CustomerUserLogOutPostModelRequestFactory)


class TestCustomerUserLogOutPostModelRequestFactoryAsync:
    """
    This class contains test cases for the
    CustomerUserLogOutPostModelRequestFactoryAsync
    class.
    """

    @pytest.mark.asyncio
    async def test_create_async(self, session):
        """
        Test the create_async method of
        CustomerUserLogOutPostModelRequestFactoryAsync
        class.
        """

        model_instance = await \
            CustomerUserLogOutPostModelRequestFactory \
            .create_async(
                session=session)

        assert isinstance(
            model_instance,
            CustomerUserLogOutPostModelRequest)
