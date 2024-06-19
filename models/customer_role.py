# models/customer_role.py
# pylint: disable=unused-import
"""
The CustomerRole model inherits from the Base model and is mapped to the
'farm_CustomerRole' table in the database.
"""
from decimal import Decimal
import uuid
from datetime import date, datetime
from sqlalchemy_utils import UUIDType
from sqlalchemy import (BigInteger, Boolean,   # noqa: F401
                        Column, Date, DateTime, Float,
                        ForeignKey, Index, Integer, Numeric, String,
                        event, func)
import models.constants.customer_role as customer_role_constants
from utils.common_functions import snake_case
from .base import Base, EncryptedType  # noqa: F401
class CustomerRole(Base):
    """
    #TODO add comment
    """
    __tablename__ = 'farm_' + snake_case('CustomerRole')
    _customer_role_id = Column(
        'customer_role_id',
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
    _customer_id = Column(
        'customer_id',
        Integer,
        ForeignKey('farm_' + snake_case('Customer') + '.customer_id'),
        index=(
            customer_role_constants.
            customer_id_calculatedIsDBColumnIndexed
        ),
        nullable=True)
    _is_placeholder = Column(
        'is_placeholder',
        Boolean,
        default=False,
        index=(
            customer_role_constants.
            is_placeholder_calculatedIsDBColumnIndexed
        ),
        nullable=True)
    _placeholder = Column(
        'placeholder',
        Boolean,
        default=False,
        index=(
            customer_role_constants.
            placeholder_calculatedIsDBColumnIndexed
        ),
        nullable=True)
    _role_id = Column(
        'role_id',
        Integer,
        ForeignKey('farm_' + snake_case('Role') + '.role_id'),
        index=(
            customer_role_constants.
            role_id_calculatedIsDBColumnIndexed
        ),
        nullable=True)
    customer_code_peek: uuid.UUID = uuid.UUID(int=0)  # CustomerID  # noqa: E501
    role_code_peek: uuid.UUID = uuid.UUID(int=0)  # RoleID  # noqa: E501
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
        self.customer_id = kwargs.get(
            'customer_id', 0)
        self.is_placeholder = kwargs.get(
            'is_placeholder', False)
        self.placeholder = kwargs.get(
            'placeholder', False)
        self.role_id = kwargs.get(
            'role_id', 0)
        self.insert_utc_date_time = kwargs.get(
            'insert_utc_date_time', datetime(1753, 1, 1))
        self.last_update_utc_date_time = kwargs.get(
            'last_update_utc_date_time', datetime(1753, 1, 1))
# endset
        self.customer_code_peek = kwargs.get(  # CustomerID
            'customer_code_peek', uuid.UUID(int=0))
        self.role_code_peek = kwargs.get(  # RoleID
            'role_code_peek', uuid.UUID(int=0))
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
    def customer_role_id(self) -> int:
        """
            #TODO add comment
        """
        return getattr(self, '_customer_role_id', 0) or 0
    @customer_role_id.setter
    def customer_role_id(self, value: int) -> None:
        """
        Set the customer_role_id.
        """
        self._customer_role_id = value
    @property
    def last_change_code(self) -> int:
        """
            #TODO add comment
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
    @property
    def insert_utc_date_time(self) -> datetime:
        """
            #TODO add comment
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
            #TODO add comment
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
    # CustomerID
    # isPlaceholder,
    @property
    def is_placeholder(self) -> bool:
        """
            #TODO add comment
        """
        return getattr(self, '_is_placeholder', False) or False
    @is_placeholder.setter
    def is_placeholder(self, value: bool) -> None:
        """
        Set the is_placeholder.
        """
        self._is_placeholder = value
    # placeholder,
    @property
    def placeholder(self) -> bool:
        """
            #TODO add comment
        """
        return getattr(self, '_placeholder', False) or False
    @placeholder.setter
    def placeholder(self, value: bool) -> None:
        """
        Set the placeholder.
        """
        self._placeholder = value
    # roleID
# endset
    # CustomerID
    # roleID
    @property
    def role_id(self) -> int:
        """
            #TODO add comment
        """
        return getattr(self, '_role_id', 0) or 0
    @role_id.setter
    def role_id(self, value: int) -> None:
        """
        Set the role_id.
        """
        self._role_id = value
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
# endset
    @staticmethod
    def property_list():
        """
            #TODO add comment
        """
        result = [
            "customer_id",
            "is_placeholder",
            "placeholder",
            "role_id",
# endset  # noqa: E122
            "code"
        ]
        return result
@event.listens_for(CustomerRole, 'before_insert')
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
@event.listens_for(CustomerRole, 'before_update')
def set_updated_on(
    mapper,
    connection,
    target
):  # pylint: disable=unused-argument
    """
        #TODO add comment
    """
    target.last_update_utc_date_time = datetime.utcnow()
