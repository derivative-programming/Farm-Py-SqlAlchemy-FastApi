import json
from business.land import LandBusObj
from datetime import date, datetime
import uuid
from flows.base.land_add_plant_init_obj_wf import BaseFlowLandAddPlantInitObjWF
from models import Land
from flows.base import LogSeverity
from helpers import SessionContext
from helpers import ApiToken
from helpers import TypeConversion
import models as farm_models
import managers as farm_managers
import business
from sqlalchemy.ext.asyncio import AsyncSession
from services.db_config import db_dialect,generate_uuid
# from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
from sqlalchemy import String
from decimal import Decimal
class FlowLandAddPlantInitObjWFResult():
    context_object_code:uuid.UUID =  uuid.UUID(int=0)
    request_flavor_code:uuid.UUID =  uuid.UUID(int=0)
    request_other_flavor:str = ""
    request_some_int_val:int = 0
    request_some_big_int_val:int = 0
    request_some_bit_val:bool = False
    request_is_delete_allowed:bool = False
    request_is_edit_allowed:bool = False
    request_some_float_val:float = 0
    request_some_decimal_val:Decimal = Decimal(0)
    request_some_utc_date_time_val:datetime = TypeConversion.get_default_date_time()
    request_some_date_val:date = TypeConversion.get_default_date()
    request_some_money_val:Decimal = Decimal(0)
    request_some_n_var_char_val:str = ""
    request_some_var_char_val:str = ""
    request_some_text_val:str = ""
    request_some_phone_number:str = ""
    request_some_email_address:str = ""
    land_name:str = ""
    tac_code:uuid.UUID =  uuid.UUID(int=0)
    def __init__(self):
        pass
    def to_json(self):
        # Create a dictionary representation of the instance
        data = {
            'context_object_code': str(self.context_object_code),
            'request_flavor_code': str(self.request_flavor_code),
            'request_other_flavor': self.request_other_flavor,
            'request_some_int_val': self.request_some_int_val,
            'request_some_big_int_val': self.request_some_big_int_val,
            'request_some_bit_val': self.request_some_bit_val,
            'request_is_delete_allowed': self.request_is_delete_allowed,
            'request_is_edit_allowed': self.request_is_edit_allowed,
            'request_some_float_val': self.request_some_float_val,
            'request_some_decimal_val': str(self.request_some_decimal_val),
            'request_some_utc_date_time_val': self.request_some_utc_date_time_val.isoformat(),
            'request_some_date_val': self.request_some_date_val.isoformat(),
            'request_some_money_val': str(self.request_some_money_val),
            'request_some_n_var_char_val': self.request_some_n_var_char_val,
            'request_some_var_char_val': self.request_some_var_char_val,
            'request_some_text_val': self.request_some_text_val,
            'request_some_phone_number': self.request_some_phone_number,
            'request_some_email_address': self.request_some_email_address,
            'land_name': self.land_name,
            'tac_code': str(self.tac_code),
        }
        # Serialize the dictionary to JSON
        return json.dumps(data)
class FlowLandAddPlantInitObjWF(BaseFlowLandAddPlantInitObjWF):
    def __init__(self, session_context:SessionContext):
        super(FlowLandAddPlantInitObjWF, self).__init__(session_context)
    async def process(self,
        land_bus_obj: LandBusObj,

        ) -> FlowLandAddPlantInitObjWFResult:
        super()._log_message_and_severity(LogSeverity.information_high_detail, "Start")
        super()._log_message_and_severity(LogSeverity.information_high_detail, "Code::" + str(land_bus_obj.code))
        await super()._process_validation_rules(
            land_bus_obj,

        )
        super()._throw_queued_validation_errors()
        request_flavor_code_output:uuid = uuid.UUID(int=0)
        request_other_flavor_output:str = ""
        request_some_int_val_output:int = 0
        request_some_big_int_val_output:int = 0
        request_some_bit_val_output:bool = False
        request_is_delete_allowed_output:bool = False
        request_is_edit_allowed_output:bool = False
        request_some_float_val_output:float = 0
        request_some_decimal_val_output:Decimal = Decimal(0)
        request_some_utc_date_time_val_output:datetime = TypeConversion.get_default_date_time()
        request_some_date_val_output:date = TypeConversion.get_default_date()
        request_some_money_val_output:Decimal = 0
        request_some_n_var_char_val_output:str = ""
        request_some_var_char_val_output:str = ""
        request_some_text_val_output:str = ""
        request_some_phone_number_output:str = ""
        request_some_email_address_output:str = ""
        land_name_output:str = ""
        tac_code_output:uuid = uuid.UUID(int=0)
        # TODO: add flow logic

        super()._log_message_and_severity(LogSeverity.information_high_detail, "Building result")
        result = FlowLandAddPlantInitObjWFResult()
        result.context_object_code = land_bus_obj.code
        result.request_flavor_code = request_flavor_code_output
        result.request_other_flavor = request_other_flavor_output
        result.request_some_int_val = request_some_int_val_output
        result.request_some_big_int_val = request_some_big_int_val_output
        result.request_some_bit_val = request_some_bit_val_output
        result.request_is_delete_allowed = request_is_delete_allowed_output
        result.request_is_edit_allowed = request_is_edit_allowed_output
        result.request_some_float_val = request_some_float_val_output
        result.request_some_decimal_val = request_some_decimal_val_output
        result.request_some_utc_date_time_val = request_some_utc_date_time_val_output
        result.request_some_date_val = request_some_date_val_output
        result.request_some_money_val = request_some_money_val_output
        result.request_some_n_var_char_val = request_some_n_var_char_val_output
        result.request_some_var_char_val = request_some_var_char_val_output
        result.request_some_text_val = request_some_text_val_output
        result.request_some_phone_number = request_some_phone_number_output
        result.request_some_email_address = request_some_email_address_output
        result.land_name = land_name_output
        result.tac_code = tac_code_output
        super()._log_message_and_severity(LogSeverity.information_high_detail, "Result:" + result.to_json())
        super()._log_message_and_severity(LogSeverity.information_high_detail, "End")
        return result
