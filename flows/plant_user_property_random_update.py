# flows/default/plant_user_property_random_update.py
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
from flows.base.plant_user_property_random_update import BaseFlowPlantUserPropertyRandomUpdate
from models import Plant
from flows.base import LogSeverity
from business.plant import PlantBusObj
from helpers import SessionContext
from helpers import ApiToken
from helpers import TypeConversion
import models as farm_models
import managers as farm_managers
import business
class FlowPlantUserPropertyRandomUpdateResult():
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
class FlowPlantUserPropertyRandomUpdate(BaseFlowPlantUserPropertyRandomUpdate):
    """
    #TODO add comment
    """
    def __init__(self, session_context: SessionContext):
        """
        #TODO add comment
        """
        super(FlowPlantUserPropertyRandomUpdate, self).__init__(session_context)
    async def process(
        self,
        plant_bus_obj: PlantBusObj,

# endset
        ) -> FlowPlantUserPropertyRandomUpdateResult:
        super()._log_message_and_severity(LogSeverity.information_high_detail, "Start")
        super()._log_message_and_severity(LogSeverity.information_high_detail, "Code::" + str(plant_bus_obj.code))
        await super()._process_validation_rules(
            plant_bus_obj,

# endset
        )
        super()._throw_queued_validation_errors()

# endset
        await plant_bus_obj.randomize_properties()
        await plant_bus_obj.save()

        super()._log_message_and_severity(LogSeverity.information_high_detail, "Building result")
        result = FlowPlantUserPropertyRandomUpdateResult()
        result.context_object_code = plant_bus_obj.code

# endset
        super()._log_message_and_severity(LogSeverity.information_high_detail, "Result:" + result.to_json())
        super()._log_message_and_severity(LogSeverity.information_high_detail, "End")
        return result
