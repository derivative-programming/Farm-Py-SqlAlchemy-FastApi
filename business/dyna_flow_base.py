# business/dyna_flow_base.py
# pylint: disable=unused-import

"""
This module contains the
DynaFlowBaseBusObj class,
which represents the base
business object for a
DynaFlow.
"""

from decimal import Decimal  # noqa: F401
import random
from typing import Optional
import uuid  # noqa: F401
from datetime import datetime, date  # noqa: F401
from helpers.session_context import SessionContext
from managers import DynaFlowManager
from models import DynaFlow
import models
import managers as managers_and_enums
from .base_bus_obj import BaseBusObj

NOT_INITIALIZED_ERROR_MESSAGE = (
    "DynaFlow object is not initialized")


class DynaFlowInvalidInitError(Exception):
    """
    Exception raised when the
    DynaFlow object
    is not initialized properly.
    """


class DynaFlowBaseBusObj(BaseBusObj):
    """
    This class represents the base business object
    for a DynaFlow.
    It requires a valid session context for initialization.
    """

    def __init__(
        self,
        session_context: SessionContext,
        dyna_flow: Optional[DynaFlow] = None
    ):
        """
        Initializes a new instance of the
        DynaFlowBusObj class.

        :param session_context: The session context.
        :raises ValueError: If the session is not provided.
        """

        if not session_context.session:
            raise ValueError("session required")

        if dyna_flow is None:
            dyna_flow = DynaFlow()

        self._session_context = session_context

        self.dyna_flow = dyna_flow

    @property
    def dyna_flow_id(self) -> int:
        """
        Get the dyna_flow ID from the
        DynaFlow object.

        :return: The dyna_flow ID.
        :raises AttributeError: If the
            DynaFlow object is not initialized.
        """

        if not self.dyna_flow:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.dyna_flow.dyna_flow_id
    # code

    @property
    def code(self):
        """
        Get the code from the
        DynaFlow object.

        :return: The code.
        :raises AttributeError: If the
            DynaFlow object is not initialized.
        """

        if not self.dyna_flow:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.dyna_flow.code

    @code.setter
    def code(self, value: uuid.UUID):  # type: ignore
        """
        Set the code for the DynaFlow object.

        :param value: The code value.
        :raises AttributeError: If the
            DynaFlow object is not initialized.
        :raises ValueError: If the code is not a UUID.
        """

        if not self.dyna_flow:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        if not isinstance(value, uuid.UUID):
            raise ValueError("code must be a UUID.")

        self.dyna_flow.code = value
    # last_change_code

    @property
    def last_change_code(self):
        """
        Get the last change code from the
        DynaFlow object.

        :return: The last change code.
        :raises AttributeError: If the
            DynaFlow object is not initialized.
        """

        if not self.dyna_flow:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.dyna_flow.last_change_code

    @last_change_code.setter
    def last_change_code(self, value: int):
        """
        Set the last change code for the
        DynaFlow object.

        :param value: The last change code value.
        :raises AttributeError: If the
            DynaFlow object is not initialized.
        :raises ValueError: If the last change code is not an integer.
        """

        if not self.dyna_flow:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        if not isinstance(value, int):
            raise ValueError("last_change_code must be an integer.")

        self.dyna_flow.last_change_code = value
    # insert_user_id

    @property
    def insert_user_id(self):
        """
        Get the insert user ID from the
        DynaFlow object.

        :return: The insert user ID.
        :raises AttributeError: If the
            DynaFlow object is not initialized.
        """

        if not self.dyna_flow:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.dyna_flow.insert_user_id

    @insert_user_id.setter
    def insert_user_id(self, value: uuid.UUID):
        """
        Set the insert user ID for the
        DynaFlow object.

        :param value: The insert user ID value.
        :raises AttributeError: If the
            DynaFlow object is not initialized.
        :raises ValueError: If the insert user ID is not a UUID.
        """

        if not self.dyna_flow:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        if not isinstance(value, uuid.UUID):
            raise ValueError(
                "insert_user_id must be a UUID.")

        self.dyna_flow.insert_user_id = value
    # last_update_user_id

    @property
    def last_update_user_id(self):
        """
        Get the last update user ID from the
        DynaFlow object.

        :return: The last update user ID.
        :raises AttributeError: If the
            DynaFlow object is not initialized.
        """

        if not self.dyna_flow:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.dyna_flow.last_update_user_id

    @last_update_user_id.setter
    def last_update_user_id(self, value: uuid.UUID):
        """
        Set the last update user ID for the
        DynaFlow object.

        :param value: The last update user ID value.
        :raises AttributeError: If the
            DynaFlow object is not initialized.
        :raises ValueError: If the last update user ID is not a UUID.
        """

        if not self.dyna_flow:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        if not isinstance(value, uuid.UUID):
            raise ValueError(
                "last_update_user_id must be a UUID.")

        self.dyna_flow.last_update_user_id = value

    # completedUTCDateTime

    @property
    def completed_utc_date_time(self):
        """
        Returns the value of
        completed_utc_date_time attribute of the
        dyna_flow.

        Raises:
            AttributeError: If the
                dyna_flow is not initialized.

        Returns:
            The value of
            completed_utc_date_time
            attribute.
        """
        if not self.dyna_flow:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.dyna_flow.completed_utc_date_time

    @completed_utc_date_time.setter
    def completed_utc_date_time(self, value):
        """
        Sets the value of
        completed_utc_date_time attribute
        for the dyna_flow.

        Args:
            value (datetime): The datetime value to be set.

        Raises:
            AttributeError: If the
                dyna_flow is not initialized.

        """
        if not self.dyna_flow:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        assert isinstance(value, datetime), (
            "completed_utc_date_time "
            "must be a datetime object")
        self.dyna_flow.completed_utc_date_time = value
    # dependencyDynaFlowID

    @property
    def dependency_dyna_flow_id(self):
        """
        Returns the value of
        dependency_dyna_flow_id attribute of the
        dyna_flow.

        Raises:
            AttributeError: If the
                dyna_flow is not initialized.

        Returns:
            int: The value of
                dependency_dyna_flow_id attribute.
        """
        if not self.dyna_flow:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.dyna_flow.dependency_dyna_flow_id

    @dependency_dyna_flow_id.setter
    def dependency_dyna_flow_id(self, value):
        """
        Sets the value of
        dependency_dyna_flow_id for the
        dyna_flow.

        Args:
            value (int): The integer value to set for
                dependency_dyna_flow_id.

        Raises:
            AttributeError: If the
                dyna_flow is not initialized.

        """
        if not self.dyna_flow:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        assert isinstance(value, int), (
            "dependency_dyna_flow_id must be an integer")
        self.dyna_flow.dependency_dyna_flow_id = value
    # description

    @property
    def description(self):
        """
        Get the Description from the
        DynaFlow object.

        :return: The Description.
        :raises AttributeError: If the
            DynaFlow object is not initialized.
        """

        if not self.dyna_flow:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        if self.dyna_flow.description is None:
            return ""

        return self.dyna_flow.description

    @description.setter
    def description(self, value):
        """
        Set the Description for the
        DynaFlow object.

        :param value: The Description value.
        :raises AttributeError: If the
            DynaFlow object is not initialized.
        :raises AssertionError: If the Description is not a string.
        """

        if not self.dyna_flow:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        assert isinstance(value, str), "description must be a string"
        self.dyna_flow.description = value
    # DynaFlowTypeID
    # isBuildTaskDebugRequired

    @property
    def is_build_task_debug_required(self):
        """
        Get the Is Build Task Debug Required flag from the
        DynaFlow object.

        :return: The Is Build Task Debug Required flag.
        :raises AttributeError: If the
            DynaFlow object is not initialized.
        """

        if not self.dyna_flow:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.dyna_flow.is_build_task_debug_required

    @is_build_task_debug_required.setter
    def is_build_task_debug_required(self, value: bool):
        """
        Set the Is Build Task Debug Required flag for the
        DynaFlow object.

        :param value: The Is Build Task Debug Required flag value.
        :raises AttributeError: If the
            DynaFlow object is not initialized.
        :raises ValueError: If the Is Build Task Debug Required flag is not a boolean.
        """

        if not self.dyna_flow:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        if not isinstance(value, bool):
            raise ValueError(
                "is_build_task_debug_required must be a boolean.")

        self.dyna_flow.is_build_task_debug_required = value
    # isCanceled

    @property
    def is_canceled(self):
        """
        Get the Is Canceled flag from the
        DynaFlow object.

        :return: The Is Canceled flag.
        :raises AttributeError: If the
            DynaFlow object is not initialized.
        """

        if not self.dyna_flow:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.dyna_flow.is_canceled

    @is_canceled.setter
    def is_canceled(self, value: bool):
        """
        Set the Is Canceled flag for the
        DynaFlow object.

        :param value: The Is Canceled flag value.
        :raises AttributeError: If the
            DynaFlow object is not initialized.
        :raises ValueError: If the Is Canceled flag is not a boolean.
        """

        if not self.dyna_flow:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        if not isinstance(value, bool):
            raise ValueError(
                "is_canceled must be a boolean.")

        self.dyna_flow.is_canceled = value
    # isCancelRequested

    @property
    def is_cancel_requested(self):
        """
        Get the Is Cancel Requested flag from the
        DynaFlow object.

        :return: The Is Cancel Requested flag.
        :raises AttributeError: If the
            DynaFlow object is not initialized.
        """

        if not self.dyna_flow:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.dyna_flow.is_cancel_requested

    @is_cancel_requested.setter
    def is_cancel_requested(self, value: bool):
        """
        Set the Is Cancel Requested flag for the
        DynaFlow object.

        :param value: The Is Cancel Requested flag value.
        :raises AttributeError: If the
            DynaFlow object is not initialized.
        :raises ValueError: If the Is Cancel Requested flag is not a boolean.
        """

        if not self.dyna_flow:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        if not isinstance(value, bool):
            raise ValueError(
                "is_cancel_requested must be a boolean.")

        self.dyna_flow.is_cancel_requested = value
    # isCompleted

    @property
    def is_completed(self):
        """
        Get the Is Completed flag from the
        DynaFlow object.

        :return: The Is Completed flag.
        :raises AttributeError: If the
            DynaFlow object is not initialized.
        """

        if not self.dyna_flow:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.dyna_flow.is_completed

    @is_completed.setter
    def is_completed(self, value: bool):
        """
        Set the Is Completed flag for the
        DynaFlow object.

        :param value: The Is Completed flag value.
        :raises AttributeError: If the
            DynaFlow object is not initialized.
        :raises ValueError: If the Is Completed flag is not a boolean.
        """

        if not self.dyna_flow:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        if not isinstance(value, bool):
            raise ValueError(
                "is_completed must be a boolean.")

        self.dyna_flow.is_completed = value
    # isPaused

    @property
    def is_paused(self):
        """
        Get the Is Paused flag from the
        DynaFlow object.

        :return: The Is Paused flag.
        :raises AttributeError: If the
            DynaFlow object is not initialized.
        """

        if not self.dyna_flow:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.dyna_flow.is_paused

    @is_paused.setter
    def is_paused(self, value: bool):
        """
        Set the Is Paused flag for the
        DynaFlow object.

        :param value: The Is Paused flag value.
        :raises AttributeError: If the
            DynaFlow object is not initialized.
        :raises ValueError: If the Is Paused flag is not a boolean.
        """

        if not self.dyna_flow:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        if not isinstance(value, bool):
            raise ValueError(
                "is_paused must be a boolean.")

        self.dyna_flow.is_paused = value
    # isResubmitted

    @property
    def is_resubmitted(self):
        """
        Get the Is Resubmitted flag from the
        DynaFlow object.

        :return: The Is Resubmitted flag.
        :raises AttributeError: If the
            DynaFlow object is not initialized.
        """

        if not self.dyna_flow:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.dyna_flow.is_resubmitted

    @is_resubmitted.setter
    def is_resubmitted(self, value: bool):
        """
        Set the Is Resubmitted flag for the
        DynaFlow object.

        :param value: The Is Resubmitted flag value.
        :raises AttributeError: If the
            DynaFlow object is not initialized.
        :raises ValueError: If the Is Resubmitted flag is not a boolean.
        """

        if not self.dyna_flow:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        if not isinstance(value, bool):
            raise ValueError(
                "is_resubmitted must be a boolean.")

        self.dyna_flow.is_resubmitted = value
    # isRunTaskDebugRequired

    @property
    def is_run_task_debug_required(self):
        """
        Get the Is Run Task Debug Required flag from the
        DynaFlow object.

        :return: The Is Run Task Debug Required flag.
        :raises AttributeError: If the
            DynaFlow object is not initialized.
        """

        if not self.dyna_flow:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.dyna_flow.is_run_task_debug_required

    @is_run_task_debug_required.setter
    def is_run_task_debug_required(self, value: bool):
        """
        Set the Is Run Task Debug Required flag for the
        DynaFlow object.

        :param value: The Is Run Task Debug Required flag value.
        :raises AttributeError: If the
            DynaFlow object is not initialized.
        :raises ValueError: If the Is Run Task Debug Required flag is not a boolean.
        """

        if not self.dyna_flow:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        if not isinstance(value, bool):
            raise ValueError(
                "is_run_task_debug_required must be a boolean.")

        self.dyna_flow.is_run_task_debug_required = value
    # isStarted

    @property
    def is_started(self):
        """
        Get the Is Started flag from the
        DynaFlow object.

        :return: The Is Started flag.
        :raises AttributeError: If the
            DynaFlow object is not initialized.
        """

        if not self.dyna_flow:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.dyna_flow.is_started

    @is_started.setter
    def is_started(self, value: bool):
        """
        Set the Is Started flag for the
        DynaFlow object.

        :param value: The Is Started flag value.
        :raises AttributeError: If the
            DynaFlow object is not initialized.
        :raises ValueError: If the Is Started flag is not a boolean.
        """

        if not self.dyna_flow:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        if not isinstance(value, bool):
            raise ValueError(
                "is_started must be a boolean.")

        self.dyna_flow.is_started = value
    # isSuccessful

    @property
    def is_successful(self):
        """
        Get the Is Successful flag from the
        DynaFlow object.

        :return: The Is Successful flag.
        :raises AttributeError: If the
            DynaFlow object is not initialized.
        """

        if not self.dyna_flow:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.dyna_flow.is_successful

    @is_successful.setter
    def is_successful(self, value: bool):
        """
        Set the Is Successful flag for the
        DynaFlow object.

        :param value: The Is Successful flag value.
        :raises AttributeError: If the
            DynaFlow object is not initialized.
        :raises ValueError: If the Is Successful flag is not a boolean.
        """

        if not self.dyna_flow:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        if not isinstance(value, bool):
            raise ValueError(
                "is_successful must be a boolean.")

        self.dyna_flow.is_successful = value
    # isTaskCreationStarted

    @property
    def is_task_creation_started(self):
        """
        Get the Is Task Creation Started flag from the
        DynaFlow object.

        :return: The Is Task Creation Started flag.
        :raises AttributeError: If the
            DynaFlow object is not initialized.
        """

        if not self.dyna_flow:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.dyna_flow.is_task_creation_started

    @is_task_creation_started.setter
    def is_task_creation_started(self, value: bool):
        """
        Set the Is Task Creation Started flag for the
        DynaFlow object.

        :param value: The Is Task Creation Started flag value.
        :raises AttributeError: If the
            DynaFlow object is not initialized.
        :raises ValueError: If the Is Task Creation Started flag is not a boolean.
        """

        if not self.dyna_flow:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        if not isinstance(value, bool):
            raise ValueError(
                "is_task_creation_started must be a boolean.")

        self.dyna_flow.is_task_creation_started = value
    # isTasksCreated

    @property
    def is_tasks_created(self):
        """
        Get the Is Tasks Created flag from the
        DynaFlow object.

        :return: The Is Tasks Created flag.
        :raises AttributeError: If the
            DynaFlow object is not initialized.
        """

        if not self.dyna_flow:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.dyna_flow.is_tasks_created

    @is_tasks_created.setter
    def is_tasks_created(self, value: bool):
        """
        Set the Is Tasks Created flag for the
        DynaFlow object.

        :param value: The Is Tasks Created flag value.
        :raises AttributeError: If the
            DynaFlow object is not initialized.
        :raises ValueError: If the Is Tasks Created flag is not a boolean.
        """

        if not self.dyna_flow:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        if not isinstance(value, bool):
            raise ValueError(
                "is_tasks_created must be a boolean.")

        self.dyna_flow.is_tasks_created = value
    # minStartUTCDateTime

    @property
    def min_start_utc_date_time(self):
        """
        Returns the value of
        min_start_utc_date_time attribute of the
        dyna_flow.

        Raises:
            AttributeError: If the
                dyna_flow is not initialized.

        Returns:
            The value of
            min_start_utc_date_time
            attribute.
        """
        if not self.dyna_flow:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.dyna_flow.min_start_utc_date_time

    @min_start_utc_date_time.setter
    def min_start_utc_date_time(self, value):
        """
        Sets the value of
        min_start_utc_date_time attribute
        for the dyna_flow.

        Args:
            value (datetime): The datetime value to be set.

        Raises:
            AttributeError: If the
                dyna_flow is not initialized.

        """
        if not self.dyna_flow:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        assert isinstance(value, datetime), (
            "min_start_utc_date_time "
            "must be a datetime object")
        self.dyna_flow.min_start_utc_date_time = value
    # PacID
    # param1

    @property
    def param_1(self):
        """
        Get the Param 1 from the
        DynaFlow object.

        :return: The Param 1.
        :raises AttributeError: If the
            DynaFlow object is not initialized.
        """

        if not self.dyna_flow:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        if self.dyna_flow.param_1 is None:
            return ""

        return self.dyna_flow.param_1

    @param_1.setter
    def param_1(self, value):
        """
        Set the Param 1 for the
        DynaFlow object.

        :param value: The Param 1 value.
        :raises AttributeError: If the
            DynaFlow object is not initialized.
        :raises AssertionError: If the Param 1 is not a string.
        """

        if not self.dyna_flow:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        assert isinstance(value, str), "param_1 must be a string"
        self.dyna_flow.param_1 = value
    # parentDynaFlowID

    @property
    def parent_dyna_flow_id(self):
        """
        Returns the value of
        parent_dyna_flow_id attribute of the
        dyna_flow.

        Raises:
            AttributeError: If the
                dyna_flow is not initialized.

        Returns:
            int: The value of
                parent_dyna_flow_id attribute.
        """
        if not self.dyna_flow:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.dyna_flow.parent_dyna_flow_id

    @parent_dyna_flow_id.setter
    def parent_dyna_flow_id(self, value):
        """
        Sets the value of
        parent_dyna_flow_id for the
        dyna_flow.

        Args:
            value (int): The integer value to set for
                parent_dyna_flow_id.

        Raises:
            AttributeError: If the
                dyna_flow is not initialized.

        """
        if not self.dyna_flow:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        assert isinstance(value, int), (
            "parent_dyna_flow_id must be an integer")
        self.dyna_flow.parent_dyna_flow_id = value
    # priorityLevel

    @property
    def priority_level(self):
        """
        Returns the value of
        priority_level attribute of the
        dyna_flow.

        Raises:
            AttributeError: If the
                dyna_flow is not initialized.

        Returns:
            int: The value of
                priority_level attribute.
        """
        if not self.dyna_flow:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.dyna_flow.priority_level

    @priority_level.setter
    def priority_level(self, value):
        """
        Sets the value of
        priority_level for the
        dyna_flow.

        Args:
            value (int): The integer value to set for
                priority_level.

        Raises:
            AttributeError: If the
                dyna_flow is not initialized.

        """
        if not self.dyna_flow:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        assert isinstance(value, int), (
            "priority_level must be an integer")
        self.dyna_flow.priority_level = value
    # requestedUTCDateTime

    @property
    def requested_utc_date_time(self):
        """
        Returns the value of
        requested_utc_date_time attribute of the
        dyna_flow.

        Raises:
            AttributeError: If the
                dyna_flow is not initialized.

        Returns:
            The value of
            requested_utc_date_time
            attribute.
        """
        if not self.dyna_flow:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.dyna_flow.requested_utc_date_time

    @requested_utc_date_time.setter
    def requested_utc_date_time(self, value):
        """
        Sets the value of
        requested_utc_date_time attribute
        for the dyna_flow.

        Args:
            value (datetime): The datetime value to be set.

        Raises:
            AttributeError: If the
                dyna_flow is not initialized.

        """
        if not self.dyna_flow:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        assert isinstance(value, datetime), (
            "requested_utc_date_time "
            "must be a datetime object")
        self.dyna_flow.requested_utc_date_time = value
    # resultValue

    @property
    def result_value(self):
        """
        Get the Result Value from the
        DynaFlow object.

        :return: The Result Value.
        :raises AttributeError: If the
            DynaFlow object is not initialized.
        """

        if not self.dyna_flow:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        if self.dyna_flow.result_value is None:
            return ""

        return self.dyna_flow.result_value

    @result_value.setter
    def result_value(self, value):
        """
        Set the Result Value for the
        DynaFlow object.

        :param value: The Result Value value.
        :raises AttributeError: If the
            DynaFlow object is not initialized.
        :raises AssertionError: If the Result Value is not a string.
        """

        if not self.dyna_flow:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        assert isinstance(value, str), "result_value must be a string"
        self.dyna_flow.result_value = value
    # rootDynaFlowID

    @property
    def root_dyna_flow_id(self):
        """
        Returns the value of
        root_dyna_flow_id attribute of the
        dyna_flow.

        Raises:
            AttributeError: If the
                dyna_flow is not initialized.

        Returns:
            int: The value of
                root_dyna_flow_id attribute.
        """
        if not self.dyna_flow:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.dyna_flow.root_dyna_flow_id

    @root_dyna_flow_id.setter
    def root_dyna_flow_id(self, value):
        """
        Sets the value of
        root_dyna_flow_id for the
        dyna_flow.

        Args:
            value (int): The integer value to set for
                root_dyna_flow_id.

        Raises:
            AttributeError: If the
                dyna_flow is not initialized.

        """
        if not self.dyna_flow:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        assert isinstance(value, int), (
            "root_dyna_flow_id must be an integer")
        self.dyna_flow.root_dyna_flow_id = value
    # startedUTCDateTime

    @property
    def started_utc_date_time(self):
        """
        Returns the value of
        started_utc_date_time attribute of the
        dyna_flow.

        Raises:
            AttributeError: If the
                dyna_flow is not initialized.

        Returns:
            The value of
            started_utc_date_time
            attribute.
        """
        if not self.dyna_flow:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.dyna_flow.started_utc_date_time

    @started_utc_date_time.setter
    def started_utc_date_time(self, value):
        """
        Sets the value of
        started_utc_date_time attribute
        for the dyna_flow.

        Args:
            value (datetime): The datetime value to be set.

        Raises:
            AttributeError: If the
                dyna_flow is not initialized.

        """
        if not self.dyna_flow:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        assert isinstance(value, datetime), (
            "started_utc_date_time "
            "must be a datetime object")
        self.dyna_flow.started_utc_date_time = value
    # subjectCode

    @property
    def subject_code(self):
        """
        Returns the value of the
        some unique identifier for the
        dyna_flow.

        Raises:
            AttributeError: If the
                dyna_flow is not initialized.

        Returns:
            The value of the some unique identifier for the
            dyna_flow.
        """
        if not self.dyna_flow:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.dyna_flow.subject_code

    @subject_code.setter
    def subject_code(self, value):
        """
        Sets the value of the
        'subject_code'
        attribute for the
        dyna_flow.

        Args:
            value (uuid.UUID): The UUID value to set for
                'subject_code'.

        Raises:
            AttributeError: If the
                dyna_flow is not initialized.

        """
        if not self.dyna_flow:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        assert isinstance(value, uuid.UUID), (
            "subject_code must be a UUID")
        self.dyna_flow.subject_code = value
    # taskCreationProcessorIdentifier

    @property
    def task_creation_processor_identifier(self):
        """
        Get the Task Creation Processor Identifier from the
        DynaFlow object.

        :return: The Task Creation Processor Identifier.
        :raises AttributeError: If the
            DynaFlow object is not initialized.
        """

        if not self.dyna_flow:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        if self.dyna_flow.task_creation_processor_identifier is None:
            return ""

        return self.dyna_flow.task_creation_processor_identifier

    @task_creation_processor_identifier.setter
    def task_creation_processor_identifier(self, value):
        """
        Set the Task Creation Processor Identifier for the
        DynaFlow object.

        :param value: The Task Creation Processor Identifier value.
        :raises AttributeError: If the
            DynaFlow object is not initialized.
        :raises AssertionError: If the Task Creation Processor Identifier is not a string.
        """

        if not self.dyna_flow:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        assert isinstance(value, str), "task_creation_processor_identifier must be a string"
        self.dyna_flow.task_creation_processor_identifier = value
    # isDeleteAllowed,
    # isEditAllowed,
    # otherFlavor,
    # someBigIntVal,
    # someBitVal,
    # someDecimalVal,
    # someEmailAddress,
    # DynaFlowTypeID

    @property
    def dyna_flow_type_id(self):
        """
        Returns the dyna_flow_type_id
        of the dyna_flow_type
        associated with the
        dyna_flow.

        Raises:
            AttributeError: If the
            dyna_flow is not initialized.

        Returns:
            int: The foreign key ID of the dyna_flow_type.
        """
        if not self.dyna_flow:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.dyna_flow.dyna_flow_type_id

    @dyna_flow_type_id.setter
    def dyna_flow_type_id(self, value: int):
        """
        Sets the foreign key ID for the
        dyna_flow_type of the
        dyna_flow.

        Args:
            value (int): The foreign key ID to set.

        Raises:
            AttributeError: If the
                dyna_flow is not initialized.
            ValueError: If the value is not an integer.
        """

        if not self.dyna_flow:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        if not isinstance(value, int):
            raise ValueError("dyna_flow_type_id must be an integer.")

        self.dyna_flow.dyna_flow_type_id = value

    @property
    def dyna_flow_type_code_peek(self) -> uuid.UUID:
        """
        Returns the dyna_flow_type_id code peek
        of the dyna_flow.

        Raises:
            AttributeError: If the dyna_flow
                is not initialized.

        Returns:
            uuid.UUID: The flvr foreign key code peek
            of the dyna_flow.
        """
        if not self.dyna_flow:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.dyna_flow.dyna_flow_type_code_peek
    # PacID
    @property
    def pac_id(self):
        """
        Returns the pac ID
        associated with the
        dyna_flow.

        Raises:
            AttributeError: If the
                dyna_flow is not initialized.

        Returns:
            int: The pac ID of the dyna_flow.
        """
        if not self.dyna_flow:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.dyna_flow.pac_id

    @pac_id.setter
    def pac_id(self, value):
        """
        Sets the pac ID
        for the dyna_flow.

        Args:
            value (int or None): The
                pac ID to be set.
                Must be an integer or None.

        Raises:
            AttributeError: If the
                dyna_flow is not initialized.

        """
        if not self.dyna_flow:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        assert isinstance(value, int) or value is None, (
            "pac_id must be an integer or None")

        self.dyna_flow.pac_id = value

    @property
    def pac_code_peek(self) -> uuid.UUID:
        """
        Returns the pac id code peek
        of the dyna_flow.

        Raises:
            AttributeError: If the
            dyna_flow is not initialized.

        Returns:
            uuid.UUID: The pac id code peek
            of the dyna_flow.
        """
        if not self.dyna_flow:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.dyna_flow.pac_code_peek
    # someFloatVal,
    # someIntVal,
    # someMoneyVal,
    # someNVarCharVal,
    # someDateVal
    # someUTCDateTimeVal

    # insert_utc_date_time

    @property
    def insert_utc_date_time(self):
        """
        Inserts the UTC date and time into
        the dyna_flow object.

        Raises:
            AttributeError: If the
                dyna_flow object is not initialized.

        Returns:
            The UTC date and time inserted into the
            dyna_flow object.
        """
        if not self.dyna_flow:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.dyna_flow.insert_utc_date_time

    @insert_utc_date_time.setter
    def insert_utc_date_time(self, value):
        """
        Inserts the UTC date and time for the
        dyna_flow.

        Args:
            value (datetime): The UTC date and time to be inserted.
                It should be a datetime object or None.

        Raises:
            AttributeError: If the
                dyna_flow is not initialized.

        """
        if not self.dyna_flow:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        assert isinstance(value, datetime) or value is None, (
            "insert_utc_date_time must be "
            "a datetime object or None")

        self.dyna_flow.insert_utc_date_time = value

    # update_utc_date_time
    @property
    def last_update_utc_date_time(self):
        """
        Returns the last update UTC date and time
        of the dyna_flow.

        Raises:
            AttributeError: If the
                dyna_flow is not initialized.

        Returns:
            datetime: The last update UTC date and time
                of the dyna_flow.
        """
        if not self.dyna_flow:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.dyna_flow.last_update_utc_date_time

    @last_update_utc_date_time.setter
    def last_update_utc_date_time(self, value):
        """
        Sets the last update UTC date and time
        for the dyna_flow.

        Args:
            value (datetime): The datetime object
                representing the last update UTC date and time.
                Pass None to unset the value.

        Raises:
            AttributeError: If the
                dyna_flow is not initialized.

        """
        if not self.dyna_flow:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        assert isinstance(value, datetime) or value is None, (
            "last_update_utc_date_time "
            "must be a datetime object or None")

        self.dyna_flow.last_update_utc_date_time = value

    async def load_from_json(
        self,
        json_data: str
    ):
        """
        Load dyna_flow data
        from JSON string.

        :param json_data: JSON string containing
            dyna_flow data.
        :raises ValueError: If json_data is not a string
            or if no dyna_flow
            data is found.
        """

        if not isinstance(json_data, str):
            raise ValueError(
                "json_data must be a string")

        dyna_flow_manager = DynaFlowManager(
            self._session_context)
        self.dyna_flow = await \
            dyna_flow_manager.from_json(json_data)

        return self

    async def load_from_code(
        self,
        code: uuid.UUID
    ):
        """
        Load dyna_flow
        data from UUID code.

        :param code: UUID code for loading a specific
            dyna_flow.
        :raises ValueError: If code is not a UUID or if no
            dyna_flow data is found.
        """
        if not isinstance(code, uuid.UUID):
            raise ValueError(
                "code must be a UUID")

        dyna_flow_manager = DynaFlowManager(
            self._session_context)
        dyna_flow_obj = await dyna_flow_manager.get_by_code(
            code)
        self.dyna_flow = dyna_flow_obj

        return self

    async def load_from_id(
        self,
        dyna_flow_id: int
    ):
        """
        Load dyna_flow data from
        dyna_flow ID.

        :param dyna_flow_id: Integer ID for loading a specific
            dyna_flow.
        :raises ValueError: If dyna_flow_id
            is not an integer or
            if no dyna_flow
            data is found.
        """

        if not isinstance(dyna_flow_id, int):
            raise ValueError(
                "dyna_flow_id must be an integer")

        dyna_flow_manager = DynaFlowManager(
            self._session_context)
        dyna_flow_obj = await dyna_flow_manager.get_by_id(
            dyna_flow_id)
        self.dyna_flow = dyna_flow_obj

        return self

    def load_from_obj_instance(
        self,
        dyna_flow_obj_instance: DynaFlow
    ):
        """
        Use the provided
        DynaFlow instance.

        :param dyna_flow_obj_instance: Instance of the
            DynaFlow class.
        :raises ValueError: If dyna_flow_obj_instance
            is not an instance of
            DynaFlow.
        """

        if not isinstance(dyna_flow_obj_instance,
                          DynaFlow):
            raise ValueError(
                "dyna_flow_obj_instance must be an "
                "instance of DynaFlow")

        self.dyna_flow = dyna_flow_obj_instance

        return self

    async def load_from_dict(
        self,
        dyna_flow_dict: dict
    ):
        """
        Load dyna_flow data
        from dictionary.

        :param dyna_flow_dict: Dictionary containing
            dyna_flow data.
        :raises ValueError: If dyna_flow_dict
            is not a
            dictionary or if no
            dyna_flow data is found.
        """
        if not isinstance(dyna_flow_dict, dict):
            raise ValueError(
                "dyna_flow_dict must be a dictionary")

        dyna_flow_manager = DynaFlowManager(
            self._session_context)

        self.dyna_flow = await \
            dyna_flow_manager.from_dict(
                dyna_flow_dict)

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
        Refreshes the dyna_flow
        object by fetching
        the latest data from the database.

        Returns:
            The updated
            dyna_flow object.
        """
        dyna_flow_manager = DynaFlowManager(
            self._session_context)
        self.dyna_flow = await \
            dyna_flow_manager.refresh(
                self.dyna_flow)

        return self

    def is_valid(self):
        """
        Check if the dyna_flow
        is valid.

        Returns:
            bool: True if the dyna_flow
                is valid, False otherwise.
        """
        return self.dyna_flow is not None

    def to_dict(self):
        """
        Converts the DynaFlow
        object to a dictionary representation.

        Returns:
            dict: A dictionary representation of the
                DynaFlow object.
        """
        dyna_flow_manager = DynaFlowManager(
            self._session_context)
        return dyna_flow_manager.to_dict(
            self.dyna_flow)

    def to_json(self):
        """
        Converts the dyna_flow
        object to a JSON representation.

        Returns:
            str: The JSON representation of the
                dyna_flow object.
        """
        dyna_flow_manager = DynaFlowManager(
            self._session_context)
        return dyna_flow_manager.to_json(
            self.dyna_flow)

    async def save(self):
        """
        Saves the dyna_flow object
        to the database.

        If the dyna_flow object
        is not initialized, an AttributeError is raised.
        If the dyna_flow_id
        is greater than 0, the
        dyna_flow is
        updated in the database.
        If the dyna_flow_id is 0,
        the dyna_flow is
        added to the database.

        Returns:
            The updated or added
            dyna_flow object.

        Raises:
            AttributeError: If the dyna_flow
            object is not initialized.
        """
        if not self.dyna_flow:
            raise AttributeError(NOT_INITIALIZED_ERROR_MESSAGE)

        dyna_flow_id = self.dyna_flow.dyna_flow_id

        if dyna_flow_id > 0:
            dyna_flow_manager = DynaFlowManager(
                self._session_context)
            self.dyna_flow = await \
                dyna_flow_manager.update(
                    self.dyna_flow)

        if dyna_flow_id == 0:
            dyna_flow_manager = DynaFlowManager(
                self._session_context)
            self.dyna_flow = await \
                dyna_flow_manager.add(
                    self.dyna_flow)

        return self

    async def delete(self):
        """
        Deletes the dyna_flow
        from the database.

        Raises:
            AttributeError: If the dyna_flow
                is not initialized.
        """
        if not self.dyna_flow:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        if self.dyna_flow.dyna_flow_id > 0:
            dyna_flow_manager = DynaFlowManager(
                self._session_context)
            await dyna_flow_manager.delete(
                self.dyna_flow.dyna_flow_id)
            self.dyna_flow = None

    async def randomize_properties(self):
        """
        Randomizes the properties of the
        dyna_flow object.

        This method generates random values for various
        properties of the dyna_flow
        object

        Returns:
            self: The current instance of the
                DynaFlow class.

        Raises:
            AttributeError: If the dyna_flow
                object is not initialized.
        """
        if not self.dyna_flow:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        self.dyna_flow.completed_utc_date_time = datetime(
            random.randint(2000, 2023),
            random.randint(1, 12),
            random.randint(1, 28))
        self.dyna_flow.dependency_dyna_flow_id = (
            random.randint(0, 100))
        self.dyna_flow.description = "".join(
            random.choices("abcdefghijklmnopqrstuvwxyz", k=10))
        self.dyna_flow.dyna_flow_type_id = random.choice(
            await managers_and_enums.DynaFlowTypeManager(
                self._session_context).get_list()).dyna_flow_type_id
        self.dyna_flow.is_build_task_debug_required = (
            random.choice([True, False]))
        self.dyna_flow.is_canceled = (
            random.choice([True, False]))
        self.dyna_flow.is_cancel_requested = (
            random.choice([True, False]))
        self.dyna_flow.is_completed = (
            random.choice([True, False]))
        self.dyna_flow.is_paused = (
            random.choice([True, False]))
        self.dyna_flow.is_resubmitted = (
            random.choice([True, False]))
        self.dyna_flow.is_run_task_debug_required = (
            random.choice([True, False]))
        self.dyna_flow.is_started = (
            random.choice([True, False]))
        self.dyna_flow.is_successful = (
            random.choice([True, False]))
        self.dyna_flow.is_task_creation_started = (
            random.choice([True, False]))
        self.dyna_flow.is_tasks_created = (
            random.choice([True, False]))
        self.dyna_flow.min_start_utc_date_time = datetime(
            random.randint(2000, 2023),
            random.randint(1, 12),
            random.randint(1, 28))
        # self.dyna_flow.pac_id = random.randint(0, 100)
        self.dyna_flow.param_1 = "".join(
            random.choices("abcdefghijklmnopqrstuvwxyz", k=10))
        self.dyna_flow.parent_dyna_flow_id = (
            random.randint(0, 100))
        self.dyna_flow.priority_level = (
            random.randint(0, 100))
        self.dyna_flow.requested_utc_date_time = datetime(
            random.randint(2000, 2023),
            random.randint(1, 12),
            random.randint(1, 28))
        self.dyna_flow.result_value = "".join(
            random.choices("abcdefghijklmnopqrstuvwxyz", k=10))
        self.dyna_flow.root_dyna_flow_id = (
            random.randint(0, 100))
        self.dyna_flow.started_utc_date_time = datetime(
            random.randint(2000, 2023),
            random.randint(1, 12),
            random.randint(1, 28))
        self.dyna_flow.subject_code = uuid.uuid4()
        self.dyna_flow.task_creation_processor_identifier = "".join(
            random.choices("abcdefghijklmnopqrstuvwxyz", k=10))

        return self

    def get_dyna_flow_obj(self) -> DynaFlow:
        """
        Returns the dyna_flow
        object.

        Raises:
            AttributeError: If the dyna_flow
                object is not initialized.

        Returns:
            DynaFlow: The dyna_flow
                object.
        """
        if not self.dyna_flow:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.dyna_flow

    def is_equal(
        self,
        dyna_flow: DynaFlow
    ) -> bool:
        """
        Checks if the current dyna_flow
        is equal to the given dyna_flow.

        Args:
            dyna_flow (DynaFlow): The
                dyna_flow to compare with.

        Returns:
            bool: True if the dyna_flows
                are equal, False otherwise.
        """
        dyna_flow_manager = DynaFlowManager(
            self._session_context)
        my_dyna_flow = self.get_dyna_flow_obj()
        return dyna_flow_manager.is_equal(
            dyna_flow, my_dyna_flow)

    def get_obj(self) -> DynaFlow:
        """
        Returns the DynaFlow object.

        :return: The DynaFlow object.
        :rtype: DynaFlow
        """

        return self.dyna_flow

    def get_object_name(self) -> str:
        """
        Returns the name of the object.

        :return: The name of the object.
        :rtype: str
        """
        return "dyna_flow"

    def get_id(self) -> int:
        """
        Returns the ID of the dyna_flow.

        :return: The ID of the dyna_flow.
        :rtype: int
        """
        return self.dyna_flow_id
    # completedUTCDateTime
    # dependencyDynaFlowID,
    # description,
    # DynaFlowTypeID
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

    async def get_parent_name(self) -> str:
        """
        Get the name of the parent dyna_flow.

        Returns:
            str: The name of the parent dyna_flow.
        """
        return 'Pac'

    async def get_parent_code(self) -> uuid.UUID:
        """
        Get the parent code of the dyna_flow.

        Returns:
            The parent code of the dyna_flow
            as a UUID.
        """
        return self.pac_code_peek

    async def get_parent_obj(self) -> models.Pac:
        """
        Get the parent object of the current
        dyna_flow.

        Returns:
            The parent object of the current
            dyna_flow,
            which is an instance of the
            Pac model.
        """
        pac_manager = managers_and_enums.PacManager(
            self._session_context)
        pac_obj = await pac_manager.get_by_id(
            self.pac_id)
        return pac_obj
    # param1,
    # parentDynaFlowID,
    # priorityLevel,
    # requestedUTCDateTime
    # resultValue,
    # rootDynaFlowID,
    # startedUTCDateTime
    # subjectCode,
    # taskCreationProcessorIdentifier,
