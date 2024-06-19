# apis/models/tests/tac_farm_dashboard_test.py
"""
This module contains unit tests for the
TacFarmDashboardGetModelRequestFactoryAsync class.
"""
import uuid
from datetime import date, datetime
from decimal import Decimal
import pytest
from ..factory.tac_farm_dashboard import TacFarmDashboardGetModelRequestFactory
from ..tac_farm_dashboard import TacFarmDashboardGetModelRequest
class TacFarmDashboardGetModelRequestFactoryAsync:
    """
    This class contains asynchronous unit tests for the
    TacFarmDashboardGetModelRequestFactory class.
    """
    @pytest.mark.asyncio
    async def test_report_generation(self, session):
        """
        Test the generation of a report using the
        TacFarmDashboardGetModelRequestFactory class.
        Args:
            session: The database session.
        Returns:
            None
        Raises:
            AssertionError: If any of the assertions fail.
        """
        model_instance = await (
            TacFarmDashboardGetModelRequestFactory
            .create_async(session=session)
        )
        assert isinstance(model_instance, TacFarmDashboardGetModelRequest)

        assert isinstance(model_instance.page_number, int)
        assert isinstance(model_instance.item_count_per_page, int)
