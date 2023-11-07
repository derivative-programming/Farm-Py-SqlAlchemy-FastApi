from business.tac import TacBusObj
from datetime import date, datetime
import uuid
from flows.base import BaseFlowTacFarmDashboardInitReport
from models import Tac
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
class FlowTacFarmDashboardInitReportResult(BaseModel):
    context_object_code:UUID4 =  uuid.UUID(int=0)
    customer_code:UUID4 =  uuid.UUID(int=0)
    def __init__(self):
        pass
class FlowTacFarmDashboardInitReport(BaseFlowTacFarmDashboardInitReport):
    def __init__(self, session_context:SessionContext):
        super(FlowTacFarmDashboardInitReport, self).__init__(session_context)
    async def process(self,
        tac_bus_obj: TacBusObj,

        ) -> FlowTacFarmDashboardInitReportResult:
        super()._log_message_and_severity(LogSeverity.information_high_detail, "Start")
        super()._log_message_and_severity(LogSeverity.information_high_detail, "Code::" + str(tac_bus_obj.code))
        await super()._process_validation_rules(
            tac_bus_obj,

        )
        super()._throw_queued_validation_errors()
        customer_code_output:uuid = uuid.UUID(int=0)
        # TODO: add flow logic

        super()._log_message_and_severity(LogSeverity.information_high_detail, "Building result")
        result = FlowTacFarmDashboardInitReportResult()
        result.context_object_code = tac_bus_obj.code
        result.customer_code = customer_code_output
        super()._log_message_and_severity(LogSeverity.information_high_detail, "Result:" + result.to_json())
        super()._log_message_and_severity(LogSeverity.information_high_detail, "End")
        return result
