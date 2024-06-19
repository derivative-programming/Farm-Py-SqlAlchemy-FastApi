# flows/base/log_severity.py

"""
This module defines the LogSeverity enumeration class.

LogSeverity represents the severity levels for logging messages.
"""

from enum import Enum


class LogSeverity(Enum):
    """
    Enumeration class representing the severity levels for logging messages.

    The available severity levels are:
    - ERROR_OCCURRED: Represents an error that occurred.
    - WARNING: Represents a warning message.
    - INFORMATION_LOW_DETAIL: Represents an 
        information message with low detail.
    - INFORMATION_MID_DETAIL: Represents an
        information message with medium detail.
    - INFORMATION_HIGH_DETAIL: Represents an
        information message with high detail.
    """

    ERROR_OCCURRED = 0
    WARNING = 1
    INFORMATION_LOW_DETAIL = 2
    INFORMATION_MID_DETAIL = 3
    INFORMATION_HIGH_DETAIL = 4
