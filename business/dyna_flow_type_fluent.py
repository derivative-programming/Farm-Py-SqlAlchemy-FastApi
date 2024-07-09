# business/dyna_flow_type_fluent.py  # pylint: disable=duplicate-code # noqa: E501
# pylint: disable=unused-import

"""
This module contains the
DynaFlowTypeFluentBusObj class,
which adds fluent properties
to the business object for a
DynaFlowType.
"""

import uuid  # noqa: F401
from datetime import date, datetime, timezone  # noqa: F401
from decimal import Decimal  # noqa: F401

import managers as managers_and_enums

from .dyna_flow_type_base import DynaFlowTypeBaseBusObj


class DynaFlowTypeFluentBusObj(DynaFlowTypeBaseBusObj):
    """
    This class add fluent properties to the
    Base DynaFlowType Business Object
    """

    # description

    def set_prop_description(self, value: str):
        """
        Set the Description for the
        DynaFlowType object.

        :param value: The Description value.
        :return: The updated
            DynaFlowTypeBusObj instance.
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
        DynaFlowType object.

        :param value: The Is Active flag value.
        :return: The updated
            DynaFlowTypeBusObj instance.
        """

        self.is_active = value
        return self
    # lookupEnumName

    def set_prop_lookup_enum_name(self, value: str):
        """
        Set the Lookup Enum Name for the
        DynaFlowType object.

        :param value: The Lookup Enum Name value.
        :return: The updated
            DynaFlowTypeBusObj instance.
        """

        self.lookup_enum_name = value
        return self
    # name

    def set_prop_name(self, value: str):
        """
        Set the Name for the
        DynaFlowType object.

        :param value: The Name value.
        :return: The updated
            DynaFlowTypeBusObj instance.
        """

        self.name = value
        return self
    # PacID
    # priorityLevel

    def set_prop_priority_level(self, value: int):
        """
        Set the value of
        priority_level property.

        Args:
            value (int): The value to set for
                priority_level.

        Returns:
            self: Returns the instance of the class.

        """
        self.priority_level = value
        return self
    # description
    # displayOrder
    # isActive
    # lookupEnumName
    # name
    # PacID

    def set_prop_pac_id(self, value: int):
        """
        Set the pac ID for the
        dyna_flow_type.

        Args:
            value (int): The pac id value.

        Returns:
            DynaFlowType: The updated
                DynaFlowType object.
        """

        self.pac_id = value
        return self
    # priorityLevel
