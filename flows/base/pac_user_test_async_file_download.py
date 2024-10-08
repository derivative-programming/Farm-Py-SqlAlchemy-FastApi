# flows/base/pac_user_test_async_file_download.py  # pylint: disable=duplicate-code # noqa: E501
# pylint: disable=unused-import

"""
This module contains the implementation
of the BaseFlow
Pac User Test Async File Download class
"""

import uuid  # noqa: F401
from datetime import date, datetime, timezone  # noqa: F401
from decimal import Decimal  # noqa: F401

import flows.constants.pac_user_test_async_file_download \
    as FlowConstants
from business.customer import CustomerBusObj  # noqa: F401
from business.factory import BusObjFactory
from business.pac import PacBusObj
from flows.base import LogSeverity
from helpers import SessionContext, TypeConversion  # noqa: F401
from managers.org_customer import OrgCustomerManager  # noqa: F401

from .base_flow import BaseFlow


class BaseFlowPacUserTestAsyncFileDownload(BaseFlow):  # pylint: disable=too-few-public-methods
    """
    Base class for PacUserTestAsyncFileDownload
    flow. Contains
    some validaiton and security check logic
    """

    def __init__(self, session_context: SessionContext):
        """
        Initializes a new instance of the
        BaseFlowPacUserTestAsyncFileDownload class.

        Args:
            session_context (SessionContext): The session context for the flow.
        """

        super().__init__(
            "PacUserTestAsyncFileDownload",
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

        item = pac_bus_obj

        while val:
            if item.get_object_name() == "pac":  # type: ignore
                val = False


            if val is True:
                item = await BusObjFactory.create_from_code(
                    item.get_session_context(),  # type: ignore
                    item.get_parent_name(),  # type: ignore
                    item.get_parent_code()  # type: ignore
                )
