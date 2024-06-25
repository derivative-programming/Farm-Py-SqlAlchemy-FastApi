# business/tests/pac_fluent_test.py
# pylint: disable=unused-import
"""
Unit tests for the
PacFluentBusObj class.
"""
import math
from datetime import date, datetime  # noqa: F401
from decimal import Decimal  # noqa: F401
from uuid import uuid4  # noqa: F401

import pytest

from business.pac_fluent import (
    PacFluentBusObj)
from helpers.session_context import SessionContext


class MockPacBaseBusObj:
    """
    A mock base class for the
    PacFluentBusObj class.
    """
    def __init__(self):
        self.description = None
        self.display_order = None
        self.is_active = None
        self.lookup_enum_name = None
        self.name = None
class TestPacFluentBusObj:
    """
    Unit tests for the
    PacFluentBusObj class.
    """
    @pytest.fixture
    def pac(self, session):
        """
        Return a PacFluentBusObj
        object.
        """
        session_context = SessionContext(dict(), session=session)
        return PacFluentBusObj(session_context)
    def test_set_prop_description(self, pac):
        """
        Test setting the description property.
        """
        result = pac.set_prop_description("Vanilla")
        assert pac.description == "Vanilla"
        assert result is pac
    def test_set_prop_display_order(self, pac):
        """
        Test setting the display_order property.
        """
        result = pac.set_prop_display_order(42)
        assert pac.display_order == 42
        assert result is pac
    def test_set_prop_is_active(self, pac):
        """
        Test setting the is_active property.
        """
        result = pac.set_prop_is_active(True)
        assert pac.is_active is True
        assert result is pac
    def test_set_prop_lookup_enum_name(self, pac):
        """
        Test setting the lookup_enum_name property.
        """
        result = pac.set_prop_lookup_enum_name("Vanilla")
        assert pac.lookup_enum_name == "Vanilla"
        assert result is pac
    def test_set_prop_name(self, pac):
        """
        Test setting the name property.
        """
        result = pac.set_prop_name("Vanilla")
        assert pac.name == "Vanilla"
        assert result is pac

