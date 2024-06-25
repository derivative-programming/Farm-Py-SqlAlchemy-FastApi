# business/tests/land_fluent_test.py
# pylint: disable=unused-import
"""
Unit tests for the
LandFluentBusObj class.
"""
import math
from datetime import date, datetime  # noqa: F401
from decimal import Decimal  # noqa: F401
from uuid import uuid4  # noqa: F401

import pytest

from business.land_fluent import (
    LandFluentBusObj)
from helpers.session_context import SessionContext


class MockLandBaseBusObj:
    """
    A mock base class for the
    LandFluentBusObj class.
    """
    def __init__(self):
        self.description = None
        self.display_order = None
        self.is_active = None
        self.lookup_enum_name = None
        self.name = None
        self.pac_id = None
class TestLandFluentBusObj:
    """
    Unit tests for the
    LandFluentBusObj class.
    """
    @pytest.fixture
    def land(self, session):
        """
        Return a LandFluentBusObj
        object.
        """
        session_context = SessionContext(dict(), session=session)
        return LandFluentBusObj(session_context)
    def test_set_prop_description(self, land):
        """
        Test setting the description property.
        """
        result = land.set_prop_description("Vanilla")
        assert land.description == "Vanilla"
        assert result is land
    def test_set_prop_display_order(self, land):
        """
        Test setting the display_order property.
        """
        result = land.set_prop_display_order(42)
        assert land.display_order == 42
        assert result is land
    def test_set_prop_is_active(self, land):
        """
        Test setting the is_active property.
        """
        result = land.set_prop_is_active(True)
        assert land.is_active is True
        assert result is land
    def test_set_prop_lookup_enum_name(self, land):
        """
        Test setting the lookup_enum_name property.
        """
        result = land.set_prop_lookup_enum_name("Vanilla")
        assert land.lookup_enum_name == "Vanilla"
        assert result is land
    def test_set_prop_name(self, land):
        """
        Test setting the name property.
        """
        result = land.set_prop_name("Vanilla")
        assert land.name == "Vanilla"
        assert result is land
    def test_set_prop_pac_id(self, land):
        """
        Test setting the pac_id property.
        """
        result = land.set_prop_pac_id(1)
        assert land.pac_id == 1
        assert result is land

