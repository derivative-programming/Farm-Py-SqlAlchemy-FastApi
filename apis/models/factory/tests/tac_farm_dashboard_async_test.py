# apis/models/factory/tests/tac_farm_dashboard_async_test.py
"""
    #TODO add comment
"""
import uuid
from datetime import date, datetime
from decimal import Decimal
import pytest
from ...tac_farm_dashboard import TacFarmDashboardGetModelRequest
from ..tac_farm_dashboard import TacFarmDashboardGetModelRequestFactory
class TestTacFarmDashboardGetModelRequestFactoryAsync:
    """
    #TODO add comment
    """
    @pytest.mark.asyncio
    async def test_create_async(self, session):
        """
            #TODO add comment
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
