# business/tac_dyna_flows.py  # pylint: disable=duplicate-code
# pylint: disable=unused-import
"""
This module contains the business logic related to tac dynamic flows.
"""
import uuid  # noqa: F401
from datetime import date, datetime, timezone  # noqa: F401
from decimal import Decimal  # noqa: F401
from typing import List  # noqa: F401

import managers as managers_and_enums  # noqa: F401
from helpers import SessionContext, TypeConversion  # noqa: F401
from models import DynaFlow, Tac, pac  # noqa: F401

from .tac_reports import TacReportsBusObj


class TacDynaFlowsBusObj(TacReportsBusObj):
    """
    Represents the business object for tac dynamic flows.
    Inherits from TacReportsBusObj.
    """
