# apis/models/factory/tests/dyna_flow_task_plant_task_two_async_test.py
# pylint: disable=unused-import, too-many-public-methods

"""
This module contains test cases for the
DynaFlowTaskPlantTaskTwoPostModelRequestFactoryAsync
class.
"""

import uuid  # noqa: F401
from datetime import date, datetime, timezone  # noqa: F401
from decimal import Decimal  # noqa: F401

import pytest

from ...dyna_flow_task_plant_task_two import (
    DynaFlowTaskPlantTaskTwoPostModelRequest)
from ..dyna_flow_task_plant_task_two import (
    DynaFlowTaskPlantTaskTwoPostModelRequestFactory)


class TestDynaFlowTaskPlantTaskTwoPostModelRequestFactoryAsync:  # pylint: disable=too-few-public-methods
    """
    This class contains test cases for the
    DynaFlowTaskPlantTaskTwoPostModelRequestFactoryAsync
    class.
    """

    @pytest.mark.asyncio
    async def test_create_async(self, session):
        """
        Test the create_async method of
        DynaFlowTaskPlantTaskTwoPostModelRequestFactoryAsync
        class.
        """

        model_instance = await \
            DynaFlowTaskPlantTaskTwoPostModelRequestFactory \
            .create_async(
                session=session)

        assert isinstance(
            model_instance,
            DynaFlowTaskPlantTaskTwoPostModelRequest)
