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
from models import Tac
from reports.tac_farm_dashboard import ReportManagerTacFarmDashboard
from reports.report_request_validation_error import ReportRequestValidationError
import apis.models as view_models
from models import Tac
from helpers.pydantic_serialization import CamelModel,SnakeModel,BaseModel
from pydantic import Field,UUID4
import logging
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
### request. expect camel case. use marshmallow to validate.
class TacFarmDashboardGetModelRequest(SnakeModel):
    page_number:int = 0
    item_count_per_page:int = 0
    order_by_column_name:str = ""
    order_by_descending:bool = False
    force_error_message:str = ""

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
    def _to_camel(self,string: str) -> str:
        return ''.join(word.capitalize() if i != 0 else word for i, word in enumerate(string.split('_')))
    def to_dict_camel(self):
        data = self.model_dump()
        return {self._to_camel(k): v for k, v in data.items()}
    def to_dict_camel_serialized(self):
        data = json.loads(self.model_dump_json() )
        return {self._to_camel(k): v for k, v in data.items()}
class TacFarmDashboardGetModelResponseItem(CamelModel):
    field_one_plant_list_link_land_code:UUID4 = uuid.UUID(int=0)
    conditional_btn_example_link_land_code:UUID4 = uuid.UUID(int=0)
    is_conditional_btn_available:bool = False

    def load_report_item(self,data:ReportItemTacFarmDashboard):
        self.field_one_plant_list_link_land_code = data.field_one_plant_list_link_land_code
        self.conditional_btn_example_link_land_code = data.conditional_btn_example_link_land_code
        self.is_conditional_btn_available = data.is_conditional_btn_available

class TacFarmDashboardGetModelResponse(ListModel):
    request:TacFarmDashboardGetModelRequest = None
    items:List[TacFarmDashboardGetModelResponseItem] = Field(default_factory=list)
    async def process_request(self,
                        session:AsyncSession,
                        session_context:SessionContext,
                        tac_code:uuid,
                        request:TacFarmDashboardGetModelRequest):
        try:
            logging.info("loading model...TacFarmDashboardGetModelResponse")
            # tac_bus_obj = TacBusObj(session=session)
            # await tac_bus_obj.load(code=tac_code)
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
                # self.validation_errors.append(view_models.ValidationError(key,ve.error_dict[key]))
    def to_json(self):
        return self.model_dump_json()
