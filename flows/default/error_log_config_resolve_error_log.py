# flows/default/error_log_config_resolve_error_log.py
# pylint: disable=unused-import
"""
This module contains the
FlowErrorLogConfigResolveErrorLog class and related classes
that handle the addition of a
 to a specific
error_log in the flow process.
"""

import uuid  # noqa: F401
import json
from datetime import date, datetime  # noqa: F401
from decimal import Decimal  # noqa: F401
from flows.base.error_log_config_resolve_error_log import (
    BaseFlowErrorLogConfigResolveErrorLog)
from flows.base import LogSeverity
from business.error_log import ErrorLogBusObj
from helpers import SessionContext  # noqa: F401
from helpers import TypeConversion


class FlowErrorLogConfigResolveErrorLogResult():
    """
    Represents the result of the
    FlowErrorLogConfigResolveErrorLog process.
    """

    context_object_code: uuid.UUID = uuid.UUID(int=0)


    def __init__(self):
        """
        Initializes a new instance of the
        FlowErrorLogConfigResolveErrorLogResult class.
        """

    def to_json(self):
        """
        Converts the FlowErrorLogConfigResolveErrorLogResult
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


class FlowErrorLogConfigResolveErrorLog(
    BaseFlowErrorLogConfigResolveErrorLog
):
    """
    FlowErrorLogConfigResolveErrorLog handles the addition of
    a  to
    a specific error_log in the flow process.

    This class extends the BaseFlowErrorLogConfigResolveErrorLog class and
    initializes it with the provided session context.
    """

    async def process(
        self,
        error_log_bus_obj: ErrorLogBusObj,

# endset  # noqa: E122
    ) -> FlowErrorLogConfigResolveErrorLogResult:
        """
        Processes the addition of a
         to a specific error_log.

        Returns:
            FlowErrorLogConfigResolveErrorLogResult: The result of the
                FlowErrorLogConfigResolveErrorLog process.
        """
        super()._log_message_and_severity(
            LogSeverity.INFORMATION_HIGH_DETAIL,
            "Start"
        )
        super()._log_message_and_severity(
            LogSeverity.INFORMATION_HIGH_DETAIL,
            "Code::" + str(error_log_bus_obj.code)
        )

        await super()._process_validation_rules(
            error_log_bus_obj,

# endset  # noqa: E122
        )

        super()._throw_queued_validation_errors()


        # TODO: add flow logic


        super()._log_message_and_severity(
            LogSeverity.INFORMATION_HIGH_DETAIL,
            "Building result")
        result = FlowErrorLogConfigResolveErrorLogResult()

        result.context_object_code = error_log_bus_obj.code


        super()._log_message_and_severity(
            LogSeverity.INFORMATION_HIGH_DETAIL,
            "Result:" + result.to_json())

        super()._log_message_and_severity(
            LogSeverity.INFORMATION_HIGH_DETAIL,
            "End")

        return result

