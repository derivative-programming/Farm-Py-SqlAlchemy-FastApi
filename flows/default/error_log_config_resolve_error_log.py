# flows/default/error_log_config_resolve_error_log.py
"""
    #TODO add comment
"""
import uuid
import json
from datetime import date, datetime
from sqlalchemy import String
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
from decimal import Decimal
from flows.base.error_log_config_resolve_error_log import BaseFlowErrorLogConfigResolveErrorLog
from models import ErrorLog
from flows.base import LogSeverity
from business.error_log import ErrorLogBusObj
from helpers import SessionContext
from helpers import ApiToken
from helpers import TypeConversion
import models as farm_models
import managers as farm_managers
import business
from services.db_config import DB_DIALECT, generate_uuid
class FlowErrorLogConfigResolveErrorLogResult():
    """
    #TODO add comment
    """
    context_object_code: uuid.UUID = uuid.UUID(int=0)

# endset
    def __init__(self):
        pass
    def to_json(self):
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
        super()._log_message_and_severity(LogSeverity.information_high_detail, "Start")
        super()._log_message_and_severity(LogSeverity.information_high_detail, "Code::" + str(error_log_bus_obj.code))
        await super()._process_validation_rules(
            error_log_bus_obj,

# endset
        )
        super()._throw_queued_validation_errors()

# endset
        # TODO: add flow logic

        super()._log_message_and_severity(LogSeverity.information_high_detail, "Building result")
        result = FlowErrorLogConfigResolveErrorLogResult()
        result.context_object_code = error_log_bus_obj.code

# endset
        super()._log_message_and_severity(LogSeverity.information_high_detail, "Result:" + result.to_json())
        super()._log_message_and_severity(LogSeverity.information_high_detail, "End")
        return result
