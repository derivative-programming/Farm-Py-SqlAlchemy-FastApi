import uuid
from models import Tac 
from .base_flow import BaseFlow
from flows.base import LogSeverity
from helpers import SessionContext
from decimal import Decimal
from datetime import date, datetime
from helpers import TypeConversion
import flows.constants.tac_login as FlowConstants
class BaseFlowTacLogin(BaseFlow):
    def __init__(self, session_context:SessionContext): 
        super(BaseFlowTacLogin, self).__init__(
            "TacLogin", 
            session_context,
            ) 
    def _process_validation_rules(self, 
            tac: Tac,
            email:str = "",
            password:str = "",
        ):
        super()._log_message_and_severity(LogSeverity.information_high_detail, "Validating...")
        if email == "" and FlowConstants.param_email_isRequired == True:
            self._add_field_validation_error("email","Please enter a Email")
        if password == "" and FlowConstants.param_password_isRequired == True:
            self._add_field_validation_error("password","Please enter a ")
        self._process_security_rules(tac)
    def _process_security_rules(self, 
        tac: Tac,
        ):
        super()._log_message_and_severity(LogSeverity.information_high_detail, "Processing security rules...")
