# apis/models/factory/tests/customer_build_temp_api_key_async_test.py
# pylint: disable=unused-import

"""
This module contains test cases for the
CustomerBuildTempApiKeyPostModelRequestFactoryAsync
class.
"""

import uuid  # noqa: F401
from datetime import date, datetime  # noqa: F401
from decimal import Decimal  # noqa: F401

import pytest

from ...customer_build_temp_api_key import (
    CustomerBuildTempApiKeyPostModelRequest)
from ..customer_build_temp_api_key import (
    CustomerBuildTempApiKeyPostModelRequestFactory)


class TestCustomerBuildTempApiKeyPostModelRequestFactoryAsync:
    """
    This class contains test cases for the
    CustomerBuildTempApiKeyPostModelRequestFactoryAsync
    class.
    """

    @pytest.mark.asyncio
    async def test_create_async(self, session):
        """
        Test the create_async method of
        CustomerBuildTempApiKeyPostModelRequestFactoryAsync
        class.
        """

        model_instance = await \
            CustomerBuildTempApiKeyPostModelRequestFactory \
            .create_async(
                session=session)

        assert isinstance(
            model_instance,
            CustomerBuildTempApiKeyPostModelRequest)
