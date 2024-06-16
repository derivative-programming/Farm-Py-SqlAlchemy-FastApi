# apis/models/tests/plant_user_details_test.py
"""
    #TODO add comment
"""
import uuid
from datetime import date, datetime
from decimal import Decimal
import pytest
from ..factory.plant_user_details import PlantUserDetailsGetModelRequestFactory
from ..plant_user_details import PlantUserDetailsGetModelRequest
class PlantUserDetailsGetModelRequestFactoryAsync:
    """
    #TODO add comment
    """
    @pytest.mark.asyncio
    async def test_report_generation(self, session):
        """
            #TODO add comment
        """
        model_instance = await (
            PlantUserDetailsGetModelRequestFactory
            .create_async(session=session)
        )
        assert isinstance(model_instance, PlantUserDetailsGetModelRequest)

        assert isinstance(model_instance.page_number, int)
        assert isinstance(model_instance.item_count_per_page, int)
