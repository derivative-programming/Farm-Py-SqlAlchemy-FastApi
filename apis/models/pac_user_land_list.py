# apis/models/pac_user_land_list.py
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
from reports.pac_user_land_list import ReportManagerPacUserLandList
from reports.report_request_validation_error import \
    ReportRequestValidationError
from reports.row_models.pac_user_land_list import ReportItemPacUserLandList
class PacUserLandListGetModelRequest(CamelModel):
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
class PacUserLandListGetModelResponseItem(CamelModel):
    """
        #TODO add comment
    """
    land_code: UUID4 = Field(
        default_factory=lambda: uuid.UUID(
            '00000000-0000-0000-0000-000000000000'
        ),
        description="Land Code")
    land_description: str = Field(
        default="",
        description="Land Description")
    land_display_order: int = Field(
        default=0,
        description="Land Display Order")
    land_is_active: bool = Field(
        default=False,
        description="Land Is Active")
    land_lookup_enum_name: str = Field(
        default="",
        description="Land Lookup Enum Name")
    land_name: str = Field(
        default="",
        description="Land Name")
    pac_name: str = Field(
        default="",
        description="Pac Name")
# endset
    def load_report_item(self, data: ReportItemPacUserLandList):
        """
            #TODO add comment
        """
        self.land_code = (
            data.land_code)
        self.land_description = (
            data.land_description)
        self.land_display_order = (
            data.land_display_order)
        self.land_is_active = (
            data.land_is_active)
        self.land_lookup_enum_name = (
            data.land_lookup_enum_name)
        self.land_name = (
            data.land_name)
        self.pac_name = (
            data.pac_name)
# endset
    def build_report_item(
        self
    ) -> ReportItemPacUserLandList:
        """
            #TODO add comment
        """
        data = ReportItemPacUserLandList()
        data.land_code = (
            self.land_code)
        data.land_description = (
            self.land_description)
        data.land_display_order = (
            self.land_display_order)
        data.land_is_active = (
            self.land_is_active)
        data.land_lookup_enum_name = (
            self.land_lookup_enum_name)
        data.land_name = (
            self.land_name)
        data.pac_name = (
            self.pac_name)
        return data
# endset
class PacUserLandListGetModelResponse(ListModel):
    """
        #TODO add comment
    """
    request: PacUserLandListGetModelRequest = PacUserLandListGetModelRequest()
    items: List[PacUserLandListGetModelResponseItem] = Field(
        default_factory=list)
    async def process_request(
        self,
        session_context: SessionContext,
        pac_code: uuid.UUID,
        request: PacUserLandListGetModelRequest
    ):
        """
            #TODO add comment
        """
        try:
            logging.info("loading model...PacUserLandListGetModelResponse")
            generator = ReportManagerPacUserLandList(session_context)
            logging.info("processing...PacUserLandListGetModelResponse")
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
                report_item = PacUserLandListGetModelResponseItem()
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
