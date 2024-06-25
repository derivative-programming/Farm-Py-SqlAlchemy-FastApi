# apis/models/factory/tests/plant_user_details_async_test.py

"""
This module contains test cases for the
PlantUserDetailsGetModelRequestFactoryAsync class.
"""

import uuid
from datetime import date, datetime
from decimal import Decimal

import pytest

from ...plant_user_details import (
    PlantUserDetailsGetModelRequest)
from ..plant_user_details import (
    PlantUserDetailsGetModelRequestFactory)


class TestPlantUserDetailsGetModelRequestFactoryAsync:
    """
    This class contains test cases for the
    PlantUserDetailsGetModelRequestFactoryAsync class.
    """

    @pytest.mark.asyncio
    async def test_create_async(self, session):
        """
        Test the create_async method of
        PlantUserDetailsGetModelRequestFactoryAsync class.
        """

        model_instance = await (
            PlantUserDetailsGetModelRequestFactory
            .create_async(
                session=session
            )
        )
        assert isinstance(model_instance,
                          PlantUserDetailsGetModelRequest)

        assert isinstance(model_instance.page_number, int)
        assert isinstance(model_instance.item_count_per_page, int)

