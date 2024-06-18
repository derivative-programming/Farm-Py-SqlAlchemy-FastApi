# flows/base/land_user_plant_multi_select_to_not_editable.py
"""
    #TODO add comment
"""
import uuid
from datetime import date, datetime
from decimal import Decimal
import flows.constants.land_user_plant_multi_select_to_not_editable as FlowConstants
from business.customer import CustomerBusObj
from business.factory import BusObjFactory
from business.land import LandBusObj
from flows.base import LogSeverity
from helpers import SessionContext, TypeConversion
from managers.org_customer import OrgCustomerManager
# from models import Land
from .base_flow import BaseFlow
class BaseFlowLandUserPlantMultiSelectToNotEditable(BaseFlow):
    """
    #TODO add comment
    """
    def __init__(self, session_context: SessionContext):
        """
        #TODO add comment
        """
        super(BaseFlowLandUserPlantMultiSelectToNotEditable, self).__init__(
            "LandUserPlantMultiSelectToNotEditable",
            session_context,
        )
    async def _process_validation_rules(
        self,
        land_bus_obj: LandBusObj,
        plant_code_list_csv: str = "",
    ):
        """
        #TODO add comment
        """
        super()._log_message_and_severity(
            LogSeverity.INFORMATION_HIGH_DETAIL,
            "Validating...")
        if plant_code_list_csv == "" and \
            FlowConstants.PARAM_PLANT_CODE_LIST_CSV_IS_REQUIRED \
                is True:
            self._add_field_validation_error(
                "plantCodeListCsv",
                "Please enter a plant Code List Csv"
            )
# end set
        await self._process_security_rules(land_bus_obj)
    async def _process_security_rules(
        self,
        land_bus_obj: LandBusObj,
    ):
        super()._log_message_and_severity(
            LogSeverity.INFORMATION_HIGH_DETAIL,
            "Processing security rules..."
        )
        customer_code_match_required = False
        role_required = "User"
        if len(role_required) > 0:
            if role_required not in self._session_context.role_name_csv:
                self._add_validation_error(
                    "Unautorized access. " + role_required + " role not found."
                )
        if FlowConstants.CALCULATED_IS_ROW_LEVEL_CUSTOMER_SECURITY_USED \
                is True:
            customer_code_match_required = True
        if FlowConstants.CALCULATED_IS_ROW_LEVEL_ORGANIZATION_SECURITY_USED \
                is True:
            customer_code_match_required = True
        if FlowConstants.CALCULATED_IS_ROW_LEVEL_ORG_CUSTOMER_SECURITY_USED \
                is True:
            customer_code_match_required = True
        if len(self.queued_validation_errors) > 0:
            return
        if customer_code_match_required is False:
            return
        val = True
        item = land_bus_obj
        while val:
            if item.get_object_name() == "pac":  # type: ignore
                val = False

            if val is True:
                # item = await item.get_parent_obj()
                item = await BusObjFactory.create_from_code(
                    item.get_session_context(),  # type: ignore
                    item.get_parent_name(),  # type: ignore
                    item.get_parent_code()  # type: ignore
                )
