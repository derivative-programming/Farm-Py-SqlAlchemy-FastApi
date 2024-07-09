# business/tests/dyna_flow_type_schedule_fluent_test.py  # pylint: disable=duplicate-code # noqa: E501
# pylint: disable=unused-import, too-many-public-methods
# pylint: disable=too-few-public-methods
"""
Unit tests for the
DynaFlowTypeScheduleFluentBusObj class.
"""
import math  # noqa: F401
from datetime import date, datetime, timezone  # noqa: F401
from decimal import Decimal  # noqa: F401
from uuid import uuid4  # noqa: F401

import pytest
from business.dyna_flow_type_schedule_fluent import \
    DynaFlowTypeScheduleFluentBusObj
from helpers.session_context import SessionContext


class MockDynaFlowTypeScheduleBaseBusObj:
    """
    A mock base class for the
    DynaFlowTypeScheduleFluentBusObj class.
    """
    def __init__(self):
        self.dyna_flow_type_id = None
        self.frequency_in_hours = None
        self.is_active = None
        self.last_utc_date_time = None
        self.next_utc_date_time = None
        self.pac_id = None
class TestDynaFlowTypeScheduleFluentBusObj:
    """
    Unit tests for the
    DynaFlowTypeScheduleFluentBusObj class.
    """
    @pytest.fixture
    def new_fluent_bus_obj(self, session):
        """
        Return a DynaFlowTypeScheduleFluentBusObj
        object.
        """
        session_context = SessionContext({}, session=session)
        return DynaFlowTypeScheduleFluentBusObj(
            session_context)
    # DynaFlowTypeID
    # frequencyInHours

    def test_set_prop_frequency_in_hours(self, new_fluent_bus_obj):
        """
        Test setting the frequency_in_hours property.
        """
        result = new_fluent_bus_obj.set_prop_frequency_in_hours(42)
        assert new_fluent_bus_obj.frequency_in_hours == 42
        assert result is new_fluent_bus_obj
    # isActive

    def test_set_prop_is_active(self, new_fluent_bus_obj):
        """
        Test setting the is_active property.
        """
        result = new_fluent_bus_obj.set_prop_is_active(True)
        assert new_fluent_bus_obj.is_active is True
        assert result is new_fluent_bus_obj
    # lastUTCDateTime

    def test_set_prop_last_utc_date_time(self, new_fluent_bus_obj):
        """
        Test setting the last_utc_date_time property.
        """
        test_datetime = datetime(2023, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
        result = new_fluent_bus_obj.set_prop_last_utc_date_time(
            test_datetime)
        assert new_fluent_bus_obj.last_utc_date_time == \
            test_datetime
        assert result is new_fluent_bus_obj
    # nextUTCDateTime

    def test_set_prop_next_utc_date_time(self, new_fluent_bus_obj):
        """
        Test setting the next_utc_date_time property.
        """
        test_datetime = datetime(2023, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
        result = new_fluent_bus_obj.set_prop_next_utc_date_time(
            test_datetime)
        assert new_fluent_bus_obj.next_utc_date_time == \
            test_datetime
        assert result is new_fluent_bus_obj
    # PacID
    # DynaFlowTypeID

    def test_set_prop_dyna_flow_type_id(self, new_fluent_bus_obj):
        """
        Test setting the dyna_flow_type_id property.
        """
        result = new_fluent_bus_obj.set_prop_dyna_flow_type_id(1)
        assert new_fluent_bus_obj.dyna_flow_type_id == 1
        assert result is new_fluent_bus_obj
    # frequencyInHours
    # isActive
    # lastUTCDateTime
    # nextUTCDateTime
    # PacID

    def test_set_prop_pac_id(self, new_fluent_bus_obj):
        """
        Test setting the pac_id property.
        """
        result = new_fluent_bus_obj.set_prop_pac_id(1)
        assert new_fluent_bus_obj.pac_id == 1
        assert result is new_fluent_bus_obj
