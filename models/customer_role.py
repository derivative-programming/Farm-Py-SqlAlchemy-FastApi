# models/customer_role.py
"""
    #TODO add comment
"""
import uuid
from datetime import date, datetime
from sqlalchemy_utils import UUIDType
from sqlalchemy import (BigInteger, Boolean, Column, Date, DateTime, Float,
                        ForeignKey, Index, Integer, Numeric, String,
                        event, func)
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
from sqlalchemy.dialects.postgresql import UUID
import models.constants.customer_role as customer_role_constants
from utils.common_functions import snake_case
from .base import Base, EncryptedType
class CustomerRole(Base):
    """
    #TODO add comment
    """
    __tablename__ = 'farm_' + snake_case('CustomerRole')
    customer_role_id = Column(
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
    customer_id = Column('customer_id',
                     Integer,
                     ForeignKey('farm_' + snake_case('Customer') + '.customer_id'),
                     index=customer_role_constants.customer_id_calculatedIsDBColumnIndexed,
                     nullable=True)
    is_placeholder = Column(
        'is_placeholder',
        Boolean,
        default=False,
        index=customer_role_constants.is_placeholder_calculatedIsDBColumnIndexed,
        nullable=True)
    placeholder = Column(
        'placeholder',
        Boolean,
        default=False,
        index=customer_role_constants.placeholder_calculatedIsDBColumnIndexed,
        nullable=True)
    role_id = Column(
        'role_id',
        Integer,
        ForeignKey('farm_' + snake_case('Role') + '.role_id'),
        index=customer_role_constants.role_id_calculatedIsDBColumnIndexed,
        nullable=True)
    _customer_code_peek = UUIDType  # CustomerID
    _role_code_peek = UUIDType  # RoleID
    insert_utc_date_time = Column(
        'insert_utc_date_time',
        DateTime,
        nullable=True)
    last_update_utc_date_time = Column(
        'last_update_utc_date_time',
        DateTime,
        nullable=True)
    #no relationsip properties. they are not updated immediately if the id prop is updated directly
    # customer = relationship('Customer', back_populates=snake_case('Customer'))
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
            'customer_code_peek', uuid.uuid4())
        self.role_code_peek = kwargs.get(  # RoleID
            'role_code_peek', uuid.uuid4())
# endset
    @property
    def code(self):
        return uuid.UUID(str(self._code))
    @code.setter
    def code(self, value):
        if isinstance(value, uuid.UUID):
            self._code = value
        else:
            self._code = uuid.UUID(value)
        self.last_update_utc_date_time = datetime.utcnow()
    @property
    def insert_user_id(self):
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
        return uuid.UUID(str(self._last_update_user_id))
    @last_update_user_id.setter
    def last_update_user_id(self, value):
        if isinstance(value, uuid.UUID):
            self._last_update_user_id = value
        else:
            self._last_update_user_id = uuid.UUID(value)
        self.last_update_utc_date_time = datetime.utcnow()
    # CustomerID
    @property
    def customer_code_peek(self):
        return uuid.UUID(str(self._customer_code_peek))
    @code.setter
    def customer_code_peek(self, value):
        if isinstance(value, uuid.UUID):
            self._customer_code_peek = value
        else:
            self._customer_code_peek = uuid.UUID(value)
    # isPlaceholder,
    # placeholder,
    # roleID
    @property
    def role_code_peek(self):
        return uuid.UUID(str(self._role_code_peek))
    @role_code_peek.setter
    def role_code_peek(self, value):
        if isinstance(value, uuid.UUID):
            self._role_code_peek = value
        else:
            self._role_code_peek = uuid.UUID(value)
# endset
    @staticmethod
    def property_list():
        result = [
            "customer_id",
            "is_placeholder",
            "placeholder",
            "role_id",
# endset
            "code"
            ]
        return result
# Define the index separately from the column
# Index('index_code', CustomerRole.code)
# Index('farm_customer_role_index_customer_id', CustomerRole.customer_id)  # CustomerID
# Index('farm_customer_role_index_role_id', CustomerRole.role_id)  # RoleID
@event.listens_for(CustomerRole, 'before_insert')
def set_created_on(mapper, connection, target):
    target.insert_utc_date_time = datetime.utcnow()
    target.last_update_utc_date_time = datetime.utcnow()
@event.listens_for(CustomerRole, 'before_update')
def set_updated_on(mapper, connection, target):
    target.last_update_utc_date_time = datetime.utcnow()
