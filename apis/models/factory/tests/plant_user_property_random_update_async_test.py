# apis/models/factory/tests/plant_user_property_random_update_async_test.py
"""
    #TODO add comment
"""
import uuid
from datetime import date, datetime
from decimal import Decimal
import pytest
from ...plant_user_property_random_update import PlantUserPropertyRandomUpdatePostModelRequest
from ..plant_user_property_random_update import PlantUserPropertyRandomUpdatePostModelRequestFactory
class TestPlantUserPropertyRandomUpdatePostModelRequestFactoryAsync:
    """
    #TODO add comment
    """
    @pytest.mark.asyncio
    async def test_create_async(self, session):
        """
            #TODO add comment
        """
        model_instance = (
            await PlantUserPropertyRandomUpdatePostModelRequestFactory.create_async(
                session=session)
        )
        assert isinstance(model_instance, PlantUserPropertyRandomUpdatePostModelRequest)

