# flows/base/log_severity.py

"""
    #TODO add comment
"""

from enum import Enum


class LogSeverity(Enum):
    """
    #TODO add comment
    """
    error_occurred = 0
    warning = 1
    information_low_detail = 2
    information_mid_detail = 3
    information_high_detail = 4

    # ERROR_OCCURRED = 0
    # WARNING = 1
    # INFORMATION_LOW_DETAIL = 2
    # INFORMATION_MID_DETAIL = 3
    # INFORMATION_HIGH_DETAIL = 4
