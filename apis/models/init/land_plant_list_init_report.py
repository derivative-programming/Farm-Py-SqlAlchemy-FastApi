# apis/models/init/land_plant_list_init_report.py
# pylint: disable=unused-import

"""
This module contains the models and request/response classes
for the LandPlantListInitReport workflow.
"""

import logging
import uuid  # noqa: F401
from datetime import date, datetime  # noqa: F401
from decimal import Decimal  # noqa: F401
from typing import List

from pydantic import Field

from apis.models.validation_error import ValidationErrorItem
from business.land import LandBusObj
from flows.base.flow_validation_error import FlowValidationError
from flows.land_plant_list_init_report import (
    FlowLandPlantListInitReport,
    FlowLandPlantListInitReportResult)
from helpers import SessionContext, TypeConversion  # noqa: F401
from helpers.formatting import snake_to_camel
from helpers.pydantic_serialization import CamelModel, SnakeModel


class LandPlantListInitReportGetInitModelResponse(
    CamelModel
):
    """
    Represents the response model for the
    LandPlantListInitReportGetInitModelRequest.
    """

    success: bool = Field(default=False, description="Success")
    message: str = Field(default="", description="Message")
    validation_errors: List[ValidationErrorItem] = Field(default_factory=list)
    some_int_val: int = Field(
        default=0,
        description="Some Int Val")
    some_big_int_val: int = Field(
        default=0,
        description="Some Big Int Val")
    some_bit_val: bool = Field(
        default=False,
        description="Some Bit Val")
    is_edit_allowed: bool = Field(
        default=False,
        description="Is Edit Allowed")
    is_delete_allowed: bool = Field(
        default=False,
        description="Is Delete Allowed")
    some_float_val: float = Field(
        default=0,
        description="Some Float Val")
    some_decimal_val: Decimal = Field(
        default=Decimal(0),
        description="Some Decimal Val")
    some_min_utc_date_time_val: datetime = Field(
        default_factory=TypeConversion.get_default_date_time,
        description="Some Min UTC Date Time Val")
    some_min_date_val: date = Field(
        default_factory=TypeConversion.get_default_date,
        description="Some Min Date Val")
    some_money_val: Decimal = Field(
        default=Decimal(0),
        description="Some Money Val")
    some_n_var_char_val: str = Field(
        default="",
        description="Some N Var Char Val")
    some_var_char_val: str = Field(
        default="",
        description="Some Var Char Val")
    some_text_val: str = Field(
        default="",
        description="Some Text Val")
    some_phone_number: str = Field(
        default="",
        description="Some Phone Number")
    some_email_address: str = Field(
        default="",
        description="Some Email Address")
    land_code: uuid.UUID = Field(
        default_factory=lambda: uuid.UUID(
            '00000000-0000-0000-0000-000000000000'
        ),
        description="Land Code")
    tac_code: uuid.UUID = Field(
        default_factory=lambda: uuid.UUID(
            '00000000-0000-0000-0000-000000000000'
        ),
        description="Tac Code")
    land_name: str = Field(
        default="",
        description="Land Name")

    def load_flow_response(
        self,
        data: FlowLandPlantListInitReportResult
    ):
        """
        Loads the response data from the
        FlowLandPlantListInitReportResult object.
        """

        self.validation_errors = list()
        self.success = False
        self.message = ""
        self.some_int_val = (
            data.some_int_val)
        self.some_big_int_val = (
            data.some_big_int_val)
        self.some_bit_val = (
            data.some_bit_val)
        self.is_edit_allowed = (
            data.is_edit_allowed)
        self.is_delete_allowed = (
            data.is_delete_allowed)
        self.some_float_val = (
            data.some_float_val)
        self.some_decimal_val = (
            data.some_decimal_val)
        self.some_min_utc_date_time_val = (
            data.some_min_utc_date_time_val)
        self.some_min_date_val = (
            data.some_min_date_val)
        self.some_money_val = (
            data.some_money_val)
        self.some_n_var_char_val = (
            data.some_n_var_char_val)
        self.some_var_char_val = (
            data.some_var_char_val)
        self.some_text_val = (
            data.some_text_val)
        self.some_phone_number = (
            data.some_phone_number)
        self.some_email_address = (
            data.some_email_address)
        self.land_code = (
            data.land_code)
        self.tac_code = (
            data.tac_code)
        self.land_name = (
            data.land_name)
    def to_json(self):
        """
        Serializes the response model to JSON.
        """

        return self.model_dump_json()


class LandPlantListInitReportGetInitModelRequest(
    SnakeModel
):
    """
    Represents the request model for the
    LandPlantListInitReportGetInitModelRequest.
    """

    async def process_request(
            self,
            session_context: SessionContext,
            land_code: uuid.UUID,
            response:
            LandPlantListInitReportGetInitModelResponse
    ) -> LandPlantListInitReportGetInitModelResponse:
        """
        Processes the request and returns the response.
        """

        try:
            logging.info(
                "loading model..."
                "LandPlantListInitReport"
                "GetInitModelRequest")
            land_bus_obj = LandBusObj(session_context)
            await land_bus_obj.load_from_code(land_code)
            if land_bus_obj.get_land_obj() is None:
                logging.info("Invalid land_code")
                raise ValueError("Invalid land_code")
            flow = FlowLandPlantListInitReport(
                session_context)
            logging.info(
                "process request..."
                "LandPlantListInitReport"
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
                "LandPlantListInitReport"
                "GetInitModelRequest")
            response.success = False
            response.validation_errors = list()
            for key in ve.error_dict:
                val_error = ValidationErrorItem()
                val_error.property = snake_to_camel(key)
                val_error.message = ve.error_dict[key]
                response.validation_errors.append(val_error)
        return response
