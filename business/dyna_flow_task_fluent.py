# business/dyna_flow_task_fluent.py
# pylint: disable=unused-import

"""
This module contains the
DynaFlowTaskFluentBusObj class,
which adds fluent properties
to the business object for a
DynaFlowTask.
"""

from decimal import Decimal  # noqa: F401
import uuid  # noqa: F401
from datetime import datetime, date  # noqa: F401
from .dyna_flow_task_base import DynaFlowTaskBaseBusObj


class DynaFlowTaskFluentBusObj(DynaFlowTaskBaseBusObj):
    """
    This class add fluent properties to the
    Base DynaFlowTask Business Object
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
    # dependencyDynaFlowTaskID

    def set_prop_dependency_dyna_flow_task_id(self, value: int):
        """
        Set the value of
        dependency_dyna_flow_task_id property.

        Args:
            value (int): The value to set for
                dependency_dyna_flow_task_id.

        Returns:
            self: Returns the instance of the class.

        """
        self.dependency_dyna_flow_task_id = value
        return self
    # description

    def set_prop_description(self, value: str):
        """
        Set the Description for the
        DynaFlowTask object.

        :param value: The Description value.
        :return: The updated
            DynaFlowTaskBusObj instance.
        """

        self.description = value
        return self
    # DynaFlowID
    # dynaFlowSubjectCode

    def set_prop_dyna_flow_subject_code(self, value: uuid.UUID):
        """
        Set the value of the
        'dyna_flow_subject_code' property.

        Args:
            value (uuid.UUID): The value to set.

        Returns:
            self: The current instance of the class.
        """
        self.dyna_flow_subject_code = value
        return self
    # DynaFlowTaskTypeID
    # isCanceled

    def set_prop_is_canceled(self, value: bool):
        """
        Set the Is Canceled flag for the
        DynaFlowTask object.

        :param value: The Is Canceled flag value.
        :return: The updated
            DynaFlowTaskBusObj instance.
        """

        self.is_canceled = value
        return self
    # isCancelRequested

    def set_prop_is_cancel_requested(self, value: bool):
        """
        Set the Is Cancel Requested flag for the
        DynaFlowTask object.

        :param value: The Is Cancel Requested flag value.
        :return: The updated
            DynaFlowTaskBusObj instance.
        """

        self.is_cancel_requested = value
        return self
    # isCompleted

    def set_prop_is_completed(self, value: bool):
        """
        Set the Is Completed flag for the
        DynaFlowTask object.

        :param value: The Is Completed flag value.
        :return: The updated
            DynaFlowTaskBusObj instance.
        """

        self.is_completed = value
        return self
    # isParallelRunAllowed

    def set_prop_is_parallel_run_allowed(self, value: bool):
        """
        Set the Is Parallel Run Allowed flag for the
        DynaFlowTask object.

        :param value: The Is Parallel Run Allowed flag value.
        :return: The updated
            DynaFlowTaskBusObj instance.
        """

        self.is_parallel_run_allowed = value
        return self
    # isRunTaskDebugRequired

    def set_prop_is_run_task_debug_required(self, value: bool):
        """
        Set the Is Run Task Debug Required flag for the
        DynaFlowTask object.

        :param value: The Is Run Task Debug Required flag value.
        :return: The updated
            DynaFlowTaskBusObj instance.
        """

        self.is_run_task_debug_required = value
        return self
    # isStarted

    def set_prop_is_started(self, value: bool):
        """
        Set the Is Started flag for the
        DynaFlowTask object.

        :param value: The Is Started flag value.
        :return: The updated
            DynaFlowTaskBusObj instance.
        """

        self.is_started = value
        return self
    # isSuccessful

    def set_prop_is_successful(self, value: bool):
        """
        Set the Is Successful flag for the
        DynaFlowTask object.

        :param value: The Is Successful flag value.
        :return: The updated
            DynaFlowTaskBusObj instance.
        """

        self.is_successful = value
        return self
    # maxRetryCount

    def set_prop_max_retry_count(self, value: int):
        """
        Set the value of
        max_retry_count property.

        Args:
            value (int): The value to set for
                max_retry_count.

        Returns:
            self: Returns the instance of the class.

        """
        self.max_retry_count = value
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
    # param1

    def set_prop_param_1(self, value: str):
        """
        Set the Param 1 for the
        DynaFlowTask object.

        :param value: The Param 1 value.
        :return: The updated
            DynaFlowTaskBusObj instance.
        """

        self.param_1 = value
        return self
    # param2

    def set_prop_param_2(self, value: str):
        """
        Set the Param 2 for the
        DynaFlowTask object.

        :param value: The Param 2 value.
        :return: The updated
            DynaFlowTaskBusObj instance.
        """

        self.param_2 = value
        return self
    # processorIdentifier

    def set_prop_processor_identifier(self, value: str):
        """
        Set the Processor Identifier for the
        DynaFlowTask object.

        :param value: The Processor Identifier value.
        :return: The updated
            DynaFlowTaskBusObj instance.
        """

        self.processor_identifier = value
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
        Set the ResultValue for the
        DynaFlowTask object.

        :param value: The ResultValue value.
        :return: The updated
            DynaFlowTaskBusObj instance.
        """

        self.result_value = value
        return self
    # retryCount

    def set_prop_retry_count(self, value: int):
        """
        Set the value of
        retry_count property.

        Args:
            value (int): The value to set for
                retry_count.

        Returns:
            self: Returns the instance of the class.

        """
        self.retry_count = value
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
    # completedUTCDateTime
    # dependencyDynaFlowTaskID,
    # description,
    # DynaFlowID

    def set_prop_dyna_flow_id(self, value: int):
        """
        Set the dyna_flow ID for the
        dyna_flow_task.

        Args:
            value (int): The dyna_flow id value.

        Returns:
            DynaFlowTask: The updated
                DynaFlowTask object.
        """

        self.dyna_flow_id = value
        return self
    # dynaFlowSubjectCode,
    # DynaFlowTaskTypeID

    def set_prop_dyna_flow_task_type_id(self, value: int):
        """
        Sets the value of the
        'dyna_flow_task_type_id' property.

        Args:
            value (int): The value to set for the
                'dyna_flow_task_type_id' property.

        Returns:
            self: The current instance of the class.

        """
        self.dyna_flow_task_type_id = value
        return self
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
