# apis/models/factory/tests/plant_user_property_random_update_async_test.py
# pylint: disable=unused-import, too-many-public-methods

"""
This module contains test cases for the
PlantUserPropertyRandomUpdatePostModelRequestFactoryAsync
class.
"""

import uuid  # noqa: F401
from datetime import date, datetime, timezone  # noqa: F401
from decimal import Decimal  # noqa: F401

import pytest

from ...plant_user_property_random_update import (
    PlantUserPropertyRandomUpdatePostModelRequest)
from ..plant_user_property_random_update import (
    PlantUserPropertyRandomUpdatePostModelRequestFactory)


class TestPlantUserPropertyRandomUpdatePostModelRequestFactoryAsync:  # pylint: disable=too-few-public-methods
    """
    This class contains test cases for the
    PlantUserPropertyRandomUpdatePostModelRequestFactoryAsync
    class.
    """

    @pytest.mark.asyncio
    async def test_create_async(self, session):
        """
        Test the create_async method of
        PlantUserPropertyRandomUpdatePostModelRequestFactoryAsync
        class.
        """

        model_instance = await \
            PlantUserPropertyRandomUpdatePostModelRequestFactory \
            .create_async(
                session=session)

        assert isinstance(
            model_instance,
            PlantUserPropertyRandomUpdatePostModelRequest)
