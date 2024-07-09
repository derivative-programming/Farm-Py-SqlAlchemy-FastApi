# business/error_log_dyna_flows.py  # pylint: disable=duplicate-code # noqa: E501
# pylint: disable=unused-import
"""
This module contains the business logic related to error_log dynamic flows.
"""
import uuid  # noqa: F401
from datetime import date, datetime, timezone  # noqa: F401
from decimal import Decimal  # noqa: F401
from typing import List  # noqa: F401

import managers as managers_and_enums  # noqa: F401
from helpers import SessionContext, TypeConversion  # noqa: F401
from models import DynaFlow, ErrorLog, pac  # noqa: F401

from .error_log_reports import ErrorLogReportsBusObj


class ErrorLogDynaFlowsBusObj(ErrorLogReportsBusObj):
    """
    Represents the business object for error_log dynamic flows.
    Inherits from ErrorLogReportsBusObj.
    """
