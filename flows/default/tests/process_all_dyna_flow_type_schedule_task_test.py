# flows/default/tests/process_all_dyna_flow_type_schedule_task_test.py
# pylint: disable=unused-import

"""
This module contains unit tests for the
`FlowProcessAllDynaFlowTypeScheduleTaskResult` and
`FlowProcessAllDynaFlowTypeScheduleTask` classes.
"""

import json
import uuid  # noqa: F401
from datetime import date, datetime  # noqa: F401
from decimal import Decimal  # noqa: F401

import pytest

import flows.constants.error_log_config_resolve_error_log as FlowConstants
from business.dyna_flow_task import DynaFlowTaskBusObj
from flows.base.flow_validation_error import FlowValidationError
from flows.process_all_dyna_flow_type_schedule_task import (
    FlowProcessAllDynaFlowTypeScheduleTask,
    FlowProcessAllDynaFlowTypeScheduleTaskResult)
from helpers.session_context import SessionContext
from helpers.type_conversion import TypeConversion  # noqa: F401
from models.factory.dyna_flow_task import (
    DynaFlowTaskFactory)


class TestProcessAllDynaFlowTypeScheduleTaskPostModelResponse:
    """
    This class contains unit tests for the
    `FlowProcessAllDynaFlowTypeScheduleTaskResult` class.
    """

    def test_flow_result_to_json(self):
        """
        Test the `to_json` method of the
        `FlowProcessAllDynaFlowTypeScheduleTaskResult` class.
        """

        # Create an instance and set attributes
        result = FlowProcessAllDynaFlowTypeScheduleTaskResult()
        result.context_object_code = uuid.uuid4()


        # Call to_json method
        json_output = result.to_json()

        # Parse JSON output
        data = json.loads(json_output)

        # Assert individual fields
        assert data["context_object_code"] == (
            str(result.context_object_code))


    @pytest.mark.asyncio
    async def test_flow_process_request(self, session):
        """
        Test the `process` method of the
        `FlowProcessAllDynaFlowTypeScheduleTask` class.
        """

        session_context = SessionContext(dict(), session)
        flow = FlowProcessAllDynaFlowTypeScheduleTask(
            session_context)

        dyna_flow_task = await \
            DynaFlowTaskFactory.create_async(
                session)

        dyna_flow_task_bus_obj = DynaFlowTaskBusObj(session_context)
        dyna_flow_task_bus_obj.load_from_obj_instance(dyna_flow_task)

        role_required = ""


        if len(role_required) > 0:
            with pytest.raises(FlowValidationError):
                await flow.process(
                    dyna_flow_task_bus_obj,

# endset  # noqa: E122
                )

        session_context.role_name_csv = role_required

        customer_code_match_required = False
        if FlowConstants.CALCULATED_IS_ROW_LEVEL_CUSTOMER_SECURITY_USED \
                is True:
            customer_code_match_required = True
        if FlowConstants.CALCULATED_IS_ROW_LEVEL_ORGANIZATION_SECURITY_USED \
                is True:
            customer_code_match_required = True
        if FlowConstants.CALCULATED_IS_ROW_LEVEL_ORG_CUSTOMER_SECURITY_USED \
                is True:
            customer_code_match_required = True

        if customer_code_match_required is True:
            with pytest.raises(FlowValidationError):

                await flow.process(
                    dyna_flow_task_bus_obj,

# endset  # noqa: E122
                )

        session_context.role_name_csv = role_required

        # result = await response_instance.process_request(
        #     session=session,
        #     session_context=session_context,
        #     dyna_flow_task_code=dyna_flow_task.code,
        #     request=request_instance
        #     )
        # assert isinstance(result,FlowProcessAllDynaFlowTypeScheduleTaskResult)
