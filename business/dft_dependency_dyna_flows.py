# business/dft_dependency_dyna_flows.py  # pylint: disable=duplicate-code
# pylint: disable=unused-import
"""
This module contains the business logic related to dft_dependency dynamic flows.
"""
import uuid  # noqa: F401
from datetime import date, datetime, timezone  # noqa: F401
from decimal import Decimal  # noqa: F401
from typing import List  # noqa: F401

import managers as managers_and_enums  # noqa: F401
from helpers import SessionContext, TypeConversion  # noqa: F401
from models import DynaFlow, DFTDependency, pac  # noqa: F401

from .dft_dependency_reports import DFTDependencyReportsBusObj


class DFTDependencyDynaFlowsBusObj(DFTDependencyReportsBusObj):
    """
    Represents the business object for dft_dependency dynamic flows.
    Inherits from DFTDependencyReportsBusObj.
    """
