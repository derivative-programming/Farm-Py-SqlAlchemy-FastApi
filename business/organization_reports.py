# business/organization_reports.py  # pylint: disable=duplicate-code
# pylint: disable=unused-import
"""
This module contains the OrganizationReportsBusObj class
which provides methods to generate various reports
related to Organization objects.
"""
import uuid
from datetime import date, datetime, timezone  # noqa: F401
from decimal import Decimal  # noqa: F401
from typing import List

import managers as managers_and_enums  # noqa: F401
import models
import reports as reports_managers  # noqa: F401
from helpers import SessionContext, TypeConversion  # noqa: F401
from models import Organization

from .organization_fluent import OrganizationFluentBusObj


class OrganizationReportsBusObj(OrganizationFluentBusObj):
    """
    This class extends the OrganizationFluentBusObj class
    and provides methods to generate various reports
    related to Organization objects.
    """
