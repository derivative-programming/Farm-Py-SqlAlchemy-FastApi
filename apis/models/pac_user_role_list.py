from typing import List
from datetime import date, datetime
import uuid
from decimal import Decimal
from helpers import TypeConversion
from reports.row_models import ReportItemPacUserRoleList
from apis.models import ListModel
from helpers import SessionContext
from models import Pac
from reports import ReportManagerPacUserRoleList
from reports import ReportRequestValidationError
import apis.models as view_models
from models import Pac
from helpers.pydantic_serialization import CamelModel,SnakeModel
from pydantic import Field,UUID4
import logging
### request. expect camel case. use marshmallow to validate.
class PacUserRoleListGetModelRequest(SnakeModel):
    pageNumber:int = 0
    itemCountPerPage:int = 0
    orderByColumnName:str = ""
    orderByDescending:bool = False
    forceErrorMessage:str = ""

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
    def process_request(self,
                        session_context:SessionContext,
                        pac_code:uuid,
                        request:PacUserRoleListGetModelRequest):
        try:
            logging.debug("loading model...")
            pac = Pac.objects.get(code=pac_code)
            generator = ReportManagerPacUserRoleList(session_context)
            items = generator.generate(
                    pac.code,

                    request.pageNumber,
                    request.itemCountPerPage,
                    request.orderByColumnName,
                    request.orderByDescending)
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
