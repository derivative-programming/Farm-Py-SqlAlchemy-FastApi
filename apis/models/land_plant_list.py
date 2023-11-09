from typing import List
from datetime import date, datetime
import uuid
from decimal import Decimal
from business.land import LandBusObj
from helpers import TypeConversion
from reports.row_models.land_plant_list import ReportItemLandPlantList 
from apis.models.list_model import ListModel 
from helpers import SessionContext 
from models import Land 
from reports.land_plant_list import ReportManagerLandPlantList
from reports.report_request_validation_error import ReportRequestValidationError 
import apis.models as view_models
from models import Land 
from helpers.pydantic_serialization import CamelModel,SnakeModel
from pydantic import Field,UUID4
import logging
from sqlalchemy.ext.asyncio import AsyncSession
### request. expect camel case. use marshmallow to validate.

class LandPlantListGetModelRequest(SnakeModel):
    page_number:int = 0
    item_count_per_page:int = 0
    order_by_column_name:str = ""
    order_by_descending:bool = False
    force_error_message:str = ""
    flavor_code:UUID4 = Field(default_factory=lambda: uuid.UUID('00000000-0000-0000-0000-000000000000'))
    some_int_val:int = 0
    some_big_int_val:int = 0
    some_float_val:float = 0
    some_bit_val:bool = False
    is_edit_allowed:bool = False
    is_delete_allowed:bool = False
    some_decimal_val:Decimal = Decimal(0)
    some_min_utc_date_time_val:datetime = Field(default_factory=TypeConversion.get_default_date_time)
    some_min_date_val:date = Field(default_factory=TypeConversion.get_default_date)
    some_money_val:Decimal = Decimal(0)
    some_n_var_char_val:str = ""
    some_var_char_val:str = ""
    some_text_val:str = ""
    some_phone_number:str = ""
    some_email_address:str = ""
#endset 

class LandPlantListGetModelResponseItem(CamelModel):
    plant_code:UUID4 = uuid.UUID(int=0)
    some_int_val:int = 0
    some_big_int_val:int = 0
    some_bit_val:bool = False
    is_edit_allowed:bool = False
    is_delete_allowed:bool = False
    some_float_val:float = 0
    some_decimal_val:Decimal = Decimal(0)
    some_utc_date_time_val:datetime = Field(default_factory=TypeConversion.get_default_date_time)
    some_date_val:date = Field(default_factory=TypeConversion.get_default_date)
    some_money_val:Decimal = Decimal(0)
    some_n_var_char_val:str = ""
    some_var_char_val:str = ""
    some_text_val:str = ""
    some_phone_number:str = ""
    some_email_address:str = ""
    flavor_name:str = ""
    flavor_code:UUID4 = uuid.UUID(int=0)
    some_int_conditional_on_deletable:int = 0
    n_var_char_as_url:str = ""
    update_link_plant_code:UUID4 = uuid.UUID(int=0)
    delete_async_button_link_plant_code:UUID4 = uuid.UUID(int=0)
    details_link_plant_code:UUID4 = uuid.UUID(int=0)
#endset
    def load_report_item(self,data:ReportItemLandPlantList):
        self.plant_code = data.plant_code
        self.some_int_val = data.some_int_val
        self.some_big_int_val = data.some_big_int_val
        self.some_bit_val = data.some_bit_val
        self.is_edit_allowed = data.is_edit_allowed
        self.is_delete_allowed = data.is_delete_allowed
        self.some_float_val = data.some_float_val
        self.some_decimal_val = data.some_decimal_val
        self.some_utc_date_time_val = data.some_utc_date_time_val
        self.some_date_val = data.some_date_val
        self.some_money_val = data.some_money_val
        self.some_n_var_char_val = data.some_n_var_char_val
        self.some_var_char_val = data.some_var_char_val
        self.some_text_val = data.some_text_val
        self.some_phone_number = data.some_phone_number
        self.some_email_address = data.some_email_address
        self.flavor_name = data.flavor_name
        self.flavor_code = data.flavor_code
        self.some_int_conditional_on_deletable = data.some_int_conditional_on_deletable
        self.n_var_char_as_url = data.n_var_char_as_url
        self.update_link_plant_code = data.update_link_plant_code
        self.delete_async_button_link_plant_code = data.delete_async_button_link_plant_code
        self.details_link_plant_code = data.details_link_plant_code
#endset

class LandPlantListGetModelResponse(ListModel):
    request:LandPlantListGetModelRequest = None
    items:List[LandPlantListGetModelResponseItem] = Field(default_factory=list)
    async def process_request(self,
                        session:AsyncSession,
                        session_context:SessionContext,
                        land_code:uuid,
                        request:LandPlantListGetModelRequest):
        try:
            logging.debug("loading model...LandPlantListGetModelResponse")
            # land_bus_obj = LandBusObj(session=session)
            # await land_bus_obj.load(code=land_code)  
            generator = ReportManagerLandPlantList(session_context)
            logging.debug("processing...LandPlantListGetModelResponse")
            items = await generator.generate(
                    land_code,
                    request.flavor_code,
                    request.some_int_val,
                    request.some_big_int_val,
                    request.some_float_val,
                    request.some_bit_val,
                    request.is_edit_allowed,
                    request.is_delete_allowed,
                    request.some_decimal_val,
                    request.some_min_utc_date_time_val,
                    request.some_min_date_val,
                    request.some_money_val,
                    request.some_n_var_char_val,
                    request.some_var_char_val,
                    request.some_text_val,
                    request.some_phone_number,
                    request.some_email_address,
#endset
                    request.page_number,
                    request.item_count_per_page,
                    request.order_by_column_name,
                    request.order_by_descending)
            self.items = list()
            for item in items:
                report_item = LandPlantListGetModelResponseItem()
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
