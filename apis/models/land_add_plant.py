# apis/models/land_add_plant.py  # pylint: disable=duplicate-code # noqa: E501
# pylint: disable=unused-import

"""
This module contains the models for the
Land Add Plant API.
"""

import json
import logging
import uuid  # noqa: F401
from datetime import date, datetime, timezone  # noqa: F401
from decimal import Decimal  # noqa: F401

from pydantic import UUID4, Field  # noqa: F401

from apis.models.validation_error import ValidationErrorItem
from business.land import LandBusObj
from flows.base.flow_validation_error import FlowValidationError
from flows.land_add_plant import (
    FlowLandAddPlant,
    FlowLandAddPlantResult)
from helpers import SessionContext, TypeConversion  # noqa: F401
from helpers.formatting import snake_to_camel, pascal_to_camel
from helpers.pydantic_serialization import CamelModel

from .post_reponse import PostResponse


class LandAddPlantPostModelRequest(CamelModel):
    """
    Represents the request model for the
    Land Add Plant API.
    """

    force_error_message: str = Field(
        default="",
        alias="forceErrorMessage",
        description="Force Error Message")
    request_flavor_code: UUID4 = Field(
        default_factory=lambda: uuid.UUID(
            '00000000-0000-0000-0000-000000000000'
        ),
        alias="requestFlavorCode",
        description="Request Flavor Code")
    request_other_flavor: str = Field(
        default="",
        alias="requestOtherFlavor",
        description="Request Other Flavor")
    request_some_int_val: int = Field(
        default=0,
        alias="requestSomeIntVal",
        description="Request Some Int Val")
    request_some_big_int_val: int = Field(
        default=0,
        alias="requestSomeBigIntVal",
        description="Request Some Big Int Val")
    request_some_float_val: float = Field(
        default=0,
        alias="requestSomeFloatVal",
        description="Request Some Float Val")
    request_some_bit_val: bool = Field(
        default=False,
        alias="requestSomeBitVal",
        description="Request Some Bit Val")
    request_is_edit_allowed: bool = Field(
        default=False,
        alias="requestIsEditAllowed",
        description="Request Is Edit Allowed")
    request_is_delete_allowed: bool = Field(
        default=False,
        alias="requestIsDeleteAllowed",
        description="Request Is Delete Allowed")
    request_some_decimal_val: Decimal = Field(
        default=Decimal(0),
        alias="requestSomeDecimalVal",
        description="Request Some Decimal Val")
    request_some_utc_date_time_val: datetime = Field(
        default_factory=TypeConversion.get_default_date_time,
        alias="requestSomeUTCDateTimeVal",
        description="Request Some UTC Date Time Val")
    request_some_date_val: date = Field(
        default_factory=TypeConversion.get_default_date,
        alias="requestSomeDateVal",
        description="Request Some Date Val")
    request_some_money_val: Decimal = Field(
        default=Decimal(0),
        alias="requestSomeMoneyVal",
        description="Request Some Money Val")
    request_some_n_var_char_val: str = Field(
        default="",
        alias="requestSomeNVarCharVal",
        description="Request Some N Var Char Val")
    request_some_var_char_val: str = Field(
        default="",
        alias="requestSomeVarCharVal",
        description="Request Some Var Char Val")
    request_some_text_val: str = Field(
        default="",
        alias="requestSomeTextVal",
        description="Request Some Text Val")
    request_some_phone_number: str = Field(
        default="",
        alias="requestSomePhoneNumber",
        description="Request Some Phone Number")
    request_some_email_address: str = Field(
        default="",
        alias="requestSomeEmailAddress",
        description="Request Some Email Address")
    request_sample_image_upload_file: str = Field(
        default="",
        alias="requestSampleImageUploadFile",
        description="Request Sample Image Upload File")
# endset

    class Config:  # pylint: disable=too-few-public-methods
        """
        Configuration class for the
        LandAddPlantPostModelRequest.
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


class LandAddPlantPostModelResponse(PostResponse):
    """
    Represents the response model for the
    Land Add Plant API.
    """

    output_flavor_code: UUID4 = Field(
        default=uuid.UUID(int=0),
        alias="outputFlavorCode",
        description="Output Flavor Code")
    output_other_flavor: str = Field(
        default="",
        alias="outputOtherFlavor",
        description="Output Other Flavor")
    output_some_int_val: int = Field(
        default=0,
        alias="outputSomeIntVal",
        description="Output Some Int Val")
    output_some_big_int_val: int = Field(
        default=0,
        alias="outputSomeBigIntVal",
        description="Output Some Big Int Val")
    output_some_bit_val: bool = Field(
        default=False,
        alias="outputSomeBitVal",
        description="Output Some Bit Val")
    output_is_edit_allowed: bool = Field(
        default=False,
        alias="outputIsEditAllowed",
        description="Output Is Edit Allowed")
    output_is_delete_allowed: bool = Field(
        default=False,
        alias="outputIsDeleteAllowed",
        description="Output Is Delete Allowed")
    output_some_float_val: float = Field(
        default=0,
        alias="outputSomeFloatVal",
        description="Output Some Float Val")
    output_some_decimal_val: Decimal = Field(
        default=Decimal(0),
        alias="outputSomeDecimalVal",
        description="Output Some Decimal Val")
    output_some_utc_date_time_val: datetime = Field(
        default_factory=TypeConversion.get_default_date_time,
        alias="outputSomeUTCDateTimeVal",
        description="Output Some UTC Date Time Val")
    output_some_date_val: date = Field(
        default_factory=TypeConversion.get_default_date,
        alias="outputSomeDateVal",
        description="Output Some Date Val")
    output_some_money_val: Decimal = Field(
        default=Decimal(0),
        alias="outputSomeMoneyVal",
        description="Output Some Money Val")
    output_some_n_var_char_val: str = Field(
        default="",
        alias="outputSomeNVarCharVal",
        description="Output Some N Var Char Val")
    output_some_var_char_val: str = Field(
        default="",
        alias="outputSomeVarCharVal",
        description="Output Some Var Char Val")
    output_some_text_val: str = Field(
        default="",
        alias="outputSomeTextVal",
        description="Output Some Text Val")
    output_some_phone_number: str = Field(
        default="",
        alias="outputSomePhoneNumber",
        description="Output Some Phone Number")
    output_some_email_address: str = Field(
        default="",
        alias="outputSomeEmailAddress",
        description="Output Some Email Address")
    land_code: UUID4 = Field(
        default=uuid.UUID(int=0),
        alias="landCode",
        description="Land Code")
    plant_code: UUID4 = Field(
        default=uuid.UUID(int=0),
        alias="plantCode",
        description="Plant Code")
# endset

    def load_flow_response(
            self, data: FlowLandAddPlantResult):
        """
        Loads the flow response data into the response model.
        """

        self.output_flavor_code = data.land_code
        self.output_other_flavor = data.output_other_flavor
        self.output_some_int_val = data.output_some_int_val
        self.output_some_big_int_val = data.output_some_big_int_val
        self.output_some_bit_val = data.output_some_bit_val
        self.output_is_edit_allowed = data.output_is_edit_allowed
        self.output_is_delete_allowed = data.output_is_delete_allowed
        self.output_some_float_val = data.output_some_float_val
        self.output_some_decimal_val = data.output_some_decimal_val
        self.output_some_utc_date_time_val = data.output_some_utc_date_time_val
        self.output_some_date_val = data.output_some_date_val
        self.output_some_money_val = data.output_some_money_val
        self.output_some_n_var_char_val = data.output_some_n_var_char_val
        self.output_some_var_char_val = data.output_some_var_char_val
        self.output_some_text_val = data.output_some_text_val
        self.output_some_phone_number = data.output_some_phone_number
        self.output_some_email_address = data.output_some_email_address
        self.land_code = data.land_code
        self.plant_code = data.plant_code
# endset

    async def process_request(
        self,
        session_context: SessionContext,
        land_code: uuid.UUID,
        request: LandAddPlantPostModelRequest
    ):  # pylint: disable=unused-argument
        """
        Processes the request and generates the response.
        """

        try:
            logging.info(
                "loading model..."
                "LandAddPlantPostModelResponse")
            land_bus_obj = LandBusObj(session_context)
            await land_bus_obj.load_from_code(code=land_code)
            if land_bus_obj.get_land_obj() is None:
                logging.info("Invalid land_code")
                raise ValueError("Invalid land_code")
            flow = FlowLandAddPlant(
                session_context)
            logging.info(
                "process flow..."
                "LandAddPlantPostModelResponse")
            flow_response = await flow.process(
                land_bus_obj,
                request.request_flavor_code,
                request.request_other_flavor,
                request.request_some_int_val,
                request.request_some_big_int_val,
                request.request_some_bit_val,
                request.request_is_edit_allowed,
                request.request_is_delete_allowed,
                request.request_some_float_val,
                request.request_some_decimal_val,
                request.request_some_utc_date_time_val,
                request.request_some_date_val,
                request.request_some_money_val,
                request.request_some_n_var_char_val,
                request.request_some_var_char_val,
                request.request_some_text_val,
                request.request_some_phone_number,
                request.request_some_email_address,
                request.request_sample_image_upload_file
# endset  # noqa: E122
            )
            self.load_flow_response(flow_response)
            self.success = True
            self.message = "Success."
        except FlowValidationError as ve:
            logging.info(
                "error..."
                "LandAddPlantPostModelResponse")
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
