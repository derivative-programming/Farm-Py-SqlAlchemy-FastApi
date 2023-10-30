import uuid
from sqlalchemy import Index, event, BigInteger, Boolean, Column, DateTime, Float, Integer, Numeric, String, ForeignKey, Uuid, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from utils.common_functions import snake_case
Base = declarative_base()
class CustomerRole(Base):
    __tablename__ = snake_case('CustomerRole')
    customer_role_id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(UUID(as_uuid=True), unique=True, default=uuid.uuid4)
    last_change_code = Column(UUID(as_uuid=True))
    customer_id = Column(Integer, ForeignKey(snake_case('Customer') + '.id'))
    is_placeholder = Column(Boolean)
    placeholder = Column(Boolean)
    role_id = Column(Integer, ForeignKey(snake_case('Role') + '.id'))
    customer_code_peek = uuid.UUID #CustomerID
    role_code_peek = uuid.UUID #RoleID
    insert_utc_date_time = Column(DateTime, default=func.now())
    last_update_utc_date_time = Column(DateTime, onupdate=func.now())
    #no relationsip properties. they are not updated immediately if the id prop is updated directly
    # customer = relationship('Customer', back_populates=snake_case('Customer'))
    # flavor = relationship('Flavor', back_populates=snake_case('Flavor'))
    __mapper_args__ = {
        'version_id_col': last_change_code
    }
# Define the index separately from the column
Index('index_code', CustomerRole.code)
Index('index_customer_id', CustomerRole.customer_id) #CustomerID
Index('index_role_id', CustomerRole.role_id) #RoleID
@event.listens_for(CustomerRole, 'before_insert')
def set_created_on(mapper, connection, target):
    target.insert_utc_date_time = func.now()
@event.listens_for(CustomerRole, 'before_update')
def set_updated_on(mapper, connection, target):
    target.last_update_utc_date_time = func.now()
    target.last_change_code = uuid.uuid4()
