# flows/default/land_user_plant_multi_select_to_editable.py  # pylint: disable=duplicate-code # noqa: E501
# pylint: disable=unused-import
# pylint: disable=too-few-public-methods
"""
This module contains the
FlowLandUserPlantMultiSelectToEditable class
and related classes
that handle the addition of a
 to a specific
land in the flow process.
"""

import json
import uuid  # noqa: F401
from datetime import date, datetime, timezone  # noqa: F401
from decimal import Decimal  # noqa: F401

import business  # noqa: F401
from business.land import LandBusObj
from flows.base import LogSeverity
from flows.base.land_user_plant_multi_select_to_editable import (
    BaseFlowLandUserPlantMultiSelectToEditable)
from helpers import SessionContext  # noqa: F401
from helpers import TypeConversion  # noqa: F401


class FlowLandUserPlantMultiSelectToEditableResult():
    """
    Represents the result of the
    FlowLandUserPlantMultiSelectToEditable process.
    """

    context_object_code: uuid.UUID = uuid.UUID(int=0)

    def __init__(self):
        """
        Initializes a new instance of the
        FlowLandUserPlantMultiSelectToEditableResult class.
        """

    def to_json(self):
        """
        Converts the FlowLandUserPlantMultiSelectToEditableResult
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


class FlowLandUserPlantMultiSelectToEditable(
    BaseFlowLandUserPlantMultiSelectToEditable
):
    """
    FlowLandUserPlantMultiSelectToEditable handles the addition of
    a  to
    a specific land in the flow process.

    This class extends the
    BaseFlowLandUserPlantMultiSelectToEditableclass and
    initializes it with the provided session context.
    """

    async def process(
        self,
        land_bus_obj: LandBusObj,
        plant_code_list_csv: str = "",
# endset  # noqa: E122
    ) -> FlowLandUserPlantMultiSelectToEditableResult:
        """
        Processes the addition of a
         to a specific land.

        Returns:
            FlowLandUserPlantMultiSelectToEditableResult:
                The result of the
                FlowLandUserPlantMultiSelectToEditable process.
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
        result = FlowLandUserPlantMultiSelectToEditableResult()
        result.context_object_code = land_bus_obj.code

        super()._log_message_and_severity(
            LogSeverity.INFORMATION_HIGH_DETAIL,
            "Result:" + result.to_json())

        super()._log_message_and_severity(
            LogSeverity.INFORMATION_HIGH_DETAIL,
            "End")
        return result
