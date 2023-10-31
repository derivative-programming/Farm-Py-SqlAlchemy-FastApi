from datetime import datetime
from sqlalchemy import Index, event, BigInteger, Boolean, Column, DateTime, Float, Integer, Numeric, String, ForeignKey, Uuid, func
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
class Customer(Base):
    __tablename__ = snake_case('Customer')
    customer_id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(UUIDType, unique=True, default=generate_uuid, nullable=True)
    last_change_code = Column(Integer, nullable=True)
    insert_user_id = Column(UUIDType, default=generate_uuid, nullable=True)
    last_update_user_id = Column(UUIDType, default=generate_uuid, nullable=True)
    active_organization_id = Column(Integer, default=0, nullable=True)
    email = Column(String, default="", nullable=True)
    email_confirmed_utc_date_time = Column(DateTime, default=datetime(1753, 1, 1), nullable=True)
    first_name = Column(String, default="", nullable=True)
    forgot_password_key_expiration_utc_date_time = Column(DateTime, default=datetime(1753, 1, 1), nullable=True)
    forgot_password_key_value = Column(String, default="", nullable=True)
    fs_user_code_value = Column(UUIDType, default=generate_uuid,  nullable=True)
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
    tac_id = Column(Integer, ForeignKey(snake_case('Tac') + '.tac_id'), nullable=True)
    utc_offset_in_minutes = Column(Integer, default=0, nullable=True)
    zip = Column(String, default="", nullable=True)
    tac_code_peek = UUIDType # TacID
    insert_utc_date_time = Column(DateTime, nullable=True)
    last_update_utc_date_time = Column(DateTime, nullable=True)
    #no relationsip properties. they are not updated immediately if the id prop is updated directly
    # tac = relationship('Tac', back_populates=snake_case('Tac'))
    # flavor = relationship('Flavor', back_populates=snake_case('Flavor'))
    __mapper_args__ = {
        'version_id_col': last_change_code
    }
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # self.customer_id = 0
        self.code = generate_uuid()
        self.last_change_code = 0
        insert_user_id = None
        last_update_user_id = None
        self.active_organization_id = 0
        self.email = ""
        self.email_confirmed_utc_date_time = datetime(1753, 1, 1)
        self.first_name = ""
        self.forgot_password_key_expiration_utc_date_time = datetime(1753, 1, 1)
        self.forgot_password_key_value = ""
        self.fs_user_code_value = generate_uuid()
        self.is_active = False
        self.is_email_allowed = False
        self.is_email_confirmed = False
        self.is_email_marketing_allowed = False
        self.is_locked = False
        self.is_multiple_organizations_allowed = False
        self.is_verbose_logging_forced = False
        self.last_login_utc_date_time = datetime(1753, 1, 1)
        self.last_name = ""
        self.password = ""
        self.phone =  ""
        self.province = ""
        self.registration_utc_date_time = datetime(1753, 1, 1)
        self.tac_id = 0
        self.utc_offset_in_minutes = 0
        self.zip = ""
        self.insert_utc_date_time = datetime(1753, 1, 1)
        self.last_update_utc_date_time = datetime(1753, 1, 1)
        self.tac_code_peek = generate_uuid() # TacID
# Define the index separately from the column
# Index('index_code', Customer.code)
Index('customer_index_tac_id', Customer.tac_id) #TacID
@event.listens_for(Customer, 'before_insert')
def set_created_on(mapper, connection, target):
    target.insert_utc_date_time = func.now()
    target.last_update_utc_date_time = func.now()
@event.listens_for(Customer, 'before_update')
def set_updated_on(mapper, connection, target):
    target.last_update_utc_date_time = func.now()
