# apis/models/tac_login.py
"""
    #TODO add comment
"""
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
from helpers.formatting import snake_to_camel
from helpers.pydantic_serialization import CamelModel,SnakeModel
from pydantic import Field, UUID4
import logging
from apis.models.validation_error import ValidationErrorItem
from sqlalchemy.ext.asyncio import AsyncSession
class TacLoginPostModelRequest(CamelModel):
    force_error_message: str = Field(default="", description="Force Error Message")
    email: str = Field(default="", description="Email")
    password: str = Field(default="", description="Password")

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
    def to_dict_snake(self):
        data = self.model_dump()
    def to_dict_snake_serialized(self):
        data = json.loads(self.model_dump_json())
    def to_dict_camel(self):
        data = self.model_dump()
        return {snake_to_camel(k): v for k, v in data.items()}
    def to_dict_camel_serialized(self):
        data = json.loads(self.model_dump_json())
        return {snake_to_camel(k): v for k, v in data.items()}
class TacLoginPostModelResponse(PostResponse):
    customer_code: UUID4 = Field(default=uuid.UUID(int=0), description="Customer Code")
    email: str = Field(default="", description="Output Some Email")
    user_code_value: UUID4 = Field(default=uuid.UUID(int=0), description="User Code Value")
    utc_offset_in_minutes: int = Field(default=0, description="UTC Offset In Minutes")
    role_name_csv_list: str = Field(default="", description="Output Some Role Name CSV List")
    api_key: str = Field(default="", description="Output Some Api Key")

    def load_flow_response(self, data:FlowTacLoginResult):
        placeholder = "" #to avoid pass line
        self.customer_code = data.customer_code
        self.email = data.email
        self.user_code_value = data.user_code_value
        self.utc_offset_in_minutes = data.utc_offset_in_minutes
        self.role_name_csv_list = data.role_name_csv_list
        self.api_key = data.api_key

    async def process_request(self,
                        session_context: SessionContext,
                        tac_code: uuid,
                        request: TacLoginPostModelRequest):
        try:
            logging.info("loading model...TacLoginPostModelResponse")
            tac_bus_obj = TacBusObj(session_context)
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
                validation_error = ValidationErrorItem()
                validation_error.property = snake_to_camel(key)
                validation_error.message = ve.error_dict[key]
                self.validation_errors.append(validation_error)
    def to_json(self):
        return self.model_dump_json()

