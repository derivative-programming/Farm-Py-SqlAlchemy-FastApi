# apis/models/tac_register.py  # pylint: disable=duplicate-code
# pylint: disable=unused-import

"""
This module contains the models for the
Tac Register API.
"""

import json
import logging
import uuid  # noqa: F401
from datetime import date, datetime, timezone  # noqa: F401
from decimal import Decimal  # noqa: F401

from pydantic import UUID4, Field  # noqa: F401

from apis.models.validation_error import ValidationErrorItem
from business.tac import TacBusObj
from flows.base.flow_validation_error import FlowValidationError
from flows.tac_register import (
    FlowTacRegister,
    FlowTacRegisterResult)
from helpers import SessionContext, TypeConversion  # noqa: F401
from helpers.formatting import snake_to_camel, pascal_to_camel
from helpers.pydantic_serialization import CamelModel

from .post_reponse import PostResponse


class TacRegisterPostModelRequest(CamelModel):
    """
    Represents the request model for the
    Tac Register API.
    """

    force_error_message: str = Field(
        default="",
        alias="forceErrorMessage",
        description="Force Error Message")
    email: str = Field(
        default="",
        alias="email",
        description="Email")
    password: str = Field(
        default="",
        alias="password",
        description="Password")
    confirm_password: str = Field(
        default="",
        alias="confirmPassword",
        description="Confirm Password")
    first_name: str = Field(
        default="",
        alias="firstName",
        description="First Name")
    last_name: str = Field(
        default="",
        alias="lastName",
        description="Last Name")

    class Config:  # pylint: disable=too-few-public-methods
        """
        Configuration class for the
        TacRegisterPostModelRequest.
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


class TacRegisterPostModelResponse(PostResponse):
    """
    Represents the response model for the
    Tac Register API.
    """
    customer_code: UUID4 = Field(
        default=uuid.UUID(int=0),
        alias="customerCode",
        description="Customer Code")
    email: str = Field(
        default="",
        alias="email",
        description="Email")
    user_code_value: UUID4 = Field(
        default=uuid.UUID(int=0),
        alias="userCodeValue",
        description="User Code Value")
    utc_offset_in_minutes: int = Field(
        default=0,
        alias="uTCOffsetInMinutes",
        description="UTC Offset In Minutes")
    role_name_csv_list: str = Field(
        default="",
        alias="roleNameCSVList",
        description="Role Name CSV List")
    api_key: str = Field(
        default="",
        alias="apiKey",
        description="Api Key")

    def load_flow_response(
            self, data: FlowTacRegisterResult):
        """
        Loads the flow response data into the response model.
        """
        self.customer_code = data.customer_code
        self.email = data.email
        self.user_code_value = data.user_code_value
        self.utc_offset_in_minutes = data.utc_offset_in_minutes
        self.role_name_csv_list = data.role_name_csv_list
        self.api_key = data.api_key

    async def process_request(
        self,
        session_context: SessionContext,
        tac_code: uuid.UUID,
        request: TacRegisterPostModelRequest
    ):  # pylint: disable=unused-argument
        """
        Processes the request and generates the response.
        """

        try:
            logging.info(
                "loading model..."
                "TacRegisterPostModelResponse")
            tac_bus_obj = TacBusObj(session_context)
            await tac_bus_obj.load_from_code(code=tac_code)
            if tac_bus_obj.get_tac_obj() is None:
                logging.info("Invalid tac_code")
                raise ValueError("Invalid tac_code")
            flow = FlowTacRegister(
                session_context)
            logging.info(
                "process flow..."
                "TacRegisterPostModelResponse")
            flow_response = await flow.process(
                tac_bus_obj,
                request.email,
                request.password,
                request.confirm_password,
                request.first_name,
                request.last_name,
# endset  # noqa: E122
            )
            self.load_flow_response(flow_response)
            self.success = True
            self.message = "Success."
        except FlowValidationError as ve:
            logging.info(
                "error..."
                "TacRegisterPostModelResponse")
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
