# flows/base/land_plant_list_init_report.py
"""
    #TODO add comment
"""
import uuid
from business.customer import CustomerBusObj
from business.land import LandBusObj
from managers.org_customer import OrgCustomerManager
from models import Land
from .base_flow import BaseFlow
from flows.base import LogSeverity
from helpers import SessionContext
from decimal import Decimal
from datetime import date, datetime
from helpers import TypeConversion
import flows.constants.land_plant_list_init_report as FlowConstants
import models as farm_models
from business.factory import BusObjFactory
class BaseFlowLandPlantListInitReport(BaseFlow):
    def __init__(self, session_context: SessionContext):
        super(BaseFlowLandPlantListInitReport, self).__init__(
            "LandPlantListInitReport",
            session_context,
            )
    async def _process_validation_rules(self,
            land_bus_obj: LandBusObj,

        ):
        super()._log_message_and_severity(LogSeverity.information_high_detail, "Validating...")

        await self._process_security_rules(land_bus_obj)
    async def _process_security_rules(self,
        land_bus_obj: LandBusObj,
        ):
        super()._log_message_and_severity(LogSeverity.information_high_detail, "Processing security rules...")
        customerCodeMatchRequired = False
        role_required = ""
        if len(role_required) > 0:
            if role_required not in self._session_context.role_name_csv:
                self._add_validation_error("Unautorized access. " + role_required + " role not found.")
        if FlowConstants.calculatedIsRowLevelCustomerSecurityUsed is True:
            customerCodeMatchRequired = True
        if FlowConstants.calculatedIsRowLevelOrganizationSecurityUsed is True:
            customerCodeMatchRequired = True
        if FlowConstants.calculatedIsRowLevelOrgCustomerSecurityUsed is True:
            customerCodeMatchRequired = True
        if customerCodeMatchRequired is True and len(self.queued_validation_errors) == 0:
            val = True
            item = land_bus_obj
            while val:
                if item.get_object_name() == "pac":
                    val = False

                if val is True:
                    # item = await item.get_parent_obj()
                    item = await BusObjFactory.create(item.session,item.get_parent_name(), item.get_parent_code())
