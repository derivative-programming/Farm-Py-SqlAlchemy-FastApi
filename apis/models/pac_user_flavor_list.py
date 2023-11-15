import json
from typing import List
from datetime import date, datetime
import uuid
from decimal import Decimal
from business.pac import PacBusObj
from helpers import TypeConversion
from reports.row_models.pac_user_flavor_list import ReportItemPacUserFlavorList
from apis.models.list_model import ListModel
from helpers import SessionContext
from helpers.formatting import snake_to_camel
from models import Pac
from reports.pac_user_flavor_list import ReportManagerPacUserFlavorList
from reports.report_request_validation_error import ReportRequestValidationError
from apis.models.validation_error import ValidationErrorItem
import apis.models as view_models
from models import Pac
from helpers.pydantic_serialization import CamelModel,SnakeModel,BaseModel
from pydantic import Field,UUID4
import logging
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
### request. expect camel case. use marshmallow to validate.
class PacUserFlavorListGetModelRequest(CamelModel):
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
class PacUserFlavorListGetModelResponseItem(CamelModel):
    flavor_code:UUID4 = Field(default_factory=lambda: uuid.UUID('00000000-0000-0000-0000-000000000000'), description="Flavor Code")
    flavor_description:str = Field(default="", description="Flavor Description")
    flavor_display_order:int = Field(default=0, description="Flavor Display Order")
    flavor_is_active:bool = Field(default=False, description="Flavor Is Active")
    flavor_lookup_enum_name:str = Field(default="", description="Flavor Lookup Enum Name")
    flavor_name:str = Field(default="", description="Flavor Name")
    pac_name:str = Field(default="", description="Pac Name")

    def load_report_item(self,data:ReportItemPacUserFlavorList):
        self.flavor_code = data.flavor_code
        self.flavor_description = data.flavor_description
        self.flavor_display_order = data.flavor_display_order
        self.flavor_is_active = data.flavor_is_active
        self.flavor_lookup_enum_name = data.flavor_lookup_enum_name
        self.flavor_name = data.flavor_name
        self.pac_name = data.pac_name

class PacUserFlavorListGetModelResponse(ListModel):
    request:PacUserFlavorListGetModelRequest = None
    items:List[PacUserFlavorListGetModelResponseItem] = Field(default_factory=list)
    async def process_request(self,
                        session:AsyncSession,
                        session_context:SessionContext,
                        pac_code:uuid,
                        request:PacUserFlavorListGetModelRequest):
        try:
            logging.info("loading model...PacUserFlavorListGetModelResponse")
            # pac_bus_obj = PacBusObj(session=session)
            # await pac_bus_obj.load(code=pac_code)
            generator = ReportManagerPacUserFlavorList(session_context)
            logging.info("processing...PacUserFlavorListGetModelResponse")
            items = await generator.generate(
                    pac_code,

                    request.page_number,
                    request.item_count_per_page,
                    request.order_by_column_name,
                    request.order_by_descending)
            self.items = list()
            for item in items:
                report_item = PacUserFlavorListGetModelResponseItem()
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
