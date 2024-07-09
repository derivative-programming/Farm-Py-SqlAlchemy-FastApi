# models/df_maintenance.py  # pylint: disable=duplicate-code
# pylint: disable=unused-import

"""
The DFMaintenance model inherits from
the Base model and is mapped to the
'farm_DFMaintenance' table in the database.
"""
from decimal import Decimal  # noqa: F401
import uuid  # noqa: F401
from datetime import date, datetime, timezone  # noqa: F401
from sqlalchemy_utils import UUIDType
from sqlalchemy import (BigInteger, Boolean,   # noqa: F401
                        Column, Date, DateTime, Float,
                        ForeignKey, Index, Integer, Numeric, String,
                        event, func)
import models.constants.df_maintenance as \
    df_maintenance_constants
from utils.common_functions import snake_case
from .base import Base, EncryptedType  # noqa: F401


class DFMaintenance(Base):
    """
    The DFMaintenance model represents a
    df_maintenance in the farm.
    It inherits from the Base model and is mapped to the
    'farm_DFMaintenance' table in the database.
    """

    __tablename__ = 'farm_' + snake_case('DFMaintenance')

    _df_maintenance_id = Column(
        'df_maintenance_id',
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
    _is_paused = Column(
        'is_paused',
        Boolean,
        default=False,
        index=(
            df_maintenance_constants.
            is_paused_calculatedIsDBColumnIndexed
        ),
        nullable=True)
    _is_scheduled_df_process_request_completed = Column(
        'is_scheduled_df_process_request_completed',
        Boolean,
        default=False,
        index=(
            df_maintenance_constants.
            is_scheduled_df_process_request_completed_calculatedIsDBColumnIndexed
        ),
        nullable=True)
    _is_scheduled_df_process_request_started = Column(
        'is_scheduled_df_process_request_started',
        Boolean,
        default=False,
        index=(
            df_maintenance_constants.
            is_scheduled_df_process_request_started_calculatedIsDBColumnIndexed
        ),
        nullable=True)
    _last_scheduled_df_process_request_utc_date_time = Column(
        'last_scheduled_df_process_request_utc_date_time',
        DateTime,
        default=datetime(1753, 1, 1, 0, 0, tzinfo=timezone.utc),
        index=(
            df_maintenance_constants.
            last_scheduled_df_process_request_utc_date_time_calculatedIsDBColumnIndexed
        ),
        nullable=True)
    _next_scheduled_df_process_request_utc_date_time = Column(
        'next_scheduled_df_process_request_utc_date_time',
        DateTime,
        default=datetime(1753, 1, 1, 0, 0, tzinfo=timezone.utc),
        index=(
            df_maintenance_constants.
            next_scheduled_df_process_request_utc_date_time_calculatedIsDBColumnIndexed
        ),
        nullable=True)
    _pac_id = Column(
        'pac_id',
        Integer,
        ForeignKey('farm_' + snake_case('Pac') + '.pac_id'),
        index=(
            df_maintenance_constants.
            pac_id_calculatedIsDBColumnIndexed
        ),
        nullable=True)
    _paused_by_username = Column(
        'paused_by_username',

        String,

        default="",
        index=(
            df_maintenance_constants.
            paused_by_username_calculatedIsDBColumnIndexed
        ),
        nullable=True)
    _paused_utc_date_time = Column(
        'paused_utc_date_time',
        DateTime,
        default=datetime(1753, 1, 1, 0, 0, tzinfo=timezone.utc),
        index=(
            df_maintenance_constants.
            paused_utc_date_time_calculatedIsDBColumnIndexed
        ),
        nullable=True)
    _scheduled_df_process_request_processor_identifier = Column(
        'scheduled_df_process_request_processor_identifier',

        String,

        default="",
        index=(
            df_maintenance_constants.
            scheduled_df_process_request_processor_identifier_calculatedIsDBColumnIndexed
        ),
        nullable=True)
    pac_code_peek: uuid.UUID = uuid.UUID(int=0)  # PacID  # noqa: E501
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
        self.is_paused = kwargs.get(
            'is_paused', False)
        self.is_scheduled_df_process_request_completed = kwargs.get(
            'is_scheduled_df_process_request_completed', False)
        self.is_scheduled_df_process_request_started = kwargs.get(
            'is_scheduled_df_process_request_started', False)
        self.last_scheduled_df_process_request_utc_date_time = kwargs.get(
            'last_scheduled_df_process_request_utc_date_time',
            datetime(1753, 1, 1, 0, 0, tzinfo=timezone.utc))
        self.next_scheduled_df_process_request_utc_date_time = kwargs.get(
            'next_scheduled_df_process_request_utc_date_time',
            datetime(1753, 1, 1, 0, 0, tzinfo=timezone.utc))
        self.pac_id = kwargs.get(
            'pac_id', 0)
        self.paused_by_username = kwargs.get(
            'paused_by_username', "")
        self.paused_utc_date_time = kwargs.get(
            'paused_utc_date_time',
            datetime(1753, 1, 1, 0, 0, tzinfo=timezone.utc))
        self.scheduled_df_process_request_processor_identifier = kwargs.get(
            'scheduled_df_process_request_processor_identifier', "")
        self.insert_utc_date_time = kwargs.get(
            'insert_utc_date_time',
            datetime(1753, 1, 1, 0, 0, tzinfo=timezone.utc))
        self.last_update_utc_date_time = kwargs.get(
            'last_update_utc_date_time',
            datetime(1753, 1, 1, 0, 0, tzinfo=timezone.utc))
        self.pac_code_peek = kwargs.get(  # PacID
            'pac_code_peek', uuid.UUID(int=0))

    @property
    def code(self):
        """
        Get the code of the df_maintenance.

        Returns:
            UUID: The code of the df_maintenance.
        """
        return uuid.UUID(str(self._code))

    @code.setter
    def code(self, value: uuid.UUID):
        """
        Set the code of the df_maintenance.

        Args:
            value (uuid.UUID): The code to set for the
                df_maintenance.

        Raises:
            TypeError: If the value is not of type uuid.UUID.

        """
        if isinstance(value, uuid.UUID):
            self._code = value
        else:
            self._code = uuid.UUID(value)
        self.last_update_utc_date_time = datetime.now(timezone.utc)

    @property
    def df_maintenance_id(self) -> int:
        """
        Get the ID of the df_maintenance.

        Returns:
            int: The ID of the df_maintenance.
        """
        return getattr(self, '_df_maintenance_id', 0) or 0

    @df_maintenance_id.setter
    def df_maintenance_id(self, value: int) -> None:
        """
        Set the df_maintenance_id.
        """

        self._df_maintenance_id = value

    @property
    def last_change_code(self) -> int:
        """
        Returns the last change code of the
        df_maintenance.

        :return: The last change code of the
            df_maintenance.
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
        df_maintenance object.

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
        df_maintenance.

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
        df_maintenance.

        Returns:
            datetime: The UTC date and time for the
                df_maintenance.
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
        df_maintenance.

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
    # isPaused

    @property
    def is_paused(self) -> bool:
        """
        Check if the delete operation is allowed for the
        df_maintenance.

        Returns:
            bool: True if delete is allowed, False otherwise.
        """
        return getattr(self, '_is_paused', False) or False

    @is_paused.setter
    def is_paused(self, value: bool) -> None:
        """
        Set the is_paused.
        """

        self._is_paused = value
    # isScheduledDFProcessRequestCompleted

    @property
    def is_scheduled_df_process_request_completed(self) -> bool:
        """
        Check if the delete operation is allowed for the
        df_maintenance.

        Returns:
            bool: True if delete is allowed, False otherwise.
        """
        return getattr(self, '_is_scheduled_df_process_request_completed', False) or False

    @is_scheduled_df_process_request_completed.setter
    def is_scheduled_df_process_request_completed(self, value: bool) -> None:
        """
        Set the is_scheduled_df_process_request_completed.
        """

        self._is_scheduled_df_process_request_completed = value
    # isScheduledDFProcessRequestStarted

    @property
    def is_scheduled_df_process_request_started(self) -> bool:
        """
        Check if the delete operation is allowed for the
        df_maintenance.

        Returns:
            bool: True if delete is allowed, False otherwise.
        """
        return getattr(self, '_is_scheduled_df_process_request_started', False) or False

    @is_scheduled_df_process_request_started.setter
    def is_scheduled_df_process_request_started(self, value: bool) -> None:
        """
        Set the is_scheduled_df_process_request_started.
        """

        self._is_scheduled_df_process_request_started = value
    # lastScheduledDFProcessRequestUTCDateTime

    @property
    def last_scheduled_df_process_request_utc_date_time(self) -> datetime:
        """
        Get the value of last_scheduled_df_process_request_utc_date_time property.

        Returns:
            datetime: The value of last_scheduled_df_process_request_utc_date_time property.
        """
        dt = getattr(
            self,
            '_last_scheduled_df_process_request_utc_date_time',
            datetime(1753, 1, 1, 0, 0, tzinfo=timezone.utc)
        ) or datetime(1753, 1, 1, 0, 0, tzinfo=timezone.utc)
        if dt is not None and dt.tzinfo is None:
            # Make the datetime aware (UTC) if it is naive
            dt = dt.replace(tzinfo=timezone.utc)
        return dt

    @last_scheduled_df_process_request_utc_date_time.setter
    def last_scheduled_df_process_request_utc_date_time(self, value: datetime) -> None:
        """
        Set the last_scheduled_df_process_request_utc_date_time.
        """
        if value is not None and value.tzinfo is None:
            # If the datetime is naive, assume UTC
            value = value.replace(tzinfo=timezone.utc)
        self._last_scheduled_df_process_request_utc_date_time = value
    # nextScheduledDFProcessRequestUTCDateTime

    @property
    def next_scheduled_df_process_request_utc_date_time(self) -> datetime:
        """
        Get the value of next_scheduled_df_process_request_utc_date_time property.

        Returns:
            datetime: The value of next_scheduled_df_process_request_utc_date_time property.
        """
        dt = getattr(
            self,
            '_next_scheduled_df_process_request_utc_date_time',
            datetime(1753, 1, 1, 0, 0, tzinfo=timezone.utc)
        ) or datetime(1753, 1, 1, 0, 0, tzinfo=timezone.utc)
        if dt is not None and dt.tzinfo is None:
            # Make the datetime aware (UTC) if it is naive
            dt = dt.replace(tzinfo=timezone.utc)
        return dt

    @next_scheduled_df_process_request_utc_date_time.setter
    def next_scheduled_df_process_request_utc_date_time(self, value: datetime) -> None:
        """
        Set the next_scheduled_df_process_request_utc_date_time.
        """
        if value is not None and value.tzinfo is None:
            # If the datetime is naive, assume UTC
            value = value.replace(tzinfo=timezone.utc)
        self._next_scheduled_df_process_request_utc_date_time = value
    # PacID
    # pausedByUsername

    @property
    def paused_by_username(self) -> str:
        """
        Returns the Paused By Username of the
        df_maintenance.

        :return: The Paused By Username of the
            df_maintenance.
        :rtype: str
        """
        return getattr(self, '_paused_by_username', "") or ""

    @paused_by_username.setter
    def paused_by_username(self, value: str) -> None:
        """
        Set the paused_by_username.
        """

        self._paused_by_username = value
    # pausedUTCDateTime

    @property
    def paused_utc_date_time(self) -> datetime:
        """
        Get the value of paused_utc_date_time property.

        Returns:
            datetime: The value of paused_utc_date_time property.
        """
        dt = getattr(
            self,
            '_paused_utc_date_time',
            datetime(1753, 1, 1, 0, 0, tzinfo=timezone.utc)
        ) or datetime(1753, 1, 1, 0, 0, tzinfo=timezone.utc)
        if dt is not None and dt.tzinfo is None:
            # Make the datetime aware (UTC) if it is naive
            dt = dt.replace(tzinfo=timezone.utc)
        return dt

    @paused_utc_date_time.setter
    def paused_utc_date_time(self, value: datetime) -> None:
        """
        Set the paused_utc_date_time.
        """
        if value is not None and value.tzinfo is None:
            # If the datetime is naive, assume UTC
            value = value.replace(tzinfo=timezone.utc)
        self._paused_utc_date_time = value
    # scheduledDFProcessRequestProcessorIdentifier

    @property
    def scheduled_df_process_request_processor_identifier(self) -> str:
        """
        Returns the Scheduled DF Process Request Processor Identifier of the
        df_maintenance.

        :return: The Scheduled DF Process Request Processor Identifier of the
            df_maintenance.
        :rtype: str
        """
        return getattr(self, '_scheduled_df_process_request_processor_identifier', "") or ""

    @scheduled_df_process_request_processor_identifier.setter
    def scheduled_df_process_request_processor_identifier(self, value: str) -> None:
        """
        Set the scheduled_df_process_request_processor_identifier.
        """

        self._scheduled_df_process_request_processor_identifier = value
    # PacID
    @property
    def pac_id(self) -> int:
        """
        Get the ID of the pac associated with this df_maintenance.

        Returns:
            int: The ID of the pac.
        """
        return getattr(self, '_pac_id', 0) or 0

    @pac_id.setter
    def pac_id(self, value: int) -> None:
        """
        Set the pac_id.
        """

        self._pac_id = value

    @staticmethod
    def property_list():
        """
        Returns a list of property names for
        the DFMaintenance model.

        Returns:
            list: A list of property names.
        """

        result = [
            "is_paused",
            "is_scheduled_df_process_request_completed",
            "is_scheduled_df_process_request_started",
            "last_scheduled_df_process_request_utc_date_time",
            "next_scheduled_df_process_request_utc_date_time",
            "pac_id",
            "paused_by_username",
            "paused_utc_date_time",
            "scheduled_df_process_request_processor_identifier",
# endset  # noqa: E122
            "code"
        ]
        return result


@event.listens_for(DFMaintenance, 'before_insert')
def set_created_on(
    mapper,
    connection,
    target
):  # pylint: disable=unused-argument
    """
    Set the created on and last update timestamps
    for a DFMaintenance object.

    Args:
        mapper: The SQLAlchemy mapper.
        connection: The SQLAlchemy connection.
        target: The DFMaintenance object
        being inserted.

    Returns:
        None
    """
    target.insert_utc_date_time = datetime.now(timezone.utc)
    target.last_update_utc_date_time = datetime.now(timezone.utc)


@event.listens_for(DFMaintenance, 'before_update')
def set_updated_on(
    mapper,
    connection,
    target
):  # pylint: disable=unused-argument
    """
    Sets the 'last_update_utc_date_time'
    attribute of
    the target object to the current UTC date and time.

    :param mapper: The SQLAlchemy mapper object.
    :param connection: The SQLAlchemy connection object.
    :param target: The target object to update.
    """
    target.last_update_utc_date_time = datetime.now(timezone.utc)
