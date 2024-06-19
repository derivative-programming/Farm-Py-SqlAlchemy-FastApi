# apis/models/tests/plant_user_details_test.py
"""
This module contains unit tests for the
PlantUserDetailsGetModelRequestFactoryAsync class.
"""
import uuid
from datetime import date, datetime
from decimal import Decimal
import pytest
from ..factory.plant_user_details import PlantUserDetailsGetModelRequestFactory
from ..plant_user_details import PlantUserDetailsGetModelRequest
class PlantUserDetailsGetModelRequestFactoryAsync:
    """
    This class contains asynchronous unit tests for the
    PlantUserDetailsGetModelRequestFactory class.
    """
    @pytest.mark.asyncio
    async def test_report_generation(self, session):
        """
        Test the generation of a report using the
        PlantUserDetailsGetModelRequestFactory class.
        Args:
            session: The database session.
        Returns:
            None
        Raises:
            AssertionError: If any of the assertions fail.
        """
        model_instance = await (
            PlantUserDetailsGetModelRequestFactory
            .create_async(session=session)
        )
        assert isinstance(model_instance, PlantUserDetailsGetModelRequest)

        assert isinstance(model_instance.page_number, int)
        assert isinstance(model_instance.item_count_per_page, int)
