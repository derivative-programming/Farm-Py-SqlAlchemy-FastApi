# apis/models/pac_user_role_list.py
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
from reports.row_models.pac_user_role_list import ReportItemPacUserRoleList
from apis.models.list_model import ListModel
from helpers import SessionContext
from helpers.formatting import snake_to_camel
from models import Pac
from reports.pac_user_role_list import ReportManagerPacUserRoleList
from reports.report_request_validation_error import ReportRequestValidationError
from apis.models.validation_error import ValidationErrorItem
import apis.models as view_models
from models import Pac
from helpers.pydantic_serialization import CamelModel, SnakeModel, BaseModel
# request. expect camel case. use marshmallow to validate.
class PacUserRoleListGetModelRequest(CamelModel):
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
class PacUserRoleListGetModelResponseItem(CamelModel):
    """
        #TODO add comment
    """
    role_code: UUID4 = Field(
        default_factory=lambda: uuid.UUID(
            '00000000-0000-0000-0000-000000000000'
        ),
        description="Role Code")
    role_description: str = Field(
        default="",
        description="Role Description")
    role_display_order: int = Field(
        default=0,
        description="Role Display Order")
    role_is_active: bool = Field(
        default=False,
        description="Role Is Active")
    role_lookup_enum_name: str = Field(
        default="",
        description="Role Lookup Enum Name")
    role_name: str = Field(
        default="",
        description="Role Name")
    pac_name: str = Field(
        default="",
        description="Pac Name")
# endset
    def load_report_item(self, data: ReportItemPacUserRoleList):
        """
            #TODO add comment
        """
        self.role_code = (
            data.role_code)
        self.role_description = (
            data.role_description)
        self.role_display_order = (
            data.role_display_order)
        self.role_is_active = (
            data.role_is_active)
        self.role_lookup_enum_name = (
            data.role_lookup_enum_name)
        self.role_name = (
            data.role_name)
        self.pac_name = (
            data.pac_name)
# endset
class PacUserRoleListGetModelResponse(ListModel):
    """
        #TODO add comment
    """
    request: PacUserRoleListGetModelRequest = None
    items: List[PacUserRoleListGetModelResponseItem] = Field(
        default_factory=list)
    async def process_request(
        self,
        session_context: SessionContext,
        pac_code: uuid,
        request: PacUserRoleListGetModelRequest
    ):
        """
            #TODO add comment
        """
        try:
            logging.info("loading model...PacUserRoleListGetModelResponse")
            generator = ReportManagerPacUserRoleList(session_context)
            logging.info("processing...PacUserRoleListGetModelResponse")
            items = await generator.generate(
                    pac_code,

# endset
                    request.page_number,
                    request.item_count_per_page,
                    request.order_by_column_name,
                    request.order_by_descending)
            self.items = list()
            for item in items:
                report_item = PacUserRoleListGetModelResponseItem()
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
