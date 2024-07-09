# business/dyna_flow_type_reports.py  # pylint: disable=duplicate-code # noqa: E501
# pylint: disable=unused-import
"""
This module contains the DynaFlowTypeReportsBusObj class
which provides methods to generate various reports
related to DynaFlowType objects.
"""
import uuid
from datetime import date, datetime, timezone  # noqa: F401
from decimal import Decimal  # noqa: F401
from typing import List

import managers as managers_and_enums  # noqa: F401
import models
import reports as reports_managers  # noqa: F401
from helpers import SessionContext, TypeConversion  # noqa: F401
from models import DynaFlowType

from .dyna_flow_type_fluent import DynaFlowTypeFluentBusObj


class DynaFlowTypeReportsBusObj(DynaFlowTypeFluentBusObj):
    """
    This class extends the DynaFlowTypeFluentBusObj class
    and provides methods to generate various reports
    related to DynaFlowType objects.
    """
