# business/flavor_reports.py  # pylint: disable=duplicate-code
# pylint: disable=unused-import
"""
This module contains the FlavorReportsBusObj class
which provides methods to generate various reports
related to Flavor objects.
"""
import uuid
from datetime import date, datetime, timezone  # noqa: F401
from decimal import Decimal  # noqa: F401
from typing import List

import managers as managers_and_enums  # noqa: F401
import models
import reports as reports_managers  # noqa: F401
from helpers import SessionContext, TypeConversion  # noqa: F401
from models import Flavor

from .flavor_fluent import FlavorFluentBusObj


class FlavorReportsBusObj(FlavorFluentBusObj):
    """
    This class extends the FlavorFluentBusObj class
    and provides methods to generate various reports
    related to Flavor objects.
    """
