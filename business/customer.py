# business/customer.py
# pylint: disable=unused-import
"""
This module contains the CustomerBusObj class,
which represents the business object for a Customer.
"""

from typing import List
from helpers.session_context import SessionContext
from models import Customer
import managers as managers_and_enums  # noqa: F401
from .customer_fluent import CustomerFluentBusObj


from business.customer_role import CustomerRoleBusObj


NOT_INITIALIZED_ERROR_MESSAGE = (
    "Customer object is not initialized")


class CustomerBusObj(CustomerFluentBusObj):
    """
    This class represents the business object for a Customer.
    It requires a valid session context for initialization.
    """

    @staticmethod
    async def to_bus_obj_list(
        session_context: SessionContext,
        obj_list: List[Customer]
    ):
        """
        Convert a list of Customer
        objects to a list of
        CustomerBusObj objects.

        Args:
            session_context (SessionContext): The session context.
            obj_list (List[Customer]): The
                list of Customer objects to convert.

        Returns:
            List[CustomerBusObj]: The
                list of converted CustomerBusObj
                objects.
        """
        result = list()

        for customer in obj_list:
            customer_bus_obj = CustomerBusObj(session_context)

            customer_bus_obj.load_from_obj_instance(
                customer)

            result.append(customer_bus_obj)

        return result


    async def build_customer_role(self) -> CustomerRoleBusObj:
        """
        build customer_role
        instance (not saved yet)
        """
        item = CustomerRoleBusObj(self._session_context)

        assert item.customer_role is not None
        role_manager = managers_and_enums.RoleManager(self._session_context)
        role_id_role = await role_manager.from_enum(
            managers_and_enums.RoleEnum.UNKNOWN)
        item.role_id = role_id_role.role_id
        item.customer_role.role_id_code_peek = role_id_role.code

        item.customer_id = self.customer_id
        item.customer_role.customer_code_peek = self.code

        return item

    async def get_all_customer_role(self) -> List[CustomerRoleBusObj]:
        """
        get all customer_role
        """
        results = list()
        customer_role_manager = managers_and_enums.CustomerRoleManager(self._session_context)
        obj_list = await customer_role_manager.get_by_customer_id(self.customer_id)
        for obj_item in obj_list:
            bus_obj_item = CustomerRoleBusObj(self._session_context)
            bus_obj_item.load_from_obj_instance(obj_item)
            results.append(bus_obj_item)
        return results

