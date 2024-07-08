# flows/default/land_user_plant_multi_select_to_not_editable.py  # pylint: disable=duplicate-code
# pylint: disable=unused-import
"""
This module contains the
FlowLandUserPlantMultiSelectToNotEditable class
and related classes
that handle the addition of a
 to a specific
land in the flow process.
"""

import json
import uuid  # noqa: F401
from datetime import date, datetime, timezone  # noqa: F401
from decimal import Decimal  # noqa: F401

from business.land import LandBusObj
from flows.base import LogSeverity
from flows.base.land_user_plant_multi_select_to_not_editable import (
    BaseFlowLandUserPlantMultiSelectToNotEditable)
from helpers import SessionContext  # noqa: F401
from helpers import TypeConversion  # noqa: F401


class FlowLandUserPlantMultiSelectToNotEditableResult():
    """
    Represents the result of the
    FlowLandUserPlantMultiSelectToNotEditable process.
    """

    context_object_code: uuid.UUID = uuid.UUID(int=0)

    def __init__(self):
        """
        Initializes a new instance of the
        FlowLandUserPlantMultiSelectToNotEditableResult class.
        """

    def to_json(self):
        """
        Converts the FlowLandUserPlantMultiSelectToNotEditableResult
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


class FlowLandUserPlantMultiSelectToNotEditable(
    BaseFlowLandUserPlantMultiSelectToNotEditable
):
    """
    FlowLandUserPlantMultiSelectToNotEditable handles the addition of
    a  to
    a specific land in the flow process.

    This class extends the
    BaseFlowLandUserPlantMultiSelectToNotEditableclass and
    initializes it with the provided session context.
    """

    async def process(
        self,
        land_bus_obj: LandBusObj,
        plant_code_list_csv: str = "",
# endset  # noqa: E122
    ) -> FlowLandUserPlantMultiSelectToNotEditableResult:
        """
        Processes the addition of a
         to a specific land.

        Returns:
            FlowLandUserPlantMultiSelectToNotEditableResult:
                The result of the
                FlowLandUserPlantMultiSelectToNotEditable process.
        """
        super()._log_message_and_severity(
            LogSeverity.INFORMATION_HIGH_DETAIL,
            "Start"
        )
        super()._log_message_and_severity(
            LogSeverity.INFORMATION_HIGH_DETAIL,
            "Code::" + str(land_bus_obj.code)
        )
        await super()._process_validation_rules(
            land_bus_obj,
            plant_code_list_csv,
# endset  # noqa: E122
        )
        super()._throw_queued_validation_errors()

        # TODO: add flow logic


        super()._log_message_and_severity(
            LogSeverity.INFORMATION_HIGH_DETAIL,
            "Building result")
        result = FlowLandUserPlantMultiSelectToNotEditableResult()
        result.context_object_code = land_bus_obj.code

        super()._log_message_and_severity(
            LogSeverity.INFORMATION_HIGH_DETAIL,
            "Result:" + result.to_json())

        super()._log_message_and_severity(
            LogSeverity.INFORMATION_HIGH_DETAIL,
            "End")
        return result
