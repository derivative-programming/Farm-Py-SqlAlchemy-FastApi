# apis/models/pac_user_date_greater_than_filter_list.py
"""
    #TODO add comment
"""
import json
from typing import List
from datetime import date, datetime
import uuid
import logging
from typing import Optional
from decimal import Decimal
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import Field, UUID4
from business.pac import PacBusObj
from helpers import TypeConversion
from reports.row_models.pac_user_date_greater_than_filter_list import ReportItemPacUserDateGreaterThanFilterList
from apis.models.list_model import ListModel
from helpers import SessionContext
from helpers.formatting import snake_to_camel
from models import Pac
from reports.pac_user_date_greater_than_filter_list import ReportManagerPacUserDateGreaterThanFilterList
from reports.report_request_validation_error import ReportRequestValidationError
from apis.models.validation_error import ValidationErrorItem
import apis.models as view_models
from helpers.pydantic_serialization import CamelModel, SnakeModel, BaseModel
class PacUserDateGreaterThanFilterListGetModelRequest(CamelModel):
    """
        #TODO add comment
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
        description="Order By Decending")
    force_error_message: str = Field(
        default="",
        description="Force Error Message")

# endset
    class Config:
        """
            #TODO add comment
        """
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
    def to_dict_snake(self):
        """
            #TODO add comment
        """
        data = self.model_dump()
        return data
    def to_dict_snake_serialized(self):
        """
            #TODO add comment
        """
        data = json.loads(self.model_dump_json())
        return data
    def to_dict_camel(self):
        """
            #TODO add comment
        """
        data = self.model_dump()
        return {snake_to_camel(k): v for k, v in data.items()}
    def to_dict_camel_serialized(self):
        """
            #TODO add comment
        """
        data = json.loads(self.model_dump_json())
        return {snake_to_camel(k): v for k, v in data.items()}
class PacUserDateGreaterThanFilterListGetModelResponseItem(CamelModel):
    """
        #TODO add comment
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
            #TODO add comment
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
class PacUserDateGreaterThanFilterListGetModelResponse(ListModel):
    """
        #TODO add comment
    """
    request: PacUserDateGreaterThanFilterListGetModelRequest = None
    items: List[PacUserDateGreaterThanFilterListGetModelResponseItem] = Field(
        default_factory=list)
    async def process_request(
        self,
        session_context: SessionContext,
        pac_code: uuid,
        request: PacUserDateGreaterThanFilterListGetModelRequest
    ):
        """
            #TODO add comment
        """
        try:
            logging.info("loading model...PacUserDateGreaterThanFilterListGetModelResponse")
            generator = ReportManagerPacUserDateGreaterThanFilterList(session_context)
            logging.info("processing...PacUserDateGreaterThanFilterListGetModelResponse")
            items = await generator.generate(
                pac_code,

# endset
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
            for key in ve.error_dict:
                self.message = self.message + ve.error_dict[key] + ','
                validation_error = ValidationErrorItem()
                validation_error.property = snake_to_camel(key)
                validation_error.message = ve.error_dict[key]
                self.validation_errors.append(validation_error)
    def to_json(self):
        """
            #TODO add comment
        """
        return self.model_dump_json()
