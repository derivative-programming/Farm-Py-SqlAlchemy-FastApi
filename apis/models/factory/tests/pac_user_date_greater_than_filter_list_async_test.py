# apis/models/factory/tests/pac_user_date_greater_than_filter_list_async_test.py
# pylint: disable=unused-import

"""
This module contains test cases for the
PacUserDateGreaterThanFilterListGetModelRequestFactoryAsync
class.
"""

import uuid  # noqa: F401
from datetime import date, datetime, timezone  # noqa: F401
from decimal import Decimal  # noqa: F401

import pytest

from ...pac_user_date_greater_than_filter_list import (
    PacUserDateGreaterThanFilterListGetModelRequest)
from ..pac_user_date_greater_than_filter_list import (
    PacUserDateGreaterThanFilterListGetModelRequestFactory)


class TestPacUserDateGreaterThanFilterListGetModelRequestFactoryAsync:
    """
    This class contains test cases for the
    PacUserDateGreaterThanFilterListGetModelRequestFactoryAsync
    class.
    """

    @pytest.mark.asyncio
    async def test_create_async(self, session):
        """
        Test the create_async method of
        PacUserDateGreaterThanFilterListGetModelRequestFactoryAsync
        class.
        """

        model_instance = await (
            PacUserDateGreaterThanFilterListGetModelRequestFactory
            .create_async(
                session=session
            )
        )
        assert isinstance(
            model_instance,
            PacUserDateGreaterThanFilterListGetModelRequest)
