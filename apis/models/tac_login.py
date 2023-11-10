from datetime import date, datetime
from decimal import Decimal
import json
import uuid
from helpers import TypeConversion
from .post_reponse import PostResponse
from flows.tac_login import FlowTacLogin, FlowTacLoginResult
from helpers import SessionContext
from business.tac import TacBusObj
from flows.base.flow_validation_error import FlowValidationError
import apis.models as view_models
from helpers.pydantic_serialization import CamelModel,SnakeModel
from pydantic import Field,UUID4
import logging
from apis.models.validation_error import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession
class TacLoginPostModelRequest(SnakeModel):
    force_error_message:str = ""
    email:str = ""
    password:str = ""

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
    def to_dict_snake(self):
        data = self.model_dump()
    def to_dict_snake_serialized(self):
        data = json.loads(self.model_dump_json() )
    def _to_camel(self,string: str) -> str:
        return ''.join(word.capitalize() if i != 0 else word for i, word in enumerate(string.split('_')))
    def to_dict_camel(self):
        data = self.model_dump()
        return {self._to_camel(k): v for k, v in data.items()}
    def to_dict_camel_serialized(self):
        data = json.loads(self.model_dump_json() )
        return {self._to_camel(k): v for k, v in data.items()}
class TacLoginPostModelResponse(PostResponse):
    customer_code:UUID4 = uuid.UUID(int=0)
    email:str = ""
    user_code_value:UUID4 = uuid.UUID(int=0)
    utc_offset_in_minutes:int = 0
    role_name_csv_list:str = ""
    api_key:str = ""

    def load_flow_response(self,data:FlowTacLoginResult):
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
                        request:TacLoginPostModelRequest):
        try:
            logging.info("loading model...TacLoginPostModelResponse")
            tac_bus_obj = TacBusObj(session=session)
            await tac_bus_obj.load(code=tac_code)
            if(tac_bus_obj.get_tac_obj() is None):
                logging.info("Invalid tac_code")
                raise ValueError("Invalid tac_code")
            flow = FlowTacLogin(session_context)
            logging.info("process flow...TacLoginPostModelResponse")
            flowResponse = await flow.process(
                tac_bus_obj,
                request.email,
                request.password,

            )
            self.load_flow_response(flowResponse);
            self.success = True
            self.message = "Success."
        except FlowValidationError as ve:
            logging.info("error...TacLoginPostModelResponse")
            self.success = False
            self.validation_errors = list()
            for key in ve.error_dict:
                validation_error = ValidationError()
                validation_error.property = key
                validation_error.message = ve.error_dict[key]
                self.validation_errors.append(validation_error)
    def to_json(self):
        return self.model_dump_json()

