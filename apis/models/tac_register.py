from datetime import date, datetime
from decimal import Decimal
import json
import uuid
from helpers import TypeConversion
from .post_reponse import PostResponse
from flows.tac_register import FlowTacRegister, FlowTacRegisterResult
from helpers import SessionContext
from business.tac import TacBusObj
from flows.base.flow_validation_error import FlowValidationError
import apis.models as view_models
from helpers.pydantic_serialization import CamelModel,SnakeModel
from pydantic import Field,UUID4
import logging
from apis.models.validation_error import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession
class TacRegisterPostModelRequest(SnakeModel):
    force_error_message:str = ""
    email:str = ""
    password:str = ""
    confirm_password:str = ""
    first_name:str = ""
    last_name:str = ""

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

    async def process_request(self,
                        session:AsyncSession,
                        session_context:SessionContext,
                        tac_code:uuid,
                        request:TacRegisterPostModelRequest):
        try:
            logging.info("loading model...TacRegisterPostModelResponse")
            tac_bus_obj = TacBusObj(session=session)
            await tac_bus_obj.load(code=tac_code)
            flow = FlowTacRegister(session_context)
            logging.info("process flow...TacRegisterPostModelResponse")
            flowResponse = await flow.process(
                tac_bus_obj,
                request.email,
                request.password,
                request.confirm_password,
                request.first_name,
                request.last_name,

            )
            self.load_flow_response(flowResponse);
            self.success = True
            self.message = "Success."
        except FlowValidationError as ve:
            logging.info("error...TacRegisterPostModelResponse")
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

