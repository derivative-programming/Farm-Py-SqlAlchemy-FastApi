from typing import List
from datetime import date, datetime
import uuid
from decimal import Decimal
from helpers import TypeConversion
from reports.row_models import ReportItemPacUserTriStateFilterList
from apis.models import ListModel
from helpers import SessionContext
from models import Pac
from reports import ReportManagerPacUserTriStateFilterList
from reports import ReportRequestValidationError
import apis.models as view_models
from models import Pac
from helpers.pydantic_serialization import CamelModel,SnakeModel
from pydantic import Field,UUID4
import logging
### request. expect camel case. use marshmallow to validate.
class PacUserTriStateFilterListGetModelRequest(SnakeModel):
    pageNumber:int = 0
    itemCountPerPage:int = 0
    orderByColumnName:str = ""
    orderByDescending:bool = False
    forceErrorMessage:str = ""

class PacUserTriStateFilterListGetModelResponseItem(CamelModel):
    tri_state_filter_code:UUID4 = uuid.UUID(int=0)
    tri_state_filter_description:str = ""
    tri_state_filter_display_order:int = 0
    tri_state_filter_is_active:bool = False
    tri_state_filter_lookup_enum_name:str = ""
    tri_state_filter_name:str = ""
    tri_state_filter_state_int_value:int = 0

    def load_report_item(self,data:ReportItemPacUserTriStateFilterList):
        self.tri_state_filter_code = data.tri_state_filter_code
        self.tri_state_filter_description = data.tri_state_filter_description
        self.tri_state_filter_display_order = data.tri_state_filter_display_order
        self.tri_state_filter_is_active = data.tri_state_filter_is_active
        self.tri_state_filter_lookup_enum_name = data.tri_state_filter_lookup_enum_name
        self.tri_state_filter_name = data.tri_state_filter_name
        self.tri_state_filter_state_int_value = data.tri_state_filter_state_int_value

class PacUserTriStateFilterListGetModelResponse(ListModel):
    request:PacUserTriStateFilterListGetModelRequest = None
    items:List[PacUserTriStateFilterListGetModelResponseItem] = Field(default_factory=list)
    def process_request(self,
                        session_context:SessionContext,
                        pac_code:uuid,
                        request:PacUserTriStateFilterListGetModelRequest):
        try:
            logging.debug("loading model...")
            pac = Pac.objects.get(code=pac_code)
            generator = ReportManagerPacUserTriStateFilterList(session_context)
            items = generator.generate(
                    pac.code,

                    request.pageNumber,
                    request.itemCountPerPage,
                    request.orderByColumnName,
                    request.orderByDescending)
            self.items = list()
            for item in items:
                report_item = PacUserTriStateFilterListGetModelResponseItem()
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
