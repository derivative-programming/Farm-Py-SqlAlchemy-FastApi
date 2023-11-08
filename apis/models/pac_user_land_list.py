from typing import List
from datetime import date, datetime
import uuid
from decimal import Decimal
from helpers import TypeConversion
from reports.row_models import ReportItemPacUserLandList
from apis.models import ListModel
from helpers import SessionContext
from models import Pac
from reports import ReportManagerPacUserLandList
from reports import ReportRequestValidationError
import apis.models as view_models
from models import Pac
from helpers.pydantic_serialization import CamelModel,SnakeModel
from pydantic import Field,UUID4
import logging
### request. expect camel case. use marshmallow to validate.
class PacUserLandListGetModelRequest(SnakeModel):
    pageNumber:int = 0
    itemCountPerPage:int = 0
    orderByColumnName:str = ""
    orderByDescending:bool = False
    forceErrorMessage:str = ""

class PacUserLandListGetModelResponseItem(CamelModel):
    land_code:UUID4 = uuid.UUID(int=0)
    land_description:str = ""
    land_display_order:int = 0
    land_is_active:bool = False
    land_lookup_enum_name:str = ""
    land_name:str = ""
    pac_name:str = ""

    def load_report_item(self,data:ReportItemPacUserLandList):
        self.land_code = data.land_code
        self.land_description = data.land_description
        self.land_display_order = data.land_display_order
        self.land_is_active = data.land_is_active
        self.land_lookup_enum_name = data.land_lookup_enum_name
        self.land_name = data.land_name
        self.pac_name = data.pac_name

class PacUserLandListGetModelResponse(ListModel):
    request:PacUserLandListGetModelRequest = None
    items:List[PacUserLandListGetModelResponseItem] = Field(default_factory=list)
    def process_request(self,
                        session_context:SessionContext,
                        pac_code:uuid,
                        request:PacUserLandListGetModelRequest):
        try:
            logging.debug("loading model...")
            pac = Pac.objects.get(code=pac_code)
            generator = ReportManagerPacUserLandList(session_context)
            items = generator.generate(
                    pac.code,

                    request.pageNumber,
                    request.itemCountPerPage,
                    request.orderByColumnName,
                    request.orderByDescending)
            self.items = list()
            for item in items:
                report_item = PacUserLandListGetModelResponseItem()
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
