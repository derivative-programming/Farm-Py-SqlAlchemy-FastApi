import uuid
from business.customer import CustomerBusObj
from business.customer import CustomerBusObj
from managers.org_customer import OrgCustomerManager
from models import Customer
from .base_flow import BaseFlow
from flows.base import LogSeverity
from helpers import SessionContext
from decimal import Decimal
from datetime import date, datetime
from helpers import TypeConversion
import flows.constants.customer_user_log_out as FlowConstants
import models as farm_models
from business.factory import BusObjFactory
class BaseFlowCustomerUserLogOut(BaseFlow):
    def __init__(self, session_context:SessionContext):
        super(BaseFlowCustomerUserLogOut, self).__init__(
            "CustomerUserLogOut",
            session_context,
            )
    async def _process_validation_rules(self,
            customer_bus_obj: CustomerBusObj,

        ):
        super()._log_message_and_severity(LogSeverity.information_high_detail, "Validating...")

        await self._process_security_rules(customer_bus_obj)
    async def _process_security_rules(self,
        customer_bus_obj: CustomerBusObj,
        ):
        super()._log_message_and_severity(LogSeverity.information_high_detail, "Processing security rules...")
        customerCodeMatchRequired = False
        role_required = "User"
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
            item = customer_bus_obj
            while val:
                if item.get_object_name() == "pac":
                    val = False

                if FlowConstants.calculatedIsRowLevelCustomerSecurityUsed == True:
                    if item.get_object_name() == "customer":
                        if item.code != self._session_context.customer_code:
                            self._add_validation_error("Unautorized access.  Invalid User.")

                if val == True:
                    # item = await item.get_parent_obj()
                    item = await BusObjFactory.create(item.session,item.get_parent_name(), item.get_parent_code())
