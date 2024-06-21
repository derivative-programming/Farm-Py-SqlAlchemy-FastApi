# business/organization_fluent.py
"""
This module contains the OrganizationBusObj class,
which represents the business object for a Organization.
"""
from decimal import Decimal
import uuid
from datetime import datetime, date
from .organization_base import OrganizationBaseBusObj
class OrganizationFluentBusObj(OrganizationBaseBusObj):
    """
    This class add fluent properties to the
    Base Organization Business Object
    """
# endset
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
# endset
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
# endset
