# flows/default/land_user_plant_multi_select_to_editable.py
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
from flows.base.land_user_plant_multi_select_to_editable import BaseFlowLandUserPlantMultiSelectToEditable
from models import Land
from flows.base import LogSeverity
from business.land import LandBusObj
from helpers import SessionContext
from helpers import ApiToken
from helpers import TypeConversion
import models as farm_models
import managers as farm_managers
import business
class FlowLandUserPlantMultiSelectToEditableResult():
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
class FlowLandUserPlantMultiSelectToEditable(BaseFlowLandUserPlantMultiSelectToEditable):
    """
    #TODO add comment
    """
    def __init__(self, session_context: SessionContext):
        """
        #TODO add comment
        """
        super(FlowLandUserPlantMultiSelectToEditable, self).__init__(session_context)
    async def process(
        self,
        land_bus_obj: LandBusObj,
        plant_code_list_csv: str = "",
# endset
        ) -> FlowLandUserPlantMultiSelectToEditableResult:
        super()._log_message_and_severity(LogSeverity.INFORMATION_HIGH_DETAIL, "Start")
        super()._log_message_and_severity(LogSeverity.INFORMATION_HIGH_DETAIL, "Code::" + str(land_bus_obj.code))
        await super()._process_validation_rules(
            land_bus_obj,
            plant_code_list_csv,
# endset
        )
        super()._throw_queued_validation_errors()

# endset
        code_list = self._parse_csv_string_to_guids(plant_code_list_csv)

        for code in code_list:
            plant_bus_obj = PlantBusObj(land_bus_obj.get_session_context())
            await plant_bus_obj.load_from_code(code)
            plant_bus_obj.is_edit_allowed = False
            await plant_bus_obj.save()

        super()._log_message_and_severity(LogSeverity.INFORMATION_HIGH_DETAIL, "Building result")
        result = FlowLandUserPlantMultiSelectToEditableResult()
        result.context_object_code = land_bus_obj.code

# endset
        super()._log_message_and_severity(LogSeverity.INFORMATION_HIGH_DETAIL, "Result:" + result.to_json())
        super()._log_message_and_severity(LogSeverity.INFORMATION_HIGH_DETAIL, "End")
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