import json
from typing import List
from datetime import date, datetime
import uuid
from decimal import Decimal
from business.pac import PacBusObj
from helpers import TypeConversion
from reports.row_models.pac_user_tac_list import ReportItemPacUserTacList
from apis.models.list_model import ListModel
from helpers import SessionContext
from models import Pac
from reports.pac_user_tac_list import ReportManagerPacUserTacList
from reports.report_request_validation_error import ReportRequestValidationError
import apis.models as view_models
from models import Pac
from helpers.pydantic_serialization import CamelModel,SnakeModel,BaseModel
from pydantic import Field,UUID4
import logging
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
### request. expect camel case. use marshmallow to validate.
class PacUserTacListGetModelRequest(SnakeModel):
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
class PacUserTacListGetModelResponseItem(CamelModel):
    tac_code:UUID4 = uuid.UUID(int=0)
    tac_description:str = ""
    tac_display_order:int = 0
    tac_is_active:bool = False
    tac_lookup_enum_name:str = ""
    tac_name:str = ""
    pac_name:str = ""

    def load_report_item(self,data:ReportItemPacUserTacList):
        self.tac_code = data.tac_code
        self.tac_description = data.tac_description
        self.tac_display_order = data.tac_display_order
        self.tac_is_active = data.tac_is_active
        self.tac_lookup_enum_name = data.tac_lookup_enum_name
        self.tac_name = data.tac_name
        self.pac_name = data.pac_name

class PacUserTacListGetModelResponse(ListModel):
    request:PacUserTacListGetModelRequest = None
    items:List[PacUserTacListGetModelResponseItem] = Field(default_factory=list)
    async def process_request(self,
                        session:AsyncSession,
                        session_context:SessionContext,
                        pac_code:uuid,
                        request:PacUserTacListGetModelRequest):
        try:
            logging.info("loading model...PacUserTacListGetModelResponse")
            # pac_bus_obj = PacBusObj(session=session)
            # await pac_bus_obj.load(code=pac_code)
            generator = ReportManagerPacUserTacList(session_context)
            logging.info("processing...PacUserTacListGetModelResponse")
            items = await generator.generate(
                    pac_code,

                    request.page_number,
                    request.item_count_per_page,
                    request.order_by_column_name,
                    request.order_by_descending)
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
            for key in ve.error_dict:
                self.message = self.message + ve.error_dict[key] + ','
                # self.validation_errors.append(view_models.ValidationError(key,ve.error_dict[key]))
    def to_json(self):
        return self.model_dump_json()
