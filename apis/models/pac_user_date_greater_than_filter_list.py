from typing import List
from datetime import date, datetime
import uuid
from decimal import Decimal
from helpers import TypeConversion
from reports.row_models import ReportItemPacUserDateGreaterThanFilterList
from apis.models import ListModel
from helpers import SessionContext
from models import Pac
from reports import ReportManagerPacUserDateGreaterThanFilterList
from reports import ReportRequestValidationError
import apis.models as view_models
from models import Pac
from helpers.pydantic_serialization import CamelModel,SnakeModel
from pydantic import Field,UUID4
import logging
### request. expect camel case. use marshmallow to validate.
class PacUserDateGreaterThanFilterListGetModelRequest(SnakeModel):
    pageNumber:int = 0
    itemCountPerPage:int = 0
    orderByColumnName:str = ""
    orderByDescending:bool = False
    forceErrorMessage:str = ""

class PacUserDateGreaterThanFilterListGetModelResponseItem(CamelModel):
    date_greater_than_filter_code:UUID4 = uuid.UUID(int=0)
    date_greater_than_filter_day_count:int = 0
    date_greater_than_filter_description:str = ""
    date_greater_than_filter_display_order:int = 0
    date_greater_than_filter_is_active:bool = False
    date_greater_than_filter_lookup_enum_name:str = ""
    date_greater_than_filter_name:str = ""

    def load_report_item(self,data:ReportItemPacUserDateGreaterThanFilterList):
        self.date_greater_than_filter_code = data.date_greater_than_filter_code
        self.date_greater_than_filter_day_count = data.date_greater_than_filter_day_count
        self.date_greater_than_filter_description = data.date_greater_than_filter_description
        self.date_greater_than_filter_display_order = data.date_greater_than_filter_display_order
        self.date_greater_than_filter_is_active = data.date_greater_than_filter_is_active
        self.date_greater_than_filter_lookup_enum_name = data.date_greater_than_filter_lookup_enum_name
        self.date_greater_than_filter_name = data.date_greater_than_filter_name

class PacUserDateGreaterThanFilterListGetModelResponse(ListModel):
    request:PacUserDateGreaterThanFilterListGetModelRequest = None
    items:List[PacUserDateGreaterThanFilterListGetModelResponseItem] = Field(default_factory=list)
    def process_request(self,
                        session_context:SessionContext,
                        pac_code:uuid,
                        request:PacUserDateGreaterThanFilterListGetModelRequest):
        try:
            logging.debug("loading model...")
            pac = Pac.objects.get(code=pac_code)
            generator = ReportManagerPacUserDateGreaterThanFilterList(session_context)
            items = generator.generate(
                    pac.code,

                    request.pageNumber,
                    request.itemCountPerPage,
                    request.orderByColumnName,
                    request.orderByDescending)
            self.items = list()
            for item in items:
                report_item = PacUserDateGreaterThanFilterListGetModelResponseItem()
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
