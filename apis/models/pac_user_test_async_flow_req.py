# apis/models/pac_user_test_async_flow_req.py  # pylint: disable=duplicate-code # noqa: E501
# pylint: disable=unused-import

"""
This module contains the models for the
Pac User Test Async Flow Req API.
"""

import json
import logging
import uuid  # noqa: F401
from datetime import date, datetime, timezone  # noqa: F401
from decimal import Decimal  # noqa: F401

from pydantic import UUID4, Field  # noqa: F401

from apis.models.validation_error import ValidationErrorItem
from business.pac import PacBusObj
from flows.base.flow_validation_error import FlowValidationError
from flows.pac_user_test_async_flow_req import (
    FlowPacUserTestAsyncFlowReq,
    FlowPacUserTestAsyncFlowReqResult)
from helpers import SessionContext, TypeConversion  # noqa: F401
from helpers.formatting import snake_to_camel, pascal_to_camel
from helpers.pydantic_serialization import CamelModel

from .post_reponse import PostResponse


class PacUserTestAsyncFlowReqPostModelRequest(CamelModel):
    """
    Represents the request model for the
    Pac User Test Async Flow Req API.
    """

    force_error_message: str = Field(
        default="",
        alias="forceErrorMessage",
        description="Force Error Message")


    class Config:  # pylint: disable=too-few-public-methods
        """
        Configuration class for the
        PacUserTestAsyncFlowReqPostModelRequest.
        """

        populate_by_name = True

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

        data = self.model_dump(by_alias=True)
        return data  # {pascal_to_camel(k): v for k, v in data.items()}

    def to_dict_camel_serialized(self):
        """
        Convert the model to a dictionary with camelCase
        keys and serialized values.
        """

        data = json.loads(self.model_dump_json(by_alias=True))
        return data  # {pascal_to_camel(k): v for k, v in data.items()}


class PacUserTestAsyncFlowReqPostModelResponse(PostResponse):
    """
    Represents the response model for the
    Pac User Test Async Flow Req API.
    """


    def load_flow_response(
            self, data: FlowPacUserTestAsyncFlowReqResult):
        """
        Loads the flow response data into the response model.
        """


    async def process_request(
        self,
        session_context: SessionContext,
        pac_code: uuid.UUID,
        request: PacUserTestAsyncFlowReqPostModelRequest
    ):  # pylint: disable=unused-argument
        """
        Processes the request and generates the response.
        """

        try:
            logging.info(
                "loading model..."
                "PacUserTestAsyncFlowReqPostModelResponse")
            pac_bus_obj = PacBusObj(session_context)
            await pac_bus_obj.load_from_code(code=pac_code)
            if pac_bus_obj.get_pac_obj() is None:
                logging.info("Invalid pac_code")
                raise ValueError("Invalid pac_code")
            flow = FlowPacUserTestAsyncFlowReq(
                session_context)
            logging.info(
                "process flow..."
                "PacUserTestAsyncFlowReqPostModelResponse")
            flow_response = await flow.process(
                pac_bus_obj,

# endset  # noqa: E122
            )
            self.load_flow_response(flow_response)
            self.success = True
            self.message = "Success."
        except FlowValidationError as ve:
            logging.info(
                "error..."
                "PacUserTestAsyncFlowReqPostModelResponse")
            self.success = False
            self.validation_errors = []
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
