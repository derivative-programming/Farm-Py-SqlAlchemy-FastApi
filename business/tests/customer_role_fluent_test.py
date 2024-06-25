# business/tests/customer_role_fluent_test.py
# pylint: disable=unused-import
"""
Unit tests for the
CustomerRoleFluentBusObj class.
"""
import math
from datetime import date, datetime  # noqa: F401
from decimal import Decimal  # noqa: F401
from uuid import uuid4  # noqa: F401

import pytest

from business.customer_role_fluent import (
    CustomerRoleFluentBusObj)
from helpers.session_context import SessionContext


class MockCustomerRoleBaseBusObj:
    """
    A mock base class for the
    CustomerRoleFluentBusObj class.
    """
    def __init__(self):
        self.customer_id = None
        self.is_placeholder = None
        self.placeholder = None
        self.role_id = None
class TestCustomerRoleFluentBusObj:
    """
    Unit tests for the
    CustomerRoleFluentBusObj class.
    """
    @pytest.fixture
    def customer_role(self, session):
        """
        Return a CustomerRoleFluentBusObj
        object.
        """
        session_context = SessionContext(dict(), session=session)
        return CustomerRoleFluentBusObj(session_context)
    def test_set_prop_customer_id(self, customer_role):
        """
        Test setting the customer_id property.
        """
        result = customer_role.set_prop_customer_id(1)
        assert customer_role.customer_id == 1
        assert result is customer_role
    def test_set_prop_is_placeholder(self, customer_role):
        """
        Test setting the is_placeholder property.
        """
        result = customer_role.set_prop_is_placeholder(True)
        assert customer_role.is_placeholder is True
        assert result is customer_role
    def test_set_prop_placeholder(self, customer_role):
        """
        Test setting the placeholder property.
        """
        result = customer_role.set_prop_placeholder(True)
        assert customer_role.placeholder is True
        assert result is customer_role
    def test_set_prop_role_id(self, customer_role):
        """
        Test setting the role_id property.
        """
        result = customer_role.set_prop_role_id(1)
        assert customer_role.role_id == 1
        assert result is customer_role

