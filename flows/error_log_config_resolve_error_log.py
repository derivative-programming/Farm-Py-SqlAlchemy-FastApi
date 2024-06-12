import json
from business.error_log import ErrorLogBusObj
from datetime import date, datetime
import uuid
from flows.base.error_log_config_resolve_error_log import BaseFlowErrorLogConfigResolveErrorLog
from models import ErrorLog
from flows.base import LogSeverity
from helpers import SessionContext
from helpers import ApiToken
from helpers import TypeConversion
import models as farm_models
import managers as farm_managers
from sqlalchemy.ext.asyncio import AsyncSession
from services.db_config import DB_DIALECT, generate_uuid
# from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
from sqlalchemy import String
from decimal import Decimal
class FlowErrorLogConfigResolveErrorLogResult():
    context_object_code: uuid.UUID =  uuid.UUID(int=0)

    def __init__(self):
        pass
    def to_json(self):
        # Create a dictionary representation of the instance
        data = {
            'context_object_code': str(self.context_object_code),

        }
        # Serialize the dictionary to JSON
        return json.dumps(data)
class FlowErrorLogConfigResolveErrorLog(BaseFlowErrorLogConfigResolveErrorLog):
    def __init__(self, session_context: SessionContext):
        super(FlowErrorLogConfigResolveErrorLog, self).__init__(session_context)
    async def process(self,
        error_log_bus_obj: ErrorLogBusObj,

        ) -> FlowErrorLogConfigResolveErrorLogResult:
        super()._log_message_and_severity(LogSeverity.information_high_detail, "Start")
        super()._log_message_and_severity(LogSeverity.information_high_detail, "Code::" + str(error_log_bus_obj.code))
        await super()._process_validation_rules(
            error_log_bus_obj,

        )
        super()._throw_queued_validation_errors()

        error_log_bus_obj = (
            error_log_bus_obj
            .set_prop_is_resolved(True)
            .set_prop_last_update_user_id(self._session_context.customer_code)
        )
        await error_log_bus_obj.save()

        super()._log_message_and_severity(LogSeverity.information_high_detail, "Building result")
        result = FlowErrorLogConfigResolveErrorLogResult()
        result.context_object_code = error_log_bus_obj.code

        super()._log_message_and_severity(LogSeverity.information_high_detail, "Result:" + result.to_json())
        super()._log_message_and_severity(LogSeverity.information_high_detail, "End")
        return result
