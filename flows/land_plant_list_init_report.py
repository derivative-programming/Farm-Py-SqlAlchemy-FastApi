from dataclasses import dataclass, field
from dataclasses_json import dataclass_json,LetterCase, config
from datetime import date, datetime
import uuid
from flows.base import BaseFlowLandPlantListInitReport
from models import Land 
from flows.base import LogSeverity
from helpers import SessionContext
from models import Customer
from django.utils import timezone
from helpers import ApiToken
from decimal import Decimal
from helpers import TypeConversion
import models as farm_models 
import managers as farm_managers
@dataclass_json
@dataclass
class FlowLandPlantListInitReportResult():
    context_object_code:uuid = uuid.UUID(int=0)
    some_int_val:int = 0
    some_big_int_val:int = 0
    some_bit_val:bool = False
    is_edit_allowed:bool = False
    is_delete_allowed:bool = False
    some_float_val:float = 0
    some_decimal_val:Decimal = Decimal(0)
    some_min_utc_date_time_val:datetime = field(default_factory=TypeConversion.get_default_date_time,
            metadata=config(
            encoder=datetime.isoformat,
            decoder=datetime.fromisoformat
        ))
    some_min_date_val:date = field(default_factory=TypeConversion.get_default_date, metadata=config(
            encoder=date.isoformat,
            decoder=date.fromisoformat
        ))
    some_money_val:Decimal = Decimal(0)
    some_n_var_char_val:str = ""
    some_var_char_val:str = ""
    some_text_val:str = ""
    some_phone_number:str = ""
    some_email_address:str = ""
    flavor_code:uuid = uuid.UUID(int=0)
    land_code:uuid = uuid.UUID(int=0)
    tac_code:uuid = uuid.UUID(int=0)
    land_name:str = ""
class FlowLandPlantListInitReport(BaseFlowLandPlantListInitReport):
    def __init__(self, session_context:SessionContext): 
        super(FlowLandPlantListInitReport, self).__init__(session_context) 
    def process(self,
        land: Land,

        ) -> FlowLandPlantListInitReportResult:
        super()._log_message_and_severity(LogSeverity.information_high_detail, "Start")
        super()._log_message_and_severity(LogSeverity.information_high_detail, "Code::" + str(land.code))
        super()._process_validation_rules(
            land,

        )
        super()._throw_queued_validation_errors()
        some_int_val_output:int = 0
        some_big_int_val_output:int = 0
        some_bit_val_output:bool = False
        is_edit_allowed_output:bool = False
        is_delete_allowed_output:bool = False
        some_float_val_output:float = 0
        some_decimal_val_output:Decimal = Decimal(0)
        some_min_utc_date_time_val_output:datetime = TypeConversion.get_default_date_time()
        some_min_date_val_output:date = TypeConversion.get_default_date()
        some_money_val_output:Decimal = 0
        some_n_var_char_val_output:str = ""
        some_var_char_val_output:str = ""
        some_text_val_output:str = ""
        some_phone_number_output:str = ""
        some_email_address_output:str = ""
        flavor_code_output:uuid = uuid.UUID(int=0)
        land_code_output:uuid = uuid.UUID(int=0)
        tac_code_output:uuid = uuid.UUID(int=0)
        land_name_output:str = ""
        # TODO: add flow logic

        flavor_code_output = farm_models.Flavor.objects.from_enum(farm_managers.FlavorEnum.Unknown).code
        land_code_output = farm_models.Land.objects.from_enum(farm_managers.LandEnum.Unknown).code
        tac_code_output = farm_models.Tac.objects.from_enum(farm_managers.TacEnum.Unknown).code
        land_name_output = land.name

        super()._log_message_and_severity(LogSeverity.information_high_detail, "Building result")
        result = FlowLandPlantListInitReportResult() 
        result.context_object_code = land.code
        result.some_int_val = some_int_val_output
        result.some_big_int_val = some_big_int_val_output
        result.some_bit_val = some_bit_val_output
        result.is_edit_allowed = is_edit_allowed_output
        result.is_delete_allowed = is_delete_allowed_output
        result.some_float_val = some_float_val_output
        result.some_decimal_val = some_decimal_val_output
        result.some_min_utc_date_time_val = some_min_utc_date_time_val_output
        result.some_min_date_val = some_min_date_val_output
        result.some_money_val = some_money_val_output
        result.some_n_var_char_val = some_n_var_char_val_output
        result.some_var_char_val = some_var_char_val_output
        result.some_text_val = some_text_val_output
        result.some_phone_number = some_phone_number_output
        result.some_email_address = some_email_address_output
        result.flavor_code = flavor_code_output
        result.land_code = land_code_output
        result.tac_code = tac_code_output
        result.land_name = land_name_output
        super()._log_message_and_severity(LogSeverity.information_high_detail, "Result:" + result.to_json())
        super()._log_message_and_severity(LogSeverity.information_high_detail, "End")
        return result
