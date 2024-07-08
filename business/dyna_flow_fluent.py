# business/dyna_flow_fluent.py  # pylint: disable=duplicate-code
# pylint: disable=unused-import

"""
This module contains the
DynaFlowFluentBusObj class,
which adds fluent properties
to the business object for a
DynaFlow.
"""

import uuid  # noqa: F401
from datetime import date, datetime, timezone  # noqa: F401
from decimal import Decimal  # noqa: F401

import managers as managers_and_enums

from .dyna_flow_base import DynaFlowBaseBusObj


class DynaFlowFluentBusObj(DynaFlowBaseBusObj):
    """
    This class add fluent properties to the
    Base DynaFlow Business Object
    """

    # completedUTCDateTime

    def set_prop_completed_utc_date_time(self, value: datetime):
        """
        Sets the value of the
        'completed_utc_date_time' property.

        Args:
            value (datetime): The datetime value to set.

        Returns:
            self: The current instance of the class.
        """
        self.completed_utc_date_time = value
        return self
    # dependencyDynaFlowID

    def set_prop_dependency_dyna_flow_id(self, value: int):
        """
        Set the value of
        dependency_dyna_flow_id property.

        Args:
            value (int): The value to set for
                dependency_dyna_flow_id.

        Returns:
            self: Returns the instance of the class.

        """
        self.dependency_dyna_flow_id = value
        return self
    # description

    def set_prop_description(self, value: str):
        """
        Set the Description for the
        DynaFlow object.

        :param value: The Description value.
        :return: The updated
            DynaFlowBusObj instance.
        """

        self.description = value
        return self
    # DynaFlowTypeID
    # isBuildTaskDebugRequired

    def set_prop_is_build_task_debug_required(self, value: bool):
        """
        Set the Is Build Task Debug Required flag for the
        DynaFlow object.

        :param value: The Is Build Task Debug Required flag value.
        :return: The updated
            DynaFlowBusObj instance.
        """

        self.is_build_task_debug_required = value
        return self
    # isCanceled

    def set_prop_is_canceled(self, value: bool):
        """
        Set the Is Canceled flag for the
        DynaFlow object.

        :param value: The Is Canceled flag value.
        :return: The updated
            DynaFlowBusObj instance.
        """

        self.is_canceled = value
        return self
    # isCancelRequested

    def set_prop_is_cancel_requested(self, value: bool):
        """
        Set the Is Cancel Requested flag for the
        DynaFlow object.

        :param value: The Is Cancel Requested flag value.
        :return: The updated
            DynaFlowBusObj instance.
        """

        self.is_cancel_requested = value
        return self
    # isCompleted

    def set_prop_is_completed(self, value: bool):
        """
        Set the Is Completed flag for the
        DynaFlow object.

        :param value: The Is Completed flag value.
        :return: The updated
            DynaFlowBusObj instance.
        """

        self.is_completed = value
        return self
    # isPaused

    def set_prop_is_paused(self, value: bool):
        """
        Set the Is Paused flag for the
        DynaFlow object.

        :param value: The Is Paused flag value.
        :return: The updated
            DynaFlowBusObj instance.
        """

        self.is_paused = value
        return self
    # isResubmitted

    def set_prop_is_resubmitted(self, value: bool):
        """
        Set the Is Resubmitted flag for the
        DynaFlow object.

        :param value: The Is Resubmitted flag value.
        :return: The updated
            DynaFlowBusObj instance.
        """

        self.is_resubmitted = value
        return self
    # isRunTaskDebugRequired

    def set_prop_is_run_task_debug_required(self, value: bool):
        """
        Set the Is Run Task Debug Required flag for the
        DynaFlow object.

        :param value: The Is Run Task Debug Required flag value.
        :return: The updated
            DynaFlowBusObj instance.
        """

        self.is_run_task_debug_required = value
        return self
    # isStarted

    def set_prop_is_started(self, value: bool):
        """
        Set the Is Started flag for the
        DynaFlow object.

        :param value: The Is Started flag value.
        :return: The updated
            DynaFlowBusObj instance.
        """

        self.is_started = value
        return self
    # isSuccessful

    def set_prop_is_successful(self, value: bool):
        """
        Set the Is Successful flag for the
        DynaFlow object.

        :param value: The Is Successful flag value.
        :return: The updated
            DynaFlowBusObj instance.
        """

        self.is_successful = value
        return self
    # isTaskCreationStarted

    def set_prop_is_task_creation_started(self, value: bool):
        """
        Set the Is Task Creation Started flag for the
        DynaFlow object.

        :param value: The Is Task Creation Started flag value.
        :return: The updated
            DynaFlowBusObj instance.
        """

        self.is_task_creation_started = value
        return self
    # isTasksCreated

    def set_prop_is_tasks_created(self, value: bool):
        """
        Set the Is Tasks Created flag for the
        DynaFlow object.

        :param value: The Is Tasks Created flag value.
        :return: The updated
            DynaFlowBusObj instance.
        """

        self.is_tasks_created = value
        return self
    # minStartUTCDateTime

    def set_prop_min_start_utc_date_time(self, value: datetime):
        """
        Sets the value of the
        'min_start_utc_date_time' property.

        Args:
            value (datetime): The datetime value to set.

        Returns:
            self: The current instance of the class.
        """
        self.min_start_utc_date_time = value
        return self
    # PacID
    # param1

    def set_prop_param_1(self, value: str):
        """
        Set the Param 1 for the
        DynaFlow object.

        :param value: The Param 1 value.
        :return: The updated
            DynaFlowBusObj instance.
        """

        self.param_1 = value
        return self
    # parentDynaFlowID

    def set_prop_parent_dyna_flow_id(self, value: int):
        """
        Set the value of
        parent_dyna_flow_id property.

        Args:
            value (int): The value to set for
                parent_dyna_flow_id.

        Returns:
            self: Returns the instance of the class.

        """
        self.parent_dyna_flow_id = value
        return self
    # priorityLevel

    def set_prop_priority_level(self, value: int):
        """
        Set the value of
        priority_level property.

        Args:
            value (int): The value to set for
                priority_level.

        Returns:
            self: Returns the instance of the class.

        """
        self.priority_level = value
        return self
    # requestedUTCDateTime

    def set_prop_requested_utc_date_time(self, value: datetime):
        """
        Sets the value of the
        'requested_utc_date_time' property.

        Args:
            value (datetime): The datetime value to set.

        Returns:
            self: The current instance of the class.
        """
        self.requested_utc_date_time = value
        return self
    # resultValue

    def set_prop_result_value(self, value: str):
        """
        Set the Result Value for the
        DynaFlow object.

        :param value: The Result Value value.
        :return: The updated
            DynaFlowBusObj instance.
        """

        self.result_value = value
        return self
    # rootDynaFlowID

    def set_prop_root_dyna_flow_id(self, value: int):
        """
        Set the value of
        root_dyna_flow_id property.

        Args:
            value (int): The value to set for
                root_dyna_flow_id.

        Returns:
            self: Returns the instance of the class.

        """
        self.root_dyna_flow_id = value
        return self
    # startedUTCDateTime

    def set_prop_started_utc_date_time(self, value: datetime):
        """
        Sets the value of the
        'started_utc_date_time' property.

        Args:
            value (datetime): The datetime value to set.

        Returns:
            self: The current instance of the class.
        """
        self.started_utc_date_time = value
        return self
    # subjectCode

    def set_prop_subject_code(self, value: uuid.UUID):
        """
        Set the value of the
        'subject_code' property.

        Args:
            value (uuid.UUID): The value to set.

        Returns:
            self: The current instance of the class.
        """
        self.subject_code = value
        return self
    # taskCreationProcessorIdentifier

    def set_prop_task_creation_processor_identifier(self, value: str):
        """
        Set the Task Creation Processor Identifier for the
        DynaFlow object.

        :param value: The Task Creation Processor Identifier value.
        :return: The updated
            DynaFlowBusObj instance.
        """

        self.task_creation_processor_identifier = value
        return self
    # completedUTCDateTime
    # dependencyDynaFlowID
    # description
    # DynaFlowTypeID

    def set_prop_dyna_flow_type_id(self, value: int):
        """
        Sets the value of the
        'dyna_flow_type_id' property.

        Args:
            value (int): The value to set for the
                'dyna_flow_type_id' property.

        Returns:
            self: The current instance of the class.

        """
        self.dyna_flow_type_id = value
        return self
    # isBuildTaskDebugRequired
    # isCanceled
    # isCancelRequested
    # isCompleted
    # isPaused
    # isResubmitted
    # isRunTaskDebugRequired
    # isStarted
    # isSuccessful
    # isTaskCreationStarted
    # isTasksCreated
    # minStartUTCDateTime
    # PacID

    def set_prop_pac_id(self, value: int):
        """
        Set the pac ID for the
        dyna_flow.

        Args:
            value (int): The pac id value.

        Returns:
            DynaFlow: The updated
                DynaFlow object.
        """

        self.pac_id = value
        return self
    # param1
    # parentDynaFlowID
    # priorityLevel
    # requestedUTCDateTime
    # resultValue
    # rootDynaFlowID
    # startedUTCDateTime
    # subjectCode
    # taskCreationProcessorIdentifier
