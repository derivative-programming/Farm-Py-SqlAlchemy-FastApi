# business/customer_dyna_flows.py  # pylint: disable=duplicate-code
# pylint: disable=unused-import
"""
This module contains the business logic related to customer dynamic flows.
"""
import uuid  # noqa: F401
from datetime import date, datetime, timezone  # noqa: F401
from decimal import Decimal  # noqa: F401
from typing import List  # noqa: F401

import managers as managers_and_enums  # noqa: F401
from helpers import SessionContext, TypeConversion  # noqa: F401
from models import DynaFlow, Customer, pac  # noqa: F401

from .customer_reports import CustomerReportsBusObj


class CustomerDynaFlowsBusObj(CustomerReportsBusObj):
    """
    Represents the business object for customer dynamic flows.
    Inherits from CustomerReportsBusObj.
    """
