# business/df_maintenance_dyna_flows.py  # pylint: disable=duplicate-code # noqa: E501
# pylint: disable=unused-import
"""
This module contains the business logic related to df_maintenance dynamic flows.
"""
import uuid  # noqa: F401
from datetime import date, datetime, timezone  # noqa: F401
from decimal import Decimal  # noqa: F401
from typing import List  # noqa: F401

import managers as managers_and_enums  # noqa: F401
from helpers import SessionContext, TypeConversion  # noqa: F401
from models import DynaFlow, DFMaintenance, pac  # noqa: F401

from .df_maintenance_reports import DFMaintenanceReportsBusObj


class DFMaintenanceDynaFlowsBusObj(DFMaintenanceReportsBusObj):
    """
    Represents the business object for df_maintenance dynamic flows.
    Inherits from DFMaintenanceReportsBusObj.
    """
