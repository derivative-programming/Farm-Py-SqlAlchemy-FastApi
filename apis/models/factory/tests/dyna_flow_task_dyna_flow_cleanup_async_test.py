# apis/models/factory/tests/dyna_flow_task_dyna_flow_cleanup_async_test.py
# pylint: disable=unused-import

"""
This module contains test cases for the
DynaFlowTaskDynaFlowCleanupPostModelRequestFactoryAsync
class.
"""

import uuid  # noqa: F401
from datetime import date, datetime  # noqa: F401
from decimal import Decimal  # noqa: F401

import pytest

from ...dyna_flow_task_dyna_flow_cleanup import (
    DynaFlowTaskDynaFlowCleanupPostModelRequest)
from ..dyna_flow_task_dyna_flow_cleanup import (
    DynaFlowTaskDynaFlowCleanupPostModelRequestFactory)


class TestDynaFlowTaskDynaFlowCleanupPostModelRequestFactoryAsync:
    """
    This class contains test cases for the
    DynaFlowTaskDynaFlowCleanupPostModelRequestFactoryAsync
    class.
    """

    @pytest.mark.asyncio
    async def test_create_async(self, session):
        """
        Test the create_async method of
        DynaFlowTaskDynaFlowCleanupPostModelRequestFactoryAsync
        class.
        """

        model_instance = await \
            DynaFlowTaskDynaFlowCleanupPostModelRequestFactory \
            .create_async(
                session=session)

        assert isinstance(
            model_instance,
            DynaFlowTaskDynaFlowCleanupPostModelRequest)
