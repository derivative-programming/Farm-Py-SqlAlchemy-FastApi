# apis/models/factory/tests/plant_user_delete_async_test.py
"""
    #TODO add comment
"""
import uuid
from datetime import date, datetime
from decimal import Decimal
import pytest
from ...plant_user_delete import PlantUserDeletePostModelRequest
from ..plant_user_delete import PlantUserDeletePostModelRequestFactory
class TestPlantUserDeletePostModelRequestFactoryAsync:
    """
    #TODO add comment
    """
    @pytest.mark.asyncio
    async def test_create_async(self, session):
        """
            #TODO add comment
        """
        model_instance = (
            await PlantUserDeletePostModelRequestFactory.create_async(
                session=session)
        )
        assert isinstance(model_instance, PlantUserDeletePostModelRequest)

