# flows/default/dyna_flow_task_dyna_flow_cleanup.py  # pylint: disable=duplicate-code # noqa: E501
# pylint: disable=unused-import
# pylint: disable=too-few-public-methods
"""
This module contains the
FlowDynaFlowTaskDynaFlowCleanup class
and related classes
that handle the addition of a
 to a specific
dyna_flow_task in the flow process.
"""

import json
from typing import List
import uuid  # noqa: F401
from datetime import date, datetime, timezone  # noqa: F401
from decimal import Decimal  # noqa: F401

from business.dyna_flow_task import DynaFlowTaskBusObj
from flows.base import LogSeverity
from flows.base.dyna_flow_task_dyna_flow_cleanup import \
    BaseFlowDynaFlowTaskDynaFlowCleanup
from helpers import SessionContext  # noqa: F401
from helpers import TypeConversion  # noqa: F401


class FlowDynaFlowTaskDynaFlowCleanupResult():
    """
    Represents the result of the
    FlowDynaFlowTaskDynaFlowCleanup process.
    """

    context_object_code: uuid.UUID = uuid.UUID(int=0)

    def __init__(self):
        """
        Initializes a new instance of the
        FlowDynaFlowTaskDynaFlowCleanupResult class.
        """

    def to_json(self):
        """
        Converts the FlowDynaFlowTaskDynaFlowCleanupResult
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


class FlowDynaFlowTaskDynaFlowCleanup(
    BaseFlowDynaFlowTaskDynaFlowCleanup
):
    """
    FlowDynaFlowTaskDynaFlowCleanup handles the addition of
    a  to
    a specific dyna_flow_task in the flow process.

    This class extends the
    BaseFlowDynaFlowTaskDynaFlowCleanupclass and
    initializes it with the provided session context.
    """

    async def process(
        self,
        dyna_flow_task_bus_obj: DynaFlowTaskBusObj,

# endset  # noqa: E122
    ) -> FlowDynaFlowTaskDynaFlowCleanupResult:
        """
        Processes the addition of a
         to a specific dyna_flow_task.

        Returns:
            FlowDynaFlowTaskDynaFlowCleanupResult:
                The result of the
                FlowDynaFlowTaskDynaFlowCleanup process.
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

        dyna_flow = await dyna_flow_task_bus_obj.get_dyna_flow_id_bus_obj()

        dyna_flow_task_list = await dyna_flow.get_all_dyna_flow_task()

        dyna_flow_task_list = next(
            (
                x
                for x in dyna_flow_task_list
                if x.dyna_flow_task_id != (
                    dyna_flow_task_bus_obj.dyna_flow_task_id)
            ),
            None
        )

        assert isinstance(dyna_flow_task_list, List)

        dyna_flow.completed_utc_date_time = datetime.now(timezone.utc)
        dyna_flow.is_completed = True
        dyna_flow.is_successful = all(
            task.is_successful for task in dyna_flow_task_list
        )
        await dyna_flow.save()

        # dyna_flow_type = await dyna_flow.get_dyna_flow_type_id_bus_obj()

        # if dyna_flow.is_successful is not True and \
        #     dyna_flow_type.lookup_enum !=  \
        #         managers_and_enums.DynaFlowTypeEnum.CustomerEmailRequestSendEmail:
        #     await DR.Core.Flows.Emails.send_email_to_config_manager_async(
        #         session_context,
        #         "Data Flow Not completed Successfully",
        #         "Data Flow Not completed Successfully",
        #         "Data Flow Not completed Successfully",
        #         "View",
        #         "/Report/TacConfigDynaFlowList/" + DR.Core.CurrentRuntime.get_tac(session_context, TacManager.LookupEnum.Primary).code,
        #         EmailTypeManager.LookupEnum.DynaFlow_Error_ToConfig,
        #         dyna_flow.code


        super()._log_message_and_severity(
            LogSeverity.INFORMATION_HIGH_DETAIL,
            "Building result")
        result = FlowDynaFlowTaskDynaFlowCleanupResult()
        result.context_object_code = dyna_flow_task_bus_obj.code

        super()._log_message_and_severity(
            LogSeverity.INFORMATION_HIGH_DETAIL,
            "Result:" + result.to_json())

        super()._log_message_and_severity(
            LogSeverity.INFORMATION_HIGH_DETAIL,
            "End")
        return result
