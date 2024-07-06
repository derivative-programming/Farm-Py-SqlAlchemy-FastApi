# business/org_customer_reports.py  # pylint: disable=duplicate-code
# pylint: disable=unused-import
"""
This module contains the OrgCustomerReportsBusObj class
which provides methods to generate various reports
related to OrgCustomer objects.
"""
import uuid
from datetime import date, datetime, timezone  # noqa: F401
from decimal import Decimal  # noqa: F401
from typing import List

import managers as managers_and_enums  # noqa: F401
import models
import reports as reports_managers  # noqa: F401
from helpers import SessionContext, TypeConversion  # noqa: F401
from models import OrgCustomer

from .org_customer_fluent import OrgCustomerFluentBusObj


class OrgCustomerReportsBusObj(OrgCustomerFluentBusObj):
    """
    This class extends the OrgCustomerFluentBusObj class
    and provides methods to generate various reports
    related to OrgCustomer objects.
    """
