# apis/models/init/customer_user_log_out_init_obj_wf.py  # pylint: disable=duplicate-code
# pylint: disable=unused-import

"""
This module contains the models and request/response classes
for the CustomerUserLogOutInitObjWF workflow.
"""

import logging
import uuid  # noqa: F401
from datetime import date, datetime, timezone  # noqa: F401
from decimal import Decimal  # noqa: F401
from typing import List

from pydantic import Field

from apis.models.validation_error import ValidationErrorItem
from business.customer import CustomerBusObj
from flows.base.flow_validation_error import FlowValidationError
from flows.customer_user_log_out_init_obj_wf import (
    FlowCustomerUserLogOutInitObjWF,
    FlowCustomerUserLogOutInitObjWFResult)
from helpers import SessionContext, TypeConversion  # noqa: F401
from helpers.formatting import snake_to_camel
from helpers.pydantic_serialization import CamelModel, SnakeModel


class CustomerUserLogOutInitObjWFGetInitModelResponse(
    CamelModel
):
    """
    Represents the response model for the
    CustomerUserLogOutInitObjWFGetInitModelRequest.
    """

    success: bool = Field(default=False, description="Success")
    message: str = Field(default="", description="Message")
    validation_errors: List[ValidationErrorItem] = Field(
        default_factory=list,
        alias="validationErrors",)
    tac_code: uuid.UUID = Field(
        default_factory=lambda: uuid.UUID(
            '00000000-0000-0000-0000-000000000000'
        ),
        alias="tacCode",
        description="Tac Code")

    def load_flow_response(
        self,
        data: FlowCustomerUserLogOutInitObjWFResult
    ):
        """
        Loads the response data from the
        FlowCustomerUserLogOutInitObjWFResult object.
        """

        self.validation_errors = []
        self.success = False
        self.message = ""
        self.tac_code = (
            data.tac_code)
    def to_json(self):
        """
        Serializes the response model to JSON.
        """

        return self.model_dump_json()


class CustomerUserLogOutInitObjWFGetInitModelRequest(
    SnakeModel
):
    """
    Represents the request model for the
    CustomerUserLogOutInitObjWFGetInitModelRequest.
    """

    async def process_request(
            self,
            session_context: SessionContext,
            customer_code: uuid.UUID,
            response:
            CustomerUserLogOutInitObjWFGetInitModelResponse
    ) -> CustomerUserLogOutInitObjWFGetInitModelResponse:
        """
        Processes the request and returns the response.
        """

        try:
            logging.info(
                "loading model..."
                "CustomerUserLogOutInitObjWF"
                "GetInitModelRequest")
            customer_bus_obj = CustomerBusObj(session_context)
            await customer_bus_obj.load_from_code(customer_code)
            if customer_bus_obj.get_customer_obj() is None:
                logging.info("Invalid customer_code")
                raise ValueError("Invalid customer_code")
            flow = FlowCustomerUserLogOutInitObjWF(
                session_context)
            logging.info(
                "process request..."
                "CustomerUserLogOutInitObjWF"
                "GetInitModelRequest")
            flow_response = await flow.process(
                customer_bus_obj
            )
            response.load_flow_response(flow_response)
            response.success = True
            response.message = "Success."
        except FlowValidationError as ve:
            logging.info(
                "error..."
                "CustomerUserLogOutInitObjWF"
                "GetInitModelRequest")
            response.success = False
            response.validation_errors = []
            for key in ve.error_dict:
                val_error = ValidationErrorItem()
                val_error.property = snake_to_camel(key)
                val_error.message = ve.error_dict[key]
                response.validation_errors.append(val_error)
        return response
