from datetime import date, datetime
from decimal import Decimal
import uuid 
from helpers import TypeConversion
from .post_reponse import PostResponse 
from flows.land_add_plant import FlowLandAddPlant, FlowLandAddPlantResult
from helpers import SessionContext 
from business.land import LandBusObj
from flows.base.flow_validation_error import FlowValidationError
import apis.models as view_models
from helpers.pydantic_serialization import CamelModel,SnakeModel
from pydantic import Field,UUID4
import logging 
from apis.models.validation_error import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession


class LandAddPlantPostModelRequest(SnakeModel):
    force_error_message:str = ""
    request_flavor_code:UUID4 = Field(default_factory=lambda: uuid.UUID('00000000-0000-0000-0000-000000000000'))
    request_other_flavor:str = ""
    request_some_int_val:int = 0
    request_some_big_int_val:int = 0
    request_some_bit_val:bool = False
    request_is_edit_allowed:bool = False
    request_is_delete_allowed:bool = False
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
    request_sample_image_upload_file:str = ""
#endset 
    

class LandAddPlantPostModelResponse(PostResponse):
    output_flavor_code:UUID4 = uuid.UUID(int=0)
    output_other_flavor:str = ""
    output_some_int_val:int = 0
    output_some_big_int_val:int = 0
    output_some_bit_val:bool = False
    output_is_edit_allowed:bool = False
    output_is_delete_allowed:bool = False
    output_some_float_val:float = 0
    output_some_decimal_val:Decimal = Decimal(0)
    output_some_utc_date_time_val:datetime = Field(default_factory=TypeConversion.get_default_date_time)
    output_some_date_val:date = Field(default_factory=TypeConversion.get_default_date)
    output_some_money_val:Decimal = Decimal(0)
    output_some_n_var_char_val:str = ""
    output_some_var_char_val:str = ""
    output_some_text_val:str = ""
    output_some_phone_number:str = ""
    output_some_email_address:str = ""
    land_code:UUID4 = uuid.UUID(int=0)
    plant_code:UUID4 = uuid.UUID(int=0)
#endset
    def load_flow_response(self,data:FlowLandAddPlantResult): 
        placeholder = "" #to avoid pass line
        self.output_flavor_code = data.land_code
        self.output_other_flavor = data.output_other_flavor
        self.output_some_int_val = data.output_some_int_val
        self.output_some_big_int_val = data.output_some_big_int_val
        self.output_some_bit_val = data.output_some_bit_val
        self.output_is_edit_allowed = data.output_is_edit_allowed
        self.output_is_delete_allowed = data.output_is_delete_allowed
        self.output_some_float_val = data.output_some_float_val
        self.output_some_decimal_val = data.output_some_decimal_val
        self.output_some_utc_date_time_val = data.output_some_utc_date_time_val
        self.output_some_date_val = data.output_some_date_val
        self.output_some_money_val = data.output_some_money_val
        self.output_some_n_var_char_val = data.output_some_n_var_char_val
        self.output_some_var_char_val = data.output_some_var_char_val
        self.output_some_text_val = data.output_some_text_val
        self.output_some_phone_number = data.output_some_phone_number
        self.output_some_email_address = data.output_some_email_address
        self.land_code = data.land_code
        self.plant_code = data.plant_code
#endset

    async def process_request(self,
                        session:AsyncSession,
                        session_context:SessionContext,
                        land_code:uuid,
                        request:LandAddPlantPostModelRequest):
        try:
            logging.debug("loading model...LandAddPlantPostModelResponse")
            land_bus_obj = LandBusObj(session=session)
            await land_bus_obj.load(code=land_code) 
            flow = FlowLandAddPlant(session_context)
            logging.debug("process flow...LandAddPlantPostModelResponse")
            flowResponse = await flow.process(
                land_bus_obj,
                request.request_flavor_code,
                request.request_other_flavor,
                request.request_some_int_val,
                request.request_some_big_int_val,
                request.request_some_bit_val,
                request.request_is_edit_allowed,
                request.request_is_delete_allowed,
                request.request_some_float_val,
                request.request_some_decimal_val,
                request.request_some_utc_date_time_val,
                request.request_some_date_val,
                request.request_some_money_val,
                request.request_some_n_var_char_val,
                request.request_some_var_char_val,
                request.request_some_text_val,
                request.request_some_phone_number,
                request.request_some_email_address,
                request.request_sample_image_upload_file
#endset
            ) 
            self.load_flow_response(flowResponse); 
            self.success = True
            self.message = "Success."
        except FlowValidationError as ve:
            logging.debug("error...LandAddPlantPostModelResponse")
            self.success = False 
            self.validation_errors = list()
            for key in ve.error_dict:
                validation_error = ValidationError()
                validation_error.property = key
                validation_error.message = ve.error_dict[key]
                self.validation_errors.append(validation_error) 
    
