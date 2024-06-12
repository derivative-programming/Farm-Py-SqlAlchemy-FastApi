# models/customer_role.py
"""
    #TODO add comment
"""
from datetime import date, datetime
from sqlalchemy import (BigInteger, Boolean, Column, Date, DateTime, Float,
                        ForeignKey, Index, Integer, Numeric, String, Uuid,
                        event, func)
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
from sqlalchemy.dialects.postgresql import UUID
import models.constants.customer_role as customer_role_constants
from services.db_config import DB_DIALECT, generate_uuid, get_uuid_type
from utils.common_functions import snake_case
from .base import Base, EncryptedType
UUIDType = get_uuid_type(DB_DIALECT)
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
    code = Column('code',
                  UUIDType,
                  unique=True,
                  default=generate_uuid,
                  nullable=True)
    last_change_code = Column(
        'last_change_code',
        Integer,
        nullable=True)
    insert_user_id = Column(
        'insert_user_id',
        UUIDType,
        default=generate_uuid,
        nullable=True)
    last_update_user_id = Column(
        'last_update_user_id',
        UUIDType,
        default=generate_uuid,
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
    customer_code_peek = UUIDType  # CustomerID
    role_code_peek = UUIDType  # RoleID
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
        self.code = kwargs.get('code', generate_uuid())
        self.last_change_code = kwargs.get(
            'last_change_code', 0)
        self.insert_user_id = kwargs.get(
            'insert_user_id', None)
        self.last_update_user_id = kwargs.get(
            'last_update_user_id', None)
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
            'customer_code_peek', generate_uuid())
        self.role_code_peek = kwargs.get(  # RoleID
            'role_code_peek', generate_uuid())
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
