# business/tri_state_filter_fluent.py

"""
This module contains the TriStateFilterFluentBusObj class,
which adds fluent properties to the business object for a TriStateFilter.
"""

from decimal import Decimal
import uuid
from datetime import datetime, date
from .tri_state_filter_base import TriStateFilterBaseBusObj


class TriStateFilterFluentBusObj(TriStateFilterBaseBusObj):
    """
    This class add fluent properties to the
    Base TriStateFilter Business Object
    """

    # description

    def set_prop_description(self, value: str):
        """
        Set the Description for the
        TriStateFilter object.

        :param value: The Description value.
        :return: The updated
            TriStateFilterBusObj instance.
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
        TriStateFilter object.

        :param value: The Is Active flag value.
        :return: The updated
            TriStateFilterBusObj instance.
        """

        self.is_active = value
        return self
    # lookupEnumName

    def set_prop_lookup_enum_name(self, value: str):
        """
        Set the Lookup Enum Name for the
        TriStateFilter object.

        :param value: The Lookup Enum Name value.
        :return: The updated
            TriStateFilterBusObj instance.
        """

        self.lookup_enum_name = value
        return self
    # name

    def set_prop_name(self, value: str):
        """
        Set the Name for the
        TriStateFilter object.

        :param value: The Name value.
        :return: The updated
            TriStateFilterBusObj instance.
        """

        self.name = value
        return self
    # PacID
    # stateIntValue

    def set_prop_state_int_value(self, value: int):
        """
        Set the value of
        state_int_value property.

        Args:
            value (int): The value to set for
                state_int_value.

        Returns:
            self: Returns the instance of the class.

        """
        self.state_int_value = value
        return self
    # description,
    # displayOrder,
    # isActive,
    # lookupEnumName,
    # name,
    # PacID

    def set_prop_pac_id(self, value: int):
        """
        Set the pac ID for the
        tri_state_filter.

        Args:
            value (int): The pac id value.

        Returns:
            TriStateFilter: The updated
                TriStateFilter object.
        """

        self.pac_id = value
        return self
    # stateIntValue,

