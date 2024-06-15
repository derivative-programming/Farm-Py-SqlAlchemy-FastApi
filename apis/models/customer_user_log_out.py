# apis/models/customer_user_log_out.py
"""
    #TODO add comment
"""
import json
import uuid
import logging
from datetime import date, datetime
from decimal import Decimal
from pydantic import Field, UUID4
from helpers import TypeConversion
from helpers import SessionContext
from flows.customer_user_log_out import FlowCustomerUserLogOut, FlowCustomerUserLogOutResult
from business.customer import CustomerBusObj
from flows.base.flow_validation_error import FlowValidationError
from helpers.formatting import snake_to_camel
from helpers.pydantic_serialization import CamelModel
from apis.models.validation_error import ValidationErrorItem
from .post_reponse import PostResponse
class CustomerUserLogOutPostModelRequest(CamelModel):
    """
        #TODO add comment
    """
    force_error_message: str = Field(
        default="",
        description="Force Error Message")

# endset
    class Config:
        """
            #TODO add comment
        """
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
    def to_dict_snake(self):
        """
            #TODO add comment
        """
        data = self.model_dump()
        return data
    def to_dict_snake_serialized(self):
        """
            #TODO add comment
        """
        data = json.loads(self.model_dump_json())
        return data
    def to_dict_camel(self):
        """
            #TODO add comment
        """
        data = self.model_dump()
        return {snake_to_camel(k): v for k, v in data.items()}
    def to_dict_camel_serialized(self):
        """
            #TODO add comment
        """
        data = json.loads(self.model_dump_json())
        return {snake_to_camel(k): v for k, v in data.items()}
class CustomerUserLogOutPostModelResponse(PostResponse):
    """
        #TODO add comment
    """

# endset
# endset
    def load_flow_response(self, data: FlowCustomerUserLogOutResult):
        """
            #TODO add comment
        """

# endset
    async def process_request(
        self,
        session_context: SessionContext,
        customer_code: uuid.UUID,
        request: CustomerUserLogOutPostModelRequest
    ):
        """
            #TODO add comment
        """
        try:
            logging.info("loading model...CustomerUserLogOutPostModelResponse")
            customer_bus_obj = CustomerBusObj(session_context)
            await customer_bus_obj.load_from_code(code=customer_code)
            if customer_bus_obj.get_customer_obj() is None:
                logging.info("Invalid customer_code")
                raise ValueError("Invalid customer_code")
            flow = FlowCustomerUserLogOut(session_context)
            logging.info("process flow...CustomerUserLogOutPostModelResponse")
            flow_response = await flow.process(
                customer_bus_obj,

# endset  # noqa: E122
            )
            self.load_flow_response(flow_response)
            self.success = True
            self.message = "Success."
        except FlowValidationError as ve:
            logging.info("error...CustomerUserLogOutPostModelResponse")
            self.success = False
            self.validation_errors = list()
            for key in ve.error_dict:
                validation_error = ValidationErrorItem()
                validation_error.property = snake_to_camel(key)
                validation_error.message = ve.error_dict[key]
                self.validation_errors.append(validation_error)
    def to_json(self):
        """
        #TODO add comment
        """
        return self.model_dump_json()

