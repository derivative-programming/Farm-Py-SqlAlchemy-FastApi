# business/tests/df_maintenance_fluent_test.py
# pylint: disable=unused-import
"""
Unit tests for the
DFMaintenanceFluentBusObj class.
"""
import math  # noqa: F401
from datetime import date, datetime  # noqa: F401
from decimal import Decimal  # noqa: F401
from uuid import uuid4  # noqa: F401

import pytest

from business.df_maintenance_fluent import (
    DFMaintenanceFluentBusObj)
from helpers.session_context import SessionContext


class MockDFMaintenanceBaseBusObj:
    """
    A mock base class for the
    DFMaintenanceFluentBusObj class.
    """
    def __init__(self):
        self.is_paused = None
        self.is_scheduled_df_process_request_completed = None
        self.is_scheduled_df_process_request_started = None
        self.last_scheduled_df_process_request_utc_date_time = None
        self.next_scheduled_df_process_request_utc_date_time = None
        self.pac_id = None
        self.paused_by_username = None
        self.paused_utc_date_time = None
        self.scheduled_df_process_request_processor_identifier = None
class TestDFMaintenanceFluentBusObj:
    """
    Unit tests for the
    DFMaintenanceFluentBusObj class.
    """
    @pytest.fixture
    def new_fluent_bus_obj(self, session):
        """
        Return a DFMaintenanceFluentBusObj
        object.
        """
        session_context = SessionContext(dict(), session=session)
        return DFMaintenanceFluentBusObj(session_context)
    # isPaused

    def test_set_prop_is_paused(self, new_fluent_bus_obj):
        """
        Test setting the is_paused property.
        """
        result = new_fluent_bus_obj.set_prop_is_paused(True)
        assert new_fluent_bus_obj.is_paused is True
        assert result is new_fluent_bus_obj
    # isScheduledDFProcessRequestCompleted

    def test_set_prop_is_scheduled_df_process_request_completed(self, new_fluent_bus_obj):
        """
        Test setting the is_scheduled_df_process_request_completed property.
        """
        result = new_fluent_bus_obj.set_prop_is_scheduled_df_process_request_completed(True)
        assert new_fluent_bus_obj.is_scheduled_df_process_request_completed is True
        assert result is new_fluent_bus_obj
    # isScheduledDFProcessRequestStarted

    def test_set_prop_is_scheduled_df_process_request_started(self, new_fluent_bus_obj):
        """
        Test setting the is_scheduled_df_process_request_started property.
        """
        result = new_fluent_bus_obj.set_prop_is_scheduled_df_process_request_started(True)
        assert new_fluent_bus_obj.is_scheduled_df_process_request_started is True
        assert result is new_fluent_bus_obj
    # lastScheduledDFProcessRequestUTCDateTime

    def test_set_prop_last_scheduled_df_process_request_utc_date_time(self, new_fluent_bus_obj):
        """
        Test setting the last_scheduled_df_process_request_utc_date_time property.
        """
        test_datetime = datetime(2023, 1, 1, 12, 0, 0)
        result = new_fluent_bus_obj.set_prop_last_scheduled_df_process_request_utc_date_time(
            test_datetime)
        assert new_fluent_bus_obj.last_scheduled_df_process_request_utc_date_time == \
            test_datetime
        assert result is new_fluent_bus_obj
    # nextScheduledDFProcessRequestUTCDateTime

    def test_set_prop_next_scheduled_df_process_request_utc_date_time(self, new_fluent_bus_obj):
        """
        Test setting the next_scheduled_df_process_request_utc_date_time property.
        """
        test_datetime = datetime(2023, 1, 1, 12, 0, 0)
        result = new_fluent_bus_obj.set_prop_next_scheduled_df_process_request_utc_date_time(
            test_datetime)
        assert new_fluent_bus_obj.next_scheduled_df_process_request_utc_date_time == \
            test_datetime
        assert result is new_fluent_bus_obj
    # PacID
    # pausedByUsername

    def test_set_prop_paused_by_username(self, new_fluent_bus_obj):
        """
        Test setting the paused_by_username property.
        """
        result = new_fluent_bus_obj.set_prop_paused_by_username(
            "Vanilla")
        assert new_fluent_bus_obj.paused_by_username == \
            "Vanilla"
        assert result is new_fluent_bus_obj
    # pausedUTCDateTime

    def test_set_prop_paused_utc_date_time(self, new_fluent_bus_obj):
        """
        Test setting the paused_utc_date_time property.
        """
        test_datetime = datetime(2023, 1, 1, 12, 0, 0)
        result = new_fluent_bus_obj.set_prop_paused_utc_date_time(
            test_datetime)
        assert new_fluent_bus_obj.paused_utc_date_time == \
            test_datetime
        assert result is new_fluent_bus_obj
    # scheduledDFProcessRequestProcessorIdentifier

    def test_set_prop_scheduled_df_process_request_processor_identifier(self, new_fluent_bus_obj):
        """
        Test setting the scheduled_df_process_request_processor_identifier property.
        """
        result = new_fluent_bus_obj.set_prop_scheduled_df_process_request_processor_identifier(
            "Vanilla")
        assert new_fluent_bus_obj.scheduled_df_process_request_processor_identifier == \
            "Vanilla"
        assert result is new_fluent_bus_obj
    # isPaused,
    # isScheduledDFProcessRequestCompleted,
    # isScheduledDFProcessRequestStarted,
    # lastScheduledDFProcessRequestUTCDateTime
    # nextScheduledDFProcessRequestUTCDateTime
    # PacID

    def test_set_prop_pac_id(self, new_fluent_bus_obj):
        """
        Test setting the pac_id property.
        """
        result = new_fluent_bus_obj.set_prop_pac_id(1)
        assert new_fluent_bus_obj.pac_id == 1
        assert result is new_fluent_bus_obj
    # pausedByUsername,
    # pausedUTCDateTime
    # scheduledDFProcessRequestProcessorIdentifier,
