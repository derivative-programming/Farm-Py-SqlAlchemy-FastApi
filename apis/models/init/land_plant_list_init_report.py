from datetime import date, datetime
from decimal import Decimal
from typing import List
import uuid
from helpers import TypeConversion
from flows.land_plant_list_init_report import FlowLandPlantListInitReportResult, FlowLandPlantListInitReport
from helpers import SessionContext
from business.land import LandBusObj
from flows.base.flow_validation_error import FlowValidationError
from helpers.pydantic_serialization import CamelModel,SnakeModel
from pydantic import Field
from apis.models.validation_error import ValidationError
import logging
from sqlalchemy.ext.asyncio import AsyncSession
class LandPlantListInitReportGetInitModelResponse(CamelModel):
    success:bool = False
    message:str = ""
    validation_errors:List[ValidationError] = Field(default_factory=list)
    some_int_val:int = 0
    some_big_int_val:int = 0
    some_bit_val:bool = False
    is_edit_allowed:bool = False
    is_delete_allowed:bool = False
    some_float_val:float = 0
    some_decimal_val:Decimal = Decimal(0)
    some_min_utc_date_time_val:datetime = Field(default_factory=TypeConversion.get_default_date_time)
    some_min_date_val:date = Field(default_factory=TypeConversion.get_default_date)
    some_money_val:Decimal = Decimal(0)
    some_n_var_char_val:str = ""
    some_var_char_val:str = ""
    some_text_val:str = ""
    some_phone_number:str = ""
    some_email_address:str = ""
    land_code:uuid.UUID = Field(default_factory=lambda: uuid.UUID('00000000-0000-0000-0000-000000000000'))
    tac_code:uuid.UUID = Field(default_factory=lambda: uuid.UUID('00000000-0000-0000-0000-000000000000'))
    land_name:str=""

    def load_flow_response(self,data:FlowLandPlantListInitReportResult):
        self.validation_errors = list()
        self.success = False
        self.message = ""
        self.some_int_val = data.some_int_val
        self.some_big_int_val = data.some_big_int_val
        self.some_bit_val = data.some_bit_val
        self.is_edit_allowed = data.is_edit_allowed
        self.is_delete_allowed = data.is_delete_allowed
        self.some_float_val = data.some_float_val
        self.some_decimal_val = data.some_decimal_val
        self.some_min_utc_date_time_val = data.some_min_utc_date_time_val
        self.some_min_date_val = data.some_min_date_val
        self.some_money_val = data.some_money_val
        self.some_n_var_char_val = data.some_n_var_char_val
        self.some_var_char_val = data.some_var_char_val
        self.some_text_val = data.some_text_val
        self.some_phone_number = data.some_phone_number
        self.some_email_address = data.some_email_address
        self.land_code = data.land_code
        self.tac_code = data.tac_code
        self.land_name = data.land_name
class LandPlantListInitReportGetInitModelRequest(SnakeModel):
    async def process_request(self,
                        session:AsyncSession,
                        session_context:SessionContext,
                        land_code:uuid,
                        response:LandPlantListInitReportGetInitModelResponse) -> LandPlantListInitReportGetInitModelResponse:
        try:
            logging.debug("loading model...LandPlantListInitReportGetInitModelRequest")
            land_bus_obj = LandBusObj(session=session)
            await land_bus_obj.load(code=land_code)
            flow = FlowLandPlantListInitReport(session_context)
            logging.debug("process request...LandPlantListInitReportGetInitModelRequest")
            flowResponse = await flow.process(
                land_bus_obj
            )
            response.load_flow_response(flowResponse);
            response.success = True
            response.message = "Success."
        except FlowValidationError as ve:
            logging.debug("error...LandPlantListInitReportGetInitModelRequest")
            response.success = False
            response.validation_errors = list()
            for key in ve.error_dict:
                response.validation_errors.append(ValidationError(key,ve.error_dict[key]))
        return response

