# apis/models/factory/tests/plant_user_details_async_test.py
# pylint: disable=unused-import, too-many-public-methods

"""
This module contains test cases for the
PlantUserDetailsGetModelRequestFactoryAsync
class.
"""

import uuid  # noqa: F401
from datetime import date, datetime, timezone  # noqa: F401
from decimal import Decimal  # noqa: F401

import pytest

from ...plant_user_details import (
    PlantUserDetailsGetModelRequest)
from ..plant_user_details import (
    PlantUserDetailsGetModelRequestFactory)


class TestPlantUserDetailsGetModelRequestFactoryAsync:  # pylint: disable=too-few-public-methods
    """
    This class contains test cases for the
    PlantUserDetailsGetModelRequestFactoryAsync
    class.
    """

    @pytest.mark.asyncio
    async def test_create_async(self, session):
        """
        Test the create_async method of
        PlantUserDetailsGetModelRequestFactoryAsync
        class.
        """

        model_instance = await (
            PlantUserDetailsGetModelRequestFactory
            .create_async(
                session=session
            )
        )
        assert isinstance(
            model_instance,
            PlantUserDetailsGetModelRequest)
