# business/tri_state_filter_dyna_flows.py  # pylint: disable=duplicate-code # noqa: E501
# pylint: disable=unused-import
"""
This module contains the business logic related to tri_state_filter dynamic flows.
"""
import uuid  # noqa: F401
from datetime import date, datetime, timezone  # noqa: F401
from decimal import Decimal  # noqa: F401
from typing import List  # noqa: F401

import managers as managers_and_enums  # noqa: F401
from helpers import SessionContext, TypeConversion  # noqa: F401
from models import DynaFlow, TriStateFilter, pac  # noqa: F401

from .tri_state_filter_reports import TriStateFilterReportsBusObj


class TriStateFilterDynaFlowsBusObj(TriStateFilterReportsBusObj):
    """
    Represents the business object for tri_state_filter dynamic flows.
    Inherits from TriStateFilterReportsBusObj.
    """
