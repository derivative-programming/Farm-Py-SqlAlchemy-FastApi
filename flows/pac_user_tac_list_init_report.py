from business.pac import PacBusObj
from datetime import date, datetime
import uuid
from flows.base import BaseFlowPacUserTacListInitReport
from models import Pac
from flows.base import LogSeverity
from helpers import SessionContext
from helpers import ApiToken
from helpers import TypeConversion
import models as farm_models
import managers as farm_managers
from sqlalchemy.ext.asyncio import AsyncSession
from services.db_config import db_dialect,generate_uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
from sqlalchemy import String
from pydantic import BaseModel, Field, UUID4
from decimal import Decimal
class FlowPacUserTacListInitReportResult(BaseModel):
    context_object_code:UUID4 =  uuid.UUID(int=0)

    def __init__(self):
        pass
class FlowPacUserTacListInitReport(BaseFlowPacUserTacListInitReport):
    def __init__(self, session_context:SessionContext):
        super(FlowPacUserTacListInitReport, self).__init__(session_context)
    async def process(self,
        pac_bus_obj: PacBusObj,

        ) -> FlowPacUserTacListInitReportResult:
        super()._log_message_and_severity(LogSeverity.information_high_detail, "Start")
        super()._log_message_and_severity(LogSeverity.information_high_detail, "Code::" + str(pac_bus_obj.code))
        await super()._process_validation_rules(
            pac_bus_obj,

        )
        super()._throw_queued_validation_errors()

        # TODO: add flow logic

        super()._log_message_and_severity(LogSeverity.information_high_detail, "Building result")
        result = FlowPacUserTacListInitReportResult()
        result.context_object_code = pac_bus_obj.code

        super()._log_message_and_severity(LogSeverity.information_high_detail, "Result:" + result.to_json())
        super()._log_message_and_severity(LogSeverity.information_high_detail, "End")
        return result
