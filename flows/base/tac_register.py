import uuid
from business.customer import CustomerBusObj
from business.tac import TacBusObj
from managers.org_customer import OrgCustomerManager
from models import Tac
from .base_flow import BaseFlow
from flows.base import LogSeverity
from helpers import SessionContext
from decimal import Decimal
from datetime import date, datetime
from helpers import TypeConversion
import flows.constants.tac_register as FlowConstants
import models as farm_models
class BaseFlowTacRegister(BaseFlow):
    def __init__(self, session_context:SessionContext):
        super(BaseFlowTacRegister, self).__init__(
            "TacRegister",
            session_context,
            )
    async def _process_validation_rules(self,
            tac_bus_obj: TacBusObj,
            email:str = "",
            password:str = "",
            confirm_password:str = "",
            first_name:str = "",
            last_name:str = "",
        ):
        super()._log_message_and_severity(LogSeverity.information_high_detail, "Validating...")
        if email == "" and FlowConstants.param_email_isRequired == True:
            self._add_field_validation_error("email","Please enter a Email")
        if password == "" and FlowConstants.param_password_isRequired == True:
            self._add_field_validation_error("password","Please enter a Password")
        if confirm_password == "" and FlowConstants.param_confirm_password_isRequired == True:
            self._add_field_validation_error("confirmPassword","Please enter a ")
        if first_name == "" and FlowConstants.param_first_name_isRequired == True:
            self._add_field_validation_error("firstName","Please enter a First Name")
        if last_name == "" and FlowConstants.param_last_name_isRequired == True:
            self._add_field_validation_error("lastName","Please enter a Last Name")
        await self._process_security_rules(tac_bus_obj)
    async def _process_security_rules(self,
        tac_bus_obj: TacBusObj,
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
        if customerCodeMatchRequired == True and len(self.queued_validation_errors) == 0:
            val = True
            item = tac_bus_obj
            while val:
                if item.get_object_name() == "pac":
                    val = False

                item = await item.get_parent_object()
