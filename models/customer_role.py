from datetime import datetime, date
from marshmallow import Schema, fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from sqlalchemy import Index, event, BigInteger, Boolean, Column, Date, DateTime, Float, Integer, Numeric, String, ForeignKey, Uuid, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm.attributes import InstrumentedAttribute
from sqlalchemy.ext.hybrid import hybrid_property
from utils.common_functions import snake_case
from .base import Base  # Importing the Base from central module
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
from services.db_config import db_dialect,generate_uuid
# Conditionally set the UUID column type
if db_dialect == 'postgresql':
    UUIDType = UUID(as_uuid=True)
elif db_dialect == 'mssql':
    UUIDType = UNIQUEIDENTIFIER
else:  # This will cover SQLite, MySQL, and other databases
    UUIDType = String(36)
class CustomerRole(Base):
    __tablename__ = snake_case('CustomerRole')
    customer_role_id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(UUIDType, unique=True, default=generate_uuid, nullable=True)
    last_change_code = Column(Integer, nullable=True)
    insert_user_id = Column(UUIDType, default=generate_uuid, nullable=True)
    last_update_user_id = Column(UUIDType, default=generate_uuid, nullable=True)
    customer_id = Column(Integer, ForeignKey(snake_case('Customer') + '.customer_id'), nullable=True)
    is_placeholder = Column(Boolean, default=False, nullable=True)
    placeholder = Column(Boolean, default=False, nullable=True)
    role_id = Column(Integer, ForeignKey(snake_case('Role') + '.role_id'), nullable=True)
    customer_code_peek = UUIDType # CustomerID
    role_code_peek = UUIDType  # RoleID
    insert_utc_date_time = Column(DateTime, nullable=True)
    last_update_utc_date_time = Column(DateTime, nullable=True)
    #no relationsip properties. they are not updated immediately if the id prop is updated directly
    # customer = relationship('Customer', back_populates=snake_case('Customer'))
    # flavor = relationship('Flavor', back_populates=snake_case('Flavor'))
    __mapper_args__ = {
        'version_id_col': last_change_code
    }
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.code = kwargs.get('code', generate_uuid())
        self.last_change_code = kwargs.get('last_change_code', 0)
        self.insert_user_id = kwargs.get('insert_user_id', None)
        self.last_update_user_id = kwargs.get('last_update_user_id', None)
        self.customer_id = kwargs.get('customer_id', 0)
        self.is_placeholder = kwargs.get('is_placeholder', False)
        self.placeholder = kwargs.get('placeholder', False)
        self.role_id = kwargs.get('role_id', 0)
        self.insert_utc_date_time = kwargs.get('insert_utc_date_time', datetime(1753, 1, 1))
        self.last_update_utc_date_time = kwargs.get('last_update_utc_date_time', datetime(1753, 1, 1))

        self.customer_code_peek = kwargs.get('customer_code_peek', generate_uuid())# CustomerID
        self.role_code_peek = kwargs.get('role_code_peek', generate_uuid()) # RoleID

# Define the index separately from the column
# Index('index_code', CustomerRole.code)
Index('customer_role_index_customer_id', CustomerRole.customer_id) #CustomerID
Index('customer_role_index_role_id', CustomerRole.role_id) #RoleID
@event.listens_for(CustomerRole, 'before_insert')
def set_created_on(mapper, connection, target):
    target.insert_utc_date_time = datetime.utcnow()
    target.last_update_utc_date_time = datetime.utcnow()
@event.listens_for(CustomerRole, 'before_update')
def set_updated_on(mapper, connection, target):
    target.last_update_utc_date_time = datetime.utcnow()