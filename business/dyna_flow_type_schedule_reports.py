# business/dyna_flow_type_schedule_reports.py  # pylint: disable=duplicate-code
# pylint: disable=unused-import
"""
This module contains the DynaFlowTypeScheduleReportsBusObj class
which provides methods to generate various reports
related to DynaFlowTypeSchedule objects.
"""
import uuid
from datetime import date, datetime, timezone  # noqa: F401
from decimal import Decimal  # noqa: F401
from typing import List

import managers as managers_and_enums  # noqa: F401
import models
import reports as reports_managers  # noqa: F401
from helpers import SessionContext, TypeConversion  # noqa: F401
from models import DynaFlowTypeSchedule

from .dyna_flow_type_schedule_fluent import DynaFlowTypeScheduleFluentBusObj


class DynaFlowTypeScheduleReportsBusObj(DynaFlowTypeScheduleFluentBusObj):
    """
    This class extends the DynaFlowTypeScheduleFluentBusObj class
    and provides methods to generate various reports
    related to DynaFlowTypeSchedule objects.
    """
