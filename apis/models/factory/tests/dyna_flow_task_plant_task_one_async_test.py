# apis/models/factory/tests/dyna_flow_task_plant_task_one_async_test.py
# pylint: disable=unused-import

"""
This module contains test cases for the
DynaFlowTaskPlantTaskOnePostModelRequestFactoryAsync
class.
"""

import uuid  # noqa: F401
from datetime import date, datetime, timezone  # noqa: F401
from decimal import Decimal  # noqa: F401

import pytest

from ...dyna_flow_task_plant_task_one import (
    DynaFlowTaskPlantTaskOnePostModelRequest)
from ..dyna_flow_task_plant_task_one import (
    DynaFlowTaskPlantTaskOnePostModelRequestFactory)


class TestDynaFlowTaskPlantTaskOnePostModelRequestFactoryAsync:
    """
    This class contains test cases for the
    DynaFlowTaskPlantTaskOnePostModelRequestFactoryAsync
    class.
    """

    @pytest.mark.asyncio
    async def test_create_async(self, session):
        """
        Test the create_async method of
        DynaFlowTaskPlantTaskOnePostModelRequestFactoryAsync
        class.
        """

        model_instance = await \
            DynaFlowTaskPlantTaskOnePostModelRequestFactory \
            .create_async(
                session=session)

        assert isinstance(
            model_instance,
            DynaFlowTaskPlantTaskOnePostModelRequest)
