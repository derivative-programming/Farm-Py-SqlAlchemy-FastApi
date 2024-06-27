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
import models
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
    # CustomerID

    async def get_customer_id_obj(self) -> models.Customer:
        """
        Retrieves the related Customer object based
        on the customer_id.

        Returns:
            An instance of the Customer model
            representing the related customer.

        """
        customer_manager = managers_and_enums.CustomerManager(
            self._session_context)
        customer_obj = await customer_manager.get_by_id(
            self.customer_id)
        return customer_obj

    async def get_customer_id_bus_obj(self):
        """
        Retrieves the related Customer
        business object based
        on the customer_id.

        Returns:
            An instance of the Customer
            business object
            representing the related customer.

        """
        from .customer import CustomerBusObj  # pylint: disable=import-outside-toplevel
        bus_obj = CustomerBusObj(self._session_context)
        await bus_obj.load_from_id(self.customer_id)
        return bus_obj
    # isPlaceholder,
    # placeholder,
    # RoleID

    async def get_role_id_obj(self) -> models.Role:
        """
        Retrieves the related Role object based on the
        role_id.

        Returns:
            The related Role object.

        """
        role_manager = managers_and_enums.RoleManager(
            self._session_context)
        role_obj = await role_manager.get_by_id(
            self.role_id
        )
        return role_obj

    async def get_role_id_bus_obj(self):
        """
        Retrieves the related Role
        business object based on the
        role_id.

        Returns:
            The related Role
            business object.

        """
        from .role import RoleBusObj  # pylint: disable=import-outside-toplevel
        bus_obj = RoleBusObj(self._session_context)
        await bus_obj.load_from_id(self.role_id)
        return bus_obj
