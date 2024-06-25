# business/customer_role_fluent.py
# pylint: disable=unused-import

"""
This module contains the
CustomerRoleFluentBusObj class,
which adds fluent properties
to the business object for a
CustomerRole.
"""

from decimal import Decimal  # noqa: F401
import uuid  # noqa: F401
from datetime import datetime, date  # noqa: F401
from .customer_role_base import CustomerRoleBaseBusObj


class CustomerRoleFluentBusObj(CustomerRoleBaseBusObj):
    """
    This class add fluent properties to the
    Base CustomerRole Business Object
    """

    # CustomerID
    # isPlaceholder

    def set_prop_is_placeholder(self, value: bool):
        """
        Set the Is Placeholder flag for the
        CustomerRole object.

        :param value: The Is Placeholder flag value.
        :return: The updated
            CustomerRoleBusObj instance.
        """

        self.is_placeholder = value
        return self
    # placeholder

    def set_prop_placeholder(self, value: bool):
        """
        Set the Placeholder flag for the
        CustomerRole object.

        :param value: The Placeholder flag value.
        :return: The updated
            CustomerRoleBusObj instance.
        """

        self.placeholder = value
        return self
    # RoleID
    # CustomerID

    def set_prop_customer_id(self, value: int):
        """
        Set the customer ID for the
        customer_role.

        Args:
            value (int): The customer id value.

        Returns:
            CustomerRole: The updated
                CustomerRole object.
        """

        self.customer_id = value
        return self
    # isPlaceholder,
    # placeholder,
    # RoleID

    def set_prop_role_id(self, value: int):
        """
        Sets the value of the
        'role_id' property.

        Args:
            value (int): The value to set for the
                'role_id' property.

        Returns:
            self: The current instance of the class.

        """
        self.role_id = value
        return self

