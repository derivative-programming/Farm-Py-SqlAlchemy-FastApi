# flows/base/tac_register.py
"""
    #TODO add comment
"""
import uuid
from datetime import date, datetime
from decimal import Decimal
import flows.constants.tac_register as FlowConstants
from business.customer import CustomerBusObj
# import models as farm_models
from business.factory import BusObjFactory
from business.tac import TacBusObj
from flows.base import LogSeverity
from helpers import SessionContext, TypeConversion
from managers.org_customer import OrgCustomerManager
# from models import Tac
from .base_flow import BaseFlow
class BaseFlowTacRegister(BaseFlow):
    """
    #TODO add comment
    """
    def __init__(self, session_context: SessionContext):
        """
        #TODO add comment
        """
        super(BaseFlowTacRegister, self).__init__(
            "TacRegister",
            session_context,
        )
    async def _process_validation_rules(
        self,
        tac_bus_obj: TacBusObj,
        email: str = "",
        password: str = "",
        confirm_password: str = "",
        first_name: str = "",
        last_name: str = "",
    ):
        """
        #TODO add comment
        """
        super()._log_message_and_severity(
            LogSeverity.INFORMATION_HIGH_DETAIL,
            "Validating...")
        if email == "" and \
                FlowConstants.param_email_isRequired \
                is True:
            self._add_field_validation_error(
                "email",
                "Please enter a Email"
            )
        if password == "" and \
                FlowConstants.param_password_isRequired \
                is True:
            self._add_field_validation_error(
                "password",
                "Please enter a Password"
            )
        if confirm_password == "" and \
                FlowConstants.param_confirm_password_isRequired \
                is True:
            self._add_field_validation_error(
                "confirmPassword",
                "Please enter a "
            )
        if first_name == "" and \
                FlowConstants.param_first_name_isRequired \
                is True:
            self._add_field_validation_error(
                "firstName",
                "Please enter a First Name"
            )
        if last_name == "" and \
                FlowConstants.param_last_name_isRequired \
                is True:
            self._add_field_validation_error(
                "lastName",
                "Please enter a Last Name"
            )
# end set
        await self._process_security_rules(tac_bus_obj)
    async def _process_security_rules(
        self,
        tac_bus_obj: TacBusObj,
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
        item = tac_bus_obj
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
