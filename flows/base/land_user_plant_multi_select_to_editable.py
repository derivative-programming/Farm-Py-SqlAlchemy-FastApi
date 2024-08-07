# flows/base/land_user_plant_multi_select_to_editable.py  # pylint: disable=duplicate-code # noqa: E501
# pylint: disable=unused-import

"""
This module contains the implementation
of the BaseFlow
Land User Plant Multi Select To Editable class
"""

import uuid  # noqa: F401
from datetime import date, datetime, timezone  # noqa: F401
from decimal import Decimal  # noqa: F401

import flows.constants.land_user_plant_multi_select_to_editable \
    as FlowConstants
from business.customer import CustomerBusObj  # noqa: F401
from business.factory import BusObjFactory
from business.land import LandBusObj
from flows.base import LogSeverity
from helpers import SessionContext, TypeConversion  # noqa: F401
from managers.org_customer import OrgCustomerManager  # noqa: F401

from .base_flow import BaseFlow


class BaseFlowLandUserPlantMultiSelectToEditable(BaseFlow):  # pylint: disable=too-few-public-methods
    """
    Base class for LandUserPlantMultiSelectToEditable
    flow. Contains
    some validaiton and security check logic
    """

    def __init__(self, session_context: SessionContext):
        """
        Initializes a new instance of the
        BaseFlowLandUserPlantMultiSelectToEditable class.

        Args:
            session_context (SessionContext): The session context for the flow.
        """

        super().__init__(
            "LandUserPlantMultiSelectToEditable",
            session_context,
        )

    async def _process_validation_rules(
        self,
        land_bus_obj: LandBusObj,
        plant_code_list_csv: str = "",
    ):
        """
        Processes the validation rules for adding s to land.

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

        item = land_bus_obj

        while val:
            if item.get_object_name() == "pac":  # type: ignore
                val = False


            if val is True:
                item = await BusObjFactory.create_from_code(
                    item.get_session_context(),  # type: ignore
                    item.get_parent_name(),  # type: ignore
                    item.get_parent_code()  # type: ignore
                )
