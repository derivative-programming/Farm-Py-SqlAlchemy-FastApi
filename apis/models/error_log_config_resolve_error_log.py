# apis/models/error_log_config_resolve_error_log.py
# pylint: disable=unused-import

"""
This module contains the models for the
Error Log Config Resolve Error Log API.
"""

import json
import logging
import uuid  # noqa: F401
from datetime import date, datetime  # noqa: F401
from decimal import Decimal  # noqa: F401

from pydantic import UUID4, Field  # noqa: F401

from apis.models.validation_error import ValidationErrorItem
from business.error_log import ErrorLogBusObj
from flows.base.flow_validation_error import FlowValidationError
from flows.error_log_config_resolve_error_log import (
    FlowErrorLogConfigResolveErrorLog,
    FlowErrorLogConfigResolveErrorLogResult)
from helpers import SessionContext, TypeConversion  # noqa: F401
from helpers.formatting import snake_to_camel
from helpers.pydantic_serialization import CamelModel

from .post_reponse import PostResponse


class ErrorLogConfigResolveErrorLogPostModelRequest(CamelModel):
    """
    Represents the request model for the
    Error Log Config Resolve Error Log API.
    """

    force_error_message: str = Field(
        default="",
        description="Force Error Message")


    class Config:
        """
        Configuration class for the
        ErrorLogConfigResolveErrorLogPostModelRequest.
        """

        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

    def to_dict_snake(self):
        """
        Convert the model to a dictionary with snake_case keys.
        """

        data = self.model_dump()
        return data

    def to_dict_snake_serialized(self):
        """
        Convert the model to a dictionary with snake_case
        keys and serialized values.
        """

        data = json.loads(self.model_dump_json())
        return data

    def to_dict_camel(self):
        """
        Convert the model to a dictionary with camelCase keys.
        """

        data = self.model_dump()
        return {snake_to_camel(k): v for k, v in data.items()}

    def to_dict_camel_serialized(self):
        """
        Convert the model to a dictionary with camelCase
        keys and serialized values.
        """

        data = json.loads(self.model_dump_json())
        return {snake_to_camel(k): v for k, v in data.items()}


class ErrorLogConfigResolveErrorLogPostModelResponse(PostResponse):
    """
    Represents the response model for the
    Error Log Config Resolve Error Log API.
    """


    def load_flow_response(
            self, data: FlowErrorLogConfigResolveErrorLogResult):
        """
        Loads the flow response data into the response model.
        """


    async def process_request(
        self,
        session_context: SessionContext,
        error_log_code: uuid.UUID,
        request: ErrorLogConfigResolveErrorLogPostModelRequest
    ):
        """
        Processes the request and generates the response.
        """

        try:
            logging.info(
                "loading model..."
                "ErrorLogConfigResolveErrorLogPostModelResponse")
            error_log_bus_obj = ErrorLogBusObj(session_context)
            await error_log_bus_obj.load_from_code(code=error_log_code)
            if error_log_bus_obj.get_error_log_obj() is None:
                logging.info("Invalid error_log_code")
                raise ValueError("Invalid error_log_code")
            flow = FlowErrorLogConfigResolveErrorLog(
                session_context)
            logging.info(
                "process flow..."
                "ErrorLogConfigResolveErrorLogPostModelResponse")
            flow_response = await flow.process(
                error_log_bus_obj,

# endset  # noqa: E122
            )
            self.load_flow_response(flow_response)
            self.success = True
            self.message = "Success."
        except FlowValidationError as ve:
            logging.info(
                "error..."
                "ErrorLogConfigResolveErrorLogPostModelResponse")
            self.success = False
            self.validation_errors = list()
            for key in ve.error_dict:
                validation_error = ValidationErrorItem()
                validation_error.property = snake_to_camel(key)
                validation_error.message = ve.error_dict[key]
                self.validation_errors.append(validation_error)

    def to_json(self):
        """
        Converts the object to a JSON representation.

        Returns:
            str: The JSON representation of the object.
        """
        return self.model_dump_json()
