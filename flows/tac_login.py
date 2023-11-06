
from dataclasses import dataclass
from dataclasses_json import dataclass_json,LetterCase 
import uuid
from flows.base import BaseFlowTacLogin
from models import Tac
from models import Customer
from flows.base import LogSeverity
from helpers import SessionContext
from django.core.exceptions import ObjectDoesNotExist
from flows.base import FlowValidationError
from helpers import ApiToken
from django.utils import timezone
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

    def __init__(self): 
        pass

class FlowTacLogin(BaseFlowTacLogin):
    def __init__(self, session_context:SessionContext): 
        super(FlowTacLogin, self).__init__(session_context) 

    def process(self, 
        tac: Tac,
        email: str,
        password: str,
        ) -> FlowTacLoginResult: 
        
        super()._log_message_and_severity(LogSeverity.information_high_detail, "Start")
        super()._log_message_and_severity(LogSeverity.information_high_detail, "Code::" + str(tac.code))

        
        customer = Customer()
        try:
            customer = Customer.objects.get(email=email) 
        except ObjectDoesNotExist:
            super()._add_field_validation_error("email","User does not exist")

        if password != customer.password:
            super()._add_field_validation_error("password","Invalid password")

        if customer.is_active == False:
            super()._add_field_validation_error("email","This user account is locked")

        super()._process_validation_rules(
            tac,
            email,
            password,
        )

        super()._throw_queued_validation_errors()

        customer_code_output = uuid.UUID(int=0)
        email_output = ""
        user_code_value_output = uuid.UUID(int=0)
        utc_offset_in_minutes_output = 0
        role_name_csv_list_output = ""
        api_key_output = ""

 
        customer_roles = farm_models.CustomerRole.objects.filter(customer_id=customer.customer_id)
       
        roles = [customer_role.role.lookup_enum_name for customer_role in customer_roles]
        roles_str = ', '.join(roles)
        roles_str = roles_str.strip(', ')
 
   
        api_key_dict = dict()
        api_key_dict["PacCode"] = str(customer.tac.pac.code)
        api_key_dict["TacCode"] = str(customer.tac.code)
        api_key_dict["CustomerCode"] = str(customer.code)
        api_key_dict["UserName"] = customer.email
        api_key_dict["role_name_csv"] = roles_str
        api_key_output = ApiToken.create_token(api_key_dict, 1)
 
        customer.last_login_utc_date_time = timezone.now() 
        customer.save()
        
        
        customer_code_output = customer.code
        email_output = customer.email
        user_code_value_output = customer.code
        utc_offset_in_minutes_output = customer.utc_offset_in_minutes 
        role_name_csv_list_output = roles_str 
 
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


    