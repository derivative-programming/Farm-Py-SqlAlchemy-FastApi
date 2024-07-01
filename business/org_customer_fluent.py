# business/org_customer_fluent.py
# pylint: disable=unused-import

"""
This module contains the
OrgCustomerFluentBusObj class,
which adds fluent properties
to the business object for a
OrgCustomer.
"""

import uuid  # noqa: F401
from datetime import date, datetime  # noqa: F401
from decimal import Decimal  # noqa: F401

import managers as managers_and_enums

from .org_customer_base import OrgCustomerBaseBusObj


class OrgCustomerFluentBusObj(OrgCustomerBaseBusObj):
    """
    This class add fluent properties to the
    Base OrgCustomer Business Object
    """

    # CustomerID
    # email

    def set_prop_email(self, value: str):
        """
        Set the value of the
        email property.

        Args:
            value (str): The Email
                to set.

        Returns:
            self: The current instance of the class.
        """
        self.email = value
        return self
    # OrganizationID
    # CustomerID

    def set_prop_customer_id(self, value: int):
        """
        Sets the value of the
        'customer_id' property.

        Args:
            value (int): The value to set for the
                'customer_id' property.

        Returns:
            self: The current instance of the class.

        """
        self.customer_id = value
        return self

    async def set_prop_customer_id_by_enum(
        self,
        customer_enum: managers_and_enums.CustomerEnum
    ):
        """
        """
        if not isinstance(
            customer_enum,
            managers_and_enums.CustomerEnum
        ):
            raise ValueError("customer_enum must be a CustomerEnum")

        customer_manager =  \
            managers_and_enums.CustomerManager(
                self._session_context
            )
        customer_obj = await (
            customer_manager.
            from_enum(customer_enum)
        )

        self.customer_id = customer_obj.customer_id
        return self
    # email,
    # OrganizationID

    def set_prop_organization_id(self, value: int):
        """
        Set the organization ID for the
        org_customer.

        Args:
            value (int): The organization id value.

        Returns:
            OrgCustomer: The updated
                OrgCustomer object.
        """

        self.organization_id = value
        return self
