import uuid
from models import Tac
from .base_flow import BaseFlow
from flows.base import LogSeverity
from helpers import SessionContext
from decimal import Decimal
from datetime import date, datetime
from helpers import TypeConversion
import flows.constants.tac_login as FlowConstants
import models as farm_models
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
        customerCodeMatchRequired = False
        role_required = ""
        if len(role_required) > 0:
            if role_required not in self._session_context.role_name_csv:
                self._add_validation_error("Unautorized access. " + role_required + " role not found.")
        if FlowConstants.calculatedIsRowLevelCustomerSecurityUsed == True:
            customerCodeMatchRequired = True
        if FlowConstants.calculatedIsRowLevelOrganizationSecurityUsed == True:
            customerCodeMatchRequired = True
        if FlowConstants.calculatedIsRowLevelOrgCustomerSecurityUsed == True:
            customerCodeMatchRequired = True
        if customerCodeMatchRequired == True:
            val = True
            item = tac
            while val:
                if item.get_object_name() == "pac":
                    val = False

                item = item.get_parent_object()
