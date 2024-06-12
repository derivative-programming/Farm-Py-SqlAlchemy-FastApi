# apis/models/init/land_add_plant_init_obj_wf.py

"""
    #TODO add comment
"""

from datetime import date, datetime
from decimal import Decimal
import json
from typing import List
import uuid
from apis.models import validation_error
from helpers import TypeConversion
from flows.land_add_plant_init_obj_wf import FlowLandAddPlantInitObjWFResult, FlowLandAddPlantInitObjWF
from helpers import SessionContext
from helpers.formatting import snake_to_camel
from business.land import LandBusObj
from flows.base.flow_validation_error import FlowValidationError
from helpers.pydantic_serialization import CamelModel, SnakeModel
from pydantic import Field
from apis.models.validation_error import ValidationErrorItem
import logging
from sqlalchemy.ext.asyncio import AsyncSession


class LandAddPlantInitObjWFGetInitModelResponse(CamelModel):
    """
    #TODO add comment
    """
    success: bool = Field(default=False, description="Success")
    message: str = Field(default="", description="Message")
    validation_errors: List[ValidationErrorItem] = Field(default_factory=list)
    request_flavor_code: uuid.UUID = Field(
        default_factory=lambda: uuid.UUID(
            '00000000-0000-0000-0000-000000000000'
        ),
        description="Request Flavor Code")
    request_other_flavor: str = Field(
        default="",
        description="Request Other Flavor")
    request_some_int_val: int = Field(
        default=0,
        description="Request Some Int Val")
    request_some_big_int_val: int = Field(
        default=0,
        description="Request Some Big Int Val")
    request_some_bit_val: bool = Field(
        default=False,
        description="Request Some Bit Val")
    request_is_edit_allowed: bool = Field(
        default=False,
        description="Request Is Edit Allowed")
    request_is_delete_allowed: bool = Field(
        default=False,
        description="Request Is Delete Allowed")
    request_some_float_val: float = Field(
        default=0,
        description="Request Some Float Val")
    request_some_decimal_val: Decimal = Field(
        default=Decimal(0),
        description="Request Some Decimal Val")
    request_some_utc_date_time_val: datetime = Field(
        default_factory=TypeConversion.get_default_date_time,
        description="Request Some UTC Date Time Val")
    request_some_date_val: date = Field(
        default_factory=TypeConversion.get_default_date,
        description="Request Some Date Val")
    request_some_money_val: Decimal = Field(
        default=Decimal(0),
        description="Request Some Money Val")
    request_some_n_var_char_val: str = Field(
        default="",
        description="Request Some N Var Char Val")
    request_some_var_char_val: str = Field(
        default="",
        description="Request Some Var Char Val")
    request_some_text_val: str = Field(
        default="",
        description="Request Some Text Val")
    request_some_phone_number: str = Field(
        default="",
        description="Request Some Phone Number")
    request_some_email_address: str = Field(
        default="",
        description="Request Some Email Address")
    land_name: str = Field(
        default="",
        description="Land Name")
    tac_code: uuid.UUID = Field(
        default_factory=lambda: uuid.UUID(
            '00000000-0000-0000-0000-000000000000'
        ),
        description="Tac Code")
# endset

    def load_flow_response(
        self,
        data: FlowLandAddPlantInitObjWFResult
    ):
        self.validation_errors = list()
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
        return self.model_dump_json()


class LandAddPlantInitObjWFGetInitModelRequest(SnakeModel):
    """
    #TODO add comment
    """
    async def process_request(
            self,
            session_context: SessionContext,
            land_code: uuid,
            response: LandAddPlantInitObjWFGetInitModelResponse
    ) -> LandAddPlantInitObjWFGetInitModelResponse:
        try:
            logging.info(
                "loading model...LandAddPlantInitObjWFGetInitModelRequest")
            land_bus_obj = LandBusObj(session_context)
            await land_bus_obj.load(code=land_code)
            if land_bus_obj.get_land_obj() is None:
                logging.info("Invalid land_code")
                raise ValueError("Invalid land_code")
            flow = FlowLandAddPlantInitObjWF(session_context)
            logging.info(
                "process request...LandAddPlantInitObjWFGetInitModelRequest")
            flowResponse = await flow.process(
                land_bus_obj
            )
            response.load_flow_response(flowResponse)
            response.success = True
            response.message = "Success."
        except FlowValidationError as ve:
            logging.info("error...LandAddPlantInitObjWFGetInitModelRequest")
            response.success = False
            response.validation_errors = list()
            for key in ve.error_dict:
                val_error = ValidationErrorItem()
                val_error.property = snake_to_camel(key)
                val_error.message = ve.error_dict[key]
                response.validation_errors.append(val_error)
        return response
