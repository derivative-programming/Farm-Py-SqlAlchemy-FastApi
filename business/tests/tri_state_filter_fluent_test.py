# business/tests/tri_state_filter_fluent_test.py
"""
Unit tests for the TriStateFilterFluentBusObj class.
"""
import math
from datetime import date, datetime
from decimal import Decimal
from uuid import uuid4
import pytest
from business.tri_state_filter_fluent import TriStateFilterFluentBusObj
from helpers.session_context import SessionContext
class MockTriStateFilterBaseBusObj:
    """
    A mock base class for the TriStateFilterFluentBusObj class.
    """
    def __init__(self):
        self.description = None
        self.display_order = None
        self.is_active = None
        self.lookup_enum_name = None
        self.name = None
        self.pac_id = None
        self.state_int_value = None
class TestTriStateFilterFluentBusObj:
    """
    Unit tests for the TriStateFilterFluentBusObj class.
    """
    @pytest.fixture
    def tri_state_filter(self, session):
        """
        Return a TriStateFilterFluentBusObj object.
        """
        session_context = SessionContext(dict(), session=session)
        return TriStateFilterFluentBusObj(session_context)
    def test_set_prop_description(self, tri_state_filter):
        """
        Test setting the description property.
        """
        result = tri_state_filter.set_prop_description("Vanilla")
        assert tri_state_filter.description == "Vanilla"
        assert result is tri_state_filter
    def test_set_prop_display_order(self, tri_state_filter):
        """
        Test setting the display_order property.
        """
        result = tri_state_filter.set_prop_display_order(42)
        assert tri_state_filter.display_order == 42
        assert result is tri_state_filter
    def test_set_prop_is_active(self, tri_state_filter):
        """
        Test setting the is_active property.
        """
        result = tri_state_filter.set_prop_is_active(True)
        assert tri_state_filter.is_active is True
        assert result is tri_state_filter
    def test_set_prop_lookup_enum_name(self, tri_state_filter):
        """
        Test setting the lookup_enum_name property.
        """
        result = tri_state_filter.set_prop_lookup_enum_name("Vanilla")
        assert tri_state_filter.lookup_enum_name == "Vanilla"
        assert result is tri_state_filter
    def test_set_prop_name(self, tri_state_filter):
        """
        Test setting the name property.
        """
        result = tri_state_filter.set_prop_name("Vanilla")
        assert tri_state_filter.name == "Vanilla"
        assert result is tri_state_filter
    def test_set_prop_pac_id(self, tri_state_filter):
        """
        Test setting the pac_id property.
        """
        result = tri_state_filter.set_prop_pac_id(1)
        assert tri_state_filter.pac_id == 1
        assert result is tri_state_filter
    def test_set_prop_state_int_value(self, tri_state_filter):
        """
        Test setting the state_int_value property.
        """
        result = tri_state_filter.set_prop_state_int_value(42)
        assert tri_state_filter.state_int_value == 42
        assert result is tri_state_filter
