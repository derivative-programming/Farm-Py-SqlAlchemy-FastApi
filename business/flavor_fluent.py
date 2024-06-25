# business/flavor_fluent.py
# pylint: disable=unused-import

"""
This module contains the
FlavorFluentBusObj class,
which adds fluent properties
to the business object for a
Flavor.
"""

from decimal import Decimal  # noqa: F401
import uuid  # noqa: F401
from datetime import datetime, date  # noqa: F401
from .flavor_base import FlavorBaseBusObj


class FlavorFluentBusObj(FlavorBaseBusObj):
    """
    This class add fluent properties to the
    Base Flavor Business Object
    """

    # description

    def set_prop_description(self, value: str):
        """
        Set the Description for the
        Flavor object.

        :param value: The Description value.
        :return: The updated
            FlavorBusObj instance.
        """

        self.description = value
        return self
    # displayOrder

    def set_prop_display_order(self, value: int):
        """
        Set the value of
        display_order property.

        Args:
            value (int): The value to set for
                display_order.

        Returns:
            self: Returns the instance of the class.

        """
        self.display_order = value
        return self
    # isActive

    def set_prop_is_active(self, value: bool):
        """
        Set the Is Active flag for the
        Flavor object.

        :param value: The Is Active flag value.
        :return: The updated
            FlavorBusObj instance.
        """

        self.is_active = value
        return self
    # lookupEnumName

    def set_prop_lookup_enum_name(self, value: str):
        """
        Set the Lookup Enum Name for the
        Flavor object.

        :param value: The Lookup Enum Name value.
        :return: The updated
            FlavorBusObj instance.
        """

        self.lookup_enum_name = value
        return self
    # name

    def set_prop_name(self, value: str):
        """
        Set the Name for the
        Flavor object.

        :param value: The Name value.
        :return: The updated
            FlavorBusObj instance.
        """

        self.name = value
        return self
    # PacID
    # description,
    # displayOrder,
    # isActive,
    # lookupEnumName,
    # name,
    # PacID

    def set_prop_pac_id(self, value: int):
        """
        Set the pac ID for the
        flavor.

        Args:
            value (int): The pac id value.

        Returns:
            Flavor: The updated
                Flavor object.
        """

        self.pac_id = value
        return self

