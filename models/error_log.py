# models/error_log.py
# pylint: disable=unused-import

"""
The ErrorLog model inherits from
the Base model and is mapped to the
'farm_ErrorLog' table in the database.
"""
from decimal import Decimal
import uuid
from datetime import date, datetime
from sqlalchemy_utils import UUIDType
from sqlalchemy import (BigInteger, Boolean,   # noqa: F401
                        Column, Date, DateTime, Float,
                        ForeignKey, Index, Integer, Numeric, String,
                        event, func)
import models.constants.error_log as error_log_constants
from utils.common_functions import snake_case
from .base import Base, EncryptedType  # noqa: F401


class ErrorLog(Base):
    """
    The ErrorLog model represents a
    error_log in the farm.
    It inherits from the Base model and is mapped to the
    'farm_ErrorLog' table in the database.
    """

    __tablename__ = 'farm_' + snake_case('ErrorLog')

    _error_log_id = Column(
        'error_log_id',
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
    _browser_code = Column(
        'browser_code',
        UUIDType(binary=False),
        default=uuid.uuid4,
        index=(
            error_log_constants.
            browser_code_calculatedIsDBColumnIndexed
        ),
        nullable=True)
    _context_code = Column(
        'context_code',
        UUIDType(binary=False),
        default=uuid.uuid4,
        index=(
            error_log_constants.
            context_code_calculatedIsDBColumnIndexed
        ),
        nullable=True)
    _created_utc_date_time = Column(
        'created_utc_date_time',
        DateTime,
        default=datetime(1753, 1, 1),
        index=(
            error_log_constants.
            created_utc_date_time_calculatedIsDBColumnIndexed
        ),
        nullable=True)
    _description = Column(
        'description',

        String,

        default="",
        index=(
            error_log_constants.
            description_calculatedIsDBColumnIndexed
        ),
        nullable=True)
    _is_client_side_error = Column(
        'is_client_side_error',
        Boolean,
        default=False,
        index=(
            error_log_constants.
            is_client_side_error_calculatedIsDBColumnIndexed
        ),
        nullable=True)
    _is_resolved = Column(
        'is_resolved',
        Boolean,
        default=False,
        index=(
            error_log_constants.
            is_resolved_calculatedIsDBColumnIndexed
        ),
        nullable=True)
    _pac_id = Column(
        'pac_id',
        Integer,
        ForeignKey('farm_' + snake_case('Pac') + '.pac_id'),
        index=(
            error_log_constants.
            pac_id_calculatedIsDBColumnIndexed
        ),
        nullable=True)
    _url = Column(
        'url',

        String,

        default="",
        index=(
            error_log_constants.
            url_calculatedIsDBColumnIndexed
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
        self.browser_code = kwargs.get(
            'browser_code', uuid.uuid4())
        self.context_code = kwargs.get(
            'context_code', uuid.uuid4())
        self.created_utc_date_time = kwargs.get(
            'created_utc_date_time', datetime(1753, 1, 1))
        self.description = kwargs.get(
            'description', "")
        self.is_client_side_error = kwargs.get(
            'is_client_side_error', False)
        self.is_resolved = kwargs.get(
            'is_resolved', False)
        self.pac_id = kwargs.get(
            'pac_id', 0)
        self.url = kwargs.get(
            'url', "")
        self.insert_utc_date_time = kwargs.get(
            'insert_utc_date_time', datetime(1753, 1, 1))
        self.last_update_utc_date_time = kwargs.get(
            'last_update_utc_date_time', datetime(1753, 1, 1))
        self.pac_code_peek = kwargs.get(  # PacID
            'pac_code_peek', uuid.UUID(int=0))

    @property
    def code(self):
        """
        Get the code of the error_log.

        Returns:
            UUID: The code of the error_log.
        """
        return uuid.UUID(str(self._code))

    @code.setter
    def code(self, value: uuid.UUID):
        """
        Set the code of the error_log.

        Args:
            value (uuid.UUID): The code to set for the error_log.

        Raises:
            TypeError: If the value is not of type uuid.UUID.

        """
        if isinstance(value, uuid.UUID):
            self._code = value
        else:
            self._code = uuid.UUID(value)
        self.last_update_utc_date_time = datetime.utcnow()

    @property
    def error_log_id(self) -> int:
        """
        Get the ID of the error_log.

        Returns:
            int: The ID of the error_log.
        """
        return getattr(self, '_error_log_id', 0) or 0

    @error_log_id.setter
    def error_log_id(self, value: int) -> None:
        """
        Set the error_log_id.
        """

        self._error_log_id = value

    @property
    def last_change_code(self) -> int:
        """
        Returns the last change code of the error_log.

        :return: The last change code of the error_log.
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
        error_log object.

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
        self.last_update_utc_date_time = datetime.utcnow()

    @property
    def last_update_user_id(self):
        """
        Returns the UUID of the last user who updated the error_log.

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
        self.last_update_utc_date_time = datetime.utcnow()

    @property
    def insert_utc_date_time(self) -> datetime:
        """
        Inserts the UTC date and time for the error_log.

        Returns:
            datetime: The UTC date and time for the error_log.
        """
        return getattr(
            self,
            '_insert_utc_date_time',
            datetime(1753, 1, 1)
        ) or datetime(1753, 1, 1)

    @insert_utc_date_time.setter
    def insert_utc_date_time(self, value: datetime) -> None:
        """
        Set the insert_utc_date_time.
        """

        self._insert_utc_date_time = value

    @property
    def last_update_utc_date_time(self) -> datetime:
        """
        Returns the last update UTC date and time of the error_log.

        :return: A datetime object representing the
            last update UTC date and time.
        """
        return getattr(
            self,
            '_last_update_utc_date_time',
            datetime(1753, 1, 1)
        ) or datetime(1753, 1, 1)

    @last_update_utc_date_time.setter
    def last_update_utc_date_time(self, value: datetime) -> None:
        """
        Set the last_update_utc_date_time.
        """

        self._last_update_utc_date_time = value
    # browserCode,

    @property
    def browser_code(self):
        """
        Returns the unique identifier as a UUID object.

        Returns:
            uuid.UUID: The unique identifier value.
        """

        return uuid.UUID(str(self._browser_code))

    @browser_code.setter
    def browser_code(self, value):
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
            self._browser_code = value
        else:
            try:
                self._browser_code = uuid.UUID(value)
            except ValueError as e:
                raise ValueError(f"Invalid UUID value: {value}") from e
        self.last_update_utc_date_time = datetime.utcnow()
    # contextCode,

    @property
    def context_code(self):
        """
        Returns the unique identifier as a UUID object.

        Returns:
            uuid.UUID: The unique identifier value.
        """

        return uuid.UUID(str(self._context_code))

    @context_code.setter
    def context_code(self, value):
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
            self._context_code = value
        else:
            try:
                self._context_code = uuid.UUID(value)
            except ValueError as e:
                raise ValueError(f"Invalid UUID value: {value}") from e
        self.last_update_utc_date_time = datetime.utcnow()
    # createdUTCDateTime

    @property
    def created_utc_date_time(self) -> datetime:
        """
        Get the value of created_utc_date_time property.

        Returns:
            datetime: The value of created_utc_date_time property.
        """
        return getattr(
            self,
            '_created_utc_date_time',
            datetime(1753, 1, 1)
        ) or datetime(1753, 1, 1)

    @created_utc_date_time.setter
    def created_utc_date_time(self, value: datetime) -> None:
        """
        Set the created_utc_date_time.
        """

        self._created_utc_date_time = value
    # description,

    @property
    def description(self) -> str:
        """
        Returns the Description of the error_log.

        :return: The Description of the error_log.
        :rtype: str
        """
        return getattr(self, '_description', "") or ""

    @description.setter
    def description(self, value: str) -> None:
        """
        Set the description.
        """

        self._description = value
    # isClientSideError,

    @property
    def is_client_side_error(self) -> bool:
        """
        Check if the delete operation is allowed for the error_log.

        Returns:
            bool: True if delete is allowed, False otherwise.
        """
        return getattr(self, '_is_client_side_error', False) or False

    @is_client_side_error.setter
    def is_client_side_error(self, value: bool) -> None:
        """
        Set the is_client_side_error.
        """

        self._is_client_side_error = value
    # isResolved,

    @property
    def is_resolved(self) -> bool:
        """
        Check if the delete operation is allowed for the error_log.

        Returns:
            bool: True if delete is allowed, False otherwise.
        """
        return getattr(self, '_is_resolved', False) or False

    @is_resolved.setter
    def is_resolved(self, value: bool) -> None:
        """
        Set the is_resolved.
        """

        self._is_resolved = value
    # PacID
    # url,

    @property
    def url(self) -> str:
        """
        Returns the Url of the error_log.

        :return: The Url of the error_log.
        :rtype: str
        """
        return getattr(self, '_url', "") or ""

    @url.setter
    def url(self, value: str) -> None:
        """
        Set the url.
        """

        self._url = value
    # PacID
    @property
    def pac_id(self) -> int:
        """
        Get the ID of the pac associated with this error_log.

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
        the ErrorLog model.

        Returns:
            list: A list of property names.
        """

        result = [
            "browser_code",
            "context_code",
            "created_utc_date_time",
            "description",
            "is_client_side_error",
            "is_resolved",
            "pac_id",
            "url",
# endset  # noqa: E122
            "code"
        ]
        return result


@event.listens_for(ErrorLog, 'before_insert')
def set_created_on(
    mapper,
    connection,
    target
):  # pylint: disable=unused-argument
    """
    Set the created on and last update timestamps
    for a ErrorLog object.

    Args:
        mapper: The SQLAlchemy mapper.
        connection: The SQLAlchemy connection.
        target: The ErrorLog object
        being inserted.

    Returns:
        None
    """
    target.insert_utc_date_time = datetime.utcnow()
    target.last_update_utc_date_time = datetime.utcnow()


@event.listens_for(ErrorLog, 'before_update')
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
    target.last_update_utc_date_time = datetime.utcnow()

