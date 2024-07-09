# business/error_log_reports.py  # pylint: disable=duplicate-code # noqa: E501
# pylint: disable=unused-import
"""
This module contains the ErrorLogReportsBusObj class
which provides methods to generate various reports
related to ErrorLog objects.
"""
import uuid
from datetime import date, datetime, timezone  # noqa: F401
from decimal import Decimal  # noqa: F401
from typing import List

import managers as managers_and_enums  # noqa: F401
import models
import reports as reports_managers  # noqa: F401
from helpers import SessionContext, TypeConversion  # noqa: F401
from models import ErrorLog

from .error_log_fluent import ErrorLogFluentBusObj


class ErrorLogReportsBusObj(ErrorLogFluentBusObj):
    """
    This class extends the ErrorLogFluentBusObj class
    and provides methods to generate various reports
    related to ErrorLog objects.
    """
