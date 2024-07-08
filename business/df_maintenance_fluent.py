# business/df_maintenance_fluent.py  # pylint: disable=duplicate-code
# pylint: disable=unused-import

"""
This module contains the
DFMaintenanceFluentBusObj class,
which adds fluent properties
to the business object for a
DFMaintenance.
"""

import uuid  # noqa: F401
from datetime import date, datetime, timezone  # noqa: F401
from decimal import Decimal  # noqa: F401

import managers as managers_and_enums

from .df_maintenance_base import DFMaintenanceBaseBusObj


class DFMaintenanceFluentBusObj(DFMaintenanceBaseBusObj):
    """
    This class add fluent properties to the
    Base DFMaintenance Business Object
    """

    # isPaused

    def set_prop_is_paused(self, value: bool):
        """
        Set the Is Paused flag for the
        DFMaintenance object.

        :param value: The Is Paused flag value.
        :return: The updated
            DFMaintenanceBusObj instance.
        """

        self.is_paused = value
        return self
    # isScheduledDFProcessRequestCompleted

    def set_prop_is_scheduled_df_process_request_completed(self, value: bool):
        """
        Set the Is Scheduled DF Process Request Completed flag for the
        DFMaintenance object.

        :param value: The Is Scheduled DF Process Request Completed flag value.
        :return: The updated
            DFMaintenanceBusObj instance.
        """

        self.is_scheduled_df_process_request_completed = value
        return self
    # isScheduledDFProcessRequestStarted

    def set_prop_is_scheduled_df_process_request_started(self, value: bool):
        """
        Set the Is Scheduled DF Process Request Started flag for the
        DFMaintenance object.

        :param value: The Is Scheduled DF Process Request Started flag value.
        :return: The updated
            DFMaintenanceBusObj instance.
        """

        self.is_scheduled_df_process_request_started = value
        return self
    # lastScheduledDFProcessRequestUTCDateTime

    def set_prop_last_scheduled_df_process_request_utc_date_time(self, value: datetime):
        """
        Sets the value of the
        'last_scheduled_df_process_request_utc_date_time' property.

        Args:
            value (datetime): The datetime value to set.

        Returns:
            self: The current instance of the class.
        """
        self.last_scheduled_df_process_request_utc_date_time = value
        return self
    # nextScheduledDFProcessRequestUTCDateTime

    def set_prop_next_scheduled_df_process_request_utc_date_time(self, value: datetime):
        """
        Sets the value of the
        'next_scheduled_df_process_request_utc_date_time' property.

        Args:
            value (datetime): The datetime value to set.

        Returns:
            self: The current instance of the class.
        """
        self.next_scheduled_df_process_request_utc_date_time = value
        return self
    # PacID
    # pausedByUsername

    def set_prop_paused_by_username(self, value: str):
        """
        Set the Paused By Username for the
        DFMaintenance object.

        :param value: The Paused By Username value.
        :return: The updated
            DFMaintenanceBusObj instance.
        """

        self.paused_by_username = value
        return self
    # pausedUTCDateTime

    def set_prop_paused_utc_date_time(self, value: datetime):
        """
        Sets the value of the
        'paused_utc_date_time' property.

        Args:
            value (datetime): The datetime value to set.

        Returns:
            self: The current instance of the class.
        """
        self.paused_utc_date_time = value
        return self
    # scheduledDFProcessRequestProcessorIdentifier

    def set_prop_scheduled_df_process_request_processor_identifier(self, value: str):
        """
        Set the Scheduled DF Process Request Processor Identifier for the
        DFMaintenance object.

        :param value: The Scheduled DF Process Request Processor Identifier value.
        :return: The updated
            DFMaintenanceBusObj instance.
        """

        self.scheduled_df_process_request_processor_identifier = value
        return self
    # isPaused
    # isScheduledDFProcessRequestCompleted
    # isScheduledDFProcessRequestStarted
    # lastScheduledDFProcessRequestUTCDateTime
    # nextScheduledDFProcessRequestUTCDateTime
    # PacID

    def set_prop_pac_id(self, value: int):
        """
        Set the pac ID for the
        df_maintenance.

        Args:
            value (int): The pac id value.

        Returns:
            DFMaintenance: The updated
                DFMaintenance object.
        """

        self.pac_id = value
        return self
    # pausedByUsername
    # pausedUTCDateTime
    # scheduledDFProcessRequestProcessorIdentifier
