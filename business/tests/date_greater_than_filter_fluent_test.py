# business/tests/date_greater_than_filter_fluent_test.py
"""
Unit tests for the DateGreaterThanFilterFluentBusObj class.
"""
from datetime import date, datetime
from decimal import Decimal
from uuid import UUID, uuid4
import pytest
from business.date_greater_than_filter_fluent import DateGreaterThanFilterFluentBusObj
from helpers.session_context import SessionContext
class MockDateGreaterThanFilterBaseBusObj:
    """
    A mock base class for the DateGreaterThanFilterFluentBusObj class.
    """
    def __init__(self):
        self.day_count = None
        self.description = None
        self.display_order = None
        self.is_active = None
        self.lookup_enum_name = None
        self.name = None
        self.pac_id = None
class TestDateGreaterThanFilterFluentBusObj:
    """
    Unit tests for the DateGreaterThanFilterFluentBusObj class.
    """
    @pytest.fixture
    def date_greater_than_filter(self, session):
        """
        Return a DateGreaterThanFilterFluentBusObj object.
        """
        session_context = SessionContext(dict(), session=session)
        return DateGreaterThanFilterFluentBusObj(session_context)
    def test_set_prop_day_count(self, date_greater_than_filter):
        """
        Test setting the day_count property.
        """
        result = date_greater_than_filter.set_prop_day_count(42)
        assert date_greater_than_filter.day_count == 42
        assert result is date_greater_than_filter
    def test_set_prop_description(self, date_greater_than_filter):
        """
        Test setting the description property.
        """
        result = date_greater_than_filter.set_prop_description("Vanilla")
        assert date_greater_than_filter.description == "Vanilla"
        assert result is date_greater_than_filter
    def test_set_prop_display_order(self, date_greater_than_filter):
        """
        Test setting the display_order property.
        """
        result = date_greater_than_filter.set_prop_display_order(42)
        assert date_greater_than_filter.display_order == 42
        assert result is date_greater_than_filter
    def test_set_prop_is_active(self, date_greater_than_filter):
        """
        Test setting the is_active property.
        """
        result = date_greater_than_filter.set_prop_is_active(True)
        assert date_greater_than_filter.is_active is True
        assert result is date_greater_than_filter
    def test_set_prop_lookup_enum_name(self, date_greater_than_filter):
        """
        Test setting the lookup_enum_name property.
        """
        result = date_greater_than_filter.set_prop_lookup_enum_name("Vanilla")
        assert date_greater_than_filter.lookup_enum_name == "Vanilla"
        assert result is date_greater_than_filter
    def test_set_prop_name(self, date_greater_than_filter):
        """
        Test setting the name property.
        """
        result = date_greater_than_filter.set_prop_name("Vanilla")
        assert date_greater_than_filter.name == "Vanilla"
        assert result is date_greater_than_filter
    def test_set_prop_pac_id(self, date_greater_than_filter):
        """
        Test setting the pac_id property.
        """
        result = date_greater_than_filter.set_prop_pac_id(1)
        assert date_greater_than_filter.pac_id == 1
        assert result is date_greater_than_filter
