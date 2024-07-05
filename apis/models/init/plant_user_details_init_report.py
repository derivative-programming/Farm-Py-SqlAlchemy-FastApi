# apis/models/init/plant_user_details_init_report.py
# pylint: disable=unused-import

"""
This module contains the models and request/response classes
for the PlantUserDetailsInitReport workflow.
"""

import logging
import uuid  # noqa: F401
from datetime import date, datetime, timezone  # noqa: F401
from decimal import Decimal  # noqa: F401
from typing import List

from pydantic import Field

from apis.models.validation_error import ValidationErrorItem
from business.plant import PlantBusObj
from flows.base.flow_validation_error import FlowValidationError
from flows.plant_user_details_init_report import (
    FlowPlantUserDetailsInitReport,
    FlowPlantUserDetailsInitReportResult)
from helpers import SessionContext, TypeConversion  # noqa: F401
from helpers.formatting import snake_to_camel
from helpers.pydantic_serialization import CamelModel, SnakeModel


class PlantUserDetailsInitReportGetInitModelResponse(
    CamelModel
):
    """
    Represents the response model for the
    PlantUserDetailsInitReportGetInitModelRequest.
    """

    success: bool = Field(default=False, description="Success")
    message: str = Field(default="", description="Message")
    validation_errors: List[ValidationErrorItem] = Field(
        default_factory=list,
        alias="validationErrors",)
    land_code: uuid.UUID = Field(
        default_factory=lambda: uuid.UUID(
            '00000000-0000-0000-0000-000000000000'
        ),
        alias="landCode",
        description="Land Code")
    tac_code: uuid.UUID = Field(
        default_factory=lambda: uuid.UUID(
            '00000000-0000-0000-0000-000000000000'
        ),
        alias="tacCode",
        description="Tac Code")

    def load_flow_response(
        self,
        data: FlowPlantUserDetailsInitReportResult
    ):
        """
        Loads the response data from the
        FlowPlantUserDetailsInitReportResult object.
        """

        self.validation_errors = []
        self.success = False
        self.message = ""
        self.land_code = (
            data.land_code)
        self.tac_code = (
            data.tac_code)
    def to_json(self):
        """
        Serializes the response model to JSON.
        """

        return self.model_dump_json()


class PlantUserDetailsInitReportGetInitModelRequest(
    SnakeModel
):
    """
    Represents the request model for the
    PlantUserDetailsInitReportGetInitModelRequest.
    """

    async def process_request(
            self,
            session_context: SessionContext,
            plant_code: uuid.UUID,
            response:
            PlantUserDetailsInitReportGetInitModelResponse
    ) -> PlantUserDetailsInitReportGetInitModelResponse:
        """
        Processes the request and returns the response.
        """

        try:
            logging.info(
                "loading model..."
                "PlantUserDetailsInitReport"
                "GetInitModelRequest")
            plant_bus_obj = PlantBusObj(session_context)
            await plant_bus_obj.load_from_code(plant_code)
            if plant_bus_obj.get_plant_obj() is None:
                logging.info("Invalid plant_code")
                raise ValueError("Invalid plant_code")
            flow = FlowPlantUserDetailsInitReport(
                session_context)
            logging.info(
                "process request..."
                "PlantUserDetailsInitReport"
                "GetInitModelRequest")
            flow_response = await flow.process(
                plant_bus_obj
            )
            response.load_flow_response(flow_response)
            response.success = True
            response.message = "Success."
        except FlowValidationError as ve:
            logging.info(
                "error..."
                "PlantUserDetailsInitReport"
                "GetInitModelRequest")
            response.success = False
            response.validation_errors = []
            for key in ve.error_dict:
                val_error = ValidationErrorItem()
                val_error.property = snake_to_camel(key)
                val_error.message = ve.error_dict[key]
                response.validation_errors.append(val_error)
        return response
