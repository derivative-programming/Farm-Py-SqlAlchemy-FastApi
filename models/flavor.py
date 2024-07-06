# models/flavor.py  # pylint: disable=duplicate-code
# pylint: disable=unused-import

"""
The Flavor model inherits from
the Base model and is mapped to the
'farm_Flavor' table in the database.
"""
from decimal import Decimal  # noqa: F401
import uuid  # noqa: F401
from datetime import date, datetime, timezone  # noqa: F401
from sqlalchemy_utils import UUIDType
from sqlalchemy import (BigInteger, Boolean,   # noqa: F401
                        Column, Date, DateTime, Float,
                        ForeignKey, Index, Integer, Numeric, String,
                        event, func)
import models.constants.flavor as \
    flavor_constants
from utils.common_functions import snake_case
from .base import Base, EncryptedType  # noqa: F401


class Flavor(Base):
    """
    The Flavor model represents a
    flavor in the farm.
    It inherits from the Base model and is mapped to the
    'farm_Flavor' table in the database.
    """

    __tablename__ = 'farm_' + snake_case('Flavor')

    _flavor_id = Column(
        'flavor_id',
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
    _description = Column(
        'description',

        String,

        default="",
        index=(
            flavor_constants.
            description_calculatedIsDBColumnIndexed
        ),
        nullable=True)
    _display_order = Column(
        'display_order',
        Integer,
        default=0,
        index=(
            flavor_constants.
            display_order_calculatedIsDBColumnIndexed
        ),
        nullable=True)
    _is_active = Column(
        'is_active',
        Boolean,
        default=False,
        index=(
            flavor_constants.
            is_active_calculatedIsDBColumnIndexed
        ),
        nullable=True)
    _lookup_enum_name = Column(
        'lookup_enum_name',

        String,

        default="",
        index=(
            flavor_constants.
            lookup_enum_name_calculatedIsDBColumnIndexed
        ),
        nullable=True)
    _name = Column(
        'name',

        String,

        default="",
        index=(
            flavor_constants.
            name_calculatedIsDBColumnIndexed
        ),
        nullable=True)
    _pac_id = Column(
        'pac_id',
        Integer,
        ForeignKey('farm_' + snake_case('Pac') + '.pac_id'),
        index=(
            flavor_constants.
            pac_id_calculatedIsDBColumnIndexed
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
        self.description = kwargs.get(
            'description', "")
        self.display_order = kwargs.get(
            'display_order', 0)
        self.is_active = kwargs.get(
            'is_active', False)
        self.lookup_enum_name = kwargs.get(
            'lookup_enum_name', "")
        self.name = kwargs.get(
            'name', "")
        self.pac_id = kwargs.get(
            'pac_id', 0)
        self.insert_utc_date_time = kwargs.get(
            'insert_utc_date_time', datetime(1753, 1, 1, 0, 0, tzinfo=timezone.utc))
        self.last_update_utc_date_time = kwargs.get(
            'last_update_utc_date_time', datetime(1753, 1, 1, 0, 0, tzinfo=timezone.utc))
        self.pac_code_peek = kwargs.get(  # PacID
            'pac_code_peek', uuid.UUID(int=0))

    @property
    def code(self):
        """
        Get the code of the flavor.

        Returns:
            UUID: The code of the flavor.
        """
        return uuid.UUID(str(self._code))

    @code.setter
    def code(self, value: uuid.UUID):
        """
        Set the code of the flavor.

        Args:
            value (uuid.UUID): The code to set for the
                flavor.

        Raises:
            TypeError: If the value is not of type uuid.UUID.

        """
        if isinstance(value, uuid.UUID):
            self._code = value
        else:
            self._code = uuid.UUID(value)
        self.last_update_utc_date_time = datetime.now(timezone.utc)

    @property
    def flavor_id(self) -> int:
        """
        Get the ID of the flavor.

        Returns:
            int: The ID of the flavor.
        """
        return getattr(self, '_flavor_id', 0) or 0

    @flavor_id.setter
    def flavor_id(self, value: int) -> None:
        """
        Set the flavor_id.
        """

        self._flavor_id = value

    @property
    def last_change_code(self) -> int:
        """
        Returns the last change code of the
        flavor.

        :return: The last change code of the
            flavor.
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
        flavor object.

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
        flavor.

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
        flavor.

        Returns:
            datetime: The UTC date and time for the
                flavor.
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
        flavor.

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
    # description,

    @property
    def description(self) -> str:
        """
        Returns the Description of the
        flavor.

        :return: The Description of the
            flavor.
        :rtype: str
        """
        return getattr(self, '_description', "") or ""

    @description.setter
    def description(self, value: str) -> None:
        """
        Set the description.
        """

        self._description = value
    # displayOrder,

    @property
    def display_order(self) -> int:
        """
        Returns the value of the '_display_order' attribute of the object.
        If the attribute is not set, it returns 0.

        :return: The value of the '_display_order' attribute or 0 if not set.
        :rtype: int
        """
        return getattr(self, '_display_order', 0) or 0

    @display_order.setter
    def display_order(self, value: int) -> None:
        """
        Set the display_order.
        """

        self._display_order = value
    # isActive,

    @property
    def is_active(self) -> bool:
        """
        Check if the delete operation is allowed for the
        flavor.

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
    # lookupEnumName,

    @property
    def lookup_enum_name(self) -> str:
        """
        Returns the Lookup Enum Name of the
        flavor.

        :return: The Lookup Enum Name of the
            flavor.
        :rtype: str
        """
        return getattr(self, '_lookup_enum_name', "") or ""

    @lookup_enum_name.setter
    def lookup_enum_name(self, value: str) -> None:
        """
        Set the lookup_enum_name.
        """

        self._lookup_enum_name = value
    # name,

    @property
    def name(self) -> str:
        """
        Returns the Name of the
        flavor.

        :return: The Name of the
            flavor.
        :rtype: str
        """
        return getattr(self, '_name', "") or ""

    @name.setter
    def name(self, value: str) -> None:
        """
        Set the name.
        """

        self._name = value
    # PacID
    # PacID
    @property
    def pac_id(self) -> int:
        """
        Get the ID of the pac associated with this flavor.

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
        the Flavor model.

        Returns:
            list: A list of property names.
        """

        result = [
            "description",
            "display_order",
            "is_active",
            "lookup_enum_name",
            "name",
            "pac_id",
# endset  # noqa: E122
            "code"
        ]
        return result


@event.listens_for(Flavor, 'before_insert')
def set_created_on(
    mapper,
    connection,
    target
):  # pylint: disable=unused-argument
    """
    Set the created on and last update timestamps
    for a Flavor object.

    Args:
        mapper: The SQLAlchemy mapper.
        connection: The SQLAlchemy connection.
        target: The Flavor object
        being inserted.

    Returns:
        None
    """
    target.insert_utc_date_time = datetime.now(timezone.utc)
    target.last_update_utc_date_time = datetime.now(timezone.utc)


@event.listens_for(Flavor, 'before_update')
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
