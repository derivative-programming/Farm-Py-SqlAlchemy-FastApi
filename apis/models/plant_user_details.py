# apis/models/plant_user_details.py
# pylint: disable=unused-import

"""
This module contains the models for the
Plant User Details API.

- PlantUserDetailsGetModelRequest: Represents the
    request model for getting the
    plant Plant Details.
- PlantUserDetailsGetModelResponseItem: Represents the
    response model item for the
    plant Plant Details.
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
from reports.plant_user_details import (
    ReportManagerPlantUserDetails)
from reports.report_request_validation_error import \
    ReportRequestValidationError
from reports.row_models.plant_user_details import (
    ReportItemPlantUserDetails)


class PlantUserDetailsGetModelRequest(CamelModel):
    """
    Represents the request model for getting the
    plant Plant Details.

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


    class Config:
        """
        Configuration class for the
        PlantUserDetails model.

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


class PlantUserDetailsGetModelResponseItem(CamelModel):
    """
    Represents the response model item for the
    plant Plant Details.

    """
    flavor_name: str = Field(
        default="",
        alias="flavorName",
        description="Flavor Name")
    is_delete_allowed: bool = Field(
        default=False,
        alias="isDeleteAllowed",
        description="Is Delete Allowed")
    is_edit_allowed: bool = Field(
        default=False,
        alias="isEditAllowed",
        description="Is Edit Allowed")
    other_flavor: str = Field(
        default="",
        alias="otherFlavor",
        description="Other Flavor")
    some_big_int_val: int = Field(
        default=0,
        alias="someBigIntVal",
        description="Some Big Int Val")
    some_bit_val: bool = Field(
        default=False,
        alias="someBitVal",
        description="Some Bit Val")
    some_date_val: date = Field(
        default_factory=TypeConversion.get_default_date,
        alias="someDateVal",
        description="Some Date Val")
    some_decimal_val: Decimal = Field(
        default=Decimal(0),
        alias="someDecimalVal",
        description="Some Decimal Val")
    some_email_address: str = Field(
        default="",
        alias="someEmailAddress",
        description="Some Email Address")
    some_float_val: float = Field(
        default=0,
        alias="someFloatVal",
        description="Some Float Val")
    some_int_val: int = Field(
        default=0,
        alias="someIntVal",
        description="Some Int Val")
    some_money_val: Decimal = Field(
        default=Decimal(0),
        alias="someMoneyVal",
        description="Some Money Val")
    some_n_var_char_val: str = Field(
        default="",
        alias="someNVarCharVal",
        description="Some N Var Char Val")
    some_phone_number: str = Field(
        default="",
        alias="somePhoneNumber",
        description="Some Phone Number")
    some_text_val: str = Field(
        default="",
        alias="someTextVal",
        description="Some Text Val")
    some_uniqueidentifier_val: UUID4 = Field(
        default_factory=lambda: uuid.UUID(
            '00000000-0000-0000-0000-000000000000'
        ),
        alias="someUniqueidentifierVal",
        description="Some Uniqueidentifier Val")
    some_utc_date_time_val: datetime = Field(
        default_factory=TypeConversion.get_default_date_time,
        alias="someUTCDateTimeVal",
        description="Some UTC Date Time Val")
    some_var_char_val: str = Field(
        default="",
        alias="someVarCharVal",
        description="Some Var Char Val")
    phone_num_conditional_on_is_editable: str = Field(
        default="",
        alias="phoneNumConditionalOnIsEditable",
        description="Phone Num Conditional On Is Editable")
    n_var_char_as_url: str = Field(
        default="",
        alias="nVarCharAsUrl",
        description="N Var Char As Url")
    update_button_text_link_plant_code: UUID4 = Field(
        default_factory=lambda: uuid.UUID(
            '00000000-0000-0000-0000-000000000000'
        ),
        alias="updateButtonTextLinkPlantCode",
        description="Update Button Text Link Plant Code")
    random_property_updates_link_plant_code: UUID4 = Field(
        default_factory=lambda: uuid.UUID(
            '00000000-0000-0000-0000-000000000000'
        ),
        alias="randomPropertyUpdatesLinkPlantCode",
        description="Random Property Updates Link Plant Code")
    back_to_dashboard_link_tac_code: UUID4 = Field(
        default_factory=lambda: uuid.UUID(
            '00000000-0000-0000-0000-000000000000'
        ),
        alias="backToDashboardLinkTacCode",
        description="Back To Dashboard Link Tac Code")

    def load_report_item(
            self, data: ReportItemPlantUserDetails):
        """
        Loads the data from a
        ReportItemPlantUserDetails
        object into the response model item.

        Args:
            data (ReportItemPlantUserDetails): The
                ReportItemPlantUserDetails object
                to load the data from.
        """
        self.flavor_name = (
            data.flavor_name)
        self.is_delete_allowed = (
            data.is_delete_allowed)
        self.is_edit_allowed = (
            data.is_edit_allowed)
        self.other_flavor = (
            data.other_flavor)
        self.some_big_int_val = (
            data.some_big_int_val)
        self.some_bit_val = (
            data.some_bit_val)
        self.some_date_val = (
            data.some_date_val)
        self.some_decimal_val = (
            data.some_decimal_val)
        self.some_email_address = (
            data.some_email_address)
        self.some_float_val = (
            data.some_float_val)
        self.some_int_val = (
            data.some_int_val)
        self.some_money_val = (
            data.some_money_val)
        self.some_n_var_char_val = (
            data.some_n_var_char_val)
        self.some_phone_number = (
            data.some_phone_number)
        self.some_text_val = (
            data.some_text_val)
        self.some_uniqueidentifier_val = (
            data.some_uniqueidentifier_val)
        self.some_utc_date_time_val = (
            data.some_utc_date_time_val)
        self.some_var_char_val = (
            data.some_var_char_val)
        self.phone_num_conditional_on_is_editable = (
            data.phone_num_conditional_on_is_editable)
        self.n_var_char_as_url = (
            data.n_var_char_as_url)
        self.update_button_text_link_plant_code = (
            data.update_button_text_link_plant_code)
        self.random_property_updates_link_plant_code = (
            data.random_property_updates_link_plant_code)
        self.back_to_dashboard_link_tac_code = (
            data.back_to_dashboard_link_tac_code)

    def build_report_item(
        self
    ) -> ReportItemPlantUserDetails:
        """
        Builds a ReportItemPlantUserDetails object
        from the response model item.

        Returns:
            ReportItemPlantUserDetails: The built
            ReportItemPlantUserDetails object.
        """

        data = ReportItemPlantUserDetails()
        data.flavor_name = (
            self.flavor_name)
        data.is_delete_allowed = (
            self.is_delete_allowed)
        data.is_edit_allowed = (
            self.is_edit_allowed)
        data.other_flavor = (
            self.other_flavor)
        data.some_big_int_val = (
            self.some_big_int_val)
        data.some_bit_val = (
            self.some_bit_val)
        data.some_date_val = (
            self.some_date_val)
        data.some_decimal_val = (
            self.some_decimal_val)
        data.some_email_address = (
            self.some_email_address)
        data.some_float_val = (
            self.some_float_val)
        data.some_int_val = (
            self.some_int_val)
        data.some_money_val = (
            self.some_money_val)
        data.some_n_var_char_val = (
            self.some_n_var_char_val)
        data.some_phone_number = (
            self.some_phone_number)
        data.some_text_val = (
            self.some_text_val)
        data.some_uniqueidentifier_val = (
            self.some_uniqueidentifier_val)
        data.some_utc_date_time_val = (
            self.some_utc_date_time_val)
        data.some_var_char_val = (
            self.some_var_char_val)
        data.phone_num_conditional_on_is_editable = (
            self.phone_num_conditional_on_is_editable)
        data.n_var_char_as_url = (
            self.n_var_char_as_url)
        data.update_button_text_link_plant_code = (
            self.update_button_text_link_plant_code)
        data.random_property_updates_link_plant_code = (
            self.random_property_updates_link_plant_code)
        data.back_to_dashboard_link_tac_code = (
            self.back_to_dashboard_link_tac_code)
        return data


class PlantUserDetailsGetModelResponse(
    ListModel
):
    """
    Represents the response model for the
    PlantUserDetailsGetModel API.

    Attributes:
        request (PlantUserDetailsGetModelRequest):
            The request model for the API.
        items (List[PlantUserDetailsGetModelResponseItem]):
            The list of response items.
    """

    request: PlantUserDetailsGetModelRequest = (
        PlantUserDetailsGetModelRequest())
    items: List[PlantUserDetailsGetModelResponseItem] = Field(
        default_factory=list)

    async def process_request(
        self,
        session_context: SessionContext,
        plant_code: uuid.UUID,
        request: PlantUserDetailsGetModelRequest
    ):
        """
        Processes the API request and generates the response items.

        Args:
            session_context (SessionContext): The session context.
            plant_code (uuid.UUID): The plant code.
            request (PlantUserDetailsGetModelRequest): The request model.

        Raises:
            ReportRequestValidationError: If there is
                a validation error in the request.

        Returns:
            None
        """
        try:
            logging.info(
                "loading model..."
                "PlantUserDetailsGetModelResponse")
            generator = ReportManagerPlantUserDetails(
                session_context)
            logging.info(
                "processing..."
                "PlantUserDetailsGetModelResponse")
            items = await generator.generate(
                plant_code,

# endset  # noqa: E122
                request.page_number,
                request.item_count_per_page,
                request.order_by_column_name,
                request.order_by_descending
            )
            self.items = list()
            for item in items:
                report_item = \
                    PlantUserDetailsGetModelResponseItem()
                report_item.load_report_item(item)
                self.items.append(report_item)
            self.success = True
            self.message = "Success."
        except ReportRequestValidationError as ve:
            self.success = False
            self.message = "Validation Error..."
            self.validation_errors = list()

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
