from datetime import datetime, date
from marshmallow import Schema, fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from sqlalchemy import Index, event, BigInteger, Boolean, Column, Date, DateTime, Float, Integer, Numeric, String, ForeignKey, Uuid, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm.attributes import InstrumentedAttribute
from sqlalchemy.ext.hybrid import hybrid_property
from utils.common_functions import snake_case
from .base import Base,EncryptedType  # Importing the Base from central module
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
from services.db_config import db_dialect,generate_uuid
import models.constants.org_customer as org_customer_constants
# Conditionally set the UUID column type
if db_dialect == 'postgresql':
    UUIDType = UUID(as_uuid=True)
elif db_dialect == 'mssql':
    UUIDType = UNIQUEIDENTIFIER
else:  # This will cover SQLite, MySQL, and other databases
    UUIDType = String(36)
class OrgCustomer(Base):
    __tablename__ = 'farm_' + snake_case('OrgCustomer')
    org_customer_id = Column('org_customer_id', Integer, primary_key=True, autoincrement=True)
    code = Column('code', UUIDType, unique=True, default=generate_uuid, nullable=True)
    last_change_code = Column('last_change_code', Integer, nullable=True)
    insert_user_id = Column('insert_user_id', UUIDType, default=generate_uuid, nullable=True)
    last_update_user_id = Column('last_update_user_id', UUIDType, default=generate_uuid, nullable=True)
    customer_id = Column('customer_id',
                                 Integer,
                                 ForeignKey('farm_' + snake_case('Customer') + '.customer_id'),
                                index=org_customer_constants.customer_id_calculatedIsDBColumnIndexed,
                                 nullable=True)
    email = Column('email',
                                 String,
                                default="",
                                index=org_customer_constants.email_calculatedIsDBColumnIndexed,
                                nullable=True)
    organization_id = Column('organization_id',
                     Integer,
                     ForeignKey('farm_' + snake_case('Organization') + '.organization_id'),
                     index=org_customer_constants.organization_id_calculatedIsDBColumnIndexed,
                     nullable=True)
    customer_code_peek = UUIDType  # CustomerID
    organization_code_peek = UUIDType # OrganizationID
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
        self.customer_id = kwargs.get('customer_id', 0)
        self.email = kwargs.get('email', "")
        self.organization_id = kwargs.get('organization_id', 0)
        self.insert_utc_date_time = kwargs.get('insert_utc_date_time', datetime(1753, 1, 1))
        self.last_update_utc_date_time = kwargs.get('last_update_utc_date_time', datetime(1753, 1, 1))

        self.customer_code_peek = kwargs.get('customer_code_peek', generate_uuid()) # CustomerID
        self.organization_code_peek = kwargs.get('organization_code_peek', generate_uuid())# OrganizationID

    @staticmethod
    def property_list():
        result = [
            "customer_id",
            "email",
            "organization_id",

            "code"
            ]
        return result
# Define the index separately from the column
# Index('index_code', OrgCustomer.code)
# Index('farm_org_customer_index_customer_id', OrgCustomer.customer_id) #CustomerID
# Index('farm_org_customer_index_organization_id', OrgCustomer.organization_id) #OrganizationID
@event.listens_for(OrgCustomer, 'before_insert')
def set_created_on(mapper, connection, target):
    target.insert_utc_date_time = datetime.utcnow()
    target.last_update_utc_date_time = datetime.utcnow()
@event.listens_for(OrgCustomer, 'before_update')
def set_updated_on(mapper, connection, target):
    target.last_update_utc_date_time = datetime.utcnow()
