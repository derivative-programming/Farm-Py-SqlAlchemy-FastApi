# flows/default/plant_user_details_init_report.py
# pylint: disable=unused-import
"""
This module contains the
FlowPlantUserDetailsInitReport class and related classes
that handle the addition of a
 to a specific
plant in the flow process.
"""
import uuid
import json
from datetime import date, datetime
from decimal import Decimal
from flows.base.plant_user_details_init_report import BaseFlowPlantUserDetailsInitReport
from flows.base import LogSeverity
from business.plant import PlantBusObj
from helpers import SessionContext  # noqa: F401
from helpers import TypeConversion
class FlowPlantUserDetailsInitReportResult():
    """
    Represents the result of the
    FlowPlantUserDetailsInitReport process.
    """
    context_object_code: uuid.UUID = uuid.UUID(int=0)
    land_code: uuid.UUID = uuid.UUID(int=0)
    tac_code: uuid.UUID = uuid.UUID(int=0)
# endset
    def __init__(self):
        """
        Initializes a new instance of the
        FlowPlantUserDetailsInitReportResult class.
        """
    def to_json(self):
        """
        Converts the FlowPlantUserDetailsInitReportResult
        instance to a JSON string.
        Returns:
            str: The JSON representation of the instance.
        """
        # Create a dictionary representation of the instance
        data = {
            'context_object_code':
                str(self.context_object_code),
            'land_code':
                str(self.land_code),
            'tac_code':
                str(self.tac_code),
# endset  # noqa: E122
        }
        # Serialize the dictionary to JSON
        return json.dumps(data)
class FlowPlantUserDetailsInitReport(
    BaseFlowPlantUserDetailsInitReport
):
    """
    FlowPlantUserDetailsInitReport handles the addition of
    a  to
    a specific plant in the flow process.
    This class extends the BaseFlowPlantUserDetailsInitReport class and
    initializes it with the provided session context.
    """
    async def process(
        self,
        plant_bus_obj: PlantBusObj,

# endset  # noqa: E122
    ) -> FlowPlantUserDetailsInitReportResult:
        """
        Processes the addition of a
         to a specific plant.
        Returns:
            FlowPlantUserDetailsInitReportResult: The result of the
                FlowPlantUserDetailsInitReport process.
        """
        super()._log_message_and_severity(
            LogSeverity.INFORMATION_HIGH_DETAIL,
            "Start"
        )
        super()._log_message_and_severity(
            LogSeverity.INFORMATION_HIGH_DETAIL,
            "Code::" + str(plant_bus_obj.code)
        )
        await super()._process_validation_rules(
            plant_bus_obj,

# endset  # noqa: E122
        )
        super()._throw_queued_validation_errors()
        land_code_output: uuid.UUID = uuid.UUID(int=0)
        tac_code_output: uuid.UUID = uuid.UUID(int=0)
# endset
        # TODO: add flow logic

        super()._log_message_and_severity(
            LogSeverity.INFORMATION_HIGH_DETAIL,
            "Building result")
        result = FlowPlantUserDetailsInitReportResult()
        result.context_object_code = plant_bus_obj.code
        result.land_code = (
            land_code_output)
        result.tac_code = (
            tac_code_output)
# endset
        super()._log_message_and_severity(
            LogSeverity.INFORMATION_HIGH_DETAIL,
            "Result:" + result.to_json())
        super()._log_message_and_severity(
            LogSeverity.INFORMATION_HIGH_DETAIL,
            "End")
        return result
