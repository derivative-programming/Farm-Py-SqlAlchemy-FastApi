# apis/models/init/land_add_plant_init_obj_wf.py  # pylint: disable=duplicate-code
# pylint: disable=unused-import

"""
This module contains the models and request/response classes
for the LandAddPlantInitObjWF workflow.
"""

import logging
import uuid  # noqa: F401
from datetime import date, datetime, timezone  # noqa: F401
from decimal import Decimal  # noqa: F401
from typing import List

from pydantic import Field

from apis.models.validation_error import ValidationErrorItem
from business.land import LandBusObj
from flows.base.flow_validation_error import FlowValidationError
from flows.land_add_plant_init_obj_wf import (
    FlowLandAddPlantInitObjWF,
    FlowLandAddPlantInitObjWFResult)
from helpers import SessionContext, TypeConversion  # noqa: F401
from helpers.formatting import snake_to_camel
from helpers.pydantic_serialization import CamelModel, SnakeModel


class LandAddPlantInitObjWFGetInitModelResponse(
    CamelModel
):
    """
    Represents the response model for the
    LandAddPlantInitObjWFGetInitModelRequest.
    """

    success: bool = Field(default=False, description="Success")
    message: str = Field(default="", description="Message")
    validation_errors: List[ValidationErrorItem] = Field(
        default_factory=list,
        alias="validationErrors",)
    request_flavor_code: uuid.UUID = Field(
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
    request_some_float_val: float = Field(
        default=0,
        alias="requestSomeFloatVal",
        description="Request Some Float Val")
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
    land_name: str = Field(
        default="",
        alias="landName",
        description="Land Name")
    tac_code: uuid.UUID = Field(
        default_factory=lambda: uuid.UUID(
            '00000000-0000-0000-0000-000000000000'
        ),
        alias="tacCode",
        description="Tac Code")
# endset

    def load_flow_response(
        self,
        data: FlowLandAddPlantInitObjWFResult
    ):
        """
        Loads the response data from the
        FlowLandAddPlantInitObjWFResult object.
        """

        self.validation_errors = []
        self.success = False
        self.message = ""
        self.request_flavor_code = (
            data.request_flavor_code)
        self.request_other_flavor = (
            data.request_other_flavor)
        self.request_some_int_val = (
            data.request_some_int_val)
        self.request_some_big_int_val = (
            data.request_some_big_int_val)
        self.request_some_bit_val = (
            data.request_some_bit_val)
        self.request_is_delete_allowed = (
            data.request_is_delete_allowed)
        self.request_is_edit_allowed = (
            data.request_is_edit_allowed)
        self.request_some_float_val = (
            data.request_some_float_val)
        self.request_some_decimal_val = (
            data.request_some_decimal_val)
        self.request_some_utc_date_time_val = (
            data.request_some_utc_date_time_val)
        self.request_some_date_val = (
            data.request_some_date_val)
        self.request_some_money_val = (
            data.request_some_money_val)
        self.request_some_n_var_char_val = (
            data.request_some_n_var_char_val)
        self.request_some_var_char_val = (
            data.request_some_var_char_val)
        self.request_some_text_val = (
            data.request_some_text_val)
        self.request_some_phone_number = (
            data.request_some_phone_number)
        self.request_some_email_address = (
            data.request_some_email_address)
        self.land_name = (
            data.land_name)
        self.tac_code = (
            data.tac_code)

    def to_json(self):
        """
        Serializes the response model to JSON.
        """

        return self.model_dump_json()


class LandAddPlantInitObjWFGetInitModelRequest(
    SnakeModel
):
    """
    Represents the request model for the
    LandAddPlantInitObjWFGetInitModelRequest.
    """

    async def process_request(
            self,
            session_context: SessionContext,
            land_code: uuid.UUID,
            response:
            LandAddPlantInitObjWFGetInitModelResponse
    ) -> LandAddPlantInitObjWFGetInitModelResponse:
        """
        Processes the request and returns the response.
        """

        try:
            logging.info(
                "loading model..."
                "LandAddPlantInitObjWF"
                "GetInitModelRequest")
            land_bus_obj = LandBusObj(session_context)
            await land_bus_obj.load_from_code(land_code)
            if land_bus_obj.get_land_obj() is None:
                logging.info("Invalid land_code")
                raise ValueError("Invalid land_code")
            flow = FlowLandAddPlantInitObjWF(
                session_context)
            logging.info(
                "process request..."
                "LandAddPlantInitObjWF"
                "GetInitModelRequest")
            flow_response = await flow.process(
                land_bus_obj
            )
            response.load_flow_response(flow_response)
            response.success = True
            response.message = "Success."
        except FlowValidationError as ve:
            logging.info(
                "error..."
                "LandAddPlantInitObjWF"
                "GetInitModelRequest")
            response.success = False
            response.validation_errors = []
            for key in ve.error_dict:
                val_error = ValidationErrorItem()
                val_error.property = snake_to_camel(key)
                val_error.message = ve.error_dict[key]
                response.validation_errors.append(val_error)
        return response
