import uuid
from sqlalchemy import Index, event, BigInteger, Boolean, Column, DateTime, Float, Integer, Numeric, String, ForeignKey, Uuid, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from utils.common_functions import snake_case
Base = declarative_base()
class OrgCustomer(Base):
    __tablename__ = snake_case('OrgCustomer')
    org_customer_id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(UUID(as_uuid=True), unique=True, default=uuid.uuid4)
    last_change_code = Column(UUID(as_uuid=True))
    customer_id = Column(Integer, ForeignKey(snake_case('Customer') + '.id'))
    email = Column(String)
    organization_id = Column(Integer, ForeignKey(snake_case('Organization') + '.id'))
    customer_code_peek = uuid.UUID #CustomerID
    organization_code_peek = uuid.UUID #OrganizationID
    insert_utc_date_time = Column(DateTime, default=func.now())
    last_update_utc_date_time = Column(DateTime, onupdate=func.now())
    #no relationsip properties. they are not updated immediately if the id prop is updated directly
    # organization = relationship('Organization', back_populates=snake_case('Organization'))
    # flavor = relationship('Flavor', back_populates=snake_case('Flavor'))
    __mapper_args__ = {
        'version_id_col': last_change_code
    }
# Define the index separately from the column
Index('index_code', OrgCustomer.code)
Index('index_customer_id', OrgCustomer.customer_id) #CustomerID
Index('index_organization_id', OrgCustomer.organization_id) #OrganizationID
@event.listens_for(OrgCustomer, 'before_insert')
def set_created_on(mapper, connection, target):
    target.insert_utc_date_time = func.now()
@event.listens_for(OrgCustomer, 'before_update')
def set_updated_on(mapper, connection, target):
    target.last_update_utc_date_time = func.now()
    target.last_change_code = uuid.uuid4()
