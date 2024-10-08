# apis/models/land_plant_list.py  # pylint: disable=duplicate-code # noqa: E501
# pylint: disable=unused-import

"""
This module contains the models for the
Land Plant List API.

- LandPlantListGetModelRequest: Represents the
    request model for getting the
    land plant list.
- LandPlantListGetModelResponseItem: Represents the
    response model item for the
    land plant list.
"""

import json
import logging
import uuid  # noqa: F401
from datetime import date, datetime, timezone  # noqa: F401
from decimal import Decimal  # noqa: F401
from typing import List

from pydantic import UUID4, Field

from apis.models.list_model import ListModel
from apis.models.validation_error import ValidationErrorItem
from helpers import SessionContext, TypeConversion  # noqa: F401
from helpers.formatting import snake_to_camel
from helpers.pydantic_serialization import CamelModel
from reports.land_plant_list import (
    ReportManagerLandPlantList)
from reports.report_request_validation_error import \
    ReportRequestValidationError
from reports.row_models.land_plant_list import (
    ReportItemLandPlantList)


class LandPlantListGetModelRequest(CamelModel):
    """
    Represents the request model for getting the
    land plant list.

    """

    page_number: int = Field(
        default=0,
        alias="pageNumber",
        description="Page Number")
    item_count_per_page: int = Field(
        default=0,
        alias="itemCountPerPage",
        description="Item Count Per Page")
    order_by_column_name: str = Field(
        default="",
        alias="orderByColumnName",
        description="Order By Column Name")
    order_by_descending: bool = Field(
        default=False,
        alias="orderByDescending",
        description="Order By Descending")
    force_error_message: str = Field(
        default="",
        alias="forceErrorMessage",
        description="Force Error Message")
    flavor_code: uuid.UUID = Field(
        default_factory=lambda: uuid.UUID(
            '00000000-0000-0000-0000-000000000000'
        ),
        alias="flavorCode",
        description="Flavor Code")
    some_int_val: int = Field(
        default=0,
        alias="someIntVal",
        description="Some Int Val")
    some_big_int_val: int = Field(
        default=0,
        alias="someBigIntVal",
        description="Some Big Int Val")
    some_float_val: float = Field(
        default=0,
        alias="someFloatVal",
        description="Some Float Val")
    some_bit_val: bool = Field(
        default=False,
        alias="someBitVal",
        description="Some Bit Val")
    is_edit_allowed: bool = Field(
        default=False,
        alias="isEditAllowed",
        description="Is Edit Allowed")
    is_delete_allowed: bool = Field(
        default=False,
        alias="isDeleteAllowed",
        description="Is Delete Allowed")
    some_decimal_val: Decimal = Field(
        default=Decimal(0),
        alias="someDecimalVal",
        description="Some Decimal Val")
    some_min_utc_date_time_val: datetime = Field(
        default_factory=TypeConversion.get_default_date_time,
        alias="someMinUTCDateTimeVal",
        description="Some Min UTC Date Time Val")
    some_min_date_val: date = Field(
        default_factory=TypeConversion.get_default_date,
        alias="someMinDateVal",
        description="Some Min Date Val")
    some_money_val: Decimal = Field(
        default=Decimal(0),
        alias="someMoneyVal",
        description="Some Money Val")
    some_n_var_char_val: str = Field(
        default="",
        alias="someNVarCharVal",
        description="Some N Var Char Val")
    some_var_char_val: str = Field(
        default="",
        alias="someVarCharVal",
        description="Some Var Char Val")
    some_text_val: str = Field(
        default="",
        alias="someTextVal",
        description="Some Text Val")
    some_phone_number: str = Field(
        default="",
        alias="somePhoneNumber",
        description="Some Phone Number")
    some_email_address: str = Field(
        default="",
        alias="someEmailAddress",
        description="Some Email Address")
# endset

    class Config:  # pylint: disable=too-few-public-methods
        """
        Configuration class for the
        LandPlantList model.

        Attributes:
            json_encoders (dict): A dictionary mapping data
            types to custom JSON encoder functions.
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
        return data  # {snake_to_camel(k): v for k, v in data.items()}

    def to_dict_camel_serialized(self):
        """
        Convert the model to a dictionary with camelCase
        keys and serialized values.
        """
        data = json.loads(self.model_dump_json(by_alias=True))
        return data  # {snake_to_camel(k): v for k, v in data.items()}


class LandPlantListGetModelResponseItem(CamelModel):
    """
    Represents the response model item for the
    land plant list.

    """

    plant_code: UUID4 = Field(
        default_factory=lambda: uuid.UUID(
            '00000000-0000-0000-0000-000000000000'
        ),
        alias="plantCode",
        description="Plant Code")
    some_int_val: int = Field(
        default=0,
        alias="someIntVal",
        description="Some Int Val")
    some_big_int_val: int = Field(
        default=0,
        alias="someBigIntVal",
        description="Some Big Int Val")
    some_bit_val: bool = Field(
        default=False,
        alias="someBitVal",
        description="Some Bit Val")
    is_edit_allowed: bool = Field(
        default=False,
        alias="isEditAllowed",
        description="Is Edit Allowed")
    is_delete_allowed: bool = Field(
        default=False,
        alias="isDeleteAllowed",
        description="Is Delete Allowed")
    some_float_val: float = Field(
        default=0,
        alias="someFloatVal",
        description="Some Float Val")
    some_decimal_val: Decimal = Field(
        default=Decimal(0),
        alias="someDecimalVal",
        description="Some Decimal Val")
    some_utc_date_time_val: datetime = Field(
        default_factory=TypeConversion.get_default_date_time,
        alias="someUTCDateTimeVal",
        description="Some UTC Date Time Val")
    some_date_val: date = Field(
        default_factory=TypeConversion.get_default_date,
        alias="someDateVal",
        description="Some Date Val")
    some_money_val: Decimal = Field(
        default=Decimal(0),
        alias="someMoneyVal",
        description="Some Money Val")
    some_n_var_char_val: str = Field(
        default="",
        alias="someNVarCharVal",
        description="Some N Var Char Val")
    some_var_char_val: str = Field(
        default="",
        alias="someVarCharVal",
        description="Some Var Char Val")
    some_text_val: str = Field(
        default="",
        alias="someTextVal",
        description="Some Text Val")
    some_phone_number: str = Field(
        default="",
        alias="somePhoneNumber",
        description="Some Phone Number")
    some_email_address: str = Field(
        default="",
        alias="someEmailAddress",
        description="Some Email Address")
    flavor_name: str = Field(
        default="",
        alias="flavorName",
        description="Flavor Name")
    flavor_code: UUID4 = Field(
        default_factory=lambda: uuid.UUID(
            '00000000-0000-0000-0000-000000000000'
        ),
        alias="flavorCode",
        description="Flavor Code")
    some_int_conditional_on_deletable: int = Field(
        default=0,
        alias="someIntConditionalOnDeletable",
        description="Some Int Conditional On Deleteable")
    n_var_char_as_url: str = Field(
        default="",
        alias="nVarCharAsUrl",
        description="N Var Char As Url")
    update_link_plant_code: UUID4 = Field(
        default_factory=lambda: uuid.UUID(
            '00000000-0000-0000-0000-000000000000'
        ),
        alias="updateLinkPlantCode",
        description="Update Link Plant Code")
    delete_async_button_link_plant_code: UUID4 = Field(
        default_factory=lambda: uuid.UUID(
            '00000000-0000-0000-0000-000000000000'
        ),
        alias="deleteAsyncButtonLinkPlantCode",
        description="Delete Async Button Link Plant Code")
    details_link_plant_code: UUID4 = Field(
        default_factory=lambda: uuid.UUID(
            '00000000-0000-0000-0000-000000000000'
        ),
        alias="detailsLinkPlantCode",
        description="Details Link Plant Code")
    test_file_download_link_pac_code: UUID4 = Field(
        default_factory=lambda: uuid.UUID(
            '00000000-0000-0000-0000-000000000000'
        ),
        alias="TestFileDownloadLinkPacCode",
        description="Test File Download Link Pac Code")
    test_conditional_file_download_link_pac_code: UUID4 = Field(
        default_factory=lambda: uuid.UUID(
            '00000000-0000-0000-0000-000000000000'
        ),
        alias="TestConditionalFileDownloadLinkPacCode",
        description="Test Conditional File Download Link Pac Code")
    test_async_flow_req_link_pac_code: UUID4 = Field(
        default_factory=lambda: uuid.UUID(
            '00000000-0000-0000-0000-000000000000'
        ),
        alias="TestAsyncFlowReqLinkPacCode",
        description="Test Async Flow Req Link Pac Code")
    test_conditional_async_flow_req_link_pac_code: UUID4 = Field(
        default_factory=lambda: uuid.UUID(
            '00000000-0000-0000-0000-000000000000'
        ),
        alias="TestConditionalAsyncFlowReqLinkPacCode",
        description="Test Conditional Async Flow Req Link Pac Code")
    conditional_btn_example_link_plant_code: UUID4 = Field(
        default_factory=lambda: uuid.UUID(
            '00000000-0000-0000-0000-000000000000'
        ),
        alias="ConditionalBtnExampleLinkPlantCode",
        description="Conditional Btn Example Link Plant Code")
# endset

    def load_report_item(
            self, data: ReportItemLandPlantList):
        """
        Loads the data from a
        ReportItemLandPlantList
        object into the response model item.

        Args:
            data (ReportItemLandPlantList): The
                ReportItemLandPlantList object
                to load the data from.
        """
        self.plant_code = (
            data.plant_code)
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
        self.some_utc_date_time_val = (
            data.some_utc_date_time_val)
        self.some_date_val = (
            data.some_date_val)
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
        self.flavor_name = (
            data.flavor_name)
        self.flavor_code = (
            data.flavor_code)
        self.some_int_conditional_on_deletable = (
            data.some_int_conditional_on_deletable)
        self.n_var_char_as_url = (
            data.n_var_char_as_url)
        self.update_link_plant_code = (
            data.update_link_plant_code)
        self.delete_async_button_link_plant_code = (
            data.delete_async_button_link_plant_code)
        self.details_link_plant_code = (
            data.details_link_plant_code)
        self.test_file_download_link_pac_code = (
            data.test_file_download_link_pac_code)
        self.test_conditional_file_download_link_pac_code = (
            data.test_conditional_file_download_link_pac_code)
        self.test_async_flow_req_link_pac_code = (
            data.test_async_flow_req_link_pac_code)
        self.test_conditional_async_flow_req_link_pac_code = (
            data.test_conditional_async_flow_req_link_pac_code)
        self.conditional_btn_example_link_plant_code = (
            data.conditional_btn_example_link_plant_code)
# endset

    def build_report_item(
        self
    ) -> ReportItemLandPlantList:
        """
        Builds a ReportItemLandPlantList object
        from the response model item.

        Returns:
            ReportItemLandPlantList: The built
            ReportItemLandPlantList object.
        """

        data = ReportItemLandPlantList()

        data.plant_code = (
            self.plant_code)
        data.some_int_val = (
            self.some_int_val)
        data.some_big_int_val = (
            self.some_big_int_val)
        data.some_bit_val = (
            self.some_bit_val)
        data.is_edit_allowed = (
            self.is_edit_allowed)
        data.is_delete_allowed = (
            self.is_delete_allowed)
        data.some_float_val = (
            self.some_float_val)
        data.some_decimal_val = (
            self.some_decimal_val)
        data.some_utc_date_time_val = (
            self.some_utc_date_time_val)
        data.some_date_val = (
            self.some_date_val)
        data.some_money_val = (
            self.some_money_val)
        data.some_n_var_char_val = (
            self.some_n_var_char_val)
        data.some_var_char_val = (
            self.some_var_char_val)
        data.some_text_val = (
            self.some_text_val)
        data.some_phone_number = (
            self.some_phone_number)
        data.some_email_address = (
            self.some_email_address)
        data.flavor_name = (
            self.flavor_name)
        data.flavor_code = (
            self.flavor_code)
        data.some_int_conditional_on_deletable = (
            self.some_int_conditional_on_deletable)
        data.n_var_char_as_url = (
            self.n_var_char_as_url)
        data.update_link_plant_code = (
            self.update_link_plant_code)
        data.delete_async_button_link_plant_code = (
            self.delete_async_button_link_plant_code)
        data.details_link_plant_code = (
            self.details_link_plant_code)
        data.test_file_download_link_pac_code = (
            self.test_file_download_link_pac_code)
        data.test_conditional_file_download_link_pac_code = (
            self.test_conditional_file_download_link_pac_code)
        data.test_async_flow_req_link_pac_code = (
            self.test_async_flow_req_link_pac_code)
        data.test_conditional_async_flow_req_link_pac_code = (
            self.test_conditional_async_flow_req_link_pac_code)
        data.conditional_btn_example_link_plant_code = (
            self.conditional_btn_example_link_plant_code)

        return data
# endset


class LandPlantListGetModelResponse(
    ListModel
):
    """
    Represents the response model for the
    LandPlantListGetModel API.

    Attributes:
        request (LandPlantListGetModelRequest):
            The request model for the API.
        items (List[LandPlantListGetModelResponseItem]):
            The list of response items.
    """

    request: LandPlantListGetModelRequest = (
        LandPlantListGetModelRequest())
    items: List[LandPlantListGetModelResponseItem] = Field(
        default_factory=list)

    async def process_request(
        self,
        session_context: SessionContext,
        land_code: uuid.UUID,
        request: LandPlantListGetModelRequest
    ):  # pylint: disable=unused-argument
        """
        Processes the API request and generates the response items.

        Args:
            session_context (SessionContext): The session context.
            land_code (uuid.UUID): The land code.
            request (LandPlantListGetModelRequest): The request model.

        Raises:
            ReportRequestValidationError: If there is
                a validation error in the request.

        Returns:
            None
        """
        try:
            logging.info(
                "loading model..."
                "LandPlantListGetModelResponse")
            generator = ReportManagerLandPlantList(
                session_context)
            logging.info(
                "processing..."
                "LandPlantListGetModelResponse")
            items = await generator.generate(
                land_code,
                request.flavor_code,
                request.some_int_val,
                request.some_big_int_val,
                request.some_float_val,
                request.some_bit_val,
                request.is_edit_allowed,
                request.is_delete_allowed,
                request.some_decimal_val,
                request.some_min_utc_date_time_val,
                request.some_min_date_val,
                request.some_money_val,
                request.some_n_var_char_val,
                request.some_var_char_val,
                request.some_text_val,
                request.some_phone_number,
                request.some_email_address,
# endset  # noqa: E122
                request.page_number,
                request.item_count_per_page,
                request.order_by_column_name,
                request.order_by_descending
            )
            self.items = []
            for item in items:
                report_item = \
                    LandPlantListGetModelResponseItem()
                report_item.load_report_item(item)
                self.items.append(report_item)
            self.success = True
            self.message = "Success."
        except ReportRequestValidationError as ve:
            self.success = False
            self.message = "Validation Error..."
            self.validation_errors = []

            error_messages = []

            for key, value in ve.error_dict.items():
                error_messages.append(value)
                validation_error = ValidationErrorItem()
                validation_error.property = snake_to_camel(key)
                validation_error.message = value
                self.validation_errors.append(validation_error)

            self.message = ','.join(error_messages)

    def to_json(self):
        """
        Converts the response model to JSON.

        Returns:
            str: The JSON representation of the response model.
        """
        return self.model_dump_json()
