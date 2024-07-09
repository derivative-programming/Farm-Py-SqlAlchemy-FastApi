# business/org_customer_dyna_flows.py  # pylint: disable=duplicate-code # noqa: E501
# pylint: disable=unused-import
"""
This module contains the business logic related to org_customer dynamic flows.
"""
import uuid  # noqa: F401
from datetime import date, datetime, timezone  # noqa: F401
from decimal import Decimal  # noqa: F401
from typing import List  # noqa: F401

import managers as managers_and_enums  # noqa: F401
from helpers import SessionContext, TypeConversion  # noqa: F401
from models import DynaFlow, OrgCustomer, pac  # noqa: F401

from .org_customer_reports import OrgCustomerReportsBusObj


class OrgCustomerDynaFlowsBusObj(OrgCustomerReportsBusObj):
    """
    Represents the business object for org_customer dynamic flows.
    Inherits from OrgCustomerReportsBusObj.
    """
