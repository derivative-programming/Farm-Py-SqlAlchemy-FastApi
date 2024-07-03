# apis/models/factory/tests/process_all_dyna_flow_type_schedule_task_async_test.py
# pylint: disable=unused-import

"""
This module contains test cases for the
ProcessAllDynaFlowTypeScheduleTaskPostModelRequestFactoryAsync
class.
"""

import uuid  # noqa: F401
from datetime import date, datetime, timezone  # noqa: F401
from decimal import Decimal  # noqa: F401

import pytest

from ...process_all_dyna_flow_type_schedule_task import (
    ProcessAllDynaFlowTypeScheduleTaskPostModelRequest)
from ..process_all_dyna_flow_type_schedule_task import (
    ProcessAllDynaFlowTypeScheduleTaskPostModelRequestFactory)


class TestProcessAllDynaFlowTypeScheduleTaskPostModelRequestFactoryAsync:
    """
    This class contains test cases for the
    ProcessAllDynaFlowTypeScheduleTaskPostModelRequestFactoryAsync
    class.
    """

    @pytest.mark.asyncio
    async def test_create_async(self, session):
        """
        Test the create_async method of
        ProcessAllDynaFlowTypeScheduleTaskPostModelRequestFactoryAsync
        class.
        """

        model_instance = await \
            ProcessAllDynaFlowTypeScheduleTaskPostModelRequestFactory \
            .create_async(
                session=session)

        assert isinstance(
            model_instance,
            ProcessAllDynaFlowTypeScheduleTaskPostModelRequest)
