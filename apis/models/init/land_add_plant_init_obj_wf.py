from datetime import date, datetime
from decimal import Decimal 
from typing import List
import uuid 
from helpers import TypeConversion 
from flows.land_add_plant_init_obj_wf import FlowLandAddPlantInitObjWFResult, FlowLandAddPlantInitObjWF
from helpers import SessionContext 
from business.land import LandBusObj
from flows.base.flow_validation_error import FlowValidationError
from helpers.pydantic_serialization import CamelModel,SnakeModel
from pydantic import Field
from apis.models.validation_error import ValidationError
import logging 
from sqlalchemy.ext.asyncio import AsyncSession

class LandAddPlantInitObjWFGetInitModelResponse(CamelModel):
    success:bool = False
    message:str = ""
    validation_errors:List[ValidationError] = Field(default_factory=list)
    request_flavor_code:uuid.UUID = Field(default_factory=lambda: uuid.UUID('00000000-0000-0000-0000-000000000000'))
    request_other_flavor:str = ""
    request_some_int_val:int = 0
    request_some_big_int_val:int = 0
    request_some_bit_val:bool = False
    request_is_delete_allowed:bool = False
    request_is_edit_allowed:bool = False
    request_some_float_val:float = 0
    request_some_decimal_val:Decimal = Decimal(0)
    request_some_utc_date_time_val:datetime = Field(default_factory=TypeConversion.get_default_date_time)
    request_some_date_val:date = Field(default_factory=TypeConversion.get_default_date)
    request_some_money_val:Decimal = Decimal(0)
    request_some_n_var_char_val:str = ""
    request_some_var_char_val:str = ""
    request_some_text_val:str = ""
    request_some_phone_number:str = ""
    request_some_email_address:str = ""
    land_name:str=""
    tac_code:uuid.UUID = Field(default_factory=lambda: uuid.UUID('00000000-0000-0000-0000-000000000000'))
#endset
    def load_flow_response(self,data:FlowLandAddPlantInitObjWFResult): 
        self.validation_errors = list()
        self.success = False
        self.message = ""
        self.request_flavor_code = data.request_flavor_code
        self.request_other_flavor = data.request_other_flavor
        self.request_some_int_val = data.request_some_int_val
        self.request_some_big_int_val = data.request_some_big_int_val
        self.request_some_bit_val = data.request_some_bit_val
        self.request_is_delete_allowed = data.request_is_delete_allowed
        self.request_is_edit_allowed = data.request_is_edit_allowed
        self.request_some_float_val = data.request_some_float_val
        self.request_some_decimal_val = data.request_some_decimal_val
        self.request_some_utc_date_time_val = data.request_some_utc_date_time_val
        self.request_some_date_val = data.request_some_date_val
        self.request_some_money_val = data.request_some_money_val
        self.request_some_n_var_char_val = data.request_some_n_var_char_val
        self.request_some_var_char_val = data.request_some_var_char_val
        self.request_some_text_val = data.request_some_text_val
        self.request_some_phone_number = data.request_some_phone_number
        self.request_some_email_address = data.request_some_email_address
        self.land_name = data.land_name
        self.tac_code = data.tac_code 

class LandAddPlantInitObjWFGetInitModelRequest(SnakeModel):
    async def process_request(self,
                        session:AsyncSession,
                        session_context:SessionContext,
                        land_code:uuid,
                        response:LandAddPlantInitObjWFGetInitModelResponse) -> LandAddPlantInitObjWFGetInitModelResponse:
        try:
            logging.debug("loading model...LandAddPlantInitObjWFGetInitModelRequest")
            land_bus_obj = LandBusObj(session=session)
            await land_bus_obj.load(code=land_code) 
            flow = FlowLandAddPlantInitObjWF(session_context)
            logging.debug("process request...LandAddPlantInitObjWFGetInitModelRequest") 
            flowResponse = await flow.process(
                land_bus_obj
            )  
            response.load_flow_response(flowResponse); 
            response.success = True
            response.message = "Success."
        except FlowValidationError as ve:
            logging.debug("error...LandAddPlantInitObjWFGetInitModelRequest") 
            response.success = False 
            response.validation_errors = list()
            for key in ve.error_dict:
                response.validation_errors.append(ValidationError(key,ve.error_dict[key]))
        return response

