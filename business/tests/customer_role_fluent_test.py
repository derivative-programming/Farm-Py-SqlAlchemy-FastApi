# business/tests/customer_role_fluent_test.py  # pylint: disable=duplicate-code # noqa: E501
# pylint: disable=unused-import, too-many-public-methods
# pylint: disable=too-few-public-methods
"""
Unit tests for the
CustomerRoleFluentBusObj class.
"""
import math  # noqa: F401
from datetime import date, datetime, timezone  # noqa: F401
from decimal import Decimal  # noqa: F401
from uuid import uuid4  # noqa: F401

import pytest
from business.customer_role_fluent import \
    CustomerRoleFluentBusObj
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
    def new_fluent_bus_obj(self, session):
        """
        Return a CustomerRoleFluentBusObj
        object.
        """
        session_context = SessionContext({}, session=session)
        return CustomerRoleFluentBusObj(
            session_context)
    # CustomerID
    # isPlaceholder

    def test_set_prop_is_placeholder(self, new_fluent_bus_obj):
        """
        Test setting the is_placeholder property.
        """
        result = new_fluent_bus_obj.set_prop_is_placeholder(True)
        assert new_fluent_bus_obj.is_placeholder is True
        assert result is new_fluent_bus_obj
    # placeholder

    def test_set_prop_placeholder(self, new_fluent_bus_obj):
        """
        Test setting the placeholder property.
        """
        result = new_fluent_bus_obj.set_prop_placeholder(True)
        assert new_fluent_bus_obj.placeholder is True
        assert result is new_fluent_bus_obj
    # RoleID
    # CustomerID

    def test_set_prop_customer_id(self, new_fluent_bus_obj):
        """
        Test setting the customer_id property.
        """
        result = new_fluent_bus_obj.set_prop_customer_id(1)
        assert new_fluent_bus_obj.customer_id == 1
        assert result is new_fluent_bus_obj
    # isPlaceholder
    # placeholder
    # RoleID

    def test_set_prop_role_id(self, new_fluent_bus_obj):
        """
        Test setting the role_id property.
        """
        result = new_fluent_bus_obj.set_prop_role_id(1)
        assert new_fluent_bus_obj.role_id == 1
        assert result is new_fluent_bus_obj
