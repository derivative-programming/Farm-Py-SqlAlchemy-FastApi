# apis/models/factory/tests/plant_user_delete_async_test.py
# pylint: disable=unused-import, too-many-public-methods

"""
This module contains test cases for the
PlantUserDeletePostModelRequestFactoryAsync
class.
"""

import uuid  # noqa: F401
from datetime import date, datetime, timezone  # noqa: F401
from decimal import Decimal  # noqa: F401

import pytest

from ...plant_user_delete import (
    PlantUserDeletePostModelRequest)
from ..plant_user_delete import (
    PlantUserDeletePostModelRequestFactory)


class TestPlantUserDeletePostModelRequestFactoryAsync:  # pylint: disable=too-few-public-methods
    """
    This class contains test cases for the
    PlantUserDeletePostModelRequestFactoryAsync
    class.
    """

    @pytest.mark.asyncio
    async def test_create_async(self, session):
        """
        Test the create_async method of
        PlantUserDeletePostModelRequestFactoryAsync
        class.
        """

        model_instance = await \
            PlantUserDeletePostModelRequestFactory \
            .create_async(
                session=session)

        assert isinstance(
            model_instance,
            PlantUserDeletePostModelRequest)
