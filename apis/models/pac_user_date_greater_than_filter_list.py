# apis/models/pac_user_date_greater_than_filter_list.py
"""
This module contains the models for the
Pac User Date Greater Than Filter List API.
- PacUserDateGreaterThanFilterListGetModelRequest: Represents the
    request model for getting the
    pac Pac User Date Greater Than Filter List Report.
- PacUserDateGreaterThanFilterListGetModelResponseItem: Represents the
    response model item for the
    pac Pac User Date Greater Than Filter List Report.
"""
import json
import logging
import uuid
from datetime import date, datetime
from decimal import Decimal
from typing import List
from pydantic import UUID4, Field
from apis.models.list_model import ListModel
from apis.models.validation_error import ValidationErrorItem
from helpers import SessionContext, TypeConversion
from helpers.formatting import snake_to_camel
from helpers.pydantic_serialization import CamelModel
from reports.pac_user_date_greater_than_filter_list import ReportManagerPacUserDateGreaterThanFilterList
from reports.report_request_validation_error import \
    ReportRequestValidationError
from reports.row_models.pac_user_date_greater_than_filter_list import ReportItemPacUserDateGreaterThanFilterList
class PacUserDateGreaterThanFilterListGetModelRequest(CamelModel):
    """
    Represents the request model for getting the
    pac Pac User Date Greater Than Filter List Report.
    """
    page_number: int = Field(
        default=0,
        description="Page Number")
    item_count_per_page: int = Field(
        default=0,
        description="Item Count Per Page")
    order_by_column_name: str = Field(
        default="",
        description="Order By Column Name")
    order_by_descending: bool = Field(
        default=False,
        description="Order By Descending")
    force_error_message: str = Field(
        default="",
        description="Force Error Message")

# endset
    class Config:
        """
        Configuration class for the
        PacUserDateGreaterThanFilterList model.
        Attributes:
            json_encoders (dict): A dictionary mapping data
            types to custom JSON encoder functions.
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
class PacUserDateGreaterThanFilterListGetModelResponseItem(CamelModel):
    """
    Represents the response model item for the
    pac Pac User Date Greater Than Filter List Report.
    """
    date_greater_than_filter_code: UUID4 = Field(
        default_factory=lambda: uuid.UUID(
            '00000000-0000-0000-0000-000000000000'
        ),
        description="Date Greater Than Filter Code")
    date_greater_than_filter_day_count: int = Field(
        default=0,
        description="Date Greater Than Filter Day Count")
    date_greater_than_filter_description: str = Field(
        default="",
        description="Date Greater Than Filter Description")
    date_greater_than_filter_display_order: int = Field(
        default=0,
        description="Date Greater Than Filter Display Order")
    date_greater_than_filter_is_active: bool = Field(
        default=False,
        description="Date Greater Than Filter Is Active")
    date_greater_than_filter_lookup_enum_name: str = Field(
        default="",
        description="Date Greater Than Filter Lookup Enum Name")
    date_greater_than_filter_name: str = Field(
        default="",
        description="Date Greater Than Filter Name")
# endset
    def load_report_item(self, data: ReportItemPacUserDateGreaterThanFilterList):
        """
        Loads the data from a ReportItemPacUserDateGreaterThanFilterList
        object into the response model item.
        Args:
            data (ReportItemPacUserDateGreaterThanFilterList): The
                ReportItemPacUserDateGreaterThanFilterList object to load the data from.
        """
        self.date_greater_than_filter_code = (
            data.date_greater_than_filter_code)
        self.date_greater_than_filter_day_count = (
            data.date_greater_than_filter_day_count)
        self.date_greater_than_filter_description = (
            data.date_greater_than_filter_description)
        self.date_greater_than_filter_display_order = (
            data.date_greater_than_filter_display_order)
        self.date_greater_than_filter_is_active = (
            data.date_greater_than_filter_is_active)
        self.date_greater_than_filter_lookup_enum_name = (
            data.date_greater_than_filter_lookup_enum_name)
        self.date_greater_than_filter_name = (
            data.date_greater_than_filter_name)
# endset
    def build_report_item(
        self
    ) -> ReportItemPacUserDateGreaterThanFilterList:
        """
        Builds a ReportItemPacUserDateGreaterThanFilterList object
        from the response model item.
        Returns:
            ReportItemPacUserDateGreaterThanFilterList: The built
            ReportItemPacUserDateGreaterThanFilterList object.
        """
        data = ReportItemPacUserDateGreaterThanFilterList()
        data.date_greater_than_filter_code = (
            self.date_greater_than_filter_code)
        data.date_greater_than_filter_day_count = (
            self.date_greater_than_filter_day_count)
        data.date_greater_than_filter_description = (
            self.date_greater_than_filter_description)
        data.date_greater_than_filter_display_order = (
            self.date_greater_than_filter_display_order)
        data.date_greater_than_filter_is_active = (
            self.date_greater_than_filter_is_active)
        data.date_greater_than_filter_lookup_enum_name = (
            self.date_greater_than_filter_lookup_enum_name)
        data.date_greater_than_filter_name = (
            self.date_greater_than_filter_name)
        return data
# endset
class PacUserDateGreaterThanFilterListGetModelResponse(ListModel):
    """
    Represents the response model for the
    PacUserDateGreaterThanFilterListGetModel API.
    Attributes:
        request (PacUserDateGreaterThanFilterListGetModelRequest):
            The request model for the API.
        items (List[PacUserDateGreaterThanFilterListGetModelResponseItem]):
            The list of response items.
    """
    request: PacUserDateGreaterThanFilterListGetModelRequest = PacUserDateGreaterThanFilterListGetModelRequest()
    items: List[PacUserDateGreaterThanFilterListGetModelResponseItem] = Field(
        default_factory=list)
    async def process_request(
        self,
        session_context: SessionContext,
        pac_code: uuid.UUID,
        request: PacUserDateGreaterThanFilterListGetModelRequest
    ):
        """
        Processes the API request and generates the response items.
        Args:
            session_context (SessionContext): The session context.
            pac_code (uuid.UUID): The pac code.
            request (PacUserDateGreaterThanFilterListGetModelRequest): The request model.
        Raises:
            ReportRequestValidationError: If there is
                a validation error in the request.
        Returns:
            None
        """
        try:
            logging.info("loading model...PacUserDateGreaterThanFilterListGetModelResponse")
            generator = ReportManagerPacUserDateGreaterThanFilterList(session_context)
            logging.info("processing...PacUserDateGreaterThanFilterListGetModelResponse")
            items = await generator.generate(
                pac_code,

# endset  # noqa: E122
                request.page_number,
                request.item_count_per_page,
                request.order_by_column_name,
                request.order_by_descending
            )
            self.items = list()
            for item in items:
                report_item = PacUserDateGreaterThanFilterListGetModelResponseItem()
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
