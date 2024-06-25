# business/customer_role.py
# pylint: disable=unused-import
"""
This module contains the
CustomerRoleBusObj class,
which represents the
business object for a
CustomerRole.
"""

from typing import List
from helpers.session_context import SessionContext
from models import CustomerRole
import managers as managers_and_enums  # noqa: F401
from .customer_role_fluent import CustomerRoleFluentBusObj


NOT_INITIALIZED_ERROR_MESSAGE = (
    "CustomerRole object is not initialized")


class CustomerRoleBusObj(CustomerRoleFluentBusObj):
    """
    This class represents the business object for a CustomerRole.
    It requires a valid session context for initialization.
    """

    @staticmethod
    async def to_bus_obj_list(
        session_context: SessionContext,
        obj_list: List[CustomerRole]
    ):
        """
        Convert a list of CustomerRole
        objects to a list of
        CustomerRoleBusObj objects.

        Args:
            session_context (SessionContext): The session context.
            obj_list (List[CustomerRole]): The
                list of CustomerRole objects to convert.

        Returns:
            List[CustomerRoleBusObj]: The
                list of converted CustomerRoleBusObj
                objects.
        """
        result = list()

        for customer_role in obj_list:
            customer_role_bus_obj = CustomerRoleBusObj(session_context)

            customer_role_bus_obj.load_from_obj_instance(
                customer_role)

            result.append(customer_role_bus_obj)

        return result

