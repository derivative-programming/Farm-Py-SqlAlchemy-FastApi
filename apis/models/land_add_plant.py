from datetime import date, datetime
from decimal import Decimal
import json
import uuid 
from helpers import TypeConversion
from .post_reponse import PostResponse 
from flows.land_add_plant import FlowLandAddPlant, FlowLandAddPlantResult
from helpers import SessionContext 
from business.land import LandBusObj
from flows.base.flow_validation_error import FlowValidationError
import apis.models as view_models
from helpers.formatting import snake_to_camel
from helpers.pydantic_serialization import CamelModel,SnakeModel
from pydantic import Field,UUID4
import logging 
from apis.models.validation_error import ValidationErrorItem
from sqlalchemy.ext.asyncio import AsyncSession


class LandAddPlantPostModelRequest(CamelModel):
    force_error_message:str = Field(default="", description="Force Error Message")
    request_flavor_code:UUID4 = Field(default_factory=lambda: uuid.UUID('00000000-0000-0000-0000-000000000000'),
                                      description="Request Flavor Code")
    request_other_flavor:str = Field(default="", description="Request Other Flavor")
    request_some_int_val:int = Field(default=0, description="Request Some Int Val")
    request_some_big_int_val:int = Field(default=0, description="Request Some Big Int Val")
    request_some_bit_val:bool = Field(default=False, description="Request Some Bit Val")
    request_is_edit_allowed:bool = Field(default=False, description="Request Is Edit Allowed")
    request_is_delete_allowed:bool = Field(default=False, description="Request Is Delete Allowed")
    request_some_float_val:float = Field(default=0, description="Request Some Float Val")
    request_some_decimal_val:Decimal = Field(default=Decimal(0), description="Request Some Decimal Val")
    request_some_utc_date_time_val:datetime = Field(default_factory=TypeConversion.get_default_date_time, description="Request Some UTC Date Time Val")
    request_some_date_val:date = Field(default_factory=TypeConversion.get_default_date, description="Request Some Date Val")
    request_some_money_val:Decimal = Field(default=Decimal(0), description="Request Some Money Val")
    request_some_n_var_char_val:str = Field(default="", description="Request Some N Var Char Val")
    request_some_var_char_val:str = Field(default="", description="Request Some Var Char Val")
    request_some_text_val:str = Field(default="", description="Request Some Text Val")
    request_some_phone_number:str = Field(default="", description="Request Some Phone Number")
    request_some_email_address:str = Field(default="", description="Request Some Email Address")
    request_sample_image_upload_file:str = Field(default="", description="Request Some Image Upload File")
#endset 
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

    def to_dict_snake(self):
        data = self.model_dump() 

    def to_dict_snake_serialized(self):
        data = json.loads(self.model_dump_json() )
     
    def to_dict_camel(self):
        data = self.model_dump() 
        return {snake_to_camel(k): v for k, v in data.items()} 
    
    def to_dict_camel_serialized(self):
        data = json.loads(self.model_dump_json() )
        return {snake_to_camel(k): v for k, v in data.items()} 
    

class LandAddPlantPostModelResponse(PostResponse):
    output_flavor_code:UUID4 = Field(default=uuid.UUID(int=0), description="Output Flavor Code")
    output_other_flavor:str = Field(default="", description="Output Some Other Flavor")
    output_some_int_val:int = Field(default=0, description="Output Some Int Val")
    output_some_big_int_val:int = Field(default=0, description="Output Some Big Int Val")
    output_some_bit_val:bool = Field(default=False, description="Output Some Bit Val")
    output_is_edit_allowed:bool = Field(default=False, description="Output Is Edit Allowed")
    output_is_delete_allowed:bool = Field(default=False, description="Output Is Delete Allowed")
    output_some_float_val:float = Field(default=0, description="Output Some Float Val")
    output_some_decimal_val:Decimal = Field(default=Decimal(0), description="Output Some Decimal Val")
    output_some_utc_date_time_val:datetime = Field(default_factory=TypeConversion.get_default_date_time, description="Output Some UTC Date Time Val")
    output_some_date_val:date = Field(default_factory=TypeConversion.get_default_date, description="Output Some Date Val")
    output_some_money_val:Decimal = Field(default=Decimal(0), description="Output Some Money Val")
    output_some_n_var_char_val:str = Field(default="", description="Output Some N Var Char Val")
    output_some_var_char_val:str = Field(default="", description="Output Some Var Char Val")
    output_some_text_val:str = Field(default="", description="Output Some Text Val")
    output_some_phone_number:str = Field(default="", description="Output Some Phone Number")
    output_some_email_address:str = Field(default="", description="Output Some Email Address")
    land_code:UUID4 = Field(default=uuid.UUID(int=0), description="Land Code")
    plant_code:UUID4 = Field(default=uuid.UUID(int=0), description="Plant Code")
#endset
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
                        session_context:SessionContext,
                        land_code:uuid,
                        request:LandAddPlantPostModelRequest):
        try:
            logging.info("loading model...LandAddPlantPostModelResponse")
            land_bus_obj = LandBusObj(session_context)
            await land_bus_obj.load(code=land_code) 
            if(land_bus_obj.get_land_obj() is None):
                logging.info("Invalid land_code")
                raise ValueError("Invalid land_code")
            flow = FlowLandAddPlant(session_context)
            logging.info("process flow...LandAddPlantPostModelResponse")
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
            logging.info("error...LandAddPlantPostModelResponse")
            self.success = False 
            self.validation_errors = list()
            for key in ve.error_dict:
                validation_error = ValidationErrorItem()
                validation_error.property = snake_to_camel(key)
                validation_error.message = ve.error_dict[key]
                self.validation_errors.append(validation_error) 
    
    def to_json(self):
        return self.model_dump_json() 

