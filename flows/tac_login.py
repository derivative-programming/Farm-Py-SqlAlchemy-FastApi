from dataclasses import dataclass, field
from dataclasses_json import dataclass_json,LetterCase, config
from datetime import date, datetime
import uuid
from flows.base import BaseFlowTacLogin
from models import Tac
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
class FlowTacLoginResult():
    context_object_code:uuid = uuid.UUID(int=0)
    customer_code:uuid = uuid.UUID(int=0)
    email:str = ""
    user_code_value:uuid = uuid.UUID(int=0)
    utc_offset_in_minutes:int = 0
    role_name_csv_list:str = ""
    api_key:str = ""
class FlowTacLogin(BaseFlowTacLogin):
    def __init__(self, session_context:SessionContext):
        super(FlowTacLogin, self).__init__(session_context)
    def process(self,
        tac: Tac,
        email:str = "",
        password:str = "",
        ) -> FlowTacLoginResult:
        super()._log_message_and_severity(LogSeverity.information_high_detail, "Start")
        super()._log_message_and_severity(LogSeverity.information_high_detail, "Code::" + str(tac.code))
        super()._process_validation_rules(
            tac,
            email,
            password,
        )
        super()._throw_queued_validation_errors()
        customer_code_output:uuid = uuid.UUID(int=0)
        email_output:str = ""
        user_code_value_output:uuid = uuid.UUID(int=0)
        utc_offset_in_minutes_output:int = 0
        role_name_csv_list_output:str = ""
        api_key_output:str = ""
        # TODO: add flow logic

        super()._log_message_and_severity(LogSeverity.information_high_detail, "Building result")
        result = FlowTacLoginResult()
        result.context_object_code = tac.code
        result.customer_code = customer_code_output
        result.email = email_output
        result.user_code_value = user_code_value_output
        result.utc_offset_in_minutes = utc_offset_in_minutes_output
        result.role_name_csv_list = role_name_csv_list_output
        result.api_key = api_key_output
        super()._log_message_and_severity(LogSeverity.information_high_detail, "Result:" + result.to_json())
        super()._log_message_and_severity(LogSeverity.information_high_detail, "End")
        return result
