# business/tri_state_filter_reports.py  # pylint: disable=duplicate-code
# pylint: disable=unused-import
"""
This module contains the TriStateFilterReportsBusObj class
which provides methods to generate various reports
related to TriStateFilter objects.
"""
import uuid
from datetime import date, datetime, timezone  # noqa: F401
from decimal import Decimal  # noqa: F401
from typing import List

import managers as managers_and_enums  # noqa: F401
import models
import reports as reports_managers  # noqa: F401
from helpers import SessionContext, TypeConversion  # noqa: F401
from models import TriStateFilter

from .tri_state_filter_fluent import TriStateFilterFluentBusObj


class TriStateFilterReportsBusObj(TriStateFilterFluentBusObj):
    """
    This class extends the TriStateFilterFluentBusObj class
    and provides methods to generate various reports
    related to TriStateFilter objects.
    """
