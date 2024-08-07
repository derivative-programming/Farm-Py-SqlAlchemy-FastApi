# apis/models/factory/tests/land_user_plant_multi_select_to_editable_async_test.py
# pylint: disable=unused-import, too-many-public-methods

"""
This module contains test cases for the
LandUserPlantMultiSelectToEditablePostModelRequestFactoryAsync
class.
"""

import uuid  # noqa: F401
from datetime import date, datetime, timezone  # noqa: F401
from decimal import Decimal  # noqa: F401

import pytest

from ...land_user_plant_multi_select_to_editable import (
    LandUserPlantMultiSelectToEditablePostModelRequest)
from ..land_user_plant_multi_select_to_editable import (
    LandUserPlantMultiSelectToEditablePostModelRequestFactory)


class TestLandUserPlantMultiSelectToEditablePostModelRequestFactoryAsync:  # pylint: disable=too-few-public-methods
    """
    This class contains test cases for the
    LandUserPlantMultiSelectToEditablePostModelRequestFactoryAsync
    class.
    """

    @pytest.mark.asyncio
    async def test_create_async(self, session):
        """
        Test the create_async method of
        LandUserPlantMultiSelectToEditablePostModelRequestFactoryAsync
        class.
        """

        model_instance = await \
            LandUserPlantMultiSelectToEditablePostModelRequestFactory \
            .create_async(
                session=session)

        assert isinstance(
            model_instance,
            LandUserPlantMultiSelectToEditablePostModelRequest)
        assert isinstance(model_instance.plant_code_list_csv,
                          str)
