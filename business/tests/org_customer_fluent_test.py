# business/tests/org_customer_fluent_test.py
# pylint: disable=unused-import
"""
Unit tests for the
OrgCustomerFluentBusObj class.
"""
import math  # noqa: F401
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
    def new_fluent_bus_obj(self, session):
        """
        Return a OrgCustomerFluentBusObj
        object.
        """
        session_context = SessionContext(dict(), session=session)
        return OrgCustomerFluentBusObj(session_context)
    # CustomerID
    # email

    def test_set_prop_email(self, new_fluent_bus_obj):
        """
        Test setting the email property.
        """
        result = new_fluent_bus_obj.set_prop_email(
            "test@example.com")
        assert new_fluent_bus_obj.email == \
            "test@example.com"
        assert result is new_fluent_bus_obj
    # OrganizationID
    # CustomerID

    def test_set_prop_customer_id(self, new_fluent_bus_obj):
        """
        Test setting the customer_id property.
        """
        result = new_fluent_bus_obj.set_prop_customer_id(1)
        assert new_fluent_bus_obj.customer_id == 1
        assert result is new_fluent_bus_obj
    # email,
    # OrganizationID

    def test_set_prop_organization_id(self, new_fluent_bus_obj):
        """
        Test setting the organization_id property.
        """
        result = new_fluent_bus_obj.set_prop_organization_id(1)
        assert new_fluent_bus_obj.organization_id == 1
        assert result is new_fluent_bus_obj
