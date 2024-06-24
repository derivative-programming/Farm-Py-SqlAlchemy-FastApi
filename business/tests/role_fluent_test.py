# business/tests/role_fluent_test.py
"""
Unit tests for the RoleFluentBusObj class.
"""
import math
from datetime import date, datetime
from decimal import Decimal
from uuid import uuid4
import pytest
from business.role_fluent import RoleFluentBusObj
from helpers.session_context import SessionContext
class MockRoleBaseBusObj:
    """
    A mock base class for the RoleFluentBusObj class.
    """
    def __init__(self):
        self.description = None
        self.display_order = None
        self.is_active = None
        self.lookup_enum_name = None
        self.name = None
        self.pac_id = None
class TestRoleFluentBusObj:
    """
    Unit tests for the RoleFluentBusObj class.
    """
    @pytest.fixture
    def role(self, session):
        """
        Return a RoleFluentBusObj object.
        """
        session_context = SessionContext(dict(), session=session)
        return RoleFluentBusObj(session_context)
    def test_set_prop_description(self, role):
        """
        Test setting the description property.
        """
        result = role.set_prop_description("Vanilla")
        assert role.description == "Vanilla"
        assert result is role
    def test_set_prop_display_order(self, role):
        """
        Test setting the display_order property.
        """
        result = role.set_prop_display_order(42)
        assert role.display_order == 42
        assert result is role
    def test_set_prop_is_active(self, role):
        """
        Test setting the is_active property.
        """
        result = role.set_prop_is_active(True)
        assert role.is_active is True
        assert result is role
    def test_set_prop_lookup_enum_name(self, role):
        """
        Test setting the lookup_enum_name property.
        """
        result = role.set_prop_lookup_enum_name("Vanilla")
        assert role.lookup_enum_name == "Vanilla"
        assert result is role
    def test_set_prop_name(self, role):
        """
        Test setting the name property.
        """
        result = role.set_prop_name("Vanilla")
        assert role.name == "Vanilla"
        assert result is role
    def test_set_prop_pac_id(self, role):
        """
        Test setting the pac_id property.
        """
        result = role.set_prop_pac_id(1)
        assert role.pac_id == 1
        assert result is role
