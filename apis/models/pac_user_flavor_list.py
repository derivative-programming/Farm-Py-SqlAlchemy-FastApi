from typing import List
from datetime import date, datetime
import uuid
from decimal import Decimal
from helpers import TypeConversion
from reports.row_models import ReportItemPacUserFlavorList
from apis.models import ListModel
from helpers import SessionContext
from models import Pac
from reports import ReportManagerPacUserFlavorList
from reports import ReportRequestValidationError
import apis.models as view_models
from models import Pac
from helpers.pydantic_serialization import CamelModel,SnakeModel
from pydantic import Field,UUID4
import logging
### request. expect camel case. use marshmallow to validate.
class PacUserFlavorListGetModelRequest(SnakeModel):
    pageNumber:int = 0
    itemCountPerPage:int = 0
    orderByColumnName:str = ""
    orderByDescending:bool = False
    forceErrorMessage:str = ""

class PacUserFlavorListGetModelResponseItem(CamelModel):
    flavor_code:UUID4 = uuid.UUID(int=0)
    flavor_description:str = ""
    flavor_display_order:int = 0
    flavor_is_active:bool = False
    flavor_lookup_enum_name:str = ""
    flavor_name:str = ""
    pac_name:str = ""

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
    def process_request(self,
                        session_context:SessionContext,
                        pac_code:uuid,
                        request:PacUserFlavorListGetModelRequest):
        try:
            logging.debug("loading model...")
            pac = Pac.objects.get(code=pac_code)
            generator = ReportManagerPacUserFlavorList(session_context)
            items = generator.generate(
                    pac.code,

                    request.pageNumber,
                    request.itemCountPerPage,
                    request.orderByColumnName,
                    request.orderByDescending)
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
                # self.validation_errors.append(view_models.ValidationError(key,ve.error_dict[key]))
