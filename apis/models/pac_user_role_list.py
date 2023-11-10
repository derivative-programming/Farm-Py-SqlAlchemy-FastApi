import json
from typing import List
from datetime import date, datetime
import uuid
from decimal import Decimal
from business.pac import PacBusObj
from helpers import TypeConversion
from reports.row_models.pac_user_role_list import ReportItemPacUserRoleList
from apis.models.list_model import ListModel
from helpers import SessionContext
from models import Pac
from reports.pac_user_role_list import ReportManagerPacUserRoleList
from reports.report_request_validation_error import ReportRequestValidationError
import apis.models as view_models
from models import Pac
from helpers.pydantic_serialization import CamelModel,SnakeModel
from pydantic import Field,UUID4
import logging
from sqlalchemy.ext.asyncio import AsyncSession
### request. expect camel case. use marshmallow to validate.
class PacUserRoleListGetModelRequest(SnakeModel):
    page_number:int = 0
    item_count_per_page:int = 0
    order_by_column_name:str = ""
    order_by_descending:bool = False
    force_error_message:str = ""

class PacUserRoleListGetModelResponseItem(CamelModel):
    role_code:UUID4 = uuid.UUID(int=0)
    role_description:str = ""
    role_display_order:int = 0
    role_is_active:bool = False
    role_lookup_enum_name:str = ""
    role_name:str = ""
    pac_name:str = ""

    def load_report_item(self,data:ReportItemPacUserRoleList):
        self.role_code = data.role_code
        self.role_description = data.role_description
        self.role_display_order = data.role_display_order
        self.role_is_active = data.role_is_active
        self.role_lookup_enum_name = data.role_lookup_enum_name
        self.role_name = data.role_name
        self.pac_name = data.pac_name

class PacUserRoleListGetModelResponse(ListModel):
    request:PacUserRoleListGetModelRequest = None
    items:List[PacUserRoleListGetModelResponseItem] = Field(default_factory=list)
    async def process_request(self,
                        session:AsyncSession,
                        session_context:SessionContext,
                        pac_code:uuid,
                        request:PacUserRoleListGetModelRequest):
        try:
            logging.info("loading model...PacUserRoleListGetModelResponse")
            # pac_bus_obj = PacBusObj(session=session)
            # await pac_bus_obj.load(code=pac_code)
            generator = ReportManagerPacUserRoleList(session_context)
            logging.info("processing...PacUserRoleListGetModelResponse")
            items = await generator.generate(
                    pac_code,

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
                # self.validation_errors.append(view_models.ValidationError(key,ve.error_dict[key]))
    def to_json(self):
        # Create a dictionary representation of the instance
        data = {
            #TODO finish to_json
        }
        # Serialize the dictionary to JSON
        return json.dumps(data)
