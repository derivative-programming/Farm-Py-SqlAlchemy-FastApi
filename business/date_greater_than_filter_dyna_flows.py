# business/date_greater_than_filter_dyna_flows.py  # pylint: disable=duplicate-code # noqa: E501
# pylint: disable=unused-import
"""
This module contains the business logic related to date_greater_than_filter dynamic flows.
"""
import uuid  # noqa: F401
from datetime import date, datetime, timezone  # noqa: F401
from decimal import Decimal  # noqa: F401
from typing import List  # noqa: F401

import managers as managers_and_enums  # noqa: F401
from helpers import SessionContext, TypeConversion  # noqa: F401
from models import DynaFlow, DateGreaterThanFilter, pac  # noqa: F401

from .date_greater_than_filter_reports import DateGreaterThanFilterReportsBusObj


class DateGreaterThanFilterDynaFlowsBusObj(DateGreaterThanFilterReportsBusObj):
    """
    Represents the business object for date_greater_than_filter dynamic flows.
    Inherits from DateGreaterThanFilterReportsBusObj.
    """
