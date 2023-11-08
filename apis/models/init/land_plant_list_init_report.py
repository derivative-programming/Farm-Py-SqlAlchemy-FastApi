from datetime import date, datetime
from decimal import Decimal
from apis.models import ValidationError
from typing import List
import uuid
from helpers import TypeConversion
from flows import FlowLandPlantListInitReportResult
from helpers import SessionContext
from models import Land
from flows import FlowLandPlantListInitReport
from flows import FlowValidationError
from helpers.pydantic_serialization import CamelModel,SnakeModel
from pydantic import Field
import apis.models as view_models
import logging
from models import Land
class LandPlantListInitReportGetInitModelResponse(CamelModel):
    success:bool = False
    message:str = ""
    validation_errors:List[ValidationError] = Field(default_factory=list)
    someIntVal:int = 0
    someBigIntVal:int = 0
    someBitVal:bool = False
    isEditAllowed:bool = False
    isDeleteAllowed:bool = False
    someFloatVal:float = 0
    someDecimalVal:Decimal = Decimal(0)
    someMinUTCDateTimeVal:datetime = Field(default_factory=TypeConversion.get_default_date_time)
    someMinDateVal:datetime.date = Field(default_factory=TypeConversion.get_default_date)
    someMoneyVal:Decimal = Decimal(0)
    someNVarCharVal:str = ""
    someVarCharVal:str = ""
    someTextVal:str = ""
    somePhoneNumber:str = ""
    someEmailAddress:str = ""
    landCode:uuid.UUID = Field(default_factory=lambda: uuid.UUID('00000000-0000-0000-0000-000000000000'))
    tacCode:uuid.UUID = Field(default_factory=lambda: uuid.UUID('00000000-0000-0000-0000-000000000000'))
    landName:str=""

    def load_flow_response(self,data:FlowLandPlantListInitReportResult):
        self.validation_errors = list()
        self.success = False
        self.message = ""
        self.someIntVal = data.some_int_val
        self.someBigIntVal = data.some_big_int_val
        self.someBitVal = data.some_bit_val
        self.isEditAllowed = data.is_edit_allowed
        self.isDeleteAllowed = data.is_delete_allowed
        self.someFloatVal = data.some_float_val
        self.someDecimalVal = data.some_decimal_val
        self.someMinUTCDateTimeVal = data.some_min_utc_date_time_val
        self.someMinDateVal = data.some_min_date_val
        self.someMoneyVal = data.some_money_val
        self.someNVarCharVal = data.some_n_var_char_val
        self.someVarCharVal = data.some_var_char_val
        self.someTextVal = data.some_text_val
        self.somePhoneNumber = data.some_phone_number
        self.someEmailAddress = data.some_email_address
        self.landCode = data.land_code
        self.tacCode = data.tac_code
        self.landName = data.land_name
class LandPlantListInitReportGetInitModelRequest(SnakeModel):
    def process_request(self,
                        session_context:SessionContext,
                        land_code:uuid,
                        response:LandPlantListInitReportGetInitModelResponse) -> LandPlantListInitReportGetInitModelResponse:
        try:
            logging.debug("loading model...")
            land = Land.objects.get(code=land_code)
            logging.debug("process request...")
            flow = FlowLandPlantListInitReport(session_context)
            flowResponse = flow.process(
                land
            )
            response.load_flow_response(flowResponse);
            response.success = True
            response.message = "Success."
        except FlowValidationError as ve:
            response.success = False
            response.validation_errors = list()
            for key in ve.error_dict:
                response.validation_errors.append(view_models.ValidationError(key,ve.error_dict[key]))
        return response

