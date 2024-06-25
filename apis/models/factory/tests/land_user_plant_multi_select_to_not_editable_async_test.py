# apis/models/factory/tests/land_user_plant_multi_select_to_not_editable_async_test.py
# pylint: disable=unused-import

"""
This module contains test cases for the
LandUserPlantMultiSelectToNotEditablePostModelRequestFactoryAsync
class.
"""

import uuid  # noqa: F401
from datetime import date, datetime  # noqa: F401
from decimal import Decimal  # noqa: F401

import pytest

from ...land_user_plant_multi_select_to_not_editable import (
    LandUserPlantMultiSelectToNotEditablePostModelRequest)
from ..land_user_plant_multi_select_to_not_editable import (
    LandUserPlantMultiSelectToNotEditablePostModelRequestFactory)


class TestLandUserPlantMultiSelectToNotEditablePostModelRequestFactoryAsync:
    """
    This class contains test cases for the
    LandUserPlantMultiSelectToNotEditablePostModelRequestFactoryAsync
    class.
    """

    @pytest.mark.asyncio
    async def test_create_async(self, session):
        """
        Test the create_async method of
        LandUserPlantMultiSelectToNotEditablePostModelRequestFactoryAsync
        class.
        """

        model_instance = (
            await LandUserPlantMultiSelectToNotEditablePostModelRequestFactory.create_async(
                session=session)
        )
        assert isinstance(model_instance,
                          LandUserPlantMultiSelectToNotEditablePostModelRequest)
        assert isinstance(model_instance.plant_code_list_csv,
                          str)

