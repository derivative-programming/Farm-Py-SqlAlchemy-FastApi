# business/customer_role.py
# pylint: disable=unused-import
"""
"""
import uuid
from decimal import Decimal  # noqa: F401
from datetime import date, datetime, timezone  # noqa: F401
from typing import List
from helpers import SessionContext, TypeConversion  # noqa: F401
from models import CustomerRole
import models
import managers as managers_and_enums  # noqa: F401
from .customer_role_fluent import CustomerRoleFluentBusObj
import reports as reports_managers  # noqa: F401


class CustomerRoleReportsBusObj(CustomerRoleFluentBusObj):
    """
    """
