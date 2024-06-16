# apis/models/factory/tests/plant_user_details_async_test.py
"""
    #TODO add comment
"""
import uuid
from datetime import date, datetime
from decimal import Decimal
import pytest
from ...plant_user_details import PlantUserDetailsGetModelRequest
from ..plant_user_details import PlantUserDetailsGetModelRequestFactory
class TestPlantUserDetailsGetModelRequestFactoryAsync:
    """
    #TODO add comment
    """
    @pytest.mark.asyncio
    async def test_create_async(self, session):
        """
            #TODO add comment
        """
        model_instance = await (
            PlantUserDetailsGetModelRequestFactory
            .create_async(
                session=session
            )
        )
        assert isinstance(model_instance, PlantUserDetailsGetModelRequest)

        assert isinstance(model_instance.page_number, int)
        assert isinstance(model_instance.item_count_per_page, int)
