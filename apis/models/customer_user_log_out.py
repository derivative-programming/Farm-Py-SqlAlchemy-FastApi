from datetime import date, datetime
from decimal import Decimal
import uuid
from helpers import TypeConversion
from .post_reponse import PostResponse
from flows import FlowCustomerUserLogOutResult
from flows import FlowCustomerUserLogOut
from helpers import SessionContext
from models import Customer
from flows import FlowValidationError
import apis.models as view_models
from helpers.pydantic_serialization import CamelModel,SnakeModel
from pydantic import Field,UUID4
import logging
from models import Customer
class CustomerUserLogOutPostModelResponse(PostResponse):

    def load_flow_response(self,data:FlowCustomerUserLogOutResult):
        placeholder = "" #to avoid pass line

### request. expect camel case. use marshmallow to validate.
class CustomerUserLogOutPostModelRequest(SnakeModel):

    def process_request(self,
                        session_context:SessionContext,
                        customer_code:uuid,
                        response:CustomerUserLogOutPostModelResponse) -> CustomerUserLogOutPostModelResponse:
        try:
            logging.debug("loading model...")
            customer = Customer.objects.get(code=customer_code)
            flow = FlowCustomerUserLogOut(session_context)
            logging.debug("process flow...")
            flowResponse = flow.process(
                customer,

            )
            response.load_flow_response(flowResponse);
            response.success = True
            response.message = "Success."
        except FlowValidationError as ve:
            response.success = False
            response.validation_errors = list()
            for key in ve.error_dict:
                response.validation_errors.append(view_models.ValidationError(key,ve.error_dict[key]))
        return response

