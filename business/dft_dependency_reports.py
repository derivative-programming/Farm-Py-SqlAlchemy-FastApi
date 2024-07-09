# business/dft_dependency_reports.py  # pylint: disable=duplicate-code # noqa: E501
# pylint: disable=unused-import
"""
This module contains the DFTDependencyReportsBusObj class
which provides methods to generate various reports
related to DFTDependency objects.
"""
import uuid
from datetime import date, datetime, timezone  # noqa: F401
from decimal import Decimal  # noqa: F401
from typing import List

import managers as managers_and_enums  # noqa: F401
import models
import reports as reports_managers  # noqa: F401
from helpers import SessionContext, TypeConversion  # noqa: F401
from models import DFTDependency

from .dft_dependency_fluent import DFTDependencyFluentBusObj


class DFTDependencyReportsBusObj(DFTDependencyFluentBusObj):
    """
    This class extends the DFTDependencyFluentBusObj class
    and provides methods to generate various reports
    related to DFTDependency objects.
    """
