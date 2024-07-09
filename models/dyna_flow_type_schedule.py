# models/dyna_flow_type_schedule.py  # pylint: disable=duplicate-code # noqa: E501
# pylint: disable=unused-import

"""
The DynaFlowTypeSchedule model inherits from
the Base model and is mapped to the
'farm_DynaFlowTypeSchedule' table in the database.
"""
from decimal import Decimal  # noqa: F401
import uuid  # noqa: F401
from datetime import date, datetime, timezone  # noqa: F401
from sqlalchemy_utils import UUIDType
from sqlalchemy import (BigInteger, Boolean,   # noqa: F401
                        Column, Date, DateTime, Float,
                        ForeignKey, Index, Integer, Numeric, String,
                        event, func)
import models.constants.dyna_flow_type_schedule as \
    dyna_flow_type_schedule_constants
from utils.common_functions import snake_case
from .base import Base, EncryptedType  # noqa: F401


class DynaFlowTypeSchedule(Base):
    """
    The DynaFlowTypeSchedule model represents a
    dyna_flow_type_schedule in the farm.
    It inherits from the Base model and is mapped to the
    'farm_DynaFlowTypeSchedule' table in the database.
    """

    __tablename__ = 'farm_' + snake_case('DynaFlowTypeSchedule')

    _dyna_flow_type_schedule_id = Column(
        'dyna_flow_type_schedule_id',
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
    _dyna_flow_type_id = Column(
        'dyna_flow_type_id',
        Integer,
        ForeignKey('farm_' + snake_case('DynaFlowType') + '.dyna_flow_type_id'),
        index=(
            dyna_flow_type_schedule_constants.
            dyna_flow_type_id_calculatedIsDBColumnIndexed
        ),
        nullable=True)
    _frequency_in_hours = Column(
        'frequency_in_hours',
        Integer,
        default=0,
        index=(
            dyna_flow_type_schedule_constants.
            frequency_in_hours_calculatedIsDBColumnIndexed
        ),
        nullable=True)
    _is_active = Column(
        'is_active',
        Boolean,
        default=False,
        index=(
            dyna_flow_type_schedule_constants.
            is_active_calculatedIsDBColumnIndexed
        ),
        nullable=True)
    _last_utc_date_time = Column(
        'last_utc_date_time',
        DateTime,
        default=datetime(1753, 1, 1, 0, 0, tzinfo=timezone.utc),
        index=(
            dyna_flow_type_schedule_constants.
            last_utc_date_time_calculatedIsDBColumnIndexed
        ),
        nullable=True)
    _next_utc_date_time = Column(
        'next_utc_date_time',
        DateTime,
        default=datetime(1753, 1, 1, 0, 0, tzinfo=timezone.utc),
        index=(
            dyna_flow_type_schedule_constants.
            next_utc_date_time_calculatedIsDBColumnIndexed
        ),
        nullable=True)
    _pac_id = Column(
        'pac_id',
        Integer,
        ForeignKey('farm_' + snake_case('Pac') + '.pac_id'),
        index=(
            dyna_flow_type_schedule_constants.
            pac_id_calculatedIsDBColumnIndexed
        ),
        nullable=True)
    dyna_flow_type_code_peek: uuid.UUID = uuid.UUID(int=0)  # DynaFlowTypeID  # noqa: E501
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
        self.dyna_flow_type_id = kwargs.get(
            'dyna_flow_type_id', 0)
        self.frequency_in_hours = kwargs.get(
            'frequency_in_hours', 0)
        self.is_active = kwargs.get(
            'is_active', False)
        self.last_utc_date_time = kwargs.get(
            'last_utc_date_time',
            datetime(1753, 1, 1, 0, 0, tzinfo=timezone.utc))
        self.next_utc_date_time = kwargs.get(
            'next_utc_date_time',
            datetime(1753, 1, 1, 0, 0, tzinfo=timezone.utc))
        self.pac_id = kwargs.get(
            'pac_id', 0)
        self.insert_utc_date_time = kwargs.get(
            'insert_utc_date_time',
            datetime(1753, 1, 1, 0, 0, tzinfo=timezone.utc))
        self.last_update_utc_date_time = kwargs.get(
            'last_update_utc_date_time',
            datetime(1753, 1, 1, 0, 0, tzinfo=timezone.utc))
        self.dyna_flow_type_code_peek = kwargs.get(  # DynaFlowTypeID
            'dyna_flow_type_code_peek', uuid.UUID(int=0))
        self.pac_code_peek = kwargs.get(  # PacID
            'pac_code_peek', uuid.UUID(int=0))

    @property
    def code(self):
        """
        Get the code of the dyna_flow_type_schedule.

        Returns:
            UUID: The code of the dyna_flow_type_schedule.
        """
        return uuid.UUID(str(self._code))

    @code.setter
    def code(self, value: uuid.UUID):
        """
        Set the code of the dyna_flow_type_schedule.

        Args:
            value (uuid.UUID): The code to set for the
                dyna_flow_type_schedule.

        Raises:
            TypeError: If the value is not of type uuid.UUID.

        """
        if isinstance(value, uuid.UUID):
            self._code = value
        else:
            self._code = uuid.UUID(value)
        self.last_update_utc_date_time = datetime.now(timezone.utc)

    @property
    def dyna_flow_type_schedule_id(self) -> int:
        """
        Get the ID of the dyna_flow_type_schedule.

        Returns:
            int: The ID of the dyna_flow_type_schedule.
        """
        return getattr(self, '_dyna_flow_type_schedule_id', 0) or 0

    @dyna_flow_type_schedule_id.setter
    def dyna_flow_type_schedule_id(self, value: int) -> None:
        """
        Set the dyna_flow_type_schedule_id.
        """

        self._dyna_flow_type_schedule_id = value

    @property
    def last_change_code(self) -> int:
        """
        Returns the last change code of the
        dyna_flow_type_schedule.

        :return: The last change code of the
            dyna_flow_type_schedule.
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
        dyna_flow_type_schedule object.

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
        dyna_flow_type_schedule.

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
        dyna_flow_type_schedule.

        Returns:
            datetime: The UTC date and time for the
                dyna_flow_type_schedule.
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
        dyna_flow_type_schedule.

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
    # dynaFlowTypeID
    # frequencyInHours

    @property
    def frequency_in_hours(self) -> int:
        """
        Returns the value of the '_frequency_in_hours'
            attribute of the object.
        If the attribute is not set, it returns 0.

        :return: The value of the '_frequency_in_hours'
            attribute or 0 if not set.
        :rtype: int
        """
        return getattr(self, '_frequency_in_hours', 0) or 0

    @frequency_in_hours.setter
    def frequency_in_hours(self, value: int) -> None:
        """
        Set the frequency_in_hours.
        """

        self._frequency_in_hours = value
    # isActive

    @property
    def is_active(self) -> bool:
        """
        Check if the delete operation is allowed for the
        dyna_flow_type_schedule.

        Returns:
            bool: True if delete is allowed, False otherwise.
        """
        return getattr(self, '_is_active', False) or False

    @is_active.setter
    def is_active(self, value: bool) -> None:
        """
        Set the is_active.
        """

        self._is_active = value
    # lastUTCDateTime

    @property
    def last_utc_date_time(self) -> datetime:
        """
        Get the value of last_utc_date_time property.

        Returns:
            datetime: The value of last_utc_date_time property.
        """
        dt = getattr(
            self,
            '_last_utc_date_time',
            datetime(1753, 1, 1, 0, 0, tzinfo=timezone.utc)
        ) or datetime(1753, 1, 1, 0, 0, tzinfo=timezone.utc)
        if dt is not None and dt.tzinfo is None:
            # Make the datetime aware (UTC) if it is naive
            dt = dt.replace(tzinfo=timezone.utc)
        return dt

    @last_utc_date_time.setter
    def last_utc_date_time(self, value: datetime) -> None:
        """
        Set the last_utc_date_time.
        """
        if value is not None and value.tzinfo is None:
            # If the datetime is naive, assume UTC
            value = value.replace(tzinfo=timezone.utc)
        self._last_utc_date_time = value
    # nextUTCDateTime

    @property
    def next_utc_date_time(self) -> datetime:
        """
        Get the value of next_utc_date_time property.

        Returns:
            datetime: The value of next_utc_date_time property.
        """
        dt = getattr(
            self,
            '_next_utc_date_time',
            datetime(1753, 1, 1, 0, 0, tzinfo=timezone.utc)
        ) or datetime(1753, 1, 1, 0, 0, tzinfo=timezone.utc)
        if dt is not None and dt.tzinfo is None:
            # Make the datetime aware (UTC) if it is naive
            dt = dt.replace(tzinfo=timezone.utc)
        return dt

    @next_utc_date_time.setter
    def next_utc_date_time(self, value: datetime) -> None:
        """
        Set the next_utc_date_time.
        """
        if value is not None and value.tzinfo is None:
            # If the datetime is naive, assume UTC
            value = value.replace(tzinfo=timezone.utc)
        self._next_utc_date_time = value
    # PacID
    # dynaFlowTypeID

    @property
    def dyna_flow_type_id(self) -> int:
        """
        Get the foreign key ID for the dyna_flow_type of the
        dyna_flow_type_schedule.

        Returns:
            int: The foreign key ID for the dyna_flow_type of the
                dyna_flow_type_schedule.
        """
        return getattr(self, '_dyna_flow_type_id', 0) or 0

    @dyna_flow_type_id.setter
    def dyna_flow_type_id(self, value: int) -> None:
        """
        Set the dyna_flow_type_id.
        """

        self._dyna_flow_type_id = value
    # PacID
    @property
    def pac_id(self) -> int:
        """
        Get the ID of the pac associated with this dyna_flow_type_schedule.

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
        the DynaFlowTypeSchedule model.

        Returns:
            list: A list of property names.
        """

        result = [
            "dyna_flow_type_id",
            "frequency_in_hours",
            "is_active",
            "last_utc_date_time",
            "next_utc_date_time",
            "pac_id",
# endset  # noqa: E122
            "code"
        ]
        return result


@event.listens_for(DynaFlowTypeSchedule, 'before_insert')
def set_created_on(
    mapper,
    connection,
    target
):  # pylint: disable=unused-argument
    """
    Set the created on and last update timestamps
    for a DynaFlowTypeSchedule object.

    Args:
        mapper: The SQLAlchemy mapper.
        connection: The SQLAlchemy connection.
        target: The DynaFlowTypeSchedule object
        being inserted.

    Returns:
        None
    """
    target.insert_utc_date_time = datetime.now(timezone.utc)
    target.last_update_utc_date_time = datetime.now(timezone.utc)


@event.listens_for(DynaFlowTypeSchedule, 'before_update')
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
