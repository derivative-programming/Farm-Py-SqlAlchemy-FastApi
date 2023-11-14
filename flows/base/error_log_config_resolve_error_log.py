import uuid
from business.customer import CustomerBusObj
from business.error_log import ErrorLogBusObj
from managers.org_customer import OrgCustomerManager
from models import ErrorLog
from .base_flow import BaseFlow
from flows.base import LogSeverity
from helpers import SessionContext
from decimal import Decimal
from datetime import date, datetime
from helpers import TypeConversion
import flows.constants.error_log_config_resolve_error_log as FlowConstants
import models as farm_models
from business.factory import BusObjFactory
class BaseFlowErrorLogConfigResolveErrorLog(BaseFlow):
    def __init__(self, session_context:SessionContext):
        super(BaseFlowErrorLogConfigResolveErrorLog, self).__init__(
            "ErrorLogConfigResolveErrorLog",
            session_context,
            )
    async def _process_validation_rules(self,
            error_log_bus_obj: ErrorLogBusObj,

        ):
        super()._log_message_and_severity(LogSeverity.information_high_detail, "Validating...")

        await self._process_security_rules(error_log_bus_obj)
    async def _process_security_rules(self,
        error_log_bus_obj: ErrorLogBusObj,
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
        if customerCodeMatchRequired == True and len(self.queued_validation_errors) == 0:
            val = True
            item = error_log_bus_obj
            while val:
                if item.get_object_name() == "pac":
                    val = False

                if val == True:
                    # item = await item.get_parent_obj()
                    item = await BusObjFactory.create(item.session,item.get_parent_name(), item.get_parent_code())
