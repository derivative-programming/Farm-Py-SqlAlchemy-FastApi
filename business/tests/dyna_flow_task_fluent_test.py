# business/tests/dyna_flow_task_fluent_test.py
# pylint: disable=unused-import
"""
Unit tests for the
DynaFlowTaskFluentBusObj class.
"""
import math  # noqa: F401
from datetime import date, datetime, timezone  # noqa: F401
from decimal import Decimal  # noqa: F401
from uuid import uuid4  # noqa: F401

import pytest

from business.dyna_flow_task_fluent import (
    DynaFlowTaskFluentBusObj)
from helpers.session_context import SessionContext


class MockDynaFlowTaskBaseBusObj:
    """
    A mock base class for the
    DynaFlowTaskFluentBusObj class.
    """
    def __init__(self):
        self.completed_utc_date_time = None
        self.dependency_dyna_flow_task_id = None
        self.description = None
        self.dyna_flow_id = None
        self.dyna_flow_subject_code = None
        self.dyna_flow_task_type_id = None
        self.is_canceled = None
        self.is_cancel_requested = None
        self.is_completed = None
        self.is_parallel_run_allowed = None
        self.is_run_task_debug_required = None
        self.is_started = None
        self.is_successful = None
        self.max_retry_count = None
        self.min_start_utc_date_time = None
        self.param_1 = None
        self.param_2 = None
        self.processor_identifier = None
        self.requested_utc_date_time = None
        self.result_value = None
        self.retry_count = None
        self.started_utc_date_time = None
class TestDynaFlowTaskFluentBusObj:
    """
    Unit tests for the
    DynaFlowTaskFluentBusObj class.
    """
    @pytest.fixture
    def new_fluent_bus_obj(self, session):
        """
        Return a DynaFlowTaskFluentBusObj
        object.
        """
        session_context = SessionContext({}, session=session)
        return DynaFlowTaskFluentBusObj(
            session_context)
    # completedUTCDateTime

    def test_set_prop_completed_utc_date_time(self, new_fluent_bus_obj):
        """
        Test setting the completed_utc_date_time property.
        """
        test_datetime = datetime(2023, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
        result = new_fluent_bus_obj.set_prop_completed_utc_date_time(
            test_datetime)
        assert new_fluent_bus_obj.completed_utc_date_time == \
            test_datetime
        assert result is new_fluent_bus_obj
    # dependencyDynaFlowTaskID

    def test_set_prop_dependency_dyna_flow_task_id(self, new_fluent_bus_obj):
        """
        Test setting the dependency_dyna_flow_task_id property.
        """
        result = new_fluent_bus_obj.set_prop_dependency_dyna_flow_task_id(42)
        assert new_fluent_bus_obj.dependency_dyna_flow_task_id == 42
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
    # DynaFlowID
    # dynaFlowSubjectCode

    def test_set_prop_dyna_flow_subject_code(self, new_fluent_bus_obj):
        """
        Test setting the dyna_flow_subject_code property.
        """
        test_uuid = uuid4()
        result = new_fluent_bus_obj.set_prop_dyna_flow_subject_code(
            test_uuid)
        assert new_fluent_bus_obj.dyna_flow_subject_code == \
            test_uuid
        assert result is new_fluent_bus_obj
    # DynaFlowTaskTypeID
    # isCanceled

    def test_set_prop_is_canceled(self, new_fluent_bus_obj):
        """
        Test setting the is_canceled property.
        """
        result = new_fluent_bus_obj.set_prop_is_canceled(True)
        assert new_fluent_bus_obj.is_canceled is True
        assert result is new_fluent_bus_obj
    # isCancelRequested

    def test_set_prop_is_cancel_requested(self, new_fluent_bus_obj):
        """
        Test setting the is_cancel_requested property.
        """
        result = new_fluent_bus_obj.set_prop_is_cancel_requested(True)
        assert new_fluent_bus_obj.is_cancel_requested is True
        assert result is new_fluent_bus_obj
    # isCompleted

    def test_set_prop_is_completed(self, new_fluent_bus_obj):
        """
        Test setting the is_completed property.
        """
        result = new_fluent_bus_obj.set_prop_is_completed(True)
        assert new_fluent_bus_obj.is_completed is True
        assert result is new_fluent_bus_obj
    # isParallelRunAllowed

    def test_set_prop_is_parallel_run_allowed(self, new_fluent_bus_obj):
        """
        Test setting the is_parallel_run_allowed property.
        """
        result = new_fluent_bus_obj.set_prop_is_parallel_run_allowed(True)
        assert new_fluent_bus_obj.is_parallel_run_allowed is True
        assert result is new_fluent_bus_obj
    # isRunTaskDebugRequired

    def test_set_prop_is_run_task_debug_required(self, new_fluent_bus_obj):
        """
        Test setting the is_run_task_debug_required property.
        """
        result = new_fluent_bus_obj.set_prop_is_run_task_debug_required(True)
        assert new_fluent_bus_obj.is_run_task_debug_required is True
        assert result is new_fluent_bus_obj
    # isStarted

    def test_set_prop_is_started(self, new_fluent_bus_obj):
        """
        Test setting the is_started property.
        """
        result = new_fluent_bus_obj.set_prop_is_started(True)
        assert new_fluent_bus_obj.is_started is True
        assert result is new_fluent_bus_obj
    # isSuccessful

    def test_set_prop_is_successful(self, new_fluent_bus_obj):
        """
        Test setting the is_successful property.
        """
        result = new_fluent_bus_obj.set_prop_is_successful(True)
        assert new_fluent_bus_obj.is_successful is True
        assert result is new_fluent_bus_obj
    # maxRetryCount

    def test_set_prop_max_retry_count(self, new_fluent_bus_obj):
        """
        Test setting the max_retry_count property.
        """
        result = new_fluent_bus_obj.set_prop_max_retry_count(42)
        assert new_fluent_bus_obj.max_retry_count == 42
        assert result is new_fluent_bus_obj
    # minStartUTCDateTime

    def test_set_prop_min_start_utc_date_time(self, new_fluent_bus_obj):
        """
        Test setting the min_start_utc_date_time property.
        """
        test_datetime = datetime(2023, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
        result = new_fluent_bus_obj.set_prop_min_start_utc_date_time(
            test_datetime)
        assert new_fluent_bus_obj.min_start_utc_date_time == \
            test_datetime
        assert result is new_fluent_bus_obj
    # param1

    def test_set_prop_param_1(self, new_fluent_bus_obj):
        """
        Test setting the param_1 property.
        """
        result = new_fluent_bus_obj.set_prop_param_1(
            "Vanilla")
        assert new_fluent_bus_obj.param_1 == \
            "Vanilla"
        assert result is new_fluent_bus_obj
    # param2

    def test_set_prop_param_2(self, new_fluent_bus_obj):
        """
        Test setting the param_2 property.
        """
        result = new_fluent_bus_obj.set_prop_param_2(
            "Vanilla")
        assert new_fluent_bus_obj.param_2 == \
            "Vanilla"
        assert result is new_fluent_bus_obj
    # processorIdentifier

    def test_set_prop_processor_identifier(self, new_fluent_bus_obj):
        """
        Test setting the processor_identifier property.
        """
        result = new_fluent_bus_obj.set_prop_processor_identifier(
            "Vanilla")
        assert new_fluent_bus_obj.processor_identifier == \
            "Vanilla"
        assert result is new_fluent_bus_obj
    # requestedUTCDateTime

    def test_set_prop_requested_utc_date_time(self, new_fluent_bus_obj):
        """
        Test setting the requested_utc_date_time property.
        """
        test_datetime = datetime(2023, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
        result = new_fluent_bus_obj.set_prop_requested_utc_date_time(
            test_datetime)
        assert new_fluent_bus_obj.requested_utc_date_time == \
            test_datetime
        assert result is new_fluent_bus_obj
    # resultValue

    def test_set_prop_result_value(self, new_fluent_bus_obj):
        """
        Test setting the result_value property.
        """
        result = new_fluent_bus_obj.set_prop_result_value(
            "Vanilla")
        assert new_fluent_bus_obj.result_value == \
            "Vanilla"
        assert result is new_fluent_bus_obj
    # retryCount

    def test_set_prop_retry_count(self, new_fluent_bus_obj):
        """
        Test setting the retry_count property.
        """
        result = new_fluent_bus_obj.set_prop_retry_count(42)
        assert new_fluent_bus_obj.retry_count == 42
        assert result is new_fluent_bus_obj
    # startedUTCDateTime

    def test_set_prop_started_utc_date_time(self, new_fluent_bus_obj):
        """
        Test setting the started_utc_date_time property.
        """
        test_datetime = datetime(2023, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
        result = new_fluent_bus_obj.set_prop_started_utc_date_time(
            test_datetime)
        assert new_fluent_bus_obj.started_utc_date_time == \
            test_datetime
        assert result is new_fluent_bus_obj
    # completedUTCDateTime
    # dependencyDynaFlowTaskID,
    # description,
    # DynaFlowID

    def test_set_prop_dyna_flow_id(self, new_fluent_bus_obj):
        """
        Test setting the dyna_flow_id property.
        """
        result = new_fluent_bus_obj.set_prop_dyna_flow_id(1)
        assert new_fluent_bus_obj.dyna_flow_id == 1
        assert result is new_fluent_bus_obj
    # dynaFlowSubjectCode,
    # DynaFlowTaskTypeID

    def test_set_prop_dyna_flow_task_type_id(self, new_fluent_bus_obj):
        """
        Test setting the dyna_flow_task_type_id property.
        """
        result = new_fluent_bus_obj.set_prop_dyna_flow_task_type_id(1)
        assert new_fluent_bus_obj.dyna_flow_task_type_id == 1
        assert result is new_fluent_bus_obj
    # isCanceled,
    # isCancelRequested,
    # isCompleted,
    # isParallelRunAllowed,
    # isRunTaskDebugRequired,
    # isStarted,
    # isSuccessful,
    # maxRetryCount,
    # minStartUTCDateTime
    # param1,
    # param2,
    # processorIdentifier,
    # requestedUTCDateTime
    # resultValue,
    # retryCount,
    # startedUTCDateTime
