from datetime import date, datetime
from decimal import Decimal
import json
import uuid
from helpers import TypeConversion
from .post_reponse import PostResponse
from flows.customer_user_log_out import FlowCustomerUserLogOut, FlowCustomerUserLogOutResult
from helpers import SessionContext
from business.customer import CustomerBusObj
from flows.base.flow_validation_error import FlowValidationError
import apis.models as view_models
from helpers.pydantic_serialization import CamelModel,SnakeModel
from pydantic import Field,UUID4
import logging
from apis.models.validation_error import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession
class CustomerUserLogOutPostModelRequest(SnakeModel):
    force_error_message:str = ""

class CustomerUserLogOutPostModelResponse(PostResponse):

    def load_flow_response(self,data:FlowCustomerUserLogOutResult):
        placeholder = "" #to avoid pass line

    async def process_request(self,
                        session:AsyncSession,
                        session_context:SessionContext,
                        customer_code:uuid,
                        request:CustomerUserLogOutPostModelRequest):
        try:
            logging.info("loading model...CustomerUserLogOutPostModelResponse")
            customer_bus_obj = CustomerBusObj(session=session)
            await customer_bus_obj.load(code=customer_code)
            flow = FlowCustomerUserLogOut(session_context)
            logging.info("process flow...CustomerUserLogOutPostModelResponse")
            flowResponse = await flow.process(
                customer_bus_obj,

            )
            self.load_flow_response(flowResponse);
            self.success = True
            self.message = "Success."
        except FlowValidationError as ve:
            logging.info("error...CustomerUserLogOutPostModelResponse")
            self.success = False
            self.validation_errors = list()
            for key in ve.error_dict:
                validation_error = ValidationError()
                validation_error.property = key
                validation_error.message = ve.error_dict[key]
                self.validation_errors.append(validation_error)
    def to_json(self):
        # Create a dictionary representation of the instance
        data = {
            #TODO finish to_json
        }
        # Serialize the dictionary to JSON
        return json.dumps(data)

