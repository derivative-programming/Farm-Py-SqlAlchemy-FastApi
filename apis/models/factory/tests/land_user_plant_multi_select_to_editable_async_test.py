# apis/models/factory/tests/land_user_plant_multi_select_to_editable_async_test.py

"""
This module contains test cases for the
LandUserPlantMultiSelectToEditablePostModelRequestFactoryAsync class.
"""

import uuid
from datetime import date, datetime
from decimal import Decimal

import pytest

from ...land_user_plant_multi_select_to_editable import (
    LandUserPlantMultiSelectToEditablePostModelRequest)
from ..land_user_plant_multi_select_to_editable import (
    LandUserPlantMultiSelectToEditablePostModelRequestFactory)


class TestLandUserPlantMultiSelectToEditablePostModelRequestFactoryAsync:
    """
    This class contains test cases for the
    LandUserPlantMultiSelectToEditablePostModelRequestFactoryAsync class.
    """

    @pytest.mark.asyncio
    async def test_create_async(self, session):
        """
        Test the create_async method of
        LandUserPlantMultiSelectToEditablePostModelRequestFactoryAsync class.
        """

        model_instance = (
            await LandUserPlantMultiSelectToEditablePostModelRequestFactory.create_async(
                session=session)
        )
        assert isinstance(model_instance,
                          LandUserPlantMultiSelectToEditablePostModelRequest)
        assert isinstance(model_instance.plant_code_list_csv,
                          str)

