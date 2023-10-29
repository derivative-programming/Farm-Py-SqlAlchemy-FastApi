import uuid
from sqlalchemy import Index, event, BigInteger, Boolean, Column, DateTime, Float, Integer, Numeric, String, ForeignKey, Uuid, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from utils.common_functions import snake_case
Base = declarative_base()
class Customer(Base):
    __tablename__ = snake_case('Customer')
    id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(UUID(as_uuid=True), unique=True, default=uuid.uuid4)
    last_change_code = Column(UUID(as_uuid=True))
    active_organization_id = Column(Integer)
    email = Column(String)
    email_confirmed_utc_date_time = Column(DateTime)
    first_name = Column(String)
    forgot_password_key_expiration_utc_date_time = Column(DateTime)
    forgot_password_key_value = Column(String)
    fs_user_code_value = Column(UUID(as_uuid=True))
    is_active = Column(Boolean)
    is_email_allowed = Column(Boolean)
    is_email_confirmed = Column(Boolean)
    is_email_marketing_allowed = Column(Boolean)
    is_locked = Column(Boolean)
    is_multiple_organizations_allowed = Column(Boolean)
    is_verbose_logging_forced = Column(Boolean)
    last_login_utc_date_time = Column(DateTime)
    last_name = Column(String)
    password = Column(String)
    phone = Column(String)
    province = Column(String)
    registration_utc_date_time = Column(DateTime)
    tac_id = Column(Integer, ForeignKey(snake_case('Tac') + '.id'))
    utc_offset_in_minutes = Column(Integer)
    zip = Column(String)
    tac_code_peek = uuid.UUID #TacID
    insert_utc_date_time = Column(DateTime, default=func.now())
    last_update_utc_date_time = Column(DateTime, onupdate=func.now())
    #no relationsip properties. they are not updated immediately if the id prop is updated directly
    # tac = relationship('Tac', back_populates=snake_case('Tac'))
    # flavor = relationship('Flavor', back_populates=snake_case('Flavor'))
    __mapper_args__ = {
        'version_id_col': last_change_code
    }
# Define the index separately from the column
Index('index_code', Customer.code)
Index('index_tac_id', Customer.tac_id) #TacID
@event.listens_for(Customer, 'before_insert')
def set_created_on(mapper, connection, target):
    target.insert_utc_date_time = func.now()
@event.listens_for(Customer, 'before_update')
def set_updated_on(mapper, connection, target):
    target.last_update_utc_date_time = func.now()
    target.last_change_code = uuid.uuid4()
