# apis/models/init/tac_register_init_obj_wf.py
# pylint: disable=unused-import

"""
This module contains the models and request/response classes
for the TacRegisterInitObjWF workflow.
"""

import logging
import uuid  # noqa: F401
from datetime import date, datetime, timezone  # noqa: F401
from decimal import Decimal  # noqa: F401
from typing import List

from pydantic import Field

from apis.models.validation_error import ValidationErrorItem
from business.tac import TacBusObj
from flows.base.flow_validation_error import FlowValidationError
from flows.tac_register_init_obj_wf import (
    FlowTacRegisterInitObjWF,
    FlowTacRegisterInitObjWFResult)
from helpers import SessionContext, TypeConversion  # noqa: F401
from helpers.formatting import snake_to_camel
from helpers.pydantic_serialization import CamelModel, SnakeModel


class TacRegisterInitObjWFGetInitModelResponse(
    CamelModel
):
    """
    Represents the response model for the
    TacRegisterInitObjWFGetInitModelRequest.
    """

    success: bool = Field(default=False, description="Success")
    message: str = Field(default="", description="Message")
    validation_errors: List[ValidationErrorItem] = Field(default_factory=list)
    email: str = Field(
        default="",
        description="Email")
    password: str = Field(
        default="",
        description="Password")
    confirm_password: str = Field(
        default="",
        description="Confirm Password")
    first_name: str = Field(
        default="",
        description="First Name")
    last_name: str = Field(
        default="",
        description="Last Name")

    def load_flow_response(
        self,
        data: FlowTacRegisterInitObjWFResult
    ):
        """
        Loads the response data from the
        FlowTacRegisterInitObjWFResult object.
        """

        self.validation_errors = list()
        self.success = False
        self.message = ""
        self.email = (
            data.email)
        self.password = (
            data.password)
        self.confirm_password = (
            data.confirm_password)
        self.first_name = (
            data.first_name)
        self.last_name = (
            data.last_name)
    def to_json(self):
        """
        Serializes the response model to JSON.
        """

        return self.model_dump_json()


class TacRegisterInitObjWFGetInitModelRequest(
    SnakeModel
):
    """
    Represents the request model for the
    TacRegisterInitObjWFGetInitModelRequest.
    """

    async def process_request(
            self,
            session_context: SessionContext,
            tac_code: uuid.UUID,
            response:
            TacRegisterInitObjWFGetInitModelResponse
    ) -> TacRegisterInitObjWFGetInitModelResponse:
        """
        Processes the request and returns the response.
        """

        try:
            logging.info(
                "loading model..."
                "TacRegisterInitObjWF"
                "GetInitModelRequest")
            tac_bus_obj = TacBusObj(session_context)
            await tac_bus_obj.load_from_code(tac_code)
            if tac_bus_obj.get_tac_obj() is None:
                logging.info("Invalid tac_code")
                raise ValueError("Invalid tac_code")
            flow = FlowTacRegisterInitObjWF(
                session_context)
            logging.info(
                "process request..."
                "TacRegisterInitObjWF"
                "GetInitModelRequest")
            flow_response = await flow.process(
                tac_bus_obj
            )
            response.load_flow_response(flow_response)
            response.success = True
            response.message = "Success."
        except FlowValidationError as ve:
            logging.info(
                "error..."
                "TacRegisterInitObjWF"
                "GetInitModelRequest")
            response.success = False
            response.validation_errors = list()
            for key in ve.error_dict:
                val_error = ValidationErrorItem()
                val_error.property = snake_to_camel(key)
                val_error.message = ve.error_dict[key]
                response.validation_errors.append(val_error)
        return response
