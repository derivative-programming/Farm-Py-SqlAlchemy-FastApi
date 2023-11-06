import uuid
from models import Pac
from .base_flow import BaseFlow
from flows.base import LogSeverity
from helpers import SessionContext
from decimal import Decimal
from datetime import date, datetime
from helpers import TypeConversion
import flows.constants.pac_user_flavor_list_init_report as FlowConstants
import models as farm_models
class BaseFlowPacUserFlavorListInitReport(BaseFlow):
    def __init__(self, session_context:SessionContext):
        super(BaseFlowPacUserFlavorListInitReport, self).__init__(
            "PacUserFlavorListInitReport",
            session_context,
            )
    def _process_validation_rules(self,
            pac: Pac,

        ):
        super()._log_message_and_severity(LogSeverity.information_high_detail, "Validating...")

        self._process_security_rules(pac)
    def _process_security_rules(self,
        pac: Pac,
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
            item = pac
            while val:
                if item.get_object_name() == "pac":
                    val = False

                item = item.get_parent_object()
