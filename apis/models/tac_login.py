# apis/models/tac_login.py
"""
    #TODO add comment
"""
import json
import uuid
import logging
from datetime import date, datetime
from decimal import Decimal
from pydantic import Field, UUID4
from sqlalchemy.ext.asyncio import AsyncSession
from helpers import TypeConversion
from helpers import SessionContext
from flows.tac_login import FlowTacLogin, FlowTacLoginResult
from business.tac import TacBusObj
from flows.base.flow_validation_error import FlowValidationError
import apis.models as view_models
from helpers.formatting import snake_to_camel
from helpers.pydantic_serialization import CamelModel, SnakeModel
from apis.models.validation_error import ValidationErrorItem
from .post_reponse import PostResponse
class TacLoginPostModelRequest(CamelModel):
    """
        #TODO add comment
    """
    force_error_message: str = Field(
        default="",
        description="Force Error Message")
    email: str = Field(
        default="",
        description="Email")
    password: str = Field(
        default="",
        description="Password")
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
class TacLoginPostModelResponse(PostResponse):
    """
        #TODO add comment
    """
    customer_code: UUID4 = Field(
        default=uuid.UUID(int=0),
        description="Customer Code")
    email: str = Field(
        default="",
        description="Output Some Email")
    user_code_value: UUID4 = Field(
        default=uuid.UUID(int=0),
        description="User Code Value")
    utc_offset_in_minutes: int = Field(
        default=0,
        description="UTC Offset In Minutes")
    role_name_csv_list: str = Field(
        default="",
        description="Output Some Role Name CSV List")
    api_key: str = Field(
        default="",
        description="Output Some Api Key")
# endset
# endset
    def load_flow_response(self, data: FlowTacLoginResult):
        """
            #TODO add comment
        """
        self.customer_code = data.customer_code
        self.email = data.email
        self.user_code_value = data.user_code_value
        self.utc_offset_in_minutes = data.utc_offset_in_minutes
        self.role_name_csv_list = data.role_name_csv_list
        self.api_key = data.api_key
# endset
    async def process_request(
        self,
        session_context: SessionContext,
        tac_code: uuid.UUID,
        request: TacLoginPostModelRequest
    ):
        """
            #TODO add comment
        """
        try:
            logging.info("loading model...TacLoginPostModelResponse")
            tac_bus_obj = TacBusObj(session_context)
            await tac_bus_obj.load_from_code(code=tac_code)
            if tac_bus_obj.get_tac_obj() is None:
                logging.info("Invalid tac_code")
                raise ValueError("Invalid tac_code")
            flow = FlowTacLogin(session_context)
            logging.info("process flow...TacLoginPostModelResponse")
            flow_response = await flow.process(
                tac_bus_obj,
                request.email,
                request.password,
# endset  # noqa: E122
            )
            self.load_flow_response(flow_response)
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
        """
        #TODO add comment
        """
        return self.model_dump_json()

