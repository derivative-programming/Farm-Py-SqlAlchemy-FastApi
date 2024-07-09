# business/customer_role_dyna_flows.py  # pylint: disable=duplicate-code # noqa: E501
# pylint: disable=unused-import
"""
This module contains the business logic related to customer_role dynamic flows.
"""
import uuid  # noqa: F401
from datetime import date, datetime, timezone  # noqa: F401
from decimal import Decimal  # noqa: F401
from typing import List  # noqa: F401

import managers as managers_and_enums  # noqa: F401
from helpers import SessionContext, TypeConversion  # noqa: F401
from models import DynaFlow, CustomerRole, pac  # noqa: F401

from .customer_role_reports import CustomerRoleReportsBusObj


class CustomerRoleDynaFlowsBusObj(CustomerRoleReportsBusObj):
    """
    Represents the business object for customer_role dynamic flows.
    Inherits from CustomerRoleReportsBusObj.
    """
