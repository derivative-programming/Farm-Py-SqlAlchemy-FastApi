# flows/default/error_log_config_resolve_error_log.py
"""
    #TODO add comment
"""
import uuid
import json
from flows.base.error_log_config_resolve_error_log import BaseFlowErrorLogConfigResolveErrorLog
from flows.base import LogSeverity
from business.error_log import ErrorLogBusObj
from helpers import SessionContext


class FlowErrorLogConfigResolveErrorLogResult():
    """
    #TODO add comment
    """
    context_object_code: uuid.UUID = uuid.UUID(int=0)

# endset
    def __init__(self):
        """
            #TODO add comment
        """

    def to_json(self):
        """
            #TODO add comment
        """

        # Create a dictionary representation of the instance
        data = {
            'context_object_code': str(self.context_object_code),

# endset
        }
        # Serialize the dictionary to JSON
        return json.dumps(data)


class FlowErrorLogConfigResolveErrorLog(BaseFlowErrorLogConfigResolveErrorLog):
    """
    #TODO add comment
    """
    def __init__(self, session_context: SessionContext):
        """
        #TODO add comment
        """

        super(FlowErrorLogConfigResolveErrorLog, self).__init__(session_context)

    async def process(
        self,
        error_log_bus_obj: ErrorLogBusObj,

# endset
        ) -> FlowErrorLogConfigResolveErrorLogResult:
        """
            #TODO add comment
        """

        super()._log_message_and_severity(LogSeverity.INFORMATION_HIGH_DETAIL, "Start")
        super()._log_message_and_severity(LogSeverity.INFORMATION_HIGH_DETAIL, "Code::" + str(error_log_bus_obj.code))
        await super()._process_validation_rules(
            error_log_bus_obj,

# endset
        )
        super()._throw_queued_validation_errors()

# endset
        error_log_bus_obj = (
            error_log_bus_obj
            .set_prop_is_resolved(True)
            .set_prop_last_update_user_id(self._session_context.customer_code)
        )
        await error_log_bus_obj.save()
        super()._log_message_and_severity(LogSeverity.INFORMATION_HIGH_DETAIL, "Building result")
        result = FlowErrorLogConfigResolveErrorLogResult()
        result.context_object_code = error_log_bus_obj.code

# endset
        super()._log_message_and_severity(LogSeverity.INFORMATION_HIGH_DETAIL, "Result:" + result.to_json())
        super()._log_message_and_severity(LogSeverity.INFORMATION_HIGH_DETAIL, "End")
        return result
