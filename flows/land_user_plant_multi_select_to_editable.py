from business.land import LandBusObj
from datetime import date, datetime
import uuid
from flows.base import BaseFlowLandUserPlantMultiSelectToEditable
from models import Land
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
class FlowLandUserPlantMultiSelectToEditableResult(BaseModel):
    context_object_code:UUID4 =  uuid.UUID(int=0)

    def __init__(self):
        pass
class FlowLandUserPlantMultiSelectToEditable(BaseFlowLandUserPlantMultiSelectToEditable):
    def __init__(self, session_context:SessionContext):
        super(FlowLandUserPlantMultiSelectToEditable, self).__init__(session_context)
    async def process(self,
        land_bus_obj: LandBusObj,
        plant_code_list_csv:str = "",
        ) -> FlowLandUserPlantMultiSelectToEditableResult:
        super()._log_message_and_severity(LogSeverity.information_high_detail, "Start")
        super()._log_message_and_severity(LogSeverity.information_high_detail, "Code::" + str(land_bus_obj.code))
        await super()._process_validation_rules(
            land_bus_obj,
            plant_code_list_csv,
        )
        super()._throw_queued_validation_errors()

        # TODO: add flow logic

        super()._log_message_and_severity(LogSeverity.information_high_detail, "Building result")
        result = FlowLandUserPlantMultiSelectToEditableResult()
        result.context_object_code = land_bus_obj.code

        super()._log_message_and_severity(LogSeverity.information_high_detail, "Result:" + result.to_json())
        super()._log_message_and_severity(LogSeverity.information_high_detail, "End")
        return result
