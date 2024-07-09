# business/error_log_fluent.py  # pylint: disable=duplicate-code # noqa: E501
# pylint: disable=unused-import

"""
This module contains the
ErrorLogFluentBusObj class,
which adds fluent properties
to the business object for a
ErrorLog.
"""

import uuid  # noqa: F401
from datetime import date, datetime, timezone  # noqa: F401
from decimal import Decimal  # noqa: F401

import managers as managers_and_enums

from .error_log_base import ErrorLogBaseBusObj


class ErrorLogFluentBusObj(ErrorLogBaseBusObj):
    """
    This class add fluent properties to the
    Base ErrorLog Business Object
    """

    # browserCode

    def set_prop_browser_code(self, value: uuid.UUID):
        """
        Set the value of the
        'browser_code' property.

        Args:
            value (uuid.UUID): The value to set.

        Returns:
            self: The current instance of the class.
        """
        self.browser_code = value
        return self
    # contextCode

    def set_prop_context_code(self, value: uuid.UUID):
        """
        Set the value of the
        'context_code' property.

        Args:
            value (uuid.UUID): The value to set.

        Returns:
            self: The current instance of the class.
        """
        self.context_code = value
        return self
    # createdUTCDateTime

    def set_prop_created_utc_date_time(self, value: datetime):
        """
        Sets the value of the
        'created_utc_date_time' property.

        Args:
            value (datetime): The datetime value to set.

        Returns:
            self: The current instance of the class.
        """
        self.created_utc_date_time = value
        return self
    # description

    def set_prop_description(self, value: str):
        """
        Set the Description for the
        ErrorLog object.

        :param value: The Description value.
        :return: The updated
            ErrorLogBusObj instance.
        """

        self.description = value
        return self
    # isClientSideError

    def set_prop_is_client_side_error(self, value: bool):
        """
        Set the Is Client Side Error flag for the
        ErrorLog object.

        :param value: The Is Client Side Error flag value.
        :return: The updated
            ErrorLogBusObj instance.
        """

        self.is_client_side_error = value
        return self
    # isResolved

    def set_prop_is_resolved(self, value: bool):
        """
        Set the Is Resolved flag for the
        ErrorLog object.

        :param value: The Is Resolved flag value.
        :return: The updated
            ErrorLogBusObj instance.
        """

        self.is_resolved = value
        return self
    # PacID
    # url

    def set_prop_url(self, value: str):
        """
        Set the Url for the
        ErrorLog object.

        :param value: The Url value.
        :return: The updated
            ErrorLogBusObj instance.
        """

        self.url = value
        return self
    # browserCode
    # contextCode
    # createdUTCDateTime
    # description
    # isClientSideError
    # isResolved
    # PacID

    def set_prop_pac_id(self, value: int):
        """
        Set the pac ID for the
        error_log.

        Args:
            value (int): The pac id value.

        Returns:
            ErrorLog: The updated
                ErrorLog object.
        """

        self.pac_id = value
        return self
    # url
