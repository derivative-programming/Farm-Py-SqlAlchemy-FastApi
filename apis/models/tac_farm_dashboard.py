from dataclasses import dataclass, field 
from dataclasses_json import dataclass_json, LetterCase, config
from typing import List
from datetime import date, datetime
import uuid
from decimal import Decimal
from helpers import TypeConversion
from reports.row_models import ReportItemTacFarmDashboard 
from apis.models import ListModel 
from helpers import SessionContext 
from models import Tac 
from reports import ReportManagerTacFarmDashboard
from reports import ReportRequestValidationError 
import apis.models as view_models
from models import Tac 
import logging
### request. expect camel case. use marshmallow to validate.
@dataclass_json(letter_case=LetterCase.SNAKE)
@dataclass
class TacFarmDashboardGetModelRequest():
    pageNumber:int = 0
    itemCountPerPage:int = 0
    orderByColumnName:str = ""
    orderByDescending:bool = False
    forceErrorMessage:str = ""

#endset 
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class TacFarmDashboardGetModelResponseItem():
    field_one_plant_list_link_land_code:uuid = uuid.UUID(int=0)
    conditional_btn_example_link_land_code:uuid = uuid.UUID(int=0)
    is_conditional_btn_available:bool = False
#endset
    def load_report_item(self,data:ReportItemTacFarmDashboard):
        self.field_one_plant_list_link_land_code = data.field_one_plant_list_link_land_code
        self.conditional_btn_example_link_land_code = data.conditional_btn_example_link_land_code
        self.is_conditional_btn_available = data.is_conditional_btn_available
#endset
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class TacFarmDashboardGetModelResponse(ListModel):
    request:TacFarmDashboardGetModelRequest = None
    items:List[TacFarmDashboardGetModelResponseItem] = field(default_factory=list)
    def process_request(self,
                        session_context:SessionContext,
                        tac_code:uuid,
                        request:TacFarmDashboardGetModelRequest):
        try:
            logging.debug("loading model...")
            tac = Tac.objects.get(code=tac_code)
            generator = ReportManagerTacFarmDashboard(session_context)
            items = generator.generate(
                    tac.code,

#endset
                    request.pageNumber,
                    request.itemCountPerPage,
                    request.orderByColumnName,
                    request.orderByDescending)
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
