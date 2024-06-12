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
