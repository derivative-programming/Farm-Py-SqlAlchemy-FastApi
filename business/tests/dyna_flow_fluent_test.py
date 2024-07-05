# business/tests/dyna_flow_fluent_test.py
# pylint: disable=unused-import
"""
Unit tests for the
DynaFlowFluentBusObj class.
"""
import math  # noqa: F401
from datetime import date, datetime, timezone  # noqa: F401
from decimal import Decimal  # noqa: F401
from uuid import uuid4  # noqa: F401

import pytest

from business.dyna_flow_fluent import (
    DynaFlowFluentBusObj)
from helpers.session_context import SessionContext


class MockDynaFlowBaseBusObj:
    """
    A mock base class for the
    DynaFlowFluentBusObj class.
    """
    def __init__(self):
        self.completed_utc_date_time = None
        self.dependency_dyna_flow_id = None
        self.description = None
        self.dyna_flow_type_id = None
        self.is_build_task_debug_required = None
        self.is_canceled = None
        self.is_cancel_requested = None
        self.is_completed = None
        self.is_paused = None
        self.is_resubmitted = None
        self.is_run_task_debug_required = None
        self.is_started = None
        self.is_successful = None
        self.is_task_creation_started = None
        self.is_tasks_created = None
        self.min_start_utc_date_time = None
        self.pac_id = None
        self.param_1 = None
        self.parent_dyna_flow_id = None
        self.priority_level = None
        self.requested_utc_date_time = None
        self.result_value = None
        self.root_dyna_flow_id = None
        self.started_utc_date_time = None
        self.subject_code = None
        self.task_creation_processor_identifier = None
class TestDynaFlowFluentBusObj:
    """
    Unit tests for the
    DynaFlowFluentBusObj class.
    """
    @pytest.fixture
    def new_fluent_bus_obj(self, session):
        """
        Return a DynaFlowFluentBusObj
        object.
        """
        session_context = SessionContext({}, session=session)
        return DynaFlowFluentBusObj(
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
    # dependencyDynaFlowID

    def test_set_prop_dependency_dyna_flow_id(self, new_fluent_bus_obj):
        """
        Test setting the dependency_dyna_flow_id property.
        """
        result = new_fluent_bus_obj.set_prop_dependency_dyna_flow_id(42)
        assert new_fluent_bus_obj.dependency_dyna_flow_id == 42
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
    # DynaFlowTypeID
    # isBuildTaskDebugRequired

    def test_set_prop_is_build_task_debug_required(self, new_fluent_bus_obj):
        """
        Test setting the is_build_task_debug_required property.
        """
        result = new_fluent_bus_obj.set_prop_is_build_task_debug_required(True)
        assert new_fluent_bus_obj.is_build_task_debug_required is True
        assert result is new_fluent_bus_obj
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
    # isPaused

    def test_set_prop_is_paused(self, new_fluent_bus_obj):
        """
        Test setting the is_paused property.
        """
        result = new_fluent_bus_obj.set_prop_is_paused(True)
        assert new_fluent_bus_obj.is_paused is True
        assert result is new_fluent_bus_obj
    # isResubmitted

    def test_set_prop_is_resubmitted(self, new_fluent_bus_obj):
        """
        Test setting the is_resubmitted property.
        """
        result = new_fluent_bus_obj.set_prop_is_resubmitted(True)
        assert new_fluent_bus_obj.is_resubmitted is True
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
    # isTaskCreationStarted

    def test_set_prop_is_task_creation_started(self, new_fluent_bus_obj):
        """
        Test setting the is_task_creation_started property.
        """
        result = new_fluent_bus_obj.set_prop_is_task_creation_started(True)
        assert new_fluent_bus_obj.is_task_creation_started is True
        assert result is new_fluent_bus_obj
    # isTasksCreated

    def test_set_prop_is_tasks_created(self, new_fluent_bus_obj):
        """
        Test setting the is_tasks_created property.
        """
        result = new_fluent_bus_obj.set_prop_is_tasks_created(True)
        assert new_fluent_bus_obj.is_tasks_created is True
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
    # PacID
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
    # parentDynaFlowID

    def test_set_prop_parent_dyna_flow_id(self, new_fluent_bus_obj):
        """
        Test setting the parent_dyna_flow_id property.
        """
        result = new_fluent_bus_obj.set_prop_parent_dyna_flow_id(42)
        assert new_fluent_bus_obj.parent_dyna_flow_id == 42
        assert result is new_fluent_bus_obj
    # priorityLevel

    def test_set_prop_priority_level(self, new_fluent_bus_obj):
        """
        Test setting the priority_level property.
        """
        result = new_fluent_bus_obj.set_prop_priority_level(42)
        assert new_fluent_bus_obj.priority_level == 42
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
    # rootDynaFlowID

    def test_set_prop_root_dyna_flow_id(self, new_fluent_bus_obj):
        """
        Test setting the root_dyna_flow_id property.
        """
        result = new_fluent_bus_obj.set_prop_root_dyna_flow_id(42)
        assert new_fluent_bus_obj.root_dyna_flow_id == 42
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
    # subjectCode

    def test_set_prop_subject_code(self, new_fluent_bus_obj):
        """
        Test setting the subject_code property.
        """
        test_uuid = uuid4()
        result = new_fluent_bus_obj.set_prop_subject_code(
            test_uuid)
        assert new_fluent_bus_obj.subject_code == \
            test_uuid
        assert result is new_fluent_bus_obj
    # taskCreationProcessorIdentifier

    def test_set_prop_task_creation_processor_identifier(self, new_fluent_bus_obj):
        """
        Test setting the task_creation_processor_identifier property.
        """
        result = new_fluent_bus_obj.set_prop_task_creation_processor_identifier(
            "Vanilla")
        assert new_fluent_bus_obj.task_creation_processor_identifier == \
            "Vanilla"
        assert result is new_fluent_bus_obj
    # completedUTCDateTime
    # dependencyDynaFlowID,
    # description,
    # DynaFlowTypeID

    def test_set_prop_dyna_flow_type_id(self, new_fluent_bus_obj):
        """
        Test setting the dyna_flow_type_id property.
        """
        result = new_fluent_bus_obj.set_prop_dyna_flow_type_id(1)
        assert new_fluent_bus_obj.dyna_flow_type_id == 1
        assert result is new_fluent_bus_obj
    # isBuildTaskDebugRequired,
    # isCanceled,
    # isCancelRequested,
    # isCompleted,
    # isPaused,
    # isResubmitted,
    # isRunTaskDebugRequired,
    # isStarted,
    # isSuccessful,
    # isTaskCreationStarted,
    # isTasksCreated,
    # minStartUTCDateTime
    # PacID

    def test_set_prop_pac_id(self, new_fluent_bus_obj):
        """
        Test setting the pac_id property.
        """
        result = new_fluent_bus_obj.set_prop_pac_id(1)
        assert new_fluent_bus_obj.pac_id == 1
        assert result is new_fluent_bus_obj
    # param1,
    # parentDynaFlowID,
    # priorityLevel,
    # requestedUTCDateTime
    # resultValue,
    # rootDynaFlowID,
    # startedUTCDateTime
    # subjectCode,
    # taskCreationProcessorIdentifier,
