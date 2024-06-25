# business/tests/org_customer_fluent_test.py
# pylint: disable=unused-import
"""
Unit tests for the
OrgCustomerFluentBusObj class.
"""
import math
from datetime import date, datetime  # noqa: F401
from decimal import Decimal  # noqa: F401
from uuid import uuid4  # noqa: F401

import pytest

from business.org_customer_fluent import (
    OrgCustomerFluentBusObj)
from helpers.session_context import SessionContext


class MockOrgCustomerBaseBusObj:
    """
    A mock base class for the
    OrgCustomerFluentBusObj class.
    """
    def __init__(self):
        self.customer_id = None
        self.email = None
        self.organization_id = None
class TestOrgCustomerFluentBusObj:
    """
    Unit tests for the
    OrgCustomerFluentBusObj class.
    """
    @pytest.fixture
    def org_customer(self, session):
        """
        Return a OrgCustomerFluentBusObj
        object.
        """
        session_context = SessionContext(dict(), session=session)
        return OrgCustomerFluentBusObj(session_context)
    def test_set_prop_customer_id(self, org_customer):
        """
        Test setting the customer_id property.
        """
        result = org_customer.set_prop_customer_id(1)
        assert org_customer.customer_id == 1
        assert result is org_customer
    def test_set_prop_email(self, org_customer):
        """
        Test setting the email property.
        """
        result = org_customer.set_prop_email("test@example.com")
        assert org_customer.email == "test@example.com"
        assert result is org_customer
    def test_set_prop_organization_id(self, org_customer):
        """
        Test setting the organization_id property.
        """
        result = org_customer.set_prop_organization_id(1)
        assert org_customer.organization_id == 1
        assert result is org_customer

