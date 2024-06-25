# flows/base/pac_user_flavor_list_init_report.py

"""
This module contains the implementation
of the BaseFlow
Pac User Flavor List Init Report class
"""

import uuid
from datetime import date, datetime
from decimal import Decimal

import flows.constants.pac_user_flavor_list_init_report as FlowConstants
from business.customer import CustomerBusObj
from business.factory import BusObjFactory
from business.pac import PacBusObj
from flows.base import LogSeverity
from helpers import SessionContext, TypeConversion
from managers.org_customer import OrgCustomerManager

# from models import Pac
from .base_flow import BaseFlow


class BaseFlowPacUserFlavorListInitReport(BaseFlow):
    """
    Base class for PacUserFlavorListInitReport flow. Contains
    some validaiton and security check logic
    """

    def __init__(self, session_context: SessionContext):
        """
        Initializes a new instance of the
        BaseFlowPacUserFlavorListInitReport class.

        Args:
            session_context (SessionContext): The session context for the flow.
        """

        super(BaseFlowPacUserFlavorListInitReport, self).__init__(
            "PacUserFlavorListInitReport",
            session_context,
        )

    async def _process_validation_rules(
        self,
        pac_bus_obj: PacBusObj,

    ):
        """
        Processes the validation rules for adding s to pac.

        """

        super()._log_message_and_severity(
            LogSeverity.INFORMATION_HIGH_DETAIL,
            "Validating...")

# end set

        await self._process_security_rules(pac_bus_obj)

    async def _process_security_rules(
        self,
        pac_bus_obj: PacBusObj,
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
                    f"Unauthorized access. {role_required} role not found."
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

        item = pac_bus_obj

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

