# business/plant_reports.py  # pylint: disable=duplicate-code
# pylint: disable=unused-import
"""
This module contains the PlantReportsBusObj class
which provides methods to generate various reports
related to Plant objects.
"""
import uuid
from datetime import date, datetime, timezone  # noqa: F401
from decimal import Decimal  # noqa: F401
from typing import List

import managers as managers_and_enums  # noqa: F401
import models
import reports as reports_managers  # noqa: F401
from helpers import SessionContext, TypeConversion  # noqa: F401
from models import Plant

from .plant_fluent import PlantFluentBusObj


class PlantReportsBusObj(PlantFluentBusObj):
    """
    This class extends the PlantFluentBusObj class
    and provides methods to generate various reports
    related to Plant objects.
    """

    ##GENINCLUDEFILE[GENVALName.report.include.*]
