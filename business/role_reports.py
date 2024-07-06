# business/role_reports.py  # pylint: disable=duplicate-code
# pylint: disable=unused-import
"""
This module contains the RoleReportsBusObj class
which provides methods to generate various reports
related to Role objects.
"""
import uuid
from datetime import date, datetime, timezone  # noqa: F401
from decimal import Decimal  # noqa: F401
from typing import List

import managers as managers_and_enums  # noqa: F401
import models
import reports as reports_managers  # noqa: F401
from helpers import SessionContext, TypeConversion  # noqa: F401
from models import Role

from .role_fluent import RoleFluentBusObj


class RoleReportsBusObj(RoleFluentBusObj):
    """
    This class extends the RoleFluentBusObj class
    and provides methods to generate various reports
    related to Role objects.
    """
