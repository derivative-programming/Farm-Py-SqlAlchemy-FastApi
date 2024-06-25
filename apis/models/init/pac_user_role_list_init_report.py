# apis/models/init/pac_user_role_list_init_report.py

"""
This module contains the models and request/response classes
for the PacUserRoleListInitReport workflow.
"""

import logging
import uuid
from datetime import date, datetime
from decimal import Decimal
from typing import List

from pydantic import Field

from apis.models.validation_error import ValidationErrorItem
from business.pac import PacBusObj
from flows.base.flow_validation_error import FlowValidationError
from flows.pac_user_role_list_init_report import (
    FlowPacUserRoleListInitReport,
    FlowPacUserRoleListInitReportResult)
from helpers import SessionContext, TypeConversion
from helpers.formatting import snake_to_camel
from helpers.pydantic_serialization import CamelModel, SnakeModel


class PacUserRoleListInitReportGetInitModelResponse(CamelModel):
    """
    Represents the response model for the
    PacUserRoleListInitReportGetInitModelRequest.
    """

    success: bool = Field(default=False, description="Success")
    message: str = Field(default="", description="Message")
    validation_errors: List[ValidationErrorItem] = Field(default_factory=list)


    def load_flow_response(
        self,
        data: FlowPacUserRoleListInitReportResult
    ):
        """
        Loads the response data from the
        FlowPacUserRoleListInitReportResult object.
        """

        self.validation_errors = list()
        self.success = False
        self.message = ""

    def to_json(self):
        """
        Serializes the response model to JSON.
        """

        return self.model_dump_json()


class PacUserRoleListInitReportGetInitModelRequest(SnakeModel):
    """
    Represents the request model for the
    PacUserRoleListInitReportGetInitModelRequest.
    """

    async def process_request(
            self,
            session_context: SessionContext,
            pac_code: uuid.UUID,
            response: PacUserRoleListInitReportGetInitModelResponse
    ) -> PacUserRoleListInitReportGetInitModelResponse:
        """
        Processes the request and returns the response.
        """

        try:
            logging.info(
                "loading model...PacUserRoleListInitReportGetInitModelRequest")
            pac_bus_obj = PacBusObj(session_context)
            await pac_bus_obj.load_from_code(pac_code)
            if pac_bus_obj.get_pac_obj() is None:
                logging.info("Invalid pac_code")
                raise ValueError("Invalid pac_code")
            flow = FlowPacUserRoleListInitReport(session_context)
            logging.info(
                "process request...PacUserRoleListInitReportGetInitModelRequest")
            flow_response = await flow.process(
                pac_bus_obj
            )
            response.load_flow_response(flow_response)
            response.success = True
            response.message = "Success."
        except FlowValidationError as ve:
            logging.info("error...PacUserRoleListInitReportGetInitModelRequest")
            response.success = False
            response.validation_errors = list()
            for key in ve.error_dict:
                val_error = ValidationErrorItem()
                val_error.property = snake_to_camel(key)
                val_error.message = ve.error_dict[key]
                response.validation_errors.append(val_error)
        return response

