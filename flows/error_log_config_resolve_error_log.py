from business.error_log import ErrorLogBusObj
from datetime import date, datetime
import uuid
from flows.base import BaseFlowErrorLogConfigResolveErrorLog
from models import ErrorLog
from flows.base import LogSeverity
from helpers import SessionContext
from helpers import ApiToken
from decimal import Decimal
from helpers import TypeConversion
import models as farm_models
import managers as farm_managers
from sqlalchemy.ext.asyncio import AsyncSession
from services.db_config import db_dialect,generate_uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
from sqlalchemy import String
# @dataclass_json
# @dataclass
class FlowErrorLogConfigResolveErrorLogResult():
    context_object_code:uuid = uuid.UUID(int=0)

class FlowErrorLogConfigResolveErrorLog(BaseFlowErrorLogConfigResolveErrorLog):
    def __init__(self, session_context:SessionContext):
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

        # TODO: add flow logic

        super()._log_message_and_severity(LogSeverity.information_high_detail, "Building result")
        result = FlowErrorLogConfigResolveErrorLogResult()
        result.context_object_code = error_log_bus_obj.code

        super()._log_message_and_severity(LogSeverity.information_high_detail, "Result:" + result.to_json())
        super()._log_message_and_severity(LogSeverity.information_high_detail, "End")
        return result
