# business/customer_role_reports.py  # pylint: disable=duplicate-code # noqa: E501
# pylint: disable=unused-import
"""
This module contains the CustomerRoleReportsBusObj class
which provides methods to generate various reports
related to CustomerRole objects.
"""
import uuid
from datetime import date, datetime, timezone  # noqa: F401
from decimal import Decimal  # noqa: F401
from typing import List

import managers as managers_and_enums  # noqa: F401
import models
import reports as reports_managers  # noqa: F401
from helpers import SessionContext, TypeConversion  # noqa: F401
from models import CustomerRole

from .customer_role_fluent import CustomerRoleFluentBusObj


class CustomerRoleReportsBusObj(CustomerRoleFluentBusObj):
    """
    This class extends the CustomerRoleFluentBusObj class
    and provides methods to generate various reports
    related to CustomerRole objects.
    """
