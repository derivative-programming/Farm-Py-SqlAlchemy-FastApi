import json
from business.land import LandBusObj
from datetime import date, datetime
import uuid
from business.plant import PlantBusObj
from flows.base.land_user_plant_multi_select_to_editable import BaseFlowLandUserPlantMultiSelectToEditable
from models import Land
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
class FlowLandUserPlantMultiSelectToEditableResult():
    context_object_code:uuid.UUID =  uuid.UUID(int=0)

    def __init__(self):
        pass
    def to_json(self):
        # Create a dictionary representation of the instance
        data = {
            'context_object_code': str(self.context_object_code),

        }
        # Serialize the dictionary to JSON
        return json.dumps(data)
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
 
        code_list = self._parse_csv_string_to_guids(plant_code_list_csv)
        
        for code in code_list:
            plant_bus_obj = PlantBusObj(land_bus_obj.session)
            await plant_bus_obj.load(code=code)
            plant_bus_obj.is_edit_allowed = False
            await plant_bus_obj.save()



        super()._log_message_and_severity(LogSeverity.information_high_detail, "Building result")
        result = FlowLandUserPlantMultiSelectToEditableResult()
        result.context_object_code = land_bus_obj.code

        super()._log_message_and_severity(LogSeverity.information_high_detail, "Result:" + result.to_json())
        super()._log_message_and_severity(LogSeverity.information_high_detail, "End")
        return result


    def _is_valid_guid(self,guid):
        try:
            uuid.UUID(guid)
            return True
        except ValueError:
            return False

    def _parse_csv_string_to_guids(self,csv_string):
        guids = []
        lines = csv_string.strip().split('\n')

        reader = csv.reader(lines)
        for row in reader:
            for cell in row:
                if self._is_valid_guid(cell.strip()):
                    guids.append(cell.strip())

        return guids