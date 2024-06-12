# flows/default/pac_user_flavor_list_init_report.py
"""
    #TODO add comment
"""
import json
from business.pac import PacBusObj
from datetime import date, datetime
import uuid
from flows.base.pac_user_flavor_list_init_report import BaseFlowPacUserFlavorListInitReport
from models import Pac
from flows.base import LogSeverity
from helpers import SessionContext
from helpers import ApiToken
from helpers import TypeConversion
import models as farm_models
import managers as farm_managers
import business
from sqlalchemy.ext.asyncio import AsyncSession
from services.db_config import DB_DIALECT,generate_uuid
# from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
from sqlalchemy import String
from decimal import Decimal
class FlowPacUserFlavorListInitReportResult():
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
class FlowPacUserFlavorListInitReport(BaseFlowPacUserFlavorListInitReport):
    """
    #TODO add comment
    """
    def __init__(self, session_context: SessionContext):
        super(FlowPacUserFlavorListInitReport, self).__init__(session_context)
    async def process(self,
        pac_bus_obj: PacBusObj,

# endset
        ) -> FlowPacUserFlavorListInitReportResult:
        super()._log_message_and_severity(LogSeverity.information_high_detail, "Start")
        super()._log_message_and_severity(LogSeverity.information_high_detail, "Code::" + str(pac_bus_obj.code))
        await super()._process_validation_rules(
            pac_bus_obj,

# endset
        )
        super()._throw_queued_validation_errors()

# endset
        # TODO: add flow logic

        super()._log_message_and_severity(LogSeverity.information_high_detail, "Building result")
        result = FlowPacUserFlavorListInitReportResult()
        result.context_object_code = pac_bus_obj.code

# endset
        super()._log_message_and_severity(LogSeverity.information_high_detail, "Result:" + result.to_json())
        super()._log_message_and_severity(LogSeverity.information_high_detail, "End")
        return result
