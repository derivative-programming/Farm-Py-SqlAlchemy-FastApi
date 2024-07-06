# business/dyna_flow_type_schedule_fluent.py  # pylint: disable=duplicate-code
# pylint: disable=unused-import

"""
This module contains the
DynaFlowTypeScheduleFluentBusObj class,
which adds fluent properties
to the business object for a
DynaFlowTypeSchedule.
"""

import uuid  # noqa: F401
from datetime import date, datetime, timezone  # noqa: F401
from decimal import Decimal  # noqa: F401

import managers as managers_and_enums

from .dyna_flow_type_schedule_base import DynaFlowTypeScheduleBaseBusObj


class DynaFlowTypeScheduleFluentBusObj(DynaFlowTypeScheduleBaseBusObj):
    """
    This class add fluent properties to the
    Base DynaFlowTypeSchedule Business Object
    """

    # DynaFlowTypeID
    # frequencyInHours

    def set_prop_frequency_in_hours(self, value: int):
        """
        Set the value of
        frequency_in_hours property.

        Args:
            value (int): The value to set for
                frequency_in_hours.

        Returns:
            self: Returns the instance of the class.

        """
        self.frequency_in_hours = value
        return self
    # isActive

    def set_prop_is_active(self, value: bool):
        """
        Set the Is Active flag for the
        DynaFlowTypeSchedule object.

        :param value: The Is Active flag value.
        :return: The updated
            DynaFlowTypeScheduleBusObj instance.
        """

        self.is_active = value
        return self
    # lastUTCDateTime

    def set_prop_last_utc_date_time(self, value: datetime):
        """
        Sets the value of the
        'last_utc_date_time' property.

        Args:
            value (datetime): The datetime value to set.

        Returns:
            self: The current instance of the class.
        """
        self.last_utc_date_time = value
        return self
    # nextUTCDateTime

    def set_prop_next_utc_date_time(self, value: datetime):
        """
        Sets the value of the
        'next_utc_date_time' property.

        Args:
            value (datetime): The datetime value to set.

        Returns:
            self: The current instance of the class.
        """
        self.next_utc_date_time = value
        return self
    # PacID
    # DynaFlowTypeID

    def set_prop_dyna_flow_type_id(self, value: int):
        """
        Sets the value of the
        'dyna_flow_type_id' property.

        Args:
            value (int): The value to set for the
                'dyna_flow_type_id' property.

        Returns:
            self: The current instance of the class.

        """
        self.dyna_flow_type_id = value
        return self

    # async def set_prop_dyna_flow_type_id_by_enum(
    #     self,
    #     dyna_flow_type_enum: managers_and_enums.DynaFlowTypeEnum
    # ):
    #     """
    #     """
    #     if not isinstance(
    #         dyna_flow_type_enum,
    #         managers_and_enums.DynaFlowTypeEnum
    #     ):
    #         raise ValueError("dyna_flow_type_enum must be a DynaFlowTypeEnum")

    #     dyna_flow_type_manager =  \
    #         managers_and_enums.DynaFlowTypeManager(
    #             self._session_context
    #         )
    #     dyna_flow_type_obj = await (
    #         dyna_flow_type_manager.
    #         from_enum(dyna_flow_type_enum)
    #     )

    #     self.dyna_flow_type_id = dyna_flow_type_obj.dyna_flow_type_id
    #     return self
    # frequencyInHours,
    # isActive,
    # lastUTCDateTime
    # nextUTCDateTime
    # PacID

    def set_prop_pac_id(self, value: int):
        """
        Set the pac ID for the
        dyna_flow_type_schedule.

        Args:
            value (int): The pac id value.

        Returns:
            DynaFlowTypeSchedule: The updated
                DynaFlowTypeSchedule object.
        """

        self.pac_id = value
        return self
