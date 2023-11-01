from datetime import datetime
from marshmallow import Schema, fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from sqlalchemy import Index, event, BigInteger, Boolean, Column, DateTime, Float, Integer, Numeric, String, ForeignKey, Uuid, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm.attributes import InstrumentedAttribute
from sqlalchemy.ext.hybrid import hybrid_property
from utils.common_functions import snake_case
from ..base import Base  # Importing the Base from central module
from models import Customer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
from services.db_config import db_dialect,generate_uuid
# Conditionally set the UUID column type
if db_dialect == 'postgresql':
    schema_UUIDType = fields.UUID()
elif db_dialect == 'mssql':
    schema_UUIDType = UNIQUEIDENTIFIER
else:  # This will cover SQLite, MySQL, and other databases
    schema_UUIDType = fields.Str()
class CustomerSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Customer
    customer_id = fields.Int()
    code = schema_UUIDType
    last_change_code = fields.Int()
    insert_user_id = schema_UUIDType
    last_update_user_id = schema_UUIDType
    active_organization_id = fields.Int()
    email = fields.Str()
    email_confirmed_utc_date_time = fields.DateTime()#(format="%Y-%m-%dT%H:%M:%S")
    first_name = fields.Str()
    forgot_password_key_expiration_utc_date_time = fields.DateTime()#(format="%Y-%m-%dT%H:%M:%S")
    forgot_password_key_value = fields.Str()
    fs_user_code_value = schema_UUIDType
    is_active = fields.Bool()
    is_email_allowed = fields.Bool()
    is_email_confirmed = fields.Bool()
    is_email_marketing_allowed = fields.Bool()
    is_locked = fields.Bool()
    is_multiple_organizations_allowed = fields.Bool()
    is_verbose_logging_forced = fields.Bool()
    last_login_utc_date_time = fields.DateTime()#(format="%Y-%m-%dT%H:%M:%S")
    last_name = fields.Str()
    password = fields.Str()
    phone = fields.Str()
    province = fields.Str()
    registration_utc_date_time = fields.DateTime()#(format="%Y-%m-%dT%H:%M:%S")
    tac_id = fields.Int()
    utc_offset_in_minutes = fields.Int()
    zip = fields.Str()
    insert_utc_date_time = fields.DateTime()
    last_update_utc_date_time = fields.DateTime()
    tac_code_peek = schema_UUIDType #TacID

