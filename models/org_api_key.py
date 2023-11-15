from datetime import datetime, date
from marshmallow import Schema, fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from sqlalchemy import Index, event, BigInteger, Boolean, Column, Date, DateTime, Float, Integer, Numeric, String, ForeignKey, Uuid, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm.attributes import InstrumentedAttribute
from sqlalchemy.ext.hybrid import hybrid_property
from utils.common_functions import snake_case
from .base import Base,EncryptedType  # Importing the Base from central module
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
from services.db_config import db_dialect,generate_uuid
import models.constants.org_api_key as org_api_key_constants
# Conditionally set the UUID column type
if db_dialect == 'postgresql':
    UUIDType = UUID(as_uuid=True)
elif db_dialect == 'mssql':
    UUIDType = UNIQUEIDENTIFIER
else:  # This will cover SQLite, MySQL, and other databases
    UUIDType = String(36)
class OrgApiKey(Base):
    __tablename__ = 'farm_' + snake_case('OrgApiKey')
    org_api_key_id = Column('org_api_key_id', Integer, primary_key=True, autoincrement=True)
    code = Column('code', UUIDType, unique=True, default=generate_uuid, nullable=True)
    last_change_code = Column('last_change_code', Integer, nullable=True)
    insert_user_id = Column('insert_user_id', UUIDType, default=generate_uuid, nullable=True)
    last_update_user_id = Column('last_update_user_id', UUIDType, default=generate_uuid, nullable=True)
    api_key_value = Column('api_key_value',
                            String,
                          default="",
                                index=org_api_key_constants.api_key_value_calculatedIsDBColumnIndexed,
                          nullable=True)
    created_by = Column('created_by',
                            String,
                          default="",
                                index=org_api_key_constants.created_by_calculatedIsDBColumnIndexed,
                          nullable=True)
    created_utc_date_time = Column('created_utc_date_time',
                                    DateTime,
                                    default=datetime(1753, 1, 1),
                                index=org_api_key_constants.created_utc_date_time_calculatedIsDBColumnIndexed,
                                    nullable=True)
    expiration_utc_date_time = Column('expiration_utc_date_time',
                                    DateTime,
                                    default=datetime(1753, 1, 1),
                                index=org_api_key_constants.expiration_utc_date_time_calculatedIsDBColumnIndexed,
                                    nullable=True)
    is_active = Column('is_active',
                               Boolean,
                               default=False,
                                index=org_api_key_constants.is_active_calculatedIsDBColumnIndexed,
                               nullable=True)
    is_temp_user_key = Column('is_temp_user_key',
                               Boolean,
                               default=False,
                                index=org_api_key_constants.is_temp_user_key_calculatedIsDBColumnIndexed,
                               nullable=True)
    name = Column('name',
                            String,
                          default="",
                                index=org_api_key_constants.name_calculatedIsDBColumnIndexed,
                          nullable=True)
    organization_id = Column('organization_id',
                     Integer,
                     ForeignKey('farm_' + snake_case('Organization') + '.organization_id'),
                     index=org_api_key_constants.organization_id_calculatedIsDBColumnIndexed,
                     nullable=True)
    org_customer_id = Column('org_customer_id',
                                 Integer,
                                 ForeignKey('farm_' + snake_case('OrgCustomer') + '.org_customer_id'),
                                index=org_api_key_constants.org_customer_id_calculatedIsDBColumnIndexed,
                                 nullable=True)
    organization_code_peek = UUIDType # OrganizationID
    org_customer_code_peek = UUIDType  # OrgCustomerID
    insert_utc_date_time = Column('insert_utc_date_time', DateTime, nullable=True)
    last_update_utc_date_time = Column('last_update_utc_date_time', DateTime, nullable=True)
    #no relationsip properties. they are not updated immediately if the id prop is updated directly
    # organization = relationship('Organization', back_populates=snake_case('Organization'))
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
        self.api_key_value = kwargs.get('api_key_value', "")
        self.created_by = kwargs.get('created_by', "")
        self.created_utc_date_time = kwargs.get('created_utc_date_time', datetime(1753, 1, 1))
        self.expiration_utc_date_time = kwargs.get('expiration_utc_date_time', datetime(1753, 1, 1))
        self.is_active = kwargs.get('is_active', False)
        self.is_temp_user_key = kwargs.get('is_temp_user_key', False)
        self.name = kwargs.get('name', "")
        self.organization_id = kwargs.get('organization_id', 0)
        self.org_customer_id = kwargs.get('org_customer_id', 0)
        self.insert_utc_date_time = kwargs.get('insert_utc_date_time', datetime(1753, 1, 1))
        self.last_update_utc_date_time = kwargs.get('last_update_utc_date_time', datetime(1753, 1, 1))

        self.organization_code_peek = kwargs.get('organization_code_peek', generate_uuid())# OrganizationID
        self.org_customer_code_peek = kwargs.get('org_customer_code_peek', generate_uuid()) # OrgCustomerID

# Define the index separately from the column
# Index('index_code', OrgApiKey.code)
# Index('farm_org_api_key_index_organization_id', OrgApiKey.organization_id) #OrganizationID
# Index('farm_org_api_key_index_org_customer_id', OrgApiKey.org_customer_id) #OrgCustomerID
@event.listens_for(OrgApiKey, 'before_insert')
def set_created_on(mapper, connection, target):
    target.insert_utc_date_time = datetime.utcnow()
    target.last_update_utc_date_time = datetime.utcnow()
@event.listens_for(OrgApiKey, 'before_update')
def set_updated_on(mapper, connection, target):
    target.last_update_utc_date_time = datetime.utcnow()
