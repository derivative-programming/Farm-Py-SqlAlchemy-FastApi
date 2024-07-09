# business/df_maintenance_reports.py  # pylint: disable=duplicate-code # noqa: E501
# pylint: disable=unused-import
"""
This module contains the DFMaintenanceReportsBusObj class
which provides methods to generate various reports
related to DFMaintenance objects.
"""
import uuid
from datetime import date, datetime, timezone  # noqa: F401
from decimal import Decimal  # noqa: F401
from typing import List

import managers as managers_and_enums  # noqa: F401
import models
import reports as reports_managers  # noqa: F401
from helpers import SessionContext, TypeConversion  # noqa: F401
from models import DFMaintenance

from .df_maintenance_fluent import DFMaintenanceFluentBusObj


class DFMaintenanceReportsBusObj(DFMaintenanceFluentBusObj):
    """
    This class extends the DFMaintenanceFluentBusObj class
    and provides methods to generate various reports
    related to DFMaintenance objects.
    """
