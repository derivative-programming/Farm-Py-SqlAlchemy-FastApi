import json
from business.plant import PlantBusObj
from datetime import date, datetime
import uuid
from flows.base.plant_user_details_init_report import BaseFlowPlantUserDetailsInitReport
from models import Plant
from flows.base import LogSeverity
from helpers import SessionContext
from helpers import ApiToken
from helpers import TypeConversion
import models as farm_models
import managers as farm_managers
import business
from sqlalchemy.ext.asyncio import AsyncSession
from services.db_config import db_dialect,generate_uuid
# from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
from sqlalchemy import String
from decimal import Decimal
class FlowPlantUserDetailsInitReportResult():
    context_object_code:uuid.UUID =  uuid.UUID(int=0)
    land_code:uuid.UUID =  uuid.UUID(int=0)
    tac_code:uuid.UUID =  uuid.UUID(int=0)

    def __init__(self):
        pass
    def to_json(self):
        # Create a dictionary representation of the instance
        data = {
            'context_object_code': str(self.context_object_code),
            'land_code': str(self.land_code),
            'tac_code': str(self.tac_code),

        }
        # Serialize the dictionary to JSON
        return json.dumps(data)
class FlowPlantUserDetailsInitReport(BaseFlowPlantUserDetailsInitReport):
    def __init__(self, session_context:SessionContext):
        super(FlowPlantUserDetailsInitReport, self).__init__(session_context)
    async def process(self,
        plant_bus_obj: PlantBusObj,

        ) -> FlowPlantUserDetailsInitReportResult:
        super()._log_message_and_severity(LogSeverity.information_high_detail, "Start")
        super()._log_message_and_severity(LogSeverity.information_high_detail, "Code::" + str(plant_bus_obj.code))
        await super()._process_validation_rules(
            plant_bus_obj,

        )
        super()._throw_queued_validation_errors()
        land_code_output:uuid = uuid.UUID(int=0)
        tac_code_output:uuid = uuid.UUID(int=0)

        # TODO: add flow logic

        super()._log_message_and_severity(LogSeverity.information_high_detail, "Building result")
        result = FlowPlantUserDetailsInitReportResult()
        result.context_object_code = plant_bus_obj.code
        result.land_code = land_code_output
        result.tac_code = tac_code_output

        super()._log_message_and_severity(LogSeverity.information_high_detail, "Result:" + result.to_json())
        super()._log_message_and_severity(LogSeverity.information_high_detail, "End")
        return result
