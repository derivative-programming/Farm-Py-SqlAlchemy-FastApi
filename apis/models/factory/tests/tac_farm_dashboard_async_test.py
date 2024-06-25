# apis/models/factory/tests/tac_farm_dashboard_async_test.py
# pylint: disable=unused-import

"""
This module contains test cases for the
TacFarmDashboardGetModelRequestFactoryAsync
class.
"""

import uuid  # noqa: F401
from datetime import date, datetime  # noqa: F401
from decimal import Decimal  # noqa: F401

import pytest

from ...tac_farm_dashboard import (
    TacFarmDashboardGetModelRequest)
from ..tac_farm_dashboard import (
    TacFarmDashboardGetModelRequestFactory)


class TestTacFarmDashboardGetModelRequestFactoryAsync:
    """
    This class contains test cases for the
    TacFarmDashboardGetModelRequestFactoryAsync
    class.
    """

    @pytest.mark.asyncio
    async def test_create_async(self, session):
        """
        Test the create_async method of
        TacFarmDashboardGetModelRequestFactoryAsync
        class.
        """

        model_instance = await (
            TacFarmDashboardGetModelRequestFactory
            .create_async(
                session=session
            )
        )
        assert isinstance(model_instance,
                          TacFarmDashboardGetModelRequest)

