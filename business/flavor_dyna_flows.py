# business/flavor_dyna_flows.py  # pylint: disable=duplicate-code # noqa: E501
# pylint: disable=unused-import
"""
This module contains the business logic related to flavor dynamic flows.
"""
import uuid  # noqa: F401
from datetime import date, datetime, timezone  # noqa: F401
from decimal import Decimal  # noqa: F401
from typing import List  # noqa: F401

import managers as managers_and_enums  # noqa: F401
from helpers import SessionContext, TypeConversion  # noqa: F401
from models import DynaFlow, Flavor, pac  # noqa: F401

from .flavor_reports import FlavorReportsBusObj


class FlavorDynaFlowsBusObj(FlavorReportsBusObj):
    """
    Represents the business object for flavor dynamic flows.
    Inherits from FlavorReportsBusObj.
    """
