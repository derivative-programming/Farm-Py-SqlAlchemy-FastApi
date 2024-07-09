# business/dyna_flow_type_schedule_dyna_flows.py  # pylint: disable=duplicate-code # noqa: E501
# pylint: disable=unused-import
"""
This module contains the business logic related to dyna_flow_type_schedule dynamic flows.
"""
import uuid  # noqa: F401
from datetime import date, datetime, timezone  # noqa: F401
from decimal import Decimal  # noqa: F401
from typing import List  # noqa: F401

import managers as managers_and_enums  # noqa: F401
from helpers import SessionContext, TypeConversion  # noqa: F401
from models import DynaFlow, DynaFlowTypeSchedule, pac  # noqa: F401

from .dyna_flow_type_schedule_reports import DynaFlowTypeScheduleReportsBusObj


class DynaFlowTypeScheduleDynaFlowsBusObj(DynaFlowTypeScheduleReportsBusObj):
    """
    Represents the business object for dyna_flow_type_schedule dynamic flows.
    Inherits from DynaFlowTypeScheduleReportsBusObj.
    """
