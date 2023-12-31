import json
from typing import List
from datetime import date, datetime
import uuid
from decimal import Decimal
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
from models import Tac
from helpers.pydantic_serialization import CamelModel,SnakeModel,BaseModel
from pydantic import Field,UUID4
import logging
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
### request. expect camel case. use marshmallow to validate.
class TacFarmDashboardGetModelRequest(CamelModel):
    page_number:int = Field(default=0, description="Page Number")
    item_count_per_page:int = Field(default=0, description="Item Count Per Page")
    order_by_column_name:str = Field(default="", description="Order By Column Name")
    order_by_descending:bool = Field(default=False, description="Order By Decending")
    force_error_message:str = Field(default="", description="Force Error Message")

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
    def to_dict_snake(self):
        data = self.model_dump()
        return data
    def to_dict_snake_serialized(self):
        data = json.loads(self.model_dump_json())
        return data
    def to_dict_camel(self):
        data = self.model_dump()
        return {snake_to_camel(k): v for k, v in data.items()}
    def to_dict_camel_serialized(self):
        data = json.loads(self.model_dump_json() )
        return {snake_to_camel(k): v for k, v in data.items()}
class TacFarmDashboardGetModelResponseItem(CamelModel):
    field_one_plant_list_link_land_code:UUID4 = Field(default_factory=lambda: uuid.UUID('00000000-0000-0000-0000-000000000000'), description="Field One Plant List Link Land Code")
    conditional_btn_example_link_land_code:UUID4 = Field(default_factory=lambda: uuid.UUID('00000000-0000-0000-0000-000000000000'), description="Conditional Btn Example Link Land Code")
    is_conditional_btn_available:bool = Field(default=False, description="Is Conditional Btn Available")

    def load_report_item(self,data:ReportItemTacFarmDashboard):
        self.field_one_plant_list_link_land_code = data.field_one_plant_list_link_land_code
        self.conditional_btn_example_link_land_code = data.conditional_btn_example_link_land_code
        self.is_conditional_btn_available = data.is_conditional_btn_available

class TacFarmDashboardGetModelResponse(ListModel):
    request:TacFarmDashboardGetModelRequest = None
    items:List[TacFarmDashboardGetModelResponseItem] = Field(default_factory=list)
    async def process_request(self,
                        session_context:SessionContext,
                        tac_code:uuid,
                        request:TacFarmDashboardGetModelRequest):
        try:
            logging.info("loading model...TacFarmDashboardGetModelResponse")
            generator = ReportManagerTacFarmDashboard(session_context)
            logging.info("processing...TacFarmDashboardGetModelResponse")
            items = await generator.generate(
                    tac_code,

                    request.page_number,
                    request.item_count_per_page,
                    request.order_by_column_name,
                    request.order_by_descending)
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
        return self.model_dump_json()
