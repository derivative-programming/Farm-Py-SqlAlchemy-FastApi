# business/dyna_flow_task_type_reports.py  # pylint: disable=duplicate-code # noqa: E501
# pylint: disable=unused-import
"""
This module contains the DynaFlowTaskTypeReportsBusObj class
which provides methods to generate various reports
related to DynaFlowTaskType objects.
"""
import uuid
from datetime import date, datetime, timezone  # noqa: F401
from decimal import Decimal  # noqa: F401
from typing import List

import managers as managers_and_enums  # noqa: F401
import models
import reports as reports_managers  # noqa: F401
from helpers import SessionContext, TypeConversion  # noqa: F401
from models import DynaFlowTaskType

from .dyna_flow_task_type_fluent import DynaFlowTaskTypeFluentBusObj


class DynaFlowTaskTypeReportsBusObj(DynaFlowTaskTypeFluentBusObj):
    """
    This class extends the DynaFlowTaskTypeFluentBusObj class
    and provides methods to generate various reports
    related to DynaFlowTaskType objects.
    """
