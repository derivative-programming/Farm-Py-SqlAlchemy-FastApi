# apis/models/pac_user_tri_state_filter_list.py
"""
    #TODO add comment
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
from reports.pac_user_tri_state_filter_list import ReportManagerPacUserTriStateFilterList
from reports.report_request_validation_error import \
    ReportRequestValidationError
from reports.row_models.pac_user_tri_state_filter_list import ReportItemPacUserTriStateFilterList
class PacUserTriStateFilterListGetModelRequest(CamelModel):
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
class PacUserTriStateFilterListGetModelResponseItem(CamelModel):
    """
        #TODO add comment
    """
    tri_state_filter_code: UUID4 = Field(
        default_factory=lambda: uuid.UUID(
            '00000000-0000-0000-0000-000000000000'
        ),
        description="Tri State Filter Code")
    tri_state_filter_description: str = Field(
        default="",
        description="Tri State Filter Description")
    tri_state_filter_display_order: int = Field(
        default=0,
        description="Tri State Filter Display Order")
    tri_state_filter_is_active: bool = Field(
        default=False,
        description="Tri State Filter Is Active")
    tri_state_filter_lookup_enum_name: str = Field(
        default="",
        description="Tri State Filter Lookup Enum Name")
    tri_state_filter_name: str = Field(
        default="",
        description="Tri State Filter Name")
    tri_state_filter_state_int_value: int = Field(
        default=0,
        description="Tri State Filter State Int Value")
# endset
    def load_report_item(self, data: ReportItemPacUserTriStateFilterList):
        """
            #TODO add comment
        """
        self.tri_state_filter_code = (
            data.tri_state_filter_code)
        self.tri_state_filter_description = (
            data.tri_state_filter_description)
        self.tri_state_filter_display_order = (
            data.tri_state_filter_display_order)
        self.tri_state_filter_is_active = (
            data.tri_state_filter_is_active)
        self.tri_state_filter_lookup_enum_name = (
            data.tri_state_filter_lookup_enum_name)
        self.tri_state_filter_name = (
            data.tri_state_filter_name)
        self.tri_state_filter_state_int_value = (
            data.tri_state_filter_state_int_value)
# endset
    def build_report_item(
        self
    ) -> ReportItemPacUserTriStateFilterList:
        """
            #TODO add comment
        """
        data = ReportItemPacUserTriStateFilterList()
        data.tri_state_filter_code = (
            self.tri_state_filter_code)
        data.tri_state_filter_description = (
            self.tri_state_filter_description)
        data.tri_state_filter_display_order = (
            self.tri_state_filter_display_order)
        data.tri_state_filter_is_active = (
            self.tri_state_filter_is_active)
        data.tri_state_filter_lookup_enum_name = (
            self.tri_state_filter_lookup_enum_name)
        data.tri_state_filter_name = (
            self.tri_state_filter_name)
        data.tri_state_filter_state_int_value = (
            self.tri_state_filter_state_int_value)
        return data
# endset
class PacUserTriStateFilterListGetModelResponse(ListModel):
    """
        #TODO add comment
    """
    request: PacUserTriStateFilterListGetModelRequest = PacUserTriStateFilterListGetModelRequest()
    items: List[PacUserTriStateFilterListGetModelResponseItem] = Field(
        default_factory=list)
    async def process_request(
        self,
        session_context: SessionContext,
        pac_code: uuid.UUID,
        request: PacUserTriStateFilterListGetModelRequest
    ):
        """
            #TODO add comment
        """
        try:
            logging.info("loading model...PacUserTriStateFilterListGetModelResponse")
            generator = ReportManagerPacUserTriStateFilterList(session_context)
            logging.info("processing...PacUserTriStateFilterListGetModelResponse")
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
                report_item = PacUserTriStateFilterListGetModelResponseItem()
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
            #TODO add comment
        """
        return self.model_dump_json()
