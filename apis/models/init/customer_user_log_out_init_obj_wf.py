# apis/models/init/customer_user_log_out_init_obj_wf.py
"""
    #TODO add comment
"""
import logging
import uuid
from datetime import date, datetime
from decimal import Decimal
from typing import List
from pydantic import Field
from apis.models.validation_error import ValidationErrorItem
from business.customer import CustomerBusObj
from flows.base.flow_validation_error import FlowValidationError
from flows.customer_user_log_out_init_obj_wf import (
    FlowCustomerUserLogOutInitObjWF,
    FlowCustomerUserLogOutInitObjWFResult)
from helpers import SessionContext, TypeConversion
from helpers.formatting import snake_to_camel
from helpers.pydantic_serialization import CamelModel, SnakeModel
class CustomerUserLogOutInitObjWFGetInitModelResponse(CamelModel):
    """
    #TODO add comment
    """
    success: bool = Field(default=False, description="Success")
    message: str = Field(default="", description="Message")
    validation_errors: List[ValidationErrorItem] = Field(default_factory=list)
    tac_code: uuid.UUID = Field(
        default_factory=lambda: uuid.UUID(
            '00000000-0000-0000-0000-000000000000'
        ),
        description="Tac Code")
# endset
    def load_flow_response(
        self,
        data: FlowCustomerUserLogOutInitObjWFResult
    ):
        """
            #TODO add comment
        """
        self.validation_errors = list()
        self.success = False
        self.message = ""
        self.tac_code = (
            data.tac_code)
    def to_json(self):
        """
            #TODO add comment
        """
        return self.model_dump_json()
class CustomerUserLogOutInitObjWFGetInitModelRequest(SnakeModel):
    """
    #TODO add comment
    """
    async def process_request(
            self,
            session_context: SessionContext,
            customer_code: uuid.UUID,
            response: CustomerUserLogOutInitObjWFGetInitModelResponse
    ) -> CustomerUserLogOutInitObjWFGetInitModelResponse:
        """
            #TODO add comment
        """
        try:
            logging.info(
                "loading model...CustomerUserLogOutInitObjWFGetInitModelRequest")
            customer_bus_obj = CustomerBusObj(session_context)
            await customer_bus_obj.load_from_code(customer_code)
            if customer_bus_obj.get_customer_obj() is None:
                logging.info("Invalid customer_code")
                raise ValueError("Invalid customer_code")
            flow = FlowCustomerUserLogOutInitObjWF(session_context)
            logging.info(
                "process request...CustomerUserLogOutInitObjWFGetInitModelRequest")
            flow_response = await flow.process(
                customer_bus_obj
            )
            response.load_flow_response(flow_response)
            response.success = True
            response.message = "Success."
        except FlowValidationError as ve:
            logging.info("error...CustomerUserLogOutInitObjWFGetInitModelRequest")
            response.success = False
            response.validation_errors = list()
            for key in ve.error_dict:
                val_error = ValidationErrorItem()
                val_error.property = snake_to_camel(key)
                val_error.message = ve.error_dict[key]
                response.validation_errors.append(val_error)
        return response

