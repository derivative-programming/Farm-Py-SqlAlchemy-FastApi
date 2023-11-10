import json
from typing import List
from datetime import date, datetime
import uuid
from decimal import Decimal
from business.plant import PlantBusObj
from helpers import TypeConversion
from reports.row_models.plant_user_details import ReportItemPlantUserDetails
from apis.models.list_model import ListModel
from helpers import SessionContext
from models import Plant
from reports.plant_user_details import ReportManagerPlantUserDetails
from reports.report_request_validation_error import ReportRequestValidationError
import apis.models as view_models
from models import Plant
from helpers.pydantic_serialization import CamelModel,SnakeModel,BaseModel
from pydantic import Field,UUID4
import logging
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
### request. expect camel case. use marshmallow to validate.
class PlantUserDetailsGetModelRequest(SnakeModel):
    page_number:int = 0
    item_count_per_page:int = 0
    order_by_column_name:str = ""
    order_by_descending:bool = False
    force_error_message:str = ""

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
    def to_dict_snake(self):
        data = self.model_dump()
        return data
    def to_dict_snake_serialized(self):
        data = json.loads(self.model_dump_json())
        return data
    def _to_camel(self,string: str) -> str:
        return ''.join(word.capitalize() if i != 0 else word for i, word in enumerate(string.split('_')))
    def to_dict_camel(self):
        data = self.model_dump()
        return {self._to_camel(k): v for k, v in data.items()}
    def to_dict_camel_serialized(self):
        data = json.loads(self.model_dump_json() )
        return {self._to_camel(k): v for k, v in data.items()}
class PlantUserDetailsGetModelResponseItem(CamelModel):
    flavor_name:str = ""
    is_delete_allowed:bool = False
    is_edit_allowed:bool = False
    other_flavor:str = ""
    some_big_int_val:int = 0
    some_bit_val:bool = False
    some_date_val:date = Field(default_factory=TypeConversion.get_default_date)
    some_decimal_val:Decimal = Decimal(0)
    some_email_address:str = ""
    some_float_val:float = 0
    some_int_val:int = 0
    some_money_val:Decimal = Decimal(0)
    some_n_var_char_val:str = ""
    some_phone_number:str = ""
    some_text_val:str = ""
    some_uniqueidentifier_val:UUID4 = uuid.UUID(int=0)
    some_utc_date_time_val:datetime = Field(default_factory=TypeConversion.get_default_date_time)
    some_var_char_val:str = ""
    phone_num_conditional_on_is_editable:str = ""
    n_var_char_as_url:str = ""
    update_button_text_link_plant_code:UUID4 = uuid.UUID(int=0)
    random_property_updates_link_plant_code:UUID4 = uuid.UUID(int=0)
    back_to_dashboard_link_tac_code:UUID4 = uuid.UUID(int=0)

    def load_report_item(self,data:ReportItemPlantUserDetails):
        self.flavor_name = data.flavor_name
        self.is_delete_allowed = data.is_delete_allowed
        self.is_edit_allowed = data.is_edit_allowed
        self.other_flavor = data.other_flavor
        self.some_big_int_val = data.some_big_int_val
        self.some_bit_val = data.some_bit_val
        self.some_date_val = data.some_date_val
        self.some_decimal_val = data.some_decimal_val
        self.some_email_address = data.some_email_address
        self.some_float_val = data.some_float_val
        self.some_int_val = data.some_int_val
        self.some_money_val = data.some_money_val
        self.some_n_var_char_val = data.some_n_var_char_val
        self.some_phone_number = data.some_phone_number
        self.some_text_val = data.some_text_val
        self.some_uniqueidentifier_val = data.some_uniqueidentifier_val
        self.some_utc_date_time_val = data.some_utc_date_time_val
        self.some_var_char_val = data.some_var_char_val
        self.phone_num_conditional_on_is_editable = data.phone_num_conditional_on_is_editable
        self.n_var_char_as_url = data.n_var_char_as_url
        self.update_button_text_link_plant_code = data.update_button_text_link_plant_code
        self.random_property_updates_link_plant_code = data.random_property_updates_link_plant_code
        self.back_to_dashboard_link_tac_code = data.back_to_dashboard_link_tac_code

class PlantUserDetailsGetModelResponse(ListModel):
    request:PlantUserDetailsGetModelRequest = None
    items:List[PlantUserDetailsGetModelResponseItem] = Field(default_factory=list)
    async def process_request(self,
                        session:AsyncSession,
                        session_context:SessionContext,
                        plant_code:uuid,
                        request:PlantUserDetailsGetModelRequest):
        try:
            logging.info("loading model...PlantUserDetailsGetModelResponse")
            # plant_bus_obj = PlantBusObj(session=session)
            # await plant_bus_obj.load(code=plant_code)
            generator = ReportManagerPlantUserDetails(session_context)
            logging.info("processing...PlantUserDetailsGetModelResponse")
            items = await generator.generate(
                    plant_code,

                    request.page_number,
                    request.item_count_per_page,
                    request.order_by_column_name,
                    request.order_by_descending)
            self.items = list()
            for item in items:
                report_item = PlantUserDetailsGetModelResponseItem()
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
    def to_json(self):
        return self.model_dump_json()
