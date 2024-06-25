# business/organization_fluent.py
# pylint: disable=unused-import

"""
This module contains the
OrganizationFluentBusObj class,
which adds fluent properties
to the business object for a
Organization.
"""

from decimal import Decimal  # noqa: F401
import uuid  # noqa: F401
from datetime import datetime, date  # noqa: F401
from .organization_base import OrganizationBaseBusObj


class OrganizationFluentBusObj(OrganizationBaseBusObj):
    """
    This class add fluent properties to the
    Base Organization Business Object
    """

    # name

    def set_prop_name(self, value: str):
        """
        Set the Name for the
        Organization object.

        :param value: The Name value.
        :return: The updated
            OrganizationBusObj instance.
        """

        self.name = value
        return self
    # TacID
    # name,
    # TacID

    def set_prop_tac_id(self, value: int):
        """
        Set the tac ID for the
        organization.

        Args:
            value (int): The tac id value.

        Returns:
            Organization: The updated
                Organization object.
        """

        self.tac_id = value
        return self

