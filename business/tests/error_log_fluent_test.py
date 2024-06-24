# business/tests/error_log_fluent_test.py
"""
Unit tests for the ErrorLogFluentBusObj class.
"""
import math
from datetime import date, datetime
from decimal import Decimal
from uuid import uuid4
import pytest
from business.error_log_fluent import ErrorLogFluentBusObj
from helpers.session_context import SessionContext
class MockErrorLogBaseBusObj:
    """
    A mock base class for the ErrorLogFluentBusObj class.
    """
    def __init__(self):
        self.browser_code = None
        self.context_code = None
        self.created_utc_date_time = None
        self.description = None
        self.is_client_side_error = None
        self.is_resolved = None
        self.pac_id = None
        self.url = None
class TestErrorLogFluentBusObj:
    """
    Unit tests for the ErrorLogFluentBusObj class.
    """
    @pytest.fixture
    def error_log(self, session):
        """
        Return a ErrorLogFluentBusObj object.
        """
        session_context = SessionContext(dict(), session=session)
        return ErrorLogFluentBusObj(session_context)
    def test_set_prop_browser_code(self, error_log):
        """
        Test setting the browser_code property.
        """
        test_uuid = uuid4()
        result = error_log.set_prop_browser_code(test_uuid)
        assert error_log.browser_code == test_uuid
        assert result is error_log
    def test_set_prop_context_code(self, error_log):
        """
        Test setting the context_code property.
        """
        test_uuid = uuid4()
        result = error_log.set_prop_context_code(test_uuid)
        assert error_log.context_code == test_uuid
        assert result is error_log
    def test_set_prop_created_utc_date_time(self, error_log):
        """
        Test setting the created_utc_date_time property.
        """
        test_datetime = datetime(2023, 1, 1, 12, 0, 0)
        result = error_log.set_prop_created_utc_date_time(test_datetime)
        assert error_log.created_utc_date_time == test_datetime
        assert result is error_log
    def test_set_prop_description(self, error_log):
        """
        Test setting the description property.
        """
        result = error_log.set_prop_description("Vanilla")
        assert error_log.description == "Vanilla"
        assert result is error_log
    def test_set_prop_is_client_side_error(self, error_log):
        """
        Test setting the is_client_side_error property.
        """
        result = error_log.set_prop_is_client_side_error(True)
        assert error_log.is_client_side_error is True
        assert result is error_log
    def test_set_prop_is_resolved(self, error_log):
        """
        Test setting the is_resolved property.
        """
        result = error_log.set_prop_is_resolved(True)
        assert error_log.is_resolved is True
        assert result is error_log
    def test_set_prop_pac_id(self, error_log):
        """
        Test setting the pac_id property.
        """
        result = error_log.set_prop_pac_id(1)
        assert error_log.pac_id == 1
        assert result is error_log
    def test_set_prop_url(self, error_log):
        """
        Test setting the url property.
        """
        result = error_log.set_prop_url("Vanilla")
        assert error_log.url == "Vanilla"
        assert result is error_log
