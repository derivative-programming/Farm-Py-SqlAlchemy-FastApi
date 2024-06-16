# flows/base/error_log_config_resolve_error_log.py
"""
    #TODO add comment
"""
import uuid
from datetime import date, datetime
from decimal import Decimal
import flows.constants.error_log_config_resolve_error_log as FlowConstants
from business.customer import CustomerBusObj
# import models as farm_models
from business.factory import BusObjFactory
from business.error_log import ErrorLogBusObj
from flows.base import LogSeverity
from helpers import SessionContext, TypeConversion
from managers.org_customer import OrgCustomerManager
# from models import ErrorLog
from .base_flow import BaseFlow
class BaseFlowErrorLogConfigResolveErrorLog(BaseFlow):
    """
    #TODO add comment
    """
    def __init__(self, session_context: SessionContext):
        """
        #TODO add comment
        """
        super(BaseFlowErrorLogConfigResolveErrorLog, self).__init__(
            "ErrorLogConfigResolveErrorLog",
            session_context,
        )
    async def _process_validation_rules(
        self,
        error_log_bus_obj: ErrorLogBusObj,

    ):
        """
        #TODO add comment
        """
        super()._log_message_and_severity(LogSeverity.information_high_detail, "Validating...")

# end set
        await self._process_security_rules(error_log_bus_obj)
    async def _process_security_rules(
        self,
        error_log_bus_obj: ErrorLogBusObj,
    ):
        super()._log_message_and_severity(
            LogSeverity.information_high_detail,
            "Processing security rules..."
        )
        customerCodeMatchRequired = False
        role_required = "Config"
        if len(role_required) > 0:
            if role_required not in self._session_context.role_name_csv:
                self._add_validation_error(
                    "Unautorized access. " + role_required + " role not found."
                )
        if FlowConstants.calculatedIsRowLevelCustomerSecurityUsed is True:
            customerCodeMatchRequired = True
        if FlowConstants.calculatedIsRowLevelOrganizationSecurityUsed is True:
            customerCodeMatchRequired = True
        if FlowConstants.calculatedIsRowLevelOrgCustomerSecurityUsed is True:
            customerCodeMatchRequired = True
        if len(self.queued_validation_errors) > 0:
            return
        if customerCodeMatchRequired is False:
            return
        val = True
        item = error_log_bus_obj
        while val:
            if item.get_object_name() == "pac":
                val = False

            if val is True:
                # item = await item.get_parent_obj()
                item = await BusObjFactory.create(
                    item.session,
                    item.get_parent_name(),
                    item.get_parent_code()
                )
