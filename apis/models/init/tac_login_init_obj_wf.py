# apis/models/init/tac_login_init_obj_wf.py

"""
This module contains the models and request/response classes
for the TacLoginInitObjWF workflow.
"""

import logging
import uuid
from datetime import date, datetime
from decimal import Decimal
from typing import List

from pydantic import Field

from apis.models.validation_error import ValidationErrorItem
from business.tac import TacBusObj
from flows.base.flow_validation_error import FlowValidationError
from flows.tac_login_init_obj_wf import (
    FlowTacLoginInitObjWF,
    FlowTacLoginInitObjWFResult)
from helpers import SessionContext, TypeConversion
from helpers.formatting import snake_to_camel
from helpers.pydantic_serialization import CamelModel, SnakeModel


class TacLoginInitObjWFGetInitModelResponse(
    CamelModel
):
    """
    Represents the response model for the
    TacLoginInitObjWFGetInitModelRequest.
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

    def load_flow_response(
        self,
        data: FlowTacLoginInitObjWFResult
    ):
        """
        Loads the response data from the
        FlowTacLoginInitObjWFResult object.
        """

        self.validation_errors = list()
        self.success = False
        self.message = ""
        self.email = (
            data.email)
        self.password = (
            data.password)
    def to_json(self):
        """
        Serializes the response model to JSON.
        """

        return self.model_dump_json()


class TacLoginInitObjWFGetInitModelRequest(SnakeModel):
    """
    Represents the request model for the
    TacLoginInitObjWFGetInitModelRequest.
    """

    async def process_request(
            self,
            session_context: SessionContext,
            tac_code: uuid.UUID,
            response: TacLoginInitObjWFGetInitModelResponse
    ) -> TacLoginInitObjWFGetInitModelResponse:
        """
        Processes the request and returns the response.
        """

        try:
            logging.info(
                "loading model...TacLoginInitObjWFGetInitModelRequest")
            tac_bus_obj = TacBusObj(session_context)
            await tac_bus_obj.load_from_code(tac_code)
            if tac_bus_obj.get_tac_obj() is None:
                logging.info("Invalid tac_code")
                raise ValueError("Invalid tac_code")
            flow = FlowTacLoginInitObjWF(session_context)
            logging.info(
                "process request...TacLoginInitObjWFGetInitModelRequest")
            flow_response = await flow.process(
                tac_bus_obj
            )
            response.load_flow_response(flow_response)
            response.success = True
            response.message = "Success."
        except FlowValidationError as ve:
            logging.info("error...TacLoginInitObjWFGetInitModelRequest")
            response.success = False
            response.validation_errors = list()
            for key in ve.error_dict:
                val_error = ValidationErrorItem()
                val_error.property = snake_to_camel(key)
                val_error.message = ve.error_dict[key]
                response.validation_errors.append(val_error)
        return response

