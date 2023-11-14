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
import flows.constants.land_user_plant_multi_select_to_not_editable as FlowConstants
import models as farm_models
from business.factory import BusObjFactory
class BaseFlowLandUserPlantMultiSelectToNotEditable(BaseFlow):
    def __init__(self, session_context:SessionContext):
        super(BaseFlowLandUserPlantMultiSelectToNotEditable, self).__init__(
            "LandUserPlantMultiSelectToNotEditable",
            session_context,
            )
    async def _process_validation_rules(self,
            land_bus_obj: LandBusObj,
            plant_code_list_csv:str = "",
        ):
        super()._log_message_and_severity(LogSeverity.information_high_detail, "Validating...")
        if plant_code_list_csv == "" and FlowConstants.param_plant_code_list_csv_isRequired == True:
            self._add_field_validation_error("plantCodeListCsv","Please enter a plant Code List Csv")
        await self._process_security_rules(land_bus_obj)
    async def _process_security_rules(self,
        land_bus_obj: LandBusObj,
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
            item = land_bus_obj
            while val:
                if item.get_object_name() == "pac":
                    val = False

                if val == True:
                    # item = await item.get_parent_obj()
                    item = await BusObjFactory.create(item.session,item.get_parent_name(), item.get_parent_code())
