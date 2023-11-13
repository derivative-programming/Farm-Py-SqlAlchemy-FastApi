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
import models.constants.customer as customer_constants
# Conditionally set the UUID column type
if db_dialect == 'postgresql':
    UUIDType = UUID(as_uuid=True)
elif db_dialect == 'mssql':
    UUIDType = UNIQUEIDENTIFIER
else:  # This will cover SQLite, MySQL, and other databases
    UUIDType = String(36)
class Customer(Base):
    __tablename__ = 'farm_' + snake_case('Customer')
    customer_id = Column('customer_id', Integer, primary_key=True, autoincrement=True)
    code = Column('code', UUIDType, unique=True, default=generate_uuid, nullable=True)
    last_change_code = Column('last_change_code', Integer, nullable=True)
    insert_user_id = Column('insert_user_id', UUIDType, default=generate_uuid, nullable=True)
    last_update_user_id = Column('last_update_user_id', UUIDType, default=generate_uuid, nullable=True)
    active_organization_id = Column('active_organization_id',
                          Integer,
                          default=0,
                                index=customer_constants.active_organization_id_calculatedIsDBColumnIndexed,
                          nullable=True)
    email = Column('email',
                                String,
                                default="",
                                index=customer_constants.email_calculatedIsDBColumnIndexed,
                                nullable=True)
    email_confirmed_utc_date_time = Column('email_confirmed_utc_date_time',
                                    DateTime,
                                    default=datetime(1753, 1, 1),
                                index=customer_constants.email_confirmed_utc_date_time_calculatedIsDBColumnIndexed,
                                    nullable=True)
    first_name = Column('first_name',
                          String,
                          default="",
                                index=customer_constants.first_name_calculatedIsDBColumnIndexed,
                          nullable=True)
    forgot_password_key_expiration_utc_date_time = Column('forgot_password_key_expiration_utc_date_time',
                                    DateTime,
                                    default=datetime(1753, 1, 1),
                                index=customer_constants.forgot_password_key_expiration_utc_date_time_calculatedIsDBColumnIndexed,
                                    nullable=True)
    forgot_password_key_value = Column('forgot_password_key_value',
                          String,
                          default="",
                                index=customer_constants.forgot_password_key_value_calculatedIsDBColumnIndexed,
                          nullable=True)
    fs_user_code_value = Column('fs_user_code_value',
                                       UUIDType,
                                       default=generate_uuid,
                                index=customer_constants.fs_user_code_value_calculatedIsDBColumnIndexed,
                                       nullable=True)
    is_active = Column('is_active',
                               Boolean,
                               default=False,
                                index=customer_constants.is_active_calculatedIsDBColumnIndexed,
                               nullable=True)
    is_email_allowed = Column('is_email_allowed',
                               Boolean,
                               default=False,
                                index=customer_constants.is_email_allowed_calculatedIsDBColumnIndexed,
                               nullable=True)
    is_email_confirmed = Column('is_email_confirmed',
                               Boolean,
                               default=False,
                                index=customer_constants.is_email_confirmed_calculatedIsDBColumnIndexed,
                               nullable=True)
    is_email_marketing_allowed = Column('is_email_marketing_allowed',
                               Boolean,
                               default=False,
                                index=customer_constants.is_email_marketing_allowed_calculatedIsDBColumnIndexed,
                               nullable=True)
    is_locked = Column('is_locked',
                               Boolean,
                               default=False,
                                index=customer_constants.is_locked_calculatedIsDBColumnIndexed,
                               nullable=True)
    is_multiple_organizations_allowed = Column('is_multiple_organizations_allowed',
                               Boolean,
                               default=False,
                                index=customer_constants.is_multiple_organizations_allowed_calculatedIsDBColumnIndexed,
                               nullable=True)
    is_verbose_logging_forced = Column('is_verbose_logging_forced',
                               Boolean,
                               default=False,
                                index=customer_constants.is_verbose_logging_forced_calculatedIsDBColumnIndexed,
                               nullable=True)
    last_login_utc_date_time = Column('last_login_utc_date_time',
                                    DateTime,
                                    default=datetime(1753, 1, 1),
                                index=customer_constants.last_login_utc_date_time_calculatedIsDBColumnIndexed,
                                    nullable=True)
    last_name = Column('last_name',
                          String,
                          default="",
                                index=customer_constants.last_name_calculatedIsDBColumnIndexed,
                          nullable=True)
    password = Column('password',
                          String,
                          default="",
                                index=customer_constants.password_calculatedIsDBColumnIndexed,
                          nullable=True)
    phone = Column('phone',
                               String,
                               default="",
                                index=customer_constants.phone_calculatedIsDBColumnIndexed,
                               nullable=True)
    province = Column('province',
                          String,
                          default="",
                                index=customer_constants.province_calculatedIsDBColumnIndexed,
                          nullable=True)
    registration_utc_date_time = Column('registration_utc_date_time',
                                    DateTime,
                                    default=datetime(1753, 1, 1),
                                index=customer_constants.registration_utc_date_time_calculatedIsDBColumnIndexed,
                                    nullable=True)
    tac_id = Column('tac_id',
                     Integer,
                     ForeignKey('farm_' + snake_case('Tac') + '.tac_id'),
                     index=customer_constants.tac_id_calculatedIsDBColumnIndexed,
                     nullable=True)
    utc_offset_in_minutes = Column('utc_offset_in_minutes',
                          Integer,
                          default=0,
                                index=customer_constants.utc_offset_in_minutes_calculatedIsDBColumnIndexed,
                          nullable=True)
    zip = Column('zip',
                          String,
                          default="",
                                index=customer_constants.zip_calculatedIsDBColumnIndexed,
                          nullable=True)
    tac_code_peek = UUIDType # TacID
    insert_utc_date_time = Column('insert_utc_date_time', DateTime, nullable=True)
    last_update_utc_date_time = Column('last_update_utc_date_time', DateTime, nullable=True)
    #no relationsip properties. they are not updated immediately if the id prop is updated directly
    # tac = relationship('Tac', back_populates=snake_case('Tac'))
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
        self.active_organization_id = kwargs.get('active_organization_id', 0)
        self.email = kwargs.get('email', "")
        self.email_confirmed_utc_date_time = kwargs.get('email_confirmed_utc_date_time', datetime(1753, 1, 1))
        self.first_name = kwargs.get('first_name', "")
        self.forgot_password_key_expiration_utc_date_time = kwargs.get('forgot_password_key_expiration_utc_date_time', datetime(1753, 1, 1))
        self.forgot_password_key_value = kwargs.get('forgot_password_key_value', "")
        self.fs_user_code_value = kwargs.get('fs_user_code_value', generate_uuid())
        self.is_active = kwargs.get('is_active', False)
        self.is_email_allowed = kwargs.get('is_email_allowed', False)
        self.is_email_confirmed = kwargs.get('is_email_confirmed', False)
        self.is_email_marketing_allowed = kwargs.get('is_email_marketing_allowed', False)
        self.is_locked = kwargs.get('is_locked', False)
        self.is_multiple_organizations_allowed = kwargs.get('is_multiple_organizations_allowed', False)
        self.is_verbose_logging_forced = kwargs.get('is_verbose_logging_forced', False)
        self.last_login_utc_date_time = kwargs.get('last_login_utc_date_time', datetime(1753, 1, 1))
        self.last_name = kwargs.get('last_name', "")
        self.password = kwargs.get('password', "")
        self.phone = kwargs.get('phone', "")
        self.province = kwargs.get('province', "")
        self.registration_utc_date_time = kwargs.get('registration_utc_date_time', datetime(1753, 1, 1))
        self.tac_id = kwargs.get('tac_id', 0)
        self.utc_offset_in_minutes = kwargs.get('utc_offset_in_minutes', 0)
        self.zip = kwargs.get('zip', "")
        self.insert_utc_date_time = kwargs.get('insert_utc_date_time', datetime(1753, 1, 1))
        self.last_update_utc_date_time = kwargs.get('last_update_utc_date_time', datetime(1753, 1, 1))

        self.tac_code_peek = kwargs.get('tac_code_peek', generate_uuid())# TacID

# Define the index separately from the column
# Index('index_code', Customer.code)
# Index('farm_customer_index_tac_id', Customer.tac_id) #TacID
@event.listens_for(Customer, 'before_insert')
def set_created_on(mapper, connection, target):
    target.insert_utc_date_time = datetime.utcnow()
    target.last_update_utc_date_time = datetime.utcnow()
@event.listens_for(Customer, 'before_update')
def set_updated_on(mapper, connection, target):
    target.last_update_utc_date_time = datetime.utcnow()
