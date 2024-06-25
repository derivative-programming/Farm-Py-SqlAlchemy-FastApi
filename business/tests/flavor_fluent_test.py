# business/tests/flavor_fluent_test.py
"""
Unit tests for the FlavorFluentBusObj class.
"""
import math
from datetime import date, datetime
from decimal import Decimal
from uuid import uuid4

import pytest

from business.flavor_fluent import FlavorFluentBusObj
from helpers.session_context import SessionContext


class MockFlavorBaseBusObj:
    """
    A mock base class for the FlavorFluentBusObj class.
    """
    def __init__(self):
        self.description = None
        self.display_order = None
        self.is_active = None
        self.lookup_enum_name = None
        self.name = None
        self.pac_id = None
class TestFlavorFluentBusObj:
    """
    Unit tests for the FlavorFluentBusObj class.
    """
    @pytest.fixture
    def flavor(self, session):
        """
        Return a FlavorFluentBusObj object.
        """
        session_context = SessionContext(dict(), session=session)
        return FlavorFluentBusObj(session_context)
    def test_set_prop_description(self, flavor):
        """
        Test setting the description property.
        """
        result = flavor.set_prop_description("Vanilla")
        assert flavor.description == "Vanilla"
        assert result is flavor
    def test_set_prop_display_order(self, flavor):
        """
        Test setting the display_order property.
        """
        result = flavor.set_prop_display_order(42)
        assert flavor.display_order == 42
        assert result is flavor
    def test_set_prop_is_active(self, flavor):
        """
        Test setting the is_active property.
        """
        result = flavor.set_prop_is_active(True)
        assert flavor.is_active is True
        assert result is flavor
    def test_set_prop_lookup_enum_name(self, flavor):
        """
        Test setting the lookup_enum_name property.
        """
        result = flavor.set_prop_lookup_enum_name("Vanilla")
        assert flavor.lookup_enum_name == "Vanilla"
        assert result is flavor
    def test_set_prop_name(self, flavor):
        """
        Test setting the name property.
        """
        result = flavor.set_prop_name("Vanilla")
        assert flavor.name == "Vanilla"
        assert result is flavor
    def test_set_prop_pac_id(self, flavor):
        """
        Test setting the pac_id property.
        """
        result = flavor.set_prop_pac_id(1)
        assert flavor.pac_id == 1
        assert result is flavor

