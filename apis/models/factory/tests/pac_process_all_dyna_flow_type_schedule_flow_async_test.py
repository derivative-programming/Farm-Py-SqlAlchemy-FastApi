# apis/models/factory/tests/pac_process_all_dyna_flow_type_schedule_flow_async_test.py
# pylint: disable=unused-import

"""
This module contains test cases for the
PacProcessAllDynaFlowTypeScheduleFlowPostModelRequestFactoryAsync
class.
"""

import uuid  # noqa: F401
from datetime import date, datetime  # noqa: F401
from decimal import Decimal  # noqa: F401

import pytest

from ...pac_process_all_dyna_flow_type_schedule_flow import (
    PacProcessAllDynaFlowTypeScheduleFlowPostModelRequest)
from ..pac_process_all_dyna_flow_type_schedule_flow import (
    PacProcessAllDynaFlowTypeScheduleFlowPostModelRequestFactory)


class TestPacProcessAllDynaFlowTypeScheduleFlowPostModelRequestFactoryAsync:
    """
    This class contains test cases for the
    PacProcessAllDynaFlowTypeScheduleFlowPostModelRequestFactoryAsync
    class.
    """

    @pytest.mark.asyncio
    async def test_create_async(self, session):
        """
        Test the create_async method of
        PacProcessAllDynaFlowTypeScheduleFlowPostModelRequestFactoryAsync
        class.
        """

        model_instance = await \
            PacProcessAllDynaFlowTypeScheduleFlowPostModelRequestFactory \
            .create_async(
                session=session)

        assert isinstance(
            model_instance,
            PacProcessAllDynaFlowTypeScheduleFlowPostModelRequest)
