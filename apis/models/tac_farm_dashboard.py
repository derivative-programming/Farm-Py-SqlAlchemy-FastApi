# apis/models/tac_farm_dashboard.py
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
from business.tac import TacBusObj
from helpers import TypeConversion
from reports.row_models.tac_farm_dashboard import ReportItemTacFarmDashboard
from apis.models.list_model import ListModel
from helpers import SessionContext
from helpers.formatting import snake_to_camel
from models import Tac
from reports.tac_farm_dashboard import ReportManagerTacFarmDashboard
from reports.report_request_validation_error import ReportRequestValidationError
from apis.models.validation_error import ValidationErrorItem
import apis.models as view_models
from helpers.pydantic_serialization import CamelModel, SnakeModel, BaseModel
class TacFarmDashboardGetModelRequest(CamelModel):
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
class TacFarmDashboardGetModelResponseItem(CamelModel):
    """
        #TODO add comment
    """
    field_one_plant_list_link_land_code: UUID4 = Field(
        default_factory=lambda: uuid.UUID(
            '00000000-0000-0000-0000-000000000000'
        ),
        description="Field One Plant List Link Land Code")
    conditional_btn_example_link_land_code: UUID4 = Field(
        default_factory=lambda: uuid.UUID(
            '00000000-0000-0000-0000-000000000000'
        ),
        description="Conditional Btn Example Link Land Code")
    is_conditional_btn_available: bool = Field(
        default=False,
        description="Is Conditional Btn Available")
# endset
    def load_report_item(self, data: ReportItemTacFarmDashboard):
        """
            #TODO add comment
        """
        self.field_one_plant_list_link_land_code = (
            data.field_one_plant_list_link_land_code)
        self.conditional_btn_example_link_land_code = (
            data.conditional_btn_example_link_land_code)
        self.is_conditional_btn_available = (
            data.is_conditional_btn_available)
# endset
class TacFarmDashboardGetModelResponse(ListModel):
    """
        #TODO add comment
    """
    request: TacFarmDashboardGetModelRequest = None
    items: List[TacFarmDashboardGetModelResponseItem] = Field(
        default_factory=list)
    async def process_request(
        self,
        session_context: SessionContext,
        tac_code: uuid.UUID,
        request: TacFarmDashboardGetModelRequest
    ):
        """
            #TODO add comment
        """
        try:
            logging.info("loading model...TacFarmDashboardGetModelResponse")
            generator = ReportManagerTacFarmDashboard(session_context)
            logging.info("processing...TacFarmDashboardGetModelResponse")
            items = await generator.generate(
                tac_code,

# endset
                request.page_number,
                request.item_count_per_page,
                request.order_by_column_name,
                request.order_by_descending
            )
            self.items = list()
            for item in items:
                report_item = TacFarmDashboardGetModelResponseItem()
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
