import json
from business.pac import PacBusObj
from datetime import date, datetime
import uuid
from flows.base.pac_user_date_greater_than_filter_list_init_report import BaseFlowPacUserDateGreaterThanFilterListInitReport
from models import Pac
from flows.base import LogSeverity
from helpers import SessionContext
from helpers import ApiToken
from helpers import TypeConversion
import models as farm_models
import managers as farm_managers
from sqlalchemy.ext.asyncio import AsyncSession
from services.db_config import db_dialect,generate_uuid
# from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
from sqlalchemy import String
from decimal import Decimal
class FlowPacUserDateGreaterThanFilterListInitReportResult():
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
class FlowPacUserDateGreaterThanFilterListInitReport(BaseFlowPacUserDateGreaterThanFilterListInitReport):
    def __init__(self, session_context: SessionContext):
        super(FlowPacUserDateGreaterThanFilterListInitReport, self).__init__(session_context)
    async def process(self,
        pac_bus_obj: PacBusObj,

        ) -> FlowPacUserDateGreaterThanFilterListInitReportResult:
        super()._log_message_and_severity(LogSeverity.information_high_detail, "Start")
        super()._log_message_and_severity(LogSeverity.information_high_detail, "Code::" + str(pac_bus_obj.code))
        await super()._process_validation_rules(
            pac_bus_obj,

        )
        super()._throw_queued_validation_errors()


        super()._log_message_and_severity(LogSeverity.information_high_detail, "Building result")
        result = FlowPacUserDateGreaterThanFilterListInitReportResult()
        result.context_object_code = pac_bus_obj.code

        super()._log_message_and_severity(LogSeverity.information_high_detail, "Result:" + result.to_json())
        super()._log_message_and_severity(LogSeverity.information_high_detail, "End")
        return result
