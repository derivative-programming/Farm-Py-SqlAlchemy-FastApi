# business/land_dyna_flows.py  # pylint: disable=duplicate-code # noqa: E501
# pylint: disable=unused-import
"""
This module contains the business logic related to land dynamic flows.
"""
import uuid  # noqa: F401
from datetime import date, datetime, timezone  # noqa: F401
from decimal import Decimal  # noqa: F401
from typing import List  # noqa: F401

import managers as managers_and_enums  # noqa: F401
from helpers import SessionContext, TypeConversion  # noqa: F401
from models import DynaFlow, Land, pac  # noqa: F401

from .land_reports import LandReportsBusObj


class LandDynaFlowsBusObj(LandReportsBusObj):
    """
    Represents the business object for land dynamic flows.
    Inherits from LandReportsBusObj.
    """
