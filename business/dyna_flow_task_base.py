# business/dyna_flow_task_base.py
# pylint: disable=unused-import

"""
This module contains the
DynaFlowTaskBaseBusObj class,
which represents the base
business object for a
DynaFlowTask.
"""

from decimal import Decimal  # noqa: F401
import random
from typing import Optional
import uuid  # noqa: F401
from datetime import datetime, date  # noqa: F401
from helpers.session_context import SessionContext
from managers import DynaFlowTaskManager
from models import DynaFlowTask
import models
import managers as managers_and_enums
from .base_bus_obj import BaseBusObj

NOT_INITIALIZED_ERROR_MESSAGE = (
    "DynaFlowTask object is not initialized")


class DynaFlowTaskInvalidInitError(Exception):
    """
    Exception raised when the
    DynaFlowTask object
    is not initialized properly.
    """


class DynaFlowTaskBaseBusObj(BaseBusObj):
    """
    This class represents the base business object
    for a DynaFlowTask.
    It requires a valid session context for initialization.
    """

    def __init__(
        self,
        session_context: SessionContext,
        dyna_flow_task: Optional[DynaFlowTask] = None
    ):
        """
        Initializes a new instance of the
        DynaFlowTaskBusObj class.

        :param session_context: The session context.
        :raises ValueError: If the session is not provided.
        """

        if not session_context.session:
            raise ValueError("session required")

        if dyna_flow_task is None:
            dyna_flow_task = DynaFlowTask()

        self._session_context = session_context

        self.dyna_flow_task = dyna_flow_task

    @property
    def dyna_flow_task_id(self) -> int:
        """
        Get the dyna_flow_task ID from the
        DynaFlowTask object.

        :return: The dyna_flow_task ID.
        :raises AttributeError: If the
            DynaFlowTask object is not initialized.
        """

        if not self.dyna_flow_task:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.dyna_flow_task.dyna_flow_task_id
    # code

    @property
    def code(self):
        """
        Get the code from the
        DynaFlowTask object.

        :return: The code.
        :raises AttributeError: If the
            DynaFlowTask object is not initialized.
        """

        if not self.dyna_flow_task:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.dyna_flow_task.code

    @code.setter
    def code(self, value: uuid.UUID):  # type: ignore
        """
        Set the code for the DynaFlowTask object.

        :param value: The code value.
        :raises AttributeError: If the
            DynaFlowTask object is not initialized.
        :raises ValueError: If the code is not a UUID.
        """

        if not self.dyna_flow_task:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        if not isinstance(value, uuid.UUID):
            raise ValueError("code must be a UUID.")

        self.dyna_flow_task.code = value
    # last_change_code

    @property
    def last_change_code(self):
        """
        Get the last change code from the
        DynaFlowTask object.

        :return: The last change code.
        :raises AttributeError: If the
            DynaFlowTask object is not initialized.
        """

        if not self.dyna_flow_task:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.dyna_flow_task.last_change_code

    @last_change_code.setter
    def last_change_code(self, value: int):
        """
        Set the last change code for the
        DynaFlowTask object.

        :param value: The last change code value.
        :raises AttributeError: If the
            DynaFlowTask object is not initialized.
        :raises ValueError: If the last change code is not an integer.
        """

        if not self.dyna_flow_task:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        if not isinstance(value, int):
            raise ValueError("last_change_code must be an integer.")

        self.dyna_flow_task.last_change_code = value
    # insert_user_id

    @property
    def insert_user_id(self):
        """
        Get the insert user ID from the
        DynaFlowTask object.

        :return: The insert user ID.
        :raises AttributeError: If the
            DynaFlowTask object is not initialized.
        """

        if not self.dyna_flow_task:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.dyna_flow_task.insert_user_id

    @insert_user_id.setter
    def insert_user_id(self, value: uuid.UUID):
        """
        Set the insert user ID for the
        DynaFlowTask object.

        :param value: The insert user ID value.
        :raises AttributeError: If the
            DynaFlowTask object is not initialized.
        :raises ValueError: If the insert user ID is not a UUID.
        """

        if not self.dyna_flow_task:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        if not isinstance(value, uuid.UUID):
            raise ValueError(
                "insert_user_id must be a UUID.")

        self.dyna_flow_task.insert_user_id = value
    # last_update_user_id

    @property
    def last_update_user_id(self):
        """
        Get the last update user ID from the
        DynaFlowTask object.

        :return: The last update user ID.
        :raises AttributeError: If the
            DynaFlowTask object is not initialized.
        """

        if not self.dyna_flow_task:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.dyna_flow_task.last_update_user_id

    @last_update_user_id.setter
    def last_update_user_id(self, value: uuid.UUID):
        """
        Set the last update user ID for the
        DynaFlowTask object.

        :param value: The last update user ID value.
        :raises AttributeError: If the
            DynaFlowTask object is not initialized.
        :raises ValueError: If the last update user ID is not a UUID.
        """

        if not self.dyna_flow_task:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        if not isinstance(value, uuid.UUID):
            raise ValueError(
                "last_update_user_id must be a UUID.")

        self.dyna_flow_task.last_update_user_id = value

    # completedUTCDateTime

    @property
    def completed_utc_date_time(self):
        """
        Returns the value of
        completed_utc_date_time attribute of the
        dyna_flow_task.

        Raises:
            AttributeError: If the
                dyna_flow_task is not initialized.

        Returns:
            The value of
            completed_utc_date_time
            attribute.
        """
        if not self.dyna_flow_task:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.dyna_flow_task.completed_utc_date_time

    @completed_utc_date_time.setter
    def completed_utc_date_time(self, value):
        """
        Sets the value of
        completed_utc_date_time attribute
        for the dyna_flow_task.

        Args:
            value (datetime): The datetime value to be set.

        Raises:
            AttributeError: If the
                dyna_flow_task is not initialized.

        """
        if not self.dyna_flow_task:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        assert isinstance(value, datetime), (
            "completed_utc_date_time "
            "must be a datetime object")
        self.dyna_flow_task.completed_utc_date_time = value
    # dependencyDynaFlowTaskID

    @property
    def dependency_dyna_flow_task_id(self):
        """
        Returns the value of
        dependency_dyna_flow_task_id attribute of the
        dyna_flow_task.

        Raises:
            AttributeError: If the
                dyna_flow_task is not initialized.

        Returns:
            int: The value of
                dependency_dyna_flow_task_id attribute.
        """
        if not self.dyna_flow_task:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.dyna_flow_task.dependency_dyna_flow_task_id

    @dependency_dyna_flow_task_id.setter
    def dependency_dyna_flow_task_id(self, value):
        """
        Sets the value of
        dependency_dyna_flow_task_id for the
        dyna_flow_task.

        Args:
            value (int): The integer value to set for
                dependency_dyna_flow_task_id.

        Raises:
            AttributeError: If the
                dyna_flow_task is not initialized.

        """
        if not self.dyna_flow_task:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        assert isinstance(value, int), (
            "dependency_dyna_flow_task_id must be an integer")
        self.dyna_flow_task.dependency_dyna_flow_task_id = value
    # description

    @property
    def description(self):
        """
        Get the Description from the
        DynaFlowTask object.

        :return: The Description.
        :raises AttributeError: If the
            DynaFlowTask object is not initialized.
        """

        if not self.dyna_flow_task:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        if self.dyna_flow_task.description is None:
            return ""

        return self.dyna_flow_task.description

    @description.setter
    def description(self, value):
        """
        Set the Description for the
        DynaFlowTask object.

        :param value: The Description value.
        :raises AttributeError: If the
            DynaFlowTask object is not initialized.
        :raises AssertionError: If the Description is not a string.
        """

        if not self.dyna_flow_task:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        assert isinstance(value, str), "description must be a string"
        self.dyna_flow_task.description = value
    # DynaFlowID
    # dynaFlowSubjectCode

    @property
    def dyna_flow_subject_code(self):
        """
        Returns the value of the
        some unique identifier for the
        dyna_flow_task.

        Raises:
            AttributeError: If the
                dyna_flow_task is not initialized.

        Returns:
            The value of the some unique identifier for the
            dyna_flow_task.
        """
        if not self.dyna_flow_task:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.dyna_flow_task.dyna_flow_subject_code

    @dyna_flow_subject_code.setter
    def dyna_flow_subject_code(self, value):
        """
        Sets the value of the
        'dyna_flow_subject_code'
        attribute for the
        dyna_flow_task.

        Args:
            value (uuid.UUID): The UUID value to set for
                'dyna_flow_subject_code'.

        Raises:
            AttributeError: If the
                dyna_flow_task is not initialized.

        """
        if not self.dyna_flow_task:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        assert isinstance(value, uuid.UUID), (
            "dyna_flow_subject_code must be a UUID")
        self.dyna_flow_task.dyna_flow_subject_code = value
    # DynaFlowTaskTypeID
    # isCanceled

    @property
    def is_canceled(self):
        """
        Get the Is Canceled flag from the
        DynaFlowTask object.

        :return: The Is Canceled flag.
        :raises AttributeError: If the
            DynaFlowTask object is not initialized.
        """

        if not self.dyna_flow_task:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.dyna_flow_task.is_canceled

    @is_canceled.setter
    def is_canceled(self, value: bool):
        """
        Set the Is Canceled flag for the
        DynaFlowTask object.

        :param value: The Is Canceled flag value.
        :raises AttributeError: If the
            DynaFlowTask object is not initialized.
        :raises ValueError: If the Is Canceled flag is not a boolean.
        """

        if not self.dyna_flow_task:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        if not isinstance(value, bool):
            raise ValueError(
                "is_canceled must be a boolean.")

        self.dyna_flow_task.is_canceled = value
    # isCancelRequested

    @property
    def is_cancel_requested(self):
        """
        Get the Is Cancel Requested flag from the
        DynaFlowTask object.

        :return: The Is Cancel Requested flag.
        :raises AttributeError: If the
            DynaFlowTask object is not initialized.
        """

        if not self.dyna_flow_task:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.dyna_flow_task.is_cancel_requested

    @is_cancel_requested.setter
    def is_cancel_requested(self, value: bool):
        """
        Set the Is Cancel Requested flag for the
        DynaFlowTask object.

        :param value: The Is Cancel Requested flag value.
        :raises AttributeError: If the
            DynaFlowTask object is not initialized.
        :raises ValueError: If the Is Cancel Requested flag is not a boolean.
        """

        if not self.dyna_flow_task:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        if not isinstance(value, bool):
            raise ValueError(
                "is_cancel_requested must be a boolean.")

        self.dyna_flow_task.is_cancel_requested = value
    # isCompleted

    @property
    def is_completed(self):
        """
        Get the Is Completed flag from the
        DynaFlowTask object.

        :return: The Is Completed flag.
        :raises AttributeError: If the
            DynaFlowTask object is not initialized.
        """

        if not self.dyna_flow_task:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.dyna_flow_task.is_completed

    @is_completed.setter
    def is_completed(self, value: bool):
        """
        Set the Is Completed flag for the
        DynaFlowTask object.

        :param value: The Is Completed flag value.
        :raises AttributeError: If the
            DynaFlowTask object is not initialized.
        :raises ValueError: If the Is Completed flag is not a boolean.
        """

        if not self.dyna_flow_task:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        if not isinstance(value, bool):
            raise ValueError(
                "is_completed must be a boolean.")

        self.dyna_flow_task.is_completed = value
    # isParallelRunAllowed

    @property
    def is_parallel_run_allowed(self):
        """
        Get the Is Parallel Run Allowed flag from the
        DynaFlowTask object.

        :return: The Is Parallel Run Allowed flag.
        :raises AttributeError: If the
            DynaFlowTask object is not initialized.
        """

        if not self.dyna_flow_task:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.dyna_flow_task.is_parallel_run_allowed

    @is_parallel_run_allowed.setter
    def is_parallel_run_allowed(self, value: bool):
        """
        Set the Is Parallel Run Allowed flag for the
        DynaFlowTask object.

        :param value: The Is Parallel Run Allowed flag value.
        :raises AttributeError: If the
            DynaFlowTask object is not initialized.
        :raises ValueError: If the Is Parallel Run Allowed flag is not a boolean.
        """

        if not self.dyna_flow_task:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        if not isinstance(value, bool):
            raise ValueError(
                "is_parallel_run_allowed must be a boolean.")

        self.dyna_flow_task.is_parallel_run_allowed = value
    # isRunTaskDebugRequired

    @property
    def is_run_task_debug_required(self):
        """
        Get the Is Run Task Debug Required flag from the
        DynaFlowTask object.

        :return: The Is Run Task Debug Required flag.
        :raises AttributeError: If the
            DynaFlowTask object is not initialized.
        """

        if not self.dyna_flow_task:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.dyna_flow_task.is_run_task_debug_required

    @is_run_task_debug_required.setter
    def is_run_task_debug_required(self, value: bool):
        """
        Set the Is Run Task Debug Required flag for the
        DynaFlowTask object.

        :param value: The Is Run Task Debug Required flag value.
        :raises AttributeError: If the
            DynaFlowTask object is not initialized.
        :raises ValueError: If the Is Run Task Debug Required flag is not a boolean.
        """

        if not self.dyna_flow_task:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        if not isinstance(value, bool):
            raise ValueError(
                "is_run_task_debug_required must be a boolean.")

        self.dyna_flow_task.is_run_task_debug_required = value
    # isStarted

    @property
    def is_started(self):
        """
        Get the Is Started flag from the
        DynaFlowTask object.

        :return: The Is Started flag.
        :raises AttributeError: If the
            DynaFlowTask object is not initialized.
        """

        if not self.dyna_flow_task:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.dyna_flow_task.is_started

    @is_started.setter
    def is_started(self, value: bool):
        """
        Set the Is Started flag for the
        DynaFlowTask object.

        :param value: The Is Started flag value.
        :raises AttributeError: If the
            DynaFlowTask object is not initialized.
        :raises ValueError: If the Is Started flag is not a boolean.
        """

        if not self.dyna_flow_task:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        if not isinstance(value, bool):
            raise ValueError(
                "is_started must be a boolean.")

        self.dyna_flow_task.is_started = value
    # isSuccessful

    @property
    def is_successful(self):
        """
        Get the Is Successful flag from the
        DynaFlowTask object.

        :return: The Is Successful flag.
        :raises AttributeError: If the
            DynaFlowTask object is not initialized.
        """

        if not self.dyna_flow_task:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.dyna_flow_task.is_successful

    @is_successful.setter
    def is_successful(self, value: bool):
        """
        Set the Is Successful flag for the
        DynaFlowTask object.

        :param value: The Is Successful flag value.
        :raises AttributeError: If the
            DynaFlowTask object is not initialized.
        :raises ValueError: If the Is Successful flag is not a boolean.
        """

        if not self.dyna_flow_task:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        if not isinstance(value, bool):
            raise ValueError(
                "is_successful must be a boolean.")

        self.dyna_flow_task.is_successful = value
    # maxRetryCount

    @property
    def max_retry_count(self):
        """
        Returns the value of
        max_retry_count attribute of the
        dyna_flow_task.

        Raises:
            AttributeError: If the
                dyna_flow_task is not initialized.

        Returns:
            int: The value of
                max_retry_count attribute.
        """
        if not self.dyna_flow_task:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.dyna_flow_task.max_retry_count

    @max_retry_count.setter
    def max_retry_count(self, value):
        """
        Sets the value of
        max_retry_count for the
        dyna_flow_task.

        Args:
            value (int): The integer value to set for
                max_retry_count.

        Raises:
            AttributeError: If the
                dyna_flow_task is not initialized.

        """
        if not self.dyna_flow_task:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        assert isinstance(value, int), (
            "max_retry_count must be an integer")
        self.dyna_flow_task.max_retry_count = value
    # minStartUTCDateTime

    @property
    def min_start_utc_date_time(self):
        """
        Returns the value of
        min_start_utc_date_time attribute of the
        dyna_flow_task.

        Raises:
            AttributeError: If the
                dyna_flow_task is not initialized.

        Returns:
            The value of
            min_start_utc_date_time
            attribute.
        """
        if not self.dyna_flow_task:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.dyna_flow_task.min_start_utc_date_time

    @min_start_utc_date_time.setter
    def min_start_utc_date_time(self, value):
        """
        Sets the value of
        min_start_utc_date_time attribute
        for the dyna_flow_task.

        Args:
            value (datetime): The datetime value to be set.

        Raises:
            AttributeError: If the
                dyna_flow_task is not initialized.

        """
        if not self.dyna_flow_task:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        assert isinstance(value, datetime), (
            "min_start_utc_date_time "
            "must be a datetime object")
        self.dyna_flow_task.min_start_utc_date_time = value
    # param1

    @property
    def param_1(self):
        """
        Get the Param 1 from the
        DynaFlowTask object.

        :return: The Param 1.
        :raises AttributeError: If the
            DynaFlowTask object is not initialized.
        """

        if not self.dyna_flow_task:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        if self.dyna_flow_task.param_1 is None:
            return ""

        return self.dyna_flow_task.param_1

    @param_1.setter
    def param_1(self, value):
        """
        Set the Param 1 for the
        DynaFlowTask object.

        :param value: The Param 1 value.
        :raises AttributeError: If the
            DynaFlowTask object is not initialized.
        :raises AssertionError: If the Param 1 is not a string.
        """

        if not self.dyna_flow_task:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        assert isinstance(value, str), "param_1 must be a string"
        self.dyna_flow_task.param_1 = value
    # param2

    @property
    def param_2(self):
        """
        Get the Param 2 from the
        DynaFlowTask object.

        :return: The Param 2.
        :raises AttributeError: If the
            DynaFlowTask object is not initialized.
        """

        if not self.dyna_flow_task:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        if self.dyna_flow_task.param_2 is None:
            return ""

        return self.dyna_flow_task.param_2

    @param_2.setter
    def param_2(self, value):
        """
        Set the Param 2 for the
        DynaFlowTask object.

        :param value: The Param 2 value.
        :raises AttributeError: If the
            DynaFlowTask object is not initialized.
        :raises AssertionError: If the Param 2 is not a string.
        """

        if not self.dyna_flow_task:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        assert isinstance(value, str), "param_2 must be a string"
        self.dyna_flow_task.param_2 = value
    # processorIdentifier

    @property
    def processor_identifier(self):
        """
        Get the Processor Identifier from the
        DynaFlowTask object.

        :return: The Processor Identifier.
        :raises AttributeError: If the
            DynaFlowTask object is not initialized.
        """

        if not self.dyna_flow_task:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        if self.dyna_flow_task.processor_identifier is None:
            return ""

        return self.dyna_flow_task.processor_identifier

    @processor_identifier.setter
    def processor_identifier(self, value):
        """
        Set the Processor Identifier for the
        DynaFlowTask object.

        :param value: The Processor Identifier value.
        :raises AttributeError: If the
            DynaFlowTask object is not initialized.
        :raises AssertionError: If the Processor Identifier is not a string.
        """

        if not self.dyna_flow_task:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        assert isinstance(value, str), "processor_identifier must be a string"
        self.dyna_flow_task.processor_identifier = value
    # requestedUTCDateTime

    @property
    def requested_utc_date_time(self):
        """
        Returns the value of
        requested_utc_date_time attribute of the
        dyna_flow_task.

        Raises:
            AttributeError: If the
                dyna_flow_task is not initialized.

        Returns:
            The value of
            requested_utc_date_time
            attribute.
        """
        if not self.dyna_flow_task:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.dyna_flow_task.requested_utc_date_time

    @requested_utc_date_time.setter
    def requested_utc_date_time(self, value):
        """
        Sets the value of
        requested_utc_date_time attribute
        for the dyna_flow_task.

        Args:
            value (datetime): The datetime value to be set.

        Raises:
            AttributeError: If the
                dyna_flow_task is not initialized.

        """
        if not self.dyna_flow_task:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        assert isinstance(value, datetime), (
            "requested_utc_date_time "
            "must be a datetime object")
        self.dyna_flow_task.requested_utc_date_time = value
    # resultValue

    @property
    def result_value(self):
        """
        Get the ResultValue from the
        DynaFlowTask object.

        :return: The ResultValue.
        :raises AttributeError: If the
            DynaFlowTask object is not initialized.
        """

        if not self.dyna_flow_task:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        if self.dyna_flow_task.result_value is None:
            return ""

        return self.dyna_flow_task.result_value

    @result_value.setter
    def result_value(self, value):
        """
        Set the ResultValue for the
        DynaFlowTask object.

        :param value: The ResultValue value.
        :raises AttributeError: If the
            DynaFlowTask object is not initialized.
        :raises AssertionError: If the ResultValue is not a string.
        """

        if not self.dyna_flow_task:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        assert isinstance(value, str), "result_value must be a string"
        self.dyna_flow_task.result_value = value
    # retryCount

    @property
    def retry_count(self):
        """
        Returns the value of
        retry_count attribute of the
        dyna_flow_task.

        Raises:
            AttributeError: If the
                dyna_flow_task is not initialized.

        Returns:
            int: The value of
                retry_count attribute.
        """
        if not self.dyna_flow_task:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.dyna_flow_task.retry_count

    @retry_count.setter
    def retry_count(self, value):
        """
        Sets the value of
        retry_count for the
        dyna_flow_task.

        Args:
            value (int): The integer value to set for
                retry_count.

        Raises:
            AttributeError: If the
                dyna_flow_task is not initialized.

        """
        if not self.dyna_flow_task:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        assert isinstance(value, int), (
            "retry_count must be an integer")
        self.dyna_flow_task.retry_count = value
    # startedUTCDateTime

    @property
    def started_utc_date_time(self):
        """
        Returns the value of
        started_utc_date_time attribute of the
        dyna_flow_task.

        Raises:
            AttributeError: If the
                dyna_flow_task is not initialized.

        Returns:
            The value of
            started_utc_date_time
            attribute.
        """
        if not self.dyna_flow_task:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.dyna_flow_task.started_utc_date_time

    @started_utc_date_time.setter
    def started_utc_date_time(self, value):
        """
        Sets the value of
        started_utc_date_time attribute
        for the dyna_flow_task.

        Args:
            value (datetime): The datetime value to be set.

        Raises:
            AttributeError: If the
                dyna_flow_task is not initialized.

        """
        if not self.dyna_flow_task:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        assert isinstance(value, datetime), (
            "started_utc_date_time "
            "must be a datetime object")
        self.dyna_flow_task.started_utc_date_time = value
    # isDeleteAllowed,
    # isEditAllowed,
    # otherFlavor,
    # someBigIntVal,
    # someBitVal,
    # someDecimalVal,
    # someEmailAddress,
    # someFloatVal,
    # someIntVal,
    # someMoneyVal,
    # someNVarCharVal,
    # someDateVal
    # someUTCDateTimeVal
    # DynaFlowID
    # DynaFlowTaskTypeID

    @property
    def dyna_flow_task_type_id(self):
        """
        Returns the dyna_flow_task_type_id
        of the dyna_flow_task_type
        associated with the
        dyna_flow_task.

        Raises:
            AttributeError: If the
            dyna_flow_task is not initialized.

        Returns:
            int: The foreign key ID of the dyna_flow_task_type.
        """
        if not self.dyna_flow_task:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.dyna_flow_task.dyna_flow_task_type_id

    @dyna_flow_task_type_id.setter
    def dyna_flow_task_type_id(self, value: int):
        """
        Sets the foreign key ID for the
        dyna_flow_task_type of the
        dyna_flow_task.

        Args:
            value (int): The foreign key ID to set.

        Raises:
            AttributeError: If the
                dyna_flow_task is not initialized.
            ValueError: If the value is not an integer.
        """

        if not self.dyna_flow_task:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        if not isinstance(value, int):
            raise ValueError("dyna_flow_task_type_id must be an integer.")

        self.dyna_flow_task.dyna_flow_task_type_id = value

    @property
    def dyna_flow_task_type_code_peek(self) -> uuid.UUID:
        """
        Returns the dyna_flow_task_type_id code peek
        of the dyna_flow_task.

        Raises:
            AttributeError: If the dyna_flow_task
                is not initialized.

        Returns:
            uuid.UUID: The flvr foreign key code peek
            of the dyna_flow_task.
        """
        if not self.dyna_flow_task:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.dyna_flow_task.dyna_flow_task_type_code_peek
    @property
    def dyna_flow_id(self):
        """
        Returns the dyna_flow ID
        associated with the
        dyna_flow_task.

        Raises:
            AttributeError: If the
                dyna_flow_task is not initialized.

        Returns:
            int: The dyna_flow ID of the dyna_flow_task.
        """
        if not self.dyna_flow_task:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.dyna_flow_task.dyna_flow_id

    @dyna_flow_id.setter
    def dyna_flow_id(self, value):
        """
        Sets the dyna_flow ID
        for the dyna_flow_task.

        Args:
            value (int or None): The
                dyna_flow ID to be set.
                Must be an integer or None.

        Raises:
            AttributeError: If the
                dyna_flow_task is not initialized.

        """
        if not self.dyna_flow_task:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        assert isinstance(value, int) or value is None, (
            "dyna_flow_id must be an integer or None")

        self.dyna_flow_task.dyna_flow_id = value

    @property
    def dyna_flow_code_peek(self) -> uuid.UUID:
        """
        Returns the dyna_flow id code peek
        of the dyna_flow_task.

        Raises:
            AttributeError: If the
            dyna_flow_task is not initialized.

        Returns:
            uuid.UUID: The dyna_flow id code peek
            of the dyna_flow_task.
        """
        if not self.dyna_flow_task:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.dyna_flow_task.dyna_flow_code_peek
    # insert_utc_date_time

    @property
    def insert_utc_date_time(self):
        """
        Inserts the UTC date and time into
        the dyna_flow_task object.

        Raises:
            AttributeError: If the
                dyna_flow_task object is not initialized.

        Returns:
            The UTC date and time inserted into the
            dyna_flow_task object.
        """
        if not self.dyna_flow_task:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.dyna_flow_task.insert_utc_date_time

    @insert_utc_date_time.setter
    def insert_utc_date_time(self, value):
        """
        Inserts the UTC date and time for the
        dyna_flow_task.

        Args:
            value (datetime): The UTC date and time to be inserted.
                It should be a datetime object or None.

        Raises:
            AttributeError: If the
                dyna_flow_task is not initialized.

        """
        if not self.dyna_flow_task:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        assert isinstance(value, datetime) or value is None, (
            "insert_utc_date_time must be "
            "a datetime object or None")

        self.dyna_flow_task.insert_utc_date_time = value

    # update_utc_date_time
    @property
    def last_update_utc_date_time(self):
        """
        Returns the last update UTC date and time
        of the dyna_flow_task.

        Raises:
            AttributeError: If the
                dyna_flow_task is not initialized.

        Returns:
            datetime: The last update UTC date and time
                of the dyna_flow_task.
        """
        if not self.dyna_flow_task:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.dyna_flow_task.last_update_utc_date_time

    @last_update_utc_date_time.setter
    def last_update_utc_date_time(self, value):
        """
        Sets the last update UTC date and time
        for the dyna_flow_task.

        Args:
            value (datetime): The datetime object
                representing the last update UTC date and time.
                Pass None to unset the value.

        Raises:
            AttributeError: If the
                dyna_flow_task is not initialized.

        """
        if not self.dyna_flow_task:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        assert isinstance(value, datetime) or value is None, (
            "last_update_utc_date_time "
            "must be a datetime object or None")

        self.dyna_flow_task.last_update_utc_date_time = value

    async def load_from_json(
        self,
        json_data: str
    ):
        """
        Load dyna_flow_task data
        from JSON string.

        :param json_data: JSON string containing
            dyna_flow_task data.
        :raises ValueError: If json_data is not a string
            or if no dyna_flow_task
            data is found.
        """

        if not isinstance(json_data, str):
            raise ValueError(
                "json_data must be a string")

        dyna_flow_task_manager = DynaFlowTaskManager(
            self._session_context)
        self.dyna_flow_task = await \
            dyna_flow_task_manager.from_json(json_data)

        return self

    async def load_from_code(
        self,
        code: uuid.UUID
    ):
        """
        Load dyna_flow_task
        data from UUID code.

        :param code: UUID code for loading a specific
            dyna_flow_task.
        :raises ValueError: If code is not a UUID or if no
            dyna_flow_task data is found.
        """
        if not isinstance(code, uuid.UUID):
            raise ValueError(
                "code must be a UUID")

        dyna_flow_task_manager = DynaFlowTaskManager(
            self._session_context)
        dyna_flow_task_obj = await dyna_flow_task_manager.get_by_code(
            code)
        self.dyna_flow_task = dyna_flow_task_obj

        return self

    async def load_from_id(
        self,
        dyna_flow_task_id: int
    ):
        """
        Load dyna_flow_task data from
        dyna_flow_task ID.

        :param dyna_flow_task_id: Integer ID for loading a specific
            dyna_flow_task.
        :raises ValueError: If dyna_flow_task_id
            is not an integer or
            if no dyna_flow_task
            data is found.
        """

        if not isinstance(dyna_flow_task_id, int):
            raise ValueError(
                "dyna_flow_task_id must be an integer")

        dyna_flow_task_manager = DynaFlowTaskManager(
            self._session_context)
        dyna_flow_task_obj = await dyna_flow_task_manager.get_by_id(
            dyna_flow_task_id)
        self.dyna_flow_task = dyna_flow_task_obj

        return self

    def load_from_obj_instance(
        self,
        dyna_flow_task_obj_instance: DynaFlowTask
    ):
        """
        Use the provided
        DynaFlowTask instance.

        :param dyna_flow_task_obj_instance: Instance of the
            DynaFlowTask class.
        :raises ValueError: If dyna_flow_task_obj_instance
            is not an instance of
            DynaFlowTask.
        """

        if not isinstance(dyna_flow_task_obj_instance,
                          DynaFlowTask):
            raise ValueError(
                "dyna_flow_task_obj_instance must be an "
                "instance of DynaFlowTask")

        self.dyna_flow_task = dyna_flow_task_obj_instance

        return self

    async def load_from_dict(
        self,
        dyna_flow_task_dict: dict
    ):
        """
        Load dyna_flow_task data
        from dictionary.

        :param dyna_flow_task_dict: Dictionary containing
            dyna_flow_task data.
        :raises ValueError: If dyna_flow_task_dict
            is not a
            dictionary or if no
            dyna_flow_task data is found.
        """
        if not isinstance(dyna_flow_task_dict, dict):
            raise ValueError(
                "dyna_flow_task_dict must be a dictionary")

        dyna_flow_task_manager = DynaFlowTaskManager(
            self._session_context)

        self.dyna_flow_task = await \
            dyna_flow_task_manager.from_dict(
                dyna_flow_task_dict)

        return self

    def get_session_context(self):
        """
        Returns the session context.

        :return: The session context.
        :rtype: SessionContext
        """
        return self._session_context

    async def refresh(self):
        """
        Refreshes the dyna_flow_task
        object by fetching
        the latest data from the database.

        Returns:
            The updated
            dyna_flow_task object.
        """
        dyna_flow_task_manager = DynaFlowTaskManager(
            self._session_context)
        self.dyna_flow_task = await \
            dyna_flow_task_manager.refresh(
                self.dyna_flow_task)

        return self

    def is_valid(self):
        """
        Check if the dyna_flow_task
        is valid.

        Returns:
            bool: True if the dyna_flow_task
                is valid, False otherwise.
        """
        return self.dyna_flow_task is not None

    def to_dict(self):
        """
        Converts the DynaFlowTask
        object to a dictionary representation.

        Returns:
            dict: A dictionary representation of the
                DynaFlowTask object.
        """
        dyna_flow_task_manager = DynaFlowTaskManager(
            self._session_context)
        return dyna_flow_task_manager.to_dict(
            self.dyna_flow_task)

    def to_json(self):
        """
        Converts the dyna_flow_task
        object to a JSON representation.

        Returns:
            str: The JSON representation of the
                dyna_flow_task object.
        """
        dyna_flow_task_manager = DynaFlowTaskManager(
            self._session_context)
        return dyna_flow_task_manager.to_json(
            self.dyna_flow_task)

    async def save(self):
        """
        Saves the dyna_flow_task object
        to the database.

        If the dyna_flow_task object
        is not initialized, an AttributeError is raised.
        If the dyna_flow_task_id
        is greater than 0, the
        dyna_flow_task is
        updated in the database.
        If the dyna_flow_task_id is 0,
        the dyna_flow_task is
        added to the database.

        Returns:
            The updated or added
            dyna_flow_task object.

        Raises:
            AttributeError: If the dyna_flow_task
            object is not initialized.
        """
        if not self.dyna_flow_task:
            raise AttributeError(NOT_INITIALIZED_ERROR_MESSAGE)

        dyna_flow_task_id = self.dyna_flow_task.dyna_flow_task_id

        if dyna_flow_task_id > 0:
            dyna_flow_task_manager = DynaFlowTaskManager(
                self._session_context)
            self.dyna_flow_task = await \
                dyna_flow_task_manager.update(
                    self.dyna_flow_task)

        if dyna_flow_task_id == 0:
            dyna_flow_task_manager = DynaFlowTaskManager(
                self._session_context)
            self.dyna_flow_task = await \
                dyna_flow_task_manager.add(
                    self.dyna_flow_task)

        return self

    async def delete(self):
        """
        Deletes the dyna_flow_task
        from the database.

        Raises:
            AttributeError: If the dyna_flow_task
                is not initialized.
        """
        if not self.dyna_flow_task:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        if self.dyna_flow_task.dyna_flow_task_id > 0:
            dyna_flow_task_manager = DynaFlowTaskManager(
                self._session_context)
            await dyna_flow_task_manager.delete(
                self.dyna_flow_task.dyna_flow_task_id)
            self.dyna_flow_task = None

    async def randomize_properties(self):
        """
        Randomizes the properties of the
        dyna_flow_task object.

        This method generates random values for various
        properties of the dyna_flow_task
        object

        Returns:
            self: The current instance of the
                DynaFlowTask class.

        Raises:
            AttributeError: If the dyna_flow_task
                object is not initialized.
        """
        if not self.dyna_flow_task:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        self.dyna_flow_task.completed_utc_date_time = datetime(
            random.randint(2000, 2023),
            random.randint(1, 12),
            random.randint(1, 28))
        self.dyna_flow_task.dependency_dyna_flow_task_id = (
            random.randint(0, 100))
        self.dyna_flow_task.description = "".join(
            random.choices("abcdefghijklmnopqrstuvwxyz", k=10))
        # self.dyna_flow_task.dyna_flow_id = random.randint(0, 100)
        self.dyna_flow_task.dyna_flow_subject_code = uuid.uuid4()
        self.dyna_flow_task.dyna_flow_task_type_id = random.choice(
            await managers_and_enums.DynaFlowTaskTypeManager(
                self._session_context).get_list()).dyna_flow_task_type_id
        self.dyna_flow_task.is_canceled = (
            random.choice([True, False]))
        self.dyna_flow_task.is_cancel_requested = (
            random.choice([True, False]))
        self.dyna_flow_task.is_completed = (
            random.choice([True, False]))
        self.dyna_flow_task.is_parallel_run_allowed = (
            random.choice([True, False]))
        self.dyna_flow_task.is_run_task_debug_required = (
            random.choice([True, False]))
        self.dyna_flow_task.is_started = (
            random.choice([True, False]))
        self.dyna_flow_task.is_successful = (
            random.choice([True, False]))
        self.dyna_flow_task.max_retry_count = (
            random.randint(0, 100))
        self.dyna_flow_task.min_start_utc_date_time = datetime(
            random.randint(2000, 2023),
            random.randint(1, 12),
            random.randint(1, 28))
        self.dyna_flow_task.param_1 = "".join(
            random.choices("abcdefghijklmnopqrstuvwxyz", k=10))
        self.dyna_flow_task.param_2 = "".join(
            random.choices("abcdefghijklmnopqrstuvwxyz", k=10))
        self.dyna_flow_task.processor_identifier = "".join(
            random.choices("abcdefghijklmnopqrstuvwxyz", k=10))
        self.dyna_flow_task.requested_utc_date_time = datetime(
            random.randint(2000, 2023),
            random.randint(1, 12),
            random.randint(1, 28))
        self.dyna_flow_task.result_value = "".join(
            random.choices("abcdefghijklmnopqrstuvwxyz", k=10))
        self.dyna_flow_task.retry_count = (
            random.randint(0, 100))
        self.dyna_flow_task.started_utc_date_time = datetime(
            random.randint(2000, 2023),
            random.randint(1, 12),
            random.randint(1, 28))

        return self

    def get_dyna_flow_task_obj(self) -> DynaFlowTask:
        """
        Returns the dyna_flow_task
        object.

        Raises:
            AttributeError: If the dyna_flow_task
                object is not initialized.

        Returns:
            DynaFlowTask: The dyna_flow_task
                object.
        """
        if not self.dyna_flow_task:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.dyna_flow_task

    def is_equal(
        self,
        dyna_flow_task: DynaFlowTask
    ) -> bool:
        """
        Checks if the current dyna_flow_task
        is equal to the given dyna_flow_task.

        Args:
            dyna_flow_task (DynaFlowTask): The
                dyna_flow_task to compare with.

        Returns:
            bool: True if the dyna_flow_tasks
                are equal, False otherwise.
        """
        dyna_flow_task_manager = DynaFlowTaskManager(
            self._session_context)
        my_dyna_flow_task = self.get_dyna_flow_task_obj()
        return dyna_flow_task_manager.is_equal(
            dyna_flow_task, my_dyna_flow_task)

    def get_obj(self) -> DynaFlowTask:
        """
        Returns the DynaFlowTask object.

        :return: The DynaFlowTask object.
        :rtype: DynaFlowTask
        """

        return self.dyna_flow_task

    def get_object_name(self) -> str:
        """
        Returns the name of the object.

        :return: The name of the object.
        :rtype: str
        """
        return "dyna_flow_task"

    def get_id(self) -> int:
        """
        Returns the ID of the dyna_flow_task.

        :return: The ID of the dyna_flow_task.
        :rtype: int
        """
        return self.dyna_flow_task_id
    # completedUTCDateTime
    # dependencyDynaFlowTaskID,
    # description,
    # DynaFlowID

    async def get_parent_name(self) -> str:
        """
        Get the name of the parent dyna_flow_task.

        Returns:
            str: The name of the parent dyna_flow_task.
        """
        return 'DynaFlow'

    async def get_parent_code(self) -> uuid.UUID:
        """
        Get the parent code of the dyna_flow_task.

        Returns:
            The parent code of the dyna_flow_task
            as a UUID.
        """
        return self.dyna_flow_code_peek

    async def get_parent_obj(self) -> models.DynaFlow:
        """
        Get the parent object of the current
        dyna_flow_task.

        Returns:
            The parent object of the current
            dyna_flow_task,
            which is an instance of the
            DynaFlow model.
        """
        dyna_flow_manager = managers_and_enums.DynaFlowManager(
            self._session_context)
        dyna_flow_obj = await dyna_flow_manager.get_by_id(
            self.dyna_flow_id)
        return dyna_flow_obj
    # dynaFlowSubjectCode,
    # DynaFlowTaskTypeID
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
