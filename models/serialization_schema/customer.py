# customer.py
"""
    #TODO add comment
"""
from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
from models import Customer
from services.db_config import DB_DIALECT
# Conditionally set the UUID column type
if DB_DIALECT == 'postgresql':
    schema_UUIDType = fields.UUID()
elif DB_DIALECT == 'mssql':
    schema_UUIDType = UNIQUEIDENTIFIER
else:  # This will cover SQLite, MySQL, and other databases
    schema_UUIDType = fields.Str()
class CustomerSchema(SQLAlchemyAutoSchema):
    """
    #TODO add comment
    """
    class Meta:
        model = Customer
    customer_id = fields.Int()
    code = schema_UUIDType
    last_change_code = fields.Int()
    insert_user_id = schema_UUIDType
    last_update_user_id = schema_UUIDType
    active_organization_id = fields.Int()
    email = fields.Str()
    email_confirmed_utc_date_time = fields.DateTime()  # (format="%Y-%m-%dT%H:%M:%S")
    first_name = fields.Str()
    forgot_password_key_expiration_utc_date_time = fields.DateTime()  # (format="%Y-%m-%dT%H:%M:%S")
    forgot_password_key_value = fields.Str()
    fs_user_code_value = schema_UUIDType
    is_active = fields.Bool()
    is_email_allowed = fields.Bool()
    is_email_confirmed = fields.Bool()
    is_email_marketing_allowed = fields.Bool()
    is_locked = fields.Bool()
    is_multiple_organizations_allowed = fields.Bool()
    is_verbose_logging_forced = fields.Bool()
    last_login_utc_date_time = fields.DateTime()  # (format="%Y-%m-%dT%H:%M:%S")
    last_name = fields.Str()
    password = fields.Str()
    phone = fields.Str()
    province = fields.Str()
    registration_utc_date_time = fields.DateTime()  # (format="%Y-%m-%dT%H:%M:%S")
    tac_id = fields.Int()
    utc_offset_in_minutes = fields.Int()
    zip = fields.Str()
    insert_utc_date_time = fields.DateTime()
    last_update_utc_date_time = fields.DateTime()
    tac_code_peek = schema_UUIDType  # TacID
# endset
