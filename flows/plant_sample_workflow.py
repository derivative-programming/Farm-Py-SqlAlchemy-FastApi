# flows/default/plant_sample_workflow.py
# pylint: disable=unused-import
"""
This module contains the
FlowPlantSampleWorkflow class
and related classes
that handle the addition of a
 to a specific
plant in the flow process.
"""

import uuid  # noqa: F401
import json
from datetime import date, datetime, timezone  # noqa: F401
from decimal import Decimal  # noqa: F401
from flows.base.plant_sample_workflow import (
    BaseFlowPlantSampleWorkflow)
from flows.base import LogSeverity
from business.plant import PlantBusObj
from helpers import SessionContext  # noqa: F401
from helpers import TypeConversion  # noqa: F401


class FlowPlantSampleWorkflowResult():
    """
    Represents the result of the
    FlowPlantSampleWorkflow process.
    """

    context_object_code: uuid.UUID = uuid.UUID(int=0)

    def __init__(self):
        """
        Initializes a new instance of the
        FlowPlantSampleWorkflowResult class.
        """

    def to_json(self):
        """
        Converts the FlowPlantSampleWorkflowResult
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


class FlowPlantSampleWorkflow(
    BaseFlowPlantSampleWorkflow
):
    """
    FlowPlantSampleWorkflow handles the addition of
    a  to
    a specific plant in the flow process.

    This class extends the
    BaseFlowPlantSampleWorkflowclass and
    initializes it with the provided session context.
    """

    async def process(
        self,
        plant_bus_obj: PlantBusObj,

# endset  # noqa: E122
    ) -> FlowPlantSampleWorkflowResult:
        """
        Processes the addition of a
         to a specific plant.

        Returns:
            FlowPlantSampleWorkflowResult:
                The result of the
                FlowPlantSampleWorkflow process.
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

        # TODO: add flow logic


        super()._log_message_and_severity(
            LogSeverity.INFORMATION_HIGH_DETAIL,
            "Building result")
        result = FlowPlantSampleWorkflowResult()
        result.context_object_code = plant_bus_obj.code

        super()._log_message_and_severity(
            LogSeverity.INFORMATION_HIGH_DETAIL,
            "Result:" + result.to_json())

        super()._log_message_and_severity(
            LogSeverity.INFORMATION_HIGH_DETAIL,
            "End")
        return result
