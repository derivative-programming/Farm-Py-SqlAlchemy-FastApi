# business/tests/pac_fluent_test.py
# pylint: disable=unused-import
"""
Unit tests for the
PacFluentBusObj class.
"""
import math  # noqa: F401
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
    def new_fluent_bus_obj(self, session):
        """
        Return a PacFluentBusObj
        object.
        """
        session_context = SessionContext(dict(), session=session)
        return PacFluentBusObj(
            session_context)
    # description

    def test_set_prop_description(self, new_fluent_bus_obj):
        """
        Test setting the description property.
        """
        result = new_fluent_bus_obj.set_prop_description(
            "Vanilla")
        assert new_fluent_bus_obj.description == \
            "Vanilla"
        assert result is new_fluent_bus_obj
    # displayOrder

    def test_set_prop_display_order(self, new_fluent_bus_obj):
        """
        Test setting the display_order property.
        """
        result = new_fluent_bus_obj.set_prop_display_order(42)
        assert new_fluent_bus_obj.display_order == 42
        assert result is new_fluent_bus_obj
    # isActive

    def test_set_prop_is_active(self, new_fluent_bus_obj):
        """
        Test setting the is_active property.
        """
        result = new_fluent_bus_obj.set_prop_is_active(True)
        assert new_fluent_bus_obj.is_active is True
        assert result is new_fluent_bus_obj
    # lookupEnumName

    def test_set_prop_lookup_enum_name(self, new_fluent_bus_obj):
        """
        Test setting the lookup_enum_name property.
        """
        result = new_fluent_bus_obj.set_prop_lookup_enum_name(
            "Vanilla")
        assert new_fluent_bus_obj.lookup_enum_name == \
            "Vanilla"
        assert result is new_fluent_bus_obj
    # name

    def test_set_prop_name(self, new_fluent_bus_obj):
        """
        Test setting the name property.
        """
        result = new_fluent_bus_obj.set_prop_name(
            "Vanilla")
        assert new_fluent_bus_obj.name == \
            "Vanilla"
        assert result is new_fluent_bus_obj
    # description,
    # displayOrder,
    # isActive,
    # lookupEnumName,
    # name,
