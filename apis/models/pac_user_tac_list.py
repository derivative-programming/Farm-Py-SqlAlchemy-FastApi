from typing import List
from datetime import date, datetime
import uuid
from decimal import Decimal
from helpers import TypeConversion
from reports.row_models import ReportItemPacUserTacList
from apis.models import ListModel
from helpers import SessionContext
from models import Pac
from reports import ReportManagerPacUserTacList
from reports import ReportRequestValidationError
import apis.models as view_models
from models import Pac
from helpers.pydantic_serialization import CamelModel,SnakeModel
from pydantic import Field,UUID4
import logging
### request. expect camel case. use marshmallow to validate.
class PacUserTacListGetModelRequest(SnakeModel):
    pageNumber:int = 0
    itemCountPerPage:int = 0
    orderByColumnName:str = ""
    orderByDescending:bool = False
    forceErrorMessage:str = ""

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
    def process_request(self,
                        session_context:SessionContext,
                        pac_code:uuid,
                        request:PacUserTacListGetModelRequest):
        try:
            logging.debug("loading model...")
            pac = Pac.objects.get(code=pac_code)
            generator = ReportManagerPacUserTacList(session_context)
            items = generator.generate(
                    pac.code,

                    request.pageNumber,
                    request.itemCountPerPage,
                    request.orderByColumnName,
                    request.orderByDescending)
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
