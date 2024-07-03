# models/dyna_flow_task.py
# pylint: disable=unused-import

"""
The DynaFlowTask model inherits from
the Base model and is mapped to the
'farm_DynaFlowTask' table in the database.
"""
from decimal import Decimal  # noqa: F401
import uuid  # noqa: F401
from datetime import date, datetime, timezone  # noqa: F401
from sqlalchemy_utils import UUIDType
from sqlalchemy import (BigInteger, Boolean,   # noqa: F401
                        Column, Date, DateTime, Float,
                        ForeignKey, Index, Integer, Numeric, String,
                        event, func)
import models.constants.dyna_flow_task as \
    dyna_flow_task_constants
from utils.common_functions import snake_case
from .base import Base, EncryptedType  # noqa: F401


class DynaFlowTask(Base):
    """
    The DynaFlowTask model represents a
    dyna_flow_task in the farm.
    It inherits from the Base model and is mapped to the
    'farm_DynaFlowTask' table in the database.
    """

    __tablename__ = 'farm_' + snake_case('DynaFlowTask')

    _dyna_flow_task_id = Column(
        'dyna_flow_task_id',
        Integer,
        primary_key=True,
        autoincrement=True)
    _code = Column(
        'code',
        UUIDType(binary=False),
        unique=True,
        default=uuid.uuid4,
        nullable=True)
    _last_change_code = Column(
        'last_change_code',
        Integer,
        nullable=True)
    _insert_user_id = Column(
        'insert_user_id',
        UUIDType(binary=False),
        default=uuid.uuid4,
        nullable=True)
    _last_update_user_id = Column(
        'last_update_user_id',
        UUIDType(binary=False),
        default=uuid.uuid4,
        nullable=True)
    _completed_utc_date_time = Column(
        'completed_utc_date_time',
        DateTime,
        default=datetime(1753, 1, 1, 0, 0, tzinfo=timezone.utc),
        index=(
            dyna_flow_task_constants.
            completed_utc_date_time_calculatedIsDBColumnIndexed
        ),
        nullable=True)
    _dependency_dyna_flow_task_id = Column(
        'dependency_dyna_flow_task_id',
        Integer,
        default=0,
        index=(
            dyna_flow_task_constants.
            dependency_dyna_flow_task_id_calculatedIsDBColumnIndexed
        ),
        nullable=True)
    _description = Column(
        'description',

        String,

        default="",
        index=(
            dyna_flow_task_constants.
            description_calculatedIsDBColumnIndexed
        ),
        nullable=True)
    _dyna_flow_id = Column(
        'dyna_flow_id',
        Integer,
        ForeignKey('farm_' + snake_case('DynaFlow') + '.dyna_flow_id'),
        index=(
            dyna_flow_task_constants.
            dyna_flow_id_calculatedIsDBColumnIndexed
        ),
        nullable=True)
    _dyna_flow_subject_code = Column(
        'dyna_flow_subject_code',
        UUIDType(binary=False),
        default=uuid.uuid4,
        index=(
            dyna_flow_task_constants.
            dyna_flow_subject_code_calculatedIsDBColumnIndexed
        ),
        nullable=True)
    _dyna_flow_task_type_id = Column(
        'dyna_flow_task_type_id',
        Integer,
        ForeignKey('farm_' + snake_case('DynaFlowTaskType') + '.dyna_flow_task_type_id'),
        index=(
            dyna_flow_task_constants.
            dyna_flow_task_type_id_calculatedIsDBColumnIndexed
        ),
        nullable=True)
    _is_canceled = Column(
        'is_canceled',
        Boolean,
        default=False,
        index=(
            dyna_flow_task_constants.
            is_canceled_calculatedIsDBColumnIndexed
        ),
        nullable=True)
    _is_cancel_requested = Column(
        'is_cancel_requested',
        Boolean,
        default=False,
        index=(
            dyna_flow_task_constants.
            is_cancel_requested_calculatedIsDBColumnIndexed
        ),
        nullable=True)
    _is_completed = Column(
        'is_completed',
        Boolean,
        default=False,
        index=(
            dyna_flow_task_constants.
            is_completed_calculatedIsDBColumnIndexed
        ),
        nullable=True)
    _is_parallel_run_allowed = Column(
        'is_parallel_run_allowed',
        Boolean,
        default=False,
        index=(
            dyna_flow_task_constants.
            is_parallel_run_allowed_calculatedIsDBColumnIndexed
        ),
        nullable=True)
    _is_run_task_debug_required = Column(
        'is_run_task_debug_required',
        Boolean,
        default=False,
        index=(
            dyna_flow_task_constants.
            is_run_task_debug_required_calculatedIsDBColumnIndexed
        ),
        nullable=True)
    _is_started = Column(
        'is_started',
        Boolean,
        default=False,
        index=(
            dyna_flow_task_constants.
            is_started_calculatedIsDBColumnIndexed
        ),
        nullable=True)
    _is_successful = Column(
        'is_successful',
        Boolean,
        default=False,
        index=(
            dyna_flow_task_constants.
            is_successful_calculatedIsDBColumnIndexed
        ),
        nullable=True)
    _max_retry_count = Column(
        'max_retry_count',
        Integer,
        default=0,
        index=(
            dyna_flow_task_constants.
            max_retry_count_calculatedIsDBColumnIndexed
        ),
        nullable=True)
    _min_start_utc_date_time = Column(
        'min_start_utc_date_time',
        DateTime,
        default=datetime(1753, 1, 1, 0, 0, tzinfo=timezone.utc),
        index=(
            dyna_flow_task_constants.
            min_start_utc_date_time_calculatedIsDBColumnIndexed
        ),
        nullable=True)
    _param_1 = Column(
        'param_1',

        String,

        default="",
        index=(
            dyna_flow_task_constants.
            param_1_calculatedIsDBColumnIndexed
        ),
        nullable=True)
    _param_2 = Column(
        'param_2',

        String,

        default="",
        index=(
            dyna_flow_task_constants.
            param_2_calculatedIsDBColumnIndexed
        ),
        nullable=True)
    _processor_identifier = Column(
        'processor_identifier',

        String,

        default="",
        index=(
            dyna_flow_task_constants.
            processor_identifier_calculatedIsDBColumnIndexed
        ),
        nullable=True)
    _requested_utc_date_time = Column(
        'requested_utc_date_time',
        DateTime,
        default=datetime(1753, 1, 1, 0, 0, tzinfo=timezone.utc),
        index=(
            dyna_flow_task_constants.
            requested_utc_date_time_calculatedIsDBColumnIndexed
        ),
        nullable=True)
    _result_value = Column(
        'result_value',

        String,

        default="",
        index=(
            dyna_flow_task_constants.
            result_value_calculatedIsDBColumnIndexed
        ),
        nullable=True)
    _retry_count = Column(
        'retry_count',
        Integer,
        default=0,
        index=(
            dyna_flow_task_constants.
            retry_count_calculatedIsDBColumnIndexed
        ),
        nullable=True)
    _started_utc_date_time = Column(
        'started_utc_date_time',
        DateTime,
        default=datetime(1753, 1, 1, 0, 0, tzinfo=timezone.utc),
        index=(
            dyna_flow_task_constants.
            started_utc_date_time_calculatedIsDBColumnIndexed
        ),
        nullable=True)
    dyna_flow_code_peek: uuid.UUID = uuid.UUID(int=0)  # DynaFlowID  # noqa: E501
    dyna_flow_task_type_code_peek: uuid.UUID = uuid.UUID(int=0)  # DynaFlowTaskTypeID  # noqa: E501
    _insert_utc_date_time = Column(
        'insert_utc_date_time',
        DateTime,
        nullable=True)
    _last_update_utc_date_time = Column(
        'last_update_utc_date_time',
        DateTime,
        nullable=True)

    __mapper_args__ = {
        'version_id_col': _last_change_code
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.code = kwargs.get('code', uuid.uuid4())
        self.last_change_code = kwargs.get(
            'last_change_code', 0)
        self.insert_user_id = kwargs.get(
            'insert_user_id', uuid.UUID(int=0))
        self.last_update_user_id = kwargs.get(
            'last_update_user_id', uuid.UUID(int=0))
        self.completed_utc_date_time = kwargs.get(
            'completed_utc_date_time', datetime(1753, 1, 1, 0, 0, tzinfo=timezone.utc))
        self.dependency_dyna_flow_task_id = kwargs.get(
            'dependency_dyna_flow_task_id', 0)
        self.description = kwargs.get(
            'description', "")
        self.dyna_flow_id = kwargs.get(
            'dyna_flow_id', 0)
        self.dyna_flow_subject_code = kwargs.get(
            'dyna_flow_subject_code', uuid.uuid4())
        self.dyna_flow_task_type_id = kwargs.get(
            'dyna_flow_task_type_id', 0)
        self.is_canceled = kwargs.get(
            'is_canceled', False)
        self.is_cancel_requested = kwargs.get(
            'is_cancel_requested', False)
        self.is_completed = kwargs.get(
            'is_completed', False)
        self.is_parallel_run_allowed = kwargs.get(
            'is_parallel_run_allowed', False)
        self.is_run_task_debug_required = kwargs.get(
            'is_run_task_debug_required', False)
        self.is_started = kwargs.get(
            'is_started', False)
        self.is_successful = kwargs.get(
            'is_successful', False)
        self.max_retry_count = kwargs.get(
            'max_retry_count', 0)
        self.min_start_utc_date_time = kwargs.get(
            'min_start_utc_date_time', datetime(1753, 1, 1, 0, 0, tzinfo=timezone.utc))
        self.param_1 = kwargs.get(
            'param_1', "")
        self.param_2 = kwargs.get(
            'param_2', "")
        self.processor_identifier = kwargs.get(
            'processor_identifier', "")
        self.requested_utc_date_time = kwargs.get(
            'requested_utc_date_time', datetime(1753, 1, 1, 0, 0, tzinfo=timezone.utc))
        self.result_value = kwargs.get(
            'result_value', "")
        self.retry_count = kwargs.get(
            'retry_count', 0)
        self.started_utc_date_time = kwargs.get(
            'started_utc_date_time', datetime(1753, 1, 1, 0, 0, tzinfo=timezone.utc))
        self.insert_utc_date_time = kwargs.get(
            'insert_utc_date_time', datetime(1753, 1, 1, 0, 0, tzinfo=timezone.utc))
        self.last_update_utc_date_time = kwargs.get(
            'last_update_utc_date_time', datetime(1753, 1, 1, 0, 0, tzinfo=timezone.utc))
        self.dyna_flow_code_peek = kwargs.get(  # DynaFlowID
            'dyna_flow_code_peek', uuid.UUID(int=0))
        self.dyna_flow_task_type_code_peek = kwargs.get(  # DynaFlowTaskTypeID
            'dyna_flow_task_type_code_peek', uuid.UUID(int=0))

    @property
    def code(self):
        """
        Get the code of the dyna_flow_task.

        Returns:
            UUID: The code of the dyna_flow_task.
        """
        return uuid.UUID(str(self._code))

    @code.setter
    def code(self, value: uuid.UUID):
        """
        Set the code of the dyna_flow_task.

        Args:
            value (uuid.UUID): The code to set for the
                dyna_flow_task.

        Raises:
            TypeError: If the value is not of type uuid.UUID.

        """
        if isinstance(value, uuid.UUID):
            self._code = value
        else:
            self._code = uuid.UUID(value)
        self.last_update_utc_date_time = datetime.now(timezone.utc)

    @property
    def dyna_flow_task_id(self) -> int:
        """
        Get the ID of the dyna_flow_task.

        Returns:
            int: The ID of the dyna_flow_task.
        """
        return getattr(self, '_dyna_flow_task_id', 0) or 0

    @dyna_flow_task_id.setter
    def dyna_flow_task_id(self, value: int) -> None:
        """
        Set the dyna_flow_task_id.
        """

        self._dyna_flow_task_id = value

    @property
    def last_change_code(self) -> int:
        """
        Returns the last change code of the
        dyna_flow_task.

        :return: The last change code of the
            dyna_flow_task.
        :rtype: int
        """
        return getattr(self, '_last_change_code', 0) or 0

    @last_change_code.setter
    def last_change_code(self, value: int) -> None:
        """
        Set the last_change_code.
        """

        self._last_change_code = value

    @property
    def insert_user_id(self):
        """
        Inserts the user ID into the
        dyna_flow_task object.

        Returns:
            UUID: The UUID of the inserted user ID.
        """
        return uuid.UUID(str(self._insert_user_id))

    @insert_user_id.setter
    def insert_user_id(self, value):
        if isinstance(value, uuid.UUID):
            self._insert_user_id = value
        else:
            self._insert_user_id = uuid.UUID(value)
        self.last_update_utc_date_time = datetime.now(timezone.utc)

    @property
    def last_update_user_id(self):
        """
        Returns the UUID of the last user who updated the
        dyna_flow_task.

        :return: The UUID of the last update user.
        :rtype: UUID
        """
        return uuid.UUID(str(self._last_update_user_id))

    @last_update_user_id.setter
    def last_update_user_id(self, value):
        if isinstance(value, uuid.UUID):
            self._last_update_user_id = value
        else:
            self._last_update_user_id = uuid.UUID(value)
        self.last_update_utc_date_time = datetime.now(timezone.utc)

    @property
    def insert_utc_date_time(self) -> datetime:
        """
        Inserts the UTC date and time for the
        dyna_flow_task.

        Returns:
            datetime: The UTC date and time for the
                dyna_flow_task.
        """
        dt = getattr(
            self,
            '_insert_utc_date_time',
            datetime(1753, 1, 1, 0, 0, tzinfo=timezone.utc)
        ) or datetime(1753, 1, 1, 0, 0, tzinfo=timezone.utc)
        if dt is not None and dt.tzinfo is None:
            # Make the datetime aware (UTC) if it is naive
            dt = dt.replace(tzinfo=timezone.utc)
        return dt

    @insert_utc_date_time.setter
    def insert_utc_date_time(self, value: datetime) -> None:
        """
        Set the insert_utc_date_time.
        """
        if value is not None and value.tzinfo is None:
            # If the datetime is naive, assume UTC
            value = value.replace(tzinfo=timezone.utc)

        self._insert_utc_date_time = value

    @property
    def last_update_utc_date_time(self) -> datetime:
        """
        Returns the last update UTC date and time of the
        dyna_flow_task.

        :return: A datetime object representing the
            last update UTC date and time.
        """
        dt = getattr(
            self,
            '_last_update_utc_date_time',
            datetime(1753, 1, 1, 0, 0, tzinfo=timezone.utc)
        ) or datetime(1753, 1, 1, 0, 0, tzinfo=timezone.utc)

        if dt is not None and dt.tzinfo is None:
            # Make the datetime aware (UTC) if it is naive
            dt = dt.replace(tzinfo=timezone.utc)
        return dt

    @last_update_utc_date_time.setter
    def last_update_utc_date_time(self, value: datetime) -> None:
        """
        Set the last_update_utc_date_time.
        """
        if value is not None and value.tzinfo is None:
            # If the datetime is naive, assume UTC
            value = value.replace(tzinfo=timezone.utc)

        self._last_update_utc_date_time = value
    # completedUTCDateTime

    @property
    def completed_utc_date_time(self) -> datetime:
        """
        Get the value of completed_utc_date_time property.

        Returns:
            datetime: The value of completed_utc_date_time property.
        """
        dt = getattr(
            self,
            '_completed_utc_date_time',
            datetime(1753, 1, 1, 0, 0, tzinfo=timezone.utc)
        ) or datetime(1753, 1, 1, 0, 0, tzinfo=timezone.utc)
        if dt is not None and dt.tzinfo is None:
            # Make the datetime aware (UTC) if it is naive
            dt = dt.replace(tzinfo=timezone.utc)
        return dt

    @completed_utc_date_time.setter
    def completed_utc_date_time(self, value: datetime) -> None:
        """
        Set the completed_utc_date_time.
        """
        if value is not None and value.tzinfo is None:
            # If the datetime is naive, assume UTC
            value = value.replace(tzinfo=timezone.utc)
        self._completed_utc_date_time = value
    # dependencyDynaFlowTaskID,

    @property
    def dependency_dyna_flow_task_id(self) -> int:
        """
        Returns the value of the '_dependency_dyna_flow_task_id' attribute of the object.
        If the attribute is not set, it returns 0.

        :return: The value of the '_dependency_dyna_flow_task_id' attribute or 0 if not set.
        :rtype: int
        """
        return getattr(self, '_dependency_dyna_flow_task_id', 0) or 0

    @dependency_dyna_flow_task_id.setter
    def dependency_dyna_flow_task_id(self, value: int) -> None:
        """
        Set the dependency_dyna_flow_task_id.
        """

        self._dependency_dyna_flow_task_id = value
    # description,

    @property
    def description(self) -> str:
        """
        Returns the Description of the
        dyna_flow_task.

        :return: The Description of the
            dyna_flow_task.
        :rtype: str
        """
        return getattr(self, '_description', "") or ""

    @description.setter
    def description(self, value: str) -> None:
        """
        Set the description.
        """

        self._description = value
    # DynaFlowID
    # dynaFlowSubjectCode,

    @property
    def dyna_flow_subject_code(self):
        """
        Returns the unique identifier as a UUID object.

        Returns:
            uuid.UUID: The unique identifier value.
        """

        return uuid.UUID(
            str(self._dyna_flow_subject_code))

    @dyna_flow_subject_code.setter
    def dyna_flow_subject_code(self, value):
        """
        Sets the unique identifier value. The input
        can be either a uuid.UUID object or a string
        that can be converted to a uuid.UUID object.
        Updates the last_update_utc_date_time to the
        current naive UTC datetime.

        Args:
            value (uuid.UUID or str): The unique identifier
            value to set.

        Raises:
            ValueError: If the provided value cannot be
            converted to a uuid.UUID.
        """

        if isinstance(value, uuid.UUID):
            self._dyna_flow_subject_code = value
        else:
            try:
                self._dyna_flow_subject_code = uuid.UUID(value)
            except ValueError as e:
                raise ValueError(f"Invalid UUID value: {value}") from e
        self.last_update_utc_date_time = datetime.now(timezone.utc)
    # dynaFlowTaskTypeID
    # isCanceled,

    @property
    def is_canceled(self) -> bool:
        """
        Check if the delete operation is allowed for the
        dyna_flow_task.

        Returns:
            bool: True if delete is allowed, False otherwise.
        """
        return getattr(self, '_is_canceled', False) or False

    @is_canceled.setter
    def is_canceled(self, value: bool) -> None:
        """
        Set the is_canceled.
        """

        self._is_canceled = value
    # isCancelRequested,

    @property
    def is_cancel_requested(self) -> bool:
        """
        Check if the delete operation is allowed for the
        dyna_flow_task.

        Returns:
            bool: True if delete is allowed, False otherwise.
        """
        return getattr(self, '_is_cancel_requested', False) or False

    @is_cancel_requested.setter
    def is_cancel_requested(self, value: bool) -> None:
        """
        Set the is_cancel_requested.
        """

        self._is_cancel_requested = value
    # isCompleted,

    @property
    def is_completed(self) -> bool:
        """
        Check if the delete operation is allowed for the
        dyna_flow_task.

        Returns:
            bool: True if delete is allowed, False otherwise.
        """
        return getattr(self, '_is_completed', False) or False

    @is_completed.setter
    def is_completed(self, value: bool) -> None:
        """
        Set the is_completed.
        """

        self._is_completed = value
    # isParallelRunAllowed,

    @property
    def is_parallel_run_allowed(self) -> bool:
        """
        Check if the delete operation is allowed for the
        dyna_flow_task.

        Returns:
            bool: True if delete is allowed, False otherwise.
        """
        return getattr(self, '_is_parallel_run_allowed', False) or False

    @is_parallel_run_allowed.setter
    def is_parallel_run_allowed(self, value: bool) -> None:
        """
        Set the is_parallel_run_allowed.
        """

        self._is_parallel_run_allowed = value
    # isRunTaskDebugRequired,

    @property
    def is_run_task_debug_required(self) -> bool:
        """
        Check if the delete operation is allowed for the
        dyna_flow_task.

        Returns:
            bool: True if delete is allowed, False otherwise.
        """
        return getattr(self, '_is_run_task_debug_required', False) or False

    @is_run_task_debug_required.setter
    def is_run_task_debug_required(self, value: bool) -> None:
        """
        Set the is_run_task_debug_required.
        """

        self._is_run_task_debug_required = value
    # isStarted,

    @property
    def is_started(self) -> bool:
        """
        Check if the delete operation is allowed for the
        dyna_flow_task.

        Returns:
            bool: True if delete is allowed, False otherwise.
        """
        return getattr(self, '_is_started', False) or False

    @is_started.setter
    def is_started(self, value: bool) -> None:
        """
        Set the is_started.
        """

        self._is_started = value
    # isSuccessful,

    @property
    def is_successful(self) -> bool:
        """
        Check if the delete operation is allowed for the
        dyna_flow_task.

        Returns:
            bool: True if delete is allowed, False otherwise.
        """
        return getattr(self, '_is_successful', False) or False

    @is_successful.setter
    def is_successful(self, value: bool) -> None:
        """
        Set the is_successful.
        """

        self._is_successful = value
    # maxRetryCount,

    @property
    def max_retry_count(self) -> int:
        """
        Returns the value of the '_max_retry_count' attribute of the object.
        If the attribute is not set, it returns 0.

        :return: The value of the '_max_retry_count' attribute or 0 if not set.
        :rtype: int
        """
        return getattr(self, '_max_retry_count', 0) or 0

    @max_retry_count.setter
    def max_retry_count(self, value: int) -> None:
        """
        Set the max_retry_count.
        """

        self._max_retry_count = value
    # minStartUTCDateTime

    @property
    def min_start_utc_date_time(self) -> datetime:
        """
        Get the value of min_start_utc_date_time property.

        Returns:
            datetime: The value of min_start_utc_date_time property.
        """
        dt = getattr(
            self,
            '_min_start_utc_date_time',
            datetime(1753, 1, 1, 0, 0, tzinfo=timezone.utc)
        ) or datetime(1753, 1, 1, 0, 0, tzinfo=timezone.utc)
        if dt is not None and dt.tzinfo is None:
            # Make the datetime aware (UTC) if it is naive
            dt = dt.replace(tzinfo=timezone.utc)
        return dt

    @min_start_utc_date_time.setter
    def min_start_utc_date_time(self, value: datetime) -> None:
        """
        Set the min_start_utc_date_time.
        """
        if value is not None and value.tzinfo is None:
            # If the datetime is naive, assume UTC
            value = value.replace(tzinfo=timezone.utc)
        self._min_start_utc_date_time = value
    # param1,

    @property
    def param_1(self) -> str:
        """
        Returns the Param 1 of the
        dyna_flow_task.

        :return: The Param 1 of the
            dyna_flow_task.
        :rtype: str
        """
        return getattr(self, '_param_1', "") or ""

    @param_1.setter
    def param_1(self, value: str) -> None:
        """
        Set the param_1.
        """

        self._param_1 = value
    # param2,

    @property
    def param_2(self) -> str:
        """
        Returns the Param 2 of the
        dyna_flow_task.

        :return: The Param 2 of the
            dyna_flow_task.
        :rtype: str
        """
        return getattr(self, '_param_2', "") or ""

    @param_2.setter
    def param_2(self, value: str) -> None:
        """
        Set the param_2.
        """

        self._param_2 = value
    # processorIdentifier,

    @property
    def processor_identifier(self) -> str:
        """
        Returns the Processor Identifier of the
        dyna_flow_task.

        :return: The Processor Identifier of the
            dyna_flow_task.
        :rtype: str
        """
        return getattr(self, '_processor_identifier', "") or ""

    @processor_identifier.setter
    def processor_identifier(self, value: str) -> None:
        """
        Set the processor_identifier.
        """

        self._processor_identifier = value
    # requestedUTCDateTime

    @property
    def requested_utc_date_time(self) -> datetime:
        """
        Get the value of requested_utc_date_time property.

        Returns:
            datetime: The value of requested_utc_date_time property.
        """
        dt = getattr(
            self,
            '_requested_utc_date_time',
            datetime(1753, 1, 1, 0, 0, tzinfo=timezone.utc)
        ) or datetime(1753, 1, 1, 0, 0, tzinfo=timezone.utc)
        if dt is not None and dt.tzinfo is None:
            # Make the datetime aware (UTC) if it is naive
            dt = dt.replace(tzinfo=timezone.utc)
        return dt

    @requested_utc_date_time.setter
    def requested_utc_date_time(self, value: datetime) -> None:
        """
        Set the requested_utc_date_time.
        """
        if value is not None and value.tzinfo is None:
            # If the datetime is naive, assume UTC
            value = value.replace(tzinfo=timezone.utc)
        self._requested_utc_date_time = value
    # resultValue,

    @property
    def result_value(self) -> str:
        """
        Returns the ResultValue of the
        dyna_flow_task.

        :return: The ResultValue of the
            dyna_flow_task.
        :rtype: str
        """
        return getattr(self, '_result_value', "") or ""

    @result_value.setter
    def result_value(self, value: str) -> None:
        """
        Set the result_value.
        """

        self._result_value = value
    # retryCount,

    @property
    def retry_count(self) -> int:
        """
        Returns the value of the '_retry_count' attribute of the object.
        If the attribute is not set, it returns 0.

        :return: The value of the '_retry_count' attribute or 0 if not set.
        :rtype: int
        """
        return getattr(self, '_retry_count', 0) or 0

    @retry_count.setter
    def retry_count(self, value: int) -> None:
        """
        Set the retry_count.
        """

        self._retry_count = value
    # startedUTCDateTime

    @property
    def started_utc_date_time(self) -> datetime:
        """
        Get the value of started_utc_date_time property.

        Returns:
            datetime: The value of started_utc_date_time property.
        """
        dt = getattr(
            self,
            '_started_utc_date_time',
            datetime(1753, 1, 1, 0, 0, tzinfo=timezone.utc)
        ) or datetime(1753, 1, 1, 0, 0, tzinfo=timezone.utc)
        if dt is not None and dt.tzinfo is None:
            # Make the datetime aware (UTC) if it is naive
            dt = dt.replace(tzinfo=timezone.utc)
        return dt

    @started_utc_date_time.setter
    def started_utc_date_time(self, value: datetime) -> None:
        """
        Set the started_utc_date_time.
        """
        if value is not None and value.tzinfo is None:
            # If the datetime is naive, assume UTC
            value = value.replace(tzinfo=timezone.utc)
        self._started_utc_date_time = value
    # DynaFlowID
    # dynaFlowTaskTypeID

    @property
    def dyna_flow_task_type_id(self) -> int:
        """
        Get the foreign key ID for the dyna_flow_task_type of the
        dyna_flow_task.

        Returns:
            int: The foreign key ID for the dyna_flow_task_type of the
                dyna_flow_task.
        """
        return getattr(self, '_dyna_flow_task_type_id', 0) or 0

    @dyna_flow_task_type_id.setter
    def dyna_flow_task_type_id(self, value: int) -> None:
        """
        Set the dyna_flow_task_type_id.
        """

        self._dyna_flow_task_type_id = value
    @property
    def dyna_flow_id(self) -> int:
        """
        Get the ID of the dyna_flow associated with this dyna_flow_task.

        Returns:
            int: The ID of the dyna_flow.
        """
        return getattr(self, '_dyna_flow_id', 0) or 0

    @dyna_flow_id.setter
    def dyna_flow_id(self, value: int) -> None:
        """
        Set the dyna_flow_id.
        """

        self._dyna_flow_id = value

    @staticmethod
    def property_list():
        """
        Returns a list of property names for
        the DynaFlowTask model.

        Returns:
            list: A list of property names.
        """

        result = [
            "completed_utc_date_time",
            "dependency_dyna_flow_task_id",
            "description",
            "dyna_flow_id",
            "dyna_flow_subject_code",
            "dyna_flow_task_type_id",
            "is_canceled",
            "is_cancel_requested",
            "is_completed",
            "is_parallel_run_allowed",
            "is_run_task_debug_required",
            "is_started",
            "is_successful",
            "max_retry_count",
            "min_start_utc_date_time",
            "param_1",
            "param_2",
            "processor_identifier",
            "requested_utc_date_time",
            "result_value",
            "retry_count",
            "started_utc_date_time",
# endset  # noqa: E122
            "code"
        ]
        return result


@event.listens_for(DynaFlowTask, 'before_insert')
def set_created_on(
    mapper,
    connection,
    target
):  # pylint: disable=unused-argument
    """
    Set the created on and last update timestamps
    for a DynaFlowTask object.

    Args:
        mapper: The SQLAlchemy mapper.
        connection: The SQLAlchemy connection.
        target: The DynaFlowTask object
        being inserted.

    Returns:
        None
    """
    target.insert_utc_date_time = datetime.now(timezone.utc)
    target.last_update_utc_date_time = datetime.now(timezone.utc)


@event.listens_for(DynaFlowTask, 'before_update')
def set_updated_on(
    mapper,
    connection,
    target
):  # pylint: disable=unused-argument
    """
    Sets the 'last_update_utc_date_time' attribute of
    the target object to the current UTC date and time.

    :param mapper: The SQLAlchemy mapper object.
    :param connection: The SQLAlchemy connection object.
    :param target: The target object to update.
    """
    target.last_update_utc_date_time = datetime.now(timezone.utc)
