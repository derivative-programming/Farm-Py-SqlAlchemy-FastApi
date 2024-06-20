# models/customer.py
# pylint: disable=unused-import
"""
The Customer model inherits from the Base model and is mapped to the
'farm_Customer' table in the database.
"""
from decimal import Decimal
import uuid
from datetime import date, datetime
from sqlalchemy_utils import UUIDType
from sqlalchemy import (BigInteger, Boolean,   # noqa: F401
                        Column, Date, DateTime, Float,
                        ForeignKey, Index, Integer, Numeric, String,
                        event, func)
import models.constants.customer as customer_constants
from utils.common_functions import snake_case
from .base import Base, EncryptedType  # noqa: F401
class Customer(Base):
    """
    The Customer model represents a customer in the farm.
    It inherits from the Base model and is mapped to the
    'farm_Customer' table in the database.
    """
    __tablename__ = 'farm_' + snake_case('Customer')
    _customer_id = Column(
        'customer_id',
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
    _active_organization_id = Column(
        'active_organization_id',
        Integer,
        default=0,
        index=(
            customer_constants.
            active_organization_id_calculatedIsDBColumnIndexed
        ),
        nullable=True)
    _email = Column(
        'email',

        String,

        default="",
        index=(
            customer_constants.
            email_calculatedIsDBColumnIndexed
        ),
        nullable=True)
    _email_confirmed_utc_date_time = Column(
        'email_confirmed_utc_date_time',
        DateTime,
        default=datetime(1753, 1, 1),
        index=(
            customer_constants.
            email_confirmed_utc_date_time_calculatedIsDBColumnIndexed
        ),
        nullable=True)
    _first_name = Column(
        'first_name',

        String,

        default="",
        index=(
            customer_constants.
            first_name_calculatedIsDBColumnIndexed
        ),
        nullable=True)
    _forgot_password_key_expiration_utc_date_time = Column(
        'forgot_password_key_expiration_utc_date_time',
        DateTime,
        default=datetime(1753, 1, 1),
        index=(
            customer_constants.
            forgot_password_key_expiration_utc_date_time_calculatedIsDBColumnIndexed
        ),
        nullable=True)
    _forgot_password_key_value = Column(
        'forgot_password_key_value',

        EncryptedType(),

        default="",
        index=(
            customer_constants.
            forgot_password_key_value_calculatedIsDBColumnIndexed
        ),
        nullable=True)
    _fs_user_code_value = Column(
        'fs_user_code_value',
        UUIDType(binary=False),
        default=uuid.uuid4,
        index=(
            customer_constants.
            fs_user_code_value_calculatedIsDBColumnIndexed
        ),
        nullable=True)
    _is_active = Column(
        'is_active',
        Boolean,
        default=False,
        index=(
            customer_constants.
            is_active_calculatedIsDBColumnIndexed
        ),
        nullable=True)
    _is_email_allowed = Column(
        'is_email_allowed',
        Boolean,
        default=False,
        index=(
            customer_constants.
            is_email_allowed_calculatedIsDBColumnIndexed
        ),
        nullable=True)
    _is_email_confirmed = Column(
        'is_email_confirmed',
        Boolean,
        default=False,
        index=(
            customer_constants.
            is_email_confirmed_calculatedIsDBColumnIndexed
        ),
        nullable=True)
    _is_email_marketing_allowed = Column(
        'is_email_marketing_allowed',
        Boolean,
        default=False,
        index=(
            customer_constants.
            is_email_marketing_allowed_calculatedIsDBColumnIndexed
        ),
        nullable=True)
    _is_locked = Column(
        'is_locked',
        Boolean,
        default=False,
        index=(
            customer_constants.
            is_locked_calculatedIsDBColumnIndexed
        ),
        nullable=True)
    _is_multiple_organizations_allowed = Column(
        'is_multiple_organizations_allowed',
        Boolean,
        default=False,
        index=(
            customer_constants.
            is_multiple_organizations_allowed_calculatedIsDBColumnIndexed
        ),
        nullable=True)
    _is_verbose_logging_forced = Column(
        'is_verbose_logging_forced',
        Boolean,
        default=False,
        index=(
            customer_constants.
            is_verbose_logging_forced_calculatedIsDBColumnIndexed
        ),
        nullable=True)
    _last_login_utc_date_time = Column(
        'last_login_utc_date_time',
        DateTime,
        default=datetime(1753, 1, 1),
        index=(
            customer_constants.
            last_login_utc_date_time_calculatedIsDBColumnIndexed
        ),
        nullable=True)
    _last_name = Column(
        'last_name',

        String,

        default="",
        index=(
            customer_constants.
            last_name_calculatedIsDBColumnIndexed
        ),
        nullable=True)
    _password = Column(
        'password',

        EncryptedType(),

        default="",
        index=(
            customer_constants.
            password_calculatedIsDBColumnIndexed
        ),
        nullable=True)
    _phone = Column(
        'phone',

        String,

        default="",
        index=(
            customer_constants.
            phone_calculatedIsDBColumnIndexed
        ),
        nullable=True)
    _province = Column(
        'province',

        String,

        default="",
        index=(
            customer_constants.
            province_calculatedIsDBColumnIndexed
        ),
        nullable=True)
    _registration_utc_date_time = Column(
        'registration_utc_date_time',
        DateTime,
        default=datetime(1753, 1, 1),
        index=(
            customer_constants.
            registration_utc_date_time_calculatedIsDBColumnIndexed
        ),
        nullable=True)
    _tac_id = Column(
        'tac_id',
        Integer,
        ForeignKey('farm_' + snake_case('Tac') + '.tac_id'),
        index=(
            customer_constants.
            tac_id_calculatedIsDBColumnIndexed
        ),
        nullable=True)
    _utc_offset_in_minutes = Column(
        'utc_offset_in_minutes',
        Integer,
        default=0,
        index=(
            customer_constants.
            utc_offset_in_minutes_calculatedIsDBColumnIndexed
        ),
        nullable=True)
    _zip = Column(
        'zip',

        String,

        default="",
        index=(
            customer_constants.
            zip_calculatedIsDBColumnIndexed
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
        self.active_organization_id = kwargs.get(
            'active_organization_id', 0)
        self.email = kwargs.get(
            'email', "")
        self.email_confirmed_utc_date_time = kwargs.get(
            'email_confirmed_utc_date_time', datetime(1753, 1, 1))
        self.first_name = kwargs.get(
            'first_name', "")
        self.forgot_password_key_expiration_utc_date_time = kwargs.get(
            'forgot_password_key_expiration_utc_date_time', datetime(1753, 1, 1))
        self.forgot_password_key_value = kwargs.get(
            'forgot_password_key_value', "")
        self.fs_user_code_value = kwargs.get(
            'fs_user_code_value', uuid.uuid4())
        self.is_active = kwargs.get(
            'is_active', False)
        self.is_email_allowed = kwargs.get(
            'is_email_allowed', False)
        self.is_email_confirmed = kwargs.get(
            'is_email_confirmed', False)
        self.is_email_marketing_allowed = kwargs.get(
            'is_email_marketing_allowed', False)
        self.is_locked = kwargs.get(
            'is_locked', False)
        self.is_multiple_organizations_allowed = kwargs.get(
            'is_multiple_organizations_allowed', False)
        self.is_verbose_logging_forced = kwargs.get(
            'is_verbose_logging_forced', False)
        self.last_login_utc_date_time = kwargs.get(
            'last_login_utc_date_time', datetime(1753, 1, 1))
        self.last_name = kwargs.get(
            'last_name', "")
        self.password = kwargs.get(
            'password', "")
        self.phone = kwargs.get(
            'phone', "")
        self.province = kwargs.get(
            'province', "")
        self.registration_utc_date_time = kwargs.get(
            'registration_utc_date_time', datetime(1753, 1, 1))
        self.tac_id = kwargs.get(
            'tac_id', 0)
        self.utc_offset_in_minutes = kwargs.get(
            'utc_offset_in_minutes', 0)
        self.zip = kwargs.get(
            'zip', "")
        self.insert_utc_date_time = kwargs.get(
            'insert_utc_date_time', datetime(1753, 1, 1))
        self.last_update_utc_date_time = kwargs.get(
            'last_update_utc_date_time', datetime(1753, 1, 1))
# endset
        self.tac_code_peek = kwargs.get(  # TacID
            'tac_code_peek', uuid.UUID(int=0))
# endset
    @property
    def code(self):
        """
        Get the code of the customer.
        Returns:
            UUID: The code of the customer.
        """
        return uuid.UUID(str(self._code))
    @code.setter
    def code(self, value: uuid.UUID):
        """
        Set the code of the customer.
        Args:
            value (uuid.UUID): The code to set for the customer.
        Raises:
            TypeError: If the value is not of type uuid.UUID.
        """
        if isinstance(value, uuid.UUID):
            self._code = value
        else:
            self._code = uuid.UUID(value)
        self.last_update_utc_date_time = datetime.utcnow()
    @property
    def customer_id(self) -> int:
        """
        Get the ID of the customer.
        Returns:
            int: The ID of the customer.
        """
        return getattr(self, '_customer_id', 0) or 0
    @customer_id.setter
    def customer_id(self, value: int) -> None:
        """
        Set the customer_id.
        """
        self._customer_id = value
    @property
    def last_change_code(self) -> int:
        """
        Returns the last change code of the customer.
        :return: The last change code of the customer.
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
        Inserts the user ID into the customer object.
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
        Returns the UUID of the last user who updated the customer.
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
        Inserts the UTC date and time for the customer.
        Returns:
            datetime: The UTC date and time for the customer.
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
        Returns the last update UTC date and time of the customer.
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
    # activeOrganizationID,
    @property
    def active_organization_id(self) -> int:
        """
        Returns the value of the '_active_organization_id' attribute of the object.
        If the attribute is not set, it returns 0.
        :return: The value of the '_active_organization_id' attribute or 0 if not set.
        :rtype: int
        """
        return getattr(self, '_active_organization_id', 0) or 0
    @active_organization_id.setter
    def active_organization_id(self, value: int) -> None:
        """
        Set the active_organization_id.
        """
        self._active_organization_id = value
    # email,
    @property
    def email(self) -> str:
        """
        Returns the email address associated with the customer.
        :return: The email address as a string.
        """
        return getattr(self, '_email', "") or ""
    @email.setter
    def email(self, value: str) -> None:
        """
        Set the email.
        """
        self._email = value
    # emailConfirmedUTCDateTime
    @property
    def email_confirmed_utc_date_time(self) -> datetime:
        """
        Get the value of email_confirmed_utc_date_time property.
        Returns:
            datetime: The value of email_confirmed_utc_date_time property.
        """
        return getattr(
            self,
            '_email_confirmed_utc_date_time',
            datetime(1753, 1, 1)
        ) or datetime(1753, 1, 1)
    @email_confirmed_utc_date_time.setter
    def email_confirmed_utc_date_time(self, value: datetime) -> None:
        """
        Set the email_confirmed_utc_date_time.
        """
        self._email_confirmed_utc_date_time = value
    # firstName,
    @property
    def first_name(self) -> str:
        """
        Returns the First Name of the customer.
        :return: The First Name of the customer.
        :rtype: str
        """
        return getattr(self, '_first_name', "") or ""
    @first_name.setter
    def first_name(self, value: str) -> None:
        """
        Set the first_name.
        """
        self._first_name = value
    # forgotPasswordKeyExpirationUTCDateTime
    @property
    def forgot_password_key_expiration_utc_date_time(self) -> datetime:
        """
        Get the value of forgot_password_key_expiration_utc_date_time property.
        Returns:
            datetime: The value of forgot_password_key_expiration_utc_date_time property.
        """
        return getattr(
            self,
            '_forgot_password_key_expiration_utc_date_time',
            datetime(1753, 1, 1)
        ) or datetime(1753, 1, 1)
    @forgot_password_key_expiration_utc_date_time.setter
    def forgot_password_key_expiration_utc_date_time(self, value: datetime) -> None:
        """
        Set the forgot_password_key_expiration_utc_date_time.
        """
        self._forgot_password_key_expiration_utc_date_time = value
    # forgotPasswordKeyValue,
    @property
    def forgot_password_key_value(self) -> str:
        """
        Returns the Forgot Password Key Value of the customer.
        :return: The Forgot Password Key Value of the customer.
        :rtype: str
        """
        return getattr(self, '_forgot_password_key_value', "") or ""
    @forgot_password_key_value.setter
    def forgot_password_key_value(self, value: str) -> None:
        """
        Set the forgot_password_key_value.
        """
        self._forgot_password_key_value = value
    # fSUserCodeValue,
    @property
    def fs_user_code_value(self):
        """
        Returns the unique identifier as a UUID object.
        Returns:
            uuid.UUID: The unique identifier value.
        """
        return uuid.UUID(str(self._fs_user_code_value))
    @fs_user_code_value.setter
    def fs_user_code_value(self, value):
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
            self._fs_user_code_value = value
        else:
            try:
                self._fs_user_code_value = uuid.UUID(value)
            except ValueError as e:
                raise ValueError(f"Invalid UUID value: {value}") from e
        self.last_update_utc_date_time = datetime.utcnow()
    # isActive,
    @property
    def is_active(self) -> bool:
        """
        Check if the delete operation is allowed for the customer.
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
    # isEmailAllowed,
    @property
    def is_email_allowed(self) -> bool:
        """
        Check if the delete operation is allowed for the customer.
        Returns:
            bool: True if delete is allowed, False otherwise.
        """
        return getattr(self, '_is_email_allowed', False) or False
    @is_email_allowed.setter
    def is_email_allowed(self, value: bool) -> None:
        """
        Set the is_email_allowed.
        """
        self._is_email_allowed = value
    # isEmailConfirmed,
    @property
    def is_email_confirmed(self) -> bool:
        """
        Check if the delete operation is allowed for the customer.
        Returns:
            bool: True if delete is allowed, False otherwise.
        """
        return getattr(self, '_is_email_confirmed', False) or False
    @is_email_confirmed.setter
    def is_email_confirmed(self, value: bool) -> None:
        """
        Set the is_email_confirmed.
        """
        self._is_email_confirmed = value
    # isEmailMarketingAllowed,
    @property
    def is_email_marketing_allowed(self) -> bool:
        """
        Check if the delete operation is allowed for the customer.
        Returns:
            bool: True if delete is allowed, False otherwise.
        """
        return getattr(self, '_is_email_marketing_allowed', False) or False
    @is_email_marketing_allowed.setter
    def is_email_marketing_allowed(self, value: bool) -> None:
        """
        Set the is_email_marketing_allowed.
        """
        self._is_email_marketing_allowed = value
    # isLocked,
    @property
    def is_locked(self) -> bool:
        """
        Check if the delete operation is allowed for the customer.
        Returns:
            bool: True if delete is allowed, False otherwise.
        """
        return getattr(self, '_is_locked', False) or False
    @is_locked.setter
    def is_locked(self, value: bool) -> None:
        """
        Set the is_locked.
        """
        self._is_locked = value
    # isMultipleOrganizationsAllowed,
    @property
    def is_multiple_organizations_allowed(self) -> bool:
        """
        Check if the delete operation is allowed for the customer.
        Returns:
            bool: True if delete is allowed, False otherwise.
        """
        return getattr(self, '_is_multiple_organizations_allowed', False) or False
    @is_multiple_organizations_allowed.setter
    def is_multiple_organizations_allowed(self, value: bool) -> None:
        """
        Set the is_multiple_organizations_allowed.
        """
        self._is_multiple_organizations_allowed = value
    # isVerboseLoggingForced,
    @property
    def is_verbose_logging_forced(self) -> bool:
        """
        Check if the delete operation is allowed for the customer.
        Returns:
            bool: True if delete is allowed, False otherwise.
        """
        return getattr(self, '_is_verbose_logging_forced', False) or False
    @is_verbose_logging_forced.setter
    def is_verbose_logging_forced(self, value: bool) -> None:
        """
        Set the is_verbose_logging_forced.
        """
        self._is_verbose_logging_forced = value
    # lastLoginUTCDateTime
    @property
    def last_login_utc_date_time(self) -> datetime:
        """
        Get the value of last_login_utc_date_time property.
        Returns:
            datetime: The value of last_login_utc_date_time property.
        """
        return getattr(
            self,
            '_last_login_utc_date_time',
            datetime(1753, 1, 1)
        ) or datetime(1753, 1, 1)
    @last_login_utc_date_time.setter
    def last_login_utc_date_time(self, value: datetime) -> None:
        """
        Set the last_login_utc_date_time.
        """
        self._last_login_utc_date_time = value
    # lastName,
    @property
    def last_name(self) -> str:
        """
        Returns the Last Name of the customer.
        :return: The Last Name of the customer.
        :rtype: str
        """
        return getattr(self, '_last_name', "") or ""
    @last_name.setter
    def last_name(self, value: str) -> None:
        """
        Set the last_name.
        """
        self._last_name = value
    # password,
    @property
    def password(self) -> str:
        """
        Returns the Password of the customer.
        :return: The Password of the customer.
        :rtype: str
        """
        return getattr(self, '_password', "") or ""
    @password.setter
    def password(self, value: str) -> None:
        """
        Set the password.
        """
        self._password = value
    # phone,
    @property
    def phone(self) -> str:
        """
        Get the value of the 'phone' property.
        Returns:
            str: The value of the 'phone' property.
        """
        return getattr(self, '_phone', "") or ""
    @phone.setter
    def phone(self, value: str) -> None:
        """
        Set the phone.
        """
        self._phone = value
    # province,
    @property
    def province(self) -> str:
        """
        Returns the Province of the customer.
        :return: The Province of the customer.
        :rtype: str
        """
        return getattr(self, '_province', "") or ""
    @province.setter
    def province(self, value: str) -> None:
        """
        Set the province.
        """
        self._province = value
    # registrationUTCDateTime
    @property
    def registration_utc_date_time(self) -> datetime:
        """
        Get the value of registration_utc_date_time property.
        Returns:
            datetime: The value of registration_utc_date_time property.
        """
        return getattr(
            self,
            '_registration_utc_date_time',
            datetime(1753, 1, 1)
        ) or datetime(1753, 1, 1)
    @registration_utc_date_time.setter
    def registration_utc_date_time(self, value: datetime) -> None:
        """
        Set the registration_utc_date_time.
        """
        self._registration_utc_date_time = value
    # TacID
    # uTCOffsetInMinutes,
    @property
    def utc_offset_in_minutes(self) -> int:
        """
        Returns the value of the '_utc_offset_in_minutes' attribute of the object.
        If the attribute is not set, it returns 0.
        :return: The value of the '_utc_offset_in_minutes' attribute or 0 if not set.
        :rtype: int
        """
        return getattr(self, '_utc_offset_in_minutes', 0) or 0
    @utc_offset_in_minutes.setter
    def utc_offset_in_minutes(self, value: int) -> None:
        """
        Set the utc_offset_in_minutes.
        """
        self._utc_offset_in_minutes = value
    # zip,
    @property
    def zip(self) -> str:
        """
        Returns the Zip of the customer.
        :return: The Zip of the customer.
        :rtype: str
        """
        return getattr(self, '_zip', "") or ""
    @zip.setter
    def zip(self, value: str) -> None:
        """
        Set the zip.
        """
        self._zip = value
# endset
    # TacID
    @property
    def tac_id(self) -> int:
        """
        Get the ID of the tac associated with this customer.
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
# endset
    @staticmethod
    def property_list():
        """
        Returns a list of property names for the Customer model.
        Returns:
            list: A list of property names.
        """
        result = [
            "active_organization_id",
            "email",
            "email_confirmed_utc_date_time",
            "first_name",
            "forgot_password_key_expiration_utc_date_time",
            "forgot_password_key_value",
            "fs_user_code_value",
            "is_active",
            "is_email_allowed",
            "is_email_confirmed",
            "is_email_marketing_allowed",
            "is_locked",
            "is_multiple_organizations_allowed",
            "is_verbose_logging_forced",
            "last_login_utc_date_time",
            "last_name",
            "password",
            "phone",
            "province",
            "registration_utc_date_time",
            "tac_id",
            "utc_offset_in_minutes",
            "zip",
# endset  # noqa: E122
            "code"
        ]
        return result
@event.listens_for(Customer, 'before_insert')
def set_created_on(
    mapper,
    connection,
    target
):  # pylint: disable=unused-argument
    """
    Set the created on and last update timestamps for a Customer object.
    Args:
        mapper: The SQLAlchemy mapper.
        connection: The SQLAlchemy connection.
        target: The Customer object being inserted.
    Returns:
        None
    """
    target.insert_utc_date_time = datetime.utcnow()
    target.last_update_utc_date_time = datetime.utcnow()
@event.listens_for(Customer, 'before_update')
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
