# flows/base/log_severity.py

"""
    #TODO add comment
"""

from enum import Enum


class LogSeverity(Enum):
    """
    #TODO add comment
    """

    ERROR_OCCURRED = 0
    WARNING = 1
    INFORMATION_LOW_DETAIL = 2
    INFORMATION_MID_DETAIL = 3
    INFORMATION_HIGH_DETAIL = 4
