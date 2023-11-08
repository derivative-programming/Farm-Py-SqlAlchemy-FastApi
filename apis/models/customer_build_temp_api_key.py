from datetime import date, datetime
from decimal import Decimal
import uuid
from helpers import TypeConversion
from .post_reponse import PostResponse
from flows import FlowCustomerBuildTempApiKeyResult
from flows import FlowCustomerBuildTempApiKey
from helpers import SessionContext
from models import Customer
from flows import FlowValidationError
import apis.models as view_models
from helpers.pydantic_serialization import CamelModel,SnakeModel
from pydantic import Field,UUID4
import logging
from models import Customer
class CustomerBuildTempApiKeyPostModelResponse(PostResponse):
    tmp_org_api_key_code:UUID4 = uuid.UUID(int=0)

    def load_flow_response(self,data:FlowCustomerBuildTempApiKeyResult):
        placeholder = "" #to avoid pass line
        self.tmp_org_api_key_code = data.tmp_org_api_key_code

### request. expect camel case. use marshmallow to validate.
class CustomerBuildTempApiKeyPostModelRequest(SnakeModel):

    def process_request(self,
                        session_context:SessionContext,
                        customer_code:uuid,
                        response:CustomerBuildTempApiKeyPostModelResponse) -> CustomerBuildTempApiKeyPostModelResponse:
        try:
            logging.debug("loading model...")
            customer = Customer.objects.get(code=customer_code)
            flow = FlowCustomerBuildTempApiKey(session_context)
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

