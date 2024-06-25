# models/org_api_key.py
# pylint: disable=unused-import

"""
The OrgApiKey model inherits from
the Base model and is mapped to the
'farm_OrgApiKey' table in the database.
"""
from decimal import Decimal
import uuid
from datetime import date, datetime
from sqlalchemy_utils import UUIDType
from sqlalchemy import (BigInteger, Boolean,   # noqa: F401
                        Column, Date, DateTime, Float,
                        ForeignKey, Index, Integer, Numeric, String,
                        event, func)
import models.constants.org_api_key as org_api_key_constants
from utils.common_functions import snake_case
from .base import Base, EncryptedType  # noqa: F401


class OrgApiKey(Base):
    """
    The OrgApiKey model represents a
    org_api_key in the farm.
    It inherits from the Base model and is mapped to the
    'farm_OrgApiKey' table in the database.
    """

    __tablename__ = 'farm_' + snake_case('OrgApiKey')

    _org_api_key_id = Column(
        'org_api_key_id',
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
    _api_key_value = Column(
        'api_key_value',

        String,

        default="",
        index=(
            org_api_key_constants.
            api_key_value_calculatedIsDBColumnIndexed
        ),
        nullable=True)
    _created_by = Column(
        'created_by',

        String,

        default="",
        index=(
            org_api_key_constants.
            created_by_calculatedIsDBColumnIndexed
        ),
        nullable=True)
    _created_utc_date_time = Column(
        'created_utc_date_time',
        DateTime,
        default=datetime(1753, 1, 1),
        index=(
            org_api_key_constants.
            created_utc_date_time_calculatedIsDBColumnIndexed
        ),
        nullable=True)
    _expiration_utc_date_time = Column(
        'expiration_utc_date_time',
        DateTime,
        default=datetime(1753, 1, 1),
        index=(
            org_api_key_constants.
            expiration_utc_date_time_calculatedIsDBColumnIndexed
        ),
        nullable=True)
    _is_active = Column(
        'is_active',
        Boolean,
        default=False,
        index=(
            org_api_key_constants.
            is_active_calculatedIsDBColumnIndexed
        ),
        nullable=True)
    _is_temp_user_key = Column(
        'is_temp_user_key',
        Boolean,
        default=False,
        index=(
            org_api_key_constants.
            is_temp_user_key_calculatedIsDBColumnIndexed
        ),
        nullable=True)
    _name = Column(
        'name',

        String,

        default="",
        index=(
            org_api_key_constants.
            name_calculatedIsDBColumnIndexed
        ),
        nullable=True)
    _organization_id = Column(
        'organization_id',
        Integer,
        ForeignKey('farm_' + snake_case('Organization') + '.organization_id'),
        index=(
            org_api_key_constants.
            organization_id_calculatedIsDBColumnIndexed
        ),
        nullable=True)
    _org_customer_id = Column(
        'org_customer_id',
        Integer,
        ForeignKey('farm_' + snake_case('OrgCustomer') + '.org_customer_id'),
        index=(
            org_api_key_constants.
            org_customer_id_calculatedIsDBColumnIndexed
        ),
        nullable=True)
    organization_code_peek: uuid.UUID = uuid.UUID(int=0)  # OrganizationID  # noqa: E501
    org_customer_code_peek: uuid.UUID = uuid.UUID(int=0)  # OrgCustomerID  # noqa: E501
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
        self.api_key_value = kwargs.get(
            'api_key_value', "")
        self.created_by = kwargs.get(
            'created_by', "")
        self.created_utc_date_time = kwargs.get(
            'created_utc_date_time', datetime(1753, 1, 1))
        self.expiration_utc_date_time = kwargs.get(
            'expiration_utc_date_time', datetime(1753, 1, 1))
        self.is_active = kwargs.get(
            'is_active', False)
        self.is_temp_user_key = kwargs.get(
            'is_temp_user_key', False)
        self.name = kwargs.get(
            'name', "")
        self.organization_id = kwargs.get(
            'organization_id', 0)
        self.org_customer_id = kwargs.get(
            'org_customer_id', 0)
        self.insert_utc_date_time = kwargs.get(
            'insert_utc_date_time', datetime(1753, 1, 1))
        self.last_update_utc_date_time = kwargs.get(
            'last_update_utc_date_time', datetime(1753, 1, 1))
        self.organization_code_peek = kwargs.get(  # OrganizationID
            'organization_code_peek', uuid.UUID(int=0))
        self.org_customer_code_peek = kwargs.get(  # OrgCustomerID
            'org_customer_code_peek', uuid.UUID(int=0))

    @property
    def code(self):
        """
        Get the code of the org_api_key.

        Returns:
            UUID: The code of the org_api_key.
        """
        return uuid.UUID(str(self._code))

    @code.setter
    def code(self, value: uuid.UUID):
        """
        Set the code of the org_api_key.

        Args:
            value (uuid.UUID): The code to set for the
                org_api_key.

        Raises:
            TypeError: If the value is not of type uuid.UUID.

        """
        if isinstance(value, uuid.UUID):
            self._code = value
        else:
            self._code = uuid.UUID(value)
        self.last_update_utc_date_time = datetime.utcnow()

    @property
    def org_api_key_id(self) -> int:
        """
        Get the ID of the org_api_key.

        Returns:
            int: The ID of the org_api_key.
        """
        return getattr(self, '_org_api_key_id', 0) or 0

    @org_api_key_id.setter
    def org_api_key_id(self, value: int) -> None:
        """
        Set the org_api_key_id.
        """

        self._org_api_key_id = value

    @property
    def last_change_code(self) -> int:
        """
        Returns the last change code of the
        org_api_key.

        :return: The last change code of the
            org_api_key.
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
        org_api_key object.

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
        Returns the UUID of the last user who updated the
        org_api_key.

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
        Inserts the UTC date and time for the
        org_api_key.

        Returns:
            datetime: The UTC date and time for the
                org_api_key.
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
        Returns the last update UTC date and time of the
        org_api_key.

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
    # apiKeyValue,

    @property
    def api_key_value(self) -> str:
        """
        Returns the Api Key Value of the
        org_api_key.

        :return: The Api Key Value of the
            org_api_key.
        :rtype: str
        """
        return getattr(self, '_api_key_value', "") or ""

    @api_key_value.setter
    def api_key_value(self, value: str) -> None:
        """
        Set the api_key_value.
        """

        self._api_key_value = value
    # createdBy,

    @property
    def created_by(self) -> str:
        """
        Returns the Created By of the
        org_api_key.

        :return: The Created By of the
            org_api_key.
        :rtype: str
        """
        return getattr(self, '_created_by', "") or ""

    @created_by.setter
    def created_by(self, value: str) -> None:
        """
        Set the created_by.
        """

        self._created_by = value
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
    # expirationUTCDateTime

    @property
    def expiration_utc_date_time(self) -> datetime:
        """
        Get the value of expiration_utc_date_time property.

        Returns:
            datetime: The value of expiration_utc_date_time property.
        """
        return getattr(
            self,
            '_expiration_utc_date_time',
            datetime(1753, 1, 1)
        ) or datetime(1753, 1, 1)

    @expiration_utc_date_time.setter
    def expiration_utc_date_time(self, value: datetime) -> None:
        """
        Set the expiration_utc_date_time.
        """

        self._expiration_utc_date_time = value
    # isActive,

    @property
    def is_active(self) -> bool:
        """
        Check if the delete operation is allowed for the
        org_api_key.

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
    # isTempUserKey,

    @property
    def is_temp_user_key(self) -> bool:
        """
        Check if the delete operation is allowed for the
        org_api_key.

        Returns:
            bool: True if delete is allowed, False otherwise.
        """
        return getattr(self, '_is_temp_user_key', False) or False

    @is_temp_user_key.setter
    def is_temp_user_key(self, value: bool) -> None:
        """
        Set the is_temp_user_key.
        """

        self._is_temp_user_key = value
    # name,

    @property
    def name(self) -> str:
        """
        Returns the Name of the
        org_api_key.

        :return: The Name of the
            org_api_key.
        :rtype: str
        """
        return getattr(self, '_name', "") or ""

    @name.setter
    def name(self, value: str) -> None:
        """
        Set the name.
        """

        self._name = value
    # OrganizationID
    # orgCustomerID
    # OrganizationID
    # orgCustomerID

    @property
    def org_customer_id(self) -> int:
        """
        Get the foreign key ID for the org_customer of the
        org_api_key.

        Returns:
            int: The foreign key ID for the org_customer of the
                org_api_key.
        """
        return getattr(self, '_org_customer_id', 0) or 0

    @org_customer_id.setter
    def org_customer_id(self, value: int) -> None:
        """
        Set the org_customer_id.
        """

        self._org_customer_id = value
    @property
    def organization_id(self) -> int:
        """
        Get the ID of the organization associated with this org_api_key.

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

    @staticmethod
    def property_list():
        """
        Returns a list of property names for
        the OrgApiKey model.

        Returns:
            list: A list of property names.
        """

        result = [
            "api_key_value",
            "created_by",
            "created_utc_date_time",
            "expiration_utc_date_time",
            "is_active",
            "is_temp_user_key",
            "name",
            "organization_id",
            "org_customer_id",
# endset  # noqa: E122
            "code"
        ]
        return result


@event.listens_for(OrgApiKey, 'before_insert')
def set_created_on(
    mapper,
    connection,
    target
):  # pylint: disable=unused-argument
    """
    Set the created on and last update timestamps
    for a OrgApiKey object.

    Args:
        mapper: The SQLAlchemy mapper.
        connection: The SQLAlchemy connection.
        target: The OrgApiKey object
        being inserted.

    Returns:
        None
    """
    target.insert_utc_date_time = datetime.utcnow()
    target.last_update_utc_date_time = datetime.utcnow()


@event.listens_for(OrgApiKey, 'before_update')
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

