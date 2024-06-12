# apis/models/error_log_config_resolve_error_log.py
"""
    #TODO add comment
"""
from datetime import date, datetime
from decimal import Decimal
import json
import uuid
from helpers import TypeConversion
from .post_reponse import PostResponse
from flows.error_log_config_resolve_error_log import FlowErrorLogConfigResolveErrorLog, FlowErrorLogConfigResolveErrorLogResult
from helpers import SessionContext
from business.error_log import ErrorLogBusObj
from flows.base.flow_validation_error import FlowValidationError
import apis.models as view_models
from helpers.formatting import snake_to_camel
from helpers.pydantic_serialization import CamelModel, SnakeModel
from pydantic import Field, UUID4
import logging
from apis.models.validation_error import ValidationErrorItem
from sqlalchemy.ext.asyncio import AsyncSession
class ErrorLogConfigResolveErrorLogPostModelRequest(CamelModel):
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
class ErrorLogConfigResolveErrorLogPostModelResponse(PostResponse):
    """
        #TODO add comment
    """

# endset
# endset
    def load_flow_response(self, data: FlowErrorLogConfigResolveErrorLogResult):
        """
            #TODO add comment
        """

# endset
    async def process_request(
        self,
        session_context: SessionContext,
        error_log_code: uuid.UUID,
        request: ErrorLogConfigResolveErrorLogPostModelRequest
    ):
        """
            #TODO add comment
        """
        try:
            logging.info("loading model...ErrorLogConfigResolveErrorLogPostModelResponse")
            error_log_bus_obj = ErrorLogBusObj(session_context)
            await error_log_bus_obj.load(code=error_log_code)
            if error_log_bus_obj.get_error_log_obj() is None:
                logging.info("Invalid error_log_code")
                raise ValueError("Invalid error_log_code")
            flow = FlowErrorLogConfigResolveErrorLog(session_context)
            logging.info("process flow...ErrorLogConfigResolveErrorLogPostModelResponse")
            flowResponse = await flow.process(
                error_log_bus_obj,

# endset
            )
            self.load_flow_response(flowResponse)
            self.success = True
            self.message = "Success."
        except FlowValidationError as ve:
            logging.info("error...ErrorLogConfigResolveErrorLogPostModelResponse")
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

