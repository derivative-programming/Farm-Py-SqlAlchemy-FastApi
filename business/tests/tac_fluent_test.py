# business/tests/tac_fluent_test.py
"""
Unit tests for the TacFluentBusObj class.
"""
from datetime import date, datetime
from decimal import Decimal
from uuid import UUID, uuid4
import pytest
from business.tac_fluent import TacFluentBusObj
from helpers.session_context import SessionContext
class MockTacBaseBusObj:
    """
    A mock base class for the TacFluentBusObj class.
    """
    def __init__(self):
        self.description = None
        self.display_order = None
        self.is_active = None
        self.lookup_enum_name = None
        self.name = None
        self.pac_id = None
class TestTacFluentBusObj:
    """
    Unit tests for the TacFluentBusObj class.
    """
    @pytest.fixture
    def tac(self, session):
        """
        Return a TacFluentBusObj object.
        """
        session_context = SessionContext(dict(), session=session)
        return TacFluentBusObj(session_context)
    def test_set_prop_description(self, tac):
        """
        Test setting the description property.
        """
        result = tac.set_prop_description("Vanilla")
        assert tac.description == "Vanilla"
        assert result is tac
    def test_set_prop_display_order(self, tac):
        """
        Test setting the display_order property.
        """
        result = tac.set_prop_display_order(42)
        assert tac.display_order == 42
        assert result is tac
    def test_set_prop_is_active(self, tac):
        """
        Test setting the is_active property.
        """
        result = tac.set_prop_is_active(True)
        assert tac.is_active is True
        assert result is tac
    def test_set_prop_lookup_enum_name(self, tac):
        """
        Test setting the lookup_enum_name property.
        """
        result = tac.set_prop_lookup_enum_name("Vanilla")
        assert tac.lookup_enum_name == "Vanilla"
        assert result is tac
    def test_set_prop_name(self, tac):
        """
        Test setting the name property.
        """
        result = tac.set_prop_name("Vanilla")
        assert tac.name == "Vanilla"
        assert result is tac
    def test_set_prop_pac_id(self, tac):
        """
        Test setting the pac_id property.
        """
        result = tac.set_prop_pac_id(1)
        assert tac.pac_id == 1
        assert result is tac
