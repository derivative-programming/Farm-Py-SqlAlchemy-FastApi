# apis/models/factory/tests/plant_sample_workflow_async_test.py
# pylint: disable=unused-import

"""
This module contains test cases for the
PlantSampleWorkflowPostModelRequestFactoryAsync
class.
"""

import uuid  # noqa: F401
from datetime import date, datetime  # noqa: F401
from decimal import Decimal  # noqa: F401

import pytest

from ...plant_sample_workflow import (
    PlantSampleWorkflowPostModelRequest)
from ..plant_sample_workflow import (
    PlantSampleWorkflowPostModelRequestFactory)


class TestPlantSampleWorkflowPostModelRequestFactoryAsync:
    """
    This class contains test cases for the
    PlantSampleWorkflowPostModelRequestFactoryAsync
    class.
    """

    @pytest.mark.asyncio
    async def test_create_async(self, session):
        """
        Test the create_async method of
        PlantSampleWorkflowPostModelRequestFactoryAsync
        class.
        """

        model_instance = await \
            PlantSampleWorkflowPostModelRequestFactory \
            .create_async(
                session=session)

        assert isinstance(
            model_instance,
            PlantSampleWorkflowPostModelRequest)
