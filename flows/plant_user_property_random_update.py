# flows/default/plant_user_property_random_update.py  # pylint: disable=duplicate-code # noqa: E501
# pylint: disable=unused-import
# pylint: disable=too-few-public-methods
"""
This module contains the
FlowPlantUserPropertyRandomUpdate class
and related classes
that handle the addition of a
 to a specific
plant in the flow process.
"""

import json
import uuid  # noqa: F401
from datetime import date, datetime, timezone  # noqa: F401
from decimal import Decimal  # noqa: F401

from business.plant import PlantBusObj
from flows.base import LogSeverity
from flows.base.plant_user_property_random_update import \
    BaseFlowPlantUserPropertyRandomUpdate
from helpers import SessionContext  # noqa: F401
from helpers import TypeConversion  # noqa: F401


class FlowPlantUserPropertyRandomUpdateResult():
    """
    Represents the result of the
    FlowPlantUserPropertyRandomUpdate process.
    """

    context_object_code: uuid.UUID = uuid.UUID(int=0)

    def __init__(self):
        """
        Initializes a new instance of the
        FlowPlantUserPropertyRandomUpdateResult class.
        """

    def to_json(self):
        """
        Converts the FlowPlantUserPropertyRandomUpdateResult
        instance to a JSON string.

        Returns:
            str: The JSON representation of the instance.
        """
        # Create a dictionary representation of the instance
        data = {
            'context_object_code':
                str(self.context_object_code),

# endset  # noqa: E122
        }
        # Serialize the dictionary to JSON
        return json.dumps(data)


class FlowPlantUserPropertyRandomUpdate(
    BaseFlowPlantUserPropertyRandomUpdate
):
    """
    FlowPlantUserPropertyRandomUpdate handles the addition of
    a  to
    a specific plant in the flow process.

    This class extends the
    BaseFlowPlantUserPropertyRandomUpdateclass and
    initializes it with the provided session context.
    """

    async def process(
        self,
        plant_bus_obj: PlantBusObj,

# endset  # noqa: E122
    ) -> FlowPlantUserPropertyRandomUpdateResult:
        """
        Processes the addition of a
         to a specific plant.

        Returns:
            FlowPlantUserPropertyRandomUpdateResult:
                The result of the
                FlowPlantUserPropertyRandomUpdate process.
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

        await plant_bus_obj.randomize_properties()
        await plant_bus_obj.save()


        super()._log_message_and_severity(
            LogSeverity.INFORMATION_HIGH_DETAIL,
            "Building result")
        result = FlowPlantUserPropertyRandomUpdateResult()
        result.context_object_code = plant_bus_obj.code

        super()._log_message_and_severity(
            LogSeverity.INFORMATION_HIGH_DETAIL,
            "Result:" + result.to_json())

        super()._log_message_and_severity(
            LogSeverity.INFORMATION_HIGH_DETAIL,
            "End")
        return result
