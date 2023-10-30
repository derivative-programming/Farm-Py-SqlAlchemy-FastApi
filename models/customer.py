from datetime import datetime
import uuid
from sqlalchemy import Index, event, BigInteger, Boolean, Column, DateTime, Float, Integer, Numeric, String, ForeignKey, Uuid, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from utils.common_functions import snake_case
from .base import Base  # Importing the Base from central module
class Customer(Base):
    __tablename__ = snake_case('Customer')
    customer_id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(UUID(as_uuid=True), unique=True, default=uuid.uuid4, nullable=True)
    last_change_code = Column(UUID(as_uuid=True), default=uuid.uuid4, nullable=True)
    insert_user_id = Column(UUID(as_uuid=True), default=uuid.uuid4, nullable=True)
    last_update_user_id = Column(UUID(as_uuid=True), default=uuid.uuid4, nullable=True)
    active_organization_id = Column(Integer, default=0, nullable=True)
    email = Column(String, default="", nullable=True)
    email_confirmed_utc_date_time = Column(DateTime, default=datetime(1753, 1, 1), nullable=True)
    first_name = Column(String, default="", nullable=True)
    forgot_password_key_expiration_utc_date_time = Column(DateTime, default=datetime(1753, 1, 1), nullable=True)
    forgot_password_key_value = Column(String, default="", nullable=True)
    fs_user_code_value = Column(UUID(as_uuid=True), nullable=True)
    is_active = Column(Boolean, default=False, nullable=True)
    is_email_allowed = Column(Boolean, default=False, nullable=True)
    is_email_confirmed = Column(Boolean, default=False, nullable=True)
    is_email_marketing_allowed = Column(Boolean, default=False, nullable=True)
    is_locked = Column(Boolean, default=False, nullable=True)
    is_multiple_organizations_allowed = Column(Boolean, default=False, nullable=True)
    is_verbose_logging_forced = Column(Boolean, default=False, nullable=True)
    last_login_utc_date_time = Column(DateTime, default=datetime(1753, 1, 1), nullable=True)
    last_name = Column(String, default="", nullable=True)
    password = Column(String, default="", nullable=True)
    phone = Column(String, default="", nullable=True)
    province = Column(String, default="", nullable=True)
    registration_utc_date_time = Column(DateTime, default=datetime(1753, 1, 1), nullable=True)
    tac_id = Column(Integer, ForeignKey(snake_case('Tac') + '.id'), nullable=True)
    utc_offset_in_minutes = Column(Integer, default=0, nullable=True)
    zip = Column(String, default="", nullable=True)
    tac_code_peek = uuid.UUID  # TacID
    insert_utc_date_time = Column(DateTime, default=func.now(), nullable=True)
    last_update_utc_date_time = Column(DateTime, onupdate=func.now(), nullable=True)
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
    target.last_update_utc_date_time = func.now()
@event.listens_for(Customer, 'before_update')
def set_updated_on(mapper, connection, target):
    target.last_update_utc_date_time = func.now()
    target.last_change_code = uuid.uuid4()
