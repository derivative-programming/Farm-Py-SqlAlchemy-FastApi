# apis/models/factory/tests/plant_user_property_random_update_async_test.py

"""
This module contains test cases for the
PlantUserPropertyRandomUpdatePostModelRequestFactoryAsync class.
"""

import uuid
from datetime import date, datetime
from decimal import Decimal

import pytest

from ...plant_user_property_random_update import PlantUserPropertyRandomUpdatePostModelRequest
from ..plant_user_property_random_update import PlantUserPropertyRandomUpdatePostModelRequestFactory


class TestPlantUserPropertyRandomUpdatePostModelRequestFactoryAsync:
    """
    This class contains test cases for the
    PlantUserPropertyRandomUpdatePostModelRequestFactoryAsync class.
    """

    @pytest.mark.asyncio
    async def test_create_async(self, session):
        """
        Test the create_async method of
        PlantUserPropertyRandomUpdatePostModelRequestFactoryAsync class.
        """

        model_instance = (
            await PlantUserPropertyRandomUpdatePostModelRequestFactory.create_async(
                session=session)
        )
        assert isinstance(model_instance, PlantUserPropertyRandomUpdatePostModelRequest)

