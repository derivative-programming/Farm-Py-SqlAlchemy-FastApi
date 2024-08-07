# flows/default/process_all_dyna_flow_type_schedule_task.py  # pylint: disable=duplicate-code # noqa: E501
# pylint: disable=unused-import
# pylint: disable=too-few-public-methods
"""
This module contains the
FlowProcessAllDynaFlowTypeScheduleTask class
and related classes
that handle the addition of a
 to a specific
dyna_flow_task in the flow process.
"""

import json
import uuid  # noqa: F401
from datetime import date, datetime, timezone  # noqa: F401
from decimal import Decimal  # noqa: F401

from business.dyna_flow_task import DynaFlowTaskBusObj
from flows.base import LogSeverity
from flows.base.process_all_dyna_flow_type_schedule_task import \
    BaseFlowProcessAllDynaFlowTypeScheduleTask
from helpers import SessionContext  # noqa: F401
from helpers import TypeConversion  # noqa: F401


class FlowProcessAllDynaFlowTypeScheduleTaskResult():
    """
    Represents the result of the
    FlowProcessAllDynaFlowTypeScheduleTask process.
    """

    context_object_code: uuid.UUID = uuid.UUID(int=0)

    def __init__(self):
        """
        Initializes a new instance of the
        FlowProcessAllDynaFlowTypeScheduleTaskResult class.
        """

    def to_json(self):
        """
        Converts the FlowProcessAllDynaFlowTypeScheduleTaskResult
        instance to a JSON string.

        Returns:
            str: The JSON representation of the instance.
        """
        # Create a dictionary representation of the instance
        data = {
            'context_object_code':
                str(self.context_object_code),

# endset  # noqa: E122
        }
        # Serialize the dictionary to JSON
        return json.dumps(data)


class FlowProcessAllDynaFlowTypeScheduleTask(
    BaseFlowProcessAllDynaFlowTypeScheduleTask
):
    """
    FlowProcessAllDynaFlowTypeScheduleTask handles the addition of
    a  to
    a specific dyna_flow_task in the flow process.

    This class extends the
    BaseFlowProcessAllDynaFlowTypeScheduleTaskclass and
    initializes it with the provided session context.
    """

    async def process(
        self,
        dyna_flow_task_bus_obj: DynaFlowTaskBusObj,

# endset  # noqa: E122
    ) -> FlowProcessAllDynaFlowTypeScheduleTaskResult:
        """
        Processes the addition of a
         to a specific dyna_flow_task.

        Returns:
            FlowProcessAllDynaFlowTypeScheduleTaskResult:
                The result of the
                FlowProcessAllDynaFlowTypeScheduleTask process.
        """
        super()._log_message_and_severity(
            LogSeverity.INFORMATION_HIGH_DETAIL,
            "Start"
        )
        super()._log_message_and_severity(
            LogSeverity.INFORMATION_HIGH_DETAIL,
            "Code::" + str(dyna_flow_task_bus_obj.code)
        )
        await super()._process_validation_rules(
            dyna_flow_task_bus_obj,

# endset  # noqa: E122
        )
        super()._throw_queued_validation_errors()

        # TODO: add flow logic


        super()._log_message_and_severity(
            LogSeverity.INFORMATION_HIGH_DETAIL,
            "Building result")
        result = FlowProcessAllDynaFlowTypeScheduleTaskResult()
        result.context_object_code = dyna_flow_task_bus_obj.code

        super()._log_message_and_severity(
            LogSeverity.INFORMATION_HIGH_DETAIL,
            "Result:" + result.to_json())

        super()._log_message_and_severity(
            LogSeverity.INFORMATION_HIGH_DETAIL,
            "End")
        return result
