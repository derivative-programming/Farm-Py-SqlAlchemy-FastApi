# apis/models/tac_farm_dashboard.py
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
from reports.tac_farm_dashboard import ReportManagerTacFarmDashboard
from reports.report_request_validation_error import \
    ReportRequestValidationError
from reports.row_models.tac_farm_dashboard import ReportItemTacFarmDashboard
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
    def build_report_item(
        self
    ) -> ReportItemTacFarmDashboard:
        """
            #TODO add comment
        """
        data = ReportItemTacFarmDashboard()
        data.field_one_plant_list_link_land_code = (
            self.field_one_plant_list_link_land_code)
        data.conditional_btn_example_link_land_code = (
            self.conditional_btn_example_link_land_code)
        data.is_conditional_btn_available = (
            self.is_conditional_btn_available)
        return data
# endset
class TacFarmDashboardGetModelResponse(ListModel):
    """
        #TODO add comment
    """
    request: TacFarmDashboardGetModelRequest = TacFarmDashboardGetModelRequest()
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

# endset  # noqa: E122
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
