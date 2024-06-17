# models/customer.py
# pylint: disable=unused-import
"""
    #TODO add comment
"""
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
    #TODO add comment
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
    last_change_code = Column(
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
    active_organization_id = Column(
        'active_organization_id',
        Integer,
        default=0,
        index=(
            customer_constants.
            active_organization_id_calculatedIsDBColumnIndexed
        ),
        nullable=True)
    email = Column(
        'email',

        String,

        default="",
        index=(
            customer_constants.
            email_calculatedIsDBColumnIndexed
        ),
        nullable=True)
    email_confirmed_utc_date_time = Column(
        'email_confirmed_utc_date_time',
        DateTime,
        default=datetime(1753, 1, 1),
        index=(
            customer_constants.
            email_confirmed_utc_date_time_calculatedIsDBColumnIndexed
        ),
        nullable=True)
    first_name = Column(
        'first_name',

        String,

        default="",
        index=(
            customer_constants.
            first_name_calculatedIsDBColumnIndexed
        ),
        nullable=True)
    forgot_password_key_expiration_utc_date_time = Column(
        'forgot_password_key_expiration_utc_date_time',
        DateTime,
        default=datetime(1753, 1, 1),
        index=(
            customer_constants.
            forgot_password_key_expiration_utc_date_time_calculatedIsDBColumnIndexed
        ),
        nullable=True)
    forgot_password_key_value = Column(
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
    is_active = Column(
        'is_active',
        Boolean,
        default=False,
        index=(
            customer_constants.
            is_active_calculatedIsDBColumnIndexed
        ),
        nullable=True)
    is_email_allowed = Column(
        'is_email_allowed',
        Boolean,
        default=False,
        index=(
            customer_constants.
            is_email_allowed_calculatedIsDBColumnIndexed
        ),
        nullable=True)
    is_email_confirmed = Column(
        'is_email_confirmed',
        Boolean,
        default=False,
        index=(
            customer_constants.
            is_email_confirmed_calculatedIsDBColumnIndexed
        ),
        nullable=True)
    is_email_marketing_allowed = Column(
        'is_email_marketing_allowed',
        Boolean,
        default=False,
        index=(
            customer_constants.
            is_email_marketing_allowed_calculatedIsDBColumnIndexed
        ),
        nullable=True)
    is_locked = Column(
        'is_locked',
        Boolean,
        default=False,
        index=(
            customer_constants.
            is_locked_calculatedIsDBColumnIndexed
        ),
        nullable=True)
    is_multiple_organizations_allowed = Column(
        'is_multiple_organizations_allowed',
        Boolean,
        default=False,
        index=(
            customer_constants.
            is_multiple_organizations_allowed_calculatedIsDBColumnIndexed
        ),
        nullable=True)
    is_verbose_logging_forced = Column(
        'is_verbose_logging_forced',
        Boolean,
        default=False,
        index=(
            customer_constants.
            is_verbose_logging_forced_calculatedIsDBColumnIndexed
        ),
        nullable=True)
    last_login_utc_date_time = Column(
        'last_login_utc_date_time',
        DateTime,
        default=datetime(1753, 1, 1),
        index=(
            customer_constants.
            last_login_utc_date_time_calculatedIsDBColumnIndexed
        ),
        nullable=True)
    last_name = Column(
        'last_name',

        String,

        default="",
        index=(
            customer_constants.
            last_name_calculatedIsDBColumnIndexed
        ),
        nullable=True)
    password = Column(
        'password',

        EncryptedType(),

        default="",
        index=(
            customer_constants.
            password_calculatedIsDBColumnIndexed
        ),
        nullable=True)
    phone = Column(
        'phone',

        String,

        default="",
        index=(
            customer_constants.
            phone_calculatedIsDBColumnIndexed
        ),
        nullable=True)
    province = Column(
        'province',

        String,

        default="",
        index=(
            customer_constants.
            province_calculatedIsDBColumnIndexed
        ),
        nullable=True)
    registration_utc_date_time = Column(
        'registration_utc_date_time',
        DateTime,
        default=datetime(1753, 1, 1),
        index=(
            customer_constants.
            registration_utc_date_time_calculatedIsDBColumnIndexed
        ),
        nullable=True)
    tac_id = Column(
        'tac_id',
        Integer,
        ForeignKey('farm_' + snake_case('Tac') + '.tac_id'),
        index=(
            customer_constants.
            tac_id_calculatedIsDBColumnIndexed
        ),
        nullable=True)
    utc_offset_in_minutes = Column(
        'utc_offset_in_minutes',
        Integer,
        default=0,
        index=(
            customer_constants.
            utc_offset_in_minutes_calculatedIsDBColumnIndexed
        ),
        nullable=True)
    zip = Column(
        'zip',

        String,

        default="",
        index=(
            customer_constants.
            zip_calculatedIsDBColumnIndexed
        ),
        nullable=True)
    tac_code_peek = uuid.UUID  # TacID
    insert_utc_date_time = Column(
        'insert_utc_date_time',
        DateTime,
        nullable=True)
    last_update_utc_date_time = Column(
        'last_update_utc_date_time',
        DateTime,
        nullable=True)
    # no relationsip properties.
    # they are not updated immediately if the id prop is updated directly
    # tac = relationship('Tac', back_populates=snake_case('Tac'))
    # flavor = relationship('Flavor', back_populates=snake_case('Flavor'))
    __mapper_args__ = {
        'version_id_col': last_change_code
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
            #TODO add comment
        """
        return uuid.UUID(str(self._code))
    @code.setter
    def code(self, value: uuid.UUID):
        """
            #TODO add comment
        """
        if isinstance(value, uuid.UUID):
            self._code = value
        else:
            self._code = uuid.UUID(value)
        self.last_update_utc_date_time = datetime.utcnow()
    @property
    def customer_id(self) -> int:
        """
            #TODO add comment
        """
        return getattr(self, '_customer_id', 0) or 0
    @customer_id.setter
    def customer_id(self, value: int) -> None:
        """
        Set the customer_id.
        """
        self._customer_id = value
    @property
    def insert_user_id(self):
        """
            #TODO add comment
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
            #TODO add comment
        """
        return uuid.UUID(str(self._last_update_user_id))
    @last_update_user_id.setter
    def last_update_user_id(self, value):
        if isinstance(value, uuid.UUID):
            self._last_update_user_id = value
        else:
            self._last_update_user_id = uuid.UUID(value)
        self.last_update_utc_date_time = datetime.utcnow()
    # activeOrganizationID,
    # email,
    # emailConfirmedUTCDateTime
    # firstName,
    # forgotPasswordKeyExpirationUTCDateTime
    # forgotPasswordKeyValue,
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
    # isEmailAllowed,
    # isEmailConfirmed,
    # isEmailMarketingAllowed,
    # isLocked,
    # isMultipleOrganizationsAllowed,
    # isVerboseLoggingForced,
    # lastLoginUTCDateTime
    # lastName,
    # password,
    # phone,
    # province,
    # registrationUTCDateTime
    # TacID
    # uTCOffsetInMinutes,
    # zip,
# endset
    @staticmethod
    def property_list():
        """
            #TODO add comment
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
        #TODO add comment
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
        #TODO add comment
    """
    target.last_update_utc_date_time = datetime.utcnow()
