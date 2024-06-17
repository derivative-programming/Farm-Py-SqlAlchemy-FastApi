# flows/default/pac_user_tri_state_filter_list_init_report.py
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
from flows.base.pac_user_tri_state_filter_list_init_report import BaseFlowPacUserTriStateFilterListInitReport
from models import Pac
from flows.base import LogSeverity
from business.pac import PacBusObj
from helpers import SessionContext
from helpers import ApiToken
from helpers import TypeConversion
import models as farm_models
import managers as farm_managers
import business
class FlowPacUserTriStateFilterListInitReportResult():
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
class FlowPacUserTriStateFilterListInitReport(BaseFlowPacUserTriStateFilterListInitReport):
    """
    #TODO add comment
    """
    def __init__(self, session_context: SessionContext):
        """
        #TODO add comment
        """
        super(FlowPacUserTriStateFilterListInitReport, self).__init__(session_context)
    async def process(
        self,
        pac_bus_obj: PacBusObj,

# endset
        ) -> FlowPacUserTriStateFilterListInitReportResult:
        super()._log_message_and_severity(LogSeverity.INFORMATION_HIGH_DETAIL, "Start")
        super()._log_message_and_severity(LogSeverity.INFORMATION_HIGH_DETAIL, "Code::" + str(pac_bus_obj.code))
        await super()._process_validation_rules(
            pac_bus_obj,

# endset
        )
        super()._throw_queued_validation_errors()

# endset
        # TODO: add flow logic

        super()._log_message_and_severity(LogSeverity.INFORMATION_HIGH_DETAIL, "Building result")
        result = FlowPacUserTriStateFilterListInitReportResult()
        result.context_object_code = pac_bus_obj.code

# endset
        super()._log_message_and_severity(LogSeverity.INFORMATION_HIGH_DETAIL, "Result:" + result.to_json())
        super()._log_message_and_severity(LogSeverity.INFORMATION_HIGH_DETAIL, "End")
        return result
