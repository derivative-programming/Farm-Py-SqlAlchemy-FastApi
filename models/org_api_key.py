import uuid
from sqlalchemy import Index, event, BigInteger, Boolean, Column, DateTime, Float, Integer, Numeric, String, ForeignKey, Uuid, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from utils.common_functions import snake_case
Base = declarative_base()
class OrgApiKey(Base):
    __tablename__ = snake_case('OrgApiKey')
    org_api_key_id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(UUID(as_uuid=True), unique=True, default=uuid.uuid4)
    last_change_code = Column(UUID(as_uuid=True))
    api_key_value = Column(String)
    created_by = Column(String)
    created_utc_date_time = Column(DateTime)
    expiration_utc_date_time = Column(DateTime)
    is_active = Column(Boolean)
    is_temp_user_key = Column(Boolean)
    name = Column(String)
    organization_id = Column(Integer, ForeignKey(snake_case('Organization') + '.id'))
    org_customer_id = Column(Integer, ForeignKey(snake_case('OrgCustomer') + '.id'))
    organization_code_peek = uuid.UUID #OrganizationID
    org_customer_code_peek = uuid.UUID #OrgCustomerID
    insert_utc_date_time = Column(DateTime, default=func.now())
    last_update_utc_date_time = Column(DateTime, onupdate=func.now())
    #no relationsip properties. they are not updated immediately if the id prop is updated directly
    # organization = relationship('Organization', back_populates=snake_case('Organization'))
    # flavor = relationship('Flavor', back_populates=snake_case('Flavor'))
    __mapper_args__ = {
        'version_id_col': last_change_code
    }
# Define the index separately from the column
Index('index_code', OrgApiKey.code)
Index('index_organization_id', OrgApiKey.organization_id) #OrganizationID
Index('index_org_customer_id', OrgApiKey.org_customer_id) #OrgCustomerID
@event.listens_for(OrgApiKey, 'before_insert')
def set_created_on(mapper, connection, target):
    target.insert_utc_date_time = func.now()
@event.listens_for(OrgApiKey, 'before_update')
def set_updated_on(mapper, connection, target):
    target.last_update_utc_date_time = func.now()
    target.last_change_code = uuid.uuid4()
