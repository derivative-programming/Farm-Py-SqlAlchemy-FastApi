# apis/models/factory/tests/tac_farm_dashboard_async_test.py

"""
This module contains test cases for the
TacFarmDashboardGetModelRequestFactoryAsync class.
"""

import uuid
from datetime import date, datetime
from decimal import Decimal

import pytest

from ...tac_farm_dashboard import TacFarmDashboardGetModelRequest
from ..tac_farm_dashboard import TacFarmDashboardGetModelRequestFactory


class TestTacFarmDashboardGetModelRequestFactoryAsync:
    """
    This class contains test cases for the
    TacFarmDashboardGetModelRequestFactoryAsync class.
    """

    @pytest.mark.asyncio
    async def test_create_async(self, session):
        """
        Test the create_async method of
        TacFarmDashboardGetModelRequestFactoryAsync class.
        """

        model_instance = await (
            TacFarmDashboardGetModelRequestFactory
            .create_async(
                session=session
            )
        )
        assert isinstance(model_instance, TacFarmDashboardGetModelRequest)

        assert isinstance(model_instance.page_number, int)
        assert isinstance(model_instance.item_count_per_page, int)

