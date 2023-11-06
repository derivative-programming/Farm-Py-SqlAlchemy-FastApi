import uuid
from models import ErrorLog
from .base_flow import BaseFlow
from flows.base import LogSeverity
from helpers import SessionContext
from decimal import Decimal
from datetime import date, datetime
from helpers import TypeConversion
import flows.constants.error_log_config_resolve_error_log as FlowConstants
import models as farm_models
class BaseFlowErrorLogConfigResolveErrorLog(BaseFlow):
    def __init__(self, session_context:SessionContext):
        super(BaseFlowErrorLogConfigResolveErrorLog, self).__init__(
            "ErrorLogConfigResolveErrorLog",
            session_context,
            )
    def _process_validation_rules(self,
            error_log: ErrorLog,

        ):
        super()._log_message_and_severity(LogSeverity.information_high_detail, "Validating...")

        self._process_security_rules(error_log)
    def _process_security_rules(self,
        error_log: ErrorLog,
        ):
        super()._log_message_and_severity(LogSeverity.information_high_detail, "Processing security rules...")
        customerCodeMatchRequired = False
        role_required = "Config"
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
            item = error_log
            while val:
                if item.get_object_name() == "pac":
                    val = False

                item = item.get_parent_object()
