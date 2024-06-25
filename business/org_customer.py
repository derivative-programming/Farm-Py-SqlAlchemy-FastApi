# business/org_customer.py
# pylint: disable=unused-import
"""
This module contains the
OrgCustomerBusObj class,
which represents the
business object for a
OrgCustomer.
"""

from typing import List
from helpers.session_context import SessionContext
from models import OrgCustomer
import managers as managers_and_enums  # noqa: F401
from .org_customer_fluent import OrgCustomerFluentBusObj


NOT_INITIALIZED_ERROR_MESSAGE = (
    "OrgCustomer object is not initialized")


class OrgCustomerBusObj(OrgCustomerFluentBusObj):
    """
    This class represents the business object for a OrgCustomer.
    It requires a valid session context for initialization.
    """

    @staticmethod
    async def to_bus_obj_list(
        session_context: SessionContext,
        obj_list: List[OrgCustomer]
    ):
        """
        Convert a list of OrgCustomer
        objects to a list of
        OrgCustomerBusObj objects.

        Args:
            session_context (SessionContext): The session context.
            obj_list (List[OrgCustomer]): The
                list of OrgCustomer objects to convert.

        Returns:
            List[OrgCustomerBusObj]: The
                list of converted OrgCustomerBusObj
                objects.
        """
        result = list()

        for org_customer in obj_list:
            org_customer_bus_obj = OrgCustomerBusObj(session_context)

            org_customer_bus_obj.load_from_obj_instance(
                org_customer)

            result.append(org_customer_bus_obj)

        return result

