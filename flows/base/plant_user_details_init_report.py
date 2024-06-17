# flows/base/plant_user_details_init_report.py
"""
    #TODO add comment
"""
import uuid
from datetime import date, datetime
from decimal import Decimal
import flows.constants.plant_user_details_init_report as FlowConstants
from business.customer import CustomerBusObj
# import models as farm_models
from business.factory import BusObjFactory
from business.plant import PlantBusObj
from flows.base import LogSeverity
from helpers import SessionContext, TypeConversion
from managers.org_customer import OrgCustomerManager
# from models import Plant
from .base_flow import BaseFlow
class BaseFlowPlantUserDetailsInitReport(BaseFlow):
    """
    #TODO add comment
    """
    def __init__(self, session_context: SessionContext):
        """
        #TODO add comment
        """
        super(BaseFlowPlantUserDetailsInitReport, self).__init__(
            "PlantUserDetailsInitReport",
            session_context,
        )
    async def _process_validation_rules(
        self,
        plant_bus_obj: PlantBusObj,

    ):
        """
        #TODO add comment
        """
        super()._log_message_and_severity(
            LogSeverity.INFORMATION_HIGH_DETAIL,
            "Validating...")

# end set
        await self._process_security_rules(plant_bus_obj)
    async def _process_security_rules(
        self,
        plant_bus_obj: PlantBusObj,
    ):
        super()._log_message_and_severity(
            LogSeverity.INFORMATION_HIGH_DETAIL,
            "Processing security rules..."
        )
        customer_code_match_required = False
        role_required = ""
        if len(role_required) > 0:
            if role_required not in self._session_context.role_name_csv:
                self._add_validation_error(
                    "Unautorized access. " + role_required + " role not found."
                )
        if FlowConstants.calculatedIsRowLevelCustomerSecurityUsed is True:
            customer_code_match_required = True
        if FlowConstants.calculatedIsRowLevelOrganizationSecurityUsed is True:
            customer_code_match_required = True
        if FlowConstants.calculatedIsRowLevelOrgCustomerSecurityUsed is True:
            customer_code_match_required = True
        if len(self.queued_validation_errors) > 0:
            return
        if customer_code_match_required is False:
            return
        val = True
        item = plant_bus_obj
        while val:
            if item.get_object_name() == "pac":
                val = False

            if val is True:
                # item = await item.get_parent_obj()
                item = await BusObjFactory.create(
                    item.get_session_context(),
                    item.get_parent_name(),
                    item.get_parent_code()
                )
