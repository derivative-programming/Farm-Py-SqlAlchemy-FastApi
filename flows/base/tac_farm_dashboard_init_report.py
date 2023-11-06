import uuid
from models import Tac
from .base_flow import BaseFlow
from flows.base import LogSeverity
from helpers import SessionContext
from decimal import Decimal
from datetime import date, datetime
from helpers import TypeConversion
import flows.constants.tac_farm_dashboard_init_report as FlowConstants
import models as farm_models
class BaseFlowTacFarmDashboardInitReport(BaseFlow):
    def __init__(self, session_context:SessionContext):
        super(BaseFlowTacFarmDashboardInitReport, self).__init__(
            "TacFarmDashboardInitReport",
            session_context,
            )
    def _process_validation_rules(self,
            tac: Tac,

        ):
        super()._log_message_and_severity(LogSeverity.information_high_detail, "Validating...")

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
