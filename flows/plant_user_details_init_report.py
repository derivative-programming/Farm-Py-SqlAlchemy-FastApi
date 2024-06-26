# flows/default/plant_user_details_init_report.py
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
from flows.base.plant_user_details_init_report import BaseFlowPlantUserDetailsInitReport
from models import Plant
from flows.base import LogSeverity
from business.plant import PlantBusObj
from helpers import SessionContext
from helpers import ApiToken
from helpers import TypeConversion
import models as farm_models
import managers as farm_managers
import business
class FlowPlantUserDetailsInitReportResult():
    """
    #TODO add comment
    """
    context_object_code: uuid.UUID = uuid.UUID(int=0)
    land_code: uuid.UUID = uuid.UUID(int=0)
    tac_code: uuid.UUID = uuid.UUID(int=0)
# endset
    def __init__(self):
        pass
    def to_json(self):
        # Create a dictionary representation of the instance
        data = {
            'context_object_code': str(self.context_object_code),
            'land_code': str(self.land_code),
            'tac_code': str(self.tac_code),
# endset
        }
        # Serialize the dictionary to JSON
        return json.dumps(data)
class FlowPlantUserDetailsInitReport(BaseFlowPlantUserDetailsInitReport):
    """
    #TODO add comment
    """
    def __init__(self, session_context: SessionContext):
        """
        #TODO add comment
        """
        super(FlowPlantUserDetailsInitReport, self).__init__(session_context)
    async def process(
        self,
        plant_bus_obj: PlantBusObj,

# endset
        ) -> FlowPlantUserDetailsInitReportResult:
        super()._log_message_and_severity(LogSeverity.INFORMATION_HIGH_DETAIL, "Start")
        super()._log_message_and_severity(LogSeverity.INFORMATION_HIGH_DETAIL, "Code::" + str(plant_bus_obj.code))
        await super()._process_validation_rules(
            plant_bus_obj,

# endset
        )
        super()._throw_queued_validation_errors()
        land_code_output: uuid.UUID = uuid.UUID(int=0)
        tac_code_output: uuid.UUID = uuid.UUID(int=0)
# endset
        land_code_output = plant_bus_obj.land_code_peek
        tac_code_output = self._session_context.tac_code
        super()._log_message_and_severity(LogSeverity.INFORMATION_HIGH_DETAIL, "Building result")
        result = FlowPlantUserDetailsInitReportResult()
        result.context_object_code = plant_bus_obj.code
        result.land_code = land_code_output
        result.tac_code = tac_code_output
# endset
        super()._log_message_and_severity(LogSeverity.INFORMATION_HIGH_DETAIL, "Result:" + result.to_json())
        super()._log_message_and_severity(LogSeverity.INFORMATION_HIGH_DETAIL, "End")
        return result
