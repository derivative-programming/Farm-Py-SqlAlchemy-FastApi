from datetime import date, datetime
from decimal import Decimal
import uuid
from helpers import TypeConversion
from .post_reponse import PostResponse
from flows import FlowTacRegisterResult
from flows import FlowTacRegister
from helpers import SessionContext
from models import Tac
from flows import FlowValidationError
import apis.models as view_models
from helpers.pydantic_serialization import CamelModel,SnakeModel
from pydantic import Field,UUID4
import logging
from models import Tac
class TacRegisterPostModelResponse(PostResponse):
    customer_code:UUID4 = uuid.UUID(int=0)
    email:str = ""
    user_code_value:UUID4 = uuid.UUID(int=0)
    utc_offset_in_minutes:int = 0
    role_name_csv_list:str = ""
    api_key:str = ""

    def load_flow_response(self,data:FlowTacRegisterResult):
        placeholder = "" #to avoid pass line
        self.customer_code = data.customer_code
        self.email = data.email
        self.user_code_value = data.user_code_value
        self.utc_offset_in_minutes = data.utc_offset_in_minutes
        self.role_name_csv_list = data.role_name_csv_list
        self.api_key = data.api_key

### request. expect camel case. use marshmallow to validate.
class TacRegisterPostModelRequest(SnakeModel):
    email:str = ""
    password:str = ""
    confirmPassword:str = ""
    firstName:str = ""
    lastName:str = ""

    def process_request(self,
                        session_context:SessionContext,
                        tac_code:uuid,
                        response:TacRegisterPostModelResponse) -> TacRegisterPostModelResponse:
        try:
            logging.debug("loading model...")
            tac = Tac.objects.get(code=tac_code)
            flow = FlowTacRegister(session_context)
            logging.debug("process flow...")
            flowResponse = flow.process(
                tac,
                self.email,
                self.password,
                self.confirmPassword,
                self.firstName,
                self.lastName,

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

