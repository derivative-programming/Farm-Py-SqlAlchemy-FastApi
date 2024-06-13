# flows/default/tac_farm_dashboard_init_report.py
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
from flows.base.tac_farm_dashboard_init_report import BaseFlowTacFarmDashboardInitReport
from models import Tac
from flows.base import LogSeverity
from business.tac import TacBusObj
from helpers import SessionContext
from helpers import ApiToken
from helpers import TypeConversion
import models as farm_models
import managers as farm_managers
import business
class FlowTacFarmDashboardInitReportResult():
    """
    #TODO add comment
    """
    context_object_code: uuid.UUID = uuid.UUID(int=0)
    customer_code: uuid.UUID = uuid.UUID(int=0)
# endset
    def __init__(self):
        pass
    def to_json(self):
        # Create a dictionary representation of the instance
        data = {
            'context_object_code': str(self.context_object_code),
            'customer_code': str(self.customer_code),
# endset
        }
        # Serialize the dictionary to JSON
        return json.dumps(data)
class FlowTacFarmDashboardInitReport(BaseFlowTacFarmDashboardInitReport):
    """
    #TODO add comment
    """
    def __init__(self, session_context: SessionContext):
        """
        #TODO add comment
        """
        super(FlowTacFarmDashboardInitReport, self).__init__(session_context)
    async def process(
        self,
        tac_bus_obj: TacBusObj,

# endset
        ) -> FlowTacFarmDashboardInitReportResult:
        super()._log_message_and_severity(LogSeverity.information_high_detail, "Start")
        super()._log_message_and_severity(LogSeverity.information_high_detail, "Code::" + str(tac_bus_obj.code))
        await super()._process_validation_rules(
            tac_bus_obj,

# endset
        )
        super()._throw_queued_validation_errors()
        customer_code_output: uuid.UUID = uuid.UUID(int=0)
# endset
        customer_code_output = self._session_context.customer_code

        super()._log_message_and_severity(LogSeverity.information_high_detail, "Building result")
        result = FlowTacFarmDashboardInitReportResult()
        result.context_object_code = tac_bus_obj.code
        result.customer_code = customer_code_output
# endset
        super()._log_message_and_severity(LogSeverity.information_high_detail, "Result:" + result.to_json())
        super()._log_message_and_severity(LogSeverity.information_high_detail, "End")
        return result
