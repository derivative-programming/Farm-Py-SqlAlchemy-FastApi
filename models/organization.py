# models/organization.py  # pylint: disable=duplicate-code
# pylint: disable=unused-import

"""
The Organization model inherits from
the Base model and is mapped to the
'farm_Organization' table in the database.
"""
from decimal import Decimal  # noqa: F401
import uuid  # noqa: F401
from datetime import date, datetime, timezone  # noqa: F401
from sqlalchemy_utils import UUIDType
from sqlalchemy import (BigInteger, Boolean,   # noqa: F401
                        Column, Date, DateTime, Float,
                        ForeignKey, Index, Integer, Numeric, String,
                        event, func)
import models.constants.organization as \
    organization_constants
from utils.common_functions import snake_case
from .base import Base, EncryptedType  # noqa: F401


class Organization(Base):
    """
    The Organization model represents a
    organization in the farm.
    It inherits from the Base model and is mapped to the
    'farm_Organization' table in the database.
    """

    __tablename__ = 'farm_' + snake_case('Organization')

    _organization_id = Column(
        'organization_id',
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
    _name = Column(
        'name',

        String,

        default="",
        index=(
            organization_constants.
            name_calculatedIsDBColumnIndexed
        ),
        nullable=True)
    _tac_id = Column(
        'tac_id',
        Integer,
        ForeignKey('farm_' + snake_case('Tac') + '.tac_id'),
        index=(
            organization_constants.
            tac_id_calculatedIsDBColumnIndexed
        ),
        nullable=True)
    tac_code_peek: uuid.UUID = uuid.UUID(int=0)  # TacID  # noqa: E501
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
        self.name = kwargs.get(
            'name', "")
        self.tac_id = kwargs.get(
            'tac_id', 0)
        self.insert_utc_date_time = kwargs.get(
            'insert_utc_date_time', datetime(1753, 1, 1, 0, 0, tzinfo=timezone.utc))
        self.last_update_utc_date_time = kwargs.get(
            'last_update_utc_date_time', datetime(1753, 1, 1, 0, 0, tzinfo=timezone.utc))
        self.tac_code_peek = kwargs.get(  # TacID
            'tac_code_peek', uuid.UUID(int=0))

    @property
    def code(self):
        """
        Get the code of the organization.

        Returns:
            UUID: The code of the organization.
        """
        return uuid.UUID(str(self._code))

    @code.setter
    def code(self, value: uuid.UUID):
        """
        Set the code of the organization.

        Args:
            value (uuid.UUID): The code to set for the
                organization.

        Raises:
            TypeError: If the value is not of type uuid.UUID.

        """
        if isinstance(value, uuid.UUID):
            self._code = value
        else:
            self._code = uuid.UUID(value)
        self.last_update_utc_date_time = datetime.now(timezone.utc)

    @property
    def organization_id(self) -> int:
        """
        Get the ID of the organization.

        Returns:
            int: The ID of the organization.
        """
        return getattr(self, '_organization_id', 0) or 0

    @organization_id.setter
    def organization_id(self, value: int) -> None:
        """
        Set the organization_id.
        """

        self._organization_id = value

    @property
    def last_change_code(self) -> int:
        """
        Returns the last change code of the
        organization.

        :return: The last change code of the
            organization.
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
        organization object.

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
        organization.

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
        organization.

        Returns:
            datetime: The UTC date and time for the
                organization.
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
        organization.

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
    # name

    @property
    def name(self) -> str:
        """
        Returns the Name of the
        organization.

        :return: The Name of the
            organization.
        :rtype: str
        """
        return getattr(self, '_name', "") or ""

    @name.setter
    def name(self, value: str) -> None:
        """
        Set the name.
        """

        self._name = value
    # TacID
    # TacID
    @property
    def tac_id(self) -> int:
        """
        Get the ID of the tac associated with this organization.

        Returns:
            int: The ID of the tac.
        """
        return getattr(self, '_tac_id', 0) or 0

    @tac_id.setter
    def tac_id(self, value: int) -> None:
        """
        Set the tac_id.
        """

        self._tac_id = value

    @staticmethod
    def property_list():
        """
        Returns a list of property names for
        the Organization model.

        Returns:
            list: A list of property names.
        """

        result = [
            "name",
            "tac_id",
# endset  # noqa: E122
            "code"
        ]
        return result


@event.listens_for(Organization, 'before_insert')
def set_created_on(
    mapper,
    connection,
    target
):  # pylint: disable=unused-argument
    """
    Set the created on and last update timestamps
    for a Organization object.

    Args:
        mapper: The SQLAlchemy mapper.
        connection: The SQLAlchemy connection.
        target: The Organization object
        being inserted.

    Returns:
        None
    """
    target.insert_utc_date_time = datetime.now(timezone.utc)
    target.last_update_utc_date_time = datetime.now(timezone.utc)


@event.listens_for(Organization, 'before_update')
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
