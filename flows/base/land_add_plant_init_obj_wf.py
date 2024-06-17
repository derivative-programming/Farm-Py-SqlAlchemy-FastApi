# flows/base/land_add_plant_init_obj_wf.py
"""
    #TODO add comment
"""
import uuid
from datetime import date, datetime
from decimal import Decimal
import flows.constants.land_add_plant_init_obj_wf as FlowConstants
from business.customer import CustomerBusObj
# import models as farm_models
from business.factory import BusObjFactory
from business.land import LandBusObj
from flows.base import LogSeverity
from helpers import SessionContext, TypeConversion
from managers.org_customer import OrgCustomerManager
# from models import Land
from .base_flow import BaseFlow
class BaseFlowLandAddPlantInitObjWF(BaseFlow):
    """
    #TODO add comment
    """
    def __init__(self, session_context: SessionContext):
        """
        #TODO add comment
        """
        super(BaseFlowLandAddPlantInitObjWF, self).__init__(
            "LandAddPlantInitObjWF",
            session_context,
        )
    async def _process_validation_rules(
        self,
        land_bus_obj: LandBusObj,

    ):
        """
        #TODO add comment
        """
        super()._log_message_and_severity(
            LogSeverity.information_high_detail,
            "Validating...")

# end set
        await self._process_security_rules(land_bus_obj)
    async def _process_security_rules(
        self,
        land_bus_obj: LandBusObj,
    ):
        super()._log_message_and_severity(
            LogSeverity.information_high_detail,
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
        item = land_bus_obj
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
