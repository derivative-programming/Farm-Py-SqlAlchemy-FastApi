# business/date_greater_than_filter_fluent.py  # pylint: disable=duplicate-code # noqa: E501
# pylint: disable=unused-import

"""
This module contains the
DateGreaterThanFilterFluentBusObj class,
which adds fluent properties
to the business object for a
DateGreaterThanFilter.
"""

import uuid  # noqa: F401
from datetime import date, datetime, timezone  # noqa: F401
from decimal import Decimal  # noqa: F401

import managers as managers_and_enums

from .date_greater_than_filter_base import DateGreaterThanFilterBaseBusObj


class DateGreaterThanFilterFluentBusObj(DateGreaterThanFilterBaseBusObj):
    """
    This class add fluent properties to the
    Base DateGreaterThanFilter Business Object
    """

    # dayCount

    def set_prop_day_count(self, value: int):
        """
        Set the value of
        day_count property.

        Args:
            value (int): The value to set for
                day_count.

        Returns:
            self: Returns the instance of the class.

        """
        self.day_count = value
        return self
    # description

    def set_prop_description(self, value: str):
        """
        Set the Description for the
        DateGreaterThanFilter object.

        :param value: The Description value.
        :return: The updated
            DateGreaterThanFilterBusObj instance.
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
        DateGreaterThanFilter object.

        :param value: The Is Active flag value.
        :return: The updated
            DateGreaterThanFilterBusObj instance.
        """

        self.is_active = value
        return self
    # lookupEnumName

    def set_prop_lookup_enum_name(self, value: str):
        """
        Set the Lookup Enum Name for the
        DateGreaterThanFilter object.

        :param value: The Lookup Enum Name value.
        :return: The updated
            DateGreaterThanFilterBusObj instance.
        """

        self.lookup_enum_name = value
        return self
    # name

    def set_prop_name(self, value: str):
        """
        Set the Name for the
        DateGreaterThanFilter object.

        :param value: The Name value.
        :return: The updated
            DateGreaterThanFilterBusObj instance.
        """

        self.name = value
        return self
    # PacID
    # dayCount
    # description
    # displayOrder
    # isActive
    # lookupEnumName
    # name
    # PacID

    def set_prop_pac_id(self, value: int):
        """
        Set the pac ID for the
        date_greater_than_filter.

        Args:
            value (int): The pac id value.

        Returns:
            DateGreaterThanFilter: The updated
                DateGreaterThanFilter object.
        """

        self.pac_id = value
        return self
