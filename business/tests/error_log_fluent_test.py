# business/tests/error_log_fluent_test.py
# pylint: disable=unused-import
"""
Unit tests for the
ErrorLogFluentBusObj class.
"""
import math  # noqa: F401
from datetime import date, datetime  # noqa: F401
from decimal import Decimal  # noqa: F401
from uuid import uuid4  # noqa: F401

import pytest

from business.error_log_fluent import (
    ErrorLogFluentBusObj)
from helpers.session_context import SessionContext


class MockErrorLogBaseBusObj:
    """
    A mock base class for the
    ErrorLogFluentBusObj class.
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
    Unit tests for the
    ErrorLogFluentBusObj class.
    """
    @pytest.fixture
    def new_fluent_bus_obj(self, session):
        """
        Return a ErrorLogFluentBusObj
        object.
        """
        session_context = SessionContext(dict(), session=session)
        return ErrorLogFluentBusObj(session_context)
    # browserCode

    def test_set_prop_browser_code(self, new_fluent_bus_obj):
        """
        Test setting the browser_code property.
        """
        test_uuid = uuid4()
        result = new_fluent_bus_obj.set_prop_browser_code(
            test_uuid)
        assert new_fluent_bus_obj.browser_code == \
            test_uuid
        assert result is new_fluent_bus_obj
    # contextCode

    def test_set_prop_context_code(self, new_fluent_bus_obj):
        """
        Test setting the context_code property.
        """
        test_uuid = uuid4()
        result = new_fluent_bus_obj.set_prop_context_code(
            test_uuid)
        assert new_fluent_bus_obj.context_code == \
            test_uuid
        assert result is new_fluent_bus_obj
    # createdUTCDateTime

    def test_set_prop_created_utc_date_time(self, new_fluent_bus_obj):
        """
        Test setting the created_utc_date_time property.
        """
        test_datetime = datetime(2023, 1, 1, 12, 0, 0)
        result = new_fluent_bus_obj.set_prop_created_utc_date_time(
            test_datetime)
        assert new_fluent_bus_obj.created_utc_date_time == \
            test_datetime
        assert result is new_fluent_bus_obj
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
    # isClientSideError

    def test_set_prop_is_client_side_error(self, new_fluent_bus_obj):
        """
        Test setting the is_client_side_error property.
        """
        result = new_fluent_bus_obj.set_prop_is_client_side_error(True)
        assert new_fluent_bus_obj.is_client_side_error is True
        assert result is new_fluent_bus_obj
    # isResolved

    def test_set_prop_is_resolved(self, new_fluent_bus_obj):
        """
        Test setting the is_resolved property.
        """
        result = new_fluent_bus_obj.set_prop_is_resolved(True)
        assert new_fluent_bus_obj.is_resolved is True
        assert result is new_fluent_bus_obj
    # PacID
    # url

    def test_set_prop_url(self, new_fluent_bus_obj):
        """
        Test setting the url property.
        """
        result = new_fluent_bus_obj.set_prop_url(
            "Vanilla")
        assert new_fluent_bus_obj.url == \
            "Vanilla"
        assert result is new_fluent_bus_obj
    # browserCode,
    # contextCode,
    # createdUTCDateTime
    # description,
    # isClientSideError,
    # isResolved,
    # PacID

    def test_set_prop_pac_id(self, new_fluent_bus_obj):
        """
        Test setting the pac_id property.
        """
        result = new_fluent_bus_obj.set_prop_pac_id(1)
        assert new_fluent_bus_obj.pac_id == 1
        assert result is new_fluent_bus_obj
    # url,
