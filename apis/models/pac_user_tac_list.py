# apis/models/pac_user_tac_list.py
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
from reports.pac_user_tac_list import ReportManagerPacUserTacList
from reports.report_request_validation_error import \
    ReportRequestValidationError
from reports.row_models.pac_user_tac_list import ReportItemPacUserTacList
class PacUserTacListGetModelRequest(CamelModel):
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
class PacUserTacListGetModelResponseItem(CamelModel):
    """
        #TODO add comment
    """
    tac_code: UUID4 = Field(
        default_factory=lambda: uuid.UUID(
            '00000000-0000-0000-0000-000000000000'
        ),
        description="Tac Code")
    tac_description: str = Field(
        default="",
        description="Tac Description")
    tac_display_order: int = Field(
        default=0,
        description="Tac Display Order")
    tac_is_active: bool = Field(
        default=False,
        description="Tac Is Active")
    tac_lookup_enum_name: str = Field(
        default="",
        description="Tac Lookup Enum Name")
    tac_name: str = Field(
        default="",
        description="Tac Name")
    pac_name: str = Field(
        default="",
        description="Pac Name")
# endset
    def load_report_item(self, data: ReportItemPacUserTacList):
        """
            #TODO add comment
        """
        self.tac_code = (
            data.tac_code)
        self.tac_description = (
            data.tac_description)
        self.tac_display_order = (
            data.tac_display_order)
        self.tac_is_active = (
            data.tac_is_active)
        self.tac_lookup_enum_name = (
            data.tac_lookup_enum_name)
        self.tac_name = (
            data.tac_name)
        self.pac_name = (
            data.pac_name)
# endset
    def build_report_item(
        self
    ) -> ReportItemPacUserTacList:
        """
            #TODO add comment
        """
        data = ReportItemPacUserTacList()
        data.tac_code = (
            self.tac_code)
        data.tac_description = (
            self.tac_description)
        data.tac_display_order = (
            self.tac_display_order)
        data.tac_is_active = (
            self.tac_is_active)
        data.tac_lookup_enum_name = (
            self.tac_lookup_enum_name)
        data.tac_name = (
            self.tac_name)
        data.pac_name = (
            self.pac_name)
        return data
# endset
class PacUserTacListGetModelResponse(ListModel):
    """
        #TODO add comment
    """
    request: PacUserTacListGetModelRequest = PacUserTacListGetModelRequest()
    items: List[PacUserTacListGetModelResponseItem] = Field(
        default_factory=list)
    async def process_request(
        self,
        session_context: SessionContext,
        pac_code: uuid.UUID,
        request: PacUserTacListGetModelRequest
    ):
        """
            #TODO add comment
        """
        try:
            logging.info("loading model...PacUserTacListGetModelResponse")
            generator = ReportManagerPacUserTacList(session_context)
            logging.info("processing...PacUserTacListGetModelResponse")
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
                report_item = PacUserTacListGetModelResponseItem()
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
